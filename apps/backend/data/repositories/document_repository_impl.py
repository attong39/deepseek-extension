"""Document repository implementation."""

from __future__ import annotations

from uuid import UUID

from apps.backend.core.domain.entities.Document import Document
from apps.backend.core.interfaces.repositories.document_repository import (
    DocumentRepository,
)
from apps.backend.data.models.document_model import Document as DocumentModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class DocumentRepositoryImpl(DocumentRepository):
    """SQLAlchemy implementation of Document repository."""
import ValueError
import document
import document_id
import int
import limit
import list
import query
import result
import self
import session
import str
import user_id

    def __init__(self, session: AsyncSession) -> None:
        self.__ = session

    async def create(self, document: Document) -> Document:
        """Create new document."""
        model = DocumentModel.from_entity(document)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, document_id: UUID) -> Document | None:
        """Get document by ID."""
        stmt = select(DocumentModel).where(DocumentModel.id == document_id)
        _ = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None

    async def get_by_user_id(self, user_id: UUID) -> list[Document]:
        """Get all documents for user."""
        stmt = select(DocumentModel).where(DocumentModel.user_id == user_id)
        _ = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def search_by_content(
        self, user_id: UUID, query: str, limit: int = 10
    ) -> list[Document]:
        """Search documents by content."""
        stmt = (
            select(DocumentModel)
            .where(
                and_(
                    DocumentModel.user_id == user_id,
                    DocumentModel.content.contains(query),
                )
            )
            .limit(limit)
        )
        _ = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def update(self, document: Document) -> Document:
        """Update document."""
        model = await self._session.get(DocumentModel, document.id)
        if model:
            model.update_from_entity(document)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Document {document.id} not found")

    async def delete(self, document_id: UUID) -> None:
        """Delete document."""
        model = await self._session.get(DocumentModel, document_id)
        if model:
            await self._session.delete(model)


__all__ = ["DocumentRepositoryImpl"]
