"""
A custom linter to enforce documentation changes alongside code changes.

This script checks a git diff for modified source files and ensures their
corresponding documentation, as defined in a rules file, has also been modified.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / "scripts" / "doc-lint-rules.yml"

# The "Trinity" of mandatory log files that must be updated in most commits.
TRINITY_LOG_FILES = {
    "project/logs/CURRENT_STATE.md",
    "project/logs/ACTIVITY.md",
    "project/logs/SESSION_LOG.md",
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


def main() -> int:
    """Main function for the linter."""
    print("="*20)
    print("Running Documentation Linter")
    print("="*20)

    changed_files = get_changed_files()
    if not changed_files:
        print("No changed files detected. Exiting.")
        return 0

    all_errors: List[str] = []

    # Run all checks and collect errors
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
