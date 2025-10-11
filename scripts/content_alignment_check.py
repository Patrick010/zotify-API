# ID: OPS-006
#!/usr/bin/env python3
"""
Content Alignment Check (Phase 2 lockdown version)

- Only considers files registered under the `project/` namespace.
- Scans project index/docs for cross-references.
- Filters noise by:
    * excluding certain file name patterns (configurable)
    * ignoring items below a minimum inbound-link threshold (configurable)
- Produces:
    * project/reports/CONTENT_ALIGNMENT_REPORT.md
    * project/reports/DESCRIPTION_COMPLIANCE_REPORT.md
    * project/reports/ALIGNMENT_INTEGRITY_SNAPSHOT.yml
- Read-only: no file edits, only reports.
- Has `--enforce` to fail CI when coverage/orphan thresholds are violated.
"""
from __future__ import annotations
import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# --- Configurable constants -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRACE_INDEX_PATH = PROJECT_ROOT / "project/reports/TRACE_INDEX.yml"
REPORT_DIR = PROJECT_ROOT / "project/reports"
CONTENT_REPORT_PATH = REPORT_DIR / "CONTENT_ALIGNMENT_REPORT.md"
DESC_REPORT_PATH = REPORT_DIR / "DESCRIPTION_COMPLIANCE_REPORT.md"
SNAPSHOT_PATH = REPORT_DIR / "ALIGNMENT_INTEGRITY_SNAPSHOT.yml"

# Documents to scan (only project docs are relevant for Phase 2)
SCAN_SCOPE = [
    "project/PROJECT_REGISTRY.md",
    "project/ALIGNMENT_MATRIX.md",
    "project/HIGH_LEVEL_DESIGN.md",
    "project/LOW_LEVEL_DESIGN.md",
    "project/USECASES.md",
    "project/USECASES_GAP_ANALYSIS.md",
    "project/FUTURE_ENHANCEMENTS.md",
    # add other project-level indices as needed
]

# only consider registered artifacts whose path starts with this prefix
PROJECT_PREFIX = "project/"

# Exclude patterns (regex) for registered files that are noise and should not be considered
# e.g. logs, temporary files, audit artifacts you don't want in alignment checks
DEFAULT_EXCLUDE_PATTERNS = [
    r"^project/logs/",       # project logs (ACTIVITY, SESSION_LOG, CURRENT_STATE)
    r"^project/archive/",    # archived docs are out of scope
    r"^project/reports/",    # reports docs are out of scope
]

# Minimum inbound links to consider something as "meaningful" (helps filter noise)
MIN_INBOUND_LINKS = 1

# Behavior thresholds for --enforce
DEFAULT_COVERAGE_THRESHOLD = 95  # require 95% aligned or partial coverage
DEFAULT_MAX_ORPHANS_RATIO = 0.03  # allow up to 3% orphans

# ---------------------------------------------------------------------------

def load_trace_index() -> List[dict]:
    if not TRACE_INDEX_PATH.exists():
        print(f"ERROR: TRACE_INDEX.yml not found at {TRACE_INDEX_PATH}", file=sys.stderr)
        sys.exit(1)
    raw = yaml.safe_load(TRACE_INDEX_PATH.read_text(encoding="utf-8")) or {}
    return raw.get("artifacts", [])  # list of artifact dicts

def filter_project_registered(artifacts: List[dict]) -> Dict[str, dict]:
    """
    Return a dict path -> metadata for registered, non-exempt artifacts that live under project/.
    """
    out = {}
    for item in artifacts:
        path = item.get("path")
        if not path:
            continue
        # only project files (Phase 2 scope)
        if not path.startswith(PROJECT_PREFIX):
            continue
        if item.get("type") == "exempt":
            continue
        if not item.get("registered", False):
            continue
        out[path] = {
            "index": item.get("index", "N/A"),
            "description": item.get("description", "") or "",
            "raw": item,
        }
    return out

def compile_master_pattern(paths: List[str]) -> re.Pattern:
    """
    Build a regex that matches either basename or full path occurrences.
    Longer patterns first to avoid partial matches.
    """
    parts = set()
    for p in paths:
        parts.add(re.escape(Path(p).as_posix()))
        parts.add(re.escape(Path(p).name))
    # sort by length desc so longer matches get preference
    parts_list = sorted(parts, key=len, reverse=True)
    if not parts_list:
        # safe fallback
        return re.compile(r"$^")
    return re.compile("|".join(parts_list))

