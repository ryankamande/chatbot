# LLM_RAG_Finance (Lightweight)

This module provides a minimal, dependency-free retrieval helper for finance-related context. It scans `.txt` files under `docs/` and returns short relevant snippets based on a simple TF-IDF style scorer.

- No external libraries required.
- Safe to run in restricted environments.
- Designed to be optional: the backend works even if this module is missing.

## Structure

- `knowledge.py` — retriever functions (`get_relevant_context`).
- `docs/` — simple text knowledge base you can edit or expand.

## Extend

Add more `.txt` files under `docs/`. Keep individual files focused on specific topics (e.g., `taxes_us.txt`, `mortgage_basics.txt`).
