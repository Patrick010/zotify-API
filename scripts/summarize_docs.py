#!/usr/bin/env python3
"""
Summarize project documentation files using Groq API.
Produces exactly 1 sentence (~15-25 words) with unique verb starters for the document's role.
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
import time

# Setup
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DOC_DIR = ROOT / "project"
MAX_TOKENS = 30  # ~15-25 words
MAX_RETRIES = 3  # Retry attempts for 429 errors

if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY not found in environment.")
    sys.exit(1)

# Prompt Template (refined for unique verb starters)
PROMPT_TEMPLATE = """
Generate exactly 1 sentence (15-25 words) in active voice describing the document's role, responsibilities, or purpose within the project, strictly using a unique starting verb per document from establishes, directs, manages, guides, ensures, regulates, or governs to avoid repetitive verb patterns across outputs.
Do NOT use the same starting verb across multiple documents.
Do NOT include self-reference phrases (e.g., "This document", "The document", "The matrix", "The policy", "This file").
Do NOT include introductory clauses (e.g., "The purpose is") or project names (e.g., "Zotify", "Spotify").
Do NOT include content details (e.g., playlists, audio, audio handling, music, music management, logging, logging scenarios, logging requirements, operations, synchronization, or specific features).
Focus purely on generic role descriptions for project processes or requirements.
Document:
{content}
Role description:
"""

# Summarize function
def summarize_doc(content: str, retries=0) -> str:
    content = content.replace("\0", "").strip()[:100000]  # Truncate to fit context
    prompt = PROMPT_TEMPLATE.format(content=content)
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Produce exactly 1 sentence (15-25 words) in active voice on the document's role, strictly using a unique starting verb (e.g., establishes, directs, manages, guides, ensures, regulates, governs) per document, avoiding repeated verbs across outputs, self-references, project names, content details (e.g., playlists, audio, music, music management, logging, logging requirements, operations, synchronization), and verbs like 'defines', 'outlines', 'describes'."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,  # Lowered for stricter adherence
        "max_tokens": MAX_TOKENS,
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        summary = result["choices"][0]["message"]["content"].strip()
        # Trim to first sentence, cap at 25 words
        sentences = summary.split('.', 1)
        final_summary = sentences[0].strip() + "." if sentences else summary.strip()
        words = final_summary.split()
        if len(words) > 25:
            final_summary = ' '.join(words[:25]) + "."
        return final_summary if final_summary else "[No summary returned]"
    except requests.RequestException as e:
        if hasattr(e, 'response') and e.response and e.response.status_code == 429 and retries < MAX_RETRIES:
            retry_after = float(e.response.headers.get("Retry-After", 60))
            print(f"429 error, retrying after {retry_after:.1f}s...")
            time.sleep(retry_after)
            return summarize_doc(content, retries + 1)
        return f"[Error: {e}]"
    except Exception as e:
        return f"[Unexpected: {e}]"

# Helper
def get_doc_files(directory: Path):
    extensions = (".md", ".rst", ".txt")
    return [f for f in directory.rglob("*") if f.is_file() and f.suffix in extensions]

# Main
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Summarize documentation files using Groq.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(DOC_DIR),
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
    
    if target.is_dir():
        files = get_doc_files(target)
        if not files:
            print("No documentation files found.")
            return
    else:
        if target.suffix not in (".md", ".rst", ".txt"):
            print(f"Invalid file type: {target.suffix}. Must be .md, .rst, or .txt.")
            sys.exit(1)
        files = [target]
    
    files = files[:args.max_files]
    print(f"Summarizing {len(files)} document(s)...\n")
    for file_path in tqdm(files, desc="Processing files", unit="file"):
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            print(f"\n=== {file_path} ===\n")
            summary = summarize_doc(content)
            print(summary or "[No summary returned]")
            time.sleep(3.0)  # ~20 RPM, avoids 429s
        except Exception as e:
            print(f"[Error processing {file_path}]: {e}")

if __name__ == "__main__":
    main()