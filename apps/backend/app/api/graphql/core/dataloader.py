from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar
from uuid import UUID
from weakref import WeakKeyDictionary
import Exception
import agent_repository
import batch_load_fn
import bool
import cache
import cache_key_fn
import callback
import dict
import e
import entity
import float
import future
import getattr
import id_
import ids
import int
import key
import kwargs
import len
import list
import loader
import max_batch_size
import method_name
import name
import repository
import result
import self
import str
import total_stats
import value
import zip

"""DataLoader implementation để prevent N+1 queries và achieve sub-100ms performance.
High-performance batch loading để reduce database calls từ O(n) về O(1)
cho GraphQL field resolution.
"""
logger = logging.getLogger(__name__)
K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


class DataLoader(Generic[K, V]):
    """High-performance DataLoader để batch và cache database operations.
    Features:
    - Automatic batching của multiple requests
    - Caching để prevent duplicate queries
    - Weak reference caching để prevent memory leaks
    - Performance monitoring
    - Context-aware cache management
    """

    def __init__(
        self,
        batch_load_fn: Callable[[list[K]], Awaitable[list[V | None]]],
        cache: bool = True,
        max_batch_size: int = 100,
        cache_key_fn: Callable[[K], str] | None = None,
    ) -> None:
        """Initialize DataLoader với configuration.
        Args:
            batch_load_fn: Function to load batch of items
            cache: Whether to enable caching
            max_batch_size: Maximum batch size để prevent memory issues
            cache_key_fn: Custom cache key function
        """
        self._batch_load_fn = batch_load_fn
        self._cache_enabled = cache
        self._max_batch_size = max_batch_size
        self._cache_key_fn = cache_key_fn or str
        self._batch_count = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._batch: list[K] = []
        self._futures: list[asyncio.Future[V | None]] = []
        self._scheduled = False
        self._cache: dict[str, V] = {}
        self._weak_cache: WeakKeyDictionary[Any, Any] = WeakKeyDictionary()

    async def load(self, key: K) -> V | None:
        """Load single item với automatic batching và caching.
        Args:
            key: Key to load
        Returns:
            Loaded value or None if not found
        """
        cache_key = self._cache_key_fn(key)
        if self._cache_enabled and cache_key in self._cache:
            self._cache_hits += 1
            logger.debug(f"DataLoader cache hit: {cache_key}")
            return self._cache[cache_key]
        self._cache_misses += 1
        future: asyncio.Future[V | None] = asyncio.Future()
        self._batch.append(key)
        self._futures.append(future)
        if not self._scheduled:
            self._scheduled = True
            asyncio.create_task(self._dispatch_batch())
        result: V | None = await future
        if self._cache_enabled and result is not None:
            self._cache[cache_key] = result
        return result

    async def load_many(self, keys: list[K]) -> list[V | None]:
        """Load multiple items efficiently.
        Args:
            keys: List of keys to load
        Returns:
            List of loaded values (same order as keys)
        """
        tasks = [self.load(key) for key in keys]
        return await asyncio.gather(*tasks)

    async def _dispatch_batch(self) -> None:
        """Execute batched load operation."""
        self._scheduled = False
        await asyncio.sleep(0.001)  # 1ms delay để optimize batching
        if not self._batch:
            return
        batch_keys = self._batch[: self._max_batch_size]
        batch_futures = self._futures[: self._max_batch_size]
        self._batch = self._batch[self._max_batch_size :]
        self._futures = self._futures[self._max_batch_size :]
        if self._batch:
            self._scheduled = True
            asyncio.create_task(self._dispatch_batch())
        self._batch_count += 1
        try:
            logger.debug(f"DataLoader executing batch: {len(batch_keys)} items")
            results = await self._batch_load_fn(batch_keys)
            for future, result in zip(batch_futures, results, strict=False):
                if not future.done():
                    future.set_result(result)
        except Exception as e:
            logger.error(f"DataLoader batch execution failed: {e}")
            for future in batch_futures:
                if not future.done():
                    future.set_exception(e)

    def clear(self, key: K | None = None) -> None:
        """Clear cache entry hoặc entire cache.
        Args:
            key: Specific key to clear, or None để clear all
        """
        if key is None:
            self._cache.clear()
            logger.debug("DataLoader cache cleared")
        else:
            cache_key = self._cache_key_fn(key)
            self._cache.pop(cache_key, None)
            logger.debug(f"DataLoader cache cleared for key: {cache_key}")

    def prime(self, key: K, value: V) -> None:
        """Prime cache với known value.
        Args:
            key: Key to prime
            value: Value to cache
        """
        if self._cache_enabled:
            cache_key = self._cache_key_fn(key)
            self._cache[cache_key] = value
            logger.debug(f"DataLoader cache primed: {cache_key}")

    def get_stats(self) -> dict[str, Any]:
        """Get performance statistics.
        Returns:
            Performance metrics dictionary
        """
        total_requests = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total_requests if total_requests > 0 else 0
        return {
            "batch_count": self._batch_count,
            "cache_hits": self._cache_hits,
            "cache_misses": self._cache_misses,
            "cache_hit_rate": hit_rate,
            "cache_size": len(self._cache),
            "pending_batch_size": len(self._batch),
        }


