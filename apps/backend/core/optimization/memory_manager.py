from __future__ import annotations

import gc
import logging
import os
import resource
import sys
import threading
import time
from collections.abc import Callable
from contextlib import contextmanager
from functools import lru_cache
from typing import Any, TypeVar
from weakref import WeakValueDictionary

import psutil
import Exception
import ImportError
import attr_name
import bool
import cache_obj
import cache_object
import dict
import dir
import e
import factory_fn
import float
import generation
import getattr
import hasattr
import int
import len
import list
import name
import operation_name
import range
import reason
import round
import self
import str
import sum

"""
Memory optimization system for achieving < 300MB target.
Provides intelligent memory management with:
- Object pooling with weak references
- Cache management with size limits
- Garbage collection optimization
- Real-time memory monitoring
- Automatic memory pressure detection
"""
try:
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
logger = logging.getLogger(__name__)
T = TypeVar("T")


class MemoryManager:
    """Intelligent memory management for < 300MB target."""

    def __init__(self, target_mb: int = 300, warning_mb: int = 250):
        """Initialize memory manager with targets."""
        self.target_bytes = target_mb * 1024 * 1024
        self.warning_bytes = warning_mb * 1024 * 1024
        self._object_pool: WeakValueDictionary[str, Any] = WeakValueDictionary()
        self._cache_registry: dict[str, Any] = {}
        self._optimization_count = 0
        self._last_optimization = 0.0
        self._lock = threading.RLock()
        logger.info(f"MemoryManager initialized with {target_mb}MB target")

    @contextmanager
    def memory_tracking(self, operation_name: str):
        """Context manager to track memory usage of operations."""
        start_memory = self.get_current_memory_mb()
        start_time = time.time()
        try:
            yield
        finally:
            end_memory = self.get_current_memory_mb()
            duration = time.time() - start_time
            memory_delta = end_memory - start_memory
            logger.debug(
                f"Operation '{operation_name}': "
                f"memory_delta={memory_delta:.1f}MB, "
                f"duration={duration:.3f}s"
            )
            if memory_delta > 50:  # 50MB increase
                self.optimize_memory(reason=f"High memory delta from {operation_name}")

    def get_current_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process(os.getpid())
                return process.memory_info().rss / 1024 / 1024
            except Exception as e:
                logger.warning(f"Failed to get psutil memory info: {e}")
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

    @lru_cache(maxsize=128)
    def get_cached_object(self, key: str, factory_fn: Callable[[], T]) -> T:
        """Object pooling with LRU eviction."""
        return factory_fn()

    def register_cache(self, name: str, cache_object: Any) -> None:
        """Register a cache for management."""
        with self._lock:
            self._cache_registry[name] = cache_object
            logger.debug(f"Registered cache: {name}")

    def monitor_memory(self) -> dict[str, Any]:
        """Real-time memory monitoring with detailed stats."""
        current_memory = self.get_current_memory_mb()
        memory_stats = {
            "current_mb": round(current_memory, 2),
            "target_mb": self.target_bytes / 1024 / 1024,
            "warning_mb": self.warning_bytes / 1024 / 1024,
            "within_target": current_memory < (self.target_bytes / 1024 / 1024),
            "within_warning": current_memory < (self.warning_bytes / 1024 / 1024),
            "usage_percentage": round(
                (current_memory / (self.target_bytes / 1024 / 1024)) * 100, 1
            ),
            "optimizations_performed": self._optimization_count,
        }
        try:
            gc_stats = {
                "generation_0": len(gc.get_objects(0)),
                "generation_1": len(gc.get_objects(1)),
                "generation_2": len(gc.get_objects(2)),
                "gc_counts": gc.get_count(),
                "gc_thresholds": gc.get_threshold(),
            }
            memory_stats["gc_stats"] = gc_stats
        except Exception as e:
            logger.debug(f"Failed to get GC stats: {e}")
        if PSUTIL_AVAILABLE:
            try:
                process = psutil.Process(os.getpid())
                memory_info = process.memory_info()
                memory_stats.update(
                    {
                        "rss_mb": round(memory_info.rss / 1024 / 1024, 2),
                        "vms_mb": round(memory_info.vms / 1024 / 1024, 2),
                        "memory_percent": round(process.memory_percent(), 2),
                    }
                )
            except Exception as e:
                logger.debug(f"Failed to get detailed process stats: {e}")
        return memory_stats

    def optimize_memory(self, reason: str = "manual") -> dict[str, Any]:
        """Trigger comprehensive memory optimization."""
        with self._lock:
            start_memory = self.get_current_memory_mb()
            start_time = time.time()
            optimization_results = {
                "reason": reason,
                "start_memory_mb": start_memory,
                "optimizations": [],
            }
            try:
                collected_objects = []
                for generation in range(3):
                    collected = gc.collect(generation)
                    collected_objects.append(collected)
                optimization_results["optimizations"].append(
                    {
                        "type": "garbage_collection",
                        "collected_objects": collected_objects,
                        "total_collected": sum(collected_objects),
                    }
                )
                cache_clears = self._clear_lru_caches()
                optimization_results["optimizations"].append(
                    {
                        "type": "lru_cache_clear",
                        "caches_cleared": cache_clears,
                    }
                )
                current_memory = self.get_current_memory_mb()
                if current_memory > (self.warning_bytes / 1024 / 1024):
                    cleared_caches = self._clear_registered_caches()
                    optimization_results["optimizations"].append(
                        {
                            "type": "registered_cache_clear",
                            "caches_cleared": cleared_caches,
                        }
                    )
                pool_optimization = self._optimize_object_pool()
                optimization_results["optimizations"].append(
                    {
                        "type": "object_pool_optimization",
                        **pool_optimization,
                    }
                )
                end_memory = self.get_current_memory_mb()
                duration = time.time() - start_time
                memory_saved = start_memory - end_memory
                optimization_results.update(
                    {
                        "end_memory_mb": end_memory,
                        "memory_saved_mb": round(memory_saved, 2),
                        "duration_ms": round(duration * 1000, 2),
                        "success": memory_saved > 0,
                    }
                )
                self._optimization_count += 1
                self._last_optimization = time.time()
                logger.info(
                    f"Memory optimization completed: "
                    f"saved {memory_saved:.1f}MB in {duration * 1000:.1f}ms"
                )
            except Exception as e:
                optimization_results["error"] = str(e)
                logger.error(f"Memory optimization failed: {e}")
            return optimization_results

    def _clear_lru_caches(self) -> list[str]:
        """Clear all LRU caches."""
        cleared = []
        try:
            self.get_cached_object.cache_clear()
            cleared.append("get_cached_object")
        except Exception as e:
            logger.debug(f"Failed to clear get_cached_object cache: {e}")
        current_module = sys.modules[__name__]
        for attr_name in dir(current_module):
            try:
                attr = getattr(current_module, attr_name)
                if hasattr(attr, "cache_clear"):
                    attr.cache_clear()
                    cleared.append(attr_name)
            except Exception as e:
                logger.debug(f"Failed to clear cache {attr_name}: {e}")
        return cleared

    def _clear_registered_caches(self) -> list[str]:
        """Clear all registered caches."""
        cleared = []
        for name, cache_obj in list(self._cache_registry.items()):
            try:
                if hasattr(cache_obj, "clear"):
                    cache_obj.clear()
                    cleared.append(name)
                elif hasattr(cache_obj, "cache_clear"):
                    cache_obj.cache_clear()
                    cleared.append(name)
            except Exception as e:
                logger.debug(f"Failed to clear registered cache {name}: {e}")
        return cleared

    def _optimize_object_pool(self) -> dict[str, Any]:
        """Optimize the object pool."""
        pool_size_before = len(self._object_pool)
        try:
            _ = list(self._object_pool.keys())
            pool_size_after = len(self._object_pool)
            return {
                "pool_size_before": pool_size_before,
                "pool_size_after": pool_size_after,
                "objects_released": pool_size_before - pool_size_after,
            }
        except Exception as e:
            logger.debug(f"Object pool optimization failed: {e}")
            return {
                "pool_size_before": pool_size_before,
                "error": str(e),
            }

    def should_optimize(self) -> bool:
        """Check if memory optimization should be triggered."""
        current_memory = self.get_current_memory_mb()
        if current_memory > (self.warning_bytes / 1024 / 1024):
            return True
        time_since_last = time.time() - self._last_optimization
        if time_since_last > 300:  # 5 minutes
            return True
        return False

    def get_memory_pressure_level(self) -> str:
        """Get current memory pressure level."""
        current_memory = self.get_current_memory_mb()
        target_mb = self.target_bytes / 1024 / 1024
        warning_mb = self.warning_bytes / 1024 / 1024
        if current_memory > target_mb:
            return "critical"
        elif current_memory > warning_mb:
            return "warning"
        elif current_memory > (warning_mb * 0.8):
            return "moderate"
        else:
            return "normal"

    def get_optimization_stats(self) -> dict[str, Any]:
        """Get statistics about memory optimizations."""
        return {
            "total_optimizations": self._optimization_count,
            "last_optimization_timestamp": self._last_optimization,
            "time_since_last_optimization": time.time() - self._last_optimization,
            "should_optimize": self.should_optimize(),
            "memory_pressure": self.get_memory_pressure_level(),
            "registered_caches": list(self._cache_registry.keys()),
            "object_pool_size": len(self._object_pool),
        }


