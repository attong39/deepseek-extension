"""
Cache Database Model - SQLAlchemy 2.x Fixed Version.

Represents cache entries with proper type safety.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel
from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
import bool
import dict
import float
import int
import self
import str


class CacheEntry(BaseModel):
    """Cache entry model for storing cached data."""

    # Cache Identification
    cache_key: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    namespace: Mapped[str] = mapped_column(
        String(100), nullable=False, default="default", index=True
    )

    # Cache Data
    data: Mapped[str] = mapped_column(Text, nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), nullable=False, default="string")
    encoding: Mapped[str] = mapped_column(String(20), nullable=False, default="utf-8")

    # Cache Behavior
    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    access_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_accessed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Tags and metadata
    tags: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    meta_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        """String representation."""
        return f"<CacheEntry(key={self.cache_key}, namespace={self.namespace})>"

    def is_expired(self) -> bool:
        """Check if cache entry is expired."""
        if not self.expires_at:
            return False
        return datetime.now(UTC) > self.expires_at

    def increment_access(self) -> None:
        """Increment access count and update last accessed time."""
        self.access_count += 1
        self.last_accessed_at = datetime.now(UTC)


class CacheStats(BaseModel):
    """Cache statistics tracking model."""

    # Statistics
    namespace: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    total_entries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hit_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    miss_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    eviction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Performance
    avg_access_time_ms: Mapped[float | None] = mapped_column(nullable=True)
    memory_usage_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def get_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0.0

    def record_hit(self) -> None:
        """Record a cache hit."""
        self.hit_count += 1

    def record_miss(self) -> None:
        """Record a cache miss."""
        self.miss_count += 1

    def record_eviction(self) -> None:
        """Record a cache eviction."""
        self.eviction_count += 1


__all__ = ["CacheEntry", "CacheStats"]
