"""Metrics collection and Prometheus endpoint - Unified Observability."""

from typing import Any

from fastapi import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from prometheus_client.core import REGISTRY, CollectorRegistry


class MetricsCollector:
    """Centralized metrics collection for ZETA AI."""
import Exception
import dict
import e
import family
import len
import list
import registry
import sample
import self
import str

    def __init__(self, registry: CollectorRegistry = REGISTRY):
        """Initialize metrics collector with registry."""
        self.registry = registry

    def get_metrics_response(self) -> Response:
        """
        Generate Prometheus metrics response.

        Returns:
            Response: Prometheus metrics in text format
        """
        try:
            # Generate metrics in Prometheus format
            metrics_data = generate_latest(self.registry)

            return Response(
                content=metrics_data, media_type=CONTENT_TYPE_LATEST, status_code=200
            )

        except Exception as e:
            # Return error response if metrics collection fails
            return Response(
                content=f"Error collecting metrics: {e!s}",
                media_type="text/plain",
                status_code=503,
            )

    def get_metrics_dict(self) -> dict[str, Any]:
        """
        Get metrics as dictionary (for JSON responses).

        Returns:
            dict: Metrics data
        """
        try:
            # Collect all metric families
            metrics = {}

            for family in self.registry.collect():
                family_data = {
                    "name": family.name,
                    "documentation": family.documentation,
                    "type": family.type,
                    "samples": [],
                }

                for sample in family.samples:
                    sample_data = {
                        "name": sample.name,
                        "labels": sample.labels,
                        "value": sample.value,
                        "timestamp": sample.timestamp,
                    }
                    family_data["samples"].append(sample_data)

                metrics[family.name] = family_data

            return metrics

        except Exception as e:
            return {"error": f"Failed to collect metrics: {e!s}"}


# Global metrics collector instance
metrics_collector = MetricsCollector()


def metrics_endpoint() -> Response:
    """
    FastAPI endpoint for Prometheus metrics.

    Returns:
        Response: Prometheus metrics
    """
    return metrics_collector.get_metrics_response()


def health_metrics() -> dict[str, Any]:
    """
    Get health-related metrics.

    Returns:
        dict: Health metrics
    """
    try:
        # Basic health metrics
        metrics = {
            "status": "healthy",
            "metrics_collector": "operational",
            "registry_families": len(list(metrics_collector.registry.collect())),
        }

        return metrics

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
