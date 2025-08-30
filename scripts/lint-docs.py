"""
A custom linter to enforce documentation changes alongside code changes.

This script checks a git diff for modified source files and ensures their
corresponding documentation, as defined in a rules file, has also been modified.
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
PROJECT_REGISTRY_FILE = PROJECT_ROOT / "project" / "PROJECT_REGISTRY.md"
API_REGISTRY_FILE = PROJECT_ROOT / "api" / "docs" / "REGISTRY.md"

# The "Trinity" of mandatory log files that must be updated in most commits.
TRINITY_LOG_FILES = {
    "project/logs/CURRENT_STATE.md",
    "project/logs/ACTIVITY.md",
    "project/logs/SESSION_LOG.md",
}

# Directories to ignore when scanning for unregistered files.
# This should contain directory NAMES, not paths.
IGNORED_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "archive",
    "site",
    "source",
    "storage",
    "templates",
    "venv",
}
# --- End Configuration ---


def get_changed_files() -> Set[str]:
    """
    Gets the set of changed files from git.
    This is a modified version to work in environments where 'git diff'
    against a branch might fail. It uses 'git status' as a more robust
    fallback.
    """
    print("Linter running (checking for all modified files)...")
    command = ["git", "status", "--porcelain=v1"]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        files = set()
        # The output of git status --porcelain is a list of lines.
        # Each line has a status code (e.g., ' M', ' A ', '??') followed by the path.
        # We only care about the path and ignore untracked files.
        for line in result.stdout.strip().split("\n"):
            if line and not line.startswith("??"):
                # The line can be like ' M path/to/file.py' or 'R old -> new'
                # We split and take the last element, which is the file path.
                # In case of rename, it correctly gets the new path.
                files.add(line.strip().split()[-1])

        if not files:
            print("No changed files detected.")
            return set()

        print(f"Found {len(files)} changed file(s):")
        for f in sorted(list(files)):
            print(f"- {f}")
        return files
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        return set()


def load_rules(rules_file: Path) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Loads and validates the rules and quality index map from the YAML file.
    Returns a tuple of (rules, quality_index_map).
    """
    if not rules_file.exists():
        print(f"Warning: Rules file not found at {rules_file}. Skipping rule checks.", file=sys.stderr)
        return [], {}
    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {rules_file}: {e}", file=sys.stderr)
        return [], {}

    if not isinstance(data, dict):
        print(f"Error: Invalid format in {rules_file}. Expected a dictionary.", file=sys.stderr)
        return [], {}

    rules = data.get("rules", [])
    quality_map = data.get("quality_index_map", {})

    if not isinstance(rules, list):
        print(f"Error: Invalid format for 'rules' in {rules_file}. Expected a list.", file=sys.stderr)
        rules = []
    if not isinstance(quality_map, dict):
        print(f"Error: Invalid format for 'quality_index_map' in {rules_file}. Expected a dictionary.", file=sys.stderr)
        quality_map = {}

    return rules, quality_map


def check_documentation_rules(rules: List[Dict[str, Any]], changed_files: Set[str]) -> List[str]:
    """
    Checks for violations of documentation rules.
    - `required_docs`: Ensures docs are updated when source files change.
    - `forbidden_docs`: Ensures specified docs are NOT changed.
    Returns a list of error messages for any violations.
    """
    errors: List[str] = []
    for rule in rules:
        name = rule.get("name", "Unnamed")
        source_paths = rule.get("source_paths", [])
        required_docs = rule.get("required_docs", [])
        forbidden_docs = rule.get("forbidden_docs", [])
        message = rule.get("message", f"Rule '{name}' failed.")

        # Check if any changed file matches a source path for this rule
        source_change_found = any(
            any(changed_file.startswith(src_path) for src_path in source_paths)
            for changed_file in changed_files
        )

        if not source_change_found:
            continue

        # --- Check for required document changes ---
        if required_docs:
            doc_change_found = any(
                any(changed_file == doc_path for doc_path in required_docs)
                for changed_file in changed_files
            )
            if not doc_change_found:
                errors.append(f"{message} - A file in {source_paths} was changed, but no required doc in {required_docs} was updated.")

        # --- Check for forbidden document changes ---
        if forbidden_docs:
            for forbidden_doc in forbidden_docs:
                if forbidden_doc in changed_files:
                    errors.append(f"Rule '{name}' violation: The document '{forbidden_doc}' should not be modified as part of this change.")

    return errors


def check_quality_index(
    quality_map: Dict[str, str], changed_files: Set[str]
) -> List[str]:
    """
    Checks that if a source file is changed, its corresponding Code Quality
    Index has also been updated.
    """
    errors: List[str] = []

    # Identify all python source files that were changed
    source_files_changed = {
        f for f in changed_files if f.endswith(".py") and "/src/" in f
    }

    # If no relevant source files were changed, there's nothing to do
    if not source_files_changed:
        return []

    for src_file in source_files_changed:
        for src_prefix, quality_doc in quality_map.items():
            if src_file.startswith(src_prefix):
                if quality_doc not in changed_files:
                    msg = (
                        f"Source file '{src_file}' was changed, but its corresponding "
                        f"Code Quality Index '{quality_doc}' was not updated."
                    )
                    errors.append(msg)
                # Once we find the rule for this source file, we can stop checking.
                break
    return errors


