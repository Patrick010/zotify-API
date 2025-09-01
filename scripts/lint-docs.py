"""
A custom linter to enforce documentation changes alongside code changes.
"""
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / "scripts" / "doc-lint-rules.yml"

def get_changed_files() -> Tuple[Set[str], Set[str]]:
    """
    Gets the set of all changed files and new files from git.
    Returns a tuple of (all_changed_files, new_files).
    """
    is_precommit = "PRE_COMMIT" in os.environ
    command = ["git", "diff", "--name-status"]

    if is_precommit:
        command.append("--cached")
    else:
        # In CI, ensure the main branch is available for comparison.
        subprocess.run(["git", "fetch", "origin", "main"], check=False, capture_output=True)
        command.append("origin/main...HEAD")

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding="utf-8")

        all_changed = set()
        new_files = set()

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            status, file_path = line.split("\t")
            all_changed.add(file_path)
            if status.startswith("A"):
                new_files.add(file_path)

        print(f"Found {len(all_changed)} changed file(s), {len(new_files)} of which are new.")
        return all_changed, new_files

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        return set(), set()

def parse_quality_index(file_path: Path) -> Set[str]:
    """Parses a CODE_QUALITY_INDEX.md file and returns a set of file paths."""
    if not file_path.exists():
        return set()
    content = file_path.read_text(encoding="utf-8")
    # Regex to find file paths in markdown table rows, e.g., | `path/to/file` |
    paths = re.findall(r"\|\s*`([^`]+)`\s*\|", content)
    return set(paths)

def parse_project_registry(file_path: Path) -> Set[str]:
    """Parses the PROJECT_REGISTRY.md file and returns a set of file paths."""
    if not file_path.exists():
        return set()
    content = file_path.read_text(encoding="utf-8")
    # Regex to find markdown links, e.g., [`...`](./path/to/file.md)
    # It specifically looks for links starting with ./ to avoid capturing external links.
    paths = re.findall(r"\[`.*?`\]\(\.\/([^)]+\.md)\)", content)
    # The paths in the registry are relative to the project/ directory, so we need to prepend that.
    return {f"project/{path}" for path in paths}

def check_new_project_docs(new_files: Set[str]) -> List[str]:
    """
    Checks that new markdown files in the 'project/' directory are registered
    in the PROJECT_REGISTRY.md file.
    """
    errors: List[str] = []
    registry_path = PROJECT_ROOT / "project" / "PROJECT_REGISTRY.md"
    registered_docs = parse_project_registry(registry_path)

    new_project_docs = {
        f for f in new_files if f.endswith(".md") and f.startswith("project/")
    }

    for doc_file in new_project_docs:
        if doc_file not in registered_docs:
            errors.append(
                f"New project document '{doc_file}' was added but is not registered in '{registry_path}'."
            )
    return errors

def check_code_doc_link_by_convention(changed_files: Set[str], new_files: Set[str]) -> List[str]:
    """
    Checks that if a source file is changed, its corresponding documentation file is also changed.
    """
    errors: List[str] = []
    # This map defines the root directories for source and their corresponding docs.
    # It assumes a parallel structure.
    CONVENTION_MAP = {
        "api/src/zotify_api/": "api/docs/reference/source/"
    }

    source_files_changed = {f for f in changed_files if f.endswith(".py") and f not in new_files}

    for src_file in source_files_changed:
        for src_prefix, doc_prefix in CONVENTION_MAP.items():
            if src_file.startswith(src_prefix):
                base_name = Path(src_file).stem
                expected_doc_file = f"{doc_prefix}{base_name.upper()}.py.md"
                if not (PROJECT_ROOT / expected_doc_file).exists():
                    errors.append(f"Source file '{src_file}' has no corresponding documentation file at '{expected_doc_file}'.")
                elif expected_doc_file not in changed_files:
                    errors.append(f"Source file '{src_file}' was changed, but its documentation file '{expected_doc_file}' was not.")
                break
    return errors

def check_new_file_rules(new_files: Set[str]) -> List[str]:
    """
    Enforces rules for newly added source code files.
    """
    errors: List[str] = []
    quality_index_path = PROJECT_ROOT / "api/docs/reference/CODE_QUALITY_INDEX.md"
    quality_indexed_files = parse_quality_index(quality_index_path)

    new_source_files = {f for f in new_files if f.endswith(".py")}

    for new_src in new_source_files:
        # Rule 1: Check for corresponding documentation file
        if "api/src/zotify_api" in new_src:
            base_name = Path(new_src).stem
            expected_doc_file = f"api/docs/reference/source/{base_name.upper()}.py.md"
            if expected_doc_file not in new_files:
                errors.append(f"New source file '{new_src}' was added, but its documentation file '{expected_doc_file}' was not created.")

        # Rule 2: Check if the new file is registered in the quality index
        if new_src not in quality_indexed_files:
            errors.append(f"New source file '{new_src}' was added but is not registered in '{quality_index_path.name}'.")
    return errors


def main() -> int:
    """Main function for the linter."""
    print("="*20)
    print("Running Documentation Linter")
    print("="*20)

    changed_files, new_files = get_changed_files()
    if not changed_files and "PRE_COMMIT" not in os.environ:
        print("No changed files detected.")
        return 0

    all_errors: List[str] = []
    all_errors.extend(check_code_doc_link_by_convention(changed_files, new_files))
    all_errors.extend(check_new_file_rules(new_files))
    all_errors.extend(check_new_project_docs(new_files))

    if all_errors:
        print("\n--- Documentation Linter Failed ---", file=sys.stderr)
        for error in sorted(list(set(all_errors))):
            print(f"ERROR: {error}", file=sys.stderr)
        print("-----------------------------------", file=sys.stderr)
        return 1

    print("\nDocumentation Linter Passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
