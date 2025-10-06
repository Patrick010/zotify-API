#!/usr/bin/env python3
import json
import yaml
from pathlib import Path
import os

TRACE_INDEX_PATH = Path("project/reports/TRACE_INDEX.yml")
OUTPUT_JSON = Path("scripts/project_registry.json")
OUTPUT_MD = Path("project/PROJECT_REGISTRY.md")

def normalize_path(path_str: str) -> str:
    """Normalize file paths to a consistent form."""
    norm = Path(path_str).as_posix().strip()
    while norm.startswith("./") or norm.startswith("../"):
        norm = norm.split("/", 1)[-1]
    return norm

def load_trace_index():
    """Load TRACE_INDEX.yml and return its entries."""
    with open(TRACE_INDEX_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    artifacts = data.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ValueError("TRACE_INDEX.yml 'artifacts' key must contain a list")
    return {item.get('path', ''): item for item in artifacts}

def load_descriptions_from_trace_index():
    """Loads descriptions from the master TRACE_INDEX.yml file."""
    with open(TRACE_INDEX_PATH, 'r', encoding='utf-8') as f:
        trace_index = yaml.safe_load(f)

    description_map = {}
    for item in trace_index.get('artifacts', []):
        description_map[item['path']] = item.get('description', '').strip()

    return description_map

def build_project_registry(trace_index, description_map):
    """Generate registry entries for all project markdown files."""
    registry = {}
    unclassified = []

    for path_str, info in trace_index.items():
        norm = normalize_path(path_str)
        if not norm.startswith("project/") or not norm.endswith(".md"):
            continue
        if "logs/" in norm or "tests/" in norm:
            continue

        description = description_map.get(norm)
        if not description:
            description = f"TODO: Add description for {Path(norm).name}"
            unclassified.append(norm)

        status = "registered"
        if not Path(norm).exists():
            status = "missing"

        registry[norm] = {
            "path": norm,
            "status": status,
            "description": description,
        }

    if unclassified:
        print("⚠️ Warning: The following files are missing descriptions in TRACE_INDEX.yml:")
        for p in sorted(unclassified):
            print(f"  - {p}")

    unique_registry = {k: v for k, v in sorted(registry.items())}
    if len(unique_registry) < len(registry):
        print(f"⚠️ Removed {len(registry) - len(unique_registry)} duplicate entries")

    return unique_registry

def write_json(registry):
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(list(registry.values()), f, indent=2)
    print(f"✅ Wrote {len(registry)} entries to {OUTPUT_JSON}")

def write_markdown(registry):
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Registry\n",
        "",
        "| Path | Status | Description |",
        "|------|---------|-------------|",
    ]
    for item in registry.values():
        lines.append(f"| `{item['path']}` | {item['status']} | {item['description']} |")
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ Wrote markdown summary to {OUTPUT_MD}")

def main():
    trace_index = load_trace_index()
    description_map = load_descriptions_from_trace_index()
    registry = build_project_registry(trace_index, description_map)
    write_json(registry)
    write_markdown(registry)

if __name__ == "__main__":
    main()