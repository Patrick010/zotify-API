# ID: OPS-036
#!/usr/bin/env python3
"""
Enhanced alignment verification script.
Summarizes missing or mismatched IDs clearly by type (doc/code/config).
"""

import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
TAG_PATTERN = re.compile(r"(?:#|<!--)\s*ID:\s*([A-Z0-9\-]+)", re.IGNORECASE)
TAG_INVENTORY = PROJECT_ROOT / "project/reports/DOCUMENT_TAG_INVENTORY.yml"
TRACE_INDEX_PATH = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"

# --- Ignored directories and file types consistent with governance scripts ---
IGNORED_DIRS = {".git", ".venv", "node_modules", "__pycache__", "archive", "templates", ".pytest_cache", "logs", "site"}
SCAN_EXTENSIONS = (".py", ".md", ".sh", ".yml", ".yaml")

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

def load_trace_index():
    """Loads TRACE_INDEX.yml and returns a path-to-index mapping."""
    if not TRACE_INDEX_PATH.exists():
        print(f"❌ Missing TRACE_INDEX.yml", file=sys.stderr)
        return {}
    with open(TRACE_INDEX_PATH, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
            if not isinstance(data, dict) or "artifacts" not in data:
                return {}
            path_to_index = {}
            for item in data.get("artifacts", []):
                path = item.get("path")
                index = item.get("index", "-")
                if path:
                    path_to_index[path] = index
            return path_to_index
        except yaml.YAMLError as e:
            print(f"❌ YAML parse error in TRACE_INDEX.yml: {e}", file=sys.stderr)
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

def should_skip_dir(path: str) -> bool:
    return any(part in IGNORED_DIRS for part in Path(path).parts)

def main():
    parser = argparse.ArgumentParser(description="Verify and optionally rebuild the tag inventory.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the inventory from embedded tags.")
    args = parser.parse_args()

    tag_inventory = load_tag_inventory()
    path_to_index_map = load_trace_index()

    if args.rebuild:
        if not path_to_index_map:
            print("❌ Could not build path-to-index map from TRACE_INDEX.yml. Aborting rebuild.", file=sys.stderr)
            sys.exit(1)

        new_inventory = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for f in files:
                if not f.endswith(SCAN_EXTENSIONS):
                    continue
                full_path = Path(root) / f
                rel_path = str(full_path.relative_to(PROJECT_ROOT))
                embedded_id = find_embedded_id(full_path)
                if embedded_id:
                    index = path_to_index_map.get(rel_path, "-")
                    new_inventory.append({"id": embedded_id, "path": rel_path, "index": index})

        with open(TAG_INVENTORY, "w", encoding="utf-8") as f:
            yaml.safe_dump(new_inventory, f, sort_keys=False)
        print(f"✅ Rebuilt inventory with {len(new_inventory)} items.")
        sys.exit(0)

    # --- Verification ---
    print("=== Verifying alignment migration (enhanced report) ===\n")
    if not tag_inventory:
        print("❌ Could not load tag inventory.")
        sys.exit(1)

    mismatched = []
    summary = defaultdict(list)

    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            if not f.endswith(SCAN_EXTENSIONS):
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
        for path in sorted(summary['missing_id']):
            print(f"  - {path}")
        print()

    if summary["unregistered_id"]:
        print("--- Files With Unregistered IDs ---")
        for path in sorted(summary['unregistered_id']):
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
