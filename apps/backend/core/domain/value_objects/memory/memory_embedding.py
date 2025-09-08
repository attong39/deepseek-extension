"""
Value Object: Memory Embedding

VO cho embedding vector storage và metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
import ValueError
import a
import abs
import b
import bool
import classmethod
import cls
import data
import dict
import enumerate
import float
import i
import int
import isinstance
import len
import list
import metadata
import model
import object
import other
import self
import str
import sum
import tolerance
import tuple
import val
import vector
import x
import zip


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(UTC)


@dataclass(frozen=True)
class MemoryEmbeddingVO:
    """
    Value Object for memory embedding vector information.

    Responsibility:
        - Immutable embedding vector storage
        - Embedding metadata và model tracking
        - Vector search optimization data

    Business Rules:
        - Vector không empty và có dimension > 0
        - Model name không empty
        - Dimension phải match vector length
        - Immutable after creation (frozen dataclass)

    Use Cases:
        - Vector storage coordinates cho data layer
        - Embedding generation tracking
        - Search performance optimization
        - Model version control
    """

    vector: tuple[float, ...]  # Immutable tuple for vector data
    model: str  # Embedding model used (e.g., "text-embedding-ada-002")
    dimension: int  # Vector dimension
    created_at: datetime = None  # Will be set in __post_init__

    # Optional metadata
    metadata: dict[str, Any] = None

    def __post_init__(self) -> None:
        """Post-initialization validation và default setting."""
        # Set default values using object.__setattr__ for frozen dataclass
        if self.created_at is None:
            object.__setattr__(self, "created_at", utc_now())

        if self.metadata is None:
            object.__setattr__(self, "metadata", {})

        # Validate business rules
        self._validate()

    def _validate(self) -> None:
        """Validate embedding VO business rules."""
        if not self.vector:
            raise ValueError("Vector cannot be empty")

        if not self.model or not self.model.strip():
            raise ValueError("Model name cannot be empty")

        if self.dimension <= 0:
            raise ValueError("Dimension must be positive")

        if len(self.vector) != self.dimension:
            raise ValueError(
                f"Vector length {len(self.vector)} doesn't match dimension {self.dimension}"
            )

        # Check for valid float values
        for i, val in enumerate(self.vector):
            if not isinstance(val, int | float):
                raise ValueError(f"Vector element at index {i} must be numeric")

    @classmethod
    def from_list(
        cls, vector: list[float], model: str, metadata: dict[str, Any] | None = None
    ) -> MemoryEmbeddingVO:
        """
        Create embedding VO from list of floats.

        Args:
            vector: List of embedding values
            model: Model name used for embedding
            metadata: Optional metadata

        Returns:
            MemoryEmbeddingVO instance
        """
        if not vector:
            raise ValueError("Vector list cannot be empty")

        return cls(
            vector=tuple(vector),
            model=model,
            dimension=len(vector),
            metadata=metadata or {},
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation
        """
        return {
            "vector": list(self.vector),
            "model": self.model,
            "dimension": self.dimension,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata.copy(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> MemoryEmbeddingVO:
        """
        Create from dictionary representation.

        Args:
            data: Dictionary with embedding data

        Returns:
            MemoryEmbeddingVO instance
        """
        return cls(
            vector=tuple(data["vector"]),
            model=data["model"],
            dimension=data["dimension"],
            created_at=datetime.fromisoformat(data["created_at"]),
            metadata=data.get("metadata", {}),
        )

    def calculate_similarity(self, other: MemoryEmbeddingVO) -> float:
        """
        Calculate cosine similarity with another embedding.

        Args:
            other: Another embedding VO

        Returns:
            Similarity score between 0.0 and 1.0

        Raises:
            ValueError: If dimensions don't match
        """
        if self.dimension != other.dimension:
            raise ValueError(
                f"Dimension mismatch: {self.dimension} vs {other.dimension}"
            )

        # Cosine similarity calculation
        dot_product = sum(a * b for a, b in zip(self.vector, other.vector, strict=True))
        magnitude_a = sum(a * a for a in self.vector) ** 0.5
        magnitude_b = sum(b * b for b in other.vector) ** 0.5

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        similarity = dot_product / (magnitude_a * magnitude_b)
        # Normalize to 0-1 range (cosine similarity can be -1 to 1)
        return (similarity + 1) / 2

    def get_magnitude(self) -> float:
        """Get vector magnitude (L2 norm)."""
        return sum(x * x for x in self.vector) ** 0.5

    def is_normalized(self, tolerance: float = 1e-6) -> bool:
        """Check if vector is normalized (magnitude ≈ 1.0)."""
        return abs(self.get_magnitude() - 1.0) < tolerance

    def get_model_family(self) -> str:
        """Extract model family from model name."""
        # Common embedding model families
        if "ada" in self.model.lower():
            return "ada"
        elif "davinci" in self.model.lower():
            return "davinci"
        elif "curie" in self.model.lower():
            return "curie"
        elif "babbage" in self.model.lower():
            return "babbage"
        elif "text-embedding" in self.model.lower():
            return "text-embedding"
        else:
            return "unknown"

    def get_storage_size_bytes(self) -> int:
        """Estimate storage size in bytes."""
        # Each float typically 4 bytes (32-bit) or 8 bytes (64-bit)
        # Assume 4 bytes per float for typical embedding storage
        return (
            self.dimension * 4 + len(self.model.encode("utf-8")) + 100
        )  # +100 for metadata overhead
