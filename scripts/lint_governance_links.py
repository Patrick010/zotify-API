#!/usr/bin/env python3
import json
from pathlib import Path
import sys

# Configuration
PROJECT_DIR = Path("project")
REPORT_MD = PROJECT_DIR / "reports" / "PROJECT_DOCUMENT_ALIGNMENT.md"
REPORT_JSON = Path("scripts") / "lint_governance_links.json"

# Load project registry
def load_registry():
    registry_file = PROJECT_DIR / "PROJECT_REGISTRY.md"
    registered_files = set()
    with open(registry_file, "r") as f:
        for line in f:
            if ".md" in line:
                parts = line.strip().split("](")
                if len(parts) > 1:
                    file_path = parts[1].rstrip(")")
                    if file_path.startswith("project/") and file_path.endswith(".md"):
                        registered_files.add(file_path)
    return registered_files

# Build reference map for all MD files
def build_reference_map():
    ref_map = {}
    for md_file in PROJECT_DIR.rglob("*.md"):
        file_path = str(md_file.relative_to(Path.cwd()))
        with open(md_file, "r") as f:
            content = f.read()
        refs = set()
        for line in content.splitlines():
            if "(" in line and ".md" in line:
                start = line.find("(") + 1
                end = line.find(")", start)
                ref_file = line[start:end]
                if ref_file.startswith("project/") and ref_file.endswith(".md"):
                    refs.add(ref_file)
        ref_map[file_path] = refs
    return ref_map

# Check alignment
def check_alignment(md_files, registry_files):
    reference_map = build_reference_map()
    fully_aligned = []
    partially_aligned = []
    unlinked = []

    expected_refs = {
        "project/ALIGNMENT_MATRIX.md": registry_files,
        "project/ROADMAP.md": registry_files,
        "project/PROPOSALS.md": registry_files,
    }

    for f in md_files:
        path = f
        if path not in registry_files:
            unlinked.append({"file": path, "registered": False})
        else:
            missing_in = []
            for key_file, expected_files in expected_refs.items():
                if path not in reference_map.get(key_file, set()):
                    missing_in.append(key_file)
            if missing_in:
                partially_aligned.append({"file": path, "registered": True, "missing_in": missing_in})
            else:
                fully_aligned.append({"file": path, "registered": True})

    return fully_aligned, partially_aligned, unlinked

# Gather all project MD files
def get_project_md_files():
    return [str(f.relative_to(Path.cwd())) for f in PROJECT_DIR.rglob("*.md")]

def generate_md_report(fully, partial, unlinked):
    lines = ["# Project Document Alignment Report\n"]
    # Fully aligned
    lines.append("## Fully Aligned\n")
    if fully:
        for f in fully:
            lines.append(f"- `{f['file']}`")
    else:
        lines.append("None\n")
    # Partially aligned
    lines.append("\n## Partially Aligned (registered but missing references)\n")
    if partial:
        for f in partial:
            missing = ", ".join(f["missing_in"])
            lines.append(f"- `{f['file']}`\n    - Missing in: {missing}")
    else:
        lines.append("None\n")
    # Unlinked / unregistered
    lines.append("\n## Unlinked / Unregistered\n")
    if unlinked:
        for f in unlinked:
            reg_status = "Registered" if f["registered"] else "Unregistered"
            lines.append(f"- `{f['file']}` ({reg_status})")
    else:
        lines.append("None\n")
    # Summary
    total_files = len(fully) + len(partial) + len(unlinked)
    lines.append("\n## Summary\n")
    lines.append(f"- Total project MD files: {total_files}")
    lines.append(f"- Fully aligned: {len(fully)}")
    lines.append(f"- Partially aligned: {len(partial)}")
    lines.append(f"- Unlinked / unregistered: {len(unlinked)}\n")
    lines.append("*Produced by lint_governance_links.py*")
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_MD, "w") as f:
        f.write("\n".join(lines))

def generate_json_report(fully, partial, unlinked):
    data = {
        "fully_aligned": fully,
        "partially_aligned": partial,
        "unlinked": unlinked,
        "summary": {
            "total_files": len(fully) + len(partial) + len(unlinked),
            "fully_aligned": len(fully),
            "partially_aligned": len(partial),
            "unlinked": len(unlinked)
        }
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_JSON, "w") as f:
        json.dump(data, f, indent=4)

def main():
    registry_files = load_registry()
    md_files = get_project_md_files()
    fully, partial, unlinked = check_alignment(md_files, registry_files)
    generate_md_report(fully, partial, unlinked)
    generate_json_report(fully, partial, unlinked)
    # Exit code: 0 if fully aligned or only partially aligned, 1 if unlinked exists
    if unlinked:
        print("Found unlinked / unregistered files. See report for details.")
        sys.exit(1)
    else:
        print("All project files are registered and references exist.")

if __name__ == "__main__":
    main()
