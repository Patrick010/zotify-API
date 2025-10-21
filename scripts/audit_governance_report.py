#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ID: OPS-037
"""
A read-only audit script to generate a complete report summarizing the state of
traceability, alignment, and governance integrity for the repository.
"""

import datetime
import os
import re
from pathlib import Path
import yaml

# === Configuration ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "project" / "reports"
TRACE_INDEX_PATH = REPORTS_DIR / "TRACE_INDEX.yml"
TAG_INVENTORY_PATH = REPORTS_DIR / "DOCUMENT_TAG_INVENTORY.yml"
OUTPUT_REPORT_PATH = REPORTS_DIR / f"ALIGNMENT_AUDIT_{datetime.date.today().isoformat()}.md"

# Keywords to detect low-quality descriptions
WEAK_DESC_KEYWORDS = [
    "tbd",
    "todo",
    "to be updated",
    "auto-generated",
    "placeholder",
    "none",
    "n/a",
    "work in progress",
    "no description",
]

# Expected tag prefixes based on directory structure
TAG_PREFIX_MAP = {
    "project/": "DOC-",
    "scripts/": "SCR-",
    "api/": "API-",
    "nlp/": "NLP-",
    "tests/": "TEST-",
    "Gonk/": "GONK-",
    "snitch/": "SNITCH-",
    "templates/": "TPL-",
    "default": "GEN-", # Generic/uncategorized
}

def get_tag_prefix(path_str: str) -> str:
    """Determines the expected tag prefix for a given file path."""
    for dir_prefix, tag_prefix in TAG_PREFIX_MAP.items():
        if path_str.startswith(dir_prefix):
            return tag_prefix
    # Check for root files like AGENTS.md
    if "/" not in path_str:
        return "DOC-"
    return TAG_PREFIX_MAP["default"]

def load_yaml_file(path: Path) -> dict | list | None:
    """Loads a YAML file and returns its content, or None on error."""
    if not path.exists():
        print(f"ERROR: File not found: {path}")
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        print(f"ERROR: Could not parse YAML file {path}: {e}")
        return None

def verify_alignment(trace_index_data: dict, tag_inventory_data: list) -> dict:
    """
    Cross-checks TRACE_INDEX.yml and DOCUMENT_TAG_INVENTORY.yml.
    """
    findings = {
        "missing_from_trace": [],
        "missing_from_inventory": [],
        "id_mismatch": [],
        "duplicate_ids_in_inventory": set(),
        "trace_count": 0,
        "inventory_count": 0,
    }

    if not trace_index_data or "artifacts" not in trace_index_data:
        return findings
    if not tag_inventory_data:
        return findings

    trace_artifacts = {item["path"]: item for item in trace_index_data.get("artifacts", [])}
    inventory_docs = {item["path"]: item for item in tag_inventory_data}

    findings["trace_count"] = len(trace_artifacts)
    findings["inventory_count"] = len(inventory_docs)

    for path in inventory_docs:
        if path not in trace_artifacts:
            findings["missing_from_trace"].append(path)

    for path in trace_artifacts:
        if path not in inventory_docs:
            findings["missing_from_inventory"].append(path)

    for path, doc in inventory_docs.items():
        inventory_id = doc.get("id")
        embedded_id = trace_artifacts.get(path, {}).get("meta", {}).get("id")
        if embedded_id and inventory_id and embedded_id != inventory_id:
            findings["id_mismatch"].append(
                f"`{path}` (Inventory: {inventory_id}, Embedded: {embedded_id})"
            )

    seen_ids = set()
    for doc in tag_inventory_data:
        doc_id = doc.get("id")
        if doc_id in seen_ids:
            findings["duplicate_ids_in_inventory"].add(doc_id)
        seen_ids.add(doc_id)

    return findings

