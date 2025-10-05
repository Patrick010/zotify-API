#!/usr/bin/env python3
import os
import re
import yaml

OUTPUT_PATH = "project/reports/DESCRIPTION_COMPLIANCE_REPORT.md"
PLACEHOLDER_PATTERN = re.compile(r"^(|N/A|TBD|temp|none|null)$", re.IGNORECASE)

def is_invalid(desc):
    if not desc or not desc.strip():
        return True
    if PLACEHOLDER_PATTERN.match(desc.strip()):
        return True
    if len(desc.strip().splitlines()) > 1:
        return True
    return False

def check_trace_index(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    results = []
    artifacts = data.get("artifacts", [])
    for entry in artifacts:
        desc = entry.get("description", "")
        status = "✅ Valid"
        notes = ""
        if is_invalid(desc):
            status = "⚠️ Missing"
            notes = "Invalid or empty description"
        results.append((path, entry.get("path", "Unknown"), status, notes))
    return results

def check_md_index(path):
    results = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    header_found = False
    for line in lines:
        if not header_found:
            if re.match(r"^\|.*\|", line) and "description" in line.lower():
                header_found = True
            continue
        if re.match(r"^\|.*\|", line):
            cols = [c.strip() for c in line.strip().split("|")[1:-1]]
            if len(cols) < 2:
                continue
            file_name = cols[0]
            desc = cols[-1]
            status = "✅ Valid"
            notes = ""
            if is_invalid(desc):
                status = "⚠️ Missing"
                notes = "Invalid or empty description"
            results.append((path, file_name, status, notes))
    return results

def main():
    all_results = []
    for root, _, files in os.walk("."):
        for file in files:
            if file == "TRACE_INDEX.yml" and "project/reports" in root:
                all_results.extend(check_trace_index(os.path.join(root, file)))
            elif file == "CODE_FILE_INDEX.md":
                all_results.extend(check_md_index(os.path.join(root, file)))
            elif file == "PROJECT_REGISTRY.md" and "project" in root:
                all_results.extend(check_md_index(os.path.join(root, file)))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("| File | Entry | Status | Notes |\n")
        f.write("|------|--------|---------|--------|\n")
        for path, entry, status, notes in all_results:
            f.write(f"| {path} | {entry} | {status} | {notes} |\n")

        total = len(all_results)
        missing = sum(1 for _, _, s, _ in all_results if "⚠️" in s)
        compliance = 100 - int((missing / total) * 100) if total else 100
        f.write(f"\n**Total entries checked:** {total}\n")
        f.write(f"**Missing/Invalid descriptions:** {missing}\n")
        f.write(f"**Overall compliance:** {compliance}%\n")

if __name__ == "__main__":
    main()