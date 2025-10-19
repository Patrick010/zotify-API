#!/usr/bin/env python3
"""
Summarize project documentation using Cohere Command R+ via nlp/summarizer_client.py
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm  # Progress bar

# Ensure repo root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

# Load environment variables
load_dotenv(ROOT / ".env")

# Import the summarizer client
from nlp.summarizer_client import summarize_text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Summarize documentation files.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(ROOT / "project"),
        help="Path to documentation folder or file (default: project/)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=5,
        help="Maximum number of files to process (default: 5)",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    # Collect all markdown or txt files if directory
    if target.is_dir():
        files = list(target.rglob("*.md")) + list(target.rglob("*.txt"))
        if not files:
            print("No documentation files found.")
            return
    else:
        files = [target]

    # Limit to max-files
    files = files[: args.max_files]

    print(f"Summarizing {len(files)} document(s)...\n")

    for file_path in tqdm(files, desc="Processing files", unit="file"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"\n=== {file_path} ===\n")
        summary = summarize_text(content)
        print(summary or "[No summary returned]")


if __name__ == "__main__":
    main()
