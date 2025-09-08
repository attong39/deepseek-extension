"""Cache model for storing cached data and responses."""

from __future__ import annotations

from apps.backend.data.models.base_model import FullFeaturedBaseModel
from sqlalchemy import JSON, Column, DateTime, Integer, LargeBinary, String, Text


class CacheEntry(FullFeaturedBaseModel):
    """Cache entry model for storing cached data."""
import self
import str

    __tablename__: str = "cache_entries"

    # Cache key and namespace
    cache_key = Column(
        String(255), nullable=False, unique=True, index=True, doc="Unique cache key"
    )
    namespace = Column(
        String(100),
        nullable=False,
        default="default",
        index=True,
        doc="Cache namespace for organization",
    )

    # Cache content
    data_type = Column(
        String(50),
        nullable=False,
        index=True,
        doc="Type of cached data (json, text, binary)",
    )
    text_data = Column(Text, nullable=True, doc="Text-based cache data")
    json_data = Column(JSON, nullable=True, doc="JSON-serializable cache data")
    binary_data = Column(LargeBinary, nullable=True, doc="Binary cache data")

    # Cache metadata
    content_hash = Column(
        String(64),
        nullable=True,
        index=True,
        doc="Hash of the cached content for integrity",
    )
    size_bytes = Column(
        Integer, nullable=False, default=0, doc="Size of cached data in bytes"
    )
    compression = Column(
        String(20), nullable=True, doc="Compression method used (gzip, lz4, etc.)"
    )

    # Cache behavior
    expires_at = Column(
        DateTime, nullable=True, index=True, doc="When the cache entry expires"
    )
    access_count = Column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of times this entry was accessed",
    )
    last_accessed_at = Column(
        DateTime, nullable=True, doc="When the cache entry was last accessed"
    )

    # Tags and metadata
    tags = Column(JSON, nullable=True, doc="Tags for cache entry organization")
    meta_data = Column(
        JSON, nullable=True, doc="Additional metadata about the cached data"
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<CacheEntry(key={self.cache_key}, namespace={self.namespace})>"


class CacheStats(FullFeaturedBaseModel):
    """Cache statistics tracking model."""

    __tablename__: str = "cache_stats"

    # Stats period
    period_start = Column(
        DateTime, nullable=False, index=True, doc="Start of statistics period"
    )
    period_end = Column(
        DateTime, nullable=False, index=True, doc="End of statistics period"
    )
    namespace = Column(String(100), nullable=False, index=True, doc="Cache namespace")

    # Hit/miss statistics
    hit_count = Column(Integer, nullable=False, default=0, doc="Number of cache hits")
    miss_count = Column(
        Integer, nullable=False, default=0, doc="Number of cache misses"
    )
    hit_rate = Column(
        Integer, nullable=False, default=0, doc="Hit rate as percentage (0-100)"
    )

    # Size statistics
    total_entries = Column(
        Integer, nullable=False, default=0, doc="Total number of cache entries"
    )
    total_size_bytes = Column(
        Integer, nullable=False, default=0, doc="Total size of cached data"
    )
    avg_entry_size = Column(
        Integer, nullable=False, default=0, doc="Average size per cache entry"
    )

    # Performance statistics
    avg_access_time_ms = Column(
        Integer, nullable=True, doc="Average cache access time in milliseconds"
    )
    eviction_count = Column(
        Integer, nullable=False, default=0, doc="Number of entries evicted"
    )

    # Additional metrics
    metrics = Column(JSON, nullable=True, doc="Additional cache metrics")

    def __repr__(self) -> str:
        """String representation."""
        return f"<CacheStats(namespace={self.namespace}, hit_rate={self.hit_rate}%)>"
