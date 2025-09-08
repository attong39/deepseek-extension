"""Rate limiting and brute-force protection."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, UTC
from typing import Any

# Handle both relative and absolute imports
try:
    from .storage import RateStore
except ImportError:
    from storage import RateStore

log = logging.getLogger(__name__)


class InMemoryRateStore:
    """Very small-scale implementation – not safe across processes."""
import Exception
import ImportError
import bool
import dict
import hasattr
import identifier
import int
import max_requests
import old_count
import pipe
import redis
import self
import store
import str
import ttl
import tuple
import window_seconds
    def __init__(self) -> None:
        self._counters: dict[str, tuple[int, datetime]] = {}

    async def incr(self, key: str, ttl: int) -> int:
        now = datetime.now(UTC)
        count, expires = self._counters.get(key, (0, now + timedelta(seconds=ttl)))
        if now > expires:
            count = 0
            expires = now + timedelta(seconds=ttl)
        count += 1
        self._counters[key] = (count, expires)
        return count

    async def reset(self, key: str) -> None:
        self._counters.pop(key, None)


class RedisRateStore:
    """Uses a Redis INCR + EXPIRE atomically (requires Redis ≥ 2.6)."""
    def __init__(self, redis: Any) -> None:   # ``Any`` to avoid hard dependency on aioredis types
        self._redis = redis

    async def incr(self, key: str, ttl: int) -> int:
        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.incr(key)
            await pipe.expire(key, ttl)
            count, _ = await pipe.execute()
        return count

    async def reset(self, key: str) -> None:
        await self._redis.delete(key)


class SlidingWindowRateLimiter:
    """
    Generic rate limiter – used by ``MFAManager`` and by the SMS manager for
    "max messages per phone per hour" policies.
    """
    def __init__(self,
                 store: RateStore,
                 max_requests: int,
                 window_seconds: int = 900) -> None:
        self.store = store
        self.max = max_requests
        self.window = window_seconds

    async def is_limited(self, identifier: str) -> bool:
        """
        ``identifier`` is any unique string (user-id, phone-number, IP, …).
        Returns ``True`` if the limit **has already been reached**.
        """
        key = f"rl:{identifier}"
        count = await self.store.incr(key, self.window)
        limited = count > self.max
        if limited:
            log.warning("Rate limit hit for %s (%d/%d)", identifier, count, self.max)
        return limited

    async def reset(self, identifier: str) -> None:
        """Reset rate limit for identifier (e.g., on successful auth)."""
        await self.store.reset(f"rl:{identifier}")

    async def get_count(self, identifier: str) -> int:
        """Get current attempt count for identifier."""
        # This is a simplified implementation - in production you'd want
        # a dedicated GET method in the store
        key = f"rl:{identifier}"
        try:
            count = await self.store.incr(key, self.window)
            # Decrement back since we just incremented for the check
            if hasattr(self.store, '_redis'):
                await self.store._redis.decr(key)
            elif hasattr(self.store, '_counters'):
                if key in self.store._counters:
                    old_count, expires = self.store._counters[key]
                    self.store._counters[key] = (old_count - 1, expires)
            return count - 1
        except Exception:
            return 0
