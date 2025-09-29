#!/usr/bin/env python3
"""
Lint Governance Links – Generate project alignment report.
"""

import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
REPORT_MD = PROJECT_ROOT / "project" / "reports" / "PROJECT_DOCUMENT_ALIGNMENT.md"
REPORT_JSON = PROJECT_ROOT / "scripts" / "lint_governance_links.json"

def collect_md_files():
    # Only project/*/*.md files, exclude archive and logs
    files = []
    for p in PROJECT_ROOT.glob("project/*/*.md"):
        if "archive" in str(p) or "logs" in str(p):
            continue
        files.append(p.relative_to(PROJECT_ROOT).as_posix())
    return files

def generate_report():
    files = collect_md_files()
    # Simulated alignment logic; adapt to your repo specifics
    report = {
        "files": [
            {"path": f, "status": "fully_aligned" if "ALIGNMENT_MATRIX" in f else "unlinked"}
            for f in files
        ],
        "summary": {
            "total_files": len(files),
            "fully_aligned": sum(1 for f in files if "ALIGNMENT_MATRIX" in f),
            "partially_aligned": 0,
            "unlinked": sum(1 for f in files if "ALIGNMENT_MATRIX" not in f),
        }
    }
    return report

def write_reports(report):
    # JSON output
    REPORT_JSON.write_text(json.dumps(report, indent=4))
    print(f"Wrote JSON report to {REPORT_JSON}")

    # Markdown output
    md_content = "# Project Document Alignment Report\n\n"
    md_content += f"Total files: {report['summary']['total_files']}\n\n"
    md_content += "## Files\n"
    for f in report["files"]:
        md_content += f"- `{f['path']}` ({f['status']})\n"
    REPORT_MD.write_text(md_content)
    print(f"Wrote Markdown report to {REPORT_MD}")

if __name__ == "__main__":
    report = generate_report()
    write_reports(report)
    unlinked_count = report['summary']['unlinked']
    if unlinked_count > 0:
        print(f"\nLinter failed: Found {unlinked_count} unlinked documents.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)