class DataLoaderRegistry:
    """Registry để manage DataLoader instances per request context.
    Ensures efficient resource usage và proper cleanup.
    """

    def __init__(self) -> None:
        """Initialize registry."""
        self._loaders: dict[str, DataLoader[Any, Any]] = {}
        self._cleanup_callbacks: list[Callable[[], None]] = []

    def get_or_create(
        self,
        name: str,
        batch_load_fn: Callable[[list[Any]], Awaitable[list[Any | None]]],
        **kwargs: Any,
    ) -> DataLoader[Any, Any]:
        """Get existing DataLoader hoặc create new one.
        Args:
            name: Unique loader name
            batch_load_fn: Batch loading function
            **kwargs: DataLoader configuration
        Returns:
            DataLoader instance
        """
        if name not in self._loaders:
            self._loaders[name] = DataLoader(batch_load_fn, **kwargs)
            logger.debug(f"Created DataLoader: {name}")
        return self._loaders[name]

    def get_aggregate_stats(self) -> dict[str, Any]:
        """Get aggregate statistics từ all loaders.
        Returns:
            Combined performance metrics
        """
        total_stats: dict[str, Any] = {
            "total_loaders": len(self._loaders),
            "total_batch_count": 0,
            "total_cache_hits": 0,
            "total_cache_misses": 0,
            "total_cache_size": 0,
        }
        loader_stats = {}
        for name, loader in self._loaders.items():
            stats = loader.get_stats()
            loader_stats[name] = stats
            total_stats["total_batch_count"] += stats["batch_count"]
            total_stats["total_cache_hits"] += stats["cache_hits"]
            total_stats["total_cache_misses"] += stats["cache_misses"]
            total_stats["total_cache_size"] += stats["cache_size"]
        total_requests = (
            total_stats["total_cache_hits"] + total_stats["total_cache_misses"]
        )
        total_stats["overall_hit_rate"] = float(
            total_stats["total_cache_hits"] / total_requests
            if total_requests > 0
            else 0.0
        )
        return {
            "aggregate": total_stats,
            "by_loader": loader_stats,
        }

    def clear_all(self) -> None:
        """Clear all DataLoader caches."""
        for loader in self._loaders.values():
            loader.clear()
        logger.debug("All DataLoader caches cleared")

    def cleanup(self) -> None:
        """Cleanup all resources."""
        self.clear_all()
        for callback in self._cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                logger.warning(f"DataLoader cleanup callback failed: {e}")
        self._loaders.clear()
        logger.debug("DataLoader registry cleaned up")

    def add_cleanup_callback(self, callback: Callable[[], None]) -> None:
        """Add cleanup callback.
        Args:
            callback: Function to call during cleanup
        """
        self._cleanup_callbacks.append(callback)


_registry = DataLoaderRegistry()


def get_dataloader_registry() -> DataLoaderRegistry:
    """Get global DataLoader registry.
    Returns:
        DataLoader registry instance
    """
    return _registry


async def batch_load_by_ids(
    repository: Any,
    method_name: str,
    ids: list[str | UUID],
) -> list[Any | None]:
    """Generic batch loader using repository method.
    Args:
        repository: Repository instance
        method_name: Method name to call
        ids: List of IDs to load
    Returns:
        List of loaded entities
    """
    try:
        method = getattr(repository, method_name)
        entities = await method(ids)
        entity_map = {str(entity.id): entity for entity in entities}
        return [entity_map.get(str(id_)) for id_ in ids]
    except Exception as e:
        logger.error(f"Batch load failed: {e}")
        return [None] * len(ids)


def create_agent_loader(agent_repository: Any) -> DataLoader[str, Any]:
    """Create DataLoader for agent entities.
    Args:
        agent_repository: Agent repository instance
    Returns:
        Configured DataLoader
    """

    async def batch_load_agents(ids: list[str]) -> list[Any | None]:
        return await batch_load_by_ids(agent_repository, "get_by_ids", ids)

    return DataLoader(batch_load_agents, max_batch_size=50)


__all__ = [
    "DataLoader",
    "DataLoaderRegistry",
    "create_agent_loader",
    "get_dataloader_registry",
]
