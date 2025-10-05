#!/usr/bin/env python3
import json
import yaml
from pathlib import Path

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

    # The actual data is under the 'artifacts' key as a list.
    # Convert it to the expected dictionary format.
    artifacts = data.get("artifacts", [])
    if not isinstance(artifacts, list):
        raise ValueError("TRACE_INDEX.yml 'artifacts' key must contain a list")

    return {item.get('path', ''): item for item in artifacts}


def build_project_registry(trace_index):
    """Generate registry entries for all project markdown files."""
    registry = {}
    for path_str, info in trace_index.items():
        norm = normalize_path(path_str)
        if not norm.startswith("project/"):
            continue
        if not norm.endswith(".md"):
            continue
        if "logs/" in norm or "tests/" in norm:
            continue

        registry[norm] = {
            "path": norm,
            "status": "registered",
            "description": info.get("description", "Project documentation file"),
        }

    # Deduplicate and sort
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
    registry = build_project_registry(trace_index)
    write_json(registry)
    write_markdown(registry)


if __name__ == "__main__":
    main()