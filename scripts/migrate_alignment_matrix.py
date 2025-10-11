# ID: OPS-020
#!/usr/bin/env python3
"""
migrate_alignment_matrix.py
Parses the legacy ALIGNMENT_MATRIX.md and generates a normalized ALIGNMENT_MATRIX.yml.
"""

import re
import yaml
from pathlib import Path

SOURCE = Path("project/ALIGNMENT_MATRIX.md")
DEST = Path("project/ALIGNMENT_MATRIX.yml")
TAG_INVENTORY = Path("project/reports/DOCUMENT_TAG_INVENTORY.yml")
ARCHIVE_DEST = Path("project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md")

def load_inventory():
    """Loads the document inventory and creates a path-to-ID mapping."""
    if not TAG_INVENTORY.exists():
        print(f"[ERROR] Missing inventory file: {TAG_INVENTORY}")
        return None
    try:
        data = yaml.safe_load(TAG_INVENTORY.read_text(encoding='utf-8'))
        return {entry["path"]: entry["id"] for entry in data if "path" in entry and "id" in entry}
    except (yaml.YAMLError, IOError) as e:
        print(f"[ERROR] Could not read or parse inventory file: {e}")
        return None

def parse_artifact_links(text: str) -> dict:
    """Parses Section 5 to get a map from Requirement ID to file paths."""
    link_map = {}
    section_match = re.search(r"## 5\. Artifact-to-Requirement Traceability\n\n(.*?)(?=\n##|$)", text, re.DOTALL)
    if not section_match:
        print("[WARNING] Could not find Section 5 'Artifact-to-Requirement Traceability'.")
        return link_map

    table_text = section_match.group(1)
    for line in table_text.splitlines()[2:]: # Skip header and separator
        if not line.strip().startswith('|'):
            continue
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) < 2:
            continue

        artifact_path = cols[0].strip('`')
        linked_to = cols[1].strip('`')

        req_match = re.search(r'([A-Z]{2,4}-\d+)', linked_to)
        if req_match:
            req_id = req_match.group(1)
            if req_id not in link_map:
                link_map[req_id] = []
            link_map[req_id].append(artifact_path)

    return link_map

def parse_legacy_matrix(text: str, artifact_links: dict) -> list:
    """Parses Section 2, the main alignment table, enriched with artifact links."""
    entries = {}
    section_match = re.search(r"## 2\. Core System & Component Alignment\n\n(.*?)(?=\n##|$)", text, re.DOTALL)
    if not section_match:
        print("[ERROR] Could not find Section 2 'Core System & Component Alignment'.")
        return []

    table_text = section_match.group(1)
    lines = table_text.strip().splitlines()
    header = [h.strip() for h in lines[0].strip('|').split('|')]

    try:
        col_indices = {
            "audit_ref": header.index('Audit Ref'),
            "feature": header.index('Feature / Component'),
            "req_id": header.index('Requirement ID'),
            "hld": header.index('HLD Reference'),
            "lld": header.index('LLD Reference'),
            "code": header.index('Code Path(s)'),
            "doc": header.index('Documentation'),
        }
    except ValueError as e:
        print(f"[ERROR] Missing expected column in alignment matrix: {e}")
        return []

    for line in lines[2:]:
        cols = [c.strip() for c in line.strip('|').split('|')]
        if len(cols) != len(header) or not cols[col_indices["audit_ref"]].startswith('AR-'):
            continue

        audit_ref = cols[col_indices["audit_ref"]]
        req_id = cols[col_indices["req_id"]]
        primary_id = req_id if req_id and any(req_id.startswith(p) for p in ['FEAT-', 'SYS-', 'UC-']) else audit_ref

        entry = entries.setdefault(primary_id, {
            "id": primary_id, "description": cols[col_indices["feature"]],
            "linked_docs": set(), "code_paths": set(), "related_tasks": set()
        })

        if primary_id != audit_ref:
            entry["related_tasks"].add(audit_ref)

        def extract_path(md_link):
            path_match = re.search(r'\((.*?)\)', md_link)
            return path_match.group(1).split('#')[0] if path_match else None

        for col_key, col_content in [('hld', cols[col_indices["hld"]]), ('lld', cols[col_indices["lld"]]), ('doc', cols[col_indices["doc"]])]:
            path = extract_path(col_content) or (col_content.strip('`') if '`' in col_content else None)
            if path:
                entry["linked_docs"].add(path)

        for p in cols[col_indices["code"]].replace('`', '').split(','):
            if p.strip():
                entry["code_paths"].add(p.strip())

        # Add files from the artifact link map
        for linked_id in [primary_id, audit_ref]:
            if linked_id in artifact_links:
                for path in artifact_links[linked_id]:
                    if any(path.endswith(ext) for ext in ['.py', '.go', '.js', '.sh', '.yml', '.toml']):
                         entry["code_paths"].add(path)
                    else:
                         entry["linked_docs"].add(path)

    # Convert sets to lists for YAML output
    final_entries = list(entries.values())
    for e in final_entries:
        e["linked_docs"] = sorted(list(e["linked_docs"]))
        e["code_paths"] = sorted(list(e["code_paths"]))
        e["related_tasks"] = sorted(list(e["related_tasks"]))

    return final_entries

