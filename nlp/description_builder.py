#!/usr/bin/env python3
import yaml
import json
from pathlib import Path
import ast
from nlp.summarizer import summarize_doc, summarize_code

# Paths for intermediate outputs (adjust if needed)
TRACE_INDEX_PATH = Path("scripts/TRACE_INDEX.yml")
INTERMEDIATE_JSON = Path("scripts/trace_description_intermediate.json")

# Verbs indicating output-generating functions in Python code
OUTPUT_VERBS = ["generate", "create", "build", "export", "save", "write", "produce"]

def detect_code_outputs(file_path: Path):
    """
    Parse Python code to detect output-generating functions and potential outputs.
    Returns a list of output descriptors (filenames, objects, reports).
    """
    outputs = []
    if not file_path.exists() or file_path.suffix != ".py":
        return outputs

    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                fname = node.name.lower()
                if any(v in fname for v in OUTPUT_VERBS):
                    returns = []
                    for n in ast.walk(node):
                        if isinstance(n, ast.Return) and isinstance(n.value, ast.Str):
                            returns.append(n.value.s)
                        elif isinstance(n, ast.Assign) and isinstance(n.value, ast.Str):
                            returns.append(n.value.s)
                    output_summary = ", ".join(returns) if returns else "an output"
                    outputs.append(f"{fname} -> {output_summary}")
    except Exception as e:
        print(f"[WARN] Failed to parse {file_path}: {e}")
    return outputs

def build_description_for_artifact(file_path: Path, file_type: str) -> str:
    """
    Generate a safe NLP description for a given artifact.
    Reads file content as string before summarization.
    """
    if not file_path or not file_path.exists():
        return "File not found"

    try:
        if file_type == "doc" or file_path.suffix.lower() in [".md", ".txt"]:
            text = file_path.read_text(encoding="utf-8")
            description = summarize_doc(text)
        elif file_type == "code" or file_path.suffix.lower() in [".py", ".go", ".js"]:
            code = file_path.read_text(encoding="utf-8")
            outputs = detect_code_outputs(file_path) if file_path.suffix == ".py" else []
            description = summarize_code(code)
        else:
            description = "No description available"

        if not description or description.strip() in ["", "X", "-", "<!--"]:
            description = "No description available."

        return description
    except Exception as e:
        return f"Error processing file: {e}"

def generate_descriptions_from_trace_index(trace_index_path: Path = TRACE_INDEX_PATH,
                                           output_json: Path = INTERMEDIATE_JSON):
    """
    Load artifacts from TRACE_INDEX.yml, generate NLP descriptions,
    and save results to JSON.
    """
    if not trace_index_path.exists():
        print(f"❌ Trace index not found at {trace_index_path}")
        return

    with open(trace_index_path, "r", encoding="utf-8") as f:
        trace_data = yaml.safe_load(f)

    artifacts = trace_data.get("artifacts", [])
    if not artifacts:
        print("⚠️ No artifacts found in TRACE_INDEX.yml.")
        return

    updated_artifacts = []
    failures = 0
    from tqdm import tqdm

    for entry in tqdm(artifacts, desc="Generating descriptions", unit="file"):
        file_path_str = entry.get("file")
        ftype = entry.get("type", "code")
        entry.setdefault("meta", {})

        if not file_path_str:
            failures += 1
            continue

        abs_path = Path(file_path_str)
        description = build_description_for_artifact(abs_path, ftype)
        if description.startswith("Error"):
            failures += 1

        entry["meta"]["description"] = description
        updated_artifacts.append(entry)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"artifacts": updated_artifacts}, f, indent=4)

    print(f"\n💾 Descriptions written to {output_json} ({len(updated_artifacts)} artifacts, {failures} failures)")

if __name__ == "__main__":
    generate_descriptions_from_trace_index()
