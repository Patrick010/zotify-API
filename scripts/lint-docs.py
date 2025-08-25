"""
A custom linter to enforce documentation changes alongside code changes.

This script checks a git diff for modified source files and ensures their
corresponding documentation, as inferred by module path, has also been modified.
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set

PROJECT_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = PROJECT_ROOT / "project" / "PROJECT_REGISTRY.md"

# Define path prefixes for different categories
SOURCE_CODE_PREFIXES = ["api/src", "snitch/", "gonk-testUI/"]
TEST_CODE_PREFIXES = ["api/tests"]
DOC_PREFIXES = ["api/docs", "snitch/docs", "gonk-testUI/docs", "project/"]


def get_changed_files() -> Set[str]:
    """
    Gets the set of changed files compared to the main branch.
    This is intended for use in a CI environment.
    """
    try:
        # In CI, we need to compare against the target branch, which is typically 'main'
        # First, ensure we have the target branch available
        subprocess.run(["git", "fetch", "origin", "main"], check=True, capture_output=True)
        # Then, get the list of changed files
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return set(line for line in result.stdout.strip().split("\n") if line)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        # If git diff fails, we cannot proceed.
        return set()


def get_module_from_path(path: str) -> str:
    """
    Determines the module ('api', 'snitch', 'gonk-testUI', 'project') from a file path.
    """
    if path.startswith("api/"):
        return "api"
    if path.startswith("snitch/"):
        return "snitch"
    if path.startswith("gonk-testUI/"):
        return "gonk-testUI"
    if path.startswith("project/"):
        return "project"
    return "other"


def categorize_files(files: Set[str]) -> Dict[str, Dict[str, bool]]:
    """
    Categorizes files into modules and checks for code vs. doc changes.
    """
    module_changes: Dict[str, Dict[str, bool]] = {
        "api": {"code_changed": False, "docs_changed": False},
        "snitch": {"code_changed": False, "docs_changed": False},
        "gonk-testUI": {"code_changed": False, "docs_changed": False},
    }
    project_docs_changed = False

    for file_path in files:
        module = get_module_from_path(file_path)

        is_code = any(
            file_path.startswith(prefix)
            for prefix in SOURCE_CODE_PREFIXES + TEST_CODE_PREFIXES
        )
        is_docs = any(file_path.startswith(prefix) for prefix in DOC_PREFIXES)

        if is_code and module in module_changes:
            module_changes[module]["code_changed"] = True

        if is_docs:
            if module in module_changes:
                module_changes[module]["docs_changed"] = True
            elif module == "project":
                project_docs_changed = True

    # If project-level docs were changed, it satisfies the linter for all modules
    if project_docs_changed:
        for module in module_changes:
            module_changes[module]["docs_changed"] = True

    return module_changes


def main() -> int:
    """
    Main function for the linter.
    """
    print("Running Documentation Linter...")
    changed_files = get_changed_files()

    if not changed_files:
        print("No changed files detected. Exiting.")
        return 0

    print(f"Found {len(changed_files)} changed file(s):")
    for f in sorted(list(changed_files)):
        print(f"- {f}")

    module_changes = categorize_files(changed_files)
    errors: List[str] = []

    for module, changes in module_changes.items():
        if changes["code_changed"] and not changes["docs_changed"]:
            errors.append(
                f"Module '{module}' has source code changes but no corresponding "
                f"documentation changes. Please update documentation in '{module}/docs/' "
                f"or in the main 'project/' directory."
            )

    if errors:
        print("\n--- Documentation Linter Failed ---", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("-----------------------------------", file=sys.stderr)
        return 1

    print("\nDocumentation Linter Passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
