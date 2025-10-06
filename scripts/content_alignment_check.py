#!/usr/bin/env python3
import os
import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRACE_INDEX_PATH = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
OUTPUT_REPORT_PATH = PROJECT_ROOT / "project/reports/CONTENT_ALIGNMENT_REPORT.md"

# Documents to scan for references (docs only)
SCAN_SCOPE = [
    "project/PROJECT_REGISTRY.md",
    "project/ALIGNMENT_MATRIX.md",
    "project/HIGH_LEVEL_DESIGN.md",
    "project/LOW_LEVEL_DESIGN.md",
    "project/USECASES.md",
    "project/USECASES_GAP_ANALYSIS.md",
    "project/FUTURE_ENHANCEMENTS.md",
]

# Design docs for alignment checks
DESIGN_DOCS = {
    "design": {"project/HIGH_LEVEL_DESIGN.md", "project/LOW_LEVEL_DESIGN.md"},
    "trace": {"project/ALIGNMENT_MATRIX.md"},
    "usecase": {"project/USECASES.md", "project/USECASES_GAP_ANALYSIS.md"},
}

# Noise filters: anything outside documentation scope
NOISE_PATTERNS = [
    r"^api/",     # code under api/, except api/docs/
    r"^scripts/",
    r"^snitch/",
    r"^Gonk/",
    r"^tests?/",
    r"\.py$",
    r"\.json$",
    r"\.yml$",
    r"\.yaml$",
    r"\.toml$",
    r"\.cfg$",
    r"\.ini$",
    r"\.lock$",
]

def is_noise(path: str) -> bool:
    """Return True if path matches an excluded pattern."""
    return any(re.search(p, path) for p in NOISE_PATTERNS)

def load_registered_files():
    """Load all non-exempt, registered files from TRACE_INDEX.yml, filtering out noise."""
    if not TRACE_INDEX_PATH.exists():
        print(f"❌ ERROR: TRACE_INDEX.yml not found at {TRACE_INDEX_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(TRACE_INDEX_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f).get("artifacts", [])

    registered_files = {}
    for item in data:
        path = item.get("path")
        if (
            path
            and item.get("registered") is True
            and item.get("type") != "exempt"
            and not is_noise(path)
        ):
            registered_files[path] = {"index": item.get("index", "N/A")}
    return registered_files

def build_cross_reference_map(all_registered_files):
    """Scan configured documents and build cross-reference graph."""
    print("Building reference graph...")
    cross_ref_map = defaultdict(set)
    link_count = 0

    all_paths = list(all_registered_files.keys())
    if not all_paths:
        print("⚠️ No registered documentation files found in scope.")
        return cross_ref_map

    # Build regex matching base names and full paths
    pattern_parts = [re.escape(Path(p).name) for p in all_paths] + [re.escape(p) for p in all_paths]
    pattern_parts = sorted(list(set(pattern_parts)), key=len, reverse=True)
    master_pattern = re.compile("|".join(pattern_parts))

    for doc_path_str in SCAN_SCOPE:
        doc_path = PROJECT_ROOT / doc_path_str
        if not doc_path.exists():
            continue

        content = doc_path.read_text(encoding="utf-8", errors="ignore")
        mentions = master_pattern.findall(content)

        for mention in set(mentions):
            found_path = next((p for p in all_paths if p.endswith(mention)), None)
            if found_path and found_path != doc_path_str:
                cross_ref_map[doc_path_str].add(found_path)
                link_count += 1

    print(f"Cross-links found: {link_count}")
    return cross_ref_map

def validate_alignment(registered_files, cross_ref_map):
    """Validate each documentation file for alignment."""
    print("Validating file alignment...")
    results = []

    all_referenced_files = set()
    for targets in cross_ref_map.values():
        all_referenced_files.update(targets)

    for path, data in registered_files.items():
        notes = []
        status = "✅ Aligned"

        linked_in_design = any(path in cross_ref_map.get(doc, set()) for doc in DESIGN_DOCS["design"])
        linked_in_trace = any(path in cross_ref_map.get(doc, set()) for doc in DESIGN_DOCS["trace"])
        linked_in_usecase = any(path in cross_ref_map.get(doc, set()) for doc in DESIGN_DOCS["usecase"])

        if not linked_in_design:
            notes.append("Missing Design link (HLD/LLD)")
        if not linked_in_trace:
            notes.append("Missing Trace link (Alignment Matrix)")

        if path not in all_referenced_files:
            status = "❌ Orphan"
            notes.append("Not referenced anywhere")
        elif not linked_in_design or not linked_in_trace:
            status = "⚠️ Partial"

        linked_from = [src for src, targets in cross_ref_map.items() if path in targets]

        results.append({
            "file": path,
            "index": data["index"],
            "linked_in": linked_from[0] if linked_from else "—",
            "link_count": len(linked_from),
            "status": status,
            "notes": ", ".join(notes) or "Referenced in other docs",
        })
    return results

def generate_report(results):
    """Generate final Markdown report (docs-only)."""
    print(f"Writing report to {OUTPUT_REPORT_PATH}...")
    OUTPUT_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    header = [
        "# Content Alignment Report (Documentation Scope)\n",
        "| File | Registered In | Linked In | Link Count | Alignment Status | Notes |",
        "|------|----------------|------------|-------------|------------------|--------|",
    ]

    lines = header
    for res in sorted(results, key=lambda x: x["file"]):
        lines.append(f"| `{res['file']}` | `{res['index']}` | `{res['linked_in']}` | {res['link_count']} | {res['status']} | {res['notes']} |")

    total = len(results)
    aligned = sum(1 for r in results if r["status"] == "✅ Aligned")
    partial = sum(1 for r in results if r["status"] == "⚠️ Partial")
    orphans = sum(1 for r in results if r["status"] == "❌ Orphan")
    coverage = int((aligned + partial) / total * 100) if total else 100

    summary = [
        "\n## Summary\n",
        f"**Total documentation items:** {total}",
        f"**Fully aligned:** {aligned}",
        f"**Partial:** {partial}",
        f"**Orphans:** {orphans}",
        f"**Alignment coverage:** {coverage}%",
        "\n> ℹ️ Only documentation files were scanned. Code and config assets excluded.\n",
    ]

    lines.extend(summary)
    OUTPUT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return aligned, partial, orphans, coverage

def main():
    parser = argparse.ArgumentParser(description="Content-Level Documentation Alignment Check")
    parser.add_argument("--scan", action="store_true", help="Scan and generate the alignment report (default).")
    parser.add_argument("--enforce", action="store_true", help="Enforce alignment policy for CI.")
    args = parser.parse_args()

    if not args.scan and not args.enforce:
        args.scan = True

    print("Scanning documentation indices...")
    registered_files = load_registered_files()
    cross_ref_map = build_cross_reference_map(registered_files)
    validation_results = validate_alignment(registered_files, cross_ref_map)
    aligned, partial, orphans, coverage = generate_report(validation_results)

    if args.enforce:
        print("\n--- Enforcing Policy ---")
        orphan_threshold = int(len(registered_files) * 0.1)
        coverage_threshold = 90
        if coverage < coverage_threshold or orphans > orphan_threshold:
            print("❌ Content alignment check failed.")
            print(f"   Coverage: {coverage}% (min {coverage_threshold}%)")
            print(f"   Orphans: {orphans} (max {orphan_threshold})")
            sys.exit(1)
        print("✅ Documentation alignment coverage acceptable.")
        sys.exit(0)

if __name__ == "__main__":
    main()
