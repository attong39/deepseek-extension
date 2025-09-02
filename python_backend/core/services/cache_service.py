"""
Cache Service implementation với Redis backend.
Support cả in-memory cache và Redis distributed cache.
"""

import json
import time
from typing import Any, Dict, Optional

from core.domain.interfaces import CacheServiceInterface, MetricsServiceInterface


class InMemoryCacheService(CacheServiceInterface):
    """
    Simple in-memory cache implementation.
    Phù hợp cho development và testing.
    """

    def __init__(self, metrics: Optional[MetricsServiceInterface] = None):
        self.metrics = metrics
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, float] = {}
        self._max_size = 10000  # Max items in cache

    async def get(self, key: str) -> Optional[Any]:
        """Lấy value từ cache"""
        try:
            if key not in self._cache:
                if self.metrics:
                    self.metrics.increment_counter("cache_misses", {"type": "in_memory"})
                return None

            item = self._cache[key]

            # Check TTL
            if item.get("expires_at") and time.time() > item["expires_at"]:
                await self.delete(key)
                if self.metrics:
                    self.metrics.increment_counter("cache_misses", {"type": "in_memory", "reason": "expired"})
                return None

            # Update access time
            self._access_times[key] = time.time()

            if self.metrics:
                self.metrics.increment_counter("cache_hits", {"type": "in_memory"})

            return item["value"]

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "in_memory", "operation": "get"})
            return None

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set value vào cache với TTL"""
        try:
            # Evict old items nếu cache đầy
            if len(self._cache) >= self._max_size:
                await self._evict_lru()

            expires_at = None
            if ttl_seconds:
                expires_at = time.time() + ttl_seconds

            self._cache[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": time.time()
            }
            self._access_times[key] = time.time()

            if self.metrics:
                self.metrics.increment_counter("cache_sets", {"type": "in_memory"})

            return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "in_memory", "operation": "set"})
            return False

    async def delete(self, key: str) -> bool:
        """Xóa key khỏi cache"""
        try:
            if key in self._cache:
                del self._cache[key]
                self._access_times.pop(key, None)
                if self.metrics:
                    self.metrics.increment_counter("cache_deletes", {"type": "in_memory"})
                return True
            return False

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "in_memory", "operation": "delete"})
            return False

    async def exists(self, key: str) -> bool:
        """Kiểm tra key có tồn tại trong cache không"""
        value = await self.get(key)
        return value is not None

    async def _evict_lru(self) -> None:
        """Evict least recently used items"""
        if not self._access_times:
            return

        # Tìm key có access time cũ nhất
        lru_key = min(self._access_times, key=self._access_times.get)
        await self.delete(lru_key)

    async def clear(self) -> None:
        """Clear toàn bộ cache"""
        self._cache.clear()
        self._access_times.clear()
        if self.metrics:
            self.metrics.increment_counter("cache_clears", {"type": "in_memory"})

    def get_stats(self) -> Dict[str, Any]:
        """Lấy cache statistics"""
        now = time.time()
        total_items = len(self._cache)
        expired_items = 0

        for item in self._cache.values():
            if item.get("expires_at") and now > item["expires_at"]:
                expired_items += 1

        return {
            "type": "in_memory",
            "total_items": total_items,
            "expired_items": expired_items,
            "active_items": total_items - expired_items,
            "max_size": self._max_size,
            "usage_percent": (total_items / self._max_size) * 100,
        }


# Redis cache implementation (placeholder for production)
class RedisCacheService(CacheServiceInterface):
    """
    Redis-based distributed cache implementation.
    Requires redis-py: pip install redis[hiredis]
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        metrics: Optional[MetricsServiceInterface] = None
    ):
        self.redis_url = redis_url
        self.metrics = metrics
        self._redis = None  # Will be initialized lazily

    async def _get_redis_client(self):
        """Lazy initialization của Redis client"""
        if self._redis is None:
            try:
                import redis.asyncio as redis
                self._redis = redis.from_url(self.redis_url, decode_responses=True)
                await self._redis.ping()  # Test connection
            except ImportError:
                raise RuntimeError("Redis not available. Install with: pip install redis[hiredis]")
            except Exception as e:
                raise RuntimeError(f"Cannot connect to Redis: {e}")
        return self._redis

    async def get(self, key: str) -> Optional[Any]:
        """Lấy value từ Redis cache"""
        try:
            redis_client = await self._get_redis_client()
            value_str = await redis_client.get(key)

            if value_str is None:
                if self.metrics:
                    self.metrics.increment_counter("cache_misses", {"type": "redis"})
                return None

            if self.metrics:
                self.metrics.increment_counter("cache_hits", {"type": "redis"})

            return json.loads(value_str)

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "redis", "operation": "get"})
            return None

    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set value vào Redis cache với TTL"""
        try:
            redis_client = await self._get_redis_client()
            value_str = json.dumps(value)

            if ttl_seconds:
                await redis_client.setex(key, ttl_seconds, value_str)
            else:
                await redis_client.set(key, value_str)

            if self.metrics:
                self.metrics.increment_counter("cache_sets", {"type": "redis"})

            return True

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "redis", "operation": "set"})
            return False

    async def delete(self, key: str) -> bool:
        """Xóa key khỏi Redis cache"""
        try:
            redis_client = await self._get_redis_client()
            result = await redis_client.delete(key)

            if self.metrics:
                self.metrics.increment_counter("cache_deletes", {"type": "redis"})

            return result > 0

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "redis", "operation": "delete"})
            return False

    async def exists(self, key: str) -> bool:
        """Kiểm tra key có tồn tại trong Redis không"""
        try:
            redis_client = await self._get_redis_client()
            result = await redis_client.exists(key)
            return result > 0

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "redis", "operation": "exists"})
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """Clear các keys theo pattern"""
        try:
            redis_client = await self._get_redis_client()
            keys = await redis_client.keys(pattern)
            if keys:
                result = await redis_client.delete(*keys)
                if self.metrics:
                    self.metrics.increment_counter("cache_pattern_clears", {"type": "redis"})
                return result
            return 0

        except Exception:
            if self.metrics:
                self.metrics.increment_counter("cache_errors", {"type": "redis", "operation": "clear_pattern"})
            return 0

    async def get_stats(self) -> Dict[str, Any]:
        """Lấy Redis statistics"""
        try:
            redis_client = await self._get_redis_client()
            info = await redis_client.info()

            return {
                "type": "redis",
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory"),
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses"),
            }

        except Exception as e:
            return {"type": "redis", "error": str(e)}


# Cache factory for easy switching
def create_cache_service(
    cache_type: str = "memory",
    redis_url: str = "redis://localhost:6379",
    metrics: Optional[MetricsServiceInterface] = None
) -> CacheServiceInterface:
    """
    Factory function để tạo cache service.
    
    Args:
        cache_type: "memory" hoặc "redis"
        redis_url: URL cho Redis (nếu sử dụng Redis)
        metrics: Metrics service instance
        
    Returns:
        CacheServiceInterface implementation
    """
    if cache_type.lower() == "redis":
        return RedisCacheService(redis_url, metrics)
    else:
        return InMemoryCacheService(metrics)
