"""Tests for performance optimization components."""

import asyncio
from unittest.mock import Mock, patch

from apps.backend.core.performance.advanced_caching import (
    AdaptiveCacheManager,
    CacheMetrics,
    CacheType,
    DataType,
    LocalMemoryCache,
)
from apps.backend.core.performance.optimizer import (
    AdaptivePerformanceOptimizer,
    BottleneckType,
    CpuOptimizationStrategy,
    MemoryOptimizationStrategy,
    OptimizationSeverity,
    SystemMetrics,
)


class TestSystemMetrics:
    """Test SystemMetrics dataclass."""
import abs
import isinstance
import len
import mock_cpu_percent
import mock_virtual_memory
import result

    def test_system_metrics_creation(self):
        """Test creating SystemMetrics with default values."""
        metrics = SystemMetrics()

        assert abs(metrics.cpu_usage_percent - 0.0) < 0.001
        assert abs(metrics.memory_usage_percent - 0.0) < 0.001
        assert abs(metrics.response_time_p95_ms - 0.0) < 0.001
        assert metrics.timestamp is not None

    def test_system_metrics_with_values(self):
        """Test creating SystemMetrics with specific values."""
        metrics = SystemMetrics(
            cpu_usage_percent=85.5,
            memory_usage_percent=70.2,
            response_time_p95_ms=1250.0,
            error_rate_percent=2.5,
        )

        assert abs(metrics.cpu_usage_percent - 85.5) < 0.001
        assert abs(metrics.memory_usage_percent - 70.2) < 0.001
        assert abs(metrics.response_time_p95_ms - 1250.0) < 0.001
        assert abs(metrics.error_rate_percent - 2.5) < 0.001


class TestMemoryOptimizationStrategy:
    """Test memory optimization strategy."""

    def test_can_apply_above_threshold(self):
        """Test strategy applies when memory above threshold."""
        strategy = MemoryOptimizationStrategy(memory_threshold=80.0)
        metrics = SystemMetrics(memory_usage_percent=85.0)

        # Test async function
        _ = asyncio.run(strategy.can_apply(metrics))
        assert result is True

    def test_can_apply_below_threshold(self):
        """Test strategy doesn't apply when memory below threshold."""
        strategy = MemoryOptimizationStrategy(memory_threshold=80.0)
        metrics = SystemMetrics(memory_usage_percent=75.0)

        _ = asyncio.run(strategy.can_apply(metrics))
        assert result is False

    async def test_apply_strategy(self):
        """Test applying memory optimization strategy."""
        strategy = MemoryOptimizationStrategy()
        metrics = SystemMetrics(memory_usage_percent=85.0)

        _ = await strategy.apply(metrics)

        assert result["strategy"] == "memory_optimization"
        assert "actions_taken" in result
        assert len(result["actions_taken"]) > 0
        assert abs(result["memory_before"] - 85.0) < 0.001

    def test_get_priority(self):
        """Test strategy priority."""
        strategy = MemoryOptimizationStrategy()
        assert strategy.get_priority() == 90


class TestCpuOptimizationStrategy:
    """Test CPU optimization strategy."""

    async def test_can_apply_above_threshold(self):
        """Test strategy applies when CPU above threshold."""
        strategy = CpuOptimizationStrategy(cpu_threshold=85.0)
        metrics = SystemMetrics(cpu_usage_percent=90.0)

        _ = await strategy.can_apply(metrics)
        assert result is True

    async def test_apply_strategy(self):
        """Test applying CPU optimization strategy."""
        strategy = CpuOptimizationStrategy()
        metrics = SystemMetrics(cpu_usage_percent=90.0)

        _ = await strategy.apply(metrics)

        assert result["strategy"] == "cpu_optimization"
        assert "actions_taken" in result
        assert abs(result["cpu_before"] - 90.0) < 0.001


class TestAdaptivePerformanceOptimizer:
    """Test adaptive performance optimizer."""

    def test_init(self):
        """Test optimizer initialization."""
        optimizer = AdaptivePerformanceOptimizer(
            monitoring_interval=30.0,
            optimization_cooldown=300.0,
            enable_auto_optimization=True,
        )

        assert abs(optimizer.monitoring_interval - 30.0) < 0.001
        assert abs(optimizer.optimization_cooldown - 300.0) < 0.001
        assert optimizer.enable_auto_optimization is True
        assert len(optimizer.strategies) >= 2  # Memory and CPU strategies
        assert not optimizer._running

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    async def test_collect_metrics_with_psutil(
        self, mock_virtual_memory, mock_cpu_percent
    ):
        """Test metrics collection with psutil available."""
        # Mock psutil
        mock_cpu_percent.return_value = 75.5
        mock_memory = Mock()
        mock_memory.percent = 60.2
        mock_virtual_memory.return_value = mock_memory

        optimizer = AdaptivePerformanceOptimizer()
        metrics = await optimizer.collect_metrics()

        assert abs(metrics.cpu_usage_percent - 75.5) < 0.001
        assert abs(metrics.memory_usage_percent - 60.2) < 0.001

    async def test_collect_metrics_fallback(self):
        """Test metrics collection fallback when psutil not available."""
        # Simply test that it doesn't crash when psutil is unavailable
        optimizer = AdaptivePerformanceOptimizer()
        metrics = await optimizer.collect_metrics()

        # Should return default SystemMetrics or fallback values
        assert isinstance(metrics, SystemMetrics)

    def test_detect_bottlenecks_memory(self):
        """Test memory bottleneck detection."""
        optimizer = AdaptivePerformanceOptimizer()
        metrics = SystemMetrics(memory_usage_percent=85.0)

        bottlenecks = optimizer.detect_bottlenecks(metrics)

        assert len(bottlenecks) == 1
        bottleneck = bottlenecks[0]
        assert bottleneck.type == BottleneckType.MEMORY
        assert bottleneck.severity == OptimizationSeverity.MEDIUM
        assert abs(bottleneck.current_value - 85.0) < 0.001

    def test_detect_bottlenecks_cpu(self):
        """Test CPU bottleneck detection."""
        optimizer = AdaptivePerformanceOptimizer()
        metrics = SystemMetrics(cpu_usage_percent=90.0)

        bottlenecks = optimizer.detect_bottlenecks(metrics)

        assert len(bottlenecks) == 1
        bottleneck = bottlenecks[0]
        assert bottleneck.type == BottleneckType.CPU
        assert bottleneck.severity == OptimizationSeverity.MEDIUM

    async def test_auto_optimize_disabled(self):
        """Test auto optimization when disabled."""
        optimizer = AdaptivePerformanceOptimizer(enable_auto_optimization=False)
        metrics = SystemMetrics(cpu_usage_percent=95.0, memory_usage_percent=90.0)

        optimizations = await optimizer.auto_optimize(metrics)

        assert len(optimizations) == 0

    async def test_auto_optimize_cooldown(self):
        """Test auto optimization respects cooldown period."""
        optimizer = AdaptivePerformanceOptimizer(optimization_cooldown=300.0)
        optimizer.last_optimization_time = (
            optimizer.last_optimization_time + 100
        )  # Recent optimization

        metrics = SystemMetrics(cpu_usage_percent=95.0)
        optimizations = await optimizer.auto_optimize(metrics)

        assert len(optimizations) == 0

    async def test_auto_optimize_applies_strategies(self):
        """Test auto optimization applies strategies."""
        optimizer = AdaptivePerformanceOptimizer(
            optimization_cooldown=0.0
        )  # No cooldown
        metrics = SystemMetrics(cpu_usage_percent=90.0, memory_usage_percent=85.0)

        optimizations = await optimizer.auto_optimize(metrics)

        assert len(optimizations) >= 1  # Should apply at least one strategy
        assert optimizer.last_optimization_time > 0

    def test_get_performance_summary_no_data(self):
        """Test performance summary with no data."""
        optimizer = AdaptivePerformanceOptimizer()
        summary = optimizer.get_performance_summary()

        assert summary["status"] == "no_data"

    def test_get_performance_summary_with_data(self):
        """Test performance summary with metrics data."""
        optimizer = AdaptivePerformanceOptimizer()
        optimizer.metrics_history.append(
            SystemMetrics(
                cpu_usage_percent=75.0,
                memory_usage_percent=60.0,
                response_time_p95_ms=800.0,
            )
        )

        summary = optimizer.get_performance_summary()

        assert "current_metrics" in summary
        assert abs(summary["current_metrics"]["cpu_percent"] - 75.0) < 0.001
        assert abs(summary["current_metrics"]["memory_percent"] - 60.0) < 0.001
        assert "optimization_stats" in summary
        assert "monitoring_status" in summary


class TestLocalMemoryCache:
    """Test local memory cache implementation."""

    async def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = LocalMemoryCache()

        await cache.set("test_key", "test_value")
        _ = await cache.get("test_key")

        assert result == "test_value"

    async def test_get_nonexistent_key(self):
        """Test getting non-existent key returns None."""
        cache = LocalMemoryCache()

        _ = await cache.get("nonexistent")

        assert result is None

    async def test_delete(self):
        """Test delete operation."""
        cache = LocalMemoryCache()

        await cache.set("test_key", "test_value")
        deleted = await cache.delete("test_key")

        assert deleted is True

        _ = await cache.get("test_key")
        assert result is None

    async def test_delete_nonexistent(self):
        """Test deleting non-existent key."""
        cache = LocalMemoryCache()

        deleted = await cache.delete("nonexistent")

        assert deleted is False

    async def test_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        cache = LocalMemoryCache(max_size=2)

        # Fill cache to capacity
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")

        # Access key1 to make it more recently used
        await cache.get("key1")

        # Add another item, should evict key2 (least recently used)
        await cache.set("key3", "value3")

        assert await cache.get("key1") == "value1"  # Should still exist
        assert await cache.get("key2") is None  # Should be evicted
        assert await cache.get("key3") == "value3"  # Should exist

    def test_get_metrics(self):
        """Test getting cache metrics."""
        cache = LocalMemoryCache()

        metrics = cache.get_metrics()

        assert isinstance(metrics, CacheMetrics)
        assert abs(metrics.hit_rate - 0.0) < 0.001
        assert abs(metrics.miss_rate - 0.0) < 0.001
        assert metrics.total_operations == 0

    async def test_metrics_hit_rate(self):
        """Test hit rate calculation."""
        cache = LocalMemoryCache()

        await cache.set("key1", "value1")

        # Hit
        await cache.get("key1")
        # Miss
        await cache.get("key2")

        metrics = cache.get_metrics()

        assert abs(metrics.hit_rate - 0.5) < 0.001  # 1 hit out of 2 operations
        assert abs(metrics.miss_rate - 0.5) < 0.001  # 1 miss out of 2 operations
        assert metrics.total_operations == 2


class TestAdaptiveCacheManager:
    """Test adaptive cache manager."""

    def test_init(self):
        """Test cache manager initialization."""
        manager = AdaptiveCacheManager()

        assert CacheType.LOCAL_MEMORY in manager.cache_strategies
        assert len(manager.optimal_cache_mapping) == 7  # All DataType enums

    def test_get_optimal_cache(self):
        """Test getting optimal cache for data type."""
        manager = AdaptiveCacheManager()

        cache = manager.get_optimal_cache(DataType.SESSION)

        assert isinstance(cache, LocalMemoryCache)

    async def test_get_and_set(self):
        """Test get and set operations through manager."""
        manager = AdaptiveCacheManager()

        await manager.set("test_key", "test_value", DataType.SESSION)
        _ = await manager.get("test_key", DataType.SESSION)

        assert result == "test_value"

    def test_get_cache_summary(self):
        """Test getting cache summary."""
        manager = AdaptiveCacheManager()

        summary = manager.get_cache_summary()

        assert "cache_strategies" in summary
        assert "optimal_mappings" in summary
        assert "local_memory" in summary["cache_strategies"]
