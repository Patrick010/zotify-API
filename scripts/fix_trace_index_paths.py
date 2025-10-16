#!/usr/bin/env python3
import yaml
from pathlib import Path

TRACE_INDEX_FILE = Path("project/reports/TRACE_INDEX.yml")

with TRACE_INDEX_FILE.open("r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

def replace_path_with_file(item):
    if isinstance(item, dict):
        if "path" in item:
            item["file"] = item.pop("path")
        for v in item.values():
            replace_path_with_file(v)
    elif isinstance(item, list):
        for elem in item:
            replace_path_with_file(elem)

replace_path_with_file(data)

with TRACE_INDEX_FILE.open("w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print(f"Replaced all 'path:' keys with 'file:' in {TRACE_INDEX_FILE}")
