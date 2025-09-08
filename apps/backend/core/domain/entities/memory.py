"""
Memory Entity - Domain-driven design pattern.

Entity lưu trữ memory/knowledge với embedding vector.
Immutable design với strong validation và business logic.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from app._base_model import DomainModel
from pydantic import Field, field_validator, model_validator
import ValueError
import bool
import case_sensitive
import category
import classmethod
import clear_embedding
import default
import dict
import embedding
import enumerate
import float
import i
import importance
import int
import isinstance
import key
import len
import metadata
import self
import sorted
import str
import text
import threshold
import tuple
import v
import val
import value

# Vector embedding dimensions được support
_SUPPORTED_EMBEDDING_DIMS = {384, 512, 768, 1024, 1536}


class MemoryImportance(str, Enum):
    """Memory importance levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Memory(DomainModel):
    """
    Memory entity cho AI agent knowledge storage.

    Lưu trữ content với vector embedding để semantic search.
    Immutable với strong validation rules.

    Business Rules:
    - content không được rỗng
    - embedding dimension phải được support
    - metadata keys phải là valid identifiers
    - importance score trong khoảng [0.0, 1.0]

    Examples:
        # Tạo memory đơn giản
        memory = Memory(
            owner_agent_id=agent_id,
            content="User prefers Python over JavaScript"
        )

        # Memory với embedding
        memory = Memory(
            owner_agent_id=agent_id,
            content="Technical discussion about FastAPI",
            embedding=vector_from_model,
            importance=0.8
        )

        # Cập nhật metadata
        updated = memory.with_metadata({"topic": "programming", "source": "conversation"})
    """

    # Identity
    id: UUID = Field(default_factory=uuid4, description="Unique identifier cho Memory")

    owner_agent_id: UUID = Field(..., description="ID của agent sở hữu memory này")

    # Core content
    content: str = Field(
        ..., min_length=1, max_length=50000, description="Nội dung text của memory"
    )

    # Vector embedding cho semantic search
    embedding: tuple[float, ...] = Field(
        default=(), description="Vector embedding của content"
    )

    # Metadata và context
    metadata: dict[str, str] = Field(
        default_factory=dict, description="Metadata key-value pairs"
    )

    # Business attributes
    importance: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Độ quan trọng của memory [0.0, 1.0]"
    )

    access_count: int = Field(
        default=0, ge=0, description="Số lần memory được truy cập"
    )

    source: str = Field(
        default="user_input", max_length=100, description="Nguồn gốc của memory"
    )

    category: str = Field(
        default="general", max_length=50, description="Phân loại memory"
    )

    @field_validator("content")
    @classmethod
    def _validate_content(cls, v: str) -> str:
        """Validate content không rỗng và trim whitespace."""
        content = v.strip()
        if not content:
            raise ValueError("Memory content must not be empty")
        return content

    @field_validator("embedding")
    @classmethod
    def _validate_embedding(cls, v: tuple[float, ...]) -> tuple[float, ...]:
        """
        Validate embedding dimension và values.

        Returns:
            Valid embedding vector

        Raises:
            ValueError: Nếu dimension không được support hoặc có NaN/Inf
        """
        if not v:  # Empty embedding OK
            return v

        # Kiểm tra dimension
        if len(v) not in _SUPPORTED_EMBEDDING_DIMS:
            raise ValueError(
                f"Embedding dimension {len(v)} not supported. "
                f"Supported: {sorted(_SUPPORTED_EMBEDDING_DIMS)}"
            )

        # Kiểm tra values hợp lệ
        for i, val in enumerate(v):
            if not isinstance(val, (int, float)):
                raise ValueError(f"Embedding value at index {i} must be numeric")
            if not (-10.0 <= val <= 10.0):  # Reasonable range
                raise ValueError(
                    f"Embedding value at index {i} out of range [-10, 10]: {val}"
                )

        return v

    @field_validator("metadata")
    @classmethod
    def _validate_metadata(cls, v: dict[str, str]) -> dict[str, str]:
        """
        Validate metadata keys và values.

        Returns:
            Valid metadata dict

        Raises:
            ValueError: Nếu key/value không hợp lệ
        """
        if not v:
            return v

        validated = {}
        for key, value in v.items():
            # Validate key
            if not isinstance(key, str) or not key.strip():
                raise ValueError("Metadata keys must be non-empty strings")

            clean_key = key.strip().lower()
            if not clean_key.replace("_", "").replace("-", "").isalnum():
                raise ValueError(
                    f"Metadata key '{key}' must be alphanumeric with _ or -"
                )

            # Validate value
            if not isinstance(value, str):
                raise ValueError("Metadata values must be strings")

            if len(value) > 500:
                raise ValueError(f"Metadata value too long: {len(value)} > 500")

            validated[clean_key] = value.strip()

        return validated

    @model_validator(mode="after")
    def _validate_consistency(self) -> Memory:
        """Validate business rules consistency."""
        # Nếu có embedding thì content phải đủ dài để có nghĩa
        if self.embedding and len(self.content.strip()) < 10:
            raise ValueError("Content too short for meaningful embedding")

        return self

    # === Business Methods ===

    def access(self) -> Memory:
        """
        Ghi nhận việc truy cập memory.

        Returns:
            Memory mới với access_count tăng và updated timestamp
        """
        return self.model_copy(
            update={
                "access_count": self.access_count + 1,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def with_embedding(self, embedding: tuple[float, ...]) -> Memory:
        """
        Cập nhật embedding vector.

        Args:
            embedding: Vector embedding mới

        Returns:
            Memory mới với embedding đã cập nhật
        """
        return self.model_copy(
            update={
                "embedding": self._validate_embedding(embedding),
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def with_metadata(self, metadata: dict[str, str]) -> Memory:
        """
        Cập nhật metadata.

        Args:
            metadata: Metadata mới (replace toàn bộ)

        Returns:
            Memory mới với metadata đã cập nhật
        """
        return self.model_copy(
            update={
                "metadata": self._validate_metadata(metadata),
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def add_metadata(self, key: str, value: str) -> Memory:
        """
        Thêm một metadata entry.

        Args:
            key: Metadata key
            value: Metadata value

        Returns:
            Memory mới với metadata entry đã thêm
        """
        new_metadata = dict(self.metadata)
        new_metadata[key] = value
        return self.with_metadata(new_metadata)

    def remove_metadata(self, key: str) -> Memory:
        """
        Xóa một metadata entry.

        Args:
            key: Metadata key cần xóa

        Returns:
            Memory mới với metadata entry đã xóa
        """
        new_metadata = dict(self.metadata)
        new_metadata.pop(key.strip().lower(), None)
        return self.with_metadata(new_metadata)

    def set_importance(self, importance: float) -> Memory:
        """
        Cập nhật độ quan trọng.

        Args:
            importance: Importance score [0.0, 1.0]

        Returns:
            Memory mới với importance đã cập nhật
        """
        if not 0.0 <= importance <= 1.0:
            raise ValueError("Importance must be between 0.0 and 1.0")

        return self.model_copy(
            update={
                "importance": importance,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    def update_content(self, content: str, clear_embedding: bool = True) -> Memory:
        """
        Cập nhật content và optionally clear embedding.

        Args:
            content: Content mới
            clear_embedding: Có xóa embedding cũ không (default: True)

        Returns:
            Memory mới với content đã cập nhật
        """
        update_data = {
            "content": self._validate_content(content),
            "updated_at": datetime.now(UTC),
            "version": self.version + 1,
        }

        if clear_embedding:
            update_data["embedding"] = ()

        return self.model_copy(update=update_data)

    # === Query Methods ===

    def has_embedding(self) -> bool:
        """Kiểm tra memory có embedding không."""
        return len(self.embedding) > 0

    def has_metadata(self, key: str) -> bool:
        """Kiểm tra có metadata key không."""
        return key.strip().lower() in self.metadata

    def get_metadata(self, key: str, default: str = "") -> str:
        """Lấy metadata value với default."""
        return self.metadata.get(key.strip().lower(), default)

    def is_important(self, threshold: float = 0.7) -> bool:
        """Kiểm tra memory có quan trọng không."""
        return self.importance >= threshold

    def is_frequently_accessed(self, threshold: int = 5) -> bool:
        """Kiểm tra memory có được truy cập thường xuyên không."""
        return self.access_count >= threshold

    def matches_category(self, category: str) -> bool:
        """Kiểm tra memory thuộc category."""
        return self.category.lower() == category.strip().lower()

    def content_contains(self, text: str, case_sensitive: bool = False) -> bool:
        """Kiểm tra content có chứa text không."""
        content = self.content if case_sensitive else self.content.lower()
        search_text = text if case_sensitive else text.lower()
        return search_text in content


__all__ = ["Memory", "MemoryImportance"]
