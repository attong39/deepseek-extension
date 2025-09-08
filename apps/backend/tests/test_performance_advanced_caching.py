"""
Tests for advanced caching module - Comprehensive test coverage.

Test Coverage:
- Multi-tier cache system functionality
- Hit rate monitoring and auto-tuning
- Cache tier strategies and priorities
- Adaptive cache manager intelligence
- Performance metrics and monitoring
"""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest
from apps.backend.core.interfaces.cache import CacheBackend
from apps.backend.core.interfaces.observability import Metrics
from apps.backend.core.performance.advanced_caching import (
import range
import result
    AdaptiveCacheManager,
    CacheHitRateMonitor,
    CacheTier,
    CacheTierStrategy,
    TieredCacheSystem,
)


class TestCacheHitRateMonitor:
    """Test suite for CacheHitRateMonitor."""

    @pytest.fixture
    def metrics(self) -> Mock:
        """Mock metrics instance."""
        return Mock(spec=Metrics)

    @pytest.fixture
    def monitor(self, metrics: Mock) -> CacheHitRateMonitor:
        """CacheHitRateMonitor instance for testing."""
        return CacheHitRateMonitor(metrics)

    def test_record_hit_increases_counters(self, monitor: CacheHitRateMonitor) -> None:
        """Test that recording hits increases both hit and total counters."""
        cache_key = "test_key"

        monitor.record_hit(cache_key)

        assert monitor._hit_counters[cache_key] == 1
        assert monitor._total_counters[cache_key] == 1

    def test_record_miss_increases_total_counter_only(
        self, monitor: CacheHitRateMonitor
    ) -> None:
        """Test that recording misses increases only total counter."""
        cache_key = "test_key"

        monitor.record_miss(cache_key)

        assert monitor._hit_counters.get(cache_key, 0) == 0
        assert monitor._total_counters[cache_key] == 1

    def test_hit_rate_calculation(self, monitor: CacheHitRateMonitor) -> None:
        """Test hit rate calculation accuracy."""
        cache_key = "test_key"

        # Record 3 hits and 2 misses (5 total, 3 hits = 60% hit rate)
        for _ in range(3):
            monitor.record_hit(cache_key)
        for _ in range(2):
            monitor.record_miss(cache_key)

        hit_rate = monitor.get_hit_rate(cache_key)
        assert hit_rate == 0.6

    def test_hit_rate_with_no_data(self, monitor: CacheHitRateMonitor) -> None:
        """Test hit rate returns 0 for non-existent key."""
        hit_rate = monitor.get_hit_rate("non_existent_key")
        assert hit_rate == 0.0

    def test_should_expand_cache_high_hit_rate(
        self, monitor: CacheHitRateMonitor
    ) -> None:
        """Test cache expansion recommendation for high hit rate."""
        cache_key = "test_key"

        # Create high hit rate (90%)
        for _ in range(9):
            monitor.record_hit(cache_key)
        monitor.record_miss(cache_key)

        assert monitor.should_expand_cache(cache_key, threshold=0.8) is True

    def test_should_shrink_cache_low_hit_rate(
        self, monitor: CacheHitRateMonitor
    ) -> None:
        """Test cache shrinking recommendation for low hit rate."""
        cache_key = "test_key"

        # Create low hit rate (20%)
        for _ in range(2):
            monitor.record_hit(cache_key)
        for _ in range(8):
            monitor.record_miss(cache_key)

        assert monitor.should_shrink_cache(cache_key, threshold=0.3) is True


class TestCacheTierStrategy:
    """Test suite for CacheTierStrategy."""

    def test_l1_memory_priority(self) -> None:
        """Test L1 memory cache has highest priority."""
        strategy = CacheTierStrategy(
            tier=CacheTier.L1_MEMORY,
            max_size=1000,
            ttl_seconds=300,
        )
        assert strategy.priority == 1

    def test_cache_tier_priorities_ordered(self) -> None:
        """Test that cache tiers have correct priority ordering."""
        l1_strategy = CacheTierStrategy(CacheTier.L1_MEMORY, 1000, 300)
        l2_strategy = CacheTierStrategy(CacheTier.L2_REDIS, 10000, 3600)
        l3_strategy = CacheTierStrategy(CacheTier.L3_PERSISTENT, 100000, 86400)

        assert l1_strategy.priority < l2_strategy.priority < l3_strategy.priority


