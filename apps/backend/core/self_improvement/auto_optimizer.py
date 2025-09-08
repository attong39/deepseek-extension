"""Auto-optimization engine cho ZETA_VN.

Tự động điều chỉnh performance parameters dựa trên metrics.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol
import Exception
import apply_callback
import dict
import e
import float
import initial_knobs
import int
import interval_s
import limit
import list
import max
import metrics_adapter
import min
import print
import result
import self
import str
import tuple


@dataclass
class PerformanceKnobs:
    """Configuration knobs cho performance tuning."""

    rag_top_k: int = 6
    ws_batch_ms: int = 16
    outbox_batch: int = 200
    cache_ttl_s: int = 600
    chat_timeout_s: int = 30
    memory_search_timeout_s: int = 5
    max_concurrent_requests: int = 100
    db_pool_size: int = 20


DEFAULT_KNOBS = PerformanceKnobs()


class MetricsAdapter(Protocol):
    """Protocol cho metrics collection."""

    async def histogram_quantile(self, metric: str, quantile: float) -> float | None:
        """Get histogram quantile value."""
        ...

    async def gauge_sum(self, metric: str) -> float | None:
        """Get gauge sum value."""
        ...

    async def counter_rate(self, metric: str, window: str) -> float | None:
        """Get counter rate over time window."""
        ...

    async def estimate_lag_seconds(self, queue_metric: str) -> float:
        """Estimate queue lag in seconds."""
        ...


class AutoOptimizer:
    """
    Tự động thu thập metrics và điều chỉnh knobs theo heuristic.

    Optimization strategies:
    - Nếu p95 chat_stream > 1.2s => giảm rag_top_k (đến min=3), tăng ws_batch_ms (<= 32)
    - Nếu outbox backlog tăng nhanh => tăng outbox_batch đến 400
    - Nếu memory usage cao => giảm cache_ttl_s
    - Nếu DB connection pool saturated => tăng pool size
    """

    def __init__(
        self,
        metrics_adapter: MetricsAdapter,
        apply_callback: Callable[[PerformanceKnobs], Any],
        initial_knobs: PerformanceKnobs | None = None,
    ):
        self.metrics = metrics_adapter
        self.apply_callback = apply_callback
        self.knobs = initial_knobs or DEFAULT_KNOBS
        self.optimization_history: list[dict[str, Any]] = []
        self.last_optimization = 0.0
        self.min_interval = 60.0  # Minimum seconds between optimizations

    async def tick(self) -> dict[str, Any]:
        """Perform one optimization cycle."""
        now = time.time()
        if now - self.last_optimization < self.min_interval:
            return {
                "skipped": "too_soon",
                "next_in": self.min_interval - (now - self.last_optimization),
            }

        # Collect current metrics
        metrics = await self._collect_metrics()

        # Analyze and decide on optimizations
        new_knobs, changes = await self._optimize_knobs(metrics)

        # Apply if there are changes
        if changes:
            old_knobs = self.knobs
            self.knobs = new_knobs

            # Record optimization
            optimization_record = {
                "timestamp": now,
                "old_knobs": old_knobs.__dict__,
                "new_knobs": new_knobs.__dict__,
                "changes": changes,
                "metrics": metrics,
                "reason": self._explain_changes(changes, metrics),
            }
            self.optimization_history.append(optimization_record)

            # Apply changes
            await self.apply_callback(new_knobs)

            self.last_optimization = now

            return {
                "optimized": True,
                "changes": changes,
                "metrics": metrics,
                "new_knobs": new_knobs.__dict__,
            }

        return {"optimized": False, "metrics": metrics, "reason": "no_changes_needed"}

    async def _collect_metrics(self) -> dict[str, Any]:
        """Collect performance metrics từ monitoring system."""
        try:
            return {
                "chat_p95_latency": await self.metrics.histogram_quantile(
                    "chat_response_duration_seconds", 0.95
                ),
                "chat_p99_latency": await self.metrics.histogram_quantile(
                    "chat_response_duration_seconds", 0.99
                ),
                "outbox_backlog": await self.metrics.gauge_sum("outbox_queue_size"),
                "outbox_lag_seconds": await self.metrics.estimate_lag_seconds(
                    "outbox_queue_size"
                ),
                "memory_usage_percent": await self.metrics.gauge_sum(
                    "memory_usage_percent"
                ),
                "db_active_connections": await self.metrics.gauge_sum(
                    "db_active_connections"
                ),
                "concurrent_requests": await self.metrics.gauge_sum("active_requests"),
                "error_rate": await self.metrics.counter_rate(
                    "http_requests_errors_total", "5m"
                ),
                "cache_hit_rate": await self.metrics.counter_rate(
                    "cache_hits_total", "10m"
                ),
            }
        except Exception:
            # Fallback metrics nếu monitoring unavailable
            return {
                "chat_p95_latency": None,
                "outbox_backlog": None,
                "memory_usage_percent": None,
                "error_rate": None,
            }

    async def _optimize_knobs(
        self, metrics: dict[str, Any]
    ) -> tuple[PerformanceKnobs, dict[str, Any]]:
        """Analyze metrics và return optimized knobs."""
        current = self.knobs
        changes = {}

        # Chat performance optimization
        chat_p95 = metrics.get("chat_p95_latency")
        if chat_p95 and chat_p95 > 1.2:
            # Chat is slow - reduce RAG complexity, increase batching
            if current.rag_top_k > 3:
                changes["rag_top_k"] = max(3, current.rag_top_k - 1)
            if current.ws_batch_ms < 32:
                changes["ws_batch_ms"] = min(32, current.ws_batch_ms + 4)
        elif chat_p95 and chat_p95 < 0.5:
            # Chat is fast - can increase quality
            if current.rag_top_k < 10:
                changes["rag_top_k"] = min(10, current.rag_top_k + 1)

        # Outbox performance optimization
        outbox_backlog = metrics.get("outbox_backlog")
        outbox_lag = metrics.get("outbox_lag_seconds")
        if outbox_backlog and outbox_backlog > 1000:
            # High backlog - increase batch size
            if current.outbox_batch < 500:
                changes["outbox_batch"] = min(500, current.outbox_batch + 50)
        elif outbox_lag and outbox_lag > 30:
            # High lag - increase batch size
            if current.outbox_batch < 400:
                changes["outbox_batch"] = min(400, current.outbox_batch + 25)

        # Memory optimization
        memory_usage = metrics.get("memory_usage_percent")
        if memory_usage and memory_usage > 80:
            # High memory - reduce cache TTL
            if current.cache_ttl_s > 300:
                changes["cache_ttl_s"] = max(300, int(current.cache_ttl_s * 0.8))
        elif memory_usage and memory_usage < 50:
            # Low memory - can increase cache TTL
            if current.cache_ttl_s < 1200:
                changes["cache_ttl_s"] = min(1200, int(current.cache_ttl_s * 1.2))

        # Database connection optimization
        db_connections = metrics.get("db_active_connections")
        if db_connections and db_connections > (current.db_pool_size * 0.9):
            # Pool near saturation - increase size
            if current.db_pool_size < 50:
                changes["db_pool_size"] = min(50, current.db_pool_size + 5)

        # Concurrent request optimization
        concurrent_requests = metrics.get("concurrent_requests")
        error_rate = metrics.get("error_rate")
        if error_rate and error_rate > 0.05:  # 5% error rate
            # High errors - reduce concurrent limit
            if current.max_concurrent_requests > 50:
                changes["max_concurrent_requests"] = max(
                    50, current.max_concurrent_requests - 10
                )
        elif concurrent_requests and concurrent_requests < (
            current.max_concurrent_requests * 0.5
        ):
            # Low utilization and low errors - can increase limit
            if current.max_concurrent_requests < 200 and (
                not error_rate or error_rate < 0.01
            ):
                changes["max_concurrent_requests"] = min(
                    200, current.max_concurrent_requests + 10
                )

        # Create new knobs with changes
        new_knobs = PerformanceKnobs(
            rag_top_k=changes.get("rag_top_k", current.rag_top_k),
            ws_batch_ms=changes.get("ws_batch_ms", current.ws_batch_ms),
            outbox_batch=changes.get("outbox_batch", current.outbox_batch),
            cache_ttl_s=changes.get("cache_ttl_s", current.cache_ttl_s),
            chat_timeout_s=changes.get("chat_timeout_s", current.chat_timeout_s),
            memory_search_timeout_s=changes.get(
                "memory_search_timeout_s", current.memory_search_timeout_s
            ),
            max_concurrent_requests=changes.get(
                "max_concurrent_requests", current.max_concurrent_requests
            ),
            db_pool_size=changes.get("db_pool_size", current.db_pool_size),
        )

        return new_knobs, changes

    def _explain_changes(self, changes: dict[str, Any], metrics: dict[str, Any]) -> str:
        """Generate human-readable explanation cho optimization changes."""
        explanations = []

        if "rag_top_k" in changes:
            if changes["rag_top_k"] < self.knobs.rag_top_k:
                explanations.append(
                    f"Reduced RAG top_k to {changes['rag_top_k']} due to high chat latency"
                )
            else:
                explanations.append(
                    f"Increased RAG top_k to {changes['rag_top_k']} due to good performance"
                )

        if "outbox_batch" in changes:
            explanations.append(
                f"Increased outbox batch to {changes['outbox_batch']} due to high backlog"
            )

        if "cache_ttl_s" in changes:
            if changes["cache_ttl_s"] < self.knobs.cache_ttl_s:
                explanations.append(
                    f"Reduced cache TTL to {changes['cache_ttl_s']}s due to high memory usage"
                )
            else:
                explanations.append(
                    f"Increased cache TTL to {changes['cache_ttl_s']}s due to available memory"
                )

        if "db_pool_size" in changes:
            explanations.append(
                f"Increased DB pool to {changes['db_pool_size']} due to connection saturation"
            )

        return (
            "; ".join(explanations) if explanations else "No significant changes needed"
        )

    async def loop(self, interval_s: int = 60) -> None:
        """Continuous optimization loop."""
        while True:
            try:
                _ = await self.tick()
                if result.get("optimized"):
                    print(f"Auto-optimization applied: {result['changes']}")
            except Exception as e:
                print(f"Auto-optimization error: {e}")

            await asyncio.sleep(interval_s)

    def get_optimization_history(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent optimization history."""
        return self.optimization_history[-limit:]

    def get_current_knobs(self) -> PerformanceKnobs:
        """Get current performance knobs."""
        return self.knobs
