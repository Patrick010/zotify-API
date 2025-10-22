#!/usr/bin/env python3
"""
generate_alignment_audit_report.py

Unified audit and alignment verification tool.
Performs governance checks, trace index validation,
and cross-domain consistency checks for documentation,
code, configuration, and metadata alignment.

Replaces audit_governance_report.py.
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from datetime import datetime


# --- Core Runner ---

def main():
    base_dir = Path(__file__).resolve().parent.parent
    report_data = {}

    # Step 1: Governance Audit
    report_data["governance"] = perform_governance_audit(base_dir)

    # Step 2: Alignment Verification
    report_data["alignment"] = perform_alignment_verification(base_dir)

    # Step 3: Config Discovery (scripts/ directory)
    report_data["config"] = discover_script_config(base_dir / "scripts")

    # Step 4: Inline Config Extraction
    report_data["config_vars"] = extract_inline_config(base_dir / "scripts")

    # Step 5: Report Generation
    report = render_report(report_data)
    save_report(base_dir, report)
    print(report)

    # Step 6: Exit with code for CI enforcement
    if any(section.get("status") == "fail" for section in report_data.values()):
        sys.exit(2)
    elif any(section.get("status") == "warn" for section in report_data.values()):
        sys.exit(1)
    else:
        sys.exit(0)


# --- Governance Audit ---

def perform_governance_audit(root):
    issues = []
    result = {"status": "pass", "issues": []}

    try:
        trace_index_path = root / "project" / "reports" / "TRACE_INDEX.yml"
        if not trace_index_path.exists():
            issues.append("TRACE_INDEX.yml missing.")
        else:
            with open(trace_index_path, "r") as f:
                trace_index = yaml.safe_load(f) or {}
            for entry in trace_index.get("files", []):
                if "type" not in entry or not entry.get("id"):
                    issues.append(f"Incomplete trace entry: {entry}")
    except Exception as e:
        issues.append(f"Error reading trace index: {e}")

    if issues:
        result["status"] = "fail"
        result["issues"] = issues
    return result


# --- Alignment Verification ---

def perform_alignment_verification(root):
    issues = []
    result = {"status": "pass", "issues": []}

    matrix_file = root / "project" / "ALIGNMENT_MATRIX.md"
    rules_file = root / "scripts" / "doc-lint-rules.yml"

    if not matrix_file.exists():
        issues.append("ALIGNMENT_MATRIX.md not found.")
    else:
        try:
            with open(matrix_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                if not line.strip().startswith("|"):
                    continue
                parts = [x.strip() for x in line.split("|") if x.strip()]
                if len(parts) < 4:
                    issues.append(f"Malformed alignment entry: {line.strip()}")
        except Exception as e:
            issues.append(f"Error parsing alignment matrix: {e}")

    if not rules_file.exists():
        issues.append("doc-lint-rules.yml missing or inaccessible.")

    if issues:
        result["status"] = "fail"
        result["issues"] = issues
    return result


# --- Config Discovery (Script List) ---

def discover_script_config(script_dir):
    result = {"status": "pass", "issues": [], "found": []}
    if not script_dir.exists():
        result["status"] = "warn"
        result["issues"].append("No scripts/ directory found.")
        return result

    for file in script_dir.glob("*.py"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            if any(keyword in content for keyword in ["ignore", "config", "settings", "rules"]):
                result["found"].append(file.name)
        except Exception as e:
            result["issues"].append(f"Error reading {file.name}: {e}")

    if not result["found"]:
        result["status"] = "warn"
    return result


# --- Inline Config Extraction ---

def extract_inline_config(script_dir):
    result = {"status": "pass", "issues": [], "variables": {}}
    if not script_dir.exists():
        result["status"] = "warn"
        result["issues"].append("No scripts/ directory found.")
        return result

    pattern = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(\[.*?\]|\{.*?\})", re.DOTALL)

    for file in script_dir.glob("*.py"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            matches = pattern.findall(content)
            for var, val in matches:
                # Only include likely config arrays
                if any(x in var.lower() for x in ["ignore", "config", "setting", "rule", "path", "dir", "file"]):
                    result["variables"].setdefault(file.name, {})[var] = val.strip()
        except Exception as e:
            result["issues"].append(f"Error parsing {file.name}: {e}")

    if not result["variables"]:
        result["status"] = "warn"
    return result


# --- Report Renderer ---

def render_report(data):
    out = []
    out.append("# Alignment and Governance Audit Report\n")
    out.append(f"Generated: {datetime.now().isoformat()}\n")

    for section, info in data.items():
        out.append(f"## {section.capitalize()}\n")
        out.append(f"**Status:** {info.get('status', 'unknown')}\n")
        if info.get("issues"):
            out.append("**Issues:**")
            for issue in info["issues"]:
                out.append(f"- {issue}")
        if info.get("found"):
            out.append("**Detected Scripts with Config Keywords:**")
            for ref in info["found"]:
                out.append(f"- {ref}")
        if info.get("variables"):
            out.append("**Inline Config Variables:**")
            for file, vars_dict in info["variables"].items():
                out.append(f"- {file}")
                for var, val in vars_dict.items():
                    out.append(f"  - `{var}` = {val}")
        out.append("")

    return "\n".join(out)


# --- Save Report ---

def save_report(root, report_text):
    report_path = root / "project" / "reports" / "ALIGNMENT_AUDIT_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)


# --- Entry Point ---

if __name__ == "__main__":
    main()
