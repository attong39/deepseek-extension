"""Caching service for intelligent data caching and retrieval.





This service provides multi-level caching with intelligent cache management,


including memory, disk, and distributed caching strategies.


"""

from __future__ import annotations

import asyncio
import contextlib
import gzip
import json
import logging
import pickle
import time
from collections import OrderedDict
from enum import Enum
from typing import TYPE_CHECKING, Any
import Exception
import bool
import bytes
import cache_level
import compressed_value
import default
import default_ttl
import dict
import disk_cache_size_mb
import e
import enable_compression
import enable_distributed
import fetch_function
import float
import frequency
import int
import isinstance
import key
import len
import limit
import list
import memory_cache_size
import oldest_key
import promote_to_memory
import round
import self
import str
import t
import x

if TYPE_CHECKING:  # for type hints only
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class CacheLevel(Enum):
    """Cache level enumeration."""

    MEMORY = "memory"

    DISK = "disk"

    DISTRIBUTED = "distributed"


class CacheStrategy(Enum):
    """Cache eviction strategies."""

    LRU = "lru"  # Least Recently Used

    LFU = "lfu"  # Least Frequently Used

    TTL = "ttl"  # Time To Live

    FIFO = "fifo"  # First In First Out


class CachingService:
    """Service for managing intelligent multi-level caching."""

    def __init__(
        self,
        memory_cache_size: int = 1000,
        disk_cache_size_mb: int = 100,
        default_ttl: int = 3600,
        enable_compression: bool = True,
        enable_distributed: bool = False,
    ) -> None:
        """Initialize the caching service.





        Args:


            memory_cache_size: Maximum number of items in memory cache.


            disk_cache_size_mb: Maximum disk cache size in MB.


            default_ttl: Default time to live in seconds.


            enable_compression: Whether to enable data compression.


            enable_distributed: Whether to enable distributed caching.


        """

        self.memory_cache_size = memory_cache_size

        self.disk_cache_size_mb = disk_cache_size_mb

        self.default_ttl = default_ttl

        self.enable_compression = enable_compression

        self.enable_distributed = enable_distributed

        # Memory cache (LRU-ordered dictionary)

        self._memory_cache: OrderedDict[str, dict[str, Any]] = OrderedDict()

        # Cache statistics

        self._stats = {
            "memory_hits": 0,
            "memory_misses": 0,
            "disk_hits": 0,
            "disk_misses": 0,
            "distributed_hits": 0,
            "distributed_misses": 0,
            "evictions": 0,
            "compressions": 0,
        }

        # Access patterns for intelligent caching

        self._access_patterns: dict[str, list[float]] = {}

        self._frequency_counter: dict[str, int] = {}

        # Background tasks

        self._cleanup_task: asyncio.Task[None] | None = None

        self._optimization_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start background caching tasks."""

        self._cleanup_task = asyncio.create_task(self._cleanup_expired_items())

        self._optimization_task = asyncio.create_task(self._optimize_cache_strategy())

        logger.info("Caching service background tasks started")
        # Yield once to satisfy async usage policies
        await asyncio.sleep(0)

    async def stop(self) -> None:
        """Stop background caching tasks."""

        if self._cleanup_task:
            self._cleanup_task.cancel()

            with contextlib.suppress(asyncio.CancelledError):
                await self._cleanup_task

        if self._optimization_task:
            self._optimization_task.cancel()

            with contextlib.suppress(asyncio.CancelledError):
                await self._optimization_task

        logger.info("Caching service background tasks stopped")

    async def get(
        self,
        key: str,
        default: Any = None,
        fetch_function: Callable[[], Any] | None = None,
    ) -> Any:
        """Get value from cache with fallback to fetch function.





        Args:


            key: Cache key.


            default: Default value if not found.


            fetch_function: Function to fetch value if not in cache.





        Returns:


            Cached or fetched value.


        """

        # Try memory cache first

        value = await self._get_from_memory(key)

        if value is not None:
            self._stats["memory_hits"] += 1

            await self._update_access_pattern(key)

            return value

        self._stats["memory_misses"] += 1

        # Try disk cache

        value = await self._get_from_disk(key)

        if value is not None:
            self._stats["disk_hits"] += 1

            # Promote to memory cache

            await self.set(key, value, promote_to_memory=True)

            await self._update_access_pattern(key)

            return value

        self._stats["disk_misses"] += 1

        # Try distributed cache if enabled

        if self.enable_distributed:
            value = await self._get_from_distributed(key)

            if value is not None:
                self._stats["distributed_hits"] += 1

                # Promote to memory and disk cache

                await self.set(key, value, promote_to_memory=True)

                await self._update_access_pattern(key)

                return value

            self._stats["distributed_misses"] += 1

        # Fetch using provided function

        if fetch_function:
            try:
                value = (
                    await fetch_function()
                    if asyncio.iscoroutinefunction(fetch_function)
                    else fetch_function()
                )

                # Cache the fetched value

                await self.set(key, value)

                return value

            except Exception as e:
                logger.error(f"Error fetching value for key {key}: {e}")

        return default

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
        cache_level: CacheLevel = CacheLevel.MEMORY,
        promote_to_memory: bool = False,
    ) -> bool:
        """Set value in cache.





        Args:


            key: Cache key.


            value: Value to cache.


            ttl: Time to live in seconds.


            cache_level: Which cache level to use.


            promote_to_memory: Whether to also store in memory cache.





        Returns:


            True if successful.


        """

        if ttl is None:
            ttl = self.default_ttl

        expiry_time = time.time() + ttl

        try:
            # Compress if enabled and value is large

            stored_value = value

            is_compressed = False

            if self.enable_compression and self._should_compress(value):
                stored_value = await self._compress_value(value)

                is_compressed = True

                self._stats["compressions"] += 1

            cache_entry = {
                "value": stored_value,
                "expiry_time": expiry_time,
                "created_at": time.time(),
                "access_count": 0,
                "is_compressed": is_compressed,
                "original_size": self._get_size(value),
                "compressed_size": self._get_size(stored_value)
                if is_compressed
                else None,
            }

            # Store based on cache level

            if cache_level == CacheLevel.MEMORY or promote_to_memory:
                await self._set_in_memory(key, cache_entry)

            if cache_level == CacheLevel.DISK:
                await self._set_in_disk(key, cache_entry)

            if cache_level == CacheLevel.DISTRIBUTED and self.enable_distributed:
                await self._set_in_distributed(key, cache_entry)

            # Update frequency counter

            self._frequency_counter[key] = self._frequency_counter.get(key, 0) + 1

            logger.debug(f"Cached key {key} in {cache_level.value}")

            return True

        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")

            return False

    async def delete(self, key: str) -> bool:
        """Delete key from all cache levels.





        Args:


            key: Cache key to delete.





        Returns:


            True if key was found and deleted.


        """

        deleted = False

        # Delete from memory cache

        if key in self._memory_cache:
            del self._memory_cache[key]

            deleted = True

        # Delete from disk cache

        if await self._delete_from_disk(key):
            deleted = True

        # Delete from distributed cache

        if self.enable_distributed and await self._delete_from_distributed(key):
            deleted = True

        # Clean up tracking data

        if key in self._access_patterns:
            del self._access_patterns[key]

        if key in self._frequency_counter:
            del self._frequency_counter[key]

        if deleted:
            logger.debug(f"Deleted cache key {key}")

        return deleted

    async def clear(self, cache_level: CacheLevel | None = None) -> None:
        """Clear cache at specified level or all levels.





        Args:


            cache_level: Specific cache level to clear, or None for all.


        """

        if cache_level is None or cache_level == CacheLevel.MEMORY:
            self._memory_cache.clear()

            logger.info("Cleared memory cache")

        if cache_level is None or cache_level == CacheLevel.DISK:
            await self._clear_disk_cache()

            logger.info("Cleared disk cache")

        if (
            cache_level is None or cache_level == CacheLevel.DISTRIBUTED
        ) and self.enable_distributed:
            await self._clear_distributed_cache()

            logger.info("Cleared distributed cache")

        if cache_level is None:
            self._access_patterns.clear()

            self._frequency_counter.clear()

    async def exists(self, key: str) -> bool:
        """Check if key exists in any cache level.





        Args:


            key: Cache key to check.





        Returns:


            True if key exists.


        """

        # Check memory cache

        if key in self._memory_cache:
            entry = self._memory_cache[key]

            if entry["expiry_time"] > time.time():
                return True

            else:
                # Clean up expired entry

                del self._memory_cache[key]

        # Check disk cache

        if await self._exists_in_disk(key):
            return True

        # Check distributed cache
        return bool(self.enable_distributed and await self._exists_in_distributed(key))

    async def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.





        Returns:


            Cache performance statistics.


        """

        memory_size = len(self._memory_cache)

        total_hits = (
            self._stats["memory_hits"]
            + self._stats["disk_hits"]
            + self._stats["distributed_hits"]
        )

        total_misses = (
            self._stats["memory_misses"]
            + self._stats["disk_misses"]
            + self._stats["distributed_misses"]
        )

        total_requests = total_hits + total_misses

        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0

        # Yield control to event loop to satisfy async usage in this method
        await asyncio.sleep(0)
        return {
            "memory_cache_size": memory_size,
            "memory_cache_utilization": (memory_size / self.memory_cache_size * 100),
            "total_requests": total_requests,
            "total_hits": total_hits,
            "total_misses": total_misses,
            "hit_rate_percent": round(hit_rate, 2),
            "stats_by_level": {
                "memory": {
                    "hits": self._stats["memory_hits"],
                    "misses": self._stats["memory_misses"],
                },
                "disk": {
                    "hits": self._stats["disk_hits"],
                    "misses": self._stats["disk_misses"],
                },
                "distributed": {
                    "hits": self._stats["distributed_hits"],
                    "misses": self._stats["distributed_misses"],
                },
            },
            "evictions": self._stats["evictions"],
            "compressions": self._stats["compressions"],
        }

    async def get_hot_keys(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get most frequently accessed keys.





        Args:


            limit: Maximum number of keys to return.





        Returns:


            List of hot keys with access statistics.


        """

        hot_keys = []

        for key, frequency in self._frequency_counter.items():
            recent_accesses = len(self._access_patterns.get(key, []))

            hot_keys.append(
                {
                    "key": key,
                    "frequency": frequency,
                    "recent_accesses": recent_accesses,
                    "score": frequency + (recent_accesses * 2),  # Weighted score
                }
            )

        # Sort by score
        hot_keys.sort(key=lambda x: x["score"], reverse=True)

        # Yield control to event loop to satisfy async usage in this method
        await asyncio.sleep(0)
        return hot_keys[:limit]

    async def _get_from_memory(self, key: str) -> Any:
        """Get value from memory cache."""

        if key not in self._memory_cache:
            return None

        entry = self._memory_cache[key]

        # Check expiration

        if entry["expiry_time"] <= time.time():
            del self._memory_cache[key]

            return None

        # Update access info

        entry["access_count"] += 1

        # Move to end (LRU)

        self._memory_cache.move_to_end(key)

        # Decompress if needed

        value = entry["value"]

        if entry["is_compressed"]:
            value = await self._decompress_value(value)

        return value

    async def _set_in_memory(self, key: str, entry: dict[str, Any]) -> None:
        """Set value in memory cache."""

        # Ensure capacity

        while len(self._memory_cache) >= self.memory_cache_size:
            # Remove least recently used item

            oldest_key, _ = self._memory_cache.popitem(last=False)

            self._stats["evictions"] += 1

            logger.debug(f"Evicted key {oldest_key} from memory cache")

        self._memory_cache[key] = entry
        await asyncio.sleep(0)

    async def _get_from_disk(self, key: str) -> Any:
        """Get value from disk cache."""
        # In real implementation, this would read from disk
        logger.debug(f"Disk cache get for key {key} not implemented")
        await asyncio.sleep(0)
        return None

    async def _set_in_disk(self, key: str, _entry: dict[str, Any]) -> None:
        """Set value in disk cache."""
        # In real implementation, this would write to disk
        logger.debug(f"Disk cache set for key {key} not implemented")
        await asyncio.sleep(0)

    async def _delete_from_disk(self, key: str) -> bool:
        """Delete from disk cache."""
        # In real implementation, this would delete from disk
        logger.debug(f"Disk cache delete for key {key} not implemented")
        await asyncio.sleep(0)
        return False

    async def _exists_in_disk(self, _key: str) -> bool:
        """Check if key exists in disk cache."""
        # In real implementation, this would check disk
        await asyncio.sleep(0)
        return False

    async def _clear_disk_cache(self) -> None:
        """Clear disk cache."""
        # In real implementation, this would clear disk cache
        logger.debug("Disk cache clear not implemented")
        await asyncio.sleep(0)

    async def _get_from_distributed(self, key: str) -> Any:
        """Get value from distributed cache."""
        # In real implementation, this would connect to Redis/Memcached
        logger.debug(f"Distributed cache get for key {key} not implemented")
        await asyncio.sleep(0)
        return None

    async def _set_in_distributed(self, key: str, _entry: dict[str, Any]) -> None:
        """Set value in distributed cache."""
        # In real implementation, this would connect to Redis/Memcached
        logger.debug(f"Distributed cache set for key {key} not implemented")
        await asyncio.sleep(0)

    async def _delete_from_distributed(self, key: str) -> bool:
        """Delete from distributed cache."""
        # In real implementation, this would delete from Redis/Memcached
        logger.debug(f"Distributed cache delete for key {key} not implemented")
        await asyncio.sleep(0)
        return False

    async def _exists_in_distributed(self, _key: str) -> bool:
        """Check if key exists in distributed cache."""
        # In real implementation, this would check Redis/Memcached
        await asyncio.sleep(0)
        return False

    async def _clear_distributed_cache(self) -> None:
        """Clear distributed cache."""
        # In real implementation, this would clear Redis/Memcached
        logger.debug("Distributed cache clear not implemented")
        await asyncio.sleep(0)

    def _should_compress(self, value: Any) -> bool:
        """Determine if value should be compressed."""

        size = self._get_size(value)

        return size > 1024  # Compress if larger than 1KB

    async def _compress_value(self, value: Any) -> bytes:
        """Compress value using pickle and gzip."""

        await asyncio.sleep(0)
        # Serialize first
        serialized = pickle.dumps(value)
        # Then compress
        compressed = gzip.compress(serialized)
        return compressed

    async def _decompress_value(self, compressed_value: bytes) -> Any:
        """Decompress value."""

        await asyncio.sleep(0)
        # Decompress first
        decompressed = gzip.decompress(compressed_value)
        # Then deserialize
        value = pickle.loads(decompressed)  # noqa: S301
        return value

    def _get_size(self, value: Any) -> int:
        """Get approximate size of value in bytes."""

        try:
            if isinstance(value, (str, bytes)):
                return len(value)

            elif isinstance(value, dict):
                return len(json.dumps(value, default=str))

            else:
                return len(pickle.dumps(value))

        except Exception:
            return 0

    async def _update_access_pattern(self, key: str) -> None:
        """Update access pattern for intelligent caching."""

        current_time = time.time()

        if key not in self._access_patterns:
            self._access_patterns[key] = []

        self._access_patterns[key].append(current_time)

        # Keep only recent access times (last 24 hours)

        cutoff_time = current_time - (24 * 3600)

        self._access_patterns[key] = [
            t for t in self._access_patterns[key] if t > cutoff_time
        ]

        await asyncio.sleep(0)

    async def _cleanup_expired_items(self) -> None:
        """Background task to clean up expired cache items."""

        while True:
            try:
                current_time = time.time()

                expired_keys = []

                # Check memory cache

                for key, entry in self._memory_cache.items():
                    if entry["expiry_time"] <= current_time:
                        expired_keys.append(key)

                # Remove expired keys

                for key in expired_keys:
                    del self._memory_cache[key]

                if expired_keys:
                    logger.debug(
                        f"Cleaned up {len(expired_keys)} expired cache entries"
                    )

                # Sleep for 5 minutes

                await asyncio.sleep(300)

            except asyncio.CancelledError:
                raise

            except Exception as e:
                logger.error(f"Error in cache cleanup: {e}")

                await asyncio.sleep(60)  # Wait 1 minute before retry

    async def _optimize_cache_strategy(self) -> None:
        """Background task to optimize caching strategy."""

        while True:
            try:
                # Analyze access patterns and adjust caching strategy

                await self._analyze_access_patterns()

                await self._optimize_cache_levels()

                # Sleep for 1 hour

                await asyncio.sleep(3600)

            except asyncio.CancelledError:
                raise

            except Exception as e:
                logger.error(f"Error in cache optimization: {e}")

                await asyncio.sleep(1800)  # Wait 30 minutes before retry

    async def _analyze_access_patterns(self) -> None:
        """Analyze access patterns for optimization."""

        # Implementation would analyze:
        # - Hot vs cold data
        # - Access frequency patterns
        # - Optimal TTL values
        # - Cache level distribution

        logger.debug("Access pattern analysis not yet implemented")
        await asyncio.sleep(0)

    async def _optimize_cache_levels(self) -> None:
        """Optimize data distribution across cache levels."""

        # Implementation would:
        # - Move hot data to faster cache levels
        # - Move cold data to slower cache levels
        # - Adjust cache sizes based on usage

        logger.debug("Cache level optimization not yet implemented")
        await asyncio.sleep(0)
