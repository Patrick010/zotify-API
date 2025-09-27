import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict

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
IGNORED_FILES = {"LICENSE", "mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md"}
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
    path_obj = Path(filepath)
    if path_obj.name.startswith(".") or path_obj.name in IGNORED_FILES:
        return "other"
    return FILETYPE_MAP.get(path_obj.suffix, "other")

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
            if relative_path in IGNORED_FILES:
                continue
            all_files.append(relative_path)
    return all_files

def is_stub_file(filepath: str, file_type: str) -> bool:
    """Checks if a file is a stub based on size, content, or structure."""
    full_path = PROJECT_ROOT / filepath
    try:
        if full_path.stat().st_size < 50:
            return True

        content = full_path.read_text(encoding="utf-8").strip()
        if not content:
            return True

        if any(re.search(r'\b' + keyword + r'\b', content, re.IGNORECASE) for keyword in STUB_KEYWORDS):
            return True

        if file_type in ["code", "script"]:
            if filepath.endswith(".py"):
                if ("def " in content and " pass" in content) or ("class " in content and " pass" in content):
                    lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
                    if len(lines) < 5:
                        return True
            elif filepath.endswith(".sh"):
                lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
                if not lines or (len(lines) == 1 and lines[0].startswith("#!")):
                    return True

        elif file_type == "doc" and filepath.endswith((".md", ".rst")):
            lines = [line for line in content.splitlines() if line.strip()]
            if len(lines) <= 2 and (lines[0].startswith("#") or "===" in lines[0] or "---" in lines[0]):
                return True

    except (IOError, UnicodeDecodeError):
        return False
    return False

def parse_markdown_index(index_path: Path) -> Set[str]:
    """Parses a markdown file and extracts all file paths from links or tables."""
    if not index_path.exists():
        return set()

    content = index_path.read_text(encoding="utf-8")

    table_paths = re.findall(r"\|\s*`([^`]+)`\s*\|", content)
    resolved_paths = set(table_paths)

    link_paths = re.findall(r"\[[^\]]+\]\((?!https?:\/\/)([^)]+)\)", content)
    for path_str in link_paths:
        try:
            absolute_path = (index_path.parent / path_str).resolve()
            relative_path = str(absolute_path.relative_to(PROJECT_ROOT))
            resolved_paths.add(relative_path)
        except (ValueError, FileNotFoundError):
            pass

    return resolved_paths

def generate_audit_report(results: List[Dict[str, Any]], report_path: Path):
    """Generates and saves a detailed markdown audit report with fix suggestions."""
    summary = defaultdict(int)
    summary['total_files'] = len(results)

    report_lines = [
        "# Governance Audit Report",
        f"**Date:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "\n| Path | File Type | Status | Details |",
        "|------|-----------|--------|---------|"
    ]

    issues = []
    for result in sorted(results, key=lambda x: x['path']):
        status_flags = []
        is_ok = not (result['is_missing'] or result['is_miscategorized'])

        if result['is_missing']:
            summary['missing_index'] += 1
            status_flags.append("Missing Index")
        if result['is_miscategorized']:
            summary['miscategorized'] += 1
            status_flags.append("Miscategorized")
        if result['is_stub']:
            summary['stub'] += 1
            status_flags.append("Stub")

        if is_ok:
            summary['ok'] += 1
            status_flags.append("OK")
        else:
            issues.append(result)

        status_str = ", ".join(sorted(status_flags))

        details = []
        if result['is_missing']:
            details.append(f"Expected in: `{', '.join(result['expected_indexes'])}`")
        if result['is_miscategorized']:
            incorrect_indexes = [idx for idx in result['found_in'] if idx not in result['all_valid_for_type']]
            details.append(f"Incorrectly in: `{', '.join(incorrect_indexes)}`")

        details_str = "<br>".join(details)
        report_lines.append(f"| `{result['path']}` | {result['type']} | {status_str} | {details_str} |")

    summary_lines = [
        "\n## Summary Statistics",
        f"- **Total Files Scanned:** {summary['total_files']}",
        f"- **Files OK:** {summary['ok']}",
        f"- **Files Missing from Index:** {summary['missing_index']}",
        f"- **Files Miscategorized:** {summary['miscategorized']}",
        f"- **Files Flagged as Stubs:** {summary['stub']}",
    ]

    fix_suggestions_lines = ["\n## Index Fix Suggestions"]
    if not issues:
        fix_suggestions_lines.append("No missing or miscategorized files detected.")
    else:
        suggestions_by_index = defaultdict(list)
        for issue in issues:
            if not issue['is_missing']:
                continue

            for target_index in issue['expected_indexes']:
                if target_index in issue['found_in']:
                    continue

                reason = "Missing from required index."
                if issue['is_miscategorized']:
                    incorrect_in = [idx for idx in issue['found_in'] if idx not in issue['all_valid_for_type']]
                    reason += f" Also found in incorrect index(es): `{', '.join(incorrect_in)}`."

                file_type_display = issue['type'].capitalize()
                entry = f"| `{issue['path']}` | {file_type_display} | TBD | Active | | Auto-generated to fix audit |"

                suggestion = (
                    f"- **File**: `{issue['path']}`\n"
                    f"  **Expected Index**: `{target_index}`\n"
                    f"  **Suggested Entry**: `{entry}`\n"
                    f"  **Reason**: {reason}"
                )
                suggestions_by_index[target_index].append(suggestion)

        for index_file, suggestions in sorted(suggestions_by_index.items()):
            fix_suggestions_lines.append(f"\n### Suggestions for `{index_file}`\n")
            fix_suggestions_lines.extend(suggestions)

    report_content = "\n".join(report_lines + summary_lines + fix_suggestions_lines)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_content, encoding="utf-8")
    print(f"Audit report saved to: {report_path}")

def main():
    """Main function to run the governance audit."""
    all_files = find_all_files()
    all_indexes = set(idx for indices in INDEX_MAP.values() for idx in indices)
    all_indexes_content = {
        str(p): parse_markdown_index(PROJECT_ROOT / p) for p in all_indexes
    }

    audit_results = []
    for file_path in all_files:
        file_type = get_file_type(file_path)
        if file_type == "other":
            continue

        is_stub = is_stub_file(file_path, file_type)

        expected_indexes = INDEX_MAP.get(file_type, [])
        if file_type == "doc":
            possible = [idx for idx in expected_indexes if file_path.startswith(str(Path(idx).parent))]
            if not possible and "project/" in file_path:
                possible = ["project/PROJECT_REGISTRY.md"]
            expected_indexes = possible

        found_in = {idx for idx, files in all_indexes_content.items() if file_path in files}
        all_valid_for_type = set(INDEX_MAP.get(file_type, []))

        is_missing = bool(expected_indexes) and not any(idx in found_in for idx in expected_indexes)
        is_miscategorized = any(idx not in all_valid_for_type for idx in found_in)

        audit_results.append({
            "path": file_path,
            "type": file_type,
            "expected_indexes": expected_indexes,
            "all_valid_for_type": all_valid_for_type,
            "found_in": found_in,
            "is_missing": is_missing,
            "is_miscategorized": is_miscategorized,
            "is_stub": is_stub,
        })

    report_path = PROJECT_ROOT / "project/reports/GOVERNANCE_AUDIT_REPORT.md"
    generate_audit_report(audit_results, report_path)

    has_errors = any(r['is_missing'] or r['is_miscategorized'] for r in audit_results)
    if has_errors:
        print("Audit complete. Errors found (missing or miscategorized files).")
        sys.exit(1)
    else:
        print("Audit complete. All files compliant.")
        sys.exit(0)

if __name__ == "__main__":
    main()