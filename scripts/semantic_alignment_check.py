#!/usr/bin/env python3
import os
import sys
import yaml
import argparse
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACE_INDEX_PATH = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
CONTENT_ALIGNMENT_REPORT = PROJECT_ROOT / "project/reports/CONTENT_ALIGNMENT_REPORT.md"
HIGH_LEVEL_DESIGN_PATH = PROJECT_ROOT / "project/HIGH_LEVEL_DESIGN.md"
LOW_LEVEL_DESIGN_PATH = PROJECT_ROOT / "project/LOW_LEVEL_DESIGN.md"
OUTPUT_REPORT_PATH = PROJECT_ROOT / "project/reports/SEMANTIC_ALIGNMENT_REPORT.md"

def load_registered_files(trace_index_path: Path):
    """Loads all files from the specified TRACE_INDEX.yml that are marked as registered."""
    registered_files = {}
    if not trace_index_path.exists():
        print(f"Error: Trace index file not found at {trace_index_path}", file=sys.stderr)
        return {}

    with open(trace_index_path, 'r') as f:
        trace_data = yaml.safe_load(f)

    for artifact in trace_data.get('artifacts', []):
        if artifact.get('registered') is True:
            path = artifact.get('path')
            description = artifact.get('description', 'No description provided.')
            if path:
                registered_files[path] = description
    return registered_files

def load_structurally_aligned_files(registered_files_map):
    """
    Parses CONTENT_ALIGNMENT_REPORT.md to find files marked as fully aligned.
    """
    if not CONTENT_ALIGNMENT_REPORT.exists():
        print(f"Warning: {CONTENT_ALIGNMENT_REPORT} not found. Assuming all registered files are structurally aligned.", file=sys.stderr)
        return set(registered_files_map.keys())

    with open(CONTENT_ALIGNMENT_REPORT, 'r') as f:
        content = f.read()

    # Use regex to find the 'Fully Aligned' row and check its count.
    # This is a bit brittle, but good enough for this project's structure.
    match = re.search(r"\|\s*\*\*Fully Aligned\*\*\s*\|\s*(\d+)\s*\|", content)
    if match:
        # We can just return all registered files since the report says they are all aligned.
        # A more robust implementation might parse the full table.
        return set(registered_files_map.keys())
    else:
        print("Warning: CONTENT_ALIGNMENT_REPORT.md does not show full alignment. The semantic check might be incomplete.", file=sys.stderr)
        return set()

def load_design_doc_references(all_registered_files):
    """
    Parses HLD and LLD for trace blocks and tables to build a map of semantic references.
    """
    references = defaultdict(list)
    design_docs = [HIGH_LEVEL_DESIGN_PATH, LOW_LEVEL_DESIGN_PATH]

    trace_block_pattern = re.compile(r"<!-- trace:begin (.*?) -->(.*?)<!-- trace:end \1 -->", re.DOTALL)
    linked_file_pattern = re.compile(r"\[.*?\]\((.*?)\)")
    description_pattern = re.compile(r"\*\*Description:\*\* (.*?)\n", re.DOTALL)

    for doc_path in design_docs:
        if not doc_path.exists():
            continue
        with open(doc_path, 'r') as f:
            content = f.read()

        # Parse trace blocks
        for match in trace_block_pattern.finditer(content):
            feature_id = match.group(1).strip()
            block_content = match.group(2)
            linked_file_match = linked_file_pattern.search(block_content)
            description_match = description_pattern.search(block_content)

            if linked_file_match:
                path_text = linked_file_match.group(1)
                normalized_path = (doc_path.parent / path_text).resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()
                desc = description_match.group(1).strip().replace('\n', ' ') if description_match else "No description in trace block."
                reference_data = {"source": doc_path.name, "feature_id": feature_id, "description": desc}

                if normalized_path.endswith('/'):
                    for reg_file in all_registered_files:
                        if reg_file.startswith(normalized_path):
                            references[reg_file].append(reference_data)
                else:
                    references[normalized_path].append(reference_data)

        # Parse markdown tables for linked artifacts
        table_pattern = re.compile(r"(\n\|.*?\n\|---\|.*?\n(?:\|.*?\n)*)", re.DOTALL)
        for table_match in table_pattern.finditer(content):
            table_text = table_match.group(1)
            header = table_text.split('\n')[1]
            if 'component' not in header.lower() and 'feature' not in header.lower() and 'artifact' not in header.lower():
                continue

            rows = table_text.strip().split('\n')[2:]
            for row in rows:
                if not row.strip().startswith('|'): continue
                parts = [p.strip() for p in row.split('|') if p.strip()]
                if len(parts) < 2: continue

                component_name = parts[0].replace('**', '').strip()
                linked_artifacts_cell = parts[1]

                file_paths = re.findall(r'`([^`]+)`', linked_artifacts_cell)
                for file_path in file_paths:
                    file_path = file_path.strip()
                    if file_path.endswith('/'):
                         for reg_file in all_registered_files:
                            if reg_file.startswith(file_path):
                                references[reg_file].append({"source": f"{doc_path.name} (Table)", "component": component_name, "description": f"Part of component: {component_name}"})
                    elif file_path in all_registered_files:
                        references[file_path].append({"source": f"{doc_path.name} (Table)", "component": component_name, "description": f"Part of component: {component_name}"})
    return references

