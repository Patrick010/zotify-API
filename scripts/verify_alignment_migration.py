#!/usr/bin/env python3
# ID: OPS-031
"""
Enhanced alignment verification script.
Summarizes missing or mismatched IDs clearly by type (doc/code/config).
"""

import os
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
TAG_PATTERN = re.compile(r"(?:#|<!--)\s*ID:\s*([A-Z0-9\-]+)", re.IGNORECASE)
TAG_INVENTORY = PROJECT_ROOT / "project/reports/DOCUMENT_TAG_INVENTORY.yml"

def load_tag_inventory():
    if not TAG_INVENTORY.exists():
        print(f"❌ Missing DOCUMENT_TAG_INVENTORY.yml", file=sys.stderr)
        return {}
    with open(TAG_INVENTORY, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            if isinstance(data, list):
                return {entry.get("id"): entry for entry in data if "id" in entry}
            elif isinstance(data, dict):
                return data
            else:
                return {}
        except yaml.YAMLError as e:
            print(f"❌ YAML parse error: {e}", file=sys.stderr)
            return {}

def find_embedded_id(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                match = TAG_PATTERN.search(line)
                if match:
                    return match.group(1).strip()
    except Exception:
        return None
    return None

def main():
    print("=== Verifying alignment migration (enhanced report) ===\n")

    tag_inventory = load_tag_inventory()
    if not tag_inventory:
        print("❌ Could not load tag inventory.")
        sys.exit(1)

    mismatched = []
    summary = defaultdict(list)

    for root, _, files in os.walk(PROJECT_ROOT):
        if any(part in root for part in [".git", ".venv", "node_modules", "archive", "__pycache__"]):
            continue
        for f in files:
            if not f.endswith((".py", ".md", ".sh", ".yml", ".yaml")):
                continue
            full_path = Path(root) / f
            rel_path = str(full_path.relative_to(PROJECT_ROOT))
            embedded_id = find_embedded_id(full_path)
            if not embedded_id:
                summary["missing_id"].append(rel_path)
                continue
            if embedded_id not in tag_inventory:
                summary["unregistered_id"].append(f"{rel_path} (ID: {embedded_id})")

    print("=== Alignment Verification Summary ===\n")
    print(f"Files with missing ID tags: {len(summary['missing_id'])}")
    print(f"Files with unregistered IDs: {len(summary['unregistered_id'])}\n")

    if summary["missing_id"]:
        print("--- Files Missing ID Tags ---")
        for path in sorted(summary["missing_id"]):
            print(f"  - {path}")
        print()

    if summary["unregistered_id"]:
        print("--- Files With Unregistered IDs ---")
        for path in sorted(summary["unregistered_id"]):
            print(f"  - {path}")
        print()

    if not summary["missing_id"] and not summary["unregistered_id"]:
        print("✅ All files have valid, registered IDs.")
        sys.exit(0)
    else:
        print("❌ Alignment verification incomplete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
