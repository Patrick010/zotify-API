"""
A unified, intelligent linter to enforce documentation and code quality standards.
"""

import os
import re
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Set, Tuple

import yaml
import datetime
import textwrap

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent


# --- Logging Functions (from log-work.py) ---
def get_formatted_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_next_act_number(file_path="project/logs/ACTIVITY.md"):
    """Finds the latest ACT-XXX number in the activity log and returns the next number."""
    try:
        with open(PROJECT_ROOT / file_path, "r") as f:
            content = f.read()
        act_numbers = re.findall(r"## ACT-(\d+):", content)
        if not act_numbers:
            return 1
        return max([int(n) for n in act_numbers]) + 1
    except FileNotFoundError:
        return 1


def format_activity_log(act_number, summary, objective, findings, files=None):
    """Formats the log entry for ACTIVITY.md."""
    related_docs_section = ""
    if files:
        file_list = "\n".join([f"- `{f}`" for f in files])
        related_docs_section = f"### Related Documents\n{file_list}"

    # Manually format the string to avoid indentation issues
    return f"""---
## ACT-{act_number:03d}: {summary}

**Date:** {get_formatted_date()}
**Status:** ✅ Done
**Assignee:** Jules

### Objective
{objective or summary}

### Outcome
{findings}

{related_docs_section}""".strip()


def format_session_log(summary, findings):
    """Formats the log entry for SESSION_LOG.md."""
    return f"""---
## Session Report: {get_formatted_date()}

**Summary:** {summary}
**Findings:**
{findings}"""


def format_current_state(summary, objective, next_steps):
    """Formats the content for CURRENT_STATE.md."""
    objective_section = f"## Objective\n{objective}\n\n" if objective else ""

    return textwrap.dedent(
        f"""
    # Project State as of {get_formatted_date()}

    **Status:** Live Document

{objective_section}    ## 1. Session Summary & Accomplishments
    {summary}

    ## 2. Known Issues & Blockers
    - None

    ## 3. Pending Work: Next Immediate Steps
    {next_steps}
    """
    )


def prepend_to_file(file_path, content):
    """Prepends new content to the beginning of a file."""
    try:
        with open(PROJECT_ROOT / file_path, "r+") as f:
            original_content = f.read()
            f.seek(0)
            f.write(content.strip() + "\n\n" + original_content)
        print(f"Successfully updated {file_path}")
    except IOError as e:
        print(f"Error updating {file_path}: {e}")


def write_to_file(file_path, content):
    """Writes content to a file, overwriting existing content."""
    try:
        with open(PROJECT_ROOT / file_path, "w") as f:
            f.write(content.strip() + "\n")
        print(f"Successfully updated {file_path}")
    except IOError as e:
        print(f"Error updating {file_path}: {e}")


def do_logging(summary: str, objective: str, findings: str, next_steps: str, files: List[str]) -> int:
    """The main logic for the logging functionality."""
    print("--- Running Logging ---")
    act_number = get_next_act_number()
    activity_entry = format_activity_log(act_number, summary, objective, findings, files)
    prepend_to_file("project/logs/ACTIVITY.md", activity_entry)

    session_entry = format_session_log(summary, findings)
    prepend_to_file("project/logs/SESSION_LOG.md", session_entry)

    current_state_content = format_current_state(summary, objective, next_steps)
    write_to_file("project/logs/CURRENT_STATE.md", current_state_content)
    print("--- Logging Complete ---")
    return 0


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


def get_changed_files() -> List[Tuple[str, str]]:
    """
    Gets the list of changed files from git, correctly handling renames.
    Returns a list of tuples (status, file_path).
    """
    # Note: This logic was updated to correctly handle renamed files, which caused
    # the previous implementation to crash. The main function is adapted to handle
    # the list of tuples return type.
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
        output = result.stdout.strip().splitlines()

        changed_files_list = []
        for line in output:
            if not line:
                continue
            parts = line.split("\t")
            status = parts[0]
            if status.startswith("R"):  # Renamed file (e.g., R100\told_path\tnew_path)
                old_path, new_path = parts[1], parts[2]
                # Treat a rename as a change to both the old and new paths
                # so that rules for both locations are triggered.
                changed_files_list.append((status, old_path))
                changed_files_list.append((status, new_path))
            else:  # Modified (M), Added (A), Deleted (D), etc.
                file_path = parts[1]
                changed_files_list.append((status, file_path))

        print(f"Found {len(changed_files_list)} changed file(s) based on status.")
        print("\n".join(f"- {status}\t{f}" for status, f in changed_files_list))
        return changed_files_list

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"FATAL: Could not get changed files from git: {e}", file=sys.stderr)
        return []


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
        is_unconditional = not source_paths

        # Check if any changed file matches any of the source paths in the rule
        source_changed = any(
            any(f.startswith(p) for p in source_paths) for f in changed_files
        )

        # A rule is triggered if it's unconditional OR if a source file matches.
        if is_unconditional or source_changed:
            # If the rule is triggered, check if the required docs also changed.
            # The "Enforce Mandatory Logging" rule is special and requires ALL docs to be present.
            # Other rules only require ANY doc to be present.
            doc_changed = False
            if rule.get("name") == "Enforce Mandatory Logging":
                doc_changed = all(d in changed_files for d in required_docs)
            else:
                doc_changed = any(d in changed_files for d in required_docs)

            if not doc_changed:
                message = rule.get(
                    "message",
                    f"Changes in {source_paths} require updates to one of {required_docs}",
                )
                errors.append(message)

    return errors


def run_mkdocs_check():
    docs_dir = "api/docs"
    if not os.path.isdir(docs_dir):
        print(f"Docs directory not found: {docs_dir}")
        return True  # no docs, nothing to check

    print("Running mkdocs validation...")
    try:
        # Note: The user-provided snippet is adapted here to use the existing
        # run_command function for consistency in output and error handling.
        # The return code of run_command is 0 on success.
        return_code = run_command(
            ["mkdocs", "build"],
        )
        if return_code == 0:
            return True
        else:
            print("mkdocs validation failed.")
            return False
    except subprocess.CalledProcessError:
        print("mkdocs validation failed.")
        return False


def check_quality_index_ratings() -> List[str]:
    """
    Parses the CODE_QUALITY_INDEX.md file and checks for invalid ratings.
    """
    errors: List[str] = []
    quality_index_file = PROJECT_ROOT / "api" / "docs" / "CODE_QUALITY_INDEX.md"
    if not quality_index_file.exists():
        return []

    valid_scores = {"A", "B", "C", "D", "F"}
    with open(quality_index_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_data_table = False
    for i, line in enumerate(lines):
        # The real data tables start with a header like this.
        # This prevents the linter from parsing the rubric tables in the legend.
        if "| File Path |" in line and "| Documentation Score |" in line:
            in_data_table = True
            continue

        if not in_data_table:
            continue

        if not line.strip().startswith("|"):
            continue
        if "---" in line:
            continue

        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue

        doc_score = parts[2]
        code_score = parts[3]

        if doc_score and doc_score not in valid_scores:
            errors.append(
                f"Invalid 'Doc Score' in CODE_QUALITY_INDEX.md on line {i+1}: '{doc_score}'. "
                f"Score must be one of {sorted(list(valid_scores))}"
            )
        if code_score and code_score not in valid_scores:
            errors.append(
                f"Invalid 'Code Score' in CODE_QUALITY_INDEX.md on line {i+1}: '{code_score}'. "
                f"Score must be one of {sorted(list(valid_scores))}"
            )

    return errors


def main() -> int:
    """Main function for the unified linter and logger."""
    parser = argparse.ArgumentParser(
        description="Unified Linter and Logger for Zotify.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # --- Logger Arguments ---
    parser.add_argument(
        "--log",
        action="store_true",
        help="Run in logging mode. Requires --summary, --findings, and --next-steps.",
    )
    parser.add_argument(
        "--summary",
        help="[Logger] A one-line summary of the task, used as the entry title.",
    )
    parser.add_argument(
        "--objective",
        help="[Logger] The high-level purpose of the task.",
    )
    parser.add_argument(
        "--findings",
        help="[Logger] A multi-line description of the findings. Use '\\n' for new lines.",
    )
    parser.add_argument(
        "--next-steps",
        help="[Logger] A multi-line description of the next immediate steps.",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="[Logger] An optional list of file paths related to the activity.",
    )
    # --- Linter Test Arguments ---
    parser.add_argument(
        "--test-files",
        nargs="*",
        help="[Linter-Test] A list of file paths to test, bypassing git.",
    )
    parser.add_argument(
        "--from-file",
        help="[Linter-CI] Read list of changed files from a text file (one file per line).",
    )

    args = parser.parse_args()
    os.chdir(PROJECT_ROOT)

    # --- Mode Selection ---
    if args.log:
        if not all([args.summary, args.findings, args.next_steps]):
            print(
                "ERROR: In --log mode, you must provide --summary, --findings, and --next-steps.",
                file=sys.stderr,
            )
            return 1
        # Run logging and exit
        return do_logging(
            args.summary,
            args.objective,
            args.findings,
            args.next_steps,
            args.files or [],
        )

    # --- Linter Mode ---
    print("=" * 30)
    print("Running Unified Linter")
    print("=" * 30)

    changed_files_with_status = []
    if args.from_file:
        print(f"--- Reading changed files from {args.from_file} ---")
        try:
            with open(args.from_file, "r") as f:
                # Assume all files from the file are 'Modified' for status
                files = [line.strip() for line in f if line.strip()]
                changed_files_with_status = [("M", f) for f in files]
            print(f"Found {len(changed_files_with_status)} changed file(s).")
        except FileNotFoundError:
            print(
                f"ERROR: File specified by --from-file not found: {args.from_file}",
                file=sys.stderr,
            )
            return 1
    elif args.test_files:
        print("--- Running in Test Mode ---")
        # In test mode, we simulate the status as 'M' (Modified) for all provided files.
        changed_files_with_status = [("M", f) for f in args.test_files]
        print(f"Injecting {len(changed_files_with_status)} file(s) for testing.")
        print("\n".join(f"- M\t{f}" for f in args.test_files))
    else:
        # Default to getting files from git
        changed_files_with_status = get_changed_files()

    if not changed_files_with_status:
        print("No changed files detected. Exiting.")
        return 0

    # The rest of the script expects a set of file paths, not a list of tuples.
    # We extract the file paths here.
    changed_files = {file_path for _, file_path in changed_files_with_status}

    # --- Flagging Phase ---
    run_mkdocs = any(f.startswith("api/docs/") for f in changed_files)
    run_quality_check = "api/docs/CODE_QUALITY_INDEX.md" in changed_files

    print("\n--- Checks to run ---")
    print("Doc Matrix Linter: Always")
    print(f"Quality Index Linter: {run_quality_check}")
    print(f"MkDocs Build: {run_mkdocs}")
    print("-----------------------\n")

    # --- Execution Phase ---
    final_return_code = 0

    # 1. Documentation Matrix Linter (Always runs)
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
        return final_return_code  # Early exit if core rules fail

    # 2. Code Quality Index Linter (Conditional)
    if run_quality_check:
        print("\n--- Running Code Quality Index Linter ---")
        quality_errors = check_quality_index_ratings()
        if quality_errors:
            print("Code Quality Index Linter Failed:", file=sys.stderr)
            for error in quality_errors:
                print(f"- {error}", file=sys.stderr)
            final_return_code = 1
        else:
            print("Code Quality Index Linter Passed!")
        print("-" * 37)

    # 3. MkDocs Build (Conditional)
    if run_mkdocs:
        print("\n--- Running MkDocs Build ---")
        if not run_mkdocs_check():
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
