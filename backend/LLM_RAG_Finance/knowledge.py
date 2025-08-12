"""
Lightweight local finance knowledge retriever.
No heavy dependencies: simple TF-IDF style scoring using Python stdlib.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import math
import re

# Simple text store path
DOCS_DIR = Path(__file__).parent / "docs"

STOPWORDS = set(
    """
    a an and the is are to of in on for with at from by as be this that which or not your you we our it it's its
    about into over under if then else when where how what why who whom theirs theirs' his her hers he she they them
    can could should would may might will just more most less least than up down out off because so very
    """.split()
)

_token_re = re.compile(r"[A-Za-z0-9$%.]+")

def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in _token_re.findall(text)]

@dataclass
class Doc:
    path: Path
    text: str


def _load_docs() -> List[Doc]:
    docs: List[Doc] = []
    if DOCS_DIR.exists():
        for p in sorted(DOCS_DIR.glob("**/*.txt")):
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            docs.append(Doc(path=p, text=txt))
    return docs

_DOCS_CACHE: List[Doc] | None = None


def _get_docs() -> List[Doc]:
    global _DOCS_CACHE
    if _DOCS_CACHE is None:
        _DOCS_CACHE = _load_docs()
    return _DOCS_CACHE


def _tf(tokens: List[str]) -> dict[str, float]:
    counts: dict[str, int] = {}
    for t in tokens:
        if t in STOPWORDS:
            continue
        counts[t] = counts.get(t, 0) + 1
    max_c = max(counts.values()) if counts else 1
    return {t: c / max_c for t, c in counts.items()}


def _idf(all_docs_tokens: List[List[str]]) -> dict[str, float]:
    df: dict[str, int] = {}
    n_docs = len(all_docs_tokens)
    for toks in all_docs_tokens:
        for t in set(toks):
            if t in STOPWORDS:
                continue
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n_docs + 1) / (df_c + 1)) + 1.0 for t, df_c in df.items()}


def _score(query: str, doc: Doc, idf: dict[str, float]) -> float:
    q_tokens = _tokenize(query)
    d_tokens = _tokenize(doc.text)
    q_tf = _tf(q_tokens)
    d_tf = _tf(d_tokens)
    # Cosine-like between TF-IDF vectors (sparse approximation)
    score = 0.0
    for t, q_w in q_tf.items():
        if t in STOPWORDS:
            continue
        idf_w = idf.get(t, 1.0)
        d_w = d_tf.get(t, 0.0)
        score += q_w * idf_w * d_w
    # Boost HF finance docs so they are preferred when relevant
    try:
        parts = set(p.lower() for p in doc.path.parts)
        if "hf_finance" in parts or doc.path.name.lower().startswith("hf_"):
            score *= 1.3
    except Exception:
        pass
    return score


def get_relevant_context(query: str, k: int = 3, max_chars: int = 800) -> str:
    docs = _get_docs()
    if not docs:
        return ""

    # Precompute IDF over the doc collection
    all_doc_tokens = [_tokenize(d.text) for d in docs]
    idf = _idf(all_doc_tokens)

    ranked: List[Tuple[float, Doc]] = []
    for d in docs:
        s = _score(query, d, idf)
        if s > 0:
            ranked.append((s, d))
    ranked.sort(key=lambda x: x[0], reverse=True)

    selected = []
    total = 0
    for _, d in ranked[: max(1, k)]:
        chunk = d.text.strip()
        if not chunk:
            continue
        if total + len(chunk) > max_chars:
            chunk = chunk[: max(0, max_chars - total)]
        selected.append(f"[Source: {d.path.name}]\n{chunk}")
        total += len(chunk)
        if total >= max_chars:
            break

    return "\n\n".join(selected)
