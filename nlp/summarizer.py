#!/usr/bin/env python3
"""
summarizer.py

Provides:
- Document summarization with optional role focus
- Code summarization (single/block)
- Validation via cosine similarity
- Lane-separated embeddings for doc vs code
- Preprocessing and normalization
- Tag generation (POS-aware for docs, regex-based for code)
- Description meta generation
- Model caching integrated
- Added: summarize_file() entrypoint for repo_inventory_and_governance.py
"""

import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
from nlp import nlp_config as cfg
import spacy
from nltk.corpus import stopwords

# ------------------------------
# Device
# ------------------------------
DEVICE_NAME = "cuda" if torch.cuda.is_available() else "cpu"
device = DEVICE_NAME

# ------------------------------
# Load models
# ------------------------------
# Document summarizer
DOC_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
doc_tokenizer = AutoTokenizer.from_pretrained(DOC_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["doc_model"])
doc_model = AutoModelForSeq2SeqLM.from_pretrained(DOC_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["doc_model"]).to(device)

# Code summarizer
CODE_MODEL_NAME = "Salesforce/codet5-base-multi-sum"
code_tokenizer = AutoTokenizer.from_pretrained(CODE_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["code_model"])
code_model = AutoModelForSeq2SeqLM.from_pretrained(CODE_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["code_model"]).to(device)

# Document embedder
doc_embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=DEVICE_NAME, cache_folder=cfg.MODEL_CACHE_DIRS["doc_embedder"])

# Code embedder (CodeBERT)
class CodeBERTEmbedder:
    def __init__(self, model_name="microsoft/codebert-base", device="cpu", cache_dir=None):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
        self.model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir).to(device)

    def encode(self, texts, convert_to_tensor=True):
        all_embs = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
                last_hidden = outputs.last_hidden_state
                mask = inputs['attention_mask'].unsqueeze(-1)
                summed = (last_hidden * mask).sum(1)
                counts = mask.sum(1).clamp(min=1)
                mean_pooled = summed / counts
                all_embs.append(mean_pooled.cpu())
        emb_array = torch.cat(all_embs, dim=0)
        if convert_to_tensor:
            return emb_array
        return emb_array.numpy()

code_embedder = CodeBERTEmbedder(model_name="microsoft/codebert-base", device=DEVICE_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["code_embedder"])

# ------------------------------
# NLP & Stopwords
# ------------------------------
nlp_pos = spacy.load("en_core_web_sm")  # POS tagging for doc tags
stop_words = set(stopwords.words("english"))

# ------------------------------
# Preprocessing & summarization
# ------------------------------
def preprocess_doc(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def summarize_doc(text: str, max_length: int = 40, min_length: int = 10) -> str:
    text = preprocess_doc(text)
    inputs = doc_tokenizer(text, return_tensors="pt", truncation=True).to(device)
    outputs = doc_model.generate(
        **inputs, max_length=max_length, min_length=min_length,
        num_beams=4, early_stopping=True
    )
    return doc_tokenizer.decode(outputs[0], skip_special_tokens=True)

def summarize_code(text: str, block_mode: bool = False, max_length: int = 40, min_length: int = 10) -> str:
    text = preprocess_doc(text)
    inputs = code_tokenizer(text, return_tensors="pt", truncation=True).to(device)
    outputs = code_model.generate(
        **inputs, max_length=max_length, min_length=min_length,
        num_beams=4, early_stopping=True
    )
    return code_tokenizer.decode(outputs[0], skip_special_tokens=True)

# ------------------------------
# Validation
# ------------------------------
def validate_summary(original: str, summary: str, is_code: bool = False) -> bool:
    embedder = code_embedder if is_code else doc_embedder
    orig_emb = embedder.encode([original], convert_to_tensor=True)
    sum_emb = embedder.encode([summary], convert_to_tensor=True)
    sim = util.cos_sim(orig_emb, sum_emb).item()
    return sim > 0.6

# ------------------------------
# Description meta
# ------------------------------
def generate_description_meta(text: str, is_code=False, max_len=40, min_len=10):
    summary = summarize_code(text, max_length=max_len, min_length=min_len) if is_code else summarize_doc(text, max_length=max_len, min_length=min_len)
    validated = validate_summary(text, summary, is_code=is_code)
    return {
        "type": "code" if is_code else "doc",
        "summary": summary,
        "validated": validated
    }

# ------------------------------
# Tag meta
# ------------------------------
def generate_tag_meta(text: str, is_code=False, top_k=10):
    text = text.lower()
    if is_code:
        # simple token extraction for code
        tokens = re.findall(r"\b\w+\b", text)
        tags = [t for t in tokens if t not in stop_words]
    else:
        # POS-based filtering for docs
        doc = nlp_pos(text)
        tokens = [tok.text.lower() for tok in doc if tok.pos_ in {"NOUN", "PROPN", "VERB"} and tok.text.lower() not in stop_words]
        tags = tokens

    # frequency ranking
    freq = {}
    for t in tags:
        freq[t] = freq.get(t, 0) + 1
    sorted_tags = sorted(freq, key=freq.get, reverse=True)
    return sorted_tags[:top_k]

# ------------------------------
# New unified entrypoint
# ------------------------------
def summarize_file(filepath: Path, is_code: bool = None, max_len=40, min_len=10, top_k_tags=10):
    """
    Returns (description: str, tags: List[str]) for repo_inventory_and_governance.py
    Auto-detects file type if is_code=None.
    """
    text = Path(filepath).read_text(encoding="utf-8")
    if is_code is None:
        ext = Path(filepath).suffix.lower()
        is_code = ext in {".py", ".sh", ".js", ".ts", ".html", ".css", ".go", ".yml", ".yaml"}

    desc_meta = generate_description_meta(text, is_code=is_code, max_len=max_len, min_len=min_len)
    tags = generate_tag_meta(text, is_code=is_code, top_k=top_k_tags)
    return desc_meta["summary"], tags
