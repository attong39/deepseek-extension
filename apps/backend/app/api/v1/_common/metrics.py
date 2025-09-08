"""
Prometheus metrics endpoint cho ZETA_VN
Export tất cả metrics theo chuẩn Prometheus format
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.observability.metrics import get_metrics
from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse
import Exception
import ImportError
import data
import dict
import e
import len
import list
import name
import str
import value

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Metrics"])

# Prometheus client imports
try:
    from prometheus_client import (
        CONTENT_TYPE_LATEST,
        REGISTRY,  # noqa: PLC0415
        generate_latest,
    )

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("prometheus_client không khả dụng")


@router.get("/metrics")
async def prometheus_metrics() -> Response:
    """
    Prometheus metrics endpoint
    Export all metrics in Prometheus format for scraping
    """
    if not PROMETHEUS_AVAILABLE:
        # Fallback response khi Prometheus không available
        metrics = get_metrics()
        simple_metrics = metrics.get_simple_metrics()

        # Convert simple metrics to pseudo-Prometheus format
        output_lines = [
            "# TYPE zeta_service_info gauge",
            'zeta_service_info{version="1.0.0",environment="development"} 1',
            "",
            "# TYPE zeta_simple_counters_total counter",
        ]

        for name, value in simple_metrics.get("counters", {}).items():
            safe_name = name.replace(".", "_").replace("-", "_")
            output_lines.append(f"zeta_simple_{safe_name}_total {value}")

        output_lines.append("")
        output_lines.append("# TYPE zeta_simple_gauges gauge")

        for name, value in simple_metrics.get("gauges", {}).items():
            safe_name = name.replace(".", "_").replace("-", "_")
            output_lines.append(f"zeta_simple_{safe_name} {value}")

        output_lines.append("")
        output_lines.append("# TYPE zeta_simple_histogram_count counter")

        for name, data in simple_metrics.get("histograms", {}).items():
            safe_name = name.replace(".", "_").replace("-", "_")
            output_lines.append(f"zeta_simple_{safe_name}_count {data['count']}")
            output_lines.append(f"zeta_simple_{safe_name}_sum {data['sum']}")

        output = "\n".join(output_lines)
        return PlainTextResponse(content=output, media_type="text/plain")

    try:
        # Generate Prometheus metrics
        metrics_data = generate_latest(REGISTRY)

        return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)

    except Exception as e:
        logger.error(f"Lỗi generate Prometheus metrics: {e}")
        return PlainTextResponse(
            content=f"# Error generating metrics: {e}\n",
            media_type="text/plain",
            status_code=500,
        )


@router.get("/metrics/health")
async def metrics_health() -> dict[str, Any]:
    """
    Metrics system health check
    Trả về status của metrics collection
    """
    try:
        metrics = get_metrics()
        simple_metrics = metrics.get_simple_metrics()

        return {
            "status": "healthy",
            "prometheus_available": PROMETHEUS_AVAILABLE,
            "prometheus_enabled": metrics.use_prometheus,
            "otel_enabled": metrics.use_otel,
            "metrics_collected": {
                "counters": len(simple_metrics.get("counters", {})),
                "histograms": len(simple_metrics.get("histograms", {})),
                "gauges": len(simple_metrics.get("gauges", {})),
            },
        }

    except Exception as e:
        logger.error(f"Lỗi metrics health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "prometheus_available": PROMETHEUS_AVAILABLE,
        }


@router.get("/metrics/labels")
async def metrics_labels() -> dict[str, Any]:
    """
    Trả về thông tin về metric labels
    Hữu ích cho Grafana query builder
    """
    return {
        "http_labels": ["route", "method", "status"],
        "ai_labels": ["model", "provider", "direction"],
        "gpu_labels": ["node", "device"],
        "rag_labels": ["index", "k"],
        "training_labels": ["job_id", "state"],
        "dataset_labels": ["user_id_hash"],
        "memory_labels": ["process", "type"],
    }


@router.get("/metrics/names")
async def metrics_names() -> dict[str, list[str]]:
    """
    Trả về danh sách tất cả metric names
    Hữu ích cho documentation và monitoring setup
    """
    return {
        "http_metrics": [
            "zeta_http_requests_total",
            "zeta_http_request_duration_seconds",
        ],
        "ai_metrics": [
            "zeta_ai_inference_duration_seconds",
            "zeta_ai_inference_tokens_total",
            "zeta_ai_uncertainty_score",
            "zeta_ai_model_load_seconds",
            "zeta_ai_gpu_utilization_ratio",
            "zeta_ai_memory_usage_bytes",
        ],
        "rag_metrics": ["zeta_rag_retrieval_duration_seconds", "zeta_rag_recall_at_k"],
        "training_metrics": ["zeta_train_job_state"],
        "dataset_metrics": ["zeta_dataset_uploaded_bytes_total"],
        "service_metrics": ["zeta_service_info"],
    }
