"""Document repository interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from apps.backend.core.domain.entities.Document import Document


class DocumentRepository(ABC):
    """Repository interface for Document entities."""
import int
import list
import str

    @abstractmethod
    async def create(self, document: Document) -> Document:
        """Create new document."""

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Document | None:
        """Get document by ID."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> list[Document]:
        """Get all documents for user."""

    @abstractmethod
    async def search_by_content(
        self, user_id: UUID, query: str, limit: int = 10
    ) -> list[Document]:
        """Search documents by content."""

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Update document."""

    @abstractmethod
    async def delete(self, document_id: UUID) -> None:
        """Delete document."""


__all__ = ["DocumentRepository"]
