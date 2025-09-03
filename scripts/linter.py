"""
A unified, intelligent linter to enforce documentation and code quality standards.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Tuple

import yaml

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(
    command: List[str], cwd: str = str(PROJECT_ROOT), env: dict = None
) -> int:
    """Runs a command and returns its exit code."""
    try:
        process_env = os.environ.copy()
        if env:
            process_env.update(env)

        process = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=cwd,
            env=process_env,
        )
        print(process.stdout)
        if process.stderr:
            print(process.stderr, file=sys.stderr)
        return process.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}", file=sys.stderr)
        print(e.stdout, file=sys.stdout)
        print(e.stderr, file=sys.stderr)
        return e.returncode


def get_all_files() -> Tuple[Set[str], Set[str]]:
    """
    Gets all relevant files in the repository for a full audit.
    Returns a tuple of (all_files, new_files=empty_set).
    """
    all_files = set()
    relevant_dirs = ["api/", "snitch/", "gonk-testUI/", "project/"]
    for directory in relevant_dirs:
        for root, _, files in os.walk(PROJECT_ROOT / directory):
            for file in files:
                # Add relevant file types
                if file.endswith((".py", ".go", ".md", ".yml", ".yaml")):
                    full_path = Path(root) / file
                    relative_path = full_path.relative_to(PROJECT_ROOT)
                    all_files.add(str(relative_path))
    print(f"Found {len(all_files)} files to check in --run-all mode.")
    return all_files, set()


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
        subprocess.run(
            ["git", "fetch", "origin", "main"], check=False, capture_output=True
        )
        command.append("origin/main...HEAD")

    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding="utf-8"
        )

        all_changed = set()
        new_files = set()

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            status, file_path = line.split("\t")
            all_changed.add(file_path)
            if status.startswith("A"):
                new_files.add(file_path)

        print(
            f"Found {len(all_changed)} changed file(s), {len(new_files)} of which are new."
        )
        print("\n".join(f"- {f}" for f in all_changed))
        return all_changed, new_files

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        return set(), set()


def check_doc_matrix_rules(changed_files: Set[str]) -> List[str]:
    """
    Checks that if a source file is changed, its corresponding documentation file is also changed,
    based on rules in a YAML file.
    """
    errors: List[str] = []
    rules_file = PROJECT_ROOT / "scripts" / "doc-lint-rules.yml"
    if not rules_file.exists():
        print(
            "WARNING: doc-lint-rules.yml not found, skipping matrix checks.",
            file=sys.stderr,
        )
        return errors

    with open(rules_file, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f).get("rules", [])

    for rule in rules:
        source_paths = rule.get("source_paths", [])
        required_docs = rule.get("required_docs", [])

        # Check if any changed file matches any of the source paths in the rule
        source_changed = any(
            any(f.startswith(p) for p in source_paths) for f in changed_files
        )

        if source_changed:
            # If a source file changed, check if at least one required doc also changed
            doc_changed = any(d in changed_files for d in required_docs)
            if not doc_changed:
                message = rule.get(
                    "message",
                    f"Changes in {source_paths} require updates to one of {required_docs}",
                )
                errors.append(message)

    return errors


def main() -> int:
    """Main function for the unified linter."""
    parser = argparse.ArgumentParser(description="Unified Linter for Zotify API.")
    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run checks on all relevant files, not just changed ones.",
    )
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)

    print("=" * 30)
    print("Running Unified Linter")
    print("=" * 30)

    if args.run_all:
        changed_files, new_files = get_all_files()
    else:
        changed_files, new_files = get_changed_files()

    if not changed_files:
        print("No changed files detected. Exiting.")
        return 0

    # --- Flagging Phase ---
    if args.run_all:
        run_pytest = True
        run_mkdocs = True
    else:
        run_pytest = any(f.endswith((".py", ".go")) for f in changed_files)
        run_mkdocs = any(f.startswith("api/docs/") for f in changed_files)

    print("\n--- Checks to run ---")
    print(f"Doc Matrix Linter: Always")
    print(f"Pytest: {run_pytest}")
    print(f"MkDocs Build: {run_mkdocs}")
    print("-----------------------\n")

    # --- Execution Phase ---
    final_return_code = 0

    # 1. Documentation Matrix Linter (Always runs on changed files)
    # This check is less meaningful in --run-all mode but we run it anyway.
    print("--- Running Documentation Matrix Linter ---")
    doc_errors = check_doc_matrix_rules(changed_files)
    if doc_errors:
        print("Documentation Matrix Linter Failed:", file=sys.stderr)
        for error in doc_errors:
            print(f"- {error}", file=sys.stderr)
        final_return_code = 1
    else:
        print("Documentation Matrix Linter Passed!")
    print("-" * 37)
    if final_return_code != 0:
        # This check is critical, so we exit early if it fails.
        return final_return_code

    # 2. Pytest (Conditional)
    if run_pytest:
        print("\n--- Running Pytest ---")
        # run_lint.sh sets APP_ENV=development, we will do the same.
        pytest_return_code = run_command(
            ["pytest"], cwd=str(PROJECT_ROOT / "api"), env={"APP_ENV": "development"}
        )
        if pytest_return_code != 0:
            print("Pytest Failed!", file=sys.stderr)
            final_return_code = 1
        else:
            print("Pytest Passed!")
        print("-" * 22)
    else:
        print("\nSkipping Pytest: No code changes detected.")

    # 3. MkDocs Build (Conditional)
    if run_mkdocs:
        print("\n--- Running MkDocs Build ---")
        mkdocs_return_code = run_command(["mkdocs", "build", "--clean"])
        if mkdocs_return_code != 0:
            print("MkDocs Build Failed!", file=sys.stderr)
            final_return_code = 1
        else:
            print("MkDocs Build Passed!")
        print("-" * 26)
    else:
        print("\nSkipping MkDocs Build: No relevant documentation changes detected.")

    print("\n" + "=" * 30)
    if final_return_code == 0:
        print("✅ Unified Linter Passed!")
    else:
        print("❌ Unified Linter Failed.")
    print("=" * 30)

    return final_return_code


if __name__ == "__main__":
    sys.exit(main())
