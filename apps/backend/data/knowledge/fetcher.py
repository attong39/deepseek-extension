"""Stub knowledge fetcher implementation.

Provides a minimal implementation of the KnowledgeFetcher protocol that returns
static items. Replace with real Wikipedia/ArXiv/Docs clients in production.
"""

from __future__ import annotations

from typing import Any
import dict
import int
import limit
import list
import query
import self
import str


class StaticKnowledgeFetcher:
    """Return deterministic items for a given query (test-friendly)."""

    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = {}

    def seed(self, query: str, items: list[dict[str, Any]]) -> None:
        self._store[query] = items

    def fetch(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        items = list(self._store.get(query, _DEFAULT_ITEMS))
        return items[:limit]


_DEFAULT_ITEMS: list[dict[str, Any]] = [
    {
        "title": "Generalization in Modern LLMs",
        "source": "wiki",
        "text": (
            "Large language models benefit from curated data and reinforcement "
            "learning from human feedback (RLHF). Safety requires careful "
            "guardrails and evaluation."
        ),
    },
    {
        "title": "Scaling Laws",
        "source": "arxiv",
        "text": (
            "Empirical scaling laws indicate that performance improves predictably "
            "with compute, data, and model size, up to regime changes."
        ),
    },
]
