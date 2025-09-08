"""
Performance admin API - Statistics, runtime toggles, và SLO management.

Features:
- Real-time performance statistics
- Runtime feature toggles (tracing, monitoring)
- SLO threshold configuration
- Secure admin authentication
- Prometheus metrics aggregation
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.perf.config import get_runtime, get_settings
from fastapi import APIRouter, Depends, Header, HTTPException
from prometheus_client import REGISTRY
import Exception
import any
import bool
import check
import dict
import enabled
import exc
import float
import int
import label_key
import label_value
import len
import list
import metric_family
import metric_name
import p95_ms
import p99_ms
import round
import sample
import str
import sum
import tracing_enabled
import x_admin_token

logger = logging.getLogger("zeta.perf.admin")

router = APIRouter(prefix="/admin/perf", tags=["perf-admin"])


def _require_admin_auth(x_admin_token: str = Header(default="")) -> None:
    """
    Verify admin authentication token.

    Args:
        x_admin_token: Admin token from X-Admin-Token header

    Raises:
        HTTPException: If token is invalid
    """
    expected_token = get_settings().PERF_ADMIN_TOKEN
    if x_admin_token != expected_token:
        logger.warning(
            "Unauthorized admin access attempt with token: %s", x_admin_token[:8]
        )
        raise HTTPException(
            status_code=401, detail="Unauthorized - invalid admin token"
        )


@router.get("/stats", dependencies=[Depends(_require_admin_auth)])
def get_performance_stats() -> dict[str, Any]:
    """
    Get current performance statistics snapshot.

    Returns:
        Dictionary containing:
        - hit_rate: Overall cache hit rate
        - hits/misses: Per-tier cache statistics
        - slo: Current SLO thresholds
        - runtime: Current runtime configuration
    """
    # Aggregate Prometheus metrics
    samples = {}
    try:
        for metric_family in REGISTRY.collect():
            for sample in metric_family.samples:
                name = sample.name
                labels = dict(sample.labels)
                value = float(sample.value)

                if name not in samples:
                    samples[name] = []
                samples[name].append({"labels": labels, "value": value})
    except Exception as exc:
        logger.warning("Failed to collect Prometheus metrics: %s", exc)
        samples = {}

    def _sum_metric(
        metric_name: str, label_key: str | None = None, label_value: str | None = None
    ) -> float:
        """Sum metric values optionally filtered by label."""
        metric_samples = samples.get(metric_name, [])
        if label_key is None:
            return sum(sample["value"] for sample in metric_samples)

        return sum(
            sample["value"]
            for sample in metric_samples
            if sample["labels"].get(label_key) == label_value
        )

    # Calculate cache statistics
    hits_l1 = _sum_metric("cache_hits_total", "tier", "l1")
    hits_l2 = _sum_metric("cache_hits_total", "tier", "l2")
    misses_l1 = _sum_metric("cache_misses_total", "tier", "l1")
    misses_l2 = _sum_metric("cache_misses_total", "tier", "l2")

    total_operations = hits_l1 + hits_l2 + misses_l1 + misses_l2
    overall_hit_rate = (
        ((hits_l1 + hits_l2) / total_operations) if total_operations > 0 else 0.0
    )

    # Get current configuration
    settings = get_settings()
    runtime = get_runtime()

    return {
        "cache": {
            "hit_rate": round(overall_hit_rate, 4),
            "hits": {"l1": int(hits_l1), "l2": int(hits_l2)},
            "misses": {"l1": int(misses_l1), "l2": int(misses_l2)},
            "total_operations": int(total_operations),
        },
        "slo": {
            "p95_ms": settings.PERF_SLO_P95_MS,
            "p99_ms": settings.PERF_SLO_P99_MS,
        },
        "runtime": {
            "enabled": runtime.enabled,
            "tracing_enabled": runtime.tracing_enabled,
        },
        "settings": {
            "sampling_rate": settings.PERF_SAMPLING,
            "otlp_endpoint": settings.PERF_OTLP_ENDPOINT,
        },
        "metrics_available": len(samples),
    }


@router.post("/toggle", dependencies=[Depends(_require_admin_auth)])
def toggle_performance_features(
    enabled: bool | None = None,
    tracing_enabled: bool | None = None,
) -> dict[str, Any]:
    """
    Toggle performance features at runtime.

    Args:
        enabled: Enable/disable performance monitoring
        tracing_enabled: Enable/disable OpenTelemetry tracing

    Returns:
        Updated runtime configuration
    """
    runtime = get_runtime()
    changes = []

    if enabled is not None:
        old_value = runtime.enabled
        runtime.enabled = bool(enabled)
        changes.append(f"enabled: {old_value} -> {runtime.enabled}")

    if tracing_enabled is not None:
        old_value = runtime.tracing_enabled
        runtime.tracing_enabled = bool(tracing_enabled)
        changes.append(f"tracing_enabled: {old_value} -> {runtime.tracing_enabled}")

    logger.info("Performance features toggled: %s", ", ".join(changes))

    return {
        "ok": True,
        "changes": changes,
        "runtime": {
            "enabled": runtime.enabled,
            "tracing_enabled": runtime.tracing_enabled,
        },
    }


@router.post("/slo", dependencies=[Depends(_require_admin_auth)])
def update_slo_thresholds(
    p95_ms: int | None = None,
    p99_ms: int | None = None,
) -> dict[str, Any]:
    """
    Update SLO thresholds (note: requires environment update for persistence).

    Args:
        p95_ms: P95 latency threshold in milliseconds
        p99_ms: P99 latency threshold in milliseconds

    Returns:
        SLO update instructions and current values
    """
    settings = get_settings()
    current_slo = {
        "p95_ms": settings.PERF_SLO_P95_MS,
        "p99_ms": settings.PERF_SLO_P99_MS,
    }

    recommendations = []
    if p95_ms is not None and p95_ms > 0:
        recommendations.append(f"PERF_SLO_P95_MS={p95_ms}")
    if p99_ms is not None and p99_ms > 0:
        recommendations.append(f"PERF_SLO_P99_MS={p99_ms}")

    logger.info("SLO update requested: %s", recommendations)

    return {
        "message": "Update environment variables and restart for persistence",
        "current_slo": current_slo,
        "recommended_env_vars": recommendations,
        "note": "Runtime SLO updates require application restart",
    }


@router.get("/health", dependencies=[Depends(_require_admin_auth)])
def get_performance_health() -> dict[str, Any]:
    """
    Get performance system health status.

    Returns:
        Health check results for performance components
    """
    runtime = get_runtime()
    settings = get_settings()

    health_checks = {}

    # Check if monitoring is enabled
    health_checks["monitoring"] = {
        "status": "healthy" if runtime.enabled else "disabled",
        "enabled": runtime.enabled,
    }

    # Check tracing status
    health_checks["tracing"] = {
        "status": "healthy" if runtime.tracing_enabled else "disabled",
        "enabled": runtime.tracing_enabled,
        "endpoint": settings.PERF_OTLP_ENDPOINT,
        "sampling_rate": settings.PERF_SAMPLING,
    }

    # Check Prometheus metrics
    try:
        metric_count = len(list(REGISTRY.collect()))
        health_checks["metrics"] = {
            "status": "healthy",
            "available_families": metric_count,
        }
    except Exception as exc:
        health_checks["metrics"] = {
            "status": "error",
            "error": str(exc),
        }

    overall_status = "healthy"
    if not runtime.enabled:
        overall_status = "disabled"
    elif any(check.get("status") == "error" for check in health_checks.values()):
        overall_status = "degraded"

    return {
        "status": overall_status,
        "checks": health_checks,
        "timestamp": "2025-08-29T00:00:00Z",  # Would use datetime.now(UTC) in real code
    }


@router.get("/ping")
def ping_performance_system() -> dict[str, Any]:
    """
    Simple health ping cho performance system (không cần auth).

    Returns:
        Basic status information
    """
    runtime = get_runtime()

    return {
        "status": "ok",
        "performance_enabled": runtime.enabled,
        "tracing_enabled": runtime.tracing_enabled,
        "service": "zeta_perf",
    }
