"""
A custom linter to enforce documentation changes alongside code changes.

This script checks a git diff for modified source files and ensures their
corresponding documentation, as inferred by module path, has also been modified.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
RULES_FILE = PROJECT_ROOT / "lint-rules.yml"

# Define the "Trinity" of mandatory log files
TRINITY_LOG_FILES = {
    "project/logs/CURRENT_STATE.md",
    "project/logs/ACTIVITY.md",
    "project/logs/SESSION_LOG.md",
}


def get_changed_files() -> Set[str]:
    """
    Gets the set of changed files.

    In a pre-commit environment, it checks staged files.
    In a CI environment, it checks files changed against the main branch.
    """
    is_precommit = os.environ.get("PRE_COMMIT") == "1"

    command = []
    if is_precommit:
        print("Running in pre-commit mode (checking staged files)...")
        command = ["git", "diff", "--name-only", "--cached"]
    else:
        print("Running in CI mode (checking against main branch)...")
        # First, ensure we have the target branch available
        subprocess.run(["git", "fetch", "origin", "main"], check=True, capture_output=True)
        command = ["git", "diff", "--name-only", "origin/main...HEAD"]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        return set(line for line in result.stdout.strip().split("\n") if line)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        return set()


def load_rules() -> List[Dict[str, Any]]:
    """Loads and validates the rules from lint-rules.yml."""
    if not RULES_FILE.exists():
        print(f"Warning: Rules file not found at {RULES_FILE}. Skipping.", file=sys.stderr)
        return []
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict) or "rules" not in data or not isinstance(data["rules"], list):
        print(f"Error: Invalid format in {RULES_FILE}. Expected a 'rules' key with a list.", file=sys.stderr)
        return []

    return data["rules"]


def check_conditional_rules(rules: List[Dict[str, Any]], changed_files: Set[str]) -> List[str]:
    """
    Checks if changes in source paths are accompanied by required doc changes.
    """
    errors: List[str] = []
    for rule in rules:
        source_paths = rule.get("source_paths", [])
        required_docs = rule.get("required_docs", [])
        message = rule.get("message", f"Rule '{rule.get('name', 'Unnamed')}' failed.")

        # Check if any changed file matches a source path for this rule
        source_change_found = any(
            any(changed_file.startswith(src_path) for src_path in source_paths)
            for changed_file in changed_files
        )

        if not source_change_found:
            continue

        # If a source change was found, check if a required doc was also changed
        doc_change_found = any(
            any(changed_file == doc_path for doc_path in required_docs)
            for changed_file in changed_files
        )

        if not doc_change_found:
            errors.append(message)

    return errors


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

    errors: List[str] = []

    # --- Trinity Check ---
    # Any commit must include the Trinity logs, unless only those logs are changed.
    if changed_files and not changed_files.issubset(TRINITY_LOG_FILES):
        missing_trinity_files = TRINITY_LOG_FILES - changed_files
        if missing_trinity_files:
            for f in sorted(list(missing_trinity_files)):
                errors.append(f"Mandatory log file was not updated: {f}")
    # --- End Trinity Check ---

    # --- Conditional Documentation Check ---
    rules = load_rules()
    conditional_errors = check_conditional_rules(rules, changed_files)
    errors.extend(conditional_errors)
    # --- End Conditional Documentation Check ---

    if errors:
        print("\n--- Documentation Linter Failed ---", file=sys.stderr)
        for error in sorted(list(set(errors))): # Use set to remove duplicate messages
            print(f"ERROR: {error}", file=sys.stderr)
        print("-----------------------------------", file=sys.stderr)
        return 1

    print("\nDocumentation Linter Passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