def audit_semantic_descriptions(trace_index: dict) -> list:
    """
    Audits the quality of semantic descriptions in the trace index.
    """
    findings = []
    if not trace_index or "artifacts" not in trace_index:
        return findings

    for item in trace_index.get("artifacts", []):
        path = item.get("path")
        description = item.get("meta", {}).get("description", "").lower().strip()
        severity = "none"

        if not description:
            severity = "missing"
        elif len(description) < 20:
            severity = "weak"
        elif any(keyword in description for keyword in WEAK_DESC_KEYWORDS):
            severity = "non-semantic"

        if severity != "none":
            findings.append({
                "path": path,
                "severity": severity,
                "description": item.get("meta", {}).get("description", "N/A"),
            })

    findings.sort(key=lambda x: ("missing", "non-semantic", "weak").index(x["severity"]))
    return findings

def check_tag_consistency() -> list:
    """
    Ensures tags follow governance prefixes and that governed documents
    contain a valid embedded ID comment.
    """
    findings = []
    all_files = [p for p in PROJECT_ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]

    for file_path in all_files:
        if file_path.name.startswith("run_audit"):
             continue
        try:
            content = file_path.read_text(encoding="utf-8")
            relative_path_str = str(file_path.relative_to(PROJECT_ROOT))

            match = re.search(r"<!--\s*ID:\s*([A-Z0-9-]+)\s*-->", content)
            if match:
                embedded_id = match.group(1)
                expected_prefix = get_tag_prefix(relative_path_str)
                if not embedded_id.startswith(expected_prefix):
                    findings.append(
                        f"ID format error in `{relative_path_str}`: "
                        f"Expected prefix `{expected_prefix}`, found `{embedded_id}`."
                    )
            elif file_path.suffix == ".md" and "logs" not in relative_path_str:
                 if not content.strip().startswith("<!-- ID:"):
                    findings.append(f"Missing embedded ID in `{relative_path_str}`.")

        except (UnicodeDecodeError, OSError):
            continue

    return findings

def audit_governance_policies(trace_index: dict) -> dict:
    """
    Refined governance audit logic to provide a more accurate classification of "unlinked" files.
    """
    project_files = [
        p.relative_to(PROJECT_ROOT).as_posix()
        for p in PROJECT_ROOT.glob("project/**/*.md")
        if p.is_file() and "archive" not in p.parts and "logs" not in p.parts
    ]

    traced_paths = set(trace_index.keys())

    report = {
        "fully_aligned": [],
        "partially_aligned": [],
        "unlinked_registered_false": [],
        "unlinked_not_in_index": []
    }

    for f_path in project_files:
        if f_path not in traced_paths:
            report["unlinked_not_in_index"].append(f_path)
            continue

        item = trace_index[f_path]
        if item and item.get("registered") is True:
            if item.get("index") and item.get("index") != "-":
                report["fully_aligned"].append(f_path)
            else:
                report["partially_aligned"].append(f_path)
        else: # registered is False or missing
            report["unlinked_registered_false"].append(f_path)

    return report

