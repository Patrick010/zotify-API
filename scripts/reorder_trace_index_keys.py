#!/usr/bin/env python3
import yaml
from pathlib import Path

TRACE_INDEX_FILE = Path("project/reports/TRACE_INDEX.yml")

PREFERRED_ORDER = ["file", "id", "type", "registered", "index", "meta"]

def reorder_dict(d):
    return {k: d[k] for k in PREFERRED_ORDER if k in d}

def reorder_items(item):
    if isinstance(item, list):
        return [reorder_items(i) for i in item]
    elif isinstance(item, dict):
        new_dict = reorder_dict(item)
        # preserve any extra keys not in preferred order
        for k in item:
            if k not in new_dict:
                new_dict[k] = reorder_items(item[k])
            else:
                new_dict[k] = reorder_items(new_dict[k])
        return new_dict
    else:
        return item

with TRACE_INDEX_FILE.open("r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

data = reorder_items(data)

with TRACE_INDEX_FILE.open("w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True)

print(f"Reordered keys in {TRACE_INDEX_FILE} according to preferred order.")