_memory_manager: MemoryManager | None = None


def get_memory_manager() -> MemoryManager:
    """Get the global memory manager instance."""
    global _memory_manager
    if _memory_manager is None:
        target_mb = int(os.getenv("MEMORY_TARGET_MB", "300"))
        _memory_manager = MemoryManager(target_mb=target_mb)
    return _memory_manager


def optimize_memory_if_needed() -> dict[str, Any] | None:
    """Auto-optimize memory if needed."""
    manager = get_memory_manager()
    if manager.should_optimize():
        return manager.optimize_memory(reason="auto_optimization")
    return None


memory_tracking = get_memory_manager().memory_tracking
monitor_memory = get_memory_manager().monitor_memory
optimize_memory = get_memory_manager().optimize_memory
__all__ = [
    "MemoryManager",
    "PSUTIL_AVAILABLE",
    "T",
    "attr",
    "cache_clears",
    "cleared",
    "cleared_caches",
    "collected",
    "collected_objects",
    "current_memory",
    "current_module",
    "duration",
    "end_memory",
    "gc_stats",
    "get_cached_object",
    "get_current_memory_mb",
    "get_memory_manager",
    "get_memory_pressure_level",
    "get_optimization_stats",
    "logger",
    "manager",
    "memory_delta",
    "memory_info",
    "memory_saved",
    "memory_stats",
    "memory_tracking",
    "monitor_memory",
    "optimization_results",
    "optimize_memory",
    "optimize_memory_if_needed",
    "pool_optimization",
    "pool_size_after",
    "pool_size_before",
    "process",
    "register_cache",
    "should_optimize",
    "start_memory",
    "start_time",
    "target_mb",
    "time_since_last",
    "warning_mb",
]
