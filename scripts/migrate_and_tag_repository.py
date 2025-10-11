# ID: OPS-021
#!/usr/bin/env python3
"""
migrate_and_tag_repository.py

Scans the entire repository, applies unique, file-type-aware ID tags to all
relevant files, and generates a comprehensive inventory. This script is the
first step in the two-tier document and task alignment system migration.

It supports three modes of operation:
  --dry-run:  Prints the actions it would take without modifying any files.
  --apply:    Applies the ID tags to files and generates the inventory.
  --validate: Checks existing tags for syntax, uniqueness, and completeness.
"""

import os
import yaml
import argparse
import re
from pathlib import Path

# --- Configuration ---

# Directories to completely exclude from scanning
EXCLUDE_DIRS = {
    '.git', '.github', '.pytest_cache', '.ruff_cache', '.mypy_cache', '.tox',
    '__pycache__', 'node_modules', 'vendor', 'api_dumps', 'storage',
    'templates', 'venv'
}

# Files to exclude from scanning
EXCLUDE_FILES = {'openapi.json'}

# Deterministic mapping of directory paths to ID prefixes
PREFIX_MAPPING = {
    'api': 'API',
    'project': 'DOC',
    'scripts': 'OPS',
    'Gonk': 'API',
    'snitch': 'API',
    'docs': 'DOC',
    'tests': 'TEST',
}

# Mapping of file extensions to their comment syntax for the ID tag
COMMENT_STYLE_MAP = {
    '.py': ('# ', ''),
    '.sh': ('# ', ''),
    '.yml': ('# ', ''),
    '.yaml': ('# ', ''),
    '.toml': ('# ', ''),
    '.md': ('<!-- ', ' -->'),
    '.html': ('<!-- ', ' -->'),
    '.js': ('// ', ''),
    '.css': ('/* ', ' */'),
    '.gitignore': ('# ', ''),
}

# --- Script Logic ---

def get_prefix(file_path: Path) -> str:
    """Determines the ID prefix for a given file path based on PREFIX_MAPPING."""
    relative_path = file_path.as_posix()

    # Handle root-level files first
    if '/' not in relative_path:
        if relative_path.endswith('.md'):
            return 'DOC'
        if relative_path in ['.gitignore', '.pre-commit-config.yaml', 'bandit.yml', 'mkdocs.yml']:
            return 'CFG'

    # Check against the directory mapping
    for part in file_path.parts:
        if part in PREFIX_MAPPING:
            return PREFIX_MAPPING[part]

    return 'GEN' # Generic fallback for files not matching any specific category

def get_comment_delimiters(file_path: Path) -> tuple[str, str]:
    """Returns the appropriate comment start and end delimiters for a file type."""
    return COMMENT_STYLE_MAP.get(file_path.suffix, ('# ', ''))

def generate_id(prefix: str, counter: int) -> str:
    """Generates a formatted ID string like 'API-001'."""
    return f'{prefix}-{counter:03d}'

def load_inventory_and_counters(inventory_path: Path) -> tuple[list, dict]:
    """Loads existing inventory and derives the latest counter for each prefix."""
    if not inventory_path.exists():
        return [], {}

    try:
        data = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            print("[WARNING] Inventory file is not a list. Starting fresh.")
            return [], {}
    except (yaml.YAMLError, IOError) as e:
        print(f"[WARNING] Could not read inventory, starting fresh: {e}")
        return [], {}

    counters = {}
    for entry in data:
        if isinstance(entry, dict) and 'id' in entry and 'prefix' in entry:
            prefix = entry['prefix']
            try:
                num = int(entry['id'].split('-')[-1])
                if num > counters.get(prefix, 0):
                    counters[prefix] = num
            except (ValueError, IndexError):
                continue # Ignore malformed IDs

    print(f"Loaded existing inventory with {len(data)} items. Current counters: {counters}")
    return data, counters

def scan_and_tag(repo_root: Path, target_path: str = None, dry_run: bool = True):
    """
    Scans the repository, tags files, and generates an inventory.
    Can be limited to a specific target_path.
    """
    mode = 'DRY RUN' if dry_run else 'APPLY'
    print(f"--- Starting Scan & Tag ({mode}) for target: {target_path or 'all'} ---")

    inventory_file = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')
    inventory, counters = load_inventory_and_counters(inventory_file)

    # Create a set of already inventoried paths for quick lookup
    inventoried_paths = {item.get('path') for item in inventory}

    files_to_scan = []
    if target_path:
        # If target is a file
        if Path(target_path).is_file():
            files_to_scan = [Path(target_path)]
        # if target is a directory
        else:
            files_to_scan = sorted([p for p in Path(target_path).rglob('*') if p.is_file()])
    else:
        files_to_scan = sorted([p for p in repo_root.rglob('*') if p.is_file()])

    newly_tagged_files = 0
    for file_path in files_to_scan:
        relative_path_str = str(file_path.as_posix())

        # If a file is being explicitly targeted, remove its old entry from the inventory first.
        if target_path and relative_path_str in inventoried_paths:
            print(f"Re-tagging explicitly targeted file: {relative_path_str}")
            inventory = [item for item in inventory if item.get('path') != relative_path_str]
            inventoried_paths.remove(relative_path_str)
        elif relative_path_str in inventoried_paths:
            continue

        # Check if the file or any of its parent directories are in the exclusion list
        if any(part in EXCLUDE_DIRS for part in file_path.parts) or file_path.name in EXCLUDE_FILES:
            continue

        prefix = get_prefix(file_path)
        counters[prefix] = counters.get(prefix, 0) + 1
        new_id = generate_id(prefix, counters[prefix])

        tag_start, tag_end = get_comment_delimiters(file_path)
        id_tag_line = f"{tag_start}ID: {new_id}{tag_end}\n"

        inventory.append({'id': new_id, 'path': relative_path_str, 'prefix': prefix})
        newly_tagged_files += 1

        if dry_run:
            print(f"[DRY RUN] Would tag '{relative_path_str}' with ID '{new_id}'")
        else:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                content = re.sub(r"^(#|//|<!--)\s*Task ID:.*(\s*-->)?\n?", "", content, flags=re.MULTILINE)

                # A more robust check for an existing ID tag on the first line.
                has_existing_tag = False
                if content:
                    first_line = content.splitlines()[0]
                    if re.search(r"(?:#|//|<!--)\s*ID:\s*([A-Z]{2,4}-\d{3,})", first_line):
                        has_existing_tag = True

                if not has_existing_tag:
                    file_path.write_text(id_tag_line + content, encoding='utf-8')
                    print(f"[APPLY] Tagged '{relative_path_str}' with ID '{new_id}'")
                else:
                    print(f"[SKIP] File '{relative_path_str}' already has an ID.")
            except Exception as e:
                print(f"[ERROR] Could not process file {relative_path_str}: {e}")

    print(f"\n--- Tagging Summary for this run ---")
    print(f"Tagged {newly_tagged_files} new files.")

    if not dry_run:
        write_inventory(inventory, inventory_file)

def validate_tags(repo_root: Path):
    """Scans the repo and validates existing ID tags for format and uniqueness."""
    print("--- Starting Tag Validation ---")
    inventory_path = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')
    if not inventory_path.exists():
        print("[ERROR] Inventory file not found. Cannot validate.")
        return

    try:
        inventory_data = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))
        path_to_id_map = {item['path']: item['id'] for item in inventory_data}
        id_to_path_map = {item['id']: item['path'] for item in inventory_data}
    except (yaml.YAMLError, IOError) as e:
        print(f"[ERROR] Could not read or parse inventory file: {e}")
        return

    errors = []

    # Check for duplicate IDs in the inventory itself
    if len(id_to_path_map) != len(inventory_data):
        from collections import Counter
        id_counts = Counter(item['id'] for item in inventory_data)
        for an_id, count in id_counts.items():
            if count > 1:
                errors.append(f"Duplicate ID '{an_id}' found in inventory file.")

    # Check each file on disk against the inventory
    for file_path_str, expected_id in path_to_id_map.items():
        file_path = Path(file_path_str)
        if not file_path.exists():
            errors.append(f"File '{file_path}' is in inventory but not found on disk.")
            continue

        # Skip validation for the inventory file itself, as it's a generated artifact.
        if file_path == inventory_path:
            continue

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if not content: # Skip empty files, they can't have tags
                continue

            first_line = content.splitlines()[0]
            # This regex must match all comment styles defined in COMMENT_STYLE_MAP
            match = re.search(r"(?:#|//|<!--|/\*)\s*ID:\s*([A-Z]{2,4}-\d{3,})\s*(?:-->|\*/)?", first_line)

            if not match:
                errors.append(f"Missing or malformed ID tag in file: '{file_path}'")
            elif match.group(1) != expected_id:
                errors.append(f"ID mismatch in '{file_path}'. Expected '{expected_id}', found '{match.group(1)}'.")

        except Exception as e:
            errors.append(f"Could not read or process file '{file_path}': {e}")

    if not errors:
        print(f"[SUCCESS] Validation complete. Verified {len(path_to_id_map)} files. No errors.")
    else:
        print(f"\n[FAILURE] Validation found {len(errors)} errors:")
        for error in errors:
            print(f"- {error}")

def write_inventory(inventory_data: list, output_path: Path):
    """Writes the collected inventory data to a YAML file."""
    print(f"\nWriting inventory to '{output_path}'...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(inventory_data, f, sort_keys=False)
    print("[SUCCESS] Inventory file written.")


def main():
    """Main function to parse arguments and run the script in the chosen mode."""
    parser = argparse.ArgumentParser(description="Scan, tag, and validate repository files for the alignment system.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--dry-run', action='store_true', help="Show what would be done without changing files.")
    group.add_argument('--apply', action='store_true', help="Apply tags to files and generate the inventory.")
    group.add_argument('--validate', action='store_true', help="Validate existing tags for uniqueness and format.")
    parser.add_argument('--target', type=str, help="Optional: a specific directory or file to process.", default=None)

    args = parser.parse_args()
    repo_root = Path('.')

    if args.dry_run:
        scan_and_tag(repo_root, target_path=args.target, dry_run=True)
    elif args.apply:
        scan_and_tag(repo_root, target_path=args.target, dry_run=False)
    elif args.validate:
        validate_tags(repo_root)

if __name__ == "__main__":
    main()