#!/usr/bin/env python3
"""
Full linter.py - Unified Linter and Logger for the repository.

Features:
- Logging mode (--log): write ACTIVITY.md, SESSION_LOG.md, CURRENT_STATE.md
- Change detection (robust): staged, unstaged, untracked, renames handled
- Doc-matrix enforcement via scripts/doc-lint-rules.yml
- Code quality index checks (api/docs/CODE_QUALITY_INDEX.md)
- Conditional mkdocs build (if api/docs/ changed)
- Governance enforcement via scripts/repo_governance.py (or lint_governance_links.py)
- Manifest generation (scripts/make_manifest.py) runs only if staged files are present OR in test mode
- Testability via --test-files and --from-file
"""
from __future__ import annotations
import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Set, Tuple, Dict

# Optional imports
try:
    import yaml
except Exception:
    yaml = None  # doc-lint rules will be skipped if PyYAML is not installed

# === Configuration ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
REPORTS_DIR = PROJECT_ROOT / "project" / "reports"
LOG_ACTIVITY = PROJECT_ROOT / "project" / "logs" / "ACTIVITY.md"
LOG_SESSION = PROJECT_ROOT / "project" / "logs" / "SESSION_LOG.md"
LOG_CURRENT = PROJECT_ROOT / "project" / "logs" / "CURRENT_STATE.md"
DOC_LINT_RULES = SCRIPTS_DIR / "doc-lint-rules.yml"
GOV_SCRIPT = SCRIPTS_DIR / "repo_governance.py"
ALT_GOV_SCRIPT = SCRIPTS_DIR / "lint_governance_links.py"
MANIFEST_SCRIPT = SCRIPTS_DIR / "make_manifest.py"

# === Utilities ===


def run_command(cmd: List[str], cwd: Path = PROJECT_ROOT, raise_on_error: bool = False) -> int:
    """Run command, print stdout/stderr, return exit code."""
    try:
        result = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    except FileNotFoundError:
        print(f"[WARN] Command not found: {cmd[0]}", file=sys.stderr)
        return 127
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if raise_on_error and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stdout, stderr=result.stderr)
    return result.returncode


def run_command_capture(cmd: List[str], cwd: Path = PROJECT_ROOT) -> str:
    """Run command and return stdout (silently returns '' on failure)."""
    try:
        res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)
        return res.stdout or ""
    except FileNotFoundError:
        return ""


# === Logging helpers ===


def get_formatted_date() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def get_next_act_number(file_path: Path = LOG_ACTIVITY) -> int:
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return 1
    act_numbers = re.findall(r"## ACT-(\d+):", text)
    if not act_numbers:
        return 1
    return max(int(n) for n in act_numbers) + 1


def format_activity_log(act_number: int, summary: str, objective: str, findings: str, files: List[str]) -> str:
    related_docs_section = ""
    if files:
        file_list = "\n".join([f"- `{f}`" for f in files])
        related_docs_section = f"\n\n### Related Documents\n{file_list}\n"
    return (
        f"---\n"
        f"## ACT-{act_number:03d}: {summary}\n\n"
        f"**Date:** {get_formatted_date()}\n"
        f"**Status:** ✅ Done\n"
        f"**Assignee:** Jules\n\n"
        f"### Objective\n{objective or summary}\n\n"
        f"### Outcome\n{findings}\n"
        f"{related_docs_section}"
    )


def format_session_log(summary: str, findings: str) -> str:
    return (
        f"---\n"
        f"## Session Report: {get_formatted_date()}\n\n"
        f"**Summary:** {summary}\n\n"
        f"**Findings:**\n{findings}\n"
    )


def format_current_state(summary: str, objective: str, next_steps: str) -> str:
    objective_section = f"## Objective\n{objective}\n\n" if objective else ""
    return (
        f"# Project State as of {get_formatted_date()}\n\n"
        f"**Status:** Live Document\n\n"
        f"{objective_section}"
        f"## 1. Session Summary & Accomplishments\n"
        f"{summary}\n\n"
        f"## 2. Known Issues & Blockers\n- None\n\n"
        f"## 3. Pending Work: Next Immediate Steps\n"
        f"{next_steps}\n"
    )


def prepend_to_file(file_path: Path, content: str) -> None:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
        else:
            existing = ""
        file_path.write_text(content.strip() + "\n\n" + existing, encoding="utf-8")
        print(f"[LOG] Updated {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not write to {file_path}: {e}", file=sys.stderr)


