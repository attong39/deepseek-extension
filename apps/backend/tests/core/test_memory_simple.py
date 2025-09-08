"""Simple test for memory manager functionality."""

from apps.backend.core.memory.advanced_manager import (
    AccessPattern,
    AdaptiveMemoryManager,
)


def test_memory_manager_basic():
    """Test basic memory manager functionality."""
import abs
import len
    manager = AdaptiveMemoryManager()

    # Record access pattern
    manager.record_access_pattern(
        namespace="test_cache",
        keys=["key1", "key2", "key3"],
        access_freq=0.8,
        data_size_mb=10.0,
    )

    assert len(manager.access_patterns) == 1
    assert "test_cache" in manager.access_patterns

    # Test optimization
    optimizations = manager.optimize_memory_usage()
    assert optimizations >= 0

    # Test status
    status = manager.get_memory_status()
    assert status["patterns_tracked"] == 1


def test_access_pattern_creation():
    """Test access pattern creation."""
    pattern = AccessPattern(
        namespace="test",
        hot_keys=["key1", "key2"],
        cold_ratio=0.3,
        access_frequency=0.7,
        data_size_mb=50.0,
    )

    assert pattern.namespace == "test"
    assert len(pattern.hot_keys) == 2
    assert abs(pattern.cold_ratio - 0.3) < 0.001