def generate_report(findings: dict) -> None:
    """
    Consolidates all findings into a single Markdown report.
    """
    print(f"Generating audit report at: {OUTPUT_REPORT_PATH}")

    # Alignment Summary
    alignment_summary = findings["alignment"]
    summary_table = f"""
| Metric                          | Count |
| ------------------------------- | ----- |
| Total Artifacts in Trace Index  | {alignment_summary.get("trace_count", 0)} |
| Total Artifacts in Tag Inventory| {alignment_summary.get("inventory_count", 0)} |
| **Orphans** (in Trace, not Inv) | {len(alignment_summary.get("missing_from_inventory", []))} |
| **Missing** (in Inv, not Trace) | {len(alignment_summary.get("missing_from_trace", []))} |
| Duplicate IDs in Inventory      | {len(alignment_summary.get("duplicate_ids_in_inventory", []))} |
| Mismatched IDs (Embedded vs Inv)| {len(alignment_summary.get("id_mismatch", []))} |
"""

    # Semantic Description Quality
    semantic_findings = findings["semantic"]
    semantic_table = "| File Path | Severity | Description Preview |\n"
    semantic_table += "| --- | --- | --- |\n"
    for item in semantic_findings:
        desc_preview = item["description"].replace("\n", " ").strip()[:100]
        semantic_table += f"| `{item['path']}` | **{item['severity'].upper()}** | `{desc_preview}` |\n"

    # Tag & ID Consistency
    tag_list = "\n".join([f"- {f}" for f in findings["tags"]])

    # Governance Violations
    gov_findings = findings["governance"]
    gov_list = "### Fully Aligned\n"
    gov_list += "\n".join([f"- `{f}`" for f in gov_findings.get("fully_aligned", [])]) or "None"
    gov_list += "\n\n### Partially Aligned (Registered but not in an index)\n"
    gov_list += "\n".join([f"- `{f}`" for f in gov_findings.get("partially_aligned", [])]) or "None"
    gov_list += "\n\n### Unlinked (Present in Index but Marked `registered: false`)\n"
    gov_list += "\n".join([f"- `{f}`" for f in gov_findings.get("unlinked_registered_false", [])]) or "None"
    gov_list += "\n\n### Unlinked (Not Found in Index)\n"
    gov_list += "\n".join([f"- `{f}`" for f in gov_findings.get("unlinked_not_in_index", [])]) or "None"

    # Recommendations
    recommendations = """
- Run `scripts/repo_inventory_and_governance.py --full-scan` to resolve discrepancies between the file system and `TRACE_INDEX.yml`.
- Review files with low-quality descriptions to improve project clarity.
- Correct files with ID format errors or missing embedded IDs.
- For `Partially Aligned` files, ensure they are correctly added to a documentation index file.
- For files `Marked 'registered: false'`, decide if they should be officially governed and update their `registered` status in `TRACE_INDEX.yml` accordingly.
"""

    # Assemble the report
    duplicates_set = alignment_summary.get("duplicate_ids_in_inventory", ["None"])
    duplicates_str = '`, `'.join(sorted(list(duplicates_set)))

    report_content = f"""
# Alignment & Governance Audit Report

**Date:** {datetime.date.today().isoformat()}

---

## 1. Alignment Summary

{summary_table}

### Details: Orphans (In Trace Index but not Tag Inventory)
- `{"`\n- `".join(alignment_summary.get("missing_from_inventory", ["None"]))}`

### Details: Missing (In Tag Inventory but not Trace Index)
- `{"`\n- `".join(alignment_summary.get("missing_from_trace", ["None"]))}`

### Details: Duplicate IDs
- `{duplicates_str}`

---

## 2. Semantic Description Quality

Found {len(semantic_findings)} files with low-quality descriptions.

{semantic_table}

---

## 3. Tag & ID Consistency

{tag_list}

---

## 4. Governance Violations

This section audits project markdown files for their registration and linkage status.

{gov_list}

---

## 5. Recommendations

{recommendations}

---
✅ Audit completed – no changes applied.
"""

    try:
        OUTPUT_REPORT_PATH.write_text(report_content.strip(), encoding="utf-8")
        print("Report successfully generated.")
    except IOError as e:
        print(f"ERROR: Could not write report to {OUTPUT_REPORT_PATH}: {e}")

def main():
    """Main execution function."""
    print("--- Starting Read-Only Repository Audit (V3) ---")

    trace_index_data = load_yaml_file(TRACE_INDEX_PATH)
    tag_inventory_data = load_yaml_file(TAG_INVENTORY_PATH)

    if not trace_index_data or not tag_inventory_data:
        print("Aborting audit due to missing or invalid core governance files.")
        return 1

    # Filter out exempt files from trace_index_data
    if "artifacts" in trace_index_data:
        trace_index_data["artifacts"] = [
            item for item in trace_index_data["artifacts"]
            if item.get("type") != "exempt"
        ]

    trace_index_map = {item["path"]: item for item in trace_index_data.get("artifacts", [])}

    all_findings = {
        "alignment": verify_alignment(trace_index_data, tag_inventory_data),
        "semantic": audit_semantic_descriptions(trace_index_data),
        "tags": check_tag_consistency(),
        "governance": audit_governance_policies(trace_index_map),
    }

    generate_report(all_findings)

    print("--- Audit Finished ---")
    return 0

if __name__ == "__main__":
    exit(main())