def write_to_file(file_path: Path, content: str) -> None:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"[LOG] Wrote {file_path}")
    except Exception as e:
        print(f"[ERROR] Could not write to {file_path}: {e}", file=sys.stderr)


def do_logging(summary: str, objective: str, findings: str, next_steps: str, files: List[str]) -> int:
    print("--- Running Logging ---")
    act_number = get_next_act_number()
    activity_entry = format_activity_log(act_number, summary, objective, findings, files)
    prepend_to_file(LOG_ACTIVITY, activity_entry)

    session_entry = format_session_log(summary, findings)
    prepend_to_file(LOG_SESSION, session_entry)

    current_state_content = format_current_state(summary, objective, next_steps)
    write_to_file(LOG_CURRENT, current_state_content)
    print("--- Logging Complete ---")
    return 0


# === Change detection (robust local) ===


def parse_name_status_output(output: str) -> List[Tuple[str, str]]:
    """
    Parse git --name-status output (lines like 'M\tpath' or 'R100\told\tnew')
    Returns list of tuples (status, path) - renames expand to both old and new.
    """
    items: List[Tuple[str, str]] = []
    for ln in output.strip().splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            old, new = parts[1], parts[2]
            items.append((status, old))
            items.append((status, new))
        elif len(parts) >= 2:
            items.append((status, parts[1]))
    return items


def get_local_changed_files(precommit: bool = False) -> List[Tuple[str, str]]:
    """
    Attempt multiple methods to detect local changes:
      - staged: git diff --cached --name-status
      - unstaged: git diff --name-status
      - untracked: git ls-files --others --exclude-standard
    Returns list of tuples (status, path).
    If PRE_COMMIT environment variable set or precommit==True, only staged are considered.
    """
    changed: List[Tuple[str, str]] = []

    # 1) Staged changes
    staged_out = run_command_capture(["git", "diff", "--cached", "--name-status"])
    changed.extend(parse_name_status_output(staged_out))

    if precommit or os.environ.get("PRE_COMMIT"):
        return changed

    # 2) Unstaged changes
    unstaged_out = run_command_capture(["git", "diff", "--name-status"])
    changed.extend(parse_name_status_output(unstaged_out))

    # 3) Untracked files (status '??')
    untracked_out = run_command_capture(["git", "ls-files", "--others", "--exclude-standard"])
    for line in untracked_out.splitlines():
        line = line.strip()
        if line:
            changed.append(("??", line))

    # Deduplicate preserving order
    seen = set()
    deduped: List[Tuple[str, str]] = []
    for s, path in changed:
        if path not in seen:
            seen.add(path)
            deduped.append((s, path))
    return deduped


def get_changed_files_from_git_status() -> List[Tuple[str, str]]:
    """
    Fallback using 'git status --porcelain' if other methods fail.
    Porcelain lines: XY PATH or with -> for renames
    """
    out = run_command_capture(["git", "status", "--porcelain"])
    items: List[Tuple[str, str]] = []
    for ln in out.splitlines():
        ln = ln.rstrip("\n")
        if not ln:
            continue
        # handle rename with -> by splitting on '->'
        # but porcelain format typically: 'R  old -> new'
        if "->" in ln:
            # pick last part as new path
            new = ln.split("->")[-1].strip()
            items.append(("R", new))
        else:
            # first 2 chars are status, rest is path
            if len(ln) > 3:
                path = ln[3:].strip()
            else:
                path = ln.strip()
            status = ln[:2].strip()
            items.append((status or "M", path))
    # dedupe
    seen = set()
    deduped = []
    for s, p in items:
        if p not in seen:
            seen.add(p)
            deduped.append((s, p))
    return deduped


# === Doc matrix rules ===


