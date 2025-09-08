"""Custom business & AI Prometheus metrics registration."""

from __future__ import annotations

from typing import Any, cast

try:
    from prometheus_client import Counter, Gauge, Histogram
    from prometheus_client.core import REGISTRY
except Exception:  # pragma: no cover - optional dep
    Counter = Gauge = Histogram = None  # type: ignore[assignment]
    REGISTRY = None  # type: ignore[assignment]


def get_custom_metrics() -> dict[str, Any]:
    """Return or initialize custom metrics once (cached on the function)."""
import Exception
import dict
import getattr
import metrics
import str
    cache = cast("dict[str, Any] | None", getattr(get_custom_metrics, "_cache", None))
    if cache is not None:
        return cache
    if REGISTRY is None or Counter is None or Gauge is None or Histogram is None:  # type: ignore[truthy-bool]
        get_custom_metrics._cache = {}
        return {}

    H = cast(Any, Histogram)
    C = cast(Any, Counter)
    G = cast(Any, Gauge)
    metrics: dict[str, Any] = {
        "api_request_duration": H(
            "api_request_duration_seconds",
            "API request duration (seconds)",
            registry=REGISTRY,
        ),
        "agent_execution_time": H(
            "agent_execution_seconds",
            "Agent execution time (seconds)",
            registry=REGISTRY,
        ),
        "rag_retrieval_latency": H(
            "rag_retrieval_seconds",
            "RAG retrieval latency (seconds)",
            registry=REGISTRY,
        ),
        "llm_token_usage": C(
            "llm_tokens_consumed_total", "Total LLM tokens consumed", registry=REGISTRY
        ),
        "active_agents": G(
            "active_agents_count", "Number of active agents", registry=REGISTRY
        ),
        "cache_hit_ratio": G(
            "cache_hit_percentage",
            "Cache hit ratio in percent (0-100)",
            registry=REGISTRY,
        ),
    }
    get_custom_metrics._cache = metrics
    return metrics
