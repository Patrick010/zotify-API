import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
FILETYPE_MAP = {
    ".sh": "script",
    ".py": "code",
    ".go": "code",
    ".md": "doc",
    ".rst": "doc",
    ".txt": "doc",
    ".yml": "config",
    ".yaml": "config",
    ".json": "config",
}
IGNORED_DIRS = {".git", ".idea", "venv", "node_modules", "build", "dist", "target", "__pycache__"}
IGNORED_FILES = {"mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md", "LICENSE"}
STUB_KEYWORDS = {"TODO", "placeholder", "stub", "TBD"}

# Consolidated index for all code, scripts, and configs
CODE_INDEX_FILE = "api/docs/CODE_FILE_INDEX.md"

# Mapping of file types to their required index files
INDEX_MAP = {
    "doc": [
        "project/PROJECT_REGISTRY.md",
        "api/docs/MASTER_INDEX.md",
        "Gonk/GonkCLI/DOCS_INDEX.md",
        "Gonk/GonkUI/DOCS_INDEX.md",
        "snitch/DOCS_INDEX.md",
    ],
    "code": [CODE_INDEX_FILE],
    "script": [CODE_INDEX_FILE],
    "config": [CODE_INDEX_FILE],
}

def get_file_type(filepath: str) -> str:
    """Classifies a file based on its extension."""
    if Path(filepath).name.startswith(".") or Path(filepath).name in IGNORED_FILES:
        return "other"
    ext = Path(filepath).suffix
    return FILETYPE_MAP.get(ext, "other")

def find_all_files() -> List[str]:
    """Scans the project root for all files, respecting IGNORED_DIRS."""
    all_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            full_path = Path(root) / file
            if any(part in IGNORED_DIRS for part in full_path.parts):
                continue
            relative_path = str(full_path.relative_to(PROJECT_ROOT))
            all_files.append(relative_path)
    return all_files

def is_stub_file(filepath: str, file_type: str) -> bool:
    """Checks if a file is a stub based on size, content, or structure."""
    full_path = PROJECT_ROOT / filepath
    try:
        if full_path.stat().st_size < 50:
            return True

        content = full_path.read_text(encoding="utf-8")
        if any(re.search(r'\b' + keyword + r'\b', content, re.IGNORECASE) for keyword in STUB_KEYWORDS):
            return True

        if file_type in ["code", "script"]:
            # Check for empty functions/classes in Python
            if filepath.endswith(".py"):
                if "def " in content and " pass" in content and len(content.splitlines()) < 10:
                     # crude check for scripts with just a pass
                    if content.strip().count('pass') > 0 and len(content.strip().split()) < 5:
                        return True
                if "class " in content and " pass" in content and len(content.splitlines()) < 10:
                    return True


            # Check for empty shell scripts
            if filepath.endswith(".sh") and content.strip() in ["", "#!/bin/bash", "#!/bin/sh"]:
                return True

        if file_type == "doc" and filepath.endswith((".md", ".rst")):
            # Check for markdown/rst with only a title
            lines = [line for line in content.splitlines() if line.strip()]
            if len(lines) <= 2 and (lines[0].strip().startswith("#") or lines[0].strip().startswith("=")):
                return True

    except (IOError, UnicodeDecodeError):
        return False # Cannot read file, assume not a stub
    return False

def parse_markdown_index(index_path: Path) -> Set[str]:
    """Parses a markdown file and extracts all linked paths or table rows."""
    if not index_path.exists():
        return set()
    content = index_path.read_text(encoding="utf-8")
    # Regex for `path` in markdown tables
    paths = re.findall(r"\|\s*`([^`]+)`\s*\|", content)
    # Regex for [text](link)
    links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)

    resolved_paths = set(paths)
    for link in links:
        try:
            # Resolve path relative to the index file's location
            resolved = (index_path.parent / link).resolve().relative_to(PROJECT_ROOT)
            resolved_paths.add(str(resolved))
        except (ValueError, FileNotFoundError):
            # Ignore broken or external links
            pass

    return resolved_paths

def generate_audit_report(results: List[Dict[str, Any]], report_path: Path):
    """Generates and saves a detailed markdown audit report."""
    summary = {
        "total_files": len(results),
        "ok": 0,
        "missing_index": 0,
        "miscategorized": 0, # Placeholder for future implementation
        "stub": 0,
    }

    report_lines = [
        "# Governance Audit Report",
        f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n| Path | File Type | Index(es) | Status |",
        "|------|-----------|-----------|--------|"
    ]

    for result in sorted(results, key=lambda x: x['path']):
        status_flags = []
        if result['status'] == 'ok':
            summary['ok'] += 1
            status_flags.append("OK")
        if result['status'] == 'missing':
            summary['missing_index'] += 1
            status_flags.append("Missing Index")
        if result['is_stub']:
            summary['stub'] += 1
            status_flags.append("Stub/Placeholder")

        status_str = ", ".join(status_flags)

        index_str = "<br>".join(result['expected_indexes']) if result['expected_indexes'] else "N/A"

        report_lines.append(f"| `{result['path']}` | {result['type']} | {index_str} | {status_str} |")

    # --- Summary Section ---
    summary_lines = [
        "\n## Summary Statistics",
        f"- **Total Files Scanned:** {summary['total_files']}",
        f"- **Files OK:** {summary['ok']}",
        f"- **Files Missing from Index:** {summary['missing_index']}",
        f"- **Files Flagged as Stubs:** {summary['stub']}",
        f"- **Files Miscategorized:** {summary['miscategorized']} (Detection not yet implemented)",
    ]

    report_content = "\n".join(report_lines + summary_lines)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_content, encoding="utf-8")
    print(f"Audit report saved to: {report_path}")

def main():
    """Main function to run the governance audit."""
    all_files = find_all_files()
    all_indexes_content = {
        str(p): parse_markdown_index(PROJECT_ROOT / p)
        for p in set(idx for indices in INDEX_MAP.values() for idx in indices)
    }

    audit_results = []

    for file_path in all_files:
        file_type = get_file_type(file_path)
        if file_type == "other":
            continue # Skip files we don't classify

        is_stub = is_stub_file(file_path, file_type)

        expected_indexes = INDEX_MAP.get(file_type, [])

        # Doc files can exist in multiple places, we need to find the correct index
        if file_type == "doc":
            possible_indexes = [idx for idx in expected_indexes if file_path.startswith(str(Path(idx).parent))]
            if not possible_indexes and "project/" in file_path:
                 possible_indexes = ["project/PROJECT_REGISTRY.md"] # Default for project docs
            expected_indexes = possible_indexes


        is_registered = False
        if expected_indexes:
            # A file is considered registered if it appears in ANY of its potential indexes
            for index_file in expected_indexes:
                if file_path in all_indexes_content.get(index_file, set()):
                    is_registered = True
                    break

        status = 'ok'
        if not is_registered and expected_indexes:
            status = 'missing'

        audit_results.append({
            "path": file_path,
            "type": file_type,
            "expected_indexes": expected_indexes,
            "status": status,
            "is_stub": is_stub,
        })

    # Generate the final report
    report_path = PROJECT_ROOT / "project/reports/GOVERNANCE_AUDIT_REPORT.md"
    generate_audit_report(audit_results, report_path)

    # For linter integration, we can return an exit code if issues are found
    if any(r['status'] != 'ok' or r['is_stub'] for r in audit_results):
        print("Audit complete. Issues found.")
        sys.exit(1)
    else:
        print("Audit complete. All files compliant.")
        sys.exit(0)

if __name__ == "__main__":
    main()