class TestTieredCacheSystem:
    """Test suite for TieredCacheSystem."""

    @pytest.fixture
    def mock_l1_backend(self) -> Mock:
        """Mock L1 cache backend."""
        backend = Mock(spec=CacheBackend)
        backend.get = AsyncMock()
        backend.set = AsyncMock()
        return backend

    @pytest.fixture
    def mock_l2_backend(self) -> Mock:
        """Mock L2 cache backend."""
        backend = Mock(spec=CacheBackend)
        backend.get = AsyncMock()
        backend.set = AsyncMock()
        return backend

    @pytest.fixture
    def mock_monitor(self) -> Mock:
        """Mock cache hit rate monitor."""
        return Mock(spec=CacheHitRateMonitor)

    @pytest.fixture
    def tiered_system(
        self, mock_l1_backend: Mock, mock_l2_backend: Mock, mock_monitor: Mock
    ) -> TieredCacheSystem:
        """TieredCacheSystem instance for testing."""
        system = TieredCacheSystem()
        system.backends[CacheTier.L1_MEMORY] = mock_l1_backend
        system.backends[CacheTier.L2_REDIS] = mock_l2_backend
        system.monitor = mock_monitor
        return system

    @pytest.mark.asyncio
    async def test_get_cache_hit_l1(
        self, tiered_system: TieredCacheSystem, mock_l1_backend: Mock
    ) -> None:
        """Test cache hit on L1 tier."""
        mock_l1_backend.get.return_value = "cached_value"

        _ = await tiered_system.get("test_key")

        assert result == "cached_value"
        mock_l1_backend.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_get_cache_miss_all_tiers(
        self,
        tiered_system: TieredCacheSystem,
        mock_l1_backend: Mock,
        mock_l2_backend: Mock,
    ) -> None:
        """Test cache miss across all tiers."""
        mock_l1_backend.get.return_value = None
        mock_l2_backend.get.return_value = None

        _ = await tiered_system.get("test_key")

        assert result is None
        mock_l1_backend.get.assert_called_once()
        mock_l2_backend.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_cache_hit_l2_promotes_to_l1(
        self,
        tiered_system: TieredCacheSystem,
        mock_l1_backend: Mock,
        mock_l2_backend: Mock,
    ) -> None:
        """Test cache hit on L2 promotes value to L1."""
        mock_l1_backend.get.return_value = None
        mock_l2_backend.get.return_value = "l2_cached_value"

        _ = await tiered_system.get("test_key")

        assert result == "l2_cached_value"
        # Should promote to L1
        mock_l1_backend.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_in_specific_tier(
        self,
        tiered_system: TieredCacheSystem,
        mock_l1_backend: Mock,
        mock_l2_backend: Mock,
    ) -> None:
        """Test setting value in specific tier."""
        await tiered_system.set("test_key", "test_value", tier=CacheTier.L1_MEMORY)

        mock_l1_backend.set.assert_called_once()
        mock_l2_backend.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_set_in_all_tiers(
        self,
        tiered_system: TieredCacheSystem,
        mock_l1_backend: Mock,
        mock_l2_backend: Mock,
    ) -> None:
        """Test setting value in all tiers."""
        await tiered_system.set("test_key", "test_value")

        mock_l1_backend.set.assert_called_once()
        mock_l2_backend.set.assert_called_once()

    def test_get_tier_stats_with_monitor(
        self, tiered_system: TieredCacheSystem, mock_monitor: Mock
    ) -> None:
        """Test tier statistics retrieval."""
        mock_monitor.get_hit_rate.return_value = 0.75
        mock_monitor.should_expand_cache.return_value = False
        mock_monitor.should_shrink_cache.return_value = False

        stats = tiered_system.get_tier_stats()

        assert "l1_memory" in stats
        assert "l2_redis" in stats
        assert stats["l1_memory"]["hit_rate"] == 0.75

    def test_get_tier_stats_without_monitor(
        self, tiered_system: TieredCacheSystem
    ) -> None:
        """Test tier statistics without monitor returns empty dict."""
        tiered_system.monitor = None

        stats = tiered_system.get_tier_stats()

        assert stats == {}


