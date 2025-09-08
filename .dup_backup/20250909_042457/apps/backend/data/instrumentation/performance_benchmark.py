# zeta_vn/data/instrumentation/performance_benchmark.py
from __future__ import annotations

import statistics
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from apps.backend.data.instrumentation.latency_timer import Timer
import dict
import filename
import float
import func
import input_control
import int
import iterations
import len
import list
import manager
import max
import min
import name
import print
import range
import result
import screen_capture
import self
import str
import t
import times


@dataclass
class BenchmarkResult:
    """Results từ performance benchmark."""

    name: str
    iterations: int
    times: list[float] = field(default_factory=list)
    avg_time: float = 0.0
    min_time: float = 0.0
    max_time: float = 0.0
    p95_time: float = 0.0
    p99_time: float = 0.0
    std_dev: float = 0.0
    throughput: float = 0.0  # Operations per second

    def __post_init__(self) -> None:
        if self.times:
            self.avg_time = statistics.mean(self.times)
            self.min_time = min(self.times)
            self.max_time = max(self.times)
            self.p95_time = statistics.quantiles(self.times, n=20)[
                18
            ]  # 95th percentile
            self.p99_time = statistics.quantiles(self.times, n=100)[
                98
            ]  # 99th percentile
            self.std_dev = statistics.stdev(self.times) if len(self.times) > 1 else 0.0
            self.throughput = 1.0 / self.avg_time if self.avg_time > 0 else 0.0


class PerformanceBenchmark:
    """Comprehensive performance benchmarking cho desktop control modules."""

    def __init__(self) -> None:
        self.results: dict[str, BenchmarkResult] = {}

    def _benchmark_function(
        self, func: Callable[[], Any], iterations: int = 1000, name: str = ""
    ) -> BenchmarkResult:
        """Generic function benchmarking."""
        times: list[float] = []

        # Warmup
        for _ in range(min(10, iterations // 10)):
            func()

        # Actual benchmark
        for _ in range(iterations):
            with Timer(name) as t:
                func()
            times.append(t.duration)

        return self._calculate_result(name, times)

    def benchmark_input_latency(
        self, input_control: Any, iterations: int = 1000
    ) -> BenchmarkResult:
        """Benchmark input control latency."""
        times: list[float] = []

        # Mouse movement benchmark
        for _ in range(iterations):
            with Timer("mouse_move") as t:
                input_control.move_to(500, 500)
            times.append(t.duration)

        _ = self._calculate_result("input_latency", times)
        self.results["input_latency"] = result
        return result

    def benchmark_screen_capture(
        self, screen_capture: Any, iterations: int = 100
    ) -> BenchmarkResult:
        """Benchmark screen capture FPS và latency."""
        times: list[float] = []

        screen_capture.start()

        try:
            # Warmup
            for _ in range(10):
                screen_capture.frame()

            # Benchmark
            for _ in range(iterations):
                with Timer("screen_capture") as t:
                    screen_capture.frame()  # Capture frame without storing
                times.append(t.duration)

        finally:
            screen_capture.stop()

        _ = self._calculate_result("screen_capture", times)
        self.results["screen_capture"] = result
        return result

    def benchmark_end_to_end(
        self, manager: Any, iterations: int = 50
    ) -> BenchmarkResult:
        """Benchmark complete automation loop (capture → detect → action)."""
        times: list[float] = []

        manager.start()

        try:
            for _ in range(iterations):
                with Timer("end_to_end") as t:
                    manager.run_once()
                times.append(t.duration)

        finally:
            manager.stop()

        _ = self._calculate_result("end_to_end", times)
        self.results["end_to_end"] = result
        return result

    def _calculate_result(self, name: str, times: list[float]) -> BenchmarkResult:
        """Calculate comprehensive benchmark statistics."""
        if not times:
            return BenchmarkResult(name=name, iterations=0)

        return BenchmarkResult(
            name=name,
            iterations=len(times),
            times=times,
            avg_time=statistics.mean(times),
            min_time=min(times),
            max_time=max(times),
            p95_time=statistics.quantiles(times, n=20)[18]
            if len(times) >= 20
            else max(times),
            p99_time=statistics.quantiles(times, n=100)[98]
            if len(times) >= 100
            else max(times),
            std_dev=statistics.stdev(times) if len(times) > 1 else 0.0,
            throughput=1.0 / statistics.mean(times)
            if statistics.mean(times) > 0
            else 0.0,
        )

    def benchmark_memory_usage(
        self, func: Callable[[], Any], iterations: int = 100
    ) -> dict[str, float]:
        """Benchmark memory usage during function execution."""
        import os  # noqa: PLC0415

        import psutil  # noqa: PLC0415

        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        for _ in range(iterations):
            func()

        mem_after = process.memory_info().rss / 1024 / 1024  # MB

        return {
            "memory_before_mb": mem_before,
            "memory_after_mb": mem_after,
            "memory_diff_mb": mem_after - mem_before,
            "memory_per_iteration_kb": (mem_after - mem_before) * 1024 / iterations,
        }

    def print_results(self) -> None:
        """Print formatted benchmark results."""
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("=" * 60)

        for name, result in self.results.items():
            print(f"\n{name.upper()}:")
            print(f"  Iterations: {result.iterations}")
            print(f"  Average:    {result.avg_time * 1000:.2f}ms")
            print(f"  Min:        {result.min_time * 1000:.2f}ms")
            print(f"  Max:        {result.max_time * 1000:.2f}ms")
            print(f"  P95:        {result.p95_time * 1000:.2f}ms")
            print(f"  P99:        {result.p99_time * 1000:.2f}ms")
            print(f"  Std Dev:    {result.std_dev * 1000:.2f}ms")
            print(f"  Throughput: {result.throughput:.1f} ops/sec")

    def save_results(self, filename: str) -> None:
        """Save results to JSON file."""
        import json  # noqa: PLC0415
        from pathlib import Path  # noqa: PLC0415

        data = {}
        for name, result in self.results.items():
            data[name] = {
                "iterations": result.iterations,
                "avg_time_ms": result.avg_time * 1000,
                "min_time_ms": result.min_time * 1000,
                "max_time_ms": result.max_time * 1000,
                "p95_time_ms": result.p95_time * 1000,
                "p99_time_ms": result.p99_time * 1000,
                "std_dev_ms": result.std_dev * 1000,
                "throughput_ops_per_sec": result.throughput,
            }

        Path(filename).write_text(json.dumps(data, indent=2))
        print(f"Results saved to {filename}")
