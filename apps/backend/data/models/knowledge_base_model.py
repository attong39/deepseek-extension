"""


Knowledge Base Database Model.





Represents knowledge bases and documents for AI agents.


"""

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel, SoftDeleteMixin, TaggedMixin
from sqlalchemy import Column, DateTime, Integer, String, Text
import TypeError
import ValueError
import bool
import delta
import dict
import float
import int
import len
import list
import max
import max_length
import metadata
import self
import settings
import size_delta
import str
import user_id
import vector


class KnowledgeBase(BaseModel, SoftDeleteMixin, TaggedMixin):
    """Knowledge base model for storing structured knowledge."""

    # Basic Information

    name = Column(String(255), nullable=False, index=True, doc="Knowledge base name")

    description = Column(Text, nullable=True, doc="Knowledge base description")

    category = Column(
        String(100), nullable=True, index=True, doc="Knowledge base category"
    )

    # Owner and Access

    owner_id = Column(String(36), nullable=False, index=True, doc="Owner user ID")

    visibility = Column(
        String(20),
        nullable=False,
        default="private",
        doc="Visibility (private, public, organization)",
    )

    # Status

    status = Column(
        String(20),
        nullable=False,
        default="draft",
        index=True,
        doc="Knowledge base status (draft, active, archived)",
    )

    # Content Metrics

    document_count = Column(
        Integer, nullable=False, default=0, doc="Number of documents"
    )

    total_size_bytes = Column(
        String(20), nullable=False, default="0", doc="Total size in bytes"
    )

    # Processing Information

    last_indexed_at = Column(
        DateTime(timezone=True), nullable=True, doc="Last indexing timestamp"
    )

    indexing_status = Column(
        String(20),
        nullable=False,
        default="pending",
        doc="Indexing status (pending, processing, completed, failed)",
    )

    # Configuration

    settings_json = Column(Text, nullable=True, doc="Knowledge base settings in JSON")

    # Embeddings Configuration

    embedding_model = Column(
        String(100),
        nullable=True,
        default="text-embedding-ada-002",
        doc="Embedding model used",
    )

    chunk_size = Column(
        Integer, nullable=False, default=1000, doc="Text chunk size for processing"
    )

    chunk_overlap = Column(
        Integer, nullable=False, default=200, doc="Overlap between chunks"
    )

    # Helper Methods

    def get_settings(self) -> dict[str, Any]:
        """Get knowledge base settings."""

        if not self.settings_json:
            return {}

        try:
            return json.loads(self.settings_json)

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_settings(self, settings: dict[str, Any]) -> None:
        """Set knowledge base settings."""

        self.settings_json = json.dumps(settings)

    def is_accessible_by_user(self, user_id: str) -> bool:
        """Check if user can access this knowledge base."""

        # Owner always has access

        if str(self.owner_id) == str(user_id):
            return True

        # Public knowledge bases are accessible to all

        if str(self.visibility) == "public":
            return True

        return False

    def can_be_indexed(self) -> bool:
        """Check if knowledge base can be indexed."""

        return (
            str(self.status) == "active" and str(self.indexing_status) != "processing"
        )

    def update_document_count(self, delta: int = 0) -> None:
        """Update document count."""

        self.document_count = max(int(self.document_count) + delta, 0)

    def update_size(self, size_delta: int = 0) -> None:
        """Update total size."""

        current_size = int(self.total_size_bytes or "0")

        new_size = max(current_size + size_delta, 0)

        self.total_size_bytes = str(new_size)

    def get_size_human(self) -> str:
        """Get human-readable size."""

        try:
            size_bytes = int(self.total_size_bytes or "0")

            if size_bytes < 1024:
                return f"{size_bytes} B"

            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"

            elif size_bytes < 1024 * 1024 * 1024:
                return f"{size_bytes / (1024 * 1024):.1f} MB"

            else:
                return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

        except (ValueError, TypeError):
            return "Unknown"

    def mark_indexing_started(self) -> None:
        """Mark indexing as started."""

        self.indexing_status = "processing"

        self.last_indexed_at = datetime.now(UTC)

    def mark_indexing_completed(self) -> None:
        """Mark indexing as completed."""

        self.indexing_status = "completed"

        self.last_indexed_at = datetime.now(UTC)

    def mark_indexing_failed(self) -> None:
        """Mark indexing as failed."""

        self.indexing_status = "failed"

    def to_dict_summary(self) -> dict[str, Any]:
        """Get summary representation."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "visibility": self.visibility,
            "document_count": self.document_count,
            "total_size": self.get_size_human(),
            "indexing_status": self.indexing_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_indexed_at": self.last_indexed_at.isoformat()
            if self.last_indexed_at
            else None,
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<KnowledgeBase(id={self.id}, name={self.name}, status={self.status})>"


class Document(BaseModel, SoftDeleteMixin, TaggedMixin):
    """Document model for storing individual documents in knowledge bases."""

    # Basic Information

    title = Column(String(500), nullable=False, index=True, doc="Document title")

    content = Column(Text, nullable=False, doc="Document content")

    content_type = Column(
        String(50), nullable=False, default="text/plain", doc="Content MIME type"
    )

    # Relationships

    knowledge_base_id = Column(
        String(36), nullable=False, index=True, doc="Knowledge base ID"
    )

    # Source Information

    source_url = Column(String(1000), nullable=True, doc="Original source URL")

    source_type = Column(
        String(50), nullable=True, doc="Source type (file, url, manual, etc.)"
    )

    file_path = Column(String(1000), nullable=True, doc="File path if uploaded")

    # Content Metrics

    word_count = Column(Integer, nullable=False, default=0, doc="Word count")

    character_count = Column(Integer, nullable=False, default=0, doc="Character count")

    # Processing Status

    processing_status = Column(
        String(20),
        nullable=False,
        default="pending",
        doc="Processing status (pending, processing, completed, failed)",
    )

    embedding_status = Column(
        String(20),
        nullable=False,
        default="pending",
        doc="Embedding status (pending, processing, completed, failed)",
    )

    # Quality Metrics

    quality_score = Column(
        String(10), nullable=True, doc="Content quality score (0-100)"
    )

    readability_score = Column(String(10), nullable=True, doc="Readability score")

    # Processing Timestamps

    processed_at = Column(
        DateTime(timezone=True), nullable=True, doc="Processing completion timestamp"
    )

    embedded_at = Column(
        DateTime(timezone=True), nullable=True, doc="Embedding completion timestamp"
    )

    # Metadata

    metadata_json = Column(Text, nullable=True, doc="Additional metadata in JSON")

    # Helper Methods

    def get_metadata(self) -> dict[str, Any]:
        """Get document metadata."""

        if not self.metadata_json:
            return {}

        try:
            return json.loads(self.metadata_json)

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_metadata(self, metadata: dict[str, Any]) -> None:
        """Set document metadata."""

        self.metadata_json = json.dumps(metadata)

    def update_content_metrics(self) -> None:
        """Update content metrics based on content."""

        if self.content:
            self.character_count = len(self.content)

            # Simple word count

            words = self.content.split()

            self.word_count = len(words)

    def mark_processing_started(self) -> None:
        """Mark processing as started."""

        self.processing_status = "processing"

    def mark_processing_completed(self) -> None:
        """Mark processing as completed."""

        self.processing_status = "completed"

        self.processed_at = datetime.now(UTC)

    def mark_processing_failed(self) -> None:
        """Mark processing as failed."""

        self.processing_status = "failed"

    def mark_embedding_started(self) -> None:
        """Mark embedding as started."""

        self.embedding_status = "processing"

    def mark_embedding_completed(self) -> None:
        """Mark embedding as completed."""

        self.embedding_status = "completed"

        self.embedded_at = datetime.now(UTC)

    def mark_embedding_failed(self) -> None:
        """Mark embedding as failed."""

        self.embedding_status = "failed"

    def is_ready_for_embedding(self) -> bool:
        """Check if document is ready for embedding."""

        return str(self.processing_status) == "completed" and str(
            self.embedding_status
        ) in [
            "pending",
            "failed",
        ]

    def get_preview(self, max_length: int = 200) -> str:
        """Get content preview."""

        if not self.content:
            return ""

        if len(self.content) <= max_length:
            return self.content

        return self.content[:max_length] + "..."

    def to_dict_summary(self) -> dict[str, Any]:
        """Get summary representation."""

        return {
            "id": self.id,
            "title": self.title,
            "content_preview": self.get_preview(),
            "content_type": self.content_type,
            "source_type": self.source_type,
            "word_count": self.word_count,
            "character_count": self.character_count,
            "processing_status": self.processing_status,
            "embedding_status": self.embedding_status,
            "quality_score": self.quality_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_at": self.processed_at.isoformat()
            if self.processed_at
            else None,
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<Document(id={self.id}, title={self.title[:50]}, status={self.processing_status})>"


class DocumentChunk(BaseModel):
    """Document chunk model for storing processed text chunks."""

    # Basic Information

    content = Column(Text, nullable=False, doc="Chunk content")

    chunk_index = Column(Integer, nullable=False, doc="Chunk index in document")

    # Relationships

    document_id = Column(String(36), nullable=False, index=True, doc="Document ID")

    knowledge_base_id = Column(
        String(36), nullable=False, index=True, doc="Knowledge base ID"
    )

    # Content Metrics

    token_count = Column(Integer, nullable=True, doc="Token count for this chunk")

    word_count = Column(Integer, nullable=False, default=0, doc="Word count")

    # Embedding Information

    embedding_vector = Column(Text, nullable=True, doc="Embedding vector as JSON")

    embedding_model = Column(String(100), nullable=True, doc="Model used for embedding")

    embedding_created_at = Column(
        DateTime(timezone=True), nullable=True, doc="Embedding creation timestamp"
    )

    # Position Information

    start_position = Column(
        Integer, nullable=True, doc="Start position in original document"
    )

    end_position = Column(
        Integer, nullable=True, doc="End position in original document"
    )

    # Helper Methods

    def get_embedding_vector(self) -> list[float] | None:
        """Get embedding vector as list."""

        if not self.embedding_vector:
            return None

        try:
            return json.loads(self.embedding_vector)

        except (json.JSONDecodeError, TypeError):
            return None

    def set_embedding_vector(self, vector: list[float]) -> None:
        """Set embedding vector."""

        self.embedding_vector = json.dumps(vector)

        self.embedding_created_at = datetime.now(UTC)

    def has_embedding(self) -> bool:
        """Check if chunk has embedding."""

        return self.embedding_vector is not None

    def update_word_count(self) -> None:
        """Update word count based on content."""

        if self.content:
            words = self.content.split()

            self.word_count = len(words)

    def get_preview(self, max_length: int = 100) -> str:
        """Get content preview."""

        if not self.content:
            return ""

        if len(self.content) <= max_length:
            return self.content

        return self.content[:max_length] + "..."

    def to_dict(self) -> dict[str, Any]:
        """Get chunk representation."""

        return {
            "id": self.id,
            "content": self.content,
            "chunk_index": self.chunk_index,
            "document_id": self.document_id,
            "knowledge_base_id": self.knowledge_base_id,
            "word_count": self.word_count,
            "token_count": self.token_count,
            "has_embedding": self.has_embedding(),
            "embedding_model": self.embedding_model,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<DocumentChunk(id={self.id}, doc={self.document_id}, index={self.chunk_index})>"
