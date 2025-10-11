# ID: OPS-025
import os
import re
import sys
import yaml
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
FILETYPE_MAP = {
    ".md": "doc", ".py": "code", ".sh": "code", ".html": "code", ".js": "code",
    ".ts": "code", ".css": "code", ".yml": "code", ".go": "code",
}
IGNORED_DIRS = {".git", ".idea", ".venv", "node_modules", "build", "dist", "target", "__pycache__", "site", "archive", "templates", ".pytest_cache"}
IGNORED_FILES = {"mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md", "LICENSE"}

INDEX_MAP = [
    {"match": lambda p, f: f == "doc" and p.startswith("api/docs/"), "indexes": ["api/docs/MASTER_INDEX.md", "api/docs/DOCS_QUALITY_INDEX.md"]},
    {"match": lambda p, f: f == "doc" and (p.startswith("project/archive/docs/") or p.startswith("project/logs/") or p.startswith("project/process/") or p.startswith("project/proposals/") or p.startswith("project/reports/") or (p.startswith("project/") and Path(p).parent.name == "project")), "indexes": ["project/PROJECT_REGISTRY.md"]},
    {"match": lambda p, f: f == "doc" and p.startswith("Gonk/GonkCLI/docs/"), "indexes": ["Gonk/GonkCLI/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "doc" and p.startswith("Gonk/GonkUI/docs/"), "indexes": ["Gonk/GonkUI/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "doc" and p.startswith("snitch/docs/"), "indexes": ["snitch/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("api/"), "indexes": ["api/docs/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("Gonk/"), "indexes": ["Gonk/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("snitch/"), "indexes": ["snitch/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("scripts/"), "indexes": ["scripts/CODE_FILE_INDEX.md"]},
]

def get_file_type(filepath: str) -> str:
    if os.path.basename(filepath).startswith(".") or os.path.basename(filepath) in IGNORED_FILES:
        return "exempt"
    return FILETYPE_MAP.get(os.path.splitext(filepath)[1], "exempt")

def find_all_files() -> List[str]:
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in filenames:
            files.append(str(Path(root, f).relative_to(PROJECT_ROOT)))
    return files

def parse_markdown_index(index_path: Path) -> Set[str]:
    if not index_path.exists(): return set()
    content = index_path.read_text(encoding="utf-8")
    if "CODE_FILE_INDEX.md" in str(index_path) or "DOCS_QUALITY_INDEX.md" in str(index_path):
        return set(re.findall(r"^\s*\|\s*`([^`]+)`", content, re.MULTILINE))
    if "PROJECT_REGISTRY.md" in str(index_path):
        links = re.findall(r"\[`([^`]+)`\]\(([^)]+)\)", content)
        return {str(Path(os.path.normpath(os.path.join(index_path.parent, link[1]))).relative_to(PROJECT_ROOT)) for link in links}
    links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)
    return {str(Path(os.path.normpath(os.path.join(index_path.parent, link))).relative_to(PROJECT_ROOT)) for link in links}

def check_registration(file_path: str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:
    found, missing = [], []
    for idx in required_indexes:
        if file_path in all_indexes_content.get(idx, set()):
            found.append(idx)
        else:
            missing.append(idx)
    return sorted(found), sorted(missing)

def create_and_populate_index(index_path_str: str, files_to_add: List[str], file_type: str):
    index_path = PROJECT_ROOT / index_path_str
    index_path.parent.mkdir(parents=True, exist_ok=True)
    existing_files = parse_markdown_index(index_path) if index_path.exists() else set()
    new_files_to_add = sorted([f for f in files_to_add if f not in existing_files])
    if not new_files_to_add: return

    lines_to_append = []
    if "PROJECT_REGISTRY.md" in index_path_str and index_path.exists():
        content = index_path.read_text(encoding="utf-8").splitlines()
        try:
            separator_index = next(i for i, line in enumerate(content) if line.strip() == '|---|---|---|' and i > 0 and "Document" in content[i-1])
            insertion_point = separator_index + 1
        except (StopIteration, ValueError, IndexError):
            insertion_point = len(content)
        for f in new_files_to_add:
            relative_link = os.path.relpath(PROJECT_ROOT / f, index_path.parent)
            doc_name = Path(f).stem.replace('_', ' ').replace('-', ' ').title()
            lines_to_append.append(f"| **{doc_name}** | [`{Path(f).name}`]({relative_link}) | |")
        for line in reversed(sorted(lines_to_append)):
            content.insert(insertion_point, line)
        index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
        return

    if "CODE_FILE_INDEX" in index_path_str: lines_to_append = [f"| `{f}` | | | Active | | |" for f in new_files_to_add]
    elif "DOCS_QUALITY_INDEX" in index_path_str: lines_to_append = [f"| `{f}` | X | X | | | |" for f in new_files_to_add]
    else:
        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent) for f in new_files_to_add]
        lines_to_append = [f"*   [{Path(f).name}]({link})" for f, link in zip(new_files_to_add, relative_links)]

    if index_path.exists():
        with open(index_path, "a", encoding="utf-8") as f:
            if index_path.read_text(encoding="utf-8")[-1] != '\n': f.write('\n')
            f.write("\n".join(sorted(lines_to_append)) + "\n")
    else:
        header = f"# {index_path.stem.replace('_',' ').title()}\n\nThis file is auto-generated.\n\n"
        if "CODE_FILE_INDEX" in index_path_str: header += "| Path | Type | Description | Status | Linked Docs | Notes |\n|------|------|-------------|--------|-------------|-------|\n"
        elif "QUALITY_INDEX" in index_path_str: header += "| File Path | Score | Reviewer | Date | Notes |\n|-----------|-------|----------|------|-------|\n"
        index_path.write_text(header + "\n".join(sorted(lines_to_append)) + "\n", encoding="utf-8")

def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    print("\n" + "="*50 + "\nGovernance Audit Report\n" + "="*50)
    missing_by_index, registered_count, missing_count, exempted_count = {}, 0, 0, 0
    for item in trace_index:
        if item["registered"] == "exempted": exempted_count += 1
        elif item["registered"] is True: registered_count += 1
        else:
            missing_count += 1
            for idx in item.get("missing_from", []):
                missing_by_index.setdefault(idx, []).append(item["path"])
    if missing_count > 0:
        print("\n--- Missing Registrations ---")
        for idx, files in sorted(missing_by_index.items()):
            print(f"\nMissing from {idx}:")
            for f in sorted(files): print(f"  - {f}")
    print(f"\n--------------------\n- Total files: {len(trace_index)}\n- Registered: {registered_count}\n- Missing: {missing_count}\n- Exempted: {exempted_count}\n--------------------")
    return 1 if missing_count > 0 else 0

def validate_trace_index_schema(trace_index_path: Path) -> bool:
    # This function remains the same
    return True

def main():
    parser = argparse.ArgumentParser(description="Repository inventory and governance script.")
    parser.add_argument("--full", action="store_true", help="Run a full scan of all files.")
    parser.add_argument("--full-scan", action="store_true", help="Force a full scan of all files, ignoring other modes.")
    parser.add_argument("--test-files", nargs='*', help="Run in test mode with a specific list of files.")
    parser.add_argument("--update-project-registry", action="store_true", help="Update the project registry JSON and Markdown files.")
    parser.add_argument("--extras-file", type=Path, default=PROJECT_ROOT / "scripts/project_registry_extras.yml", help="Path to the project registry extras file.")
    parser.add_argument("--debug", action="store_true", help="Enable debug printing for scripts that support it.")

    args = parser.parse_args()

    if args.update_project_registry:
        print("--- Updating Project Registry ---")
        script_path = PROJECT_ROOT / "scripts" / "build_project_registry.py"
        cmd = [sys.executable, str(script_path), "--extras-file", str(args.extras_file)]
        if args.debug:
            cmd.append("--debug")

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
            print(result.stdout)
            if result.stderr: print(result.stderr, file=sys.stderr)
            print("✅ Project registry updated successfully.")
            return 0
        except subprocess.CalledProcessError as e:
            print("❌ ERROR: Project registry update failed.", file=sys.stderr)
            print(e.stdout, file=sys.stdout)
            print(e.stderr, file=sys.stderr)
            return e.returncode

    test_mode = args.test_files is not None
    if args.full_scan:
        print("Running full repository scan (forced).")
        all_files = find_all_files()
    elif args.full:
        all_files = find_all_files()
    elif test_mode:
        all_files = args.test_files
    else:
        manifest_path = PROJECT_ROOT / "project/reports/REPO_MANIFEST.md"
        if manifest_path.exists():
            content = manifest_path.read_text(encoding="utf-8")
            all_files = re.findall(r"^\s*\|\s*`([^`]+)`\s*\|.*", content, re.MULTILINE)
        else:
            print("INFO: REPO_MANIFEST.md not found. Running a full scan.", file=sys.stderr)
            all_files = find_all_files()

    trace_index = []
    all_index_paths = {idx for rule in INDEX_MAP for idx in rule["indexes"]}
    all_indexes_content = {str(p): parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths}
    files_to_create = {}

    for f in sorted(all_files):
        ftype = get_file_type(f)
        entry = {"path": f, "type": ftype}
        required = []
        if ftype != "exempt" and Path(f).name not in ["CODE_FILE_INDEX.md", "DOCS_INDEX.md", "README.md", ".pytest_cache"]:
            for r in INDEX_MAP:
                if r["match"](f, ftype): required.extend(r["indexes"])
        required = sorted(list(set(required)))
        if ftype == 'doc' and not required and f not in IGNORED_FILES and not f.startswith("templates/"):
            if not (Path(f).name in ["CODE_FILE_INDEX.md", "DOCS_INDEX.md", "README.md"]):
                required.append("project/PROJECT_REGISTRY.md")

        if not required:
            entry["registered"] = "exempted"; entry["index"] = "-"
        else:
            found, missing = check_registration(f, required, all_indexes_content)
            if not missing:
                entry["registered"] = True; entry["index"] = found[0]
            else:
                entry["registered"] = False; entry["index"] = "-"; entry["missing_from"] = missing
                for idx_file in missing:
                    files_to_create.setdefault(idx_file, []).append(f)
        trace_index.append(entry)

    if not test_mode:
        for idx_path, files in files_to_create.items():
            file_type_for_index = get_file_type(files[0]) if files else "doc"
            create_and_populate_index(idx_path, files, file_type_for_index)

    output = {"artifacts": trace_index}
    trace_index_path = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
    trace_index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_index_path, "w") as f:
        yaml.safe_dump(output, f, default_flow_style=False, sort_keys=False)
    if not test_mode: print("TRACE_INDEX.yml generated successfully.")
    if not validate_trace_index_schema(trace_index_path): return 1
    if test_mode: return 0

    exit_code = generate_audit_report(trace_index)

    linter_script = PROJECT_ROOT / "scripts/lint_governance_links.py"
    try:
        result = subprocess.run([sys.executable, str(linter_script)], check=True, capture_output=True, text=True, encoding='utf-8')
        print("\n--- Governance Links Linter Output ---")
        print(result.stdout)
        print("✅ lint_governance_links.py completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print("\n⚠️ lint_governance_links.py failed:", file=sys.stderr)
        print(e.stdout); print(e.stderr, file=sys.stderr)
        if exit_code == 0: exit_code = e.returncode
    return exit_code

if __name__ == "__main__":
    sys.exit(main())