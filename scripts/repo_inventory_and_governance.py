#!/usr/bin/env python3
"""
repo_inventory_and_governance.py - inventory + governance index generator (patched)

Fixes applied:
- Ensure PROJECT_ROOT is resolved correctly to avoid walking the entire filesystem.
- Robustly ignore directories by checking path parts.
- Exclude chat logs explicitly from registration logic.
- Replaced extract_metadata() with new summarizer.
- Minimal behavior changes — preserves existing index-generation and audit output logic.
"""

import os
import re
import sys
import yaml
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple

# Ensure scripts directory is in the Python path
sys.path.append(str(Path(__file__).resolve().parent))

from summarize_docs import summarize_doc
from summarize_code import summarize_code_file
from summarize_tags import generate_tags_from_text

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
print("PROJECT_ROOT:", PROJECT_ROOT)

FILETYPE_MAP = {
    ".md": "doc", ".py": "code", ".sh": "code", ".html": "code", ".js": "code",
    ".ts": "code", ".css": "code", ".yml": "code", ".go": "code",
}

IGNORED_DIRS = {
    "project/logs/chat", ".git", ".idea", ".venv", "node_modules",
    "build", "dist", "target", "__pycache__", "site", "archive",
    "templates", ".pytest_cache", "cache", ".cache", "storage", "chat"
}

IGNORED_FILES = {
    "mkdocs.yml", "openapi.json", "bandit.yml", "changed_files.txt",
    "verification_report.md", "LICENSE"
}

INDEX_MAP = [
    {"match": lambda p, f: f == "doc" and p.startswith("api/docs/"),
     "indexes": ["api/docs/MASTER_INDEX.md", "api/docs/DOCS_QUALITY_INDEX.md"]},

    {"match": lambda p, f: f == "doc" and (
        (p.startswith("project/archive/docs/") or
         p.startswith("project/process/") or
         p.startswith("project/proposals/") or
         p.startswith("project/reports/") or
         (p.startswith("project/") and Path(p).parent.name == "project"))
        and not p.startswith("project/logs/chat/")
    ), "indexes": ["project/PROJECT_REGISTRY.md"]},

    {"match": lambda p, f: f == "doc" and p.startswith("Gonk/GonkCLI/docs/"),
     "indexes": ["Gonk/GonkCLI/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "doc" and p.startswith("Gonk/GonkUI/docs/"),
     "indexes": ["Gonk/GonkUI/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "doc" and p.startswith("snitch/docs/"),
     "indexes": ["snitch/DOCS_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("api/"),
     "indexes": ["api/docs/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("Gonk/"),
     "indexes": ["Gonk/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("snitch/"),
     "indexes": ["snitch/CODE_FILE_INDEX.md"]},
    {"match": lambda p, f: f == "code" and p.startswith("scripts/"),
     "indexes": ["scripts/CODE_FILE_INDEX.md"]},
]

# --- Helper functions ---
def get_file_type(filepath: str) -> str:
    name = os.path.basename(filepath)
    if name.startswith(".") or name in IGNORED_FILES:
        return "exempt"
    return FILETYPE_MAP.get(os.path.splitext(filepath)[1], "exempt")

def extract_metadata(filepath: Path) -> dict:
    """
    Extracts metadata for a given file by calling the appropriate summarizer function.
    """
    file_type = get_file_type(str(filepath))
    summary = ""

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")

        if file_type == "doc":
            summary = summarize_doc(content)
        elif file_type == "code":
            summary = summarize_code_file(content)
        else:
            return {"description": "No description available.", "tags": []}

    except Exception as e:
        summary = f"[Error reading or summarizing file: {e}]"

    tags = generate_tags_from_text(summary)

    return {"description": summary, "tags": tags}


def find_all_files() -> List[str]:
    files: List[str] = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        root_path = Path(root)
        rel_parts = root_path.relative_to(PROJECT_ROOT).parts
        if any(p in IGNORED_DIRS for p in rel_parts):
            dirs[:] = []  # prevent descending
            continue
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in filenames:
            if f in IGNORED_FILES:
                continue
            files.append(str(Path(root_path, f).relative_to(PROJECT_ROOT)).replace(os.sep, "/"))
    return files


def parse_markdown_index(index_path: Path) -> Set[str]:
    if not index_path.exists():
        return set()
    content = index_path.read_text(encoding="utf-8")
    if "CODE_FILE_INDEX.md" in str(index_path) or "DOCS_QUALITY_INDEX.md" in str(index_path):
        return set(re.findall(r"^\s*\|\s*`([^`]+)`", content, re.MULTILINE))
    if "PROJECT_REGISTRY.md" in str(index_path):
        links = re.findall(r"\[`([^`]+)`\]\(([^)]+)\)", content)
        resolved = set()
        for _, link in links:
            try:
                resolved.add(str(Path(os.path.normpath(os.path.join(index_path.parent, link))).relative_to(PROJECT_ROOT)))
            except Exception:
                continue
        return resolved
    links = re.findall(r"\[[^\]]+\]\((?!https?://)([^)]+)\)", content)
    resolved = set()
    for link in links:
        try:
            resolved.add(str(Path(os.path.normpath(os.path.join(index_path.parent, link))).relative_to(PROJECT_ROOT)))
        except Exception:
            continue
    return resolved


def check_registration(file_path: str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:
    found, missing = [], []
    for idx in required_indexes:
        if file_path in all_indexes_content.get(idx, set()):
            found.append(idx)
        else:
            missing.append(idx)
    return sorted(found), sorted(missing)


def create_and_populate_index(index_path_str: str, files_to_add: List[str], file_type: str):
    index_path = PROJECT_ROOT / index_path_str
    index_path.parent.mkdir(parents=True, exist_ok=True)
    existing_files = parse_markdown_index(index_path) if index_path.exists() else set()
    new_files_to_add = sorted([f for f in files_to_add if f not in existing_files])
    if not new_files_to_add:
        return
    lines_to_append = []
    if "CODE_FILE_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | | | Active | | |" for f in new_files_to_add]
    elif "DOCS_QUALITY_INDEX" in index_path_str:
        lines_to_append = [f"| `{f}` | X | X | | | |" for f in new_files_to_add]
    elif "PROJECT_REGISTRY.md" in index_path_str:
        for f in new_files_to_add:
            rel_link = os.path.relpath(PROJECT_ROOT / f, index_path.parent)
            doc_name = Path(f).stem.replace('_', ' ').replace('-', ' ').title()
            lines_to_append.append(f"| **{doc_name}** | [`{Path(f).name}`]({rel_link}) | |")
    if not index_path.exists() and ("CODE_FILE_INDEX" in index_path_str or "DOCS_QUALITY_INDEX" in index_path_str):
        if "CODE_FILE_INDEX" in index_path_str:
            header = ("# Code File Index\n\nThis file is auto-generated.\n\n"
                      "| Path | Type | Description | Status | Linked Docs | Notes |\n"
                      "|------|------|-------------|--------|-------------|-------|\n")
        else:
            header = ("# Docs Quality Index\n\nThis file is auto-generated.\n\n"
                      "| File Path | Score | Reviewer | Date | Notes |\n"
                      "|-----------|-------|----------|------|-------|\n")
        index_path.write_text(header + "\n".join(sorted(lines_to_append)) + "\n", encoding="utf-8")
        return
    with open(index_path, "a", encoding="utf-8") as fh:
        try:
            if index_path.exists() and index_path.read_text(encoding="utf-8")[-1] != "\n":
                fh.write("\n")
        except Exception:
            pass
        fh.write("\n".join(sorted(lines_to_append)) + "\n")


def generate_audit_report(trace_index: List[Dict[str, Any]]) -> int:
    print("\n=== GAP Analysis Report ===\n")
    missing_by_index: Dict[str, List[str]] = {}
    registered_count = 0
    missing_count = 0
    exempted_count = 0
    for item in trace_index:
        if item.get("registered") == "exempted":
            exempted_count += 1
        elif item.get("registered") is True:
            registered_count += 1
        else:
            missing_count += 1
            for idx in item.get("missing_from", []):
                missing_by_index.setdefault(idx, []).append(item["path"])
    if missing_count > 0:
        print("\n--- Missing Registrations ---")
        for idx, files in sorted(missing_by_index.items()):
            print(f"\nMissing from {idx}:")
            for f in sorted(files):
                print(f"  - {f}")
    print(f"\nTotal files: {len(trace_index)}\nRegistered: {registered_count}\nMissing: {missing_count}\nExempted: {exempted_count}\n")
    return 1 if missing_count > 0 else 0


def validate_trace_index_schema(trace_index_path: Path) -> bool:
    return True


def validate_metadata(trace_index: List[Dict[str, Any]]) -> None:
    print("\n--- Validating Metadata ---")
    warnings = 0
    for item in trace_index:
        path = item.get("path")
        meta = item.get("meta")
        if not meta:
            print(f"⚠️  Warning: Missing 'meta' field for artifact: {path}")
            warnings += 1
            continue
        description = meta.get("description", "").strip()
        if not description or description == "No description available.":
            print(f"⚠️  Warning: Missing 'meta.description' for artifact: {path}")
            warnings += 1
        tags = meta.get("tags", [])
        if item.get("type") in ["code", "doc"] and not tags:
            print(f"⚠️  Warning: Missing 'meta.tags' for artifact: {path}")
            warnings += 1
    if warnings == 0:
        print("✅ Metadata validation passed with no warnings.")
    else:
        print(f"\nFound {warnings} metadata warning(s).")


# --- Main ---
def main():
    parser = argparse.ArgumentParser(description="Repository inventory and governance script.")
    parser.add_argument("--full", action="store_true", help="Run a full scan of all files.")
    parser.add_argument("--full-scan", action="store_true", help="Force a full scan of all files, ignoring other modes.")
    parser.add_argument("--test-files", nargs='*', help="Run in test mode with a specific list of files.")
    parser.add_argument("--update-project-registry", action="store_true", help="Update the project registry JSON and Markdown files.")
    parser.add_argument("--extras-file", type=Path, default=PROJECT_ROOT / "scripts/project_registry_extras.yml", help="Path to the project registry extras file.")
    parser.add_argument("--debug", action="store_true", help="Enable debug printing for scripts that support it.")
    parser.add_argument("--progress", action="store_true", help="Show a progress bar during full scans.")
    args = parser.parse_args()

    if args.update_project_registry:
        script_path = PROJECT_ROOT / "scripts" / "build_project_registry.py"
        cmd = [sys.executable, str(script_path), "--extras-file", str(args.extras_file)]
        if args.debug:
            cmd.append("--debug")
        try:
            subprocess.run(cmd, check=True)
            print("✅ Project registry updated successfully.")
            return 0
        except subprocess.CalledProcessError as e:
            print("❌ ERROR: Project registry update failed.", file=sys.stderr)
            print(e, file=sys.stderr)
            return e.returncode

    test_mode = args.test_files is not None
    all_files = args.test_files if test_mode else find_all_files()
    trace_index: List[Dict[str, Any]] = []
    all_index_paths = {idx for rule in INDEX_MAP for idx in rule["indexes"]}
    all_indexes_content = {str(p): parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths}
    files_to_create: Dict[str, List[str]] = {}

    from tqdm import tqdm

    iterator = tqdm(sorted(all_files), desc="Processing files", unit="file") if args.progress and not test_mode else sorted(all_files)

    for f in iterator:
        ftype = get_file_type(f)
        full_path = PROJECT_ROOT / f
        meta = extract_metadata(full_path) if full_path.exists() else {"description": "File not found.", "tags": []}
        entry: Dict[str, Any] = {"path": f, "type": ftype, "meta": meta}
        required: List[str] = []
        if ftype != "exempt":
            for r in INDEX_MAP:
                try:
                    if r["match"](f, ftype):
                        required.extend(r["indexes"])
                except Exception:
                    continue
        required = sorted(list(set(required)))
        if not required:
            entry["registered"] = "exempted"
            entry["index"] = "-"
        else:
            found, missing = check_registration(f, required, all_indexes_content)
            if not missing:
                entry["registered"] = True
                entry["index"] = found[0]
            else:
                entry["registered"] = False
                entry["index"] = "-"
                entry["missing_from"] = missing
                for idx_file in missing:
                    files_to_create.setdefault(idx_file, []).append(f)
        trace_index.append(entry)

    if not test_mode:
        for idx_path, files in files_to_create.items():
            if files:
                file_type_for_index = get_file_type(files[0])
                create_and_populate_index(idx_path, files, file_type_for_index)

    doc_tag_inventory_path = PROJECT_ROOT / "project/reports/DOCUMENT_TAG_INVENTORY.yml"
    if doc_tag_inventory_path.exists():
        try:
            with doc_tag_inventory_path.open("r", encoding="utf-8") as f:
                tag_inventory = yaml.safe_load(f) or []
            file_to_id = {item.get('path'): item.get('id') for item in tag_inventory if isinstance(item, dict) and 'path' in item and 'id' in item}
            for entry in trace_index:
                entry['id'] = file_to_id.get(entry['path'], 'MISSING')
        except Exception as e:
            print(f"⚠️ Warning: could not load DOCUMENT_TAG_INVENTORY.yml: {e}", file=sys.stderr)

    output = {"artifacts": trace_index}
    trace_index_path = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
    trace_index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(trace_index_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(output, f, default_flow_style=False, sort_keys=False)

    if not validate_trace_index_schema(trace_index_path):
        return 1

    validate_metadata(trace_index)

    if test_mode:
        return 0

    exit_code = generate_audit_report(trace_index)

    linter_script = PROJECT_ROOT / "scripts/lint_governance_links.py"
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("linter_script:", linter_script, "exists?", linter_script.exists())
    if linter_script.exists():
        try:
            subprocess.run([sys.executable, str(linter_script)], check=True)
        except subprocess.CalledProcessError as e:
            print("⚠️ lint_governance_links.py failed:", file=sys.stderr)
            if exit_code == 0:
                exit_code = e.returncode
    else:
        print("⚠️ lint_governance_links.py not found; skipping governance link check.", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
