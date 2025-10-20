#!/usr/bin/env python3
"""
Summarize Python code files using GROQ Chat API with chunking for large files.
- Truncates or splits large files to avoid 400 Bad Request errors.
- Preserves full prompt requirements.
"""
import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from tqdm import tqdm
import math
import time

# ----------------------------
# Setup
# ----------------------------
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
CODE_DIR = ROOT / "api/src/zotify_api"
MAX_TOKENS = 150
MAX_CHARS = 1500  # ~375 tokens, conservative for 8k limit

if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY not found in environment.")
    sys.exit(1)

# ----------------------------
# Prompt Template
# ----------------------------
PROMPT_TEMPLATE = """
You are a helpful developer assistant. Summarize the following Python code file in 1-3 sentences.
Requirements:
- Friendly, conversational tone, like explaining to a teammate.
- Focus on what the code actually does, not just literal syntax or imports.
- Mention important side effects, interactions, or state changes.
- Be concise, avoid filler and boilerplate descriptions.
- Do not include introductions like "This document..." or "The file contains..."
Python code:
{code}
"""

# ----------------------------
# Client function
# ----------------------------
def summarize_code_chunk(code_chunk: str) -> str:
    code_chunk = code_chunk.replace("\0", "").replace('"', '\\"').replace('\n', '\\n').strip()[:MAX_CHARS]
    prompt = PROMPT_TEMPLATE.format(code=code_chunk)
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a helpful developer assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
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
        
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"]["content"].strip()
            return content if content else "[No summary returned]"
        return "[No summary returned]"
    
    except requests.RequestException as e:
        error_msg = f"[Error during API request: {e}]"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f" [Details: {error_detail.get('error', {}).get('message', 'Unknown')}]"
            except:
                error_msg += f" [Raw: {e.response.text[:200]}...]"
        return error_msg
    except Exception as e:
        return f"[Unexpected response format: {e}]"

# ----------------------------
# Summarize a whole file safely
# ----------------------------
def summarize_code_file(code: str) -> str:
    code = ''.join(c for c in code if ord(c) < 128).replace("\0", "").strip()
    if len(code) <= MAX_CHARS:
        return summarize_code_chunk(code)
    
    summaries = []
    num_chunks = math.ceil(len(code) / MAX_CHARS)
    for i in range(num_chunks):
        chunk = code[i * MAX_CHARS: (i + 1) * MAX_CHARS]
        summary = summarize_code_chunk(chunk)
        summaries.append(summary)
        time.sleep(2)  # Avoid rate limits
    return " ".join(summaries)

# ----------------------------
# Helper
# ----------------------------
def get_python_files(directory: Path):
    return [f for f in directory.rglob("*.py") if f.is_file()]

# ----------------------------
# Main
# ----------------------------
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Summarize Python code files.")
    parser.add_argument(
        "path",
        nargs="?",
        default=str(CODE_DIR),
        help="Path to code folder (default: api/src/zotify_api/)"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=10,
        help="Maximum number of files to process (default: 10)"
    )
    args = parser.parse_args()
    code_dir = Path(args.path)
    if not code_dir.exists():
        print(f"Path not found: {code_dir}")
        sys.exit(1)
    files = get_python_files(code_dir)
    if not files:
        print("No Python files found.")
        return
    files = files[:args.max_files]
    print(f"Summarizing {len(files)} Python file(s)...\n")
    for file_path in tqdm(files, desc="Processing files", unit="file"):
        try:
            code_content = file_path.read_text(encoding="utf-8", errors="replace")
            print(f"\n=== {file_path} ===\n")
            summary = summarize_code_file(code_content)
            print(summary or "[No summary returned]")
        except Exception as e:
            print(f"[Error summarizing {file_path}]: {e}")

if __name__ == "__main__":
    main()