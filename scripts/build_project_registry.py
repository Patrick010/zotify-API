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


def derive_module_category(path_obj):
    """Derives the module and category from a given path."""
    parts = path_obj.parts
    if not parts:
        return "general", "general"

    module = parts[0]

    if len(parts) > 2:
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
            # Resolve the path relative to the markdown file, then make it relative to the repo root
            full_path = (base_dir / rel_path).resolve()
            repo_relative_path = full_path.relative_to(repo_root).as_posix()

            legacy_entries[repo_relative_path] = {
                "name": name,
                "path": repo_relative_path,
                "notes": description,
                "verbatim": line,
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

    registry = []
    processed_paths = set()

    all_paths_to_process = set(trace_map.keys()) | set(legacy_entries.keys()) | set(extras_to_include)

    for path_str in all_paths_to_process:
        # 1. Path Normalization
        normalized_path_str = os.path.normpath(path_str).replace("\\", "/")
        path_obj = Path(normalized_path_str)

        # 2. Stricter Filtering
        is_project_doc = normalized_path_str.startswith("project/")
        is_code_file_index = normalized_path_str == "api/docs/CODE_FILE_INDEX.md"

        if not (is_project_doc or is_code_file_index):
            if debug:
                print(f"[FILTERED OUT] {normalized_path_str}")
            continue

        processed_paths.add(normalized_path_str)

        trace_item = trace_map.get(normalized_path_str, {})
        legacy_entry = legacy_entries.get(normalized_path_str)

        # 3. Correct Status Assignment
        exists_on_disk = (repo_root / normalized_path_str).exists()

        if legacy_entry and not trace_item and not exists_on_disk:
            status = "legacy"
        elif exists_on_disk and trace_item.get("registered"):
             status = "registered"
        elif not exists_on_disk:
             status = "missing"
        else: # Exists on disk but not registered in trace
             status = "orphan"

        source = "project/PROJECT_REGISTRY.md" if status == "legacy" else "TRACE_INDEX.yml"

        module, category = derive_module_category(path_obj)
        entry = {
            "name": derive_name(path_obj, legacy_entry), "path": normalized_path_str, "type": trace_item.get("type", "doc"),
            "module": module, "category": category, "registered_in": trace_item.get("registered_in", []),
            "status": status, "notes": legacy_entry["notes"] if legacy_entry else "", "source": source,
        }
        registry.append(entry)

    # Orphan detection for files on disk but not in any loaded source
    if project_dir.exists():
        for file_path in project_dir.rglob('*'):
            if file_path.is_file():
                path_str = file_path.relative_to(repo_root).as_posix()
                if path_str not in processed_paths:
                    if not (path_str.startswith("project/")):
                        if debug:
                            print(f"[FILTERED OUT] Orphan scan skipped non-project file: {path_str}")
                        continue
                    processed_paths.add(path_str)
                    path_obj = Path(path_str)
                    module, category = derive_module_category(path_obj)
                    entry = {
                        "name": derive_name(path_obj), "path": path_str, "type": "doc", "module": module, "category": category,
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
    """Generates the project registry markdown file."""
    header = "<!-- AUTO-GENERATED from scripts/project_registry.json — manual edits may be overwritten. Historical legacy entries preserved below. -->\n\n"
    table_header = "| Document | Location | Description | Status |\n|---|---|---|---|\n"

    main_entries = [e for e in registry_data if e.get("status") in ["registered", "missing"]]
    legacy_entries = [e for e in registry_data if e.get("status") == "legacy"]
    orphan_entries = [e for e in registry_data if e.get("status") == "orphan"]

    table_rows = []
    for entry in main_entries:
        try:
            relative_path = Path(entry["path"]).relative_to(output_md_path.parent)
        except ValueError:
            relative_path = Path(entry["path"])
        location_str = f"[`{relative_path}`](./{relative_path})"
        table_rows.append(f"| **{entry['name']}** | {location_str} | {entry['notes']} | {entry['status']} |")

    content = header + table_header + "\n".join(sorted(table_rows))

    if legacy_entries:
        legacy_lines = [f"| **{e['name']}** | [`{e['path']}`](./{e['path']}) | {e['notes']} | {e['status']} |" for e in legacy_entries]
        content += "\n\n## Historical / Legacy Entries\n\n" + table_header + "\n".join(sorted(legacy_lines))

    if orphan_entries:
        content += "\n\n## Orphan Files\n\n"
        orphan_list = [f"- `{entry['path']}`" for entry in orphan_entries]
        content += "\n".join(sorted(orphan_list))

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