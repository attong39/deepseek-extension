from __future__ import annotations

import hashlib
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator
import ValueError
import bool
import chunks
import classmethod
import content
import data
import dict
import embeddings
import file_size
import file_type
import float
import int
import len
import list
import self
import staticmethod
import str
import super
import title
import v

"""
🎯 ZETA_AI Core Domain - RAG Document Entity
Clean Architecture domain model cho One-Click Learning pipeline
Features:
- ✅ Immutable domain entity với Pydantic v2
- ✅ Rich domain logic với validation
- ✅ Type-safe với proper annotations
- ✅ No external dependencies (pure domain)
"""


class DocumentStatus(str, Enum):
    """Document processing status"""

    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class DocumentMetadata(BaseModel):
    """Document metadata value object"""

    file_type: str
    file_size: int
    language: str | None = None
    encoding: str | None = "utf-8"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("file_type")
    @classmethod
    def validate_file_type(cls, v: str) -> str:
        allowed_types = {"txt", "pdf", "docx", "md", "html"}
        if v.lower() not in allowed_types:
            raise ValueError(f"Unsupported file type: {v}")
        return v.lower()


class DocumentChunk(BaseModel):
    """Document chunk for RAG processing."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str
    content: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    embedding: list[float] | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    """
    RAG Document domain entity - immutable aggregate root
    Business Rules:
    - Document ID must be unique
    - Content cannot be empty
    - Processing updates status atomically
    - Hash ensures content integrity
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    status: DocumentStatus = DocumentStatus.PENDING
    metadata: DocumentMetadata
    content_hash: str = Field(default="")
    processed_at: datetime | None = None
    chunks: list[str] = Field(default_factory=list)
    embeddings: list[list[float]] = Field(default_factory=list)
    model_config = {"frozen": True}  # Immutable

    def __init__(self, **data: Any) -> None:
        if "content_hash" not in data or not data["content_hash"]:
            data["content_hash"] = self._generate_content_hash(data.get("content", ""))
        super().__init__(**data)

    @staticmethod
    def _generate_content_hash(content: str) -> str:
        """Generate SHA-256 hash of content for integrity"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Document content cannot be empty")
        return v.strip()

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Document title cannot be empty")
        return v.strip()

    def mark_as_processing(self) -> Document:
        """Domain method: Start processing"""
        if self.status != DocumentStatus.PENDING:
            raise ValueError(f"Cannot process document in {self.status} status")
        return self.model_copy(update={"status": DocumentStatus.PROCESSING})

    def mark_as_processed(
        self, chunks: list[str], embeddings: list[list[float]]
    ) -> Document:
        """Domain method: Complete processing with results"""
        if self.status != DocumentStatus.PROCESSING:
            raise ValueError(
                f"Cannot complete processing for document in {self.status} status"
            )
        if not chunks:
            raise ValueError("Processed document must have chunks")
        return self.model_copy(
            update={
                "status": DocumentStatus.PROCESSED,
                "processed_at": datetime.utcnow(),
                "chunks": chunks,
                "embeddings": embeddings,
            }
        )

    def mark_as_failed(self) -> Document:
        """Domain method: Mark processing as failed"""
        if self.status not in {DocumentStatus.PENDING, DocumentStatus.PROCESSING}:
            raise ValueError(f"Cannot fail document in {self.status} status")
        return self.model_copy(update={"status": DocumentStatus.FAILED})

    def is_ready_for_search(self) -> bool:
        """Domain query: Check if document is ready for RAG search"""
        return (
            self.status == DocumentStatus.PROCESSED
            and len(self.chunks) > 0
            and len(self.embeddings) > 0
        )

    def get_chunk_count(self) -> int:
        """Domain query: Get number of chunks"""
        return len(self.chunks)

    def verify_integrity(self) -> bool:
        """Domain method: Verify content integrity"""
        current_hash = self._generate_content_hash(self.content)
        return current_hash == self.content_hash


def create_document(
    title: str, content: str, file_type: str, file_size: int
) -> Document:
    """
    Factory function for creating new documents
    Encapsulates business logic for document creation
    """
    metadata = DocumentMetadata(file_type=file_type, file_size=file_size)
    return Document(title=title, content=content, metadata=metadata)


__all__ = [
    "Document",
    "DocumentChunk",
    "DocumentMetadata",
    "DocumentStatus",
    "create_document",
]
