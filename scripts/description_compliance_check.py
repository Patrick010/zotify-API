#!/usr/bin/env python3
import os
import re
import yaml
import sys

OUTPUT_PATH = "reports/description_compliance_report.md"
TRACE_INDEX_PATH = 'project/reports/TRACE_INDEX.yml'

def get_master_descriptions(trace_index_path):
    """
    Loads descriptions from the master TRACE_INDEX.yml file for non-exempt artifacts.
    """
    with open(trace_index_path, 'r', encoding='utf-8') as f:
        trace_index = yaml.safe_load(f)

    description_map = {}
    for item in trace_index.get('artifacts', []):
        if item.get('type') != 'exempt':
            description_map[item['path']] = item.get('description', '').strip()

    return description_map

def check_md_index(index_path, master_descriptions):
    """
    Checks a markdown index file against the master descriptions.
    """
    results = []
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return [(index_path, "File not found", "⚠️ Missing", "The index file itself is missing.")]

    header_found = False
    headers = []
    for line in lines:
        if not header_found:
            if re.match(r'\|.*Path.*\|', line):
                header_found = True
                headers = [h.strip().lower() for h in line.split('|') if h.strip()]
            continue

        if re.match(r'^\|-.*\|$', line.strip()):
            continue

        if re.match(r'^\|.*\|$', line.strip()):
            cols = [c.strip() for c in line.strip().split('|')][1:-1]
            if len(cols) < 1:
                continue

            path_match = re.search(r'`([^`]+)`', cols[0])
            file_path = path_match.group(1) if path_match else cols[0]

            if file_path not in master_descriptions:
                continue # Skip files not in the master index (or exempt)

            try:
                desc_index = headers.index('description')
                current_desc = cols[desc_index].strip() if desc_index < len(cols) else ""
                master_desc = master_descriptions[file_path]

                status = "✅ Valid"
                notes = ""
                if not current_desc:
                    status = "⚠️ Missing"
                    notes = "Description is missing from index file."
                elif current_desc != master_desc:
                    status = "⚠️ Mismatched"
                    notes = f"Description does not match master. Expected: '{master_desc}'"

                results.append((file_path, index_path, status, notes))

            except ValueError:
                results.append((file_path, index_path, "⚠️ Missing", "Could not find 'Description' column in table."))
                break # Stop processing this file if header is broken

    return results

def find_all_indices():
    """Finds all CODE_FILE_INDEX.md and PROJECT_REGISTRY.md files."""
    index_files = []
    for root, _, files in os.walk("."):
        for file in files:
            if file in ["CODE_FILE_INDEX.md", "PROJECT_REGISTRY.md"]:
                index_files.append(os.path.join(root, file))
    return index_files

def main():
    """
    Main function to run the compliance check and generate the report.
    """
    master_descriptions = get_master_descriptions(TRACE_INDEX_PATH)
    all_indices = find_all_indices()

    all_results = []
    for index_path in all_indices:
        all_results.extend(check_md_index(index_path, master_descriptions))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Description Compliance Report\n\n")
        f.write("| File | Index | Status | Notes |\n")
        f.write("|------|-------|--------|-------|\n")

        for file_path, index, status, notes in sorted(all_results):
            f.write(f"| `{file_path}` | `{index}` | {status} | {notes} |\n")

        total = len(all_results)
        non_compliant = sum(1 for _, _, s, _ in all_results if "⚠️" in s)
        compliance = 100
        if total > 0:
            compliance = int(((total - non_compliant) / total) * 100)

        f.write(f"\n**Total entries checked:** {total}\n")
        f.write(f"**Non-compliant entries:** {non_compliant}\n")
        f.write(f"**Overall compliance:** {compliance}%\n")

    print(f"Compliance report generated at {OUTPUT_PATH}")
    if non_compliant > 0:
        print(f"Found {non_compliant} non-compliant entries.")
        # sys.exit(1) # We won't fail the build for now, just report.
    else:
        print("All checked files are compliant.")

if __name__ == "__main__":
    main()