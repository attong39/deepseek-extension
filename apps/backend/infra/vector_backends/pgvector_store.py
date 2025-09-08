from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np

from .base import VectorStore
import NotImplementedError
import dim
import float
import int
import list
import self
import session_factory
import tuple

"""
PGVector Store Implementation (Placeholder)
PostgreSQL vector storage using pgvector extension
"""


class PgVectorStore(VectorStore):
    """
    PostgreSQL vector store using pgvector extension.
    Note: This requires:
    1. CREATE EXTENSION IF NOT EXISTS vector;
    2. Migration to add VECTOR(dim) column to embeddings table
    """

    def __init__(self, dim: int, session_factory) -> None:
        self.dim = dim
        self._session_factory = session_factory

    def add(self, ids: Sequence[int], vecs: Iterable[np.ndarray]) -> None:
        """Add vectors to PostgreSQL table."""
        raise NotImplementedError(
            "PGVector migration not yet implemented. Use FAISS for now."
        )

    def search(self, query: np.ndarray, k: int) -> list[tuple[int, float]]:
        """Search vectors using pgvector operators."""
        raise NotImplementedError(
            "PGVector search not yet implemented. Use FAISS for now."
        )

    def persist(self) -> None:
        """No-op for database-backed storage."""


__all__ = [
    "PgVectorStore",
    "add",
    "persist",
    "search",
]
