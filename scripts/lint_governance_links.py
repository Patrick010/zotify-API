#!/usr/bin/env python3
"""
Lint Governance Links - Automatically checks all project Markdown files
and generates JSON and human-readable alignment reports.
"""

import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent
ALIGNMENT_MATRIX_FILE = PROJECT_ROOT / "project/ALIGNMENT_MATRIX.md"
OUTPUT_JSON = PROJECT_ROOT / "scripts/lint_governance_links.json"
OUTPUT_MD = PROJECT_ROOT / "project/reports/PROJECT_DOCUMENT_ALIGNMENT.md"

def load_registered_files():
    """Parse ALIGNMENT_MATRIX.md to get all registered files."""
    registered = set()
    if not ALIGNMENT_MATRIX_FILE.exists():
        print("WARNING: ALIGNMENT_MATRIX.md not found. Treating all files as unlinked.")
        return registered

    with open(ALIGNMENT_MATRIX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("project/") and line.endswith(".md"):
                registered.add(line)
    return registered

def scan_project_files():
    """Scan project for all Markdown files under project/, excluding archive/logs."""
    files = []
    for path in PROJECT_ROOT.glob("project/**/*.md"):
        if "archive" in path.parts or "logs" in path.parts:
            continue
        files.append(str(path.relative_to(PROJECT_ROOT)))
    return files

def generate_reports():
    """
    Generates JSON and Markdown reports detailing the alignment status of project documents.
    Exits with a non-zero status code if any unlinked documents are found.
    """
    registered = load_registered_files()
    all_files = scan_project_files()

    files_report = []
    summary = {"total_files": len(all_files), "fully_aligned": 0, "partially_aligned": 0, "unlinked": 0}

    has_unlinked = False
    for f in all_files:
        status = "fully_aligned" if f in registered else "unlinked"
        files_report.append({"path": f, "status": status})
        if status == "fully_aligned":
            summary["fully_aligned"] += 1
        else:
            summary["unlinked"] += 1
            has_unlinked = True

    # JSON output
    data = {"files": files_report, "summary": summary}
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f_json:
        json.dump(data, f_json, indent=4)

    # Markdown output
    md_lines = ["# Project Document Alignment Report\n"]
    md_lines.append("## Summary\n")
    md_lines.append(f"- Total files: {summary['total_files']}")
    md_lines.append(f"- Fully aligned: {summary['fully_aligned']}")
    md_lines.append(f"- Partially aligned: {summary['partially_aligned']}")
    md_lines.append(f"- Unlinked: {summary['unlinked']}\n")

    md_lines.append("## Files\n")
    for file_entry in files_report:
        md_lines.append(f"- `{file_entry['path']}` - {file_entry['status']}")

    md_lines.append("\n**Note:** Produced by `lint_governance_links.py`. Use `PROJECT_AUDIT_FINAL_REPORT.md` for review purposes.")

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f_md:
        f_md.write("\n".join(md_lines))

    print(f"Reports generated: {OUTPUT_JSON} and {OUTPUT_MD}")

    if has_unlinked:
        print("\nError: Found unlinked project documents.", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(generate_reports())