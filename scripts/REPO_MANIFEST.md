

--- FILE: REPO_MANIFEST.md ---



--- FILE: CODE_FILE_INDEX.md ---

# Code File Index

This file is auto-generated. Do not edit manually.

| Path | Type | Description | Status | Linked Docs | Notes |
|------|------|-------------|--------|-------------|-------|
| `scripts/audit_api.py` | | | Active | | |
| `scripts/audit_endpoints.py` | | | Active | | |
| `scripts/doc-lint-rules.yml` | | | Active | | |
| `scripts/functional_test.py` | | | Active | | |
| `scripts/generate_endpoints_doc.py` | | | Active | | |
| `scripts/generate_openapi.py` | | | Active | | |
| `scripts/linter.py` | | | Active | | |
| `scripts/manage_docs_index.py` | | | Active | | |
| `scripts/repo_inventory_and_governance.py` | | | Active | | |
| `scripts/run_e2e_auth_test.sh` | | | Active | | |
| `scripts/start.sh` | | | Active | | |
| `scripts/test_auth_flow.py` | | | Active | | |
| `scripts/test_single_config.sh` | | | Active | | |
| `scripts/validate_code_index.py` | | | Active | | |


--- FILE: repo_inventory_and_governance.py ---

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
IGNORED_FILES = {"mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt", "verification_report.md", "LICENSE"}

INDEX_MAP = [
    # --- API Documentation ---
    {
        "match": lambda path, ftype: ftype == "doc" and path.startswith("api/docs/"),
        "indexes": [
            "api/docs/MASTER_INDEX.md",
            "api/docs/DOCS_QUALITY_INDEX.md",
        ],
    },
    # --- Project-level Documentation ---
    {
        "match": lambda path, ftype: ftype == "doc" and (
            path.startswith("project/archive/docs/") or
            path.startswith("project/logs/") or
            path.startswith("project/process/") or
            path.startswith("project/proposals/") or
            path.startswith("project/reports/") or
            path.startswith("project/") and Path(path).parent.name == "project"
        ),
        "indexes": ["project/PROJECT_REGISTRY.md"],
    },
    # --- Component Documentation ---
    {
        "match": lambda path, ftype: ftype == "doc" and path.startswith("Gonk/GonkCLI/docs/"),
        "indexes": ["Gonk/GonkCLI/DOCS_INDEX.md"],
    },
    {
        "match": lambda path, ftype: ftype == "doc" and path.startswith("Gonk/GonkUI/docs/"),
        "indexes": ["Gonk/GonkUI/DOCS_INDEX.md"],
    },
    {
        "match": lambda path, ftype: ftype == "doc" and path.startswith("snitch/docs/"),
        "indexes": ["snitch/DOCS_INDEX.md"],
    },
    # --- Code Indexes ---
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
        # Resolve path relative to the index file's location
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
    else: # Default to a simple list for other doc indexes
        # Make links relative to the new index file
        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent) for f in files_to_add]
        lines = [f"*   [{Path(f).name}]({link})" for f, link in zip(files_to_add, relative_links)]


    with open(index_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(sorted(lines)) + "\n")

def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    """Generates a human-readable audit report and returns an exit code."""
    print("\n" + "=" * 50)
    print("Governance Audit Report")
    print("=" * 50)

    missing_by_index = {}
    registered_count = 0
    missing_count = 0
    exempted_count = 0
    wrongly_exempted = []

    for item in trace_index:
        if item["registered"] == "exempted":
            exempted_count += 1
            if item['type'] == 'doc':
                wrongly_exempted.append(item['path'])
        elif item["registered"] is True:
            registered_count += 1
        else:
            missing_count += 1
            for index_file in item.get("missing_from", []):
                if index_file not in missing_by_index:
                    missing_by_index[index_file] = []
                missing_by_index[index_file].append(item["path"])

    if wrongly_exempted:
        print("\n--- 🚨 Wrongly Exempted Documents ---")
        print("The following .md files were marked 'exempted' but should be registered:")
        for path in sorted(wrongly_exempted):
            print(f"  - {path}")


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
    print(f"- Wrongly Exempted Docs: {len(wrongly_exempted)}")
    print("-" * 20)

    if missing_count > 0 or wrongly_exempted:
        print("\nStatus: ❌ FAIL")
        return 1
    else:
        print("\nStatus: ✅ PASS")
        return 0

