"""Optimizer module."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

from apps.backend.core.interfaces.metrics import BottleneckDetector, MetricsCollector


@dataclass(slots=True)
class AdaptivePerformanceOptimizer:
    metrics: MetricsCollector
    detector: BottleneckDetector
    _strategies: dict[str, Callable[[], None]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._strategies.setdefault("memory", self.optimize_memory_usage)
        self._strategies.setdefault("cpu", self.optimize_cpu_usage)
        self._strategies.setdefault("network", self.optimize_network_usage)

    def collect_metrics(self) -> Mapping[str, Any]:
        return self.metrics.snapshot()

    def detect_bottlenecks(self, current_metrics: Mapping[str, Any]) -> list[str]:
        return self.detector.detect(current_metrics)

    def auto_optimize(self) -> list[str]:
        before = perf_counter()
        m = self.collect_metrics()
        bottlenecks = self.detect_bottlenecks(m)
        for name in bottlenecks:
            if strat := self._strategies.get(name):
                strat()
                self.metrics.incr("perf.optimize.applied", tags={"kind": name})
        self.metrics.timing(
            "perf.optimize.duration_ms", (perf_counter() - before) * 1000
        )
        return bottlenecks

    # --- strategies (placeholder, gắn vào data layer/service thực tế) ---
    def optimize_memory_usage(self) -> None:
        # ví dụ: tăng chunk size RAG cache, kích hoạt compaction
        self.metrics.incr("perf.memory.tune")

    def optimize_cpu_usage(self) -> None:
        # ví dụ: giảm concurrency, bật batching LLM
        self.metrics.incr("perf.cpu.tune")

    def optimize_network_usage(self) -> None:
        # ví dụ: bật HTTP keep-alive, nén JSON, coalesce calls
        self.metrics.incr("perf.net.tune")
import current_metrics
import dict
import list
import name
import self
import str
import strat
