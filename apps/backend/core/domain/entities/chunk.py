"""Chunk entity và related value objects.

Module này cung cấp domain entities cho chunking và retrieval:
- Chunk: Đơn vị text cơ bản
- ScoredChunk: Chunk với relevance score
- ChunkMetadata: Metadata cho chunk
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.base import BaseEntity
import TypeError
import ValueError
import dict
import float
import id
import int
import isinstance
import len
import max_chars
import object
import property
import self
import str
import super


@dataclass(frozen=True)
class ChunkMetadata:
    """Metadata cho chunk."""

    source: str = ""
    page: int | None = None
    section: str | None = None
    tokens: int = 0
    language: str = "en"
    created_at: datetime | None = None
    custom: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Post-init validation."""
        if self.created_at is None:
            object.__setattr__(self, "created_at", datetime.now(UTC))
        if self.custom is None:
            object.__setattr__(self, "custom", {})


class Chunk(BaseEntity):
    """Entity đại diện cho một chunk text."""

    def __init__(
        self,
        text: str,
        doc_id: str,
        chunk_index: int = 0,
        metadata: ChunkMetadata | None = None,
        id: UUID | None = None,
    ) -> None:
        """Tạo Chunk entity.

        Args:
            text: Nội dung text của chunk
            doc_id: ID của document chứa chunk này
            chunk_index: Vị trí chunk trong document
            metadata: Metadata bổ sung
            id: UUID của chunk (auto-generate nếu None)
        """
        super().__init__(id or uuid4())

        if not text.strip():
            raise ValueError("Chunk text không được rỗng")
        if not doc_id.strip():
            raise ValueError("Document ID không được rỗng")
        if chunk_index < 0:
            raise ValueError("Chunk index phải >= 0")

        self._text = text.strip()
        self._doc_id = doc_id.strip()
        self._chunk_index = chunk_index
        self._metadata = metadata or ChunkMetadata()

    @property
    def text(self) -> str:
        """Nội dung text của chunk."""
        return self._text

    @property
    def doc_id(self) -> str:
        """ID của document chứa chunk."""
        return self._doc_id

    @property
    def chunk_index(self) -> int:
        """Vị trí chunk trong document."""
        return self._chunk_index

    @property
    def metadata(self) -> ChunkMetadata:
        """Metadata của chunk."""
        return self._metadata

    @property
    def token_count(self) -> int:
        """Số tokens ước tính (rough)."""
        return len(self._text.split())

    def get_preview(self, max_chars: int = 100) -> str:
        """Lấy preview ngắn của chunk.

        Args:
            max_chars: Số ký tự tối đa

        Returns:
            Text preview
        """
        if len(self._text) <= max_chars:
            return self._text
        return self._text[: max_chars - 3] + "..."

    def __str__(self) -> str:
        """String representation."""
        return f"Chunk({self.doc_id}[{self.chunk_index}]: {self.get_preview(50)})"

    def __repr__(self) -> str:
        """Detailed representation."""
        return (
            f"Chunk(id={self.id}, doc_id='{self.doc_id}', "
            f"index={self.chunk_index}, tokens={self.token_count})"
        )


@dataclass(frozen=True)
class ScoredChunk:
    """Chunk với relevance score từ retrieval."""

    chunk: Chunk
    score: float

    def __post_init__(self) -> None:
        """Post-init validation."""
        if not isinstance(self.chunk, Chunk):
            raise TypeError("chunk phải là Chunk instance")
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("Score phải trong khoảng [0.0, 1.0]")

    @property
    def text(self) -> str:
        """Shortcut để lấy text từ chunk."""
        return self.chunk.text

    @property
    def doc_id(self) -> str:
        """Shortcut để lấy doc_id từ chunk."""
        return self.chunk.doc_id

    def __str__(self) -> str:
        """String representation."""
        return f"ScoredChunk(score={self.score:.3f}, {self.chunk})"
