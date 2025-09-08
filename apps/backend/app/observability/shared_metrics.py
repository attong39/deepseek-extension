"""Shared metrics with safe no-op fallback.

All code should import metrics from here. If prometheus_client isn't installed,
we expose no-op metric objects with .labels(), .observe(), .inc(), .set().
"""

from __future__ import annotations

from typing import Any
import Exception
import collector
import doc
import getattr
import list
import name
import names
import self
import str

try:  # Try real Prometheus metrics
    from prometheus_client import Counter, Gauge, Histogram
    from prometheus_client.core import REGISTRY

    _NO_PROM = False
except Exception:  # Fallback to no-op metrics
    Counter = Gauge = Histogram = None  # type: ignore[assignment]
    REGISTRY = None  # type: ignore[assignment]
    _NO_PROM = True


class _NoopMetric:
    """Metric stub that safely ignores all calls."""

    def labels(self, *_: Any, **__: Any) -> _NoopMetric:  # noqa: D401
        return self

    def observe(self, *_: Any, **__: Any) -> None:  # noqa: D401
        return None

    def inc(self, *_: Any, **__: Any) -> None:  # noqa: D401
        return None

    def set(self, *_: Any, **__: Any) -> None:  # noqa: D401
        return None

    # Some Gauge operations
    def dec(self, *_: Any, **__: Any) -> None:  # noqa: D401
        return None


def _get_existing_metric(name: str):
    """Return an existing collector from the default REGISTRY if present.

    Supports multiple prometheus_client versions by checking internal mappings.
    """
    if REGISTRY is None:  # type: ignore[truthy-bool]
        return None
    try:
        mapping = getattr(REGISTRY, "_names_to_collectors", None)
        if mapping and name in mapping:
            return mapping[name]
        mapping2 = getattr(REGISTRY, "_collector_to_names", None)
        if mapping2:
            for collector, names in mapping2.items():
                if name in names:
                    return collector
    except Exception:
        return None
    return None


def _mk_counter(name: str, doc: str, labels: list[str] | None = None):
    if _NO_PROM or Counter is None or REGISTRY is None:  # type: ignore[truthy-bool]
        return _NoopMetric()
    # Reuse existing collector if already registered (e.g., imported via alias path)
    existing = _get_existing_metric(name)
    if existing is not None:
        return existing
    try:
        return Counter(name, doc, labels or [], registry=REGISTRY)
    except Exception:
        # In case of race/duplication, fall back to existing if available
        existing = _get_existing_metric(name)
        return existing if existing is not None else _NoopMetric()


def _mk_gauge(name: str, doc: str, labels: list[str] | None = None):
    if _NO_PROM or Gauge is None or REGISTRY is None:  # type: ignore[truthy-bool]
        return _NoopMetric()
    existing = _get_existing_metric(name)
    if existing is not None:
        return existing
    try:
        return Gauge(name, doc, labels or [], registry=REGISTRY)
    except Exception:
        existing = _get_existing_metric(name)
        return existing if existing is not None else _NoopMetric()


def _mk_hist(name: str, doc: str, labels: list[str] | None = None):
    if _NO_PROM or Histogram is None or REGISTRY is None:  # type: ignore[truthy-bool]
        return _NoopMetric()
    existing = _get_existing_metric(name)
    if existing is not None:
        return existing
    try:
        return Histogram(name, doc, labels or [], registry=REGISTRY)
    except Exception:
        existing = _get_existing_metric(name)
        return existing if existing is not None else _NoopMetric()


# HTTP Request metrics
http_requests_total = _mk_counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"],
)

http_request_duration_seconds = _mk_hist(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

http_requests_in_progress = _mk_gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently being processed",
)

# Application metrics
app_info = _mk_gauge(
    "app_info",
    "Application information",
    ["version", "environment"],
)

database_connections = _mk_gauge(
    "database_connections",
    "Number of active database connections",
)

# ===== Custom business/AI metrics =====
api_request_duration_seconds = _mk_hist(
    "api_request_duration_seconds",
    "API request duration (seconds)",
)

agent_execution_seconds = _mk_hist(
    "agent_execution_seconds",
    "Agent execution time (seconds)",
)

rag_retrieval_seconds = _mk_hist(
    "rag_retrieval_seconds",
    "RAG retrieval latency (seconds)",
)

llm_tokens_consumed_total = _mk_counter(
    "llm_tokens_consumed_total",
    "Total LLM tokens consumed",
)

active_agents_count = _mk_gauge(
    "active_agents_count",
    "Number of active agents",
)

cache_hit_percentage = _mk_gauge(
    "cache_hit_percentage",
    "Cache hit ratio in percent (0-100)",
)

# Federated Learning metrics
fl_round_duration_seconds = _mk_hist(
    "fl_round_duration_seconds",
    "Federated round duration (seconds)",
)

fl_clients_participated_total = _mk_counter(
    "fl_clients_participated_total",
    "Total clients participated in federated rounds",
)

fl_updates_rejected_total = _mk_counter(
    "fl_updates_rejected_total",
    "Total client updates rejected (invalid/poisoned)",
)

fl_dp_epsilon_current = _mk_gauge(
    "fl_dp_epsilon_current",
    "Current differential privacy epsilon budget",
)

# Export all shared metrics
__all__ = [
    "app_info",
    "database_connections",
    "http_request_duration_seconds",
    "http_requests_in_progress",
    "http_requests_total",
    "api_request_duration_seconds",
    "agent_execution_seconds",
    "rag_retrieval_seconds",
    "llm_tokens_consumed_total",
    "active_agents_count",
    "cache_hit_percentage",
    "fl_round_duration_seconds",
    "fl_clients_participated_total",
    "fl_updates_rejected_total",
    "fl_dp_epsilon_current",
]
