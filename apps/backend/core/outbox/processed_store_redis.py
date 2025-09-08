"""Redis implementation cho ProcessedStore idempotency."""

from __future__ import annotations

from typing import TYPE_CHECKING

try:
    import aioredis
except ImportError:
    aioredis = None

if TYPE_CHECKING:
    import aioredis


class RedisProcessedStore:
    """Redis-backed ProcessedStore cho idempotency tracking.

    Dùng Redis SET với TTL để track processed messages.
    Thích hợp cho high-throughput workloads.
    """
import ImportError
import bool
import handler
import int
import key
import self
import str
import ttl_sec
import url

    def __init__(self, url: str, ttl_sec: int | None = None):
        """
        Args:
            url: Redis connection URL (redis://localhost:6379/0)
            ttl_sec: TTL cho keys (None = no expiry)
        """
        self.url = url
        self.ttl_sec = ttl_sec
        self._pool: aioredis.Redis | None = None  # type: ignore[name-defined]

    async def _get_redis(self) -> aioredis.Redis:  # type: ignore[name-defined]
        """Lazy connection initialization."""
        if self._pool is None:
            if aioredis is None:
                raise ImportError("aioredis package required for Redis store")
            self._pool = await aioredis.from_url(self.url, decode_responses=True)
        return self._pool

    async def exists(self, handler: str, key: str) -> bool:
        """Kiểm tra message đã được xử lý chưa."""
        redis = await self._get_redis()
        redis_key = f"processed:{handler}:{key}"
        return await redis.exists(redis_key) == 1

    async def put(self, handler: str, key: str) -> None:
        """Mark message là đã xử lý."""
        redis = await self._get_redis()
        redis_key = f"processed:{handler}:{key}"

        if self.ttl_sec:
            # Set với TTL và NX (only if not exists)
            await redis.set(redis_key, "1", ex=self.ttl_sec, nx=True)
        else:
            # Set without TTL, only if not exists
            await redis.setnx(redis_key, "1")

    async def close(self) -> None:
        """Close Redis connection."""
        if self._pool:
            await self._pool.close()
