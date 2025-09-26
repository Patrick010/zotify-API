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