def build_cross_references(registered: Dict[str, dict]) -> Dict[str, Set[str]]:
    """
    Scan SCAN_SCOPE files and return a map: source_doc -> set(target_paths)
    Only project docs are scanned (SCAN_SCOPE contains project docs).
    """
    print("Building reference graph (project scope)...")
    cross_ref = defaultdict(set)
    registered_paths = list(registered.keys())
    pattern = compile_master_pattern(registered_paths)

    link_count = 0
    for doc_rel in SCAN_SCOPE:
        doc_path = PROJECT_ROOT / doc_rel
        if not doc_path.exists():
            continue
        content = doc_path.read_text(encoding="utf-8")
        matches = set(pattern.findall(content))
        for m in matches:
            # resolve to first registered path that endswith the matched token
            found = next((p for p in registered_paths if p.endswith(m)), None)
            if found and found != doc_rel:
                cross_ref[doc_rel].add(found)
                link_count += 1
    print(f"Cross-links found: {link_count}")
    return cross_ref

def apply_exclude_filters(registered: Dict[str, dict], exclude_patterns: List[str]) -> Dict[str, dict]:
    """Remove any registered items whose path matches any exclude regex."""
    compiled = [re.compile(p) for p in exclude_patterns]
    out = {}
    for path, meta in registered.items():
        if any(pat.search(path) for pat in compiled):
            continue
        out[path] = meta
    return out

