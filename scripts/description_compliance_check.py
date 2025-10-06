#!/usr/bin/env python3
import os
import re
import yaml
import sys
import argparse
from pathlib import Path
from collections import defaultdict

OUTPUT_PATH = Path("project/reports/DESCRIPTION_COMPLIANCE_REPORT.md")
TRACE_INDEX_PATH = Path("project/reports/TRACE_INDEX.yml")

def load_trace_index_data():
    """Loads all file paths and their descriptions from the TRACE_INDEX."""
    with open(TRACE_INDEX_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f).get('artifacts', [])

    master_descriptions = {}
    exempt_files = []

    for item in data:
        path = item.get('path')
        if not path:
            continue

        if item.get('type') == 'exempt' or item.get('registered') == 'exempted':
            exempt_files.append(path)
        elif item.get('registered') is True and 'index' in item and item['index'] != '-':
            master_descriptions[path] = {
                "description": item.get('description', '').strip(),
                "index_file": item['index']
            }

    return master_descriptions, exempt_files

def parse_unified_md_index(index_path_str):
    """Parses the new, unified markdown table format."""
    found_in_index = {}
    index_path = Path(index_path_str)

    if not index_path.exists():
        return {}

    with open(index_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if not line.strip().startswith('|'):
            continue

        cols = [c.strip() for c in line.split('|')]
        if len(cols) < 3: # | `path` | description |
            continue

        path_match = re.search(r'`([^`]+)`', cols[1])
        if path_match:
            file_path = path_match.group(1)
            description = cols[2]
            found_in_index[file_path] = description.strip()

    return found_in_index

def main():
    parser = argparse.ArgumentParser(description="Validates that all registered files have descriptions in their respective indices.")
    parser.add_argument("--validate", action="store_true", help="Run the validation process.")
    args = parser.parse_args()

    if not args.validate:
        print("Script requires the --validate flag to run.", file=sys.stderr)
        sys.exit(0)

    master_descriptions, exempt_files = load_trace_index_data()

    report_lines = [
        "# Description Compliance Report\n",
        "| File | Registered In | Status | Notes |",
        "|------|----------------|--------|-------|",
    ]

    valid_count = 0
    missing_count = 0

    all_found_descriptions = {}
    all_indices = set(v['index_file'] for v in master_descriptions.values())
    for index_file in all_indices:
        all_found_descriptions.update(parse_unified_md_index(index_file))

    for file_path, data in sorted(master_descriptions.items()):
        index_file = data['index_file']
        master_desc = data['description']

        status = "✅ Valid"
        notes = "Description present"

        if file_path not in all_found_descriptions:
            status = "⚠️ Missing"
            notes = "File not found in its registered index."
            missing_count += 1
        else:
            found_desc = all_found_descriptions[file_path]
            if not found_desc or found_desc.lower() in ["tbd", "n/a", ""]:
                status = "⚠️ Missing"
                notes = "Description is missing or a placeholder in the index file."
                missing_count += 1
            elif found_desc != master_desc:
                status = "⚠️ Mismatched"
                notes = f"Description does not match master. Expected: '{master_desc}', Found: '{found_desc}'"
                missing_count += 1
            else:
                valid_count += 1

        report_lines.append(f"| `{file_path}` | `{index_file}` | {status} | {notes} |")

    total_checked = len(master_descriptions)
    compliance_rate = 100
    if total_checked > 0:
        compliance_rate = int((valid_count / total_checked) * 100)

    summary = [
        "\n## Summary\n",
        f"**Total files checked:** {total_checked}",
        f"**Valid:** {valid_count}",
        f"**Missing/Mismatched:** {missing_count}",
        f"**Exempt:** {len(exempt_files)}",
        f"**Overall compliance:** {compliance_rate}%"
    ]

    report_lines.extend(summary)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Compliance report generated at {OUTPUT_PATH}")
    if missing_count > 0:
        print(f"Found {missing_count} non-compliant entries.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All checked files are compliant.")

if __name__ == "__main__":
    main()