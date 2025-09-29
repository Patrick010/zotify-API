#!/usr/bin/env python3
"""
verify_governance.py
Checks that all governance-related files in project/*/ are
present in PROJECT_REGISTRY.md. Ignores code files, archive junk,
and other non-governance paths by default.
"""

import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT / "project"
REGISTRY_FILE = PROJECT_DIR / "PROJECT_REGISTRY.md"
TRACE_INDEX = ROOT / "TRACE_INDEX.yml"

# Folders/files we don’t require in the registry
IGNORED_PREFIXES = (
    "project/archive/",
)
IGNORED_SUFFIXES = (
    ".py", ".js", ".css", ".html", ".toml",
    ".yml", ".yaml", ".lock", ".json",
)
IGNORED_FILES = {
    "project/.gitignore",
}

def parse_registry_paths(registry_file):
    """Extract all project/* paths from PROJECT_REGISTRY.md."""
    paths = set()
    link_re = re.compile(r"\]\(([^)]+)\)")
    for line in registry_file.read_text(encoding="utf-8").splitlines():
        for m in link_re.finditer(line):
            p = m.group(1).strip()
            if p.startswith("./"):
                p = p[2:]
            if not p.startswith("project/"):
                if "/" not in p:  # bare filename (e.g. HIGH_LEVEL_DESIGN.md)
                    p = f"project/{p}"
            paths.add(normalize_path(p))
    return paths


def parse_trace_index(trace_file):
    """Read TRACE_INDEX.yml and return all project/* paths."""
    data = yaml.safe_load(trace_file.read_text(encoding="utf-8"))
    files = set()
    for f in data.get("files", []):
        if f.startswith("project/"):
            files.add(normalize_path(f))
    return files


def normalize_path(p):
    """Canonicalize paths for comparison."""
    return str(Path(p)).replace("\\", "/")


def should_ignore(path):
    if path in IGNORED_FILES:
        return True
    if any(path.startswith(pref) for pref in IGNORED_PREFIXES):
        return True
    if any(path.endswith(suff) for suff in IGNORED_SUFFIXES):
        return True
    return False


def main():
    if not REGISTRY_FILE.exists():
        print(f"[!] Missing {REGISTRY_FILE}", file=sys.stderr)
        sys.exit(1)
    if not TRACE_INDEX.exists():
        print(f"[!] Missing {TRACE_INDEX}", file=sys.stderr)
        sys.exit(1)

    registry_paths = parse_registry_paths(REGISTRY_FILE)
    trace_paths = parse_trace_index(TRACE_INDEX)

    # Filter ignored
    registry_paths = {p for p in registry_paths if not should_ignore(p)}
    trace_paths = {p for p in trace_paths if not should_ignore(p)}

    missing_from_registry = sorted(trace_paths - registry_paths)
    missing_on_disk = sorted(registry_paths - trace_paths)

    if missing_from_registry:
        print("[!] Files present in TRACE_INDEX.yml but missing from PROJECT_REGISTRY.md:")
        for f in missing_from_registry:
            print(f" - {f}")
        print()

    if missing_on_disk:
        print("[!] Files listed in PROJECT_REGISTRY.md but not found in TRACE_INDEX.yml:")
        for f in missing_on_disk:
            print(f" - {f}")
        print()

    if not missing_from_registry and not missing_on_disk:
        print("[✓] PROJECT_REGISTRY.md and TRACE_INDEX.yml are in sync.")


if __name__ == "__main__":
    main()
