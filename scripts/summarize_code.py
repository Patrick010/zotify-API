#!/usr/bin/env python3
"""
Summarize all code files in a directory or single file using Groq Llama 3.1.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm

# Ensure repo root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

load_dotenv(ROOT / ".env")

from nlp.summarizer_client import summarize_code_text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Summarize code files.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(ROOT / "api/src/zotify_api"),
        help="Path to code folder or single file",
    )
    parser.add_argument(
        "--max-files", type=int, default=10, help="Maximum files to process"
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    if target.is_dir():
        files = list(target.rglob("*.py")) + list(target.rglob("*.js")) + list(target.rglob("*.ts"))
        if not files:
            print("No code files found.")
            return
    else:
        files = [target]

    files = files[: args.max_files]

    print(f"Summarizing {len(files)} code file(s)...\n")

    for file_path in tqdm(files, desc="Processing files", unit="file"):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        print(f"\n=== {file_path} ===\n")
        summary = summarize_code_text(code)
        print(summary or "[No summary returned]")


if __name__ == "__main__":
    main()
