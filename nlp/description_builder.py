import yaml
import json
from pathlib import Path
import ast
from summarizer import summarize_doc, summarize_code_nlp  # updated NLP summarizer that handles outputs

# Paths (adjust for testing vs production)
TRACE_INDEX_PATH = Path("scripts/TRACE_INDEX_test.yml")
INTERMEDIATE_JSON = Path("scripts/trace_description_test.json")

# Verbs indicating output-generating functions
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
                    # Attempt to infer result/output name
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

def generate_descriptions():
    with open(TRACE_INDEX_PATH, "r", encoding="utf-8") as f:
        trace_data = yaml.safe_load(f)

    artifacts = trace_data.get("artifacts", [])
    updated_artifacts = []

    for entry in artifacts:
        file_path = Path(entry["file"])
        ftype = entry.get("type", "code")
        entry.setdefault("meta", {})

        if ftype == "doc":
            description = summarize_doc(file_path)
        else:
            # Detect outputs and generate NLP description
            outputs = detect_code_outputs(file_path)
            description = summarize_code_nlp(file_path, outputs)

        # Validate description is meaningful
        if not description or description.strip() in ["", "X", "-", "<!--"]:
            description = "No description available."

        entry["meta"]["description"] = description
        updated_artifacts.append(entry)

    # Write intermediate JSON for inspection
    with open(INTERMEDIATE_JSON, "w", encoding="utf-8") as f:
        json.dump({"artifacts": updated_artifacts}, f, indent=4)

    print(f"Updated descriptions written to {INTERMEDIATE_JSON}")

if __name__ == "__main__":
    generate_descriptions()
