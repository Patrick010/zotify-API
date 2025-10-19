#!/usr/bin/env python3
"""
Self-test for summarizer.py
Validates doc/code summaries, semantic similarity, and reports cache status
"""

import sys
import time
import statistics
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
import summarizer as sm
import nlp_config as cfg

# Sample inputs
DOC_SAMPLE = """
# Zotify API Manual
The Zotify API provides a backend wrapper around Librespot to allow automation of Spotify downloads,
media metadata synchronization, and playlist management. It exposes endpoints for user configuration,
authentication, and privacy compliance. Each module is isolated and configurable.
"""

ROLE_DOC_SAMPLE = """
# ROADMAP.md
Tracks milestones, feature sets, and progress of the Zotify API implementation.
It defines priorities and next-phase planning for Snitch integration.
"""

CODE_SAMPLE = """
class PlaylistManager:
    def __init__(self, client):
        self.client = client

    def fetch_playlist(self, playlist_id):
        data = self.client.get_playlist(playlist_id)
        return data

    def sync_playlist(self, playlist_id, local_tracks):
        remote = self.fetch_playlist(playlist_id)
        updated = [t for t in local_tracks if t not in remote['tracks']]
        for track in updated:
            self.client.add_to_playlist(playlist_id, track)
        return True
"""

# ------------------------------
# Helpers
# ------------------------------
def safe_summarize_doc(text: str, max_len=40, min_len=10) -> str:
    return sm.summarize_doc(text, max_length=max_len, min_length=min_len)

def print_cache_status():
    print("\n=== MODEL CACHE STATUS ===")
    for k, path in cfg.MODEL_CACHE_DIRS.items():
        status = "HIT" if any(path.glob("**/*")) else "MISS"
        print(f"{k:25}: {status}")

# ------------------------------
# Tests
# ------------------------------
def run_doc_tests():
    print("\n=== DOC SUMMARIZATION TEST ===")
    t0 = time.time()
    doc_summary = safe_summarize_doc(DOC_SAMPLE)
    t1 = time.time()
    role_summary = safe_summarize_doc(ROLE_DOC_SAMPLE)
    t2 = time.time()

    print("Doc summary:", doc_summary)
    print("Role summary:", role_summary)

    valid_doc = sm.validate_summary(DOC_SAMPLE, doc_summary, is_code=False)
    valid_role = sm.validate_summary(ROLE_DOC_SAMPLE, role_summary, is_code=False)

    print(f"Doc validation: {valid_doc}, inference time: {t1-t0:.2f}s")
    print(f"Role validation: {valid_role}, inference time: {t2-t1:.2f}s")

    return {
        "doc_valid": valid_doc,
        "role_valid": valid_role,
        "doc_summary_len": len(doc_summary.split()),
        "role_summary_len": len(role_summary.split())
    }

def run_code_tests():
    print("\n=== CODE SUMMARIZATION TEST ===")
    t0 = time.time()
    summary_basic = sm.summarize_code(CODE_SAMPLE, block_mode=False)
    summary_block = sm.summarize_code(CODE_SAMPLE, block_mode=True)
    t1 = time.time()

    print("Basic code summary:", summary_basic)
    print("Block code summary:", summary_block)

    valid_basic = sm.validate_summary(CODE_SAMPLE, summary_basic, is_code=True)
    valid_block = sm.validate_summary(CODE_SAMPLE, summary_block, is_code=True)

    print(f"Validation (basic): {valid_basic}")
    print(f"Validation (block): {valid_block}")
    print(f"Total code runtime: {t1 - t0:.2f}s")

    return {
        "valid_basic": valid_basic,
        "valid_block": valid_block,
        "summary_basic_len": len(summary_basic.split()),
        "summary_block_len": len(summary_block.split()),
        "runtime_sec": t1 - t0
    }

# ------------------------------
# Main
# ------------------------------
def main():
    print("=== SUMMARIZER SELF TEST ===")
    print(f"Using device: {sm.DEVICE_NAME}")
    print_cache_status()

    doc_results = run_doc_tests()
    code_results = run_code_tests()

    summary_len_avg = statistics.mean([
        doc_results["doc_summary_len"],
        doc_results["role_summary_len"],
        code_results["summary_basic_len"],
        code_results["summary_block_len"]
    ])

    pass_rate = sum([
        doc_results["doc_valid"],
        doc_results["role_valid"],
        code_results["valid_basic"],
        code_results["valid_block"]
    ]) / 4.0

    print("\n=== SUMMARY ===")
    print(f"Average summary length: {summary_len_avg:.1f} words")
    print(f"Validation pass rate: {pass_rate * 100:.1f}%")
    print(f"Code runtime: {code_results['runtime_sec']:.2f}s")

    if pass_rate < 0.5:
        print("WARNING: semantic similarity low. Check model download/inference.")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
