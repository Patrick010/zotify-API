#!/usr/bin/env python3
import os
import yaml

# Configuration
IGNORED_DIRS = {'.git', '.github', '.venv', '__pycache__', 'archive', 'api_dumps',
                'zotify_api.egg-info', 'src', 'templates', 'docs', 'alembic'}
IGNORED_FILES = {'.DS_Store', '.gitignore', 'REPO_MANIFEST.md', 'openapi.json',
                 'LICENSE', 'CONTRIBUTING.md', 'alembic.ini'}
# Files that should be included even if in ignored dirs
INCLUDED_FILES = {'api/docs/MASTER_INDEX.md'}
OUTPUT_FILE = os.path.join('project', 'reports', 'REPO_MANIFEST.md')


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


def save_manifest(manifest, output_file=OUTPUT_FILE):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, sort_keys=False, allow_unicode=True)


if __name__ == '__main__':
    repo_manifest = scan_repo('.')
    save_manifest(repo_manifest)
    print(f"REPO_MANIFEST.md generated at {OUTPUT_FILE} with {len(repo_manifest)} entries")
