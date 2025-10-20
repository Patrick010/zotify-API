#!/usr/bin/env python3
"""
Role-focused document summarizer using Cohere v2 Chat API.

Generates a concise 1–2 sentence description of a document's role, responsibilities, and purpose.
Self-reference phrases and introductions are removed.
"""

import os
import logging
import requests
from dotenv import load_dotenv

# ------------------------------
# Environment
# ------------------------------
load_dotenv()
COHERE_KEY = os.getenv("COHERE_API_KEY")
COHERE_URL = "https://api.cohere.ai/v2/chat"

logger = logging.getLogger("summarizer_client")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ------------------------------
# Client
# ------------------------------
class SummarizerClient:
    def __init__(self):
        if not COHERE_KEY:
            raise ValueError("COHERE_API_KEY is missing from environment variables.")

    def summarize_doc(self, text: str) -> str:
        """
        Returns a concise (1–2 sentences) description of the document's role and responsibilities,
        avoiding any self-reference or introductory clauses.
        """
        prompt = f"""Generate a concise 1–2 sentence description of the document's role, responsibilities, and purpose within the project. 
Do NOT include any self-reference phrases (e.g., "This document…" or "This matrix…") or introductory clauses (e.g., "The purpose of this document is…"). 
Do NOT include project names or references to the document itself. 
Focus purely on what the document defines, enables, or governs in terms of processes, features, or requirements.

Document:
{text}

Role description:"""

        payload = {
            "model": "command-r-plus-08-2024",
            "messages": [
                {"role": "system", "content": "You are an assistant that produces concise, informative role descriptions of project documents without self-reference."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 200,
        }

        headers = {"Authorization": f"Bearer {COHERE_KEY}", "Content-Type": "application/json"}

        try:
            resp = requests.post(COHERE_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            # Handle Chat API v2 response
            if "message" in data and "content" in data["message"]:
                content_list = data["message"]["content"]
                summary = " ".join(item.get("text", "") for item in content_list if item.get("type") == "text").strip()
                return summary
            elif "generations" in data:
                content_list = data["generations"][0]["message"]["content"]
                summary = " ".join(item.get("text", "") for item in content_list if item.get("type") == "text").strip()
                return summary
            else:
                logger.error(f"Unexpected response format: {data}")
                return ""

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during API request: {e}")
            return ""
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Unexpected response format: {data} ({e})")
            return ""


# ------------------------------
# Convenience function
# ------------------------------
def summarize_text(text: str) -> str:
    client = SummarizerClient()
    return client.summarize_doc(text)


# ------------------------------
# CLI interface
# ------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: summarizer_client.py <path_to_document>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    summary = summarize_text(text)
    print("\n--- CONCISE ROLE DESCRIPTION ---\n")
    print(summary)