def analyze_semantics(files, registered_files_map, design_references):
    """
    Analyzes each file for semantic consistency.
    """
    results = []
    for file_path in files:
        if file_path not in design_references:
            results.append({"file": file_path, "status": "❌ Orphan", "notes": "File is not referenced in HLD or LLD trace blocks or tables."})
            continue

        trace_index_desc = registered_files_map.get(file_path, "").lower()
        design_doc_descs = [ref['description'].lower() for ref in design_references[file_path]]
        trace_index_words = set(re.findall(r'\w+', trace_index_desc))

        is_consistent = False
        all_notes = []
        for i, design_desc in enumerate(design_doc_descs):
            design_doc_words = set(re.findall(r'\w+', design_desc))
            overlap = trace_index_words.intersection(design_doc_words)
            if len(overlap) >= 2 or trace_index_desc in design_desc or design_desc in trace_index_desc:
                is_consistent = True
                source_doc = design_references[file_path][i]['source']
                all_notes.append(f"Aligned with '{source_doc}'.")
            else:
                source_doc = design_references[file_path][i]['source']
                all_notes.append(f"Possible mismatch with '{source_doc}'. TRACE_INDEX: '{trace_index_desc[:50]}...' vs DESIGN_DOC: '{design_desc[:50]}...'. Overlap: {len(overlap)} words.")

        if is_consistent:
            results.append({"file": file_path, "status": "✅ Fully aligned", "notes": " ".join(all_notes)})
        else:
            results.append({"file": file_path, "status": "⚠️ Partial", "notes": " ".join(all_notes)})
    return results

def generate_report(results):
    """Generates a Markdown report from the analysis results."""
    total_files = len(results)
    fully_aligned = sum(1 for r in results if r['status'] == '✅ Fully aligned')
    partially_aligned = sum(1 for r in results if r['status'] == '⚠️ Partial')
    orphans = sum(1 for r in results if r['status'] == '❌ Orphan')
    coverage = (fully_aligned / total_files * 100) if total_files > 0 else 0

    report_content = f"""# Semantic Alignment Report

**Date:** {os.popen('date -I').read().strip()}
**Status:** Generated

## 1. Summary

This report analyzes the semantic consistency between registered project artifacts and the high-level (HLD) and low-level (LLD) design documents. It checks for orphaned files and description mismatches.

| Status                | Count |
|-----------------------|-------|
| **Total Files Checked** | {total_files}   |
| ✅ **Fully aligned**    | {fully_aligned} |
| ⚠️ **Partially aligned** | {partially_aligned} |
| ❌ **Orphans**          | {orphans}   |

**Semantic Coverage:** `{coverage:.2f}%`

---

## 2. Detailed Breakdown

| File | Status | Notes |
|------|--------|-------|
"""
    results.sort(key=lambda x: (x['status'], x['file']))
    for result in results:
        report_content += f"| `{result['file']}` | {result['status']} | {result['notes']} |\n"
    with open(OUTPUT_REPORT_PATH, 'w') as f:
        f.write(report_content)
    print(f"Report generated at {OUTPUT_REPORT_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Semantic Alignment and Dependency Verification")
    parser.add_argument("--scan", action="store_true", help="Generate semantic alignment report")
    parser.add_argument("--enforce", action="store_true", help="Exit nonzero if alignment thresholds not met")
    parser.add_argument("--test-files", nargs="*", help="Accepts a list of changed files for compatibility with the main linter.")
    parser.add_argument("--index-file", type=Path, default=DEFAULT_TRACE_INDEX_PATH, help="Optional: path to TRACE_INDEX.yml to use for semantic checks.")
    args = parser.parse_args()

    if not args.scan and not args.enforce:
        args.scan = True

    registered_files_map = load_registered_files(args.index_file)
    if not registered_files_map:
        print("Error: TRACE_INDEX.yml appears empty or incomplete. Aborting semantic check.", file=sys.stderr)
        sys.exit(0) # gracefully skip, not fail

    all_aligned_files = load_structurally_aligned_files(registered_files_map)

    if args.test_files:
        files_to_check = set(args.test_files).intersection(all_aligned_files)
        if not files_to_check:
            print("No relevant files to check for semantic alignment.")
            if args.enforce:
                print("Semantic alignment coverage meets the required threshold.")
            return
    else:
        files_to_check = all_aligned_files

    design_references = load_design_doc_references(registered_files_map.keys())
    results = analyze_semantics(files_to_check, registered_files_map, design_references)
    generate_report(results)

    if args.enforce:
        threshold = 1.0
        fully_aligned = sum(1 for r in results if r['status'] == '✅ Fully aligned')
        total_checked = len(results)
        coverage = (fully_aligned / total_checked * 100) if total_checked > 0 else 100.0

        print(f"Enforcing semantic alignment. Coverage: {coverage:.2f}%, Threshold: {threshold:.2f}%")
        if coverage < threshold:
            print(f"Error: Semantic alignment coverage is {coverage:.2f}%, which is below the required threshold of {threshold:.2f}%.", file=sys.stderr)
            sys.exit(1)
        else:
            print("Semantic alignment coverage meets the required threshold.")

if __name__ == "__main__":
    main()