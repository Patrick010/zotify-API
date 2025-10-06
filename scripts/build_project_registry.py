#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds a machine-readable project registry from the TRACE_INDEX.yml.
"""
import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path
import os

import yaml

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))


def normalize_path(path_str):
    """Normalizes a path string to a consistent format, removing leading './'."""
    return os.path.normpath(path_str).replace("\\", "/").lstrip("./")


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


def derive_name(path_obj, legacy_entry=None):
    """Derives a human-readable name from a path or legacy entry."""
    if legacy_entry and legacy_entry.get("name"):
        return legacy_entry["name"]
    return path_obj.stem.replace("_", " ").replace("-", " ").title()


def parse_legacy_registry(md_content, md_path, repo_root):
    """Parses the legacy PROJECT_REGISTRY.md to extract entries."""
    legacy_entries = {}
    base_dir = md_path.parent
    table_row_re = re.compile(r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|([^|]*)\|")

    for line in md_content.splitlines():
        match = table_row_re.search(line)
        if match:
            name, rel_path, description = [m.strip() for m in match.groups()]

            # Correct the corrupted path before resolving it.
            # This handles the case where './project/' was incorrectly prepended.
            if rel_path.startswith('./project/'):
                rel_path = rel_path[len('./project/'):]

            full_path = (base_dir / rel_path).resolve()
            repo_relative_path = normalize_path(str(full_path.relative_to(repo_root)))

            legacy_entries[repo_relative_path] = {
                "name": name, "path": repo_relative_path, "notes": description,
            }
    return legacy_entries


def build_registry(
    trace_index_path, project_registry_md_path, extras_file_path, output_json_path, project_dir, repo_root, debug=False
):
    """Builds the project registry."""
    trace_map = {}
    if trace_index_path.exists():
        with open(trace_index_path, "r", encoding="utf-8") as f:
            trace_data = yaml.safe_load(f)
            artifacts = trace_data.get("artifacts", []) if isinstance(trace_data, dict) else trace_data or []
            trace_map = {normalize_path(item["path"]): item for item in artifacts}

    legacy_entries = {}
    if project_registry_md_path.exists():
        with open(project_registry_md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
            legacy_entries = parse_legacy_registry(md_content, project_registry_md_path, repo_root)

    extras_to_include = []
    if extras_file_path.exists():
        with open(extras_file_path, "r", encoding="utf-8") as f:
            extras_data = yaml.safe_load(f)
            extras_to_include = [normalize_path(p) for p in extras_data.get("include", [])]

    registry = []
    processed_paths = set()

    all_paths_to_process = set(trace_map.keys()) | set(legacy_entries.keys()) | set(extras_to_include)

    for path_str in all_paths_to_process:
        path_obj = Path(path_str)

        is_project_doc = path_str.startswith("project/")
        is_code_file_index = path_str == "api/docs/CODE_FILE_INDEX.md"
        is_in_extras = path_str in extras_to_include

        if not (is_project_doc or is_code_file_index or is_in_extras):
            if debug: print(f"[FILTERED OUT] Path '{path_str}' does not match project scope.")
            continue

        processed_paths.add(path_str)

        trace_item = trace_map.get(path_str)
        legacy_item = legacy_entries.get(path_str)
        exists_on_disk = (repo_root / path_str).exists()

        status = "unknown"
        source = "unknown"

        if trace_item:
            status = "registered" if exists_on_disk else "missing"
            source = "TRACE_INDEX.yml"
        elif legacy_item:
            status = "legacy" if not exists_on_disk else "orphan"
            source = "project/PROJECT_REGISTRY.md"
        elif path_str in extras_to_include:
             status = "missing"
             source = "extras"

        if exists_on_disk and not trace_item and not legacy_item:
            status = "orphan"
            source = "filesystem"

        module, category = derive_module_category(path_obj)
        entry = {
            "name": derive_name(path_obj, legacy_item), "path": path_str, "type": "doc",
            "module": module, "category": category, "registered_in": trace_item.get("registered_in", []) if trace_item else [],
            "status": status, "notes": legacy_item["notes"] if legacy_item else "", "source": source,
        }
        registry.append(entry)

    if project_dir.exists():
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                path_str = normalize_path(str(file_path.relative_to(repo_root)))
                if path_str not in processed_paths:
                    if not path_str.startswith("project/"):
                        if debug: print(f"[FILTERED OUT] Orphan scan skipped non-project file: {path_str}")
                        continue

                    processed_paths.add(path_str)
                    path_obj = Path(path_str)
                    module, category = derive_module_category(path_obj)
                    entry = { "name": derive_name(path_obj), "path": path_str, "type": "doc", "module": module, "category": category,
                        "registered_in": [], "status": "orphan", "notes": "", "source": "filesystem",
                    }
                    registry.append(entry)

    registry.sort(key=lambda x: (x["module"], x["category"], x["path"]))

    if output_json_path.exists():
        try:
            with open(output_json_path, "r", encoding="utf-8") as f:
                if json.load(f) == registry:
                    print(f"No changes to {output_json_path}. Skipping write.")
                    return registry
        except (json.JSONDecodeError, IOError):
            pass

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
            # Paths are already repo-relative, so make them relative to the MD file's location
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

    if output_md_path.exists():
        with open(output_md_path, 'r', encoding='utf-8') as f:
            if f.read() == content:
                print(f"No changes to {output_md_path}. Skipping write.")
                return

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