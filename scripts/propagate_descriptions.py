# ID: OPS-023
#!/usr/bin/env python3
import os
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

TRACE_INDEX_PATH = Path("project/reports/TRACE_INDEX.yml")

def load_master_data():
    """Loads all file paths, their descriptions, and their target index files from TRACE_INDEX.yml."""
    with open(TRACE_INDEX_PATH, 'r', encoding='utf-8') as f:
        trace_index = yaml.safe_load(f)

    files_by_index = defaultdict(list)
    for item in trace_index.get('artifacts', []):
        if item.get('type') != 'exempt' and 'index' in item and item.get('registered') and item['index'] != '-':
            files_by_index[item['index']].append({
                "path": item['path'],
                "description": item.get('description', '').strip(),
                "type": item.get('type', 'N/A')
            })
    return files_by_index

def regenerate_index_file(index_path_str, files_in_index, apply_changes=False):
    """Regenerates an entire index file from scratch with a unified table format."""
    index_path = Path(index_path_str)

    if not apply_changes:
        print(f"--- (Dry Run) Would regenerate {index_path} with {len(files_in_index)} entries ---")
        return

    print(f"--- Regenerating {index_path} ---")

    # Unified Header for ALL index files
    header = [
        f"# {index_path.stem.replace('_', ' ').title()}",
        "",
        "This file is auto-generated. Do not edit manually.",
        "",
        "| Path | Description |",
        "|------|-------------|",
    ]

    new_lines = header

    for file_info in sorted(files_in_index, key=lambda x: x['path']):
        path = file_info['path']
        desc = file_info['description']
        new_lines.append(f"| `{path}` | {desc} |")

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text("\n".join(new_lines) + "\n", encoding='utf-8')
    print(f"✅ Successfully regenerated {index_path} with {len(files_in_index)} entries.")

def main():
    parser = argparse.ArgumentParser(description="Regenerates all index files with a unified format from TRACE_INDEX.yml.")
    parser.add_argument("--apply", action="store_true", help="Apply the changes to the files. Without this flag, it runs in dry-run mode.")
    args = parser.parse_args()

    if not args.apply:
        print("--- Running in DRY-RUN mode. No files will be changed. Use --apply to write changes. ---")

    files_by_index = load_master_data()

    for index_file, files in files_by_index.items():
        regenerate_index_file(index_file, files, args.apply)

    print("\n--- Propagation complete. ---")

if __name__ == "__main__":
    main()