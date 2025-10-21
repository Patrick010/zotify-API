#!/usr/bin/env python3
"""
summarize_tags.py

Generate semantic tags from a summary text using NLP.
This script uses POS (Part-of-Speech) tagging to identify meaningful keywords.
"""

import sys
import spacy
from nltk.corpus import stopwords
from collections import Counter

# ------------------------------
# NLP setup
# ------------------------------
try:
    nlp_pos = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words("english"))
except (OSError, ImportError):
    print("NLP models not found. Please run:")
    print("pip install spacy nltk")
    print("python -m spacy download en_core_web_sm")
    print("python -c \"import nltk; nltk.download('stopwords')\"")
    sys.exit(1)

# ------------------------------
# Tag generation
# ------------------------------
def generate_tags_from_summary(summary_text: str, top_k: int = 10) -> list[str]:
    """
    Returns top_k tags from a given summary text using POS tagging.
    """
    if not summary_text:
        return []

    summary_text = summary_text.lower()
    doc = nlp_pos(summary_text)

    # Extract tokens that are nouns, proper nouns, or verbs, and are not stopwords.
    tokens = [
        tok.text
        for tok in doc
        if tok.pos_ in {"NOUN", "PROPN", "VERB"} and tok.text not in stop_words
    ]

    # Calculate frequency and return the most common tags.
    if not tokens:
        return []

    freq = Counter(tokens)
    most_common_tags = [tag for tag, count in freq.most_common(top_k)]
    return most_common_tags

# ------------------------------
# CLI for testing
# ------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If an argument is provided, use it as the summary.
        summary = sys.argv[1]
        top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    else:
        # Otherwise, read from stdin for easy piping.
        print("Reading from stdin... Press Ctrl+D to finish.", file=sys.stderr)
        summary = sys.stdin.read()
        top_k = 10

    if not summary.strip():
        print("No summary text provided.", file=sys.stderr)
        sys.exit(1)

    tags = generate_tags_from_summary(summary, top_k=top_k)
    print(",".join(tags))
