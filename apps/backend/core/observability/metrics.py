"""Metrics module."""

from __future__ import annotations

from typing import Any

try:
    from prometheus_client import Counter, Gauge, Histogram
except Exception:  # pragma: no cover
    # Lightweight fallbacks if prometheus_client not available
    class _Dummy:
        def __init__(self, *_: Any, **__: Any) -> None:
            # Empty init for dummy fallback - no state needed for no-op metrics
            pass

        def __call__(self, *_: Any, **__: Any) -> _Dummy:
            return self

        def labels(self, *_: Any, **__: Any) -> _Dummy:
            return self

        def inc(self, *_: Any, **__: Any) -> None:
            # no-op fallback when prometheus_client is unavailable
            return None

        def dec(self, *_: Any, **__: Any) -> None:
            # no-op fallback when prometheus_client is unavailable
            return None

        def observe(self, *_: Any, **__: Any) -> None:
            # no-op fallback when prometheus_client is unavailable
            return None

    Counter = Gauge = Histogram = _Dummy  # type: ignore

REQUEST_COUNT = Counter(
    "zeta_request_total", "Total HTTP requests", ["path", "method", "status"]
)  # type: ignore
LATENCY = Histogram(
    "zeta_request_latency_seconds", "HTTP request latency", ["path", "method"]
)  # type: ignore

# RAG retrieval latency histogram (used by memory/search)
RAG_RETRIEVAL_SECONDS = Histogram(
    "rag_retrieval_seconds",
    "RAG retrieval latency in seconds",
    buckets=(0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.2, 0.5, 1, 2),
)  # type: ignore

# DB queries counter for detecting N+1 patterns.
DB_QUERIES_TOTAL = Counter(
    "db_queries_total",
    "Database query invocations",
    ["operation", "model", "route"],
)  # type: ignore
import Exception
import self