def check_trinity_logs(changed_files: Set[str]) -> List[str]:
    """
    Checks that the three mandatory log files have been updated.
    This check is skipped if the ONLY files being committed are the logs themselves.
    """
    # If there are changed files, but those files are NOT a subset of the log files
    # (meaning, something OTHER than just the logs was changed), then we must
    # enforce that the logs were also changed.
    if changed_files and not changed_files.issubset(TRINITY_LOG_FILES):
        missing_logs = TRINITY_LOG_FILES - changed_files
        if missing_logs:
            return [f"Mandatory log file was not updated: {log}" for log in sorted(list(missing_logs))]
    return []


def get_registered_files(registry_file: Path) -> Set[str]:
    """
    Parses the project registry to find all registered file paths by looking
    for markdown links.
    """
    if not registry_file.exists():
        print(f"Warning: Registry file not found at {registry_file}", file=sys.stderr)
        return set()
    content = registry_file.read_text(encoding="utf-8")

    # Regex to find all markdown links, e.g., [text](path)
    links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", content)

    normalized_paths = set()
    for link in links:
        # Ignore external URLs
        if link.startswith("http"):
            continue

        try:
            # All links in markdown are relative to the file they are in.
            # So we resolve from the registry file's parent directory.
            abs_path = (registry_file.parent / link).resolve()
            relative_path = abs_path.relative_to(PROJECT_ROOT.resolve())
            normalized_paths.add(str(relative_path).replace("\\", "/"))
        except (ValueError, FileNotFoundError):
            # ValueError: path is outside project root
            # FileNotFoundError: link is broken
            # In either case, we can't check it, so we warn and ignore.
            print(
                f"Warning: Could not resolve or find path '{link}' in registry.",
                file=sys.stderr,
            )
            pass

    return normalized_paths


def get_all_relevant_files() -> Set[str]:
    """Scans the filesystem for all .md and script files."""
    all_files: Set[str] = set()
    for root, dirs, files in os.walk(PROJECT_ROOT, topdown=True):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        # Convert root to a Path object for easier manipulation
        root_path = Path(root)

        for file in files:
            file_path = root_path / file
            relative_path_str = str(file_path.relative_to(PROJECT_ROOT)).replace("\\", "/")

            # Check if the file is a markdown file or a script in the scripts/ dir
            if file.endswith(".md") or str(file_path.parent).endswith("scripts"):
                # Exclude this script itself from the check
                if "lint-docs.py" in relative_path_str:
                    continue
                all_files.add(relative_path_str)

    return all_files


def check_registry_completeness() -> List[str]:
    """
    Ensures that all .md and script files on disk are registered in one of the
    two project registries.
    """
    errors: List[str] = []

    # Get registered files from both registries and combine them
    project_registered = get_registered_files(PROJECT_REGISTRY_FILE)
    api_registered = get_registered_files(API_REGISTRY_FILE)
    registered_files = project_registered.union(api_registered)

    # Add the registry files themselves to the set to avoid self-reporting
    registered_files.add("project/PROJECT_REGISTRY.md")
    registered_files.add("api/docs/REGISTRY.md")

    all_files = get_all_relevant_files()

    unregistered_files = all_files - registered_files
    if unregistered_files:
        for file in sorted(list(unregistered_files)):
            errors.append(
                f"File '{file}' exists but is not listed in either project registry."
            )

    return errors


def main() -> int:
    """Main function for the linter."""
    print("="*20)
    print("Running Documentation Linter")
    print("="*20)

    all_errors: List[str] = []

    # --- Global Checks (Always Run) ---
    # The registry check is critical and should run regardless of what has changed.
    all_errors.extend(check_registry_completeness())

    # --- Change-Specific Checks ---
    changed_files = get_changed_files()
    if not changed_files and "PRE_COMMIT" in os.environ:
        print("No changed files detected in pre-commit mode. Skipping change-specific checks.")
    else:
        rules, quality_map = load_rules(RULES_FILE)
        all_errors.extend(check_trinity_logs(changed_files))
        all_errors.extend(check_documentation_rules(rules, changed_files))
        all_errors.extend(check_quality_index(quality_map, changed_files))


    # Report results
    if all_errors:
        print("\n--- Documentation Linter Failed ---", file=sys.stderr)
        for error in sorted(list(set(all_errors))): # Use set to remove duplicate messages
            print(f"ERROR: {error}", file=sys.stderr)
        print("-----------------------------------", file=sys.stderr)
        return 1

    print("\nDocumentation Linter Passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
