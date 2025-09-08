from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import ValueError
import bool
import dict
import float
import int
import len
import self
import str

"""Vector Query Value Objects."""


@dataclass(frozen=True)
class VectorQuery:
    """Value object for vector similarity queries."""

    query_vector: np.ndarray
    top_k: int = 10
    similarity_threshold: float = 0.0
    metadata_filter: dict[str, Any] | None = None
    include_embeddings: bool = False

    def __post_init__(self) -> None:
        """Validate query parameters."""
        if self.top_k <= 0:
            raise ValueError("top_k must be positive")
        if not 0.0 <= self.similarity_threshold <= 1.0:
            raise ValueError("similarity_threshold must be between 0 and 1")
        if len(self.query_vector) == 0:
            raise ValueError("query_vector cannot be empty")


@dataclass(frozen=True)
class VectorSearchResult:
    """Result of vector similarity search."""

    document_id: str
    score: float
    metadata: dict[str, Any]
    content: str | None = None
    embeddings: np.ndarray | None = None

    def __post_init__(self) -> None:
        """Validate result."""
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1")


__all__ = [
    "VectorQuery",
    "VectorSearchResult",
]
