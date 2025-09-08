"""Enhanced RAG cache with 2-tier architecture (LRU + Redis).

This module provides production-ready caching for ZETA_AI 2025:
- Two-tier caching: In-memory LRU + Redis fallback
- Configurable serialization for complex objects
- TTL support with automatic expiration
- Performance metrics and health monitoring
- Graceful failure handling

Architecture:
- Tier 1: In-memory LRU (fastest access, ~1μs)
- Tier 2: Redis (persistent, shared, ~100μs)
- Smart promotion: Redis hits promoted to memory
"""

from __future__ import annotations

import json
import pickle
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
import Exception
import ImportError
import bool
import bytes
import capacity
import data
import deserializer
import dict
import e
import enable_redis
import float
import int
import isinstance
import k
import key
import key_prefix
import len
import obj
import print
import property
import redis_url
import result
import self
import serializer
import str
import ttl_seconds
import v

# Optional Redis dependency
try:
    import redis as _redis
except ImportError:
    _redis = None


# === Enhanced LRU Cache with Redis Fallback ===

K = TypeVar("K")
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """Simple LRU cache implementation."""

    def __init__(self, capacity: int = 256):
        self.capacity = capacity
        self._d: OrderedDict[K, V] = OrderedDict()

    def get(self, k: K) -> V | None:
        """Get value by key, marking as recently used."""
        if k in self._d:
            self._d.move_to_end(k)
            return self._d[k]
        return None

    def put(self, k: K, v: V) -> None:
        """Put key-value pair, evicting LRU if necessary."""
        if k in self._d:
            self._d.move_to_end(k)
        self._d[k] = v
        if len(self._d) > self.capacity:
            self._d.popitem(last=False)

    def size(self) -> int:
        """Get current cache size."""
        return len(self._d)

    def clear(self) -> None:
        """Clear all cached items."""
        self._d.clear()


# === Serialization Strategies ===


def json_serializer(obj: Any) -> bytes:
    """JSON serialization with UTF-8 encoding."""
    return json.dumps(obj, ensure_ascii=False, default=str).encode("utf-8")


def json_deserializer(data: bytes) -> Any:
    """JSON deserialization from UTF-8 bytes."""
    return json.loads(data.decode("utf-8"))


def pickle_serializer(obj: Any) -> bytes:
    """Pickle serialization for complex Python objects."""
    return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)


def pickle_deserializer(data: bytes) -> Any:
    """Pickle deserialization."""
    return pickle.loads(data)


@dataclass
class CacheStats:
    """Cache performance statistics."""

    memory_hits: int = 0
    memory_misses: int = 0
    redis_hits: int = 0
    redis_misses: int = 0
    memory_size: int = 0
    memory_capacity: int = 0

    @property
    def total_hits(self) -> int:
        return self.memory_hits + self.redis_hits

    @property
    def total_misses(self) -> int:
        return self.memory_misses + self.redis_misses

    @property
    def hit_rate(self) -> float:
        total = self.total_hits + self.total_misses
        return self.total_hits / total if total > 0 else 0.0

    @property
    def redis_hit_rate(self) -> float:
        redis_total = self.redis_hits + self.redis_misses
        return self.redis_hits / redis_total if redis_total > 0 else 0.0


