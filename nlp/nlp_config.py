#!/usr/bin/env python3
"""
Configuration for NLP module
- Model cache directories
- API cache directories
- Environment-variable override for flexible deployment

Default behavior: uses ~/.zotify_nlp_cache/... for everything.
Environment override: any of the following can be set to redirect cache locations:

export ZOTIFY_NLP_CACHE=/mnt/nlp_cache
export ZOTIFY_DOC_MODEL_CACHE=/mnt/nlp_cache/doc_model
export ZOTIFY_CODE_MODEL_CACHE=/mnt/nlp_cache/code_model
export ZOTIFY_DOC_EMBED_CACHE=/mnt/nlp_cache/doc_embedder
export ZOTIFY_CODE_EMBED_CACHE=/mnt/nlp_cache/code_embedder
export ZOTIFY_API_CACHE=/mnt/nlp_cache/api_cache

"""

import os
from pathlib import Path

# Base cache path
CACHE_BASE = Path(os.environ.get("ZOTIFY_NLP_CACHE", Path.home() / ".zotify_nlp_cache"))
CACHE_BASE.mkdir(exist_ok=True, parents=True)

# Model caches
MODEL_CACHE_DIRS = {
    "doc_model": Path(os.environ.get("ZOTIFY_DOC_MODEL_CACHE", CACHE_BASE / "doc_model")),
    "code_model": Path(os.environ.get("ZOTIFY_CODE_MODEL_CACHE", CACHE_BASE / "code_model")),
    "doc_embedder": Path(os.environ.get("ZOTIFY_DOC_EMBED_CACHE", CACHE_BASE / "doc_embedder")),
    "code_embedder": Path(os.environ.get("ZOTIFY_CODE_EMBED_CACHE", CACHE_BASE / "code_embedder"))
}

# Create all directories if they do not exist
for path in MODEL_CACHE_DIRS.values():
    path.mkdir(exist_ok=True, parents=True)

# API cache (optional, used later)
API_CACHE_DIR = Path(os.environ.get("ZOTIFY_API_CACHE", CACHE_BASE / "api_cache"))
API_CACHE_DIR.mkdir(exist_ok=True)
