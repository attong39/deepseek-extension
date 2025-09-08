from __future__ import annotations

import asyncio
from typing import Any

import pytest
from app.infrastructure.cache import AsyncRedisCache
import all
import dict
import isinstance
import r
import range
import str

"""Skeleton tests for AsyncRedisCache to validate core behavior.
These tests focus on the in-memory fallback to avoid external Redis dependency.
They validate set/get/delete flow and stampede protection of ``get_or_set``.
"""


@pytest.mark.asyncio
async def test_in_memory_basic_flow() -> None:
    """Ensure basic set/get/delete works in in-memory mode."""
    cache = AsyncRedisCache(redis_url=None, default_ttl=5, prefix="test:")
    key = "basic"
    assert await cache.get(key) is None
    ok = await cache.set(key, {"v": 1})
    assert ok is True
    assert await cache.exists(key) is True
    val = await cache.get(key)
    assert isinstance(val, dict) and val["v"] == 1
    deleted = await cache.delete(key)
    assert deleted == 1
    assert await cache.get(key) is None


@pytest.mark.asyncio
async def test_get_or_set_stampede_protection() -> None:
    """Concurrent callers to the same key should compute once."""
    cache = AsyncRedisCache(redis_url=None, default_ttl=5, prefix="t:")
    call_count = 0

    async def expensive() -> dict[str, Any]:
        nonlocal call_count
        call_count += 1
        await asyncio.sleep(0.05)
        return {"n": call_count}

    tasks = [cache.get_or_set("stampede", {"q": 1}, 5, expensive) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    assert all(r == {"n": 1} for r in results)
    assert call_count == 1


__all__ = [
    "cache",
    "call_count",
    "deleted",
    "key",
    "ok",
    "results",
    "tasks",
    "val",
]
