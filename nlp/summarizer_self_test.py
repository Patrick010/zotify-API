#!/usr/bin/env python3
"""
summarizer_self_test.py

Comprehensive regression test for summarizer.py.

Covers:
- Document summarization
- Code summarization
- Validation logic
- generate_description_meta()
- generate_tag_meta()
- Embedding consistency checks
- summarize_file() entrypoint
"""

import json
import sys
import torch
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import summarizer as s

def print_header(title):
    print(f"\n{'='*60}\n{title}\n{'='*60}")

def run_tests():
    results = {}

    # ------------------------------
    # 1. Basic Doc Summarization
    # ------------------------------
    print_header("TEST 1: Document summarization")
    sample_doc = (
        "The Zotify API allows developers to manage Spotify downloads, "
        "perform track analysis, and integrate metadata enrichment."
    )
    summary = s.summarize_doc(sample_doc)
    results["doc_summary"] = summary
    print(f"Summary: {summary}")

    # ------------------------------
    # 2. Code Summarization
    # ------------------------------
    print_header("TEST 2: Code summarization")
    sample_code = (
        "def download_track(track_id):\n"
        "    '''Download a track from Spotify using its ID'''\n"
        "    response = api.get(f'/track/{track_id}')\n"
        "    save_to_disk(response.data)\n"
    )
    code_summary = s.summarize_code(sample_code)
    results["code_summary"] = code_summary
    print(f"Summary: {code_summary}")

    # ------------------------------
    # 3. Validation
    # ------------------------------
    print_header("TEST 3: Validation")
    valid_doc = s.validate_summary(sample_doc, summary)
    valid_code = s.validate_summary(sample_code, code_summary, is_code=True)
    results["validation_doc"] = valid_doc
    results["validation_code"] = valid_code
    print(f"Doc validation passed: {valid_doc}")
    print(f"Code validation passed: {valid_code}")

    # ------------------------------
    # 4. Description Meta Generation
    # ------------------------------
    print_header("TEST 4: generate_description_meta()")
    doc_meta = s.generate_description_meta(sample_doc)
    code_meta = s.generate_description_meta(sample_code, is_code=True)
    results["doc_meta"] = doc_meta
    results["code_meta"] = code_meta
    print(json.dumps({"doc_meta": doc_meta, "code_meta": code_meta}, indent=2))

    # ------------------------------
    # 5. Tag Meta Generation
    # ------------------------------
    print_header("TEST 5: generate_tag_meta()")
    doc_tags = s.generate_tag_meta(sample_doc)
    code_tags = s.generate_tag_meta(sample_code, is_code=True)
    results["doc_tags"] = doc_tags
    results["code_tags"] = code_tags
    print(f"Doc tags: {doc_tags}")
    print(f"Code tags: {code_tags}")

    # ------------------------------
    # 6. Embedding Consistency Check
    # ------------------------------
    print_header("TEST 6: Embedding consistency")
    doc_emb = s.doc_embedder.encode([sample_doc], convert_to_tensor=True)
    code_emb = s.code_embedder.encode([sample_code], convert_to_tensor=True)
    results["embedding_doc_shape"] = tuple(doc_emb.shape)
    results["embedding_code_shape"] = tuple(code_emb.shape)
    print(f"Doc embedding shape: {doc_emb.shape}")
    print(f"Code embedding shape: {code_emb.shape}")

    # ------------------------------
    # 7. File-based summarize_file() test
    # ------------------------------
    print_header("TEST 7: summarize_file() entrypoint")
    with tempfile.TemporaryDirectory() as tmpdir:
        doc_path = Path(tmpdir) / "sample_doc.txt"
        code_path = Path(tmpdir) / "sample_code.py"
        doc_path.write_text(sample_doc, encoding="utf-8")
        code_path.write_text(sample_code, encoding="utf-8")

        doc_summary_file, doc_tags_file = s.summarize_file(doc_path)
        code_summary_file, code_tags_file = s.summarize_file(code_path)
        results["file_doc_summary"] = doc_summary_file
        results["file_doc_tags"] = doc_tags_file
        results["file_code_summary"] = code_summary_file
        results["file_code_tags"] = code_tags_file

        print(f"File Doc Summary: {doc_summary_file}")
        print(f"File Doc Tags: {doc_tags_file}")
        print(f"File Code Summary: {code_summary_file}")
        print(f"File Code Tags: {code_tags_file}")

    # ------------------------------
    # 8. Summary
    # ------------------------------
    print_header("SUMMARY")
    print(json.dumps(results, indent=2))

    # Sanity validations
    if not summary or not code_summary:
        raise AssertionError("Summaries are empty.")
    if not isinstance(doc_tags, list) or not isinstance(code_tags, list):
        raise AssertionError("Tag generation failed.")
    if doc_emb.shape[1] != s.doc_embedder.encode(["test"]).shape[1]:
        raise AssertionError("Doc embedding dimension mismatch.")
    if code_emb.shape[1] != s.code_embedder.encode(["test"], convert_to_tensor=True).shape[1]:
        raise AssertionError("Code embedding dimension mismatch.")

    print("\n✅ All summarizer regression tests passed successfully.")

if __name__ == "__main__":
    torch.set_grad_enabled(False)
    run_tests()