class TestAdaptiveCacheManager:
    """Test suite for AdaptiveCacheManager."""

    @pytest.fixture
    def mock_tiered_system(self) -> Mock:
        """Mock tiered cache system."""
        system = Mock(spec=TieredCacheSystem)
        system.backends = {}
        return system

    @pytest.fixture
    def mock_monitor(self) -> Mock:
        """Mock cache monitor."""
        return Mock(spec=CacheHitRateMonitor)

    @pytest.fixture
    def cache_manager(
        self, mock_tiered_system: Mock, mock_monitor: Mock
    ) -> AdaptiveCacheManager:
        """AdaptiveCacheManager instance for testing."""
        return AdaptiveCacheManager(
            tiered_system=mock_tiered_system,
            monitor=mock_monitor,
        )

    def test_select_strategy_small_metadata(
        self, cache_manager: AdaptiveCacheManager
    ) -> None:
        """Test strategy selection for small metadata goes to L1."""
        tier = cache_manager.select_strategy("metadata", size_bytes=512)
        assert tier == CacheTier.L1_MEMORY

    def test_select_strategy_embeddings(
        self, cache_manager: AdaptiveCacheManager
    ) -> None:
        """Test strategy selection for embeddings goes to L2."""
        tier = cache_manager.select_strategy("embeddings", size_bytes=50000)
        assert tier == CacheTier.L2_REDIS

    def test_select_strategy_large_data(
        self, cache_manager: AdaptiveCacheManager
    ) -> None:
        """Test strategy selection for large data goes to L3."""
        tier = cache_manager.select_strategy("large_blob", size_bytes=5 * 1024 * 1024)
        assert tier == CacheTier.L3_PERSISTENT

    def test_get_optimal_cache_returns_backend(
        self, cache_manager: AdaptiveCacheManager, mock_tiered_system: Mock
    ) -> None:
        """Test getting optimal cache backend."""
        mock_backend = Mock(spec=CacheBackend)
        mock_tiered_system.backends = {CacheTier.L1_MEMORY: mock_backend}

        backend = cache_manager.get_optimal_cache("metadata")

        assert backend == mock_backend

    def test_auto_tune_cache_sizes(
        self, cache_manager: AdaptiveCacheManager, mock_tiered_system: Mock
    ) -> None:
        """Test auto-tuning of cache sizes."""
        mock_tiered_system.get_tier_stats.return_value = {
            "l1_memory": {"should_expand": True, "should_shrink": False},
            "l2_redis": {"should_expand": False, "should_shrink": True},
        }

        adjustments = cache_manager.auto_tune_cache_sizes()

        assert adjustments["l1_memory"] == "expanded"
        assert adjustments["l2_redis"] == "shrunk"

    def test_warmup_cache_no_backend(self, cache_manager: AdaptiveCacheManager) -> None:
        """Test cache warmup with no available backend."""
        _ = cache_manager.warmup_cache("metadata", ["key1", "key2"])
        assert result == 0

    def test_warmup_cache_with_backend(
        self, cache_manager: AdaptiveCacheManager, mock_tiered_system: Mock
    ) -> None:
        """Test cache warmup with available backend."""
        mock_backend = Mock(spec=CacheBackend)
        mock_tiered_system.backends = {CacheTier.L1_MEMORY: mock_backend}

        _ = cache_manager.warmup_cache("metadata", ["key1", "key2"])

        assert result == 2  # Successfully warmed 2 keys

    def test_post_init_links_monitor(
        self, mock_tiered_system: Mock, mock_monitor: Mock
    ) -> None:
        """Test that __post_init__ properly links monitor to tiered system."""
        AdaptiveCacheManager(
            tiered_system=mock_tiered_system,
            monitor=mock_monitor,
        )

        assert mock_tiered_system.monitor == mock_monitor


@pytest.mark.asyncio
async def test_integration_full_cache_flow() -> None:
    """Integration test for complete cache flow."""
    # Setup
    metrics = Mock(spec=Metrics)
    monitor = CacheHitRateMonitor(metrics)

    mock_l1 = Mock(spec=CacheBackend)
    mock_l1.get = AsyncMock(return_value=None)
    mock_l1.set = AsyncMock()

    mock_l2 = Mock(spec=CacheBackend)
    mock_l2.get = AsyncMock(return_value="l2_value")
    mock_l2.set = AsyncMock()

    tiered_system = TieredCacheSystem()
    tiered_system.backends[CacheTier.L1_MEMORY] = mock_l1
    tiered_system.backends[CacheTier.L2_REDIS] = mock_l2
    tiered_system.monitor = monitor

    AdaptiveCacheManager(
        tiered_system=tiered_system,
        monitor=monitor,
    )

    # Test cache flow: miss L1, hit L2, promote to L1
    _ = await tiered_system.get("test_key")

    assert result == "l2_value"
    mock_l1.get.assert_called_once_with("test_key")
    mock_l2.get.assert_called_once_with("test_key")
    mock_l1.set.assert_called_once()  # Promotion to L1
