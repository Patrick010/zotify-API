#!/usr/bin/env python3
"""
summarizer.py

Provides:
- Document summarization with optional role focus
- Code summarization (single/block)
- Validation via cosine similarity
- Lane-separated embeddings for doc vs code
- Preprocessing and normalization
- Model caching integrated
"""

import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel
from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import nlp_config as cfg

DEVICE_NAME = "cuda" if torch.cuda.is_available() else "cpu"
device = DEVICE_NAME

# ------------------------------
# Load doc summarizer (cached)
# ------------------------------
DOC_MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
doc_tokenizer = AutoTokenizer.from_pretrained(
    DOC_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["doc_model"]
)
doc_model = AutoModelForSeq2SeqLM.from_pretrained(
    DOC_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["doc_model"]
).to(device)

# ------------------------------
# Load CodeT5 summarizer (cached)
# ------------------------------
CODE_MODEL_NAME = "Salesforce/codet5-base-multi-sum"
code_tokenizer = AutoTokenizer.from_pretrained(
    CODE_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["code_model"]
)
code_model = AutoModelForSeq2SeqLM.from_pretrained(
    CODE_MODEL_NAME, cache_dir=cfg.MODEL_CACHE_DIRS["code_model"]
).to(device)

# ------------------------------
# Load doc embedder
# ------------------------------
doc_embedder = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device=DEVICE_NAME,
    cache_folder=cfg.MODEL_CACHE_DIRS["doc_embedder"]
)

# ------------------------------
# CodeBERT embedding wrapper
# ------------------------------
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
        else:
            return emb_array.numpy()

code_embedder = CodeBERTEmbedder(
    model_name="microsoft/codebert-base",
    device=DEVICE_NAME,
    cache_dir=cfg.MODEL_CACHE_DIRS["code_embedder"]
)

# ------------------------------
# Preprocessing & summarization
# ------------------------------
def preprocess_doc(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text

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
