#!/usr/bin/env python3
"""
backfill_trace_meta.py - A one-time script to backfill metadata into TRACE_INDEX.yml.

This script reads the existing `project/PROJECT_REGISTRY.md` to find human-written
descriptions and injects them into the `meta.description` field for corresponding
artifacts in `project/reports/TRACE_INDEX.yml`.

It is designed to be idempotent, meaning it can be run multiple times without
corrupting or duplicating data.
"""
import os
import re
import yaml
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_INDEX_PATH = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
LEGACY_REGISTRY_PATH = PROJECT_ROOT / "project/PROJECT_REGISTRY.md"

def parse_legacy_registry(md_content: str, md_path: Path) -> dict:
    """Parses the legacy PROJECT_REGISTRY.md to extract file paths and descriptions."""
    legacy_entries = {}
    base_dir = md_path.parent
    # Regex to capture the link, path, and description from a markdown table row
    table_row_re = re.compile(r"\|\s*\*\*.*\*\*.*\[`([^`]+)`\]\(([^)]+)\)\s*\|([^|]*)\|")

    for line in md_content.splitlines():
        match = table_row_re.search(line)
        if match:
            _, rel_path, description = [m.strip() for m in match.groups()]

            # Resolve the path relative to the markdown file
            try:
                # Normalize the path to be relative to the project root
                full_path = (base_dir / rel_path).resolve()
                repo_relative_path = str(full_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
                legacy_entries[repo_relative_path] = description
            except (ValueError, FileNotFoundError):
                # Ignore broken links or files outside the project root
                continue
    return legacy_entries

def main():
    """Main function to perform the backfill operation."""
    if not TRACE_INDEX_PATH.exists():
        print(f"❌ ERROR: Trace index not found at {TRACE_INDEX_PATH}")
        return 1

    with open(TRACE_INDEX_PATH, "r", encoding="utf-8") as f:
        trace_data = yaml.safe_load(f)

    artifacts = trace_data.get("artifacts", [])
    if not artifacts:
        print("✅ No artifacts found in trace index. Nothing to do.")
        return 0

    legacy_descriptions = {}
    if LEGACY_REGISTRY_PATH.exists():
        with open(LEGACY_REGISTRY_PATH, "r", encoding="utf-8") as f:
            md_content = f.read()
            legacy_descriptions = parse_legacy_registry(md_content, LEGACY_REGISTRY_PATH)
    else:
        print(f"⚠️ Warning: Legacy registry not found at {LEGACY_REGISTRY_PATH}. Descriptions will not be backfilled.")

    updated_count = 0
    for artifact in artifacts:
        path = artifact.get("path")
        if not path:
            continue

        meta = artifact.setdefault("meta", {})
        current_description = meta.get("description", "").strip()

        # Check if description is missing or is the default placeholder
        if not current_description or current_description == "No description available.":
            legacy_desc = legacy_descriptions.get(path)
            if legacy_desc:
                meta["description"] = legacy_desc
                updated_count += 1
                print(f"  -> Updated description for {path}")

    if updated_count > 0:
        with open(TRACE_INDEX_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(trace_data, f, default_flow_style=False, sort_keys=False)
        print(f"\n✅ Successfully updated {updated_count} artifact(s) in {TRACE_INDEX_PATH}.")
    else:
        print("\n✅ No missing descriptions found to backfill. Trace index is already up-to-date.")

    return 0

if __name__ == "__main__":
    exit(main())