def validate_trace_index_schema(trace_index_path: Path) -> bool:
    """Loads the generated TRACE_INDEX.yml and validates its schema."""
    print("\n--- Validating TRACE_INDEX.yml Schema ---")
    try:
        with open(trace_index_path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: Could not load or parse TRACE_INDEX.yml: {e}", file=sys.stderr)
        return False

    errors = []
    if 'artifacts' not in data or not isinstance(data['artifacts'], list):
        errors.append("FATAL: 'artifacts' key is missing or not a list.")
        print("\n".join(errors), file=sys.stderr)
        return False

    for i, artifact in enumerate(data['artifacts']):
        path = artifact.get('path')
        reg_status = artifact.get('registered')
        index_val = artifact.get('index')

        if reg_status is True:
            if not isinstance(index_val, list) or not all(isinstance(x, str) for x in index_val):
                errors.append(f"Schema Error (path: {path}): If registered is true, 'index' must be a list of strings.")
        elif reg_status is False:
            if index_val != "-":
                errors.append(f"Schema Error (path: {path}): If registered is false, 'index' must be '-'.")
            if 'missing_from' not in artifact or not isinstance(artifact['missing_from'], list):
                errors.append(f"Schema Error (path: {path}): If registered is false, 'missing_from' must be a list.")
        elif reg_status == "exempted":
            if index_val != "-":
                 errors.append(f"Schema Error (path: {path}): If registered is 'exempted', 'index' must be '-'.")
        else:
            errors.append(f"Schema Error (path: {path}): Invalid 'registered' status: {reg_status}")

    if errors:
        print("TRACE_INDEX.yml schema validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return False

    print("Schema validation passed!")
    return True


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

        # Core logic change: No .md file should be exempt unless explicitly ignored.
        if file_type == 'doc' and not required_indexes and file_path not in IGNORED_FILES:
             # This doc file has no rule. Flag it as unregistered against the default project registry.
            required_indexes.append("project/PROJECT_REGISTRY.md")


        if not required_indexes:
            trace_entry["registered"] = "exempted"
            trace_entry["index"] = "-"
        else:
            found_in, missing_from = check_registration(file_path, required_indexes, all_indexes_content)

            if not missing_from:
                trace_entry["registered"] = True
                trace_entry["index"] = found_in
            else:
                trace_entry["registered"] = False
                trace_entry["index"] = "-"
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

    output = {"artifacts": trace_index}
    trace_index_path = PROJECT_ROOT / "TRACE_INDEX.yml"
    with open(trace_index_path, "w") as f:
        yaml.safe_dump(output, f, default_flow_style=False, sort_keys=False)
    print("TRACE_INDEX.yml generated successfully.")

    # --- Validation and Reporting ---
    if not validate_trace_index_schema(trace_index_path):
        return 1 # Exit with failure if schema is invalid

    return generate_audit_report(trace_index)

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

--- FILE: generate_endpoints_doc.py ---

import json


def generate_endpoints_md():
    with open("openapi.json", "r") as f:
        openapi_spec = json.load(f)

    endpoints_by_tag = {}
    for path, path_item in openapi_spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if "tags" in operation and operation["tags"]:
                tag = operation["tags"][0]
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []

                auth_required = False
                if "parameters" in operation:
                    for param in operation["parameters"]:
                        if param.get("name") == "X-API-Key":
                            auth_required = True
                            break

                # Also check security at operation level
                if "security" in operation:
                    # A bit simplistic, but good enough for this purpose
                    auth_required = True

                summary = operation.get("summary", "")
                endpoints_by_tag[tag].append(
                    f"| {method.upper()} | `{path}` | {summary} | {'Yes' if auth_required else 'No'} |"
                )

    markdown_content = """# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify API project, generated from the OpenAPI schema. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   This file is auto-generated. Do not edit it manually.

---

## Zotify API Endpoints
"""

    for tag in sorted(endpoints_by_tag.keys()):
        markdown_content += f"\n### `{tag}`\n"
        markdown_content += "| Method | Path | Summary | Auth Required |\n"
        markdown_content += "|---|---|---|---|\n"
        markdown_content += "\n".join(sorted(endpoints_by_tag[tag]))
        markdown_content += "\n"

    with open("project/ENDPOINTS.md", "w") as f:
        f.write(markdown_content)

    print("project/ENDPOINTS.md generated successfully.")


if __name__ == "__main__":
    generate_endpoints_md()


--- FILE: test_auth_flow.py ---

import os
import sys
import time
import secrets
import string
import webbrowser
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
REDIRECT_URI = "http://127.0.0.1:4381/login"
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
CALLBACK_POLL_URL = f"{API_BASE_URL}/login"  # Adjust if needed


def check_api():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if r.status_code == 200:
            print(f"[INFO] API reachable at {API_BASE_URL}")
            return True
    except requests.RequestException:
        pass  # The error is logged below
    print(f"[ERROR] Cannot reach API at {API_BASE_URL}")
    return False


def generate_state(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def build_auth_url(client_id, redirect_uri, state, scope="user-read-email"):
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": scope,
        "show_dialog": "true",
    }
    from urllib.parse import urlencode

    return f"{AUTH_ENDPOINT}?{urlencode(params)}"


def poll_callback(state, timeout=180, interval=3):
    print(f"[WAITING] Polling for callback for up to {timeout} seconds...")
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            resp = requests.get(CALLBACK_POLL_URL, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("state") == state and "code" in data:
                    print("[INFO] Received callback data:")
                    print(f"       Code: {data['code']}")
                    print(f"       State: {data['state']}")
                    return True
        except requests.RequestException:
            pass
        time.sleep(interval)
    print("[ERROR] Timeout waiting for callback.")
    return False


def main():
    if not SPOTIFY_CLIENT_ID:
        print("[ERROR] SPOTIFY_CLIENT_ID environment variable is not set.")
        sys.exit(1)
    if not check_api():
        sys.exit(1)

    state = generate_state()
    auth_url = build_auth_url(SPOTIFY_CLIENT_ID, REDIRECT_URI, state)

    print(
        "\n[STEP] Open this URL in your Windows browser to start Spotify auth flow:\n"
    )
    print(auth_url + "\n")

    print("[STEP] Then manually run 'snitch_debug.exe' on your Windows machine.")
    print(f"        It must listen on {REDIRECT_URI} to capture the callback.\n")

    try:
        webbrowser.open(auth_url)
    except Exception:
        print("[WARN] Could not open browser automatically. Open URL manually.")

    success = poll_callback(state)
    if success:
        print("[SUCCESS] Auth flow completed.")
    else:
        print("[FAILURE] Auth flow did not complete successfully.")


if __name__ == "__main__":
    main()


--- FILE: linter.py ---

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


def run_governance_check() -> int:
    """Runs the repository inventory and governance check."""
    print("\n--- Running Repository Governance Check ---")
    script_path = PROJECT_ROOT / "scripts" / "repo_inventory_and_governance.py"
    if not script_path.exists():
        print("ERROR: repo_inventory_and_governance.py not found.", file=sys.stderr)
        return 1

    return_code = run_command([sys.executable, str(script_path)])
    if return_code != 0:
        print("Repository Governance Check Failed!", file=sys.stderr)
    else:
        print("Repository Governance Check Passed!")
    print("-" * 41)
    return return_code


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
    parser.add_argument(
        "--skip-governance",
        action="store_true",
        help="[Linter] Skip the repository inventory and governance check.",
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

    # The governance check runs independently of changed files, so we run it first.
    final_return_code = 0
    if not args.skip_governance:
        gov_return_code = run_governance_check()
        if gov_return_code != 0:
            final_return_code = 1
            # Early exit if governance fails, as it's a fundamental check
            print("\n" + "=" * 30)
            print("❌ Unified Linter Failed.")
            print("=" * 30)
            return final_return_code
    else:
        print("Skipping Repository Governance Check.")


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


--- FILE: audit_api.py ---

import importlib
import os
import httpx
from fastapi import FastAPI

# Adjust this to your actual app import path:
app_module = "zotify_api.main"
app_attr = "app"
BASE_URL = "http://127.0.0.1:8000"


def main():
    """
    Dynamically imports the FastAPI app, discovers all GET routes that
    don't require path parameters, and then sends a request to each one
    to check its status.
    """
    print(f"--- Starting API Audit for {app_module} ---")
    print(f"--- Target Base URL: {BASE_URL} ---")

    # Set the app environment to development to avoid startup errors
    os.environ["APP_ENV"] = "development"

    try:
        module = importlib.import_module(app_module)
        app: FastAPI = getattr(module, app_attr)
    except Exception as e:
        print(
            f"Error: Could not import FastAPI app '{app_attr}' from module '{app_module}'."
        )
        print(f"Details: {e}")
        return

    ok_routes = []
    error_routes = []

    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        for route in app.routes:
            # We can only automatically test GET routes that have no path parameters
            if "GET" in route.methods and "{" not in route.path:
                path = route.path
                print(f"Testing GET {path}...")
                try:
                    response = client.get(path)
                    if response.status_code == 200:
                        ok_routes.append(path)
                    else:
                        error_routes.append(f"{path} (Status: {response.status_code})")
                except httpx.RequestError as e:
                    error_routes.append(f"{path} (Request Error: {e})")

    print("\n--- API Audit Summary ---")
    if ok_routes:
        print("✅ OK Routes:")
        for r in sorted(ok_routes):
            print(f" - {r}")

    if error_routes:
        print("\n❌ Error Routes:")
        for r in sorted(error_routes):
            print(f" - {r}")

    if not error_routes:
        print("\nAll discoverable GET routes responded successfully.")


if __name__ == "__main__":
    main()


--- FILE: generate_openapi.py ---

import json
import os
import sys
from pathlib import Path

# Set app environment to testing
os.environ["APP_ENV"] = "testing"

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.src.zotify_api.main import app


def generate_openapi_spec():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("openapi.json generated successfully.")


if __name__ == "__main__":
    generate_openapi_spec()


--- FILE: manage_docs_index.py ---

import os
import re
import argparse
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
DOC_DIRS_TO_INDEX = ["api/docs", "snitch/docs", "Gonk/GonkUI/docs"]
DOCS_QUALITY_INDEX = PROJECT_ROOT / "api/docs/DOCS_QUALITY_INDEX.md"

# --- Main Functions ---

def get_all_markdown_files():
    """Scans the doc directories and returns a list of all .md files."""
    md_files = []
    for directory in DOC_DIRS_TO_INDEX:
        for root, _, files in os.walk(PROJECT_ROOT / directory):
            for file in files:
                if file.endswith(".md"):
                    # Store the path relative to the project root
                    md_files.append(Path(root) / file)
    return md_files

def get_indexed_docs():
    """Parses the DOCS_QUALITY_INDEX.md to find which files are already indexed."""
    indexed = set()
    if not DOCS_QUALITY_INDEX.is_file():
        return indexed

    with open(DOCS_QUALITY_INDEX, "r", encoding="utf-8") as f:
        # Skip header and separator
        f.readline()
        f.readline()
        for line in f:
            if not line.strip():
                continue
            try:
                # Path is in the second column
                path = line.split("|")[2].strip()
                indexed.add(path)
            except IndexError:
                continue
    return indexed

def add_to_docs_quality_index(doc_path):
    """Appends a new entry for a markdown file to the quality index."""
    # Use the filename as the module name for simplicity
    module_name = doc_path.stem.replace("_", " ").title()
    # Get path relative to project root
    relative_path = doc_path.relative_to(PROJECT_ROOT).as_posix()
    entry = f"| {module_name} | {relative_path} | X |\n"

    with open(DOCS_QUALITY_INDEX, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  - Added '{relative_path}' to {DOCS_QUALITY_INDEX.name}")

def main():
    """Main function to manage the documentation quality index."""
    parser = argparse.ArgumentParser(description="Manage the documentation quality index.")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run the script to find and add missing markdown files to the index."
    )
    args = parser.parse_args()

    if not args.run:
        print("This script populates the DOCS_QUALITY_INDEX.md file.")
        print("Run with the --run flag to execute.")
        return

    print("--- Starting Docs Quality Indexer ---")

    all_md_files = get_all_markdown_files()
    indexed_docs = get_indexed_docs()

    new_entries_added = 0

    for md_path in all_md_files:
        relative_path_str = md_path.relative_to(PROJECT_ROOT).as_posix()
        if relative_path_str not in indexed_docs:
            new_entries_added += 1
            print(f"\nFound un-indexed doc file: {relative_path_str}")
            add_to_docs_quality_index(md_path)

    if new_entries_added == 0:
        print("\nNo new markdown files to index. Everything is up to date.")
    else:
        print(f"\nSuccessfully added {new_entries_added} new file(s) to the index.")

    print("--- Indexer Finished ---")

if __name__ == "__main__":
    main()


--- FILE: doc-lint-rules.yml ---

# This file defines the "documentation matrix" for the custom linter.
# It maps changes in source code paths to required changes in documentation files.

rules:
  - name: "Source Documentation Registration"
    source_paths:
      - "api/docs/reference/source/"
    required_docs:
      - "api/docs/MASTER_INDEX.md"
    message: |
      New source documentation must be registered in MASTER_INDEX.md.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Source Documentation Quality Tracking"
    source_paths:
      - "api/docs/reference/source/"
    required_docs:
      - "api/docs/DOCS_QUALITY_INDEX.md"
    message: |
      New source documentation must be added to the DOCS_QUALITY_INDEX.md for quality tracking.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Enforce Mandatory Logging"
    source_paths:
      - "api/src/zotify_api/"
      - "project/"
      - "api/docs/"
      - "snitch/"
      - "Gonk/GonkUI/"
      - "scripts/"
      - "AGENTS.md"
      - ".github/workflows/ci.yml"
      - "README.md"
    required_docs:
      - "project/logs/ACTIVITY.md"
      - "project/logs/SESSION_LOG.md"
      - "project/logs/CURRENT_STATE.md"
    message: |
      Changes to code or documentation must be logged. Please run the linter's
      --log command to update the project logs.

  - name: "API Route Change"
    source_paths:
      - "api/src/zotify_api/routes/"
    required_docs:
      - "project/ENDPOINTS.md"
      - "api/docs/reference/API_REFERENCE.md"
    message: |
      Changes to API routes require an update to the endpoint documentation.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "High-Level Design Change"
    source_paths:
      - "project/HIGH_LEVEL_DESIGN.md"
      - "project/LOW_LEVEL_DESIGN.md"
    required_docs:
      - "project/ALIGNMENT_MATRIX.md"
    message: |
      Changes to core design documents must be reflected in the traceability matrix.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Agent Workflow Change"
    source_paths:
      - "AGENTS.md"
      - "scripts/linter.py"
    # The Handover Brief is a point-in-time document and must not be changed
    # after the initial session, except when the user asks for it.
    forbidden_docs:
      - "project/HANDOVER_BRIEF.md"
    message: |
      The Handover Brief cannot be modified.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Database Model Change"
    source_paths:
      - "api/src/zotify_api/database/models.py"
    required_docs:
      - "project/LOW_LEVEL_DESIGN.md"
    message: |
      Changes to database models should be reflected in the Low-Level Design document.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "CI/CD Pipeline Change"
    source_paths:
      - ".github/workflows/ci.yml"
    required_docs:
      - "project/CICD.md"
      - "api/docs/manuals/CICD.md"
    message: |
      Changes to the CI/CD pipeline must be documented in the CICD guides.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Alignment Matrix Maintenance"
    source_paths:
      - "api/src/zotify_api/"
      - "snitch/"
      - "Gonk/GonkUI/"
      - "scripts/"
    required_docs:
      - "project/ALIGNMENT_MATRIX.md"
    message: |
      All code changes must be reflected in `project/ALIGNMENT_MATRIX.md`.
      Refer to QA_GOVERNANCE.md (Section: Alignment & Traceability) for policy details.

  - name: "MASTER Index Maintenance"
    source_paths:
      - "api/docs/"
    required_docs:
      - "api/docs/MASTER_INDEX.md"
    message: |
      All documents under api/docs/ must be registered in api/docs/MASTER_INDEX.md.
      Update MASTER_INDEX.md to reflect additions, removals, or renames.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Code Quality Index Maintenance"
    source_paths:
      - "api/src/"
      - "snitch/"
      - "Gonk/GonkUI/"
      - "scripts/"
    required_docs:
      - "api/docs/CODE_QUALITY_INDEX.md"
    message: |
      Any source file changes must be reflected in api/docs/CODE_QUALITY_INDEX.md.
      Add/update the relevant entry to maintain code quality coverage.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Project Registry Maintenance"
    source_paths:
      - "project/"
    required_docs:
      - "project/PROJECT_REGISTRY.md"
    message: |
      All project-level governance and process documents must be registered in
      `project/PROJECT_REGISTRY.md`. Update it when adding, renaming, or removing docs.
      Refer to QA_GOVERNANCE.md for policy details.

  - name: "Documentation Update Enforcement"
    source_paths:
      - "api/src/"
      - "snitch/"
      - "Gonk/GonkUI/"
      - "scripts/"
      - "project/"
      - "api/docs/"
    required_docs:
      - "project/ALIGNMENT_MATRIX.md"
      - "api/docs/CODE_QUALITY_INDEX.md"
      - "project/PROJECT_REGISTRY.md"
      - "api/docs/MASTER_INDEX.md"
    message: |
      Code or documentation changes must be reflected in the relevant index/matrix docs.
      Refer to QA_GOVERNANCE.md for update policies.


--- FILE: make_manifest.py ---

#!/usr/bin/env python3
import os

OUTPUT = "REPO_MANIFEST.md"
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "node_modules", "dist", "build"}
TEXT_EXTENSIONS = {".py", ".md", ".yml", ".yaml", ".toml", ".json", ".txt", ".ini", ".cfg"}

def is_text_file(filename):
    return any(filename.endswith(ext) for ext in TEXT_EXTENSIONS)

with open(OUTPUT, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if is_text_file(f):
                path = os.path.join(root, f).lstrip("./")
                out.write(f"\n\n--- FILE: {path} ---\n\n")
                try:
                    with open(os.path.join(root, f), encoding="utf-8") as fh:
                        out.write(fh.read())
                except Exception as e:
                    out.write(f"[Error reading {path}: {e}]")

print(f"Manifest written to {OUTPUT}")


--- FILE: validate_code_index.py ---

import os
from pathlib import Path
import sys

# --- Configuration ---
PROJECT_ROOT = Path(__file__).parent.parent
CODE_INDEX_PATH = PROJECT_ROOT / "api/docs/CODE_FILE_INDEX.md"
DIRS_TO_SCAN = [
    PROJECT_ROOT / "api/src/zotify_api",
    PROJECT_ROOT / "scripts",
    PROJECT_ROOT / "api/tests",
    PROJECT_ROOT / "Gonk",
    PROJECT_ROOT / "snitch",
]
FILE_EXTENSIONS = {".py", ".go", ".js"}


def get_indexed_files(index_path: Path) -> set[str]:
    """Parses the code index markdown file and returns a set of file paths."""
    if not index_path.exists():
        print(f"Error: Code index file not found at {index_path}", file=sys.stderr)
        sys.exit(1)

    indexed_files = set()
    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("|"):
                continue
            if "---" in line or "Path" in line:
                continue

            parts = [p.strip().strip("`") for p in line.split("|")]
            if len(parts) > 1 and parts[1]:
                # Convert to relative path from project root
                indexed_files.add(parts[1])
    return indexed_files


def get_actual_files(directories: list[Path], extensions: set[str]) -> set[str]:
    """Walks the given directories and returns a set of actual file paths."""
    actual_files = set()
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if Path(file).suffix in extensions:
                    full_path = Path(root) / file
                    # Make path relative to project root for comparison
                    relative_path = str(full_path.relative_to(PROJECT_ROOT))
                    actual_files.add(relative_path)
    return actual_files


def main() -> int:
    """Main function to compare indexed files vs. actual files."""
    print("--- Running Code File Index Validator ---")
    indexed_files = get_indexed_files(CODE_INDEX_PATH)
    actual_files = get_actual_files(DIRS_TO_SCAN, FILE_EXTENSIONS)

    # Ignore __init__.py files as they are for packaging, not standalone code logic
    actual_files = {f for f in actual_files if not f.endswith("__init__.py")}
    indexed_files = {f for f in indexed_files if not f.endswith("__init__.py")}

    unindexed_files = actual_files - indexed_files
    stale_index_entries = indexed_files - actual_files

    if not unindexed_files and not stale_index_entries:
        print("✅ Success: Code file index is up-to-date.")
        return 0

    if unindexed_files:
        print("\n❌ Error: The following code files are present in the repository but not in the index:", file=sys.stderr)
        for file in sorted(list(unindexed_files)):
            print(f"- {file}", file=sys.stderr)

    if stale_index_entries:
        print("\n❌ Error: The following files are in the index but do not exist in the repository:", file=sys.stderr)
        for file in sorted(list(stale_index_entries)):
            print(f"- {file}", file=sys.stderr)

    print("\nPlease update api/docs/CODE_FILE_INDEX.md to match the repository.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())


--- FILE: functional_test.py ---

import pytest
import httpx

BASE_URL = "http://localhost:8000"
TEST_TOKEN = "test_key"


@pytest.fixture
def client():
    # allow_redirects=True will handle the 307 from FastAPI
    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        yield client


def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    json_resp = r.json()
    assert json_resp.get("status") == "ok"


def test_get_playlists(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/api/playlists/", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    assert "data" in json_resp
    assert isinstance(json_resp["data"], list)


def test_error_handling(client):
    r = client.get("/api/nonexistent/endpoint")
    assert r.status_code == 404
    json_resp = r.json()
    assert "detail" in json_resp


def test_get_user_profile(client):
    headers = {"Authorization": f"Bearer {TEST_TOKEN}"}
    r = client.get("/api/user/profile", headers=headers)
    assert r.status_code == 200
    json_resp = r.json()
    assert "data" in json_resp
    # The user service returns 'email', not 'id'.
    assert "email" in json_resp["data"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])


--- FILE: audit_endpoints.py ---

import inspect
from fastapi import FastAPI
from fastapi.routing import APIRoute
import sys
from pathlib import Path

# Add the project source to the Python path
project_root = Path(__file__).parent
api_src_path = project_root / "api" / "src"
sys.path.insert(0, str(api_src_path))


def analyze_route_status(app: FastAPI):
    route_status = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path = route.path
        methods = route.methods
        endpoint = route.endpoint
        doc = inspect.getdoc(endpoint) or ""

        try:
            source = inspect.getsource(endpoint)
        except TypeError:
            # This can happen for functools.partial objects, etc.
            # We'll assume these are not stubs for this analysis.
            source = ""

        # Heuristic: look for '501' or 'NotImplementedError' in source code to flag stubs
        if "501" in source or "NotImplementedError" in source:
            status = "Stub"
        # Another heuristic: check for a placeholder response
        elif 'return {"status":' in source and "stub" in source:
            status = "Stub"
        else:
            status = "Functional"

        route_status.append(
            {
                "path": path,
                "methods": sorted(list(methods)),
                "status": status,
                "doc": doc.strip(),
            }
        )

    return route_status


if __name__ == "__main__":
    try:
        from zotify_api.main import app  # Adjust import path as necessary
    except ImportError as e:
        print(f"Failed to import FastAPI app: {e}")
        print(f"Current sys.path: {sys.path}")
        sys.exit(1)

    status_report = analyze_route_status(app)

    # This is not for the final report, just for me to parse
    for route in status_report:
        print(
            f"{'|'.join(route['methods'])}|{route['path']}|{route['status']}|{route['doc']}"
        )


--- FILE: api/src/zotify_api/temp_violation.py ---

# Temporary violation file
