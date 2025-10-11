# ID: OPS-010
#!/usr/bin/env python3
"""
generate_alignment_matrix_md.py
Converts ALIGNMENT_MATRIX.yml back into a readable Markdown version.
"""

import yaml
from pathlib import Path

SRC = Path("project/ALIGNMENT_MATRIX.yml")
DEST = Path("project/ALIGNMENT_MATRIX.md")

def main():
    print("--- Regenerating Markdown Alignment Matrix ---")
    if not SRC.exists():
        print(f"[ERROR] Missing canonical source: {SRC}")
        return

    try:
        data = yaml.safe_load(SRC.read_text())
    except yaml.YAMLError as e:
        print(f"[ERROR] Could not parse YAML file {SRC}: {e}")
        return

    if not data:
        print("[INFO] YAML source is empty. Generating an empty Markdown file.")
        out = ["# Alignment Matrix\n\n*No entries found.*"]
    else:
        out = ["# Alignment Matrix\n"]
        # Sort entries by ID for consistent output
        data.sort(key=lambda x: x.get('id', ''))

        for entry in data:
            entry_id = entry.get('id', 'N/A')
            out.append(f"## {entry_id}")

            if "description" in entry and entry['description']:
                out.append(f"**Description:** {entry['description']}")

            if entry.get("linked_docs"):
                out.append("\n**Linked Docs:**")
                out.extend([f"- `{d}`" for d in sorted(entry["linked_docs"])])

            if entry.get("code_paths"):
                out.append("\n**Code Paths:**")
                out.extend([f"- `{p}`" for p in sorted(entry["code_paths"])])

            if entry.get("related_tasks"):
                out.append("\n**Related Tasks:**")
                out.extend([f"- {t}" for t in sorted(entry["related_tasks"])])

            out.append("\n---") # Add a separator for readability

    try:
        DEST.write_text("\n".join(out), encoding='utf-8')
        print(f"[OK] Markdown alignment matrix regenerated at {DEST}")
    except Exception as e:
        print(f"[ERROR] Failed to write Markdown file: {e}")


if __name__ == "__main__":
    main()