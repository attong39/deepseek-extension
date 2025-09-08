from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.vector_document import VectorDocument
from apps.backend.core.domain.value_objects.vector_query import (
import bool
import dict
import int
import list
    VectorQuery,
    VectorSearchResult,
)

"""Vector Repository Interface."""


class VectorRepositoryInterface(ABC):
    """Interface for vector document repository."""

    @abstractmethod
    async def save(self, document: VectorDocument) -> bool:
        """Save vector document."""

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> VectorDocument | None:
        """Get document by ID."""

    @abstractmethod
    async def delete(self, document_id: UUID) -> bool:
        """Delete document by ID."""

    @abstractmethod
    async def search_similar(self, query: VectorQuery) -> list[VectorSearchResult]:
        """Search for similar vectors."""

    @abstractmethod
    async def batch_save(self, documents: list[VectorDocument]) -> int:
        """Save multiple documents, return count saved."""

    @abstractmethod
    async def get_stats(self) -> dict:
        """Get repository statistics."""


__all__ = [
    "VectorRepositoryInterface",
]