def check_doc_matrix_rules(changed_files: Set[str]) -> List[str]:
    """
    Enforce doc-lint rules: rules format (YAML):
    rules:
      - name: "Rule name"
        source_paths: ["api/src/..."]
        required_docs: ["project/XYZ.md"]
        message: "custom message"
    """
    errors: List[str] = []
    if yaml is None:
        print("[WARN] PyYAML not installed; skipping doc-lint rules.")
        return errors
    if not DOC_LINT_RULES.exists():
        print("[WARN] doc-lint-rules.yml not found; skipping doc matrix checks.")
        return errors

    try:
        rules_doc = yaml.safe_load(DOC_LINT_RULES.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] Could not parse {DOC_LINT_RULES}: {e}", file=sys.stderr)
        return ["doc-lint-rules parse error"]

    rules = rules_doc.get("rules", []) if isinstance(rules_doc, dict) else []
    for rule in rules:
        source_paths = rule.get("source_paths", [])
        required_docs = rule.get("required_docs", [])
        is_unconditional = not source_paths

        source_changed = False
        if is_unconditional:
            source_changed = True
        else:
            for sf in changed_files:
                if any(sf.startswith(sp) for sp in source_paths):
                    source_changed = True
                    break

        if source_changed:
            if not required_docs:
                continue
            # For "Enforce Mandatory Logging" type rule (special-case), require all docs
            if rule.get("name") == "Enforce Mandatory Logging":
                ok = all(d in changed_files for d in required_docs)
            else:
                ok = any(d in changed_files for d in required_docs)
            if not ok:
                message = rule.get(
                    "message",
                    f"Changes in {source_paths or 'repo'} require updates to one of {required_docs}",
                )
                errors.append(message)
    return errors


# === Code quality index checks ===


def check_quality_index_ratings() -> List[str]:
    """Validate CODE_QUALITY_INDEX.md scoring cells for valid single-letter grades."""
    errors: List[str] = []
    quality_index_file = PROJECT_ROOT / "api" / "docs" / "CODE_QUALITY_INDEX.md"
    if not quality_index_file.exists():
        return []
    valid_scores = {"A", "B", "C", "D", "F", "X", ""}
    lines = quality_index_file.read_text(encoding="utf-8").splitlines()
    in_data_table = False
    for i, line in enumerate(lines):
        if "| File Path |" in line and "| Documentation Score |" in line:
            in_data_table = True
            continue
        if not in_data_table:
            continue
        if "|" not in line or "---" in line:
            continue
        cols = [c.strip() for c in line.split("|")]
        # expected: | `path` | DocScore | CodeScore | ...
        if len(cols) < 4:
            continue
        doc_score = cols[2]
        code_score = cols[3]
        if doc_score and doc_score not in valid_scores:
            errors.append(f"Invalid Doc Score on line {i+1}: '{doc_score}'")
        if code_score and code_score not in valid_scores:
            errors.append(f"Invalid Code Score on line {i+1}: '{code_score}'")
    return errors


# === MkDocs build check ===


def run_mkdocs_check() -> bool:
    docs_dir = PROJECT_ROOT / "api" / "docs"
    if not docs_dir.exists():
        print("[INFO] No api/docs/ found; skipping mkdocs build.")
        return True
    print("[LINT] Running mkdocs build...")
    rc = run_command(["mkdocs", "build"], cwd=PROJECT_ROOT)
    return rc == 0


# === Governance & Manifest ===


def run_lint_governance_links() -> int:
    print("\n--- Running Governance Links Linter ---")
    script_path = PROJECT_ROOT / "scripts" / "lint_governance_links.py"
    if not script_path.exists():
        print("ERROR: lint_governance_links.py not found.", file=sys.stderr)
        return 1
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        print("Governance Links Linter Failed!", file=sys.stderr)
    else:
        print("Governance Links Linter Passed!")
    return result.returncode


def run_manifest_generation(test_files: list[str] | None = None) -> int:
    """
    Run make_manifest.py, passing test files if provided.
    """
    if not MANIFEST_SCRIPT.exists():
        print("[WARN] make_manifest.py not found; cannot regenerate REPO_MANIFEST.md")
        return 1

    cmd = [sys.executable, str(MANIFEST_SCRIPT)]
    if test_files:
        print(f"[LINT] Propagating --test-files to make_manifest.py ({len(test_files)} files).")
        cmd.extend(["--test-files"] + test_files)
    else:
        print("[LINT] Running make_manifest.py to regenerate REPO_MANIFEST.md")

    return run_command(cmd, cwd=PROJECT_ROOT)


