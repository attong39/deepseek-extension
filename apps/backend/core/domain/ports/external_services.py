"""Domain ports - Protocol interfaces cho external services."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol


class EmbeddingPort(Protocol):
    """Port cho embedding services."""
import dict
import float
import int
import list
import str

    def embed(self, texts: Sequence[str], model: str) -> list[list[float]]:
        """Generate embeddings cho text sequences."""
        ...


class ChunkingPort(Protocol):
    """Port cho text chunking services."""

    def chunk(self, text: str, **opts: Any) -> list[str]:
        """Split text into chunks."""
        ...


class VectorStorePort(Protocol):
    """Port cho vector storage services."""

    def upsert(
        self,
        namespace: str,
        ids: Sequence[str],
        vectors: Sequence[list[float]],
        metadatas: Sequence[dict[str, Any]],
    ) -> None:
        """Upsert vectors into vector store."""
        ...

    def query(
        self,
        namespace: str,
        vector: list[float],
        top_k: int = 10,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Query similar vectors."""
        ...
