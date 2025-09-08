"""Production metrics system với outbox monitoring."""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


try:
    from prometheus_client import Counter, Gauge, Histogram, start_http_server

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.warning("prometheus_client not available, using simple metrics")


class ProductionMetrics:
    """Production-ready metrics collector với Prometheus support."""
import Exception
import ImportError
import args
import batch_size
import bool
import dict
import duration_seconds
import e
import error_type
import event_type
import float
import func
import int
import kwargs
import labels
import len
import list
import max
import metric_name
import min
import name
import port
import production
import result
import self
import staticmethod
import str
import sum
import value

    def __init__(self) -> None:
        if not PROMETHEUS_AVAILABLE:
            raise ImportError("prometheus_client required for ProductionMetrics")

        # Domain event metrics
        self.events_published = Counter(
            "zeta_events_published_total",
            "Total domain events published",
            ["event_type", "aggregate"],
        )

        self.events_processed = Counter(
            "zeta_events_processed_total",
            "Total domain events processed by handlers",
            ["event_type", "handler", "status"],
        )

        # Outbox pattern metrics
        self.outbox_messages_added = Counter(
            "zeta_outbox_messages_added_total",
            "Total messages added to outbox",
            ["event_type", "partition_key"],
        )

        self.outbox_messages_claimed = Counter(
            "zeta_outbox_messages_claimed_total",
            "Total messages claimed from outbox",
            ["worker_id", "shard"],
        )

        self.outbox_messages_dispatched = Counter(
            "zeta_outbox_messages_dispatched_total",
            "Total messages successfully dispatched",
            ["event_type", "worker_id"],
        )

        self.outbox_messages_failed = Counter(
            "zeta_outbox_messages_failed_total",
            "Total messages that failed dispatch",
            ["event_type", "error_type"],
        )

        self.outbox_backlog = Gauge(
            "zeta_outbox_backlog",
            "Number of pending messages in outbox",
            ["partition_key"],
        )

        self.outbox_processing_time = Histogram(
            "zeta_outbox_processing_seconds",
            "Time taken to process outbox messages",
            ["worker_id"],
        )

        # Dead letter queue metrics
        self.dlq_messages_total = Counter(
            "zeta_dlq_messages_total",
            "Total messages moved to dead letter queue",
            ["event_type", "reason"],
        )

        # Memory processing metrics
        self.memory_chunks_processed = Counter(
            "zeta_memory_chunks_processed_total",
            "Total memory chunks processed",
            ["namespace", "tenant_id"],
        )

        self.memory_upserts = Counter(
            "zeta_memory_upserts_total",
            "Total memory upserts to vector store",
            ["tenant_id", "namespace"],
        )

        self.memory_processing_errors = Counter(
            "zeta_memory_processing_errors_total",
            "Total memory processing errors",
            ["error_type"],
        )

        # Agent metrics
        self.agents_created = Counter(
            "zeta_agents_created_total", "Total agents created", ["model"]
        )

        self.agents_activated = Counter(
            "zeta_agents_activated_total", "Total agents activated"
        )

        logger.info("Initialized production metrics system with Prometheus")

    def start_metrics_server(self, port: int = 8080) -> None:
        """Start Prometheus metrics HTTP server."""
        try:
            start_http_server(port)
            logger.info(f"Metrics server started on port {port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")

    def inc(self, name: str, value: int = 1, **labels) -> None:
        """Generic counter increment with labels."""
        # Map simple names to Prometheus metrics
        if name == "memory_upserts" and "tenant_id" in labels:
            self.memory_upserts.labels(
                tenant_id=labels.get("tenant_id", "default"),
                namespace=labels.get("namespace", "default"),
            ).inc(value)
        elif name == "agents_created":
            self.agents_created.labels(model=labels.get("model", "unknown")).inc(value)
        elif name == "agents_activated":
            self.agents_activated.inc(value)


class SimpleMetrics:
    """Simple metrics collector cho development."""

    def __init__(self) -> None:
        self.counters: defaultdict[str, int] = defaultdict(int)
        self.histograms: defaultdict[str, list[float]] = defaultdict(list)
        self.gauges: dict[str, float] = {}
        self._start_time = time.time()

    def inc(self, name: str, value: int = 1, **labels) -> None:
        """Increment counter."""
        self.counters[name] += value

    def observe(self, name: str, value: float) -> None:
        """Observe histogram value."""
        self.histograms[name].append(value)

    def set(self, name: str, value: float) -> None:
        """Set gauge value."""
        self.gauges[name] = value

    def get_stats(self) -> dict[str, Any]:
        """Get all metrics."""
        uptime = time.time() - self._start_time
        return {
            "uptime_seconds": uptime,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                name: {
                    "count": len(values),
                    "avg": sum(values) / len(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                }
                for name, values in self.histograms.items()
            },
        }

    def start_metrics_server(self, port: int = 8080) -> None:
        """No-op for simple metrics."""
        logger.info("Simple metrics - no HTTP server started")


# Global metrics instance - will be initialized in app startup
METRICS: ProductionMetrics | SimpleMetrics


def init_metrics(production: bool = False) -> ProductionMetrics | SimpleMetrics:
    """Initialize metrics system."""
    global METRICS

    if production and PROMETHEUS_AVAILABLE:
        METRICS = ProductionMetrics()
        logger.info("Initialized production metrics with Prometheus")
    else:
        METRICS = SimpleMetrics()
        logger.info("Initialized simple metrics for development")

    return METRICS


def get_metrics() -> ProductionMetrics | SimpleMetrics:
    """Get current metrics instance."""
    return METRICS


class MetricsMiddleware:
    """Metrics collection for event processing."""

    @staticmethod
    def record_event_published(event_type: str) -> None:
        """Record event publication."""
        METRICS.inc("events_published_total")
        METRICS.inc(f"events_published_{event_type}")

    @staticmethod
    def record_event_processed(event_type: str, duration_seconds: float) -> None:
        """Record event processing."""
        METRICS.inc("events_processed_total")
        METRICS.inc(f"events_processed_{event_type}")
        METRICS.observe("event_processing_duration_seconds", duration_seconds)

    @staticmethod
    def record_event_failed(event_type: str, error_type: str) -> None:
        """Record event processing failure."""
        METRICS.inc("events_failed_total")
        METRICS.inc(f"events_failed_{event_type}")
        METRICS.inc(f"events_failed_{error_type}")

    @staticmethod
    def record_outbox_batch_processed(batch_size: int, duration_seconds: float) -> None:
        """Record outbox batch processing."""
        METRICS.inc("outbox_batches_processed_total")
        METRICS.observe("outbox_batch_size", float(batch_size))
        METRICS.observe("outbox_batch_duration_seconds", duration_seconds)

    @staticmethod
    def record_outbox_message_dispatched(event_type: str) -> None:
        """Record outbox message dispatch."""
        METRICS.inc("outbox_messages_dispatched_total")
        METRICS.inc(f"outbox_messages_dispatched_{event_type}")


# Decorator for timing functions
def timed_operation(metric_name: str):
    """Decorator to time operations."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                _ = func(*args, **kwargs)
                duration = time.time() - start_time
                METRICS.observe(metric_name, duration)
                return result
            except Exception:
                duration = time.time() - start_time
                METRICS.observe(f"{metric_name}_error", duration)
                METRICS.inc(f"{metric_name}_errors_total")
                raise

        return wrapper

    return decorator


# Initialize with simple metrics by default
METRICS = SimpleMetrics()
