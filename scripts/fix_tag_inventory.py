#!/usr/bin/env python3
import yaml
from pathlib import Path

TAG_FILE = Path("project/reports/DOCUMENT_TAG_INVENTORY.yml")

def main(dry_run=True):
    if not TAG_FILE.exists():
        print(f"❌ {TAG_FILE} does not exist.")
        return 1

    with TAG_FILE.open("r", encoding="utf-8") as f:
        try:
            tags = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"❌ YAML parse error: {e}")
            return 1

    if not isinstance(tags, list):
        print("❌ Expected a list of tag entries.")
        return 1

    fixed = 0
    for i, entry in enumerate(tags):
        if 'file' not in entry:
            print(f"⚠️ Entry {i} missing 'file': {entry}")
            # Auto-fill file as 'UNKNOWN' or some default path
            if not dry_run:
                entry['file'] = "UNKNOWN"
            fixed += 1

    if fixed == 0:
        print("✅ All entries have 'file' keys.")
    else:
        print(f"⚠️ Fixed {fixed} entries missing 'file' keys.")
        if not dry_run:
            TAG_FILE.write_text(yaml.safe_dump(tags, sort_keys=False), encoding="utf-8")
            print(f"✅ Written corrected {TAG_FILE}")

    return 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate and fix DOCUMENT_TAG_INVENTORY.yml")
    parser.add_argument("--apply", action="store_true", help="Write fixes to the file instead of dry-run")
    args = parser.parse_args()
    exit(main(dry_run=not args.apply))
