# ID: OPS-013
#!/usr/bin/env python3
import os
import json

# --- Config ---
# Where to save the manifest (relative to repo root)
manifest_path = "scripts/repo_manifest.txt"

# Base URL where the files will be served
base_url = "https://chatgtp.sixfold.nl"

# Folders/files to include in the manifest
include_paths = [
    "project",
    "api",
    "Gonk",
    "scripts",
    "snitch",
    "templates",
    "tests",
    "AGENTS.md",
]

# File types to include
include_extensions = [".md", ".yml", ".json", ".sh", ".go", ".py"]  # adjust as needed

# --- Script ---
manifest = {}
order = []

for root_dir in include_paths:
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d != '.venv']
        for f in filenames:
            if any(f.endswith(ext) for ext in include_extensions):
                rel_path = os.path.join(dirpath, f).replace("\\", "/")
                key = os.path.splitext(f)[0].upper()  # e.g., ONBOARDING.md → ONBOARDING
                url = f"{base_url}/{rel_path}"
                manifest[key] = url
                order.append(key)

# Add order array for deterministic reading
manifest["order"] = order

# Ensure target folder exists
os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

# Write manifest
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest generated at {manifest_path}, {len(order)} files included.")