class EnhancedLRUCache(Generic[K, V]):
    """
    Enhanced LRU cache with Redis fallback and custom serialization.

    Two-tier caching architecture:
    1. In-memory LRU (fastest access, ~1μs)
    2. Redis fallback (persistent, shared, ~100μs)

    Features:
    - Custom serialization/deserialization for complex objects
    - TTL support for automatic expiration
    - Hit/miss metrics tracking
    - Graceful Redis failure handling
    - Smart promotion: Redis hits promoted to memory
    """

    def __init__(
        self,
        capacity: int = 512,
        redis_url: str | None = None,
        serializer: Callable[[V], bytes] | None = None,
        deserializer: Callable[[bytes], V] | None = None,
        ttl_seconds: int | None = None,
        key_prefix: str = "rag:",
        enable_redis: bool = True,
    ):
        """
        Initialize enhanced LRU cache.

        Args:
            capacity: In-memory LRU capacity
            redis_url: Redis connection URL (optional)
            serializer: Function to serialize values to bytes
            deserializer: Function to deserialize bytes to values
            ttl_seconds: Time-to-live for Redis entries (default: 1 hour)
            key_prefix: Prefix for Redis keys
            enable_redis: Whether to enable Redis fallback
        """
        self._lru = LRUCache[K, V](capacity)
        self._ttl_seconds = ttl_seconds or 3600  # 1 hour default
        self._key_prefix = key_prefix
        self._enable_redis = enable_redis

        # Default to JSON serialization
        self._serializer = serializer or json_serializer
        self._deserializer = deserializer or json_deserializer

        # Redis connection (optional)
        self._redis = None
        if enable_redis and redis_url and _redis:
            try:
                self._redis = _redis.from_url(
                    redis_url,
                    decode_responses=False,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                )
                # Test connection
                self._redis.ping()
            except Exception as e:
                # Log warning but continue without Redis
                print(f"Warning: Redis connection failed: {e}")
                self._redis = None

        # Statistics
        self._stats = CacheStats()
        self._last_stats_reset = time.time()

    def _make_redis_key(self, key: K) -> str:
        """Generate Redis key with prefix."""
        return f"{self._key_prefix}{str(key)}"

    def get(self, key: K) -> V | None:
        """
        Get value with two-tier lookup.

        1. Check in-memory LRU first
        2. Fallback to Redis if available
        3. Promote Redis hits to in-memory cache
        """
        # Tier 1: In-memory LRU
        value = self._lru.get(key)
        if value is not None:
            self._stats.memory_hits += 1
            return value

        self._stats.memory_misses += 1

        # Tier 2: Redis fallback
        if self._redis is not None:
            try:
                redis_key = self._make_redis_key(key)
                raw_data = self._redis.get(redis_key)

                if raw_data is not None:
                    # Deserialize and promote to in-memory cache
                    value = self._deserializer(raw_data)
                    self._lru.put(key, value)  # Promote to LRU

                    self._stats.redis_hits += 1
                    return value
                else:
                    self._stats.redis_misses += 1
            except Exception as e:
                # Log Redis error but continue
                print(f"Redis get error for key {key}: {e}")
                self._stats.redis_misses += 1

        return None

    def put(self, key: K, value: V) -> None:
        """
        Put value in both tiers.

        1. Store in in-memory LRU
        2. Store in Redis if available and serializer provided
        """
        # Tier 1: In-memory
        self._lru.put(key, value)

        # Tier 2: Redis
        if self._redis is not None:
            try:
                redis_key = self._make_redis_key(key)
                serialized_data = self._serializer(value)

                self._redis.setex(redis_key, self._ttl_seconds, serialized_data)
            except Exception as e:
                # Log Redis error but continue
                print(f"Redis put error for key {key}: {e}")

    def delete(self, key: K) -> bool:
        """Delete key from both tiers."""
        deleted = False

        # Remove from in-memory cache
        if key in self._lru._d:
            del self._lru._d[key]
            deleted = True

        # Remove from Redis
        if self._redis is not None:
            try:
                redis_key = self._make_redis_key(key)
                _ = self._redis.delete(redis_key)
                deleted = deleted or bool(result)
            except Exception as e:
                print(f"Redis delete error for key {key}: {e}")

        return deleted

    def clear(self) -> None:
        """Clear both in-memory and Redis caches."""
        self._lru.clear()

        if self._redis is not None:
            try:
                # Delete all keys with our prefix
                pattern = f"{self._key_prefix}*"
                keys = self._redis.keys(pattern)
                if keys:
                    self._redis.delete(*keys)
            except Exception as e:
                print(f"Redis clear error: {e}")

    def size(self) -> int:
        """Get in-memory cache size."""
        self._stats.memory_size = self._lru.size()
        self._stats.memory_capacity = self._lru.capacity
        return self._stats.memory_size

    def get_stats(self) -> CacheStats:
        """Get cache performance statistics."""
        self._stats.memory_size = self._lru.size()
        self._stats.memory_capacity = self._lru.capacity
        return self._stats

    def reset_stats(self) -> None:
        """Reset performance statistics."""
        self._stats = CacheStats()
        self._last_stats_reset = time.time()

    def health_check(self) -> dict[str, Any]:
        """Check cache health status."""
        health = {
            "memory_cache": "healthy",
            "redis_cache": "not_configured" if not self._enable_redis else "disabled",
            "redis_available": False,
        }

        if self._redis is not None:
            try:
                latency = self._redis.ping()
                health["redis_cache"] = "healthy"
                health["redis_available"] = True
                health["redis_latency_ms"] = (
                    latency * 1000 if isinstance(latency, float) else None
                )
            except Exception as e:
                health["redis_cache"] = f"unhealthy: {e}"
                health["redis_available"] = False

        return health

    def get_redis_info(self) -> dict[str, Any] | None:
        """Get Redis server information."""
        if self._redis is None:
            return None

        try:
            info = self._redis.info()
            return {
                "redis_version": info.get("redis_version"),
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses"),
            }
        except Exception as e:
            return {"error": str(e)}


# === Factory Functions ===


def create_rag_cache(
    redis_url: str | None = None, capacity: int = 512, ttl_seconds: int = 3600
) -> EnhancedLRUCache[str, Any]:
    """
    Create a RAG cache optimized for retrieval results.

    Args:
        redis_url: Redis connection URL
        capacity: In-memory cache capacity
        ttl_seconds: Time-to-live for cached items

    Returns:
        Enhanced cache instance
    """
    return EnhancedLRUCache[str, Any](
        capacity=capacity,
        redis_url=redis_url,
        serializer=json_serializer,
        deserializer=json_deserializer,
        ttl_seconds=ttl_seconds,
        key_prefix="rag:retrieval:",
        enable_redis=redis_url is not None,
    )


def create_embedding_cache(
    redis_url: str | None = None, capacity: int = 1024, ttl_seconds: int = 7200
) -> EnhancedLRUCache[str, Any]:
    """
    Create a cache optimized for embeddings (binary serialization).

    Args:
        redis_url: Redis connection URL
        capacity: In-memory cache capacity
        ttl_seconds: Time-to-live for cached embeddings

    Returns:
        Enhanced cache instance with pickle serialization
    """
    return EnhancedLRUCache[str, Any](
        capacity=capacity,
        redis_url=redis_url,
        serializer=pickle_serializer,
        deserializer=pickle_deserializer,
        ttl_seconds=ttl_seconds,
        key_prefix="rag:embeddings:",
        enable_redis=redis_url is not None,
    )
