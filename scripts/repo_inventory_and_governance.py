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
IGNORED_DIRS = {".git", ".idea", "venv", "node_modules", "build", "dist", "target", "__pycache__"}
IGNORED_FILES = {"mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md"}

INDEX_MAP = [
    {
        "match": lambda path, ftype: ftype == "doc" and path.startswith("api/docs/"),
        "indexes": [
            "api/docs/MASTER_INDEX.md",
            "api/docs/DOCS_QUALITY_INDEX.md",
        ],
    },
    {
        "match": lambda path, ftype: ftype == "code" and path.startswith("api/"),
        "indexes": ["api/docs/CODE_FILE_INDEX.md"],
    },
    {
        "match": lambda path, ftype: ftype == "code" and path.startswith("Gonk/"),
        "indexes": ["Gonk/CODE_FILE_INDEX.md"],
    },
    {
        "match": lambda path, ftype: ftype == "code" and path.startswith("snitch/"),
        "indexes": ["snitch/CODE_FILE_INDEX.md"],
    },
    {
        "match": lambda path, ftype: ftype == "code" and path.startswith("scripts/"),
        "indexes": ["scripts/CODE_FILE_INDEX.md"],
    },
]

def get_file_type(filepath: str) -> str:
    """Classifies a file based on its extension using FILETYPE_MAP."""
    if os.path.basename(filepath).startswith("."):
        return "exempt"
    if os.path.basename(filepath) in IGNORED_FILES:
        return "exempt"

    ext = os.path.splitext(filepath)[1]
    return FILETYPE_MAP.get(ext, "exempt")

def find_all_files() -> List[str]:
    """Scans the project root for all files, respecting IGNORED_DIRS."""
    all_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            all_files.append(
                str(Path(os.path.join(root, file)).relative_to(PROJECT_ROOT))
            )
    return all_files

def parse_markdown_index(index_path: Path) -> Set[str]:
    """Parses a markdown file and extracts all linked paths or table rows."""
    if not index_path.exists():
        return set()
    content = index_path.read_text(encoding="utf-8")

    if "| Path " in content or "| File Path " in content:
        paths = re.findall(r"\|\s*`([^`]+)`\s*\|", content)
        return set(paths)
    else:
        links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)
        return {str(Path(index_path.parent / link).resolve().relative_to(PROJECT_ROOT)) for link in links}

def check_registration(file_path: str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:
    """
    Checks if a file is registered in the required indexes.
    Returns two lists: one of found indexes and one of missing indexes.
    """
    found_in = []
    missing_from = []
    normalized_file_path = str(Path(file_path).resolve().relative_to(PROJECT_ROOT))
    for index_file in required_indexes:
        if normalized_file_path in all_indexes_content.get(index_file, set()):
            found_in.append(index_file)
        else:
            missing_from.append(index_file)
    return sorted(found_in), sorted(missing_from)

def create_and_populate_index(index_path_str: str, files_to_add: List[str], file_type: str):
    """Creates a new index file and populates it with the given files."""
    index_path = PROJECT_ROOT / index_path_str
    print(f"Creating missing index file: {index_path}")
    index_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"# {index_path.stem.replace('_', ' ').title()}\n\nThis file is auto-generated. Do not edit manually.\n\n"
    lines = []

    if "CODE_FILE_INDEX" in index_path_str:
        header += "| Path | Type | Description | Status | Linked Docs | Notes |\n"
        header += "|------|------|-------------|--------|-------------|-------|\n"
        lines = [f"| `{f}` | | | Active | | |" for f in sorted(files_to_add)]
    elif "QUALITY_INDEX" in index_path_str:
        header += "| File Path | Documentation Score | Code Score | Reviewer | Review Date | Notes |\n"
        header += "|-----------|---------------------|------------|----------|-------------|-------|\n"
        lines = [f"| `{f}` | X | X | | | |" for f in sorted(files_to_add)]
    else:
        lines = [f"*   [{Path(f).name}]({f})" for f in sorted(files_to_add)]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(lines) + "\n")

def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    """Generates a human-readable audit report and returns an exit code."""
    print("\n" + "=" * 50)
    print("Governance Audit Report")
    print("=" * 50)

    missing_by_index = {}
    registered_count = 0
    missing_count = 0
    exempted_count = 0

    for item in trace_index:
        if item["registered"] == "exempted":
            exempted_count += 1
        elif item["registered"] is True:
            registered_count += 1
        else:
            missing_count += 1
            for index_file in item.get("missing_from", []):
                if index_file not in missing_by_index:
                    missing_by_index[index_file] = []
                missing_by_index[index_file].append(item["path"])

    if missing_count > 0:
        print("\n--- Missing Registrations ---")
        for index_file, files in sorted(missing_by_index.items()):
            print(f"\nMissing from {index_file}:")
            for file_path in sorted(files):
                print(f"  - {file_path}")

    print("\n" + "-" * 20)
    print("Summary:")
    print(f"- Total files checked: {len(trace_index)}")
    print(f"- Registered: {registered_count}")
    print(f"- Missing: {missing_count}")
    print(f"- Exempted: {exempted_count}")
    print("-" * 20)

    if missing_count > 0:
        print("\nStatus: ❌ FAIL")
        return 1
    else:
        print("\nStatus: ✅ PASS")
        return 0

def main():
    """Main function to run the governance check."""
    all_files = find_all_files()
    trace_index = []

    all_index_paths = {idx for rule in INDEX_MAP for idx in rule["indexes"]}
    all_indexes_content = {
        str(p): parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths
    }

    files_to_create_in_indexes = {}

    for file_path in sorted(all_files):
        file_type = get_file_type(file_path)

        trace_entry = {
            "path": file_path,
            "type": file_type,
        }

        required_indexes = []
        if file_type != "exempt":
            for rule in INDEX_MAP:
                if rule["match"](file_path, file_type):
                    required_indexes.extend(rule["indexes"])

        required_indexes = sorted(list(set(required_indexes)))

        if not required_indexes:
            trace_entry["registered"] = "exempted"
            trace_entry["index"] = None
        else:
            found_in, missing_from = check_registration(file_path, required_indexes, all_indexes_content)

            if not missing_from:
                trace_entry["registered"] = True
                trace_entry["index"] = found_in
            else:
                trace_entry["registered"] = False
                trace_entry["index"] = None
                trace_entry["missing_from"] = missing_from

                for index_file in missing_from:
                    if index_file not in files_to_create_in_indexes:
                        files_to_create_in_indexes[index_file] = []
                    files_to_create_in_indexes[index_file].append(file_path)

        trace_index.append(trace_entry)

    for index_path_str, files in files_to_create_in_indexes.items():
        if not (PROJECT_ROOT / index_path_str).exists():
            first_file_type = get_file_type(files[0])
            create_and_populate_index(index_path_str, files, first_file_type)

    # Custom representer for None -> '-'
    def represent_none(self, _):
        return self.represent_scalar('tag:yaml.org,2002:null', '-')
    yaml.add_representer(type(None), represent_none)

    output = {"artifacts": trace_index}
    with open(PROJECT_ROOT / "TRACE_INDEX.yml", "w") as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False)
    print("TRACE_INDEX.yml generated successfully.")

    return generate_audit_report(trace_index)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)