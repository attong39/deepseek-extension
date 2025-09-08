from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

import numpy as np
import classmethod
import cls
import content
import dict
import embeddings
import float
import int
import len
import metadata
import other_vector
import property
import self
import str
import vector_embeddings

"""Vector Document Domain Entity."""


@dataclass
class VectorDocument:
    """Domain entity for vector documents."""

    id: UUID
    content: str
    vector_embeddings: np.ndarray
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        content: str,
        vector_embeddings: np.ndarray,
        metadata: dict[str, Any] | None = None,
    ) -> VectorDocument:
        """Create new vector document."""
        return cls(
            id=uuid4(),
            content=content,
            vector_embeddings=vector_embeddings,
            metadata=metadata or {},
            created_at=datetime.now(),
        )

    def update_content(self, content: str, embeddings: np.ndarray) -> None:
        """Update document content and embeddings."""
        self.content = content
        self.vector_embeddings = embeddings
        self.updated_at = datetime.now()

    @property
    def dimension(self) -> int:
        """Get vector dimension."""
        return len(self.vector_embeddings)

    def calculate_similarity(self, other_vector: np.ndarray) -> float:
        """Calculate cosine similarity with another vector."""
        dot_product = np.dot(self.vector_embeddings, other_vector)
        norm_a = np.linalg.norm(self.vector_embeddings)
        norm_b = np.linalg.norm(other_vector)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)


__all__ = [
    "VectorDocument",
    "calculate_similarity",
    "create",
    "dimension",
    "dot_product",
    "norm_a",
    "norm_b",
    "update_content",
]