# === Argument parser and main ===


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Linter and Logger for repository")
    parser.add_argument("--log", action="store_true", help="Run in logging mode (writes ACTIVITY, SESSION, CURRENT_STATE).")
    parser.add_argument("--summary", help="[log] One-line summary (required with --log)")
    parser.add_argument("--objective", help="[log] High-level objective")
    parser.add_argument("--findings", help="[log] Findings (multi-line; use '\\n' for newlines)")
    parser.add_argument("--next-steps", help="[log] Next immediate steps (required with --log)")
    parser.add_argument("--files", nargs="*", help="[log] Files related to activity")
    parser.add_argument("--test-files", nargs="*", help="[linter] Provide list of changed files for testing (bypass git).")
    parser.add_argument("--from-file", help="[linter] Read changed files from a file (one per line).")
    parser.add_argument("--skip-governance", action="store_true", help="Skip governance enforcement.")
    parser.add_argument("--skip-manifest", action="store_true", help="Skip manifest generation even if staged files exist.")
    args = parser.parse_args()

    # Logging mode
    if args.log:
        if not all([args.summary, args.findings, args.next_steps]):
            print("ERROR: --log requires --summary, --findings, and --next-steps.", file=sys.stderr)
            return 1
        files = args.files or []
        return do_logging(args.summary, args.objective or "", args.findings, args.next_steps, files)

    print("=" * 40)
    print("Running Unified Linter")
    print("=" * 40)

    # 1) Governance Links Linter (unless skipped)
    if not args.skip_governance:
        gov_links_return = run_lint_governance_links()
        if gov_links_return != 0:
            return gov_links_return
    else:
        print("[INFO] Skipping governance links linter (--skip-governance).")

    # 2) Find changed files
    changed_with_status: List[Tuple[str, str]] = []
    if args.from_file:
        try:
            lines = Path(args.from_file).read_text(encoding="utf-8").splitlines()
            changed_with_status = [("M", ln.strip()) for ln in lines if ln.strip()]
            print(f"[INFO] Loaded {len(changed_with_status)} files from {args.from_file}")
        except Exception as e:
            print(f"[ERROR] Could not read --from-file: {e}", file=sys.stderr)
            return 1
    elif args.test_files:
        changed_with_status = [("M", f) for f in args.test_files]
        print(f"[INFO] Test mode: injecting {len(changed_with_status)} test files.")
    else:
        # normal git detection
        changed_with_status = get_local_changed_files()
        if not changed_with_status:
            # try fallback
            changed_with_status = get_changed_files_from_git_status()

    if not changed_with_status:
        print("[INFO] No changed files detected. Nothing to lint for changes.")
        # even if no changed files, still may need to exit 0 (no errors)
        return 0

    # Convert to set of file paths for checks
    changed_files_set: Set[str] = {p for (_s, p) in changed_with_status}
    print(f"[INFO] Detected {len(changed_files_set)} changed files.")
    for s, p in changed_with_status:
        print(f"- {s}\t{p}")

    # 3) Doc-matrix rules – always run
    print("\n--- Doc-matrix checks ---")
    doc_errors = check_doc_matrix_rules(changed_files_set)
    if doc_errors:
        print("[ERROR] Documentation matrix checks failed:", file=sys.stderr)
        for msg in doc_errors:
            print(f"- {msg}", file=sys.stderr)
        return 1
    print("[OK] Documentation matrix checks passed.")

    # 4) Quality index checks (conditional)
    print("\n--- Code quality index checks ---")
    quality_errors = check_quality_index_ratings()
    if quality_errors:
        print("[ERROR] Code quality index issues:", file=sys.stderr)
        for e in quality_errors:
            print(f"- {e}", file=sys.stderr)
        return 1
    print("[OK] Code quality index checks passed.")

    # 5) MkDocs build (if api docs changed)
    print("\n--- MkDocs check ---")
    if any(f.startswith("api/docs/") or f.startswith("api/") and f.endswith(".md") for f in changed_files_set):
        if not run_mkdocs_check():
            print("[ERROR] MkDocs build failed.", file=sys.stderr)
            return 1
        print("[OK] MkDocs build passed.")
    else:
        print("[INFO] No API docs changes detected; skipped mkdocs.")

    # 6) Manifest Generation
    if args.skip_manifest:
        print("[INFO] Skipping manifest generation (--skip-manifest).")
    else:
        print("\n--- Running Repository Manifest Generation ---")
        # Propagate --test-files if they were provided to the linter
        manifest_return_code = run_manifest_generation(test_files=args.test_files)
        if manifest_return_code != 0:
            print("❌ Manifest Generation Failed!", file=sys.stderr)
            return manifest_return_code
        # No success message here, as the manifest script prints its own status.

    print("\n=== Linter completed successfully ===")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        sys.exit(2)