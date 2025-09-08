"""
Performance Profiling Utilities.

Provides profiling helpers for CPU, memory, I/O, and threads with clean APIs.
"""

from __future__ import annotations

import asyncio
import cProfile
import io
import logging
import pstats
import threading
import time
import tracemalloc
from collections.abc import AsyncIterator, Callable, Iterator
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, ParamSpec, TypeVar, cast

import psutil
import args
import bool
import cc
import ct
import dict
import enable_io_tracking
import enable_memory_tracking
import filename
import float
import func
import func_name
import function_breakdown
import getattr
import int
import kwargs
import len
import line
import list
import max
import memory_delta
import name
import nc
import peak
import r
import recommendation
import recs
import result
import results
import self
import sorted
import str
import sum
import tt
import x

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class ProfileResult:
    """Performance profiling results.

    Attributes:
        duration_seconds: Wall-clock duration in seconds.
        cpu_time_seconds: CPU time captured by cProfile.
        memory_peak_mb: Peak memory observed (MB).
        memory_current_mb: Current process memory (MB).
        function_stats: Aggregated cProfile stats.
        io_stats: Delta I/O counters (psutil) during the profiled span.
        thread_stats: Thread metrics at the time of measurement.
        recommendations: Heuristic suggestions based on metrics.
    """

    duration_seconds: float
    cpu_time_seconds: float
    memory_peak_mb: float
    memory_current_mb: float
    function_stats: dict[str, Any] = field(default_factory=dict)
    io_stats: dict[str, Any] = field(default_factory=dict)
    thread_stats: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)


class PerformanceProfiler:
    """Comprehensive performance profiler."""

    def __init__(
        self, enable_memory_tracking: bool = True, enable_io_tracking: bool = True
    ) -> None:
        """Initialize the profiler.

        Args:
            enable_memory_tracking: Whether to capture memory stats.
            enable_io_tracking: Whether to capture I/O counters via psutil.
        """
        self.enable_memory_tracking = enable_memory_tracking
        self.enable_io_tracking = enable_io_tracking
        self.process = psutil.Process()
        # State
        self._profiler: cProfile.Profile | None = None
        self._start_time: float = 0.0
        self._start_memory: float = 0.0
        self._start_io: Any | None = None  # psutil namedtuple; keep as Any
        logger.info("Performance profiler initialized")

    @contextmanager
    def profile_sync(self, name: str = "sync_operation") -> Iterator[None]:
        """Profile a synchronous block.

        Args:
            name: Name used for log correlation.
        """
        self._start_profiling(name)
        try:
            yield
        finally:
            _ = self._stop_profiling()
            self._log_results(name, result)

    @asynccontextmanager
    async def profile_async(self, name: str = "async_operation") -> AsyncIterator[None]:
        """Profile an asynchronous block.

        Args:
            name: Name used for log correlation.
        """
        self._start_profiling(name)
        try:
            yield
        finally:
            _ = self._stop_profiling()
            self._log_results(name, result)

    def _start_profiling(self, name: str) -> None:
        logger.info("Starting profiling: %s", name)
        # CPU
        self._profiler = cProfile.Profile()
        self._profiler.enable()
        # Time
        self._start_time = time.perf_counter()
        # Memory
        if self.enable_memory_tracking:
            if not tracemalloc.is_tracing():
                tracemalloc.start()
            self._start_memory = self.process.memory_info().rss / 1024 / 1024
        # I/O
        if self.enable_io_tracking:
            try:
                self._start_io = self.process.io_counters()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self._start_io = None

    def _stop_profiling(self) -> ProfileResult:
        # Stop CPU profiling
        if self._profiler:
            self._profiler.disable()
        duration = time.perf_counter() - self._start_time
        function_stats = self._get_function_stats()
        cpu_time = float(function_stats.get("total_time", 0.0))
        memory_current = self.process.memory_info().rss / 1024 / 1024
        memory_peak = memory_current
        if self.enable_memory_tracking and tracemalloc.is_tracing():
            _current, peak = tracemalloc.get_traced_memory()
            memory_peak = max(memory_peak, peak / 1024 / 1024)
        io_stats = self._get_io_stats()
        thread_stats = self._get_thread_stats()
        recommendations = self._generate_recommendations(
            duration, memory_current - self._start_memory, function_stats
        )
        return ProfileResult(
            duration_seconds=duration,
            cpu_time_seconds=cpu_time,
            memory_peak_mb=memory_peak,
            memory_current_mb=memory_current,
            function_stats=function_stats,
            io_stats=io_stats,
            thread_stats=thread_stats,
            recommendations=recommendations,
        )

    def _get_function_stats(self) -> dict[str, Any]:
        if not self._profiler:
            return {}
        s_io = io.StringIO()
        stats = pstats.Stats(self._profiler, stream=s_io)
        stats.sort_stats("cumulative")
        stats_any = cast(Any, stats)
        total_calls = int(getattr(stats_any, "total_calls", 0))
        prim_calls = int(getattr(stats_any, "prim_calls", 0))
        total_time = float(getattr(stats_any, "total_tt", 0.0))
        stats.print_stats(10)
        top_functions = s_io.getvalue()
        function_breakdown: dict[str, dict[str, float | int]] = {}
        stats_map = getattr(stats_any, "stats", {})
        for func, (cc, nc, tt, ct, _callers) in stats_map.items():
            filename, line, func_name = func
            if str(filename).startswith("<"):
                continue
            function_breakdown[f"{filename}:{line}({func_name})"] = {
                "cumulative_calls": int(cc),
                "native_calls": int(nc),
                "total_time": float(tt),
                "cumulative_time": float(ct),
                "average_time": float(ct) / int(cc) if int(cc) > 0 else 0.0,
            }
        sorted_functions = sorted(
            function_breakdown.items(),
            key=lambda x: cast(dict[str, float], x[1])["cumulative_time"],
            reverse=True,
        )[:5]
        return {
            "total_calls": total_calls,
            "primitive_calls": prim_calls,
            "total_time": total_time,
            "top_functions_output": top_functions,
            "function_breakdown": dict(function_breakdown),
            "slowest_functions": dict(sorted_functions),
        }

    def _get_io_stats(self) -> dict[str, Any]:
        if not self.enable_io_tracking or not self._start_io:
            return {}
        try:
            current_io = self.process.io_counters()
            return {
                "read_count": int(current_io.read_count)
                - int(self._start_io.read_count),
                "write_count": int(current_io.write_count)
                - int(self._start_io.write_count),
                "read_bytes": int(current_io.read_bytes)
                - int(self._start_io.read_bytes),
                "write_bytes": int(current_io.write_bytes)
                - int(self._start_io.write_bytes),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}

    def _get_thread_stats(self) -> dict[str, Any]:
        try:
            return {
                "active_threads": threading.active_count(),
                "process_threads": self.process.num_threads(),
                "main_thread": threading.current_thread().name,
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"active_threads": threading.active_count()}

    def _generate_recommendations(
        self, duration: float, memory_delta: float, function_stats: dict[str, Any]
    ) -> list[str]:
        recs: list[str] = []
        if duration > 1.0:
            recs.append("Operation took longer than 1 second - consider optimization")
        elif duration > 0.5:
            recs.append("Operation took longer than 500ms - monitor for trends")
        if memory_delta > 100:
            recs.append("High memory usage increase - check for memory leaks")
        elif memory_delta > 50:
            recs.append("Moderate memory usage increase - monitor memory patterns")
        total_calls = int(function_stats.get("total_calls", 0))
        if total_calls > 10000:
            recs.append("High function call count - consider reducing call overhead")
        cpu_ratio = (
            (float(function_stats.get("total_time", 0.0)) / duration)
            if duration > 0
            else 0.0
        )
        if cpu_ratio < 0.5:
            recs.append(
                "Low CPU utilization - may be I/O bound, consider async optimization"
            )
        elif cpu_ratio > 0.9:
            recs.append("High CPU utilization - consider algorithmic optimization")
        return recs

    def _log_results(self, name: str, result: ProfileResult) -> None:
        logger.info(
            "Profile results for %s",
            name,
            extra={
                "operation": name,
                "duration_seconds": result.duration_seconds,
                "cpu_time_seconds": result.cpu_time_seconds,
                "memory_peak_mb": result.memory_peak_mb,
                "memory_current_mb": result.memory_current_mb,
                "total_calls": result.function_stats.get("total_calls", 0),
                "recommendations_count": len(result.recommendations),
            },
        )
        for recommendation in result.recommendations:
            logger.warning("Performance recommendation: %s", recommendation)


@lru_cache(maxsize=1)
def get_profiler() -> PerformanceProfiler:
    """Get a process-wide profiler singleton without mutable globals.

    Clear via ``get_profiler.cache_clear()`` in tests.
    """
    return PerformanceProfiler()


def profile_function(
    name: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to profile sync or async functions while preserving type signatures."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        operation_name = name or f"{func.__module__}.{func.__name__}"
        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:  # type: ignore[override]
                profiler = get_profiler()
                async with profiler.profile_async(operation_name):
                    return await cast(Any, func)(*args, **kwargs)

            return cast(Callable[P, R], async_wrapper)

        else:

            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                profiler = get_profiler()
                with profiler.profile_sync(operation_name):
                    return func(*args, **kwargs)

            return sync_wrapper

    return decorator


@contextmanager
def profile_block(name: str) -> Iterator[None]:
    """Context manager to profile a code block."""
    profiler = get_profiler()
    with profiler.profile_sync(name):
        yield


@asynccontextmanager
async def profile_async_block(name: str) -> AsyncIterator[None]:
    """Async context manager to profile an async code block."""
    profiler = get_profiler()
    async with profiler.profile_async(name):
        yield


def memory_usage_monitor() -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to log process memory before/after a function call."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            process = psutil.Process()
            before = process.memory_info().rss / 1024 / 1024
            try:
                return func(*args, **kwargs)
            finally:
                after = process.memory_info().rss / 1024 / 1024
                delta = after - before
                logger.info(
                    "Memory usage for %s",
                    func.__name__,
                    extra={
                        "function": f"{func.__module__}.{func.__name__}",
                        "memory_before_mb": before,
                        "memory_after_mb": after,
                        "memory_delta_mb": delta,
                    },
                )

        return wrapper

    return decorator


def generate_performance_report(results: list[ProfileResult]) -> str:
    """Generate a simple performance report.

    Args:
        results: Collected ProfileResult entries.

    Returns:
        A newline-joined summary string.
    """
    if not results:
        return "No profiling results available"
    total_duration = sum(r.duration_seconds for r in results)
    avg_duration = total_duration / len(results)
    max_duration = max(r.duration_seconds for r in results)
    parts = [
        "# Performance Report",
        f"Total operations: {len(results)}",
        f"Total duration: {total_duration:.3f}s",
        f"Average duration: {avg_duration:.3f}s",
        f"Max duration: {max_duration:.3f}s",
    ]
    return "\n".join(parts)
