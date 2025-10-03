import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
FILETYPE_MAP = {
    ".md": "doc",
    ".py": "code",
    ".sh": "code",
    ".html": "code",
    ".js": "code",
    ".ts": "code",
    ".css": "code",
    ".yml": "code",
    ".go": "code",
}
IGNORED_DIRS = {".git", ".idea", ".venv", "node_modules", "build", "dist", "target", "__pycache__", "site", "archive", "templates", ".pytest_cache"}
IGNORED_FILES = {"mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md", "LICENSE"}

INDEX_MAP = [
    {"match": lambda path, ftype: ftype == "doc" and path.startswith("api/docs/"),
     "indexes": ["api/docs/MASTER_INDEX.md", "api/docs/DOCS_QUALITY_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "doc" and (
            path.startswith("project/archive/docs/") or
            path.startswith("project/logs/") or
            path.startswith("project/process/") or
            path.startswith("project/proposals/") or
            path.startswith("project/reports/") or
            (path.startswith("project/") and Path(path).parent.name == "project")),
     "indexes": ["project/PROJECT_REGISTRY.md"]},
    {"match": lambda path, ftype: ftype == "doc" and path.startswith("Gonk/GonkCLI/docs/"),
     "indexes": ["Gonk/GonkCLI/DOCS_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "doc" and path.startswith("Gonk/GonkUI/docs/"),
     "indexes": ["Gonk/GonkUI/DOCS_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "doc" and path.startswith("snitch/docs/"),
     "indexes": ["snitch/DOCS_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "code" and path.startswith("api/"),
     "indexes": ["api/docs/CODE_FILE_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "code" and path.startswith("Gonk/"),
     "indexes": ["Gonk/CODE_FILE_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "code" and path.startswith("snitch/"),
     "indexes": ["snitch/CODE_FILE_INDEX.md"]},
    {"match": lambda path, ftype: ftype == "code" and path.startswith("scripts/"),
     "indexes": ["scripts/CODE_FILE_INDEX.md"]},
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
    if not index_path.exists():
        return set()
    content = index_path.read_text(encoding="utf-8")

    # More specific regex for table-based indexes to only capture the first column.
    if "CODE_FILE_INDEX.md" in str(index_path) or "DOCS_QUALITY_INDEX.md" in str(index_path):
        return set(re.findall(r"^\s*\|\s*`([^`]+)`", content, re.MULTILINE))

    # Logic for link-based registries like PROJECT_REGISTRY.md
    if "PROJECT_REGISTRY.md" in str(index_path):
        links = re.findall(r"\[`([^`]+)`\]\(([^)]+)\)", content)
        # We need to reconstruct the full path from the relative link
        return {str(Path(os.path.normpath(os.path.join(index_path.parent, link[1]))).relative_to(PROJECT_ROOT)) for link in links}

    # Fallback for other markdown link styles (like MASTER_INDEX.md)
    links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)
    return {str(Path(os.path.normpath(os.path.join(index_path.parent, link))).relative_to(PROJECT_ROOT)) for link in links}


def check_registration(file_path: str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:
    found, missing = [], []
    normalized_path = file_path # Path is already normalized by find_all_files
    for idx in required_indexes:
        if normalized_path in all_indexes_content.get(idx, set()):
            found.append(idx)
        else:
            missing.append(idx)
    return sorted(found), sorted(missing)


def create_and_populate_index(index_path_str: str, files_to_add: List[str], file_type: str):
    index_path = PROJECT_ROOT / index_path_str
    index_path.parent.mkdir(parents=True, exist_ok=True)

    existing_files = set()
    if index_path.exists():
        existing_files = parse_markdown_index(index_path)

    new_files_to_add = sorted([f for f in files_to_add if f not in existing_files])

    if not new_files_to_add:
        return

    lines_to_append = []
    # Handle PROJECT_REGISTRY.md separately because of its table structure
    if "PROJECT_REGISTRY.md" in index_path_str and index_path.exists():
        content = index_path.read_text(encoding="utf-8").splitlines()

        try:
            separator_index = -1
            # Find the specific table separator to be more precise
            for i, line in enumerate(content):
                if line.strip() == '|---|---|---|' and i > 0 and "Document" in content[i-1] and "Location" in content[i-1]:
                    separator_index = i
                    break

            if separator_index == -1:
                 raise ValueError("Main table separator not found in PROJECT_REGISTRY.md")

            insertion_point = separator_index + 1
        except (ValueError, IndexError):
            # Fallback if table not found, append at end (less ideal but safe)
            insertion_point = len(content)

        for f in new_files_to_add:
            relative_link = os.path.relpath(PROJECT_ROOT / f, index_path.parent)
            doc_name_human = Path(f).stem.replace('_', ' ').replace('-', ' ').title()
            lines_to_append.append(f"| **{doc_name_human}** | [`{Path(f).name}`]({relative_link}) | |")

        for line in reversed(sorted(lines_to_append)):
            content.insert(insertion_point, line)

        index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
        return

    # --- Logic for other, simpler index files ---
    if "CODE_FILE_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | | | Active | | |" for f in new_files_to_add]
    elif "DOCS_QUALITY_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | X | X | | | |" for f in new_files_to_add]
    else: # For list-based indexes like MASTER_INDEX.md
        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent) for f in new_files_to_add]
        lines_to_append = [f"*   [{Path(f).name}]({link})" for f, link in zip(new_files_to_add, relative_links)]

    # Append to existing file or create a new one
    if index_path.exists():
        with open(index_path, "a", encoding="utf-8") as f:
            content = index_path.read_text(encoding="utf-8")
            if content and content[-1] != '\n':
                f.write('\n')
            f.write("\n".join(sorted(lines_to_append)) + "\n")
    else:
        header = f"# {index_path.stem.replace('_',' ').title()}\n\nThis file is auto-generated. Do not edit manually.\n\n"
        if "CODE_FILE_INDEX" in index_path_str:
            header += "| Path | Type | Description | Status | Linked Docs | Notes |\n|------|------|-------------|--------|-------------|-------|\n"
        elif "QUALITY_INDEX" in index_path_str:
            header += "| File Path | Documentation Score | Code Score | Reviewer | Review Date | Notes |\n|-----------|---------------------|------------|----------|-------------|-------|\n"

        index_path.write_text(header + "\n".join(sorted(lines_to_append)) + "\n", encoding="utf-8")


def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    print("\n" + "="*50 + "\nGovernance Audit Report\n" + "="*50)
    missing_by_index, registered_count, missing_count, exempted_count = {},0,0,0
    for item in trace_index:
        if item["registered"]=="exempted":
            exempted_count += 1
        elif item["registered"] is True:
            registered_count += 1
        else:
            missing_count += 1
            for idx in item.get("missing_from", []):
                missing_by_index.setdefault(idx,[]).append(item["path"])
    if missing_count>0:
        print("\n--- Missing Registrations ---")
        for idx, files in sorted(missing_by_index.items()):
            print(f"\nMissing from {idx}:")
            for f in sorted(files):
                print(f"  - {f}")
    print("\n" + "-"*20)
    print(f"- Total files checked: {len(trace_index)}\n- Registered: {registered_count}\n- Missing: {missing_count}\n- Exempted: {exempted_count}\n" + "-"*20)
    return 1 if missing_count>0 else 0


def validate_trace_index_schema(trace_index_path: Path) -> bool:
    print("\n--- Validating TRACE_INDEX.yml Schema ---")
    try:
        with open(trace_index_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Could not load TRACE_INDEX.yml: {e}", file=sys.stderr)
        return False
    errors=[]
    if 'artifacts' not in data or not isinstance(data['artifacts'], list):
        errors.append("FATAL: 'artifacts' key missing or not a list.")
        print("\n".join(errors), file=sys.stderr)
        return False
    for a in data['artifacts']:
        path=a.get('path')
        reg=a.get('registered')
        idx=a.get('index')
        miss=a.get('missing_from')
        if reg is True and not isinstance(idx, str):
            errors.append(f"Schema Error (path:{path}): If registered is true, 'index' must be a string.")
        if reg is False:
            if idx!="-":
                errors.append(f"Schema Error (path:{path}): If registered is false, 'index' must be '-'.")
            if not isinstance(miss, list):
                errors.append(f"Schema Error (path:{path}): If registered is false, 'missing_from' must be a list of strings.")
        if reg=="exempted" and idx!="-":
            errors.append(f"Schema Error (path:{path}): If registered is 'exempted', 'index' must be '-'.")
    if errors:
        print("TRACE_INDEX.yml schema validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return False
    print("Schema validation passed!")
    return True


def main():
    # Determine if running in test mode (for linter)
    test_mode = "--test-files" in sys.argv
    full_mode = "--full" in sys.argv

    if full_mode:
        all_files = find_all_files()
    elif test_mode:
        # In test mode, we get the file list from the command line
        try:
            file_list_index = sys.argv.index("--test-files") + 1
            all_files = sys.argv[file_list_index:]
        except (ValueError, IndexError):
            all_files = []
    else:
        # Default mode: read from manifest
        manifest_path = PROJECT_ROOT / "project" / "reports" / "REPO_MANIFEST.md"
        if manifest_path.exists():
            content = manifest_path.read_text(encoding="utf-8")
            all_files = re.findall(r"^\s*\|\s*`([^`]+)`\s*\|.*", content, re.MULTILINE)
        else:
            print("INFO: REPO_MANIFEST.md not found. Running a full scan.", file=sys.stderr)
            all_files = find_all_files()

    trace_index = []
    all_index_paths = {idx for rule in INDEX_MAP for idx in rule["indexes"]}
    all_indexes_content = {str(p): parse_markdown_.md" in str(index_path):
        return set(re.findall(r"^\s*\|\s*`([^`]+)`", content, re.MULTILINE))

    # Logic for link-based registries like PROJECT_REGISTRY.md
    if "PROJECT_REGISTRY.md" in str(index_path):
        links = re.findall(r"\[`([^`]+)`\]\(([^)]+)\)", content)
        # We need to reconstruct the full path from the relative link
        return {str(Path(os.path.normpath(os.path.join(index_path.parent, link[1]))).relative_to(PROJECT_ROOT)) for link in links}

    # Fallback for other markdown link styles (like MASTER_INDEX.md)
    links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)
    return {str(Path(os.path.normpath(os.path.join(index_path.parent, link))).relative_to(PROJECT_ROOT)) for link in links}


def check_registration(file_path: str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:
    found, missing = [], []
    normalized_path = file_path # Path is already normalized by find_all_files
    for idx in required_indexes:
        if normalized_path in all_indexes_content.get(idx, set()):
            found.append(idx)
        else:
            missing.append(idx)
    return sorted(found), sorted(missing)


def create_and_populate_index(index_path_str: str, files_to_add: List[str], file_type: str):
    index_path = PROJECT_ROOT / index_path_str
    index_path.parent.mkdir(parents=True, exist_ok=True)

    existing_files = set()
    if index_path.exists():
        existing_files = parse_markdown_index(index_path)

    new_files_to_add = sorted([f for f in files_to_add if f not in existing_files])

    if not new_files_to_add:
        return

    lines_to_append = []
    # Handle PROJECT_REGISTRY.md separately because of its table structure
    if "PROJECT_REGISTRY.md" in index_path_str and index_path.exists():
        content = index_path.read_text(encoding="utf-8").splitlines()

        try:
            separator_index = -1
            # Find the specific table separator to be more precise
            for i, line in enumerate(content):
                if line.strip() == '|---|---|---|' and i > 0 and "Document" in content[i-1] and "Location" in content[i-1]:
                    separator_index = i
                    break

            if separator_index == -1:
                 raise ValueError("Main table separator not found in PROJECT_REGISTRY.md")

            insertion_point = separator_index + 1
        except (ValueError, IndexError):
            # Fallback if table not found, append at end (less ideal but safe)
            insertion_point = len(content)

        for f in new_files_to_add:
            relative_link = os.path.relpath(PROJECT_ROOT / f, index_path.parent)
            doc_name_human = Path(f).stem.replace('_', ' ').replace('-', ' ').title()
            lines_to_append.append(f"| **{doc_name_human}** | [`{Path(f).name}`]({relative_link}) | |")

        for line in reversed(sorted(lines_to_append)):
            content.insert(insertion_point, line)

        index_path.write_text("\n".join(content) + "\n", encoding="utf-8")
        return

    # --- Logic for other, simpler index files ---
    if "CODE_FILE_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | | | Active | | |" for f in new_files_to_add]
    elif "DOCS_QUALITY_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | X | X | | | |" for f in new_files_to_add]
    else: # For list-based indexes like MASTER_INDEX.md
        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent) for f in new_files_to_add]
        lines_to_append = [f"*   [{Path(f).name}]({link})" for f, link in zip(new_files_to_add, relative_links)]

    # Append to existing file or create a new one
    if index_path.exists():
        with open(index_path, "a", encoding="utf-8") as f:
            content = index_path.read_text(encoding="utf-8")
            if content and content[-1] != '\n':
                f.write('\n')
            f.write("\n".join(sorted(lines_to_append)) + "\n")
    else:
        header = f"# {index_path.stem.replace('_',' ').title()}\n\nThis file is auto-generated. Do not edit manually.\n\n"
        if "CODE_FILE_INDEX" in index_path_str:
            header += "| Path | Type | Description | Status | Linked Docs | Notes |\n|------|------|-------------|--------|-------------|-------|\n"
        elif "QUALITY_INDEX" in index_path_str:
            header += "| File Path | Documentation Score | Code Score | Reviewer | Review Date | Notes |\n|-----------|---------------------|------------|----------|-------------|-------|\n"

        index_path.write_text(header + "\n".join(sorted(lines_to_append)) + "\n", encoding="utf-8")


def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    print("\n" + "="*50 + "\nGovernance Audit Report\n" + "="*50)
    missing_by_index, registered_count, missing_count, exempted_count = {},0,0,0
    for item in trace_index:
        if item["registered"]=="exempted":
            exempted_count += 1
        elif item["registered"] is True:
            registered_count += 1
        else:
            missing_count += 1
            for idx in item.get("missing_from", []):
                missing_by_index.setdefault(idx,[]).append(item["path"])
    if missing_count>0:
        print("\n--- Missing Registrations ---")
        for idx, files in sorted(missing_by_index.items()):
            print(f"\nMissing from {idx}:")
            for f in sorted(files):
                print(f"  - {f}")
    print("\n" + "-"*20)
    print(f"- Total files checked: {len(trace_index)}\n- Registered: {registered_count}\n- Missing: {missing_count}\n- Exempted: {exempted_count}\n" + "-"*20)
    return 1 if missing_count>0 else 0


def validate_trace_index_schema(trace_index_path: Path) -> bool:
    print("\n--- Validating TRACE_INDEX.yml Schema ---")
    try:
        with open(trace_index_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Could not load TRACE_INDEX.yml: {e}", file=sys.stderr)
        return False
    errors=[]
    if 'artifacts' not in data or not isinstance(data['artifacts'], list):
        errors.append("FATAL: 'artifacts' key missing or not a list.")
        print("\n".join(errors), file=sys.stderr)
        return False
    for a in data['artifacts']:
        path=a.get('path')
        reg=a.get('registered')
        idx=a.get('index')
        miss=a.get('missing_from')
        if reg is True and not isinstance(idx, str):
            errors.append(f"Schema Error (path:{path}): If registered is true, 'index' must be a string.")
        if reg is False:
            if idx!="-":
                errors.append(f"Schema Error (path:{path}): If registered is false, 'index' must be '-'.")
            if not isinstance(miss, list):
                errors.append(f"Schema Error (path:{path}): If registered is false, 'missing_from' must be a list of strings.")
        if reg=="exempted" and idx!="-":
            errors.append(f"Schema Error (path:{path}): If registered is 'exempted', 'index' must be '-'.")
    if errors:
        print("TRACE_INDEX.yml schema validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return False
    print("Schema validation passed!")
    return True


def main():
    # Determine if running in test mode (for linter)
    test_mode = "--test-files" in sys.argv
    full_mode = "--full" in sys.argv

    if full_mode:
        all_files = find_all_files()
    elif test_mode:
        # In test mode, we get the file list from the command line
        try:
            file_list_index = sys.argv.index("--test-files") + 1
            all_files = sys.argv[file_list_index:]
        except (ValueError, IndexError):
            all_files = []
    else:
        # Default mode: read from manifest
        manifest_path = PROJECT_ROOT / "project" / "reports" / "REPO_MANIFEST.md"
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

        if ftype != "exempt":
            # This logic is to ignore module-level index files from the main project registry
            if Path(f).name in ["CODE_FILE_INDEX.md", "DOCS_INDEX.md", "README.md", ".pytest_cache"]:
                 pass
            else:
                for r in INDEX_MAP:
                    if r["match"](f, ftype):
                        required.extend(r["indexes"])

        required = sorted(list(set(required)))

        # Assign default project registry if doc is unassigned
        if ftype == 'doc' and not required and f not in IGNORED_FILES and not f.startswith("templates/"):
             is_module_index = Path(f).name in ["CODE_FILE_INDEX.md", "DOCS_INDEX.md"]
             is_readme = Path(f).name == "README.md"
             if not (is_module_index or is_readme):
                required.append("project/PROJECT_REGISTRY.md")

        if not required:
            entry["registered"] = "exempted"
            entry["index"] = "-"
        else:
            found, missing = check_registration(f, required, all_indexes_content)
            if not missing:
                entry["registered"] = True
                # If a file is in multiple indexes, just record the first one found.
                entry["index"] = found[0]
            else:
                entry["registered"] = False
                entry["index"] = "-"
                entry["missing_from"] = missing
                for idx_file in missing:
                    files_to_create.setdefault(idx_file, []).append(f)
        trace_index.append(entry)

    if not test_mode:
        for idx_path, files in files_to_create.items():
            # Determine file type from the first file in the list
            file_type_for_index = get_file_type(files[0]) if files else "doc"
            create_and_populate_index(idx_path, files, file_type_for_index)

    output = {"artifacts": trace_index}
    trace_index_path = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
    trace_index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_index_path, "w") as f:
        yaml.safe_dump(output, f, default_flow_style=False, sort_keys=False)

    if not test_mode:
        print("TRACE_INDEX.yml generated successfully.")

    if not validate_trace_index_schema(trace_index_path):
        return 1

    if test_mode:
        return 0

    return generate_audit_report(trace_index)

if __name__ == "__main__":
    sys.exit(main())