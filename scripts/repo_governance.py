# ID: OPS-024
#!/usr/bin/env python3
import os
import re
import json
import argparse
import sys
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "project" / "reports"
SCRIPTS_DIR = ROOT / "scripts"

JSON_OUTPUT = SCRIPTS_DIR / "lint_governance_links.json"
MD_OUTPUT = REPORTS_DIR / "PROJECT_DOCUMENT_ALIGNMENT.md"
TRACE_INDEX = ROOT / "TRACE_INDEX.yml"

# Regex patterns
MD_PATTERN = re.compile(r"\[.*?\]\((project/.*?\.md)\)")

def load_trace_index():
    """Read TRACE_INDEX.yml for registered project files."""
    if not TRACE_INDEX.exists():
        return set()
    registered = set()
    with TRACE_INDEX.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith("project/") and line.endswith(".md"):
                registered.add(line.split()[0])
    return registered

def scan_project_md_files():
    """Return all .md files under project/."""
    return {str(p.relative_to(ROOT)) for p in ROOT.glob("project/**/*.md")}

def extract_links_from_file(path):
    """Extract markdown links to project/*.md files from a file."""
    text = path.read_text(errors="ignore")
    return set(MD_PATTERN.findall(text))

def build_alignment():
    """Produce alignment data structures."""
    registered = load_trace_index()
    all_files = scan_project_md_files()

    references = {}
    for md in all_files:
        links = extract_links_from_file(ROOT / md)
        for target in links:
            references.setdefault(target, set()).add(md)

    fully_aligned, partially_aligned, unlinked = {}, {}, {}

    for md in sorted(all_files):
        refs = references.get(md, set())
        is_registered = md in registered
        if is_registered and refs:
            fully_aligned[md] = sorted(refs)
        elif is_registered and not refs:
            unlinked[md] = "Registered"
        elif not is_registered and refs:
            partially_aligned[md] = sorted(refs)
        else:
            unlinked[md] = "Unregistered"

    summary = {
        "total_files": len(all_files),
        "fully_aligned": len(fully_aligned),
        "partially_aligned": len(partially_aligned),
        "unlinked": len(unlinked),
    }

    return fully_aligned, partially_aligned, unlinked, summary

def write_json(fully, partial, unlinked, summary):
    data = {
        "fully_aligned": fully,
        "partially_aligned": partial,
        "unlinked": unlinked,
        "summary": summary,
    }
    with JSON_OUTPUT.open("w") as f:
        json.dump(data, f, indent=4)

def write_markdown(fully, partial, unlinked, summary):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with MD_OUTPUT.open("w") as f:
        f.write("# Project Document Alignment Report\n\n")
        f.write("_Generated automatically by repo_governance.py_\n\n")

        f.write("## Fully Aligned\n\n")
        if fully:
            for md, refs in fully.items():
                f.write(f"- `{md}`\n")
                for r in refs:
                    f.write(f"    - Present in: {r}\n")
        else:
            f.write("None\n")
        f.write("\n")

        f.write("## Partially Aligned (linked but unregistered)\n\n")
        if partial:
            for md, refs in partial.items():
                f.write(f"- `{md}`\n")
                for r in refs:
                    f.write(f"    - Present in: {r}\n")
        else:
            f.write("None\n")
        f.write("\n")

        f.write("## Unlinked / Unregistered\n\n")
        if unlinked:
            for md, status in unlinked.items():
                f.write(f"- `{md}` ({status})\n")
        else:
            f.write("None\n")
        f.write("\n")

        f.write("## Summary\n\n")
        f.write(f"- Total project MD files: {summary['total_files']}\n")
        f.write(f"- Fully aligned: {summary['fully_aligned']}\n")
        f.write(f"- Partially aligned: {summary['partially_aligned']}\n")
        f.write(f"- Unlinked / unregistered: {summary['unlinked']}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", help="Generate full alignment reports")
    parser.add_argument("--enforce", action="store_true", help="Exit non-zero if misaligned")
    args = parser.parse_args()

    fully, partial, unlinked, summary = build_alignment()

    if args.audit:
        write_json(fully, partial, unlinked, summary)
        write_markdown(fully, partial, unlinked, summary)
        print(f"[INFO] Audit complete. JSON: {JSON_OUTPUT}, MD: {MD_OUTPUT}")
        return 0

    if args.enforce:
        if summary["partially_aligned"] > 0 or summary["unlinked"] > 0:
            print("[ERROR] Governance misalignment detected. Run with --audit for details.")
            return 1
        return 0

    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())
