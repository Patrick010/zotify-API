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
from typing import Any, Dict, List, Set

import yaml

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / "scripts" / "doc-lint-rules.yml"
REGISTRY_FILE = PROJECT_ROOT / "project" / "PROJECT_REGISTRY.md"

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

    In a pre-commit hook, it checks staged files.
    In a CI environment, it checks files changed against the main branch.
    """
    is_precommit = "PRE_COMMIT" in os.environ

    if is_precommit:
        print("Linter running in pre-commit mode (checking staged files)...")
        command = ["git", "diff", "--name-only", "--cached"]
    else:
        print("Linter running in CI mode (checking against main branch)...")
        # In CI, ensure the main branch is available for comparison.
        subprocess.run(["git", "fetch", "origin", "main"], check=False, capture_output=True)
        command = ["git", "diff", "--name-only", "origin/main...HEAD"]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        files = set(line for line in result.stdout.strip().split("\n") if line)
        print(f"Found {len(files)} changed file(s):")
        for f in sorted(list(files)):
            print(f"- {f}")
        return files
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        # In pre-commit, a failure to get files is a critical error.
        if is_precommit:
             print("This can happen if you haven't staged any files for commit yet.", file=sys.stderr)
        return set()


def load_rules(rules_file: Path) -> List[Dict[str, Any]]:
    """Loads and validates the rules from the YAML configuration file."""
    if not rules_file.exists():
        print(f"Warning: Rules file not found at {rules_file}. Skipping rule checks.", file=sys.stderr)
        return []
    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in {rules_file}: {e}", file=sys.stderr)
        return []


    if not isinstance(data, dict) or "rules" not in data or not isinstance(data["rules"], list):
        print(f"Error: Invalid format in {rules_file}. Expected a 'rules' key with a list of rule objects.", file=sys.stderr)
        return []

    return data["rules"]


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
    Ensures that all .md and script files on disk are registered in the
    PROJECT_REGISTRY.md file.
    """
    errors: List[str] = []
    registered_files = get_registered_files(REGISTRY_FILE)

    # Add the registry file itself to the set of registered files to avoid self-reporting
    registered_files.add("project/PROJECT_REGISTRY.md")

    all_files = get_all_relevant_files()

    unregistered_files = all_files - registered_files
    if unregistered_files:
        for file in sorted(list(unregistered_files)):
            errors.append(f"File '{file}' exists but is not listed in the project registry ({REGISTRY_FILE.name}).")

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
        all_errors.extend(check_trinity_logs(changed_files))
        rules = load_rules(RULES_FILE)
        all_errors.extend(check_documentation_rules(rules, changed_files))


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