def invert_cross_ref(cross_ref: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Return target_path -> set(sources)"""
    inverted = defaultdict(set)
    for src, targets in cross_ref.items():
        for t in targets:
            inverted[t].add(src)
    return inverted

def evaluate_alignment(registered: Dict[str, dict], cross_ref: Dict[str, Set[str]], min_inbound: int) -> List[dict]:
    """
    Evaluate alignment for each registered project file. Returns list of result dicts.
    Status semantics:
     - ✅ Aligned: has at least min_inbound links AND linked from design (HLD/LLD) AND alignment matrix
     - ⚠️ Partial: referenced but missing one or more design/trace links
     - ❌ Orphan: not referenced anywhere
     - ⛔ Excluded: filtered out (should not appear since filtered earlier)
    """
    print("Validating file alignment...")
    inverted = invert_cross_ref(cross_ref)
    results = []
    for path, meta in registered.items():
        notes = []
        status = "✅ Aligned"
        sources = sorted(list(inverted.get(path, set())))
        inbound = len(sources)

        # design links: check if any of the design docs mention path
        linked_in_design = any(path in cross_ref.get(doc, set()) for doc in ("project/HIGH_LEVEL_DESIGN.md", "project/LOW_LEVEL_DESIGN.md"))
        linked_in_trace = any(path in cross_ref.get(doc, set()) for doc in ("project/ALIGNMENT_MATRIX.md",))
        linked_in_usecase = any(path in cross_ref.get(doc, set()) for doc in ("project/USECASES.md", "project/USECASES_GAP_ANALYSIS.md"))

        if inbound < 1:
            status = "❌ Orphan"
            notes.append("Not referenced anywhere")
        else:
            # inbound exists
            if inbound < min_inbound:
                notes.append(f"Low inbound links ({inbound} < {min_inbound})")
                # keep as partial unless other conditions met
            if not linked_in_design:
                notes.append("Missing Design link (HLD/LLD)")
            if not linked_in_trace:
                notes.append("Missing Trace link (ALIGNMENT_MATRIX.md)")

            if notes:
                # if there's at least one inbound link but missing design/trace -> partial
                status = "⚠️ Partial"

        results.append({
            "file": path,
            "index": meta.get("index", "N/A"),
            "description": meta.get("description", "") or "",
            "linked_in": sources[0] if sources else "—",
            "link_count": inbound,
            "status": status,
            "notes": "; ".join(notes) if notes else "Referenced in other docs"
        })
    return sorted(results, key=lambda r: r["file"])

def generate_content_report(results: List[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Content Alignment Report\n",
        "| File | Registered In | Linked In | Link Count | Alignment Status | Notes |",
        "|------|----------------|------------|-------------|------------------|--------|",
    ]
    for r in results:
        lines.append(f"| `{r['file']}` | `{r['index']}` | `{r['linked_in']}` | {r['link_count']} | {r['status']} | {r['notes']} |")
    # summary
    total = len(results)
    aligned = sum(1 for r in results if r["status"] == "✅ Aligned")
    partial = sum(1 for r in results if r["status"] == "⚠️ Partial")
    orphans = sum(1 for r in results if r["status"] == "❌ Orphan")
    coverage = int((aligned + partial) / total * 100) if total else 100

    lines.extend([
        "\n## Footer Summary\n",
        f"**Total items:** {total}",
        f"**Fully aligned:** {aligned}",
        f"**Partial:** {partial}",
        f"**Orphans:** {orphans}",
        f"**Alignment coverage:** {coverage}%",
    ])
    CONTENT_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

def generate_description_report(registered: Dict[str, dict]) -> None:
    """
    Very simple description compliance report.
    A description is valid if the TRACE_INDEX 'description' is non-empty OR
    the index (the registered file's index) contains a description column (not parsed here).
    For Phase 2 we rely on TRACE_INDEX descriptions.
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Description Compliance Report\n",
        "| File | Registered In | Status | Notes |",
        "|------|---------------|--------|-------|",
    ]
    non_compliant = 0
    total = 0
    for path, meta in sorted(registered.items()):
        total += 1
        desc = (meta.get("description") or "").strip()
        if desc:
            lines.append(f"| `{path}` | `{meta.get('index','N/A')}` | ✅ Valid |  |")
        else:
            lines.append(f"| `{path}` | `{meta.get('index','N/A')}` | ⚠️ Missing | Invalid or empty description |")
            non_compliant += 1
    lines.append("\n")
    lines.append(f"**Total entries checked:** {total}")
    lines.append(f"**Non-compliant entries:** {non_compliant}")
    ok_pct = int((total - non_compliant) / total * 100) if total else 100
    lines.append(f"**Overall compliance:** {ok_pct}%")
    DESC_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

def generate_snapshot(registered: Dict[str, dict], results: List[dict]) -> None:
    """
    Produce an ALIGNMENT_INTEGRITY_SNAPSHOT.yml that maps canonical IDs (if present)
    to file paths and their alignment state. Snapshot is machine-readable and intended
    as the Phase-2 baseline for Phase-3 semantic checks.
    """
    snapshot = {
        "phase": "phase-2-lockdown",
        "total_registered": len(registered),
        "items": []
    }
    for r in results:
        item = {
            "path": r["file"],
            "index": r["index"],
            "description": registered.get(r["file"], {}).get("description", ""),
            "status": r["status"],
            "link_count": r["link_count"],
            "notes": r["notes"],
        }
        # if the original TRACE_INDEX provides canonical IDs, include them
        raw = registered.get(r["file"], {}).get("raw", {}) or {}
        if raw.get("meta"):
            # include any meta fields the trace index carried (e.g., ids)
            item["meta"] = raw["meta"]
        snapshot["items"].append(item)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(yaml.safe_dump(snapshot, sort_keys=False), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Phase 2 Content Alignment Check (read-only)")
    parser.add_argument("--scan", action="store_true", help="Run scan and generate reports (default).")
    parser.add_argument("--enforce", action="store_true", help="Enforce thresholds (CI).")
    parser.add_argument("--min-inbound", type=int, default=MIN_INBOUND_LINKS, help="Minimum inbound links to consider meaningful.")
    parser.add_argument("--exclude", action="append", default=None, help="Additional exclude regex (repeatable).")
    parser.add_argument("--coverage-threshold", type=int, default=DEFAULT_COVERAGE_THRESHOLD, help="Coverage percent required to pass enforcement.")
    parser.add_argument("--max-orphans-ratio", type=float, default=DEFAULT_MAX_ORPHANS_RATIO, help="Max allowed orphans ratio to pass enforcement.")
    args = parser.parse_args()

    # default to scan if nothing specified
    if not args.scan and not args.enforce:
        args.scan = True

    artifacts = load_trace_index()
    registered_all = filter_project_registered(artifacts)

    # merge default excludes with any provided on CLI
    excludes = list(DEFAULT_EXCLUDE_PATTERNS)
    if args.exclude:
        excludes.extend(args.exclude)

    registered = apply_exclude_filters(registered_all, excludes)
    cross_ref = build_cross_references(registered)
    results = evaluate_alignment(registered, cross_ref, args.min_inbound)

    # write reports
    generate_content_report(results)
    generate_description_report(registered)
    generate_snapshot(registered, results)

    # summary for CLI
    total = len(results)
    aligned = sum(1 for r in results if r["status"] == "✅ Aligned")
    partial = sum(1 for r in results if r["status"] == "⚠️ Partial")
    orphans = sum(1 for r in results if r["status"] == "❌ Orphan")
    coverage = int((aligned + partial) / total * 100) if total else 100

    print(f"Wrote {CONTENT_REPORT_PATH}, {DESC_REPORT_PATH}, {SNAPSHOT_PATH}")
    print(f"Summary: total={total} aligned={aligned} partial={partial} orphans={orphans} coverage={coverage}%")

    if args.enforce:
        max_orphans = int(len(results) * args.max_orphans_ratio)
        if coverage < args.coverage_threshold or orphans > max_orphans:
            print("❌ Content alignment enforcement FAILED.")
            print(f"   - coverage {coverage}% < threshold {args.coverage_threshold}%")
            print(f"   - orphans {orphans} > allowed {max_orphans}")
            sys.exit(1)
        else:
            print("✅ Content alignment enforcement PASSED.")
            sys.exit(0)

if __name__ == "__main__":
    main()
