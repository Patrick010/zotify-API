#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds a machine-readable project registry from various sources.
"""
import argparse
import json
import re
import sys
from pathlib import Path
import os
import yaml

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))


def normalize_path(path_str: str) -> str:
    """
    Normalize and clean file paths so duplicates across data sources resolve to a single form.
    This implementation is based on the user's specific request.
    """
    path_str = re.sub(r"[`\[\]]", "", path_str)
    path_str = path_str.strip().replace("\\", "/")
    # Use os.path.normpath for robust handling of '..' and '.'
    norm = os.path.normpath(path_str)
    # Further cleaning to handle cases normpath might miss and ensure posix style
    norm = Path(norm).as_posix()
    while norm.startswith("./"):
        norm = norm[2:]
    # Remove any leading slashes that might result from aggressive splitting
    norm = norm.lstrip('/')
    norm = re.sub(r"/+", "/", norm)
    return norm


def derive_module_category(path_obj):
    """Derives the module and category from a given path."""
    parts = path_obj.parts
    if not parts:
        return "general", "general"
    module = parts[0]
    if len(parts) > 2 and parts[1] not in ("src", "tests"):
        category = parts[1]
    else:
        category = "general"
    return module, category


def derive_name(path_obj, item=None):
    """Derives a human-readable name from a path or an item entry."""
    if item and item.get("name"):
        return item["name"]
    return path_obj.stem.replace("_", " ").replace("-", " ").title()


def parse_legacy_registry(md_content, md_path, repo_root):
    """
    Parses the legacy PROJECT_REGISTRY.md to extract entries. This function
    now correctly distinguishes between file-relative and repo-relative paths.
    """
    legacy_entries = {}
    base_dir = md_path.parent
    table_row_re = re.compile(r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|([^|]*)\|")

    for line in md_content.splitlines():
        match = table_row_re.search(line)
        if match:
            name, rel_path, description = [m.strip() for m in match.groups()]

            # If the path starts with './' or '../', it's relative to the MD file.
            if rel_path.startswith('./') or rel_path.startswith('../'):
                try:
                    full_path = (base_dir / rel_path).resolve()
                    repo_relative_path = str(full_path.relative_to(repo_root))
                except (FileNotFoundError, ValueError):
                    repo_relative_path = os.path.normpath(os.path.join(base_dir.name, rel_path))
            else:
                # Otherwise, assume it's relative to the repository root.
                repo_relative_path = rel_path

            normalized_repo_path = normalize_path(repo_relative_path)
            legacy_entries[normalized_repo_path] = {
                "name": name, "path": normalized_repo_path, "notes": description,
            }
    return legacy_entries


def build_registry(
    trace_index_path, project_registry_md_path, extras_file_path, output_json_path, project_dir, repo_root, debug=False
):
    """Builds the project registry using a definitive multi-pass approach."""
    # --- 1. Load all data sources ---
    trace_map = {}
    if trace_index_path.exists():
        with open(trace_index_path, "r", encoding="utf-8") as f:
            trace_data = yaml.safe_load(f)
            artifacts = trace_data.get("artifacts", []) if isinstance(trace_data, dict) else trace_data or []
            trace_map = {item["path"]: item for item in artifacts}

    legacy_entries = {}
    if project_registry_md_path.exists():
        with open(project_registry_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            legacy_entries = parse_legacy_registry(md_content, project_registry_md_path, repo_root)

    extras_to_include = []
    if extras_file_path.exists():
        with open(extras_file_path, "r", encoding="utf-8") as f:
            extras_data = yaml.safe_load(f)
            extras_to_include = extras_data.get("include", [])

    # --- 2. Process entries with a clear priority order ---
    registry_map = {}
    processed = set()

    blacklist = {
        normalize_path(str(project_registry_md_path.relative_to(repo_root)))
    }
    raw_extras = set(extras_to_include)

    def is_path_allowed(path_str):
        norm_path = normalize_path(path_str)
        is_project_doc = norm_path.startswith("project/")
        is_code_file_index = norm_path == "api/docs/CODE_FILE_INDEX.md"
        is_in_extras = any(normalize_path(p) == norm_path for p in raw_extras)
        return is_project_doc or is_code_file_index or is_in_extras

    def make_entry(item, status):
        path_str = item.get("path")
        path_obj = Path(path_str)
        exists_on_disk = (repo_root / path_str).exists()

        final_status = status
        if status == "registered" and not exists_on_disk:
            final_status = "missing"

        return {
            "name": derive_name(path_obj, item), "path": path_str, "type": "doc",
            "module": derive_module_category(path_obj)[0], "category": derive_module_category(path_obj)[1],
            "registered_in": item.get("registered_in", []),
            "status": final_status, "notes": item.get("notes", ""), "source": "",
        }

    def register(path_str, entry_data, source):
        p = normalize_path(path_str)
        if p in blacklist or not is_path_allowed(p) or p in processed:
            return
        processed.add(p)
        entry_data["source"] = source
        registry_map[p] = entry_data

    # Pass 0: Special Cases
    code_file_index_path = "api/docs/CODE_FILE_INDEX.md"
    if is_path_allowed(code_file_index_path):
        register(code_file_index_path, make_entry({"path": code_file_index_path, "notes": "Canonical source code index."}, "registered"), "Special Case")

    # Pass 1: TRACE_INDEX.yml
    for path_str, item in trace_map.items():
        register(path_str, make_entry(item, "registered"), "TRACE_INDEX.yml")

    # Pass 2: extras.yml
    for path_str in extras_to_include:
        register(path_str, make_entry({"path": path_str, "notes": "Included via extras file"}, "registered"), "extras.yml")

    # Pass 3: Legacy registry
    for path_str, item in legacy_entries.items():
        p = normalize_path(path_str)
        if p in registry_map:
            if "Originally in legacy registry" not in registry_map[p]["notes"]:
                registry_map[p]["notes"] += "; Originally in legacy registry"
            continue
        exists_on_disk = (repo_root / p).exists()
        register(p, make_entry(item, "orphan" if exists_on_disk else "legacy"), "project/PROJECT_REGISTRY.md")

    # Pass 4: Orphan scan
    if project_dir.exists():
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                path_str = str(file_path.relative_to(repo_root))
                register(path_str, make_entry({"path": path_str, "notes": "File exists on disk but is not tracked."}, "orphan"), "filesystem")

    # --- 4. Finalize and write to JSON ---
    registry = list(registry_map.values())
    registry.sort(key=lambda x: (x["module"], x["category"], x["path"]))

    if output_json_path.exists():
        try:
            with open(output_json_path, "r", encoding="utf-8") as f:
                if json.load(f) == registry:
                    print(f"No changes to {output_json_path}. Skipping write.")
                    return registry
        except (json.JSONDecodeError, IOError):
            pass # File is corrupt or unreadable, so we'll overwrite it.

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4, sort_keys=False)
    print(f"Successfully wrote project registry to {output_json_path}")
    return registry


def generate_markdown(registry_data, output_md_path):
    """Generates the project registry markdown file from the final registry data."""
    header = "<!-- AUTO-GENERATED from scripts/project_registry.json — manual edits may be overwritten. Historical legacy entries preserved below. -->\n\n"
    table_header = "| Document | Location | Description | Status |\n|---|---|---|---|\n"

    main_entries = sorted([e for e in registry_data if e.get("status") in ["registered", "missing"]], key=lambda x: x['path'])
    legacy_entries = sorted([e for e in registry_data if e.get("status") == "legacy"], key=lambda x: x['path'])
    orphan_entries = sorted([e for e in registry_data if e.get("status") == "orphan"], key=lambda x: x['path'])

    def create_table_row(entry, base_path):
        try:
            relative_path = Path(entry["path"]).relative_to(base_path.parent)
        except ValueError:
            relative_path = Path(entry["path"])
        location_str = f"[`{entry['path']}`](./{relative_path})"
        return f"| **{entry['name']}** | {location_str} | {entry['notes']} | {entry['status']} |"

    table_rows = [create_table_row(e, output_md_path) for e in main_entries]
    content = header + table_header + "\n".join(table_rows)

    if legacy_entries:
        legacy_lines = [create_table_row(e, output_md_path) for e in legacy_entries]
        content += "\n\n## Historical / Legacy Entries\n\n" + table_header + "\n".join(legacy_lines)

    if orphan_entries:
        content += "\n\n## Orphan Files\n\n"
        orphan_list = [f"- `{entry['path']}`" for entry in orphan_entries]
        content += "\n".join(orphan_list)

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Successfully generated {output_md_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    repo_root = Path.cwd()
    parser.add_argument("--trace-index", type=Path, default=repo_root / "project/reports/TRACE_INDEX.yml")
    parser.add_argument("--project-registry-md", type=Path, default=repo_root / "project/PROJECT_REGISTRY.md")
    parser.add_argument("--extras-file", type=Path, default=repo_root / "scripts/project_registry_extras.yml")
    parser.add_argument("--output-json", type=Path, default=repo_root / "scripts/project_registry.json")
    parser.add_argument("--output-md", type=Path, default=repo_root / "project/PROJECT_REGISTRY.md")
    parser.add_argument("--project-dir", type=Path, default=repo_root / "project", help="The project directory to scan for orphans.")
    parser.add_argument("--debug", action="store_true", help="Enable debug printing.")
    args = parser.parse_args()

    registry_data = build_registry(
        args.trace_index, args.project_registry_md, args.extras_file, args.output_json, args.project_dir, repo_root, args.debug
    )

    if registry_data is not None:
        generate_markdown(registry_data, args.output_md)


if __name__ == "__main__":
    main()