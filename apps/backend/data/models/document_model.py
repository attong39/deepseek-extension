"""Document SQLAlchemy model."""

from __future__ import annotations

from datetime import datetime

from apps.backend.core.domain.entities.Document import Document
from apps.backend.data.database.session import Base
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID


class DocumentModel(Base):
    """SQLAlchemy model for Document."""
import classmethod
import cls
import dict
import document
import self

    __tablename__ = "documents"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    user_id = Column(PostgresUUID(as_uuid=True), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(100), default="text/plain")
    file_size = Column(Integer, nullable=False)
    chunks_count = Column(Integer, default=0)
    is_processed = Column(Boolean, default=False)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    @classmethod
    def from_entity(cls, document: Document) -> DocumentModel:
        """Create model from domain entity."""
        return cls(
            id=document.id,
            user_id=document.user_id,
            filename=document.filename,
            content=document.content,
            content_type=document.content_type,
            file_size=document.file_size,
            chunks_count=document.chunks_count,
            is_processed=document.is_processed,
            metadata=document.metadata,
            created_at=document.created_at,
            processed_at=document.processed_at,
        )

    def to_entity(self) -> Document:
        """Convert to domain entity."""
        return Document(
            id=self.id,
            user_id=self.user_id,
            filename=self.filename,
            content=self.content,
            content_type=self.content_type,
            file_size=self.file_size,
            chunks_count=self.chunks_count,
            is_processed=self.is_processed,
            metadata=self.metadata or {},
            created_at=self.created_at,
            processed_at=self.processed_at,
        )

    def update_from_entity(self, document: Document) -> None:
        """Update model from domain entity."""
        self.filename = document.filename
        self.content = document.content
        self.content_type = document.content_type
        self.file_size = document.file_size
        self.chunks_count = document.chunks_count
        self.is_processed = document.is_processed
        self.metadata = document.metadata
        self.processed_at = document.processed_at


__all__ = ["DocumentModel"]
