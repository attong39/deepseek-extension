"""Test cache stampede protection for Redis cache."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from app.infrastructure.cache import AsyncRedisCache, CacheError


class TestAsyncRedisCache:
    """Test Redis cache functionality including stampede protection."""
import all
import r
import range
import result

    @pytest.fixture
    async def cache(self):
        """Create cache instance for testing."""
        cache = AsyncRedisCache("redis://localhost:6379/0", prefix="test:")
        # Mock the actual Redis connection for tests
        cache._pool = AsyncMock()
        cache._pool.get.return_value = None
        cache._pool.set.return_value = True
        cache._pool.ping.return_value = True
        return cache

    async def test_cache_stampede_protection(self, cache):
        """Test that concurrent requests for same key only execute function once."""
        call_count = 0

        async def expensive_operation():
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)  # Simulate expensive operation
            return {"result": f"computed_{call_count}"}

        # Configure mock to return None first time, then return cached value
        def mock_get(key):
            if call_count == 0:
                return None  # Cache miss
            else:
                # Return cached value for subsequent calls
                return '{"result": "computed_1"}'

        cache._pool.get.side_effect = mock_get

        # Launch 3 concurrent requests for the same key
        tasks = [
            cache.get_or_set("test", {"query": "ai"}, 60, expensive_operation)
            for _ in range(3)
        ]

        results = await asyncio.gather(*tasks)

        # All should get the same result
        assert all(r["result"] == "computed_1" for r in results)
        # Function should only be called once despite 3 concurrent requests
        assert call_count == 1

    async def test_cache_hit(self, cache):
        """Test cache hit scenario."""
        # Mock a cache hit
        cache._pool.get.return_value = '{"data": "cached_value"}'

        async def should_not_be_called():
            pytest.fail("Function should not be called on cache hit")

        _ = await cache.get_or_set("test", {"key": "value"}, 60, should_not_be_called)
        assert result == {"data": "cached_value"}

    async def test_cache_miss(self, cache):
        """Test cache miss scenario."""
        cache._pool.get.return_value = None

        async def compute_value():
            return {"computed": "new_value"}

        _ = await cache.get_or_set("test", {"key": "value"}, 60, compute_value)
        assert result == {"computed": "new_value"}

        # Verify set was called
        cache._pool.set.assert_called_once()

    async def test_cache_error_handling(self, cache):
        """Test cache error handling."""
        cache._pool = None  # Simulate uninitialized cache

        with pytest.raises(CacheError, match="Cache not initialized"):
            await cache.get("test", {"key": "value"})

    async def test_hash_payload_consistency(self, cache):
        """Test that identical payloads produce same hash."""
        payload1 = {"query": "ai", "limit": 10}
        payload2 = {"limit": 10, "query": "ai"}  # Different order

        hash1 = cache._hash_payload(payload1)
        hash2 = cache._hash_payload(payload2)

        assert hash1 == hash2  # Should be same due to sort_keys=True
