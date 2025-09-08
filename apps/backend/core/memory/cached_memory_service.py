from __future__ import annotations

import hashlib
import json
import logging
import os
from threading import Semaphore
from typing import Any

from apps.backend.core.interfaces.memory_backend import MemoryBackend, MemoryResult
from diskcache import Cache
import backend
import batch_size
import bool
import cache_size
import cache_ttl
import cached_result
import dict
import embedding_model
import filters
import getattr
import hard
import hasattr
import ids
import int
import key
import len
import list
import max_concurrent
import namespace
import records
import self
import str
import target_model
import top_k

"""Caching Layer với Semaphore cho Memory Operations.
Module này cung cấp:
- CachedMemoryService với disk cache
- Semaphore cho concurrent access control
- Cache key generation và invalidation
"""
logger = logging.getLogger(__name__)


class CachedMemoryService:
    """Memory service với caching layer và semaphore protection."""

    def __init__(
        self,
        backend: MemoryBackend,
        cache_dir: str | None = None,
        max_concurrent: int = 10,
        cache_ttl: int = 3600,  # 1 hour
        cache_size: int = 1000,
    ):
        """Initialize cached memory service.
        Args:
            backend: Underlying memory backend
            cache_dir: Directory for cache storage
            max_concurrent: Maximum concurrent operations
            cache_ttl: Cache TTL in seconds
            cache_size: Maximum cache entries
        """
        self.backend = backend
        self.cache_ttl = cache_ttl
        self.cache_size = cache_size
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.zeta_cache")
        os.makedirs(cache_dir, exist_ok=True)
        self._cache = Cache(cache_dir, size_limit=cache_size)
        self._lock = Semaphore(value=max_concurrent)
        logger.info(
            f"Initialized cached memory service with {max_concurrent} concurrent limit"
        )

    def upsert(
        self, namespace: str, records: list[dict], embedding_model: str | None = None
    ) -> MemoryResult:
        """Upsert với cache invalidation.
        Args:
            namespace: Target namespace
            records: Records to upsert
            embedding_model: Optional embedding model
        Returns:
            Upsert result
        """
        result = self.backend.upsert(namespace, records, embedding_model)
        if result.status == "success":
            self._invalidate_namespace_cache(namespace)
            logger.debug(f"Cache invalidated for namespace: {namespace}")
        return result

    def query(
        self,
        namespace: str,
        query: str,
        top_k: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> MemoryResult:
        """Query với cache support.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters
        Returns:
            Query result (cached or fresh)
        """
        cache_key = self._hash_query(namespace, query, top_k, filters)
        with self._lock:
            if cached_result := self._cache.get(cache_key):
                logger.debug(f"Cache hit for query: {cache_key[:16]}...")
                return MemoryResult(**cached_result)
        logger.debug(f"Cache miss for query: {cache_key[:16]}...")
        result = self.backend.query(namespace, query, top_k, filters)
        if result.status == "success" and result.data:
            with self._lock:
                cache_data = result.model_dump()
                self._cache.set(cache_key, cache_data, expire=self.cache_ttl)
                logger.debug(f"Cached result for query: {cache_key[:16]}...")
        return result

    def delete(
        self,
        namespace: str,
        ids: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        hard: bool = False,
    ) -> MemoryResult:
        """Delete với cache invalidation.
        Args:
            namespace: Target namespace
            ids: Record IDs to delete
            filters: Optional filters
            hard: Hard delete flag
        Returns:
            Delete result
        """
        result = self.backend.delete(namespace, ids, filters, hard)
        if result.status == "success":
            self._invalidate_namespace_cache(namespace)
            logger.debug(f"Cache invalidated after delete in namespace: {namespace}")
        return result

    def rebuild_embeddings(
        self, namespace: str, target_model: str, batch_size: int = 256
    ) -> MemoryResult:
        """Rebuild embeddings với cache invalidation.
        Args:
            namespace: Target namespace
            target_model: Target embedding model
            batch_size: Batch size
        Returns:
            Rebuild result
        """
        result = self.backend.rebuild_embeddings(namespace, target_model, batch_size)
        if result.status == "success":
            self._invalidate_namespace_cache(namespace)
            logger.debug(f"Cache invalidated after rebuild in namespace: {namespace}")
        return result

    def _hash_query(
        self, namespace: str, query: str, top_k: int, filters: dict[str, Any] | None
    ) -> str:
        """Generate cache key từ query parameters.
        Args:
            namespace: Target namespace
            query: Search query
            top_k: Number of results
            filters: Optional filters
        Returns:
            Cache key hash
        """
        query_parts = [
            f"ns:{namespace}",
            f"q:{query}",
            f"k:{top_k}",
            f"f:{json.dumps(filters, sort_keys=True) if filters else 'none'}",
        ]
        query_string = "|".join(query_parts)
        return hashlib.sha256(query_string.encode()).hexdigest()

    def _invalidate_namespace_cache(self, namespace: str) -> None:
        """Invalidate all cache entries cho namespace.
        Args:
            namespace: Namespace to invalidate
        """
        keys_to_delete = []
        for key in self._cache:
            keys_to_delete.append(key)
        for key in keys_to_delete:
            del self._cache[key]
        logger.debug(
            f"Invalidated {len(keys_to_delete)} cache entries for namespace: {namespace}"
        )

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.
        Returns:
            Cache statistics
        """
        return {
            "cache_size": len(self._cache),
            "cache_dir": self._cache.directory,
            "max_concurrent": self._lock._value,
            "cache_ttl": self.cache_ttl,
            "hit_rate": getattr(self._cache, "hit_rate", 0.0),
        }

    def clear_cache(self, namespace: str | None = None) -> int:
        """Clear cache entries.
        Args:
            namespace: Optional namespace to clear (None = all)
        Returns:
            Number of entries cleared
        """
        if namespace:
            self._invalidate_namespace_cache(namespace)
            return 1  # Approximate
        else:
            cleared = len(self._cache)
            self._cache.clear()
            logger.info(f"Cleared {cleared} cache entries")
            return cleared

    def __del__(self):
        """Cleanup cache on deletion."""
        if hasattr(self, "_cache"):
            self._cache.close()


__all__ = [
    "CachedMemoryService",
    "cache_data",
    "cache_dir",
    "cache_key",
    "clear_cache",
    "cleared",
    "delete",
    "get_cache_stats",
    "keys_to_delete",
    "logger",
    "query",
    "query_parts",
    "query_string",
    "rebuild_embeddings",
    "result",
    "upsert",
]
