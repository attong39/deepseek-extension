"""Prometheus metrics cho Outbox pattern.

Định nghĩa các metrics để monitor performance, reliability và health
của Outbox event processing system.
"""

from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram
import active
import age_seconds
import attempt
import bool
import component
import dict
import dlq_sizes
import duration
import error_type
import event_type
import failure_reason
import float
import from_version
import handler
import healthy
import idle
import int
import operation
import partition
import partitions
import queue_sizes
import size
import str
import to_version
import waiting
import worker_index

# Event processing metrics
EVENT_PROCESSED = Counter(
    "outbox_event_processed_total",
    "Tổng số events đã process thành công",
    ["event_type", "handler"],
)

EVENT_FAILED = Counter(
    "outbox_event_failed_total",
    "Tổng số events process thất bại",
    ["event_type", "handler", "error_type"],
)

EVENT_RETRIED = Counter(
    "outbox_event_retried_total",
    "Tổng số events được retry",
    ["event_type", "handler", "attempt"],
)

DLQ_WRITTEN = Counter(
    "outbox_dlq_written_total",
    "Tổng số events gửi vào DLQ",
    ["event_type", "handler", "failure_reason"],
)

# Processing latency metrics
PROC_LATENCY = Histogram(
    "outbox_processing_seconds",
    "Thời gian process một event (seconds)",
    ["event_type", "handler"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Queue size metrics
QUEUE_GAUGE = Gauge(
    "outbox_queue_size", "Số lượng events đang chờ trong outbox queue", ["partition"]
)

DLQ_GAUGE = Gauge(
    "outbox_dlq_size",
    "Số lượng events trong Dead Letter Queue",
    ["partition", "event_type"],
)

# Worker metrics
WORKER_ACTIVE = Gauge(
    "outbox_worker_active", "Số lượng workers đang active", ["worker_index"]
)

LOCK_CONTENTION = Counter(
    "outbox_lock_contention_total", "Số lần worker không lấy được lock do contention"
)

BATCH_SIZE = Histogram(
    "outbox_batch_size",
    "Kích thước batch mỗi lần worker fetch events",
    buckets=[1, 5, 10, 25, 50, 100, 200, 500],
)

# Database metrics
DB_QUERY_DURATION = Histogram(
    "outbox_db_query_seconds",
    "Thời gian thực hiện DB queries",
    ["operation"],  # fetch, claim, mark_done, mark_retry, to_dlq
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)

DB_CONNECTION_POOL = Gauge(
    "outbox_db_connection_pool_size",
    "Số connections trong pool",
    ["pool_type"],  # active, idle, waiting
)

# Schema evolution metrics
UPCASTER_APPLIED = Counter(
    "outbox_upcaster_applied_total",
    "Số lần upcaster được áp dụng",
    ["event_type", "from_version", "to_version"],
)

UPCASTER_FAILED = Counter(
    "outbox_upcaster_failed_total",
    "Số lần upcaster thất bại",
    ["event_type", "from_version", "error_type"],
)

# Idempotency metrics
IDEMPOTENCY_HIT = Counter(
    "outbox_idempotency_hit_total",
    "Số lần skip do đã process (idempotency)",
    ["handler"],
)

IDEMPOTENCY_MISS = Counter(
    "outbox_idempotency_miss_total", "Số lần process mới (không duplicate)", ["handler"]
)

# System health metrics
OUTBOX_HEALTH = Gauge(
    "outbox_health_status",
    "Health status của Outbox system (1=healthy, 0=unhealthy)",
    ["component"],  # worker, database, queue, dlq
)

MEMORY_USAGE = Gauge(
    "outbox_memory_usage_bytes",
    "Memory usage của Outbox workers",
    ["worker_index", "type"],  # heap, rss, etc.
)

# Event age metrics
EVENT_AGE = Histogram(
    "outbox_event_age_seconds",
    "Tuổi của events (từ lúc tạo đến lúc process)",
    ["event_type"],
    buckets=[1, 5, 10, 30, 60, 300, 900, 1800, 3600, 7200, 14400],  # 1s to 4h
)

DLQ_EVENT_AGE = Histogram(
    "outbox_dlq_event_age_seconds",
    "Tuổi của events trong DLQ",
    ["event_type"],
    buckets=[3600, 7200, 14400, 43200, 86400, 259200, 604800],  # 1h to 1week
)


# Helper functions để record metrics


def record_event_processed(event_type: str, handler: str, duration: float) -> None:
    """Record event được process thành công."""
    EVENT_PROCESSED.labels(event_type=event_type, handler=handler).inc()
    PROC_LATENCY.labels(event_type=event_type, handler=handler).observe(duration)
    IDEMPOTENCY_MISS.labels(handler=handler).inc()


def record_event_failed(
    event_type: str, handler: str, error_type: str, duration: float
) -> None:
    """Record event process thất bại."""
    EVENT_FAILED.labels(
        event_type=event_type, handler=handler, error_type=error_type
    ).inc()
    PROC_LATENCY.labels(event_type=event_type, handler=handler).observe(duration)


def record_event_retried(event_type: str, handler: str, attempt: int) -> None:
    """Record event được retry."""
    EVENT_RETRIED.labels(
        event_type=event_type, handler=handler, attempt=str(attempt)
    ).inc()


def record_dlq_written(event_type: str, handler: str, failure_reason: str) -> None:
    """Record event được gửi vào DLQ."""
    DLQ_WRITTEN.labels(
        event_type=event_type, handler=handler, failure_reason=failure_reason
    ).inc()


def record_idempotency_hit(handler: str) -> None:
    """Record idempotency hit (skip duplicate)."""
    IDEMPOTENCY_HIT.labels(handler=handler).inc()


def record_upcaster_applied(
    event_type: str, from_version: str, to_version: str
) -> None:
    """Record upcaster được áp dụng."""
    UPCASTER_APPLIED.labels(
        event_type=event_type, from_version=from_version, to_version=to_version
    ).inc()


def record_upcaster_failed(event_type: str, from_version: str, error_type: str) -> None:
    """Record upcaster thất bại."""
    UPCASTER_FAILED.labels(
        event_type=event_type, from_version=from_version, error_type=error_type
    ).inc()


def update_queue_sizes(queue_sizes: dict[int, int]) -> None:
    """Update queue size gauges."""
    for partition, size in queue_sizes.items():
        QUEUE_GAUGE.labels(partition=str(partition)).set(size)


def update_dlq_sizes(dlq_sizes: dict[str, dict[int, int]]) -> None:
    """Update DLQ size gauges."""
    for event_type, partitions in dlq_sizes.items():
        for partition, size in partitions.items():
            DLQ_GAUGE.labels(partition=str(partition), event_type=event_type).set(size)


def set_worker_active(worker_index: int, active: bool) -> None:
    """Set worker active status."""
    WORKER_ACTIVE.labels(worker_index=str(worker_index)).set(1 if active else 0)


def record_db_query(operation: str, duration: float) -> None:
    """Record database query duration."""
    DB_QUERY_DURATION.labels(operation=operation).observe(duration)


def update_db_pool_stats(active: int, idle: int, waiting: int) -> None:
    """Update database connection pool stats."""
    DB_CONNECTION_POOL.labels(pool_type="active").set(active)
    DB_CONNECTION_POOL.labels(pool_type="idle").set(idle)
    DB_CONNECTION_POOL.labels(pool_type="waiting").set(waiting)


def set_health_status(component: str, healthy: bool) -> None:
    """Set health status cho component."""
    OUTBOX_HEALTH.labels(component=component).set(1 if healthy else 0)


def record_event_age(event_type: str, age_seconds: float) -> None:
    """Record tuổi của event khi được process."""
    EVENT_AGE.labels(event_type=event_type).observe(age_seconds)
