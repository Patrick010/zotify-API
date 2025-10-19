#!/usr/bin/env python3
"""
summarizer_client.py

Integrated summarizer client for repo_inventory_and_governance.py.
Uses the new summarizer scripts to produce real summaries and tags.
"""

import subprocess
import json
from pathlib import Path
from typing import Tuple, List

# Dynamic import of summarize_tags
from scripts.summarize_tags import generate_tags_from_text as extract_tags


def run_summarizer_script(script_path: Path, content: str) -> str:
    """
    Run a summarizer script (docs or code) via subprocess and return summary text.
    """
    try:
        proc = subprocess.run(
            ["python3", str(script_path)],
            input=content.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        # Expect the script to print the summary to stdout
        return proc.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return f"Error running {script_path.name}: {e.stderr.decode('utf-8')}"


def summarize_file_content(filepath: Path) -> Tuple[str, List[str]]:
    """
    Summarize a single file and generate tags.
    Returns: (summary, tags)
    """
    if not filepath.exists():
        return f"File not found: {filepath}", []

    ext = filepath.suffix.lower()
    content = filepath.read_text(encoding="utf-8")

    # Determine which summarizer to use
    if ext in (".py", ".js", ".go", ".sh", ".ts"):
        script_path = Path(__file__).resolve().parent.parent / "scripts" / "summarize_code.py"
    elif ext in (".md", ".txt", ".rst"):
        script_path = Path(__file__).resolve().parent.parent / "scripts" / "summarize_docs.py"
    else:
        return f"Unrecognized file type ({ext}) – skipped.", []

    # Run summarizer
    summary = run_summarizer_script(script_path, content)
    tags = extract_tags(summary)
    return summary, tags


class SummarizerClient:
    """Wrapper to summarize files and generate tags."""

    def summarize_file(self, filepath: str) -> dict:
        filepath_obj = Path(filepath)
        summary, tags = summarize_file_content(filepath_obj)
        return {
            "file": filepath,
            "description": summary,
            "tags": tags,
        }

    def batch_summarize(self, files: list[str]) -> list[dict]:
        return [self.summarize_file(f) for f in files]


# --- CLI entrypoint for testing ---
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python summarizer_client.py <file1> [file2 ...]")
        sys.exit(1)

    client = SummarizerClient()
    results = client.batch_summarize(sys.argv[1:])
    for r in results:
        print("\n=== Summary ===")
        print(f"File: {r['file']}")
        print(f"Description: {r['description']}")
        print(f"Tags: {r['tags'][:15]}")
