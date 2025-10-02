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

PROJECT_ROOT = Path(__file__).parent.parent

# --- Functions from the original script ---

# Configuration
IGNORED_DIRS = {'.git', '.github', '.venv', '__pycache__', 'archive', 'api_dumps',
                'zotify_api.egg-info', 'templates', 'docs', 'alembic', 'build', 'dist'}
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
    manifest = []
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
            file_type = get_file_type(f)
            try:
                with open(path, 'r', encoding='utf-8') as file_obj:
                    content = file_obj.read()
            except Exception:
                content = '<binary or unreadable content>'
            # Determine workflow based on previous mapping
            workflow = []
            if f.startswith('audit'):
                workflow.append('audit')
            elif 'test' in f or f.startswith('run_e2e'):
                workflow.append('testing')
            elif f.startswith('generate'):
                workflow.append('documentation')
            elif f.startswith('linter') or f.startswith('validate'):
                workflow.append('validation')
            # Determine indexes
            indexes = []
            if f.endswith('CODE_FILE_INDEX.md') or f.endswith('MASTER_INDEX.md'):
                indexes.append(f)
            manifest.append({
                'path': rel_path.replace(os.sep, '/'),
                'type': file_type,
                'workflow': workflow,
                'indexes': indexes,
                'content': content
            })
    return manifest

def save_manifest(manifest, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, sort_keys=False, allow_unicode=True)

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

    print(f"Changes detected ({len(files_to_consider)} files), regenerating manifest...")
    manifest_file = PROJECT_ROOT / "project" / "reports" / "REPO_MANIFEST.md"

    # Call the original logic, ensuring we scan from the project root
    repo_manifest = scan_repo(str(PROJECT_ROOT))
    save_manifest(repo_manifest, manifest_file)
    print(f"Manifest regenerated: {manifest_file} with {len(repo_manifest)} entries")

if __name__ == "__main__":
    main()
