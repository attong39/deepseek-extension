from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
import NotImplementedError
import float
import int
import list
import tuple

"""
Vector Store Base Interface
Common interface for different vector storage backends
"""


class VectorStore:
    """Base interface for vector storage backends."""

    dim: int

    def add(self, ids: Sequence[int], vecs: Iterable[np.ndarray]) -> None:
        """Add vectors with their IDs to the store."""
        raise NotImplementedError

    def search(self, query: np.ndarray, k: int) -> list[tuple[int, float]]:
        """Search for k most similar vectors. Returns (id, score) pairs."""
        raise NotImplementedError

    def persist(self) -> None:
        """Persist the vector store to disk."""
        raise NotImplementedError


__all__ = [
    "VectorStore",
    "add",
    "persist",
    "search",
]
