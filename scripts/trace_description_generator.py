# nlp/summarizer.py

import torch
from transformers import pipeline
import logging
import time
from sentence_transformers import SentenceTransformer, util

# -------------------------
# Logging Setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

# -------------------------
# Device / Model Initialization
# -------------------------
device = 0 if torch.cuda.is_available() else -1
print(f"Device set to use {'cuda' if device == 0 else 'cpu'}")

summarizer_pipeline = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=device
)

# Semantic similarity model
_sem_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# -------------------------
# Helper Functions
# -------------------------
def _semantic_similarity(text1: str, text2: str) -> float:
    """Return cosine similarity between two texts (0-1)."""
    embeddings = _sem_model.encode([text1, text2], convert_to_tensor=True)
    sim = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    return sim.item()


def _generate_summary(text: str, prefix: str = "", max_tokens: int = None) -> str:
    """Generate a summary using dynamic max_length scaling and proper input handling."""
    if not text or len(text.strip()) == 0:
        return ""

    start_time = time.time()
    input_text = f"{prefix.strip()} {text.strip()}" if prefix else text.strip()

    # Tokenize to determine size and dynamically set max_length
    tokens = summarizer_pipeline.tokenizer.encode(input_text, truncation=False)
    input_len = len(tokens)
    if max_tokens is None:
        max_len = max(20, min(80, input_len // 2))  # adaptive summarization window
    else:
        max_len = max_tokens

    try:
        result = summarizer_pipeline(
            input_text,
            max_length=max_len,
            min_length=10,
            do_sample=False
        )
        summary = result[0]["summary_text"].strip()
        elapsed = time.time() - start_time
        logging.info(f"Summarized file ({input_len} tokens) in {elapsed:.2f}s")
        return summary

    except Exception as e:
        logging.warning(f"Failed to summarize text: {e}")
        return ""

# -------------------------
# Public Functions
# -------------------------
def summarize_doc(text: str, role_focused: bool = False) -> str:
    """
    Summarize documentation or markdown text.
    If role_focused=True, generate a short description of the document's role, not content.
    """
    if role_focused:
        prefix = (
            "Provide a short, role-focused description of this document. "
            "Explain its purpose in the project, what decisions or information it supports, "
            "without summarizing content. Keep it concise, under two sentences, complete sentences:\n"
        )
        return _generate_summary(text, prefix, max_tokens=50)
    else:
        prefix = (
            "Summarize the following documentation clearly and concisely. "
            "Highlight key concepts, modules, and main functions:\n"
        )
        return _generate_summary(text, prefix)

def summarize_code(code: str) -> str:
    """
    Summarize source code files with emphasis on intent and structure.
    Focus on functionality, modules, classes, and architecture.
    """
    prefix = (
        "Explain the purpose and main logic of the following source code. "
        "Focus on functionality, modules, classes, and architecture. "
        "Do not restate comments or file names literally. Return a concise summary paragraph:\n"
    )
    return _generate_summary(code, prefix)

def validate_summary(original_text: str, summary: str, threshold: float = 0.4) -> bool:
    """Return True if summary is semantically similar enough to original text."""
    if not summary:
        return False
    sim = _semantic_similarity(original_text, summary)
    if sim < threshold:
        logging.warning(f"Low semantic similarity detected ({sim:.3f})")
        return False
    return True
