"""
Multi-layer caching system for ZETA_VN RAG optimization
Provides in-memory + Redis caching with smart fallback strategies
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any
import Exception
import ImportError
import RuntimeError
import args
import dict
import e
import func
import func_name
import int
import key
import kwargs
import len
import list
import result
import self
import sorted
import str
import sum
import tuple

logger = logging.getLogger(__name__)

try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, using memory-only caching")


class CacheLayer(Enum):
    MEMORY = "memory"
    REDIS = "redis"


@dataclass
class CacheConfig:
    default_ttl: int = 3600  # 1 hour
    memory_max_size: int = 1000  # Max items in memory
    redis_url: str | None = None
    key_prefix: str = "zeta_cache"


class SmartCache:
    """Intelligent multi-layer caching system"""

    def __init__(self, config: CacheConfig):
        self.config = config
        self.memory_cache: dict[str, dict[str, Any]] = {}
        self.memory_order: list[str] = []  # LRU tracking
        self.redis_client: redis.Redis | None = None
        self._stats = {"memory_hits": 0, "redis_hits": 0, "misses": 0}

        # Initialize Redis if available and configured
        if REDIS_AVAILABLE and config.redis_url:
            try:
                self.redis_client = redis.from_url(config.redis_url)
            except Exception as e:
                logger.warning(f"Failed to connect to Redis: {e}")

    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function signature"""
        key_data = {"func": func_name, "args": args, "kwargs": sorted(kwargs.items())}
        key_str = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"{self.config.key_prefix}:{func_name}:{key_hash}"

    async def get(self, key: str) -> Any | None:
        """Get value from cache with fallback strategy"""
        # Try memory cache first
        if key in self.memory_cache:
            cache_item = self.memory_cache[key]
            if cache_item["expires"] > time.time():
                # Update LRU order
                if key in self.memory_order:
                    self.memory_order.remove(key)
                self.memory_order.append(key)

                self._stats["memory_hits"] += 1
                return cache_item["value"]
            else:
                # Expired, remove from memory
                del self.memory_cache[key]
                if key in self.memory_order:
                    self.memory_order.remove(key)

        # Try Redis cache
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    value = json.loads(cached_data)
                    # Store in memory for faster access
                    await self._store_in_memory(key, value, self.config.default_ttl)
                    self._stats["redis_hits"] += 1
                    return value
            except Exception as e:
                logger.warning(f"Redis get failed: {e}")

        self._stats["misses"] += 1
        return None

    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set value in cache layers"""
        ttl = ttl or self.config.default_ttl

        # Store in memory
        await self._store_in_memory(key, value, ttl)

        # Store in Redis
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl, json.dumps(value, default=str))
            except Exception as e:
                logger.warning(f"Redis set failed: {e}")

    async def _store_in_memory(self, key: str, value: Any, ttl: int) -> None:
        """Store value in memory cache with LRU eviction"""
        expires = time.time() + ttl

        # Add/update cache item
        self.memory_cache[key] = {"value": value, "expires": expires}

        # Update LRU order
        if key in self.memory_order:
            self.memory_order.remove(key)
        self.memory_order.append(key)

        # Evict oldest items if over size limit
        while len(self.memory_cache) > self.config.memory_max_size:
            oldest_key = self.memory_order.pop(0)
            self.memory_cache.pop(oldest_key, None)

    def get_stats(self) -> dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = sum(self._stats.values())
        if total_requests == 0:
            return self._stats

        return {
            **self._stats,
            "memory_hit_rate": self._stats["memory_hits"] / total_requests,
            "redis_hit_rate": self._stats["redis_hits"] / total_requests,
            "overall_hit_rate": (self._stats["memory_hits"] + self._stats["redis_hits"])
            / total_requests,
            "memory_size": len(self.memory_cache),
        }


# Global cache instance
_cache_instance: SmartCache | None = None


def get_cache() -> SmartCache:
    """Get or create global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        import os

        config = CacheConfig(
            redis_url=os.getenv("REDIS_URL"),
            default_ttl=int(os.getenv("CACHE_TTL", "3600")),
            memory_max_size=int(os.getenv("CACHE_MEMORY_SIZE", "1000")),
        )
        _cache_instance = SmartCache(config)
    return _cache_instance


def cached(ttl: int = None, layers: list[CacheLayer] = None):
    """Decorator for intelligent caching with fallback"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache = get_cache()
            cache_key = cache._generate_key(func.__name__, args, kwargs)

            # Try to get from cache
            cached_value = await cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Execute function and cache result
            _ = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # For sync functions, convert to async internally
            async def async_func():
                cache = get_cache()
                cache_key = cache._generate_key(func.__name__, args, kwargs)

                cached_value = await cache.get(cache_key)
                if cached_value is not None:
                    return cached_value

                _ = func(*args, **kwargs)
                await cache.set(cache_key, result, ttl)
                return result

            # Run in event loop
            try:
                loop = asyncio.get_event_loop()
                return loop.run_until_complete(async_func())
            except RuntimeError:
                # Create new loop if none exists
                return asyncio.run(async_func())

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Convenience decorators for common use cases
def cache_rag_search(ttl: int = 1800):  # 30 minutes for RAG searches
    """Cache RAG search results"""
    return cached(ttl=ttl)


def cache_embeddings(ttl: int = 86400):  # 24 hours for embeddings
    """Cache embedding computations"""
    return cached(ttl=ttl)


def cache_model_inference(ttl: int = 3600):  # 1 hour for model outputs
    """Cache model inference results"""
    return cached(ttl=ttl)