def map_paths_to_ids(entries: list, inventory_map: dict) -> tuple[list, list]:
    """Maps file paths to new document IDs, archiving entries that can't be mapped."""
    migrated_entries = []
    archived_entries = []

    path_to_id_map_clean = {k.strip('`'): v for k, v in inventory_map.items()}

    for e in entries:
        all_paths = e["linked_docs"] + e["code_paths"]
        mapped_docs, mapped_code = set(), set()
        unmapped_paths = []

        for p in e["linked_docs"]:
            mapped_id = path_to_id_map_clean.get(p)
            if mapped_id:
                mapped_docs.add(mapped_id)
            else:
                unmapped_paths.append(p)

        for p in e["code_paths"]:
            mapped_id = path_to_id_map_clean.get(p)
            if mapped_id:
                mapped_code.add(mapped_id)
            else:
                unmapped_paths.append(p)

        if not mapped_docs and not mapped_code:
            e["reason_for_archival"] = "No valid, inventoried files could be linked."
            e["unmapped_paths"] = unmapped_paths
            archived_entries.append(e)
        else:
            e["linked_docs"] = sorted(list(mapped_docs))
            e["code_paths"] = sorted(list(mapped_code))
            migrated_entries.append(e)

    return migrated_entries, archived_entries

def main():
    print("--- Starting Alignment Matrix Migration ---")
    inventory_map = load_inventory()
    if inventory_map is None:
        return

    if not SOURCE.exists():
        print(f"[ERROR] Missing source file: {SOURCE}")
        return

    source_text = SOURCE.read_text(encoding='utf-8')
    artifact_links = parse_artifact_links(source_text)
    parsed_entries = parse_legacy_matrix(source_text, artifact_links)

    if not parsed_entries:
        print("[ERROR] Failed to parse any entries from the legacy matrix.")
        return

    migrated, archived = map_paths_to_ids(parsed_entries, inventory_map)

    # Write migrated entries
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with open(DEST, "w", encoding='utf-8') as f:
        yaml.safe_dump(migrated, f, sort_keys=False, indent=2, default_flow_style=False)
    print(f"[OK] Migrated {len(migrated)} entries to {DEST}")

    # Write archived entries
    if archived:
        ARCHIVE_DEST.parent.mkdir(parents=True, exist_ok=True)
        with open(ARCHIVE_DEST, "w", encoding='utf-8') as f:
            f.write("# Archived Alignment Matrix Entries\n\n")
            yaml.safe_dump(archived, f, sort_keys=False, indent=2)
        print(f"[OK] Archived {len(archived)} entries to {ARCHIVE_DEST}")

if __name__ == "__main__":
    main()