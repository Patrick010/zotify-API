# ID: OPS-016
#!/usr/bin/env python3
"""
Lint Governance Links Script
Generates PROJECT_DOCUMENT_ALIGNMENT.md and lint_governance_links.json.
Tracks document alignment based on TRACE_INDEX.yml and project/*.md files.
"""

import json
from pathlib import Path
import yaml

PROJECT_ROOT = Path(__file__).parent.parent
TRACE_INDEX_FILE = PROJECT_ROOT / "project" / "reports" / "TRACE_INDEX.yml"
OUTPUT_JSON = PROJECT_ROOT / "scripts" / "lint_governance_links.json"
OUTPUT_MD = PROJECT_ROOT / "project" / "reports" / "PROJECT_DOCUMENT_ALIGNMENT.md"

def load_and_normalize_trace_index():
    """
    Loads and normalizes the TRACE_INDEX.yml file.
    Handles three formats:
    1. A dictionary with an "artifacts" key holding a list of file objects.
    2. A direct list of file objects.
    3. A legacy dictionary where file paths are top-level keys.
    Returns a unified dictionary mapping file paths to their data.
    """
    with open(TRACE_INDEX_FILE, "r") as f:
        data = yaml.safe_load(f)

    if isinstance(data, dict):
        if "artifacts" in data and isinstance(data.get("artifacts"), list):
            # New format: dict with "artifacts" key
            return {item["path"]: item for item in data["artifacts"] if "path" in item}
        else:
            # Legacy format: dict with paths as keys
            return data
    elif isinstance(data, list):
        # New format: list of objects
        return {item["path"]: item for item in data if "path" in item}
    raise ValueError("Unknown format for TRACE_INDEX.yml")

def scan_project_files():
    files = list(PROJECT_ROOT.glob("project/**/*.md"))
    return [f.relative_to(PROJECT_ROOT).as_posix() for f in files
            if not f.parts[1] in ("archive", "logs")]

def classify_files(trace_index, project_files):
    files_report = []
    fully_aligned = partially_aligned = 0
    unlinked = []

    traced_paths = set(trace_index.keys())

    for f_path in project_files:
        status = "unlinked"
        if f_path in traced_paths:
            item = trace_index[f_path]
            if item and item.get("registered"):
                # A file is considered fully aligned if it is registered and has a valid index reference.
                if item.get("index") and item.get("index") != "-":
                    status = "fully_aligned"
                    fully_aligned += 1
                else:
                    status = "partially_aligned"
                    partially_aligned += 1
            else:
                unlinked.append(f_path)
        else:
            unlinked.append(f_path)

        files_report.append({"path": f_path, "status": status})

    return files_report, fully_aligned, partially_aligned, len(unlinked)

def write_json_report(report_data):
    with open(OUTPUT_JSON, "w") as f:
        json.dump(report_data, f, indent=4)

def write_md_report(report_data):
    md_lines = ["# Project Document Alignment Report\n"]
    categories = {"fully_aligned": [], "partially_aligned": [], "unlinked": []}
    for entry in report_data["files"]:
        categories[entry["status"]].append(entry["path"])

    md_lines.append("## Fully Aligned\n")
    if categories["fully_aligned"]:
        md_lines += [f"- `{f}`" for f in categories["fully_aligned"]]
    else:
        md_lines.append("None")

    md_lines.append("\n## Partially Aligned (registered but missing references)\n")
    if categories["partially_aligned"]:
        md_lines += [f"- `{f}`" for f in categories["partially_aligned"]]
    else:
        md_lines.append("None")

    md_lines.append("\n## Unlinked / Unregistered\n")
    if categories["unlinked"]:
        md_lines += [f"- `{f}`" for f in categories["unlinked"]]
    else:
        md_lines.append("None")

    summary = report_data["summary"]
    md_lines.append("\n## Summary\n")
    md_lines.append(f"- Total project MD files: {summary['total_files']}")
    md_lines.append(f"- Fully aligned: {summary['fully_aligned']}")
    md_lines.append(f"- Partially aligned: {summary['partially_aligned']}")
    md_lines.append(f"- Unlinked: {summary['unlinked']}\n")
    md_lines.append("**Note:** Generated automatically. Do not overwrite manually.\n")

    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(md_lines))

def main():
    trace_index = load_and_normalize_trace_index()
    project_files = scan_project_files()
    files_report, full, partial, unlinked_count = classify_files(trace_index, project_files)
    report_data = {
        "files": files_report,
        "summary": {
            "total_files": len(project_files),
            "fully_aligned": full,
            "partially_aligned": partial,
            "unlinked": unlinked_count,
        },
    }
    write_json_report(report_data)
    write_md_report(report_data)
    print(f"Generated {OUTPUT_JSON} and {OUTPUT_MD}")
    return 0

if __name__ == "__main__":
    main()