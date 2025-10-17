#!/usr/bin/env python3
import sys
from pathlib import Path
import json
import yaml
from tqdm import tqdm

# --- Ensure repo root and nlp folder are importable ---
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(repo_root / "nlp"))

from nlp.description_builder import build_description_for_artifact

def generate_descriptions():
    """
    Loads artifacts from TRACE_INDEX.yml, generates NLP descriptions,
    and saves the result to a JSON file.
    """
    trace_index_path = repo_root / "project/reports/TRACE_INDEX.yml"
    output_path = repo_root / "scripts/trace_description_intermediate.json"

    if not trace_index_path.exists():
        print(f"❌ Error: Trace index not found at {trace_index_path}")
        sys.exit(1)

    print("📘 Loading trace index...")
    with open(trace_index_path, "r", encoding="utf-8") as f:
        trace_index = yaml.safe_load(f)

    artifacts = trace_index.get("artifacts", [])
    total = len(artifacts)
    if not artifacts:
        print("⚠️ No artifacts found in TRACE_INDEX.yml.")
        return

    print(f"📦 Found {total} artifacts.")
    descriptions = {}
    failures = 0

    for artifact in tqdm(artifacts, desc="Generating descriptions", unit="file"):
        file_path_str = artifact.get("file")
        file_type = artifact.get("type", "code")

        if not file_path_str:
            failures += 1
            continue

        abs_file_path = repo_root / file_path_str
        description = build_description_for_artifact(abs_file_path, file_type)
        if description.startswith("Error"):
            failures += 1
        descriptions[file_path_str] = description

    # --- Save JSON ---
    print(f"\n💾 Saving updates ({len(descriptions)} files processed)...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=4, ensure_ascii=False)

    print(f"✅ Done.")
    print(f"   - Total processed: {total}")
    print(f"   - Successful: {total - failures}")
    print(f"   - Failures: {failures}")
    print(f"   - Output saved to: {output_path}")


if __name__ == "__main__":
    generate_descriptions()
