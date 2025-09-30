#!/usr/bin/env python3
"""
Self-checking repository manifest generator.
Regenerates manifest only if there are staged changes or if --test-files is provided.
"""

import subprocess
import sys
from pathlib import Path
import os
import yaml
import argparse
import zipfile

PROJECT_ROOT = Path(__file__).parent.parent

# --- Functions from the original script ---

# Configuration
IGNORED_DIRS = {'.git', '.github', '.venv', '__pycache__', 'archive', 'api_dumps',
                'zotify_api.egg-info', 'src', 'templates', 'docs', 'alembic'}
IGNORED_FILES = {'.DS_Store', '.gitignore', 'REPO_MANIFEST.md', 'openapi.json',
                 'LICENSE', 'CONTRIBUTING.md', 'alembic.ini'}
# Files that should be included even if in ignored dirs
INCLUDED_FILES = {'api/docs/MASTER_INDEX.md'}

def get_file_type(filename):
    if filename.endswith('.py') or filename.endswith('.sh'):
        return 'script'
    elif filename.endswith('.md') or filename.endswith('.rst') or filename.endswith('.txt'):
        return 'doc'
    elif filename.endswith('.yml') or filename.endswith('.yaml') or filename.endswith('.json'):
        return 'config'
    else:
        return 'other'

def is_ignored_file(rel_path):
    normalized = os.path.normpath(rel_path).replace(os.sep, '/')
    # Always include files explicitly listed
    if normalized in INCLUDED_FILES:
        return False
    # Skip ignored filenames
    if os.path.basename(rel_path) in IGNORED_FILES:
        return True
    # Skip if any parent dir is in IGNORED_DIRS
    parts = normalized.split('/')
    for p in parts[:-1]:
        if p in IGNORED_DIRS:
            return True
    return False

def scan_repo(base_dir='.'):
    """Scans the repository and returns a list of files to be included in the manifest."""
    file_paths = []
    for root, dirs, files in os.walk(base_dir):
        # Skip ignored dirs unless they lead to an included file
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS or
                   any(inc.startswith(os.path.relpath(os.path.join(root, d), base_dir).replace(os.sep, '/') + '/')
                       for inc in INCLUDED_FILES)]
        for f in files:
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, start=base_dir)
            if is_ignored_file(rel_path):
                continue
            file_paths.append(rel_path)
    return file_paths

def create_zip_archive(output_path, files_to_zip):
    """Creates a ZIP archive from a list of repository files."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_zip:
                full_path = PROJECT_ROOT / file_path
                try:
                    # The arcname is the path inside the zip file, relative to the repo root.
                    zipf.write(full_path, arcname=file_path)
                except FileNotFoundError:
                    # This case should ideally not happen if scan_repo is correct, but good to have.
                    print(f"Warning: File not found during zipping and will be skipped: {file_path}", file=sys.stderr)
                except Exception as e:
                    # Per user request, fail hard on read errors.
                    print(f"Error: Could not read file {file_path}: {e}", file=sys.stderr)
                    # Clean up the partially created zip file before exiting
                    zipf.close()
                    if output_path.exists():
                        output_path.unlink()
                    raise  # Re-raise to be caught by main and trigger a non-zero exit.
    except Exception as e:
        print(f"Error: Failed to create ZIP archive at {output_path}: {e}", file=sys.stderr)
        # Ensure cleanup if the error was outside the 'with' block
        if output_path.exists():
            output_path.unlink()
        raise

# --- New self-checking and main execution logic ---

def get_staged_files():
    """Returns a list of staged files for commit."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )
    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    return files

def main():
    parser = argparse.ArgumentParser(description="Self-checking repository manifest generator.")
    parser.add_argument("--test-files", nargs="*", help="Provide a list of changed files for testing (bypasses git).")
    args = parser.parse_args()

    files_to_consider = []
    if args.test_files:
        print(f"Using --test-files: {len(args.test_files)} files provided for manifest generation.")
        files_to_consider = args.test_files
    else:
        files_to_consider = get_staged_files()

    if not files_to_consider:
        print("No staged changes detected or test files provided; skipping manifest generation.")
        sys.exit(0)

    print(f"Changes detected ({len(files_to_consider)} files), regenerating manifest archive...")

    zip_output_path = PROJECT_ROOT / "project" / "reports" / "REPO_MANIFEST.zip"

    try:
        # Scan the repo to get the list of all files to be included.
        files_to_archive = scan_repo(str(PROJECT_ROOT))

        # Create the ZIP archive.
        create_zip_archive(zip_output_path, files_to_archive)

        print(f"Manifest ZIP successfully created at {zip_output_path}")

    except Exception:
        # The error message is already printed inside create_zip_archive.
        # Exit with a non-zero status code to signal failure.
        sys.exit(1)

if __name__ == "__main__":
    main()