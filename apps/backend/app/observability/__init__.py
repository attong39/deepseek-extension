"""
zeta_vn.app.observability package.

This module provides observability utilities for the Zeta application, including metrics collection,
tracing, logging configuration, and performance monitoring. It integrates with OpenTelemetry (OTEL)
for tracing and supports Prometheus for metrics exposure, with async operations where applicable.

Auto-fixed by comprehensive_init_fixer.py

Agent Orchestration Metrics:
- Agent step execution counters
- Team workflow latency histograms  
- Knowledge graph entity/relation metrics
- WebSocket connection tracking

Typical usage example:
    from app.observability import setup_tracing, MetricsCollector

    # Setup tracing
    setup_tracing()

    # Use metrics collector
    collector = MetricsCollector()
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

# Import logger from project's standard logging module (assuming zeta_vn.app.logger exists)
from app.logger import get_logger

from .custom_metrics import custom_metrics
from .logging import logging

# Import submodules and expose their contents
from .metrics import (
import Exception
import RuntimeError
import ValueError
import bool
import config
import dict
import e
import enable_metrics
import enable_tracing
import hasattr
import isinstance
import key
import str
    BYTES,
    COUNT,
    COUNTER,
    GAUGE,
    HISTOGRAM,
    KILOBYTES,
    MEGABYTES,
    MILLISECONDS,
    PERCENT,
    RATE,
    REGISTRY,
    REQUESTS_PER_SECOND,
    SECONDS,
    TIMER,
    C,
    Counter,
    G,
    Gauge,
    H,
    Histogram,
    MetricsCollector,
    MetricType,
    MetricUnit,
    TimerContext,
    active_agents_count,
    actual_window,
    agent_execution_seconds,
    api_request_duration_seconds,
    app_info,
    cache,
    cache_hit_percentage,
    clean_name,
    count,
    cpu_percent,
    current_time,
    cutoff_time,
    database_connections,
    dec,
    decorator,
    disk,
    duration,
    existing,
    export_metrics,
    family_data,
    filtered_history,
    fl_clients_participated_total,
    fl_dp_epsilon_current,
    fl_round_duration_seconds,
    fl_updates_rejected_total,
    flag,
    fmt,
    full_name,
    get_all_metrics,
    get_counter,
    get_custom_metrics,
    get_gauge,
    get_histogram_stats,
    get_metric_history,
    get_metrics_dict,
    get_metrics_response,
    get_rate_stats,
    get_registry,
    get_timer_stats,
    handler,
    health_metrics,
    histogram,
    history,
    http_request_duration_seconds,
    http_requests_in_progress,
    http_requests_total,
    inc,
    increment_counter,
    labels,
    lines,
    llm_tokens_consumed_total,
    mapping,
    mapping2,
    memory,
    metrics,
    metrics_collector,
    metrics_data,
    metrics_endpoint,
    net_io,
    observe,
    provider,
    rag_retrieval_seconds,
    rate_data,
    recent_data,
    record_histogram,
    record_rate,
    record_timing,
    register_custom_collector,
    register_metric,
    resource,
    result,
    sample_data,
    set,
    set_gauge,
    snapshot,
    sorted_timings,
    sorted_values,
    stats,
    tag_string,
    time_operation,
    timings,
    timings_ms,
    total_events,
    values,
    window_start,
    wrapper,
)
from .metrics_collector import metrics_collector
from .metrics_registry import metrics_registry
from .shared_metrics import shared_metrics
from .tracing import (
    OTEL_AVAILABLE,
    TracingConfig,
    configure_logging,
    core,
    create_span,
    get_tracer,
    instrument_fastapi,
    instrument_requests,
    instrument_sqlalchemy,
    jaeger_exporter,
    logger,
    setup_tracing,
    span_processor,
    trace_span,
    tracing,
    tracing_config,
)

# Get logger instance for this module
logger = get_logger(__name__)

__all__ = [
    "BYTES",
    "C",
    "COUNT",
    "COUNTER",
    "Counter",
    "G",
    "GAUGE",
    "Gauge",
    "H",
    "HISTOGRAM",
    "Histogram",
    "KILOBYTES",
    "MEGABYTES",
    "MILLISECONDS",
    "MetricType",
    "MetricUnit",
    "MetricsCollector",
    "OTEL_AVAILABLE",
    "PERCENT",
    "RATE",
    "REGISTRY",
    "REQUESTS_PER_SECOND",
    "SECONDS",
    "TIMER",
    "TimerContext",
    "TracingConfig",
    "active_agents_count",
    "actual_window",
    "agent_execution_seconds",
    "api_request_duration_seconds",
    "app_info",
    "cache",
    "cache_hit_percentage",
    "clean_name",
    "configure_logging",
    "core",
    "count",
    "cpu_percent",
    "create_span",
    "current_time",
    "cutoff_time",
    "database_connections",
    "dec",
    "decorator",
    "disk",
    "duration",
    "existing",
    "export_metrics",
    "family_data",
    "filtered_history",
    "fl_clients_participated_total",
    "fl_dp_epsilon_current",
    "fl_round_duration_seconds",
    "fl_updates_rejected_total",
    "flag",
    "fmt",
    "full_name",
    "get_all_metrics",
    "get_counter",
    "get_custom_metrics",
    "get_gauge",
    "get_histogram_stats",
    "get_metric_history",
    "get_metrics_dict",
    "get_metrics_response",
    "get_rate_stats",
    "get_registry",
    "get_timer_stats",
    "get_tracer",
    "handler",
    "health_metrics",
    "histogram",
    "history",
    "http_request_duration_seconds",
    "http_requests_in_progress",
    "http_requests_total",
    "inc",
    "increment_counter",
    "instrument_fastapi",
    "instrument_requests",
    "instrument_sqlalchemy",
    "jaeger_exporter",
    "labels",
    "lines",
    "llm_tokens_consumed_total",
    "logger",
    "mapping",
    "mapping2",
    "memory",
    "metrics",
    "metrics_collector",
    "metrics_data",
    "metrics_endpoint",
    "net_io",
    "observe",
    "provider",
    "rag_retrieval_seconds",
    "rate_data",
    "recent_data",
    "record_histogram",
    "record_rate",
    "record_timing",
    "register_custom_collector",
    "register_metric",
    "resource",
    "result",
    "sample_data",
    "set",
    "set_gauge",
    "setup_tracing",
    "snapshot",
    "sorted_timings",
    "sorted_values",
    "span_processor",
    "stats",
    "tag_string",
    "time_operation",
    "timings",
    "timings_ms",
    "total_events",
    "trace_span",
    "tracing_config",
    "values",
    "window_start",
    "wrapper",
    # AUTO-GEN items
    "custom_metrics",
    "logging",
    "metrics",
    "metrics_collector",
    "metrics_registry",
    "shared_metrics",
    "tracing",
]


def initialize_observability(
    config: dict[str, Any] | None = None,
    enable_tracing: bool = True,
    enable_metrics: bool = True,
) -> None:
    """
    Initialize the observability system with optional configuration.

    This function sets up tracing, metrics collection, and logging configuration.
    It handles exceptions gracefully and validates input.

    Args:
        config (Optional[Dict[str, Any]]): Configuration dictionary for observability setup.
            Defaults to None, which uses default settings.
        enable_tracing (bool): Whether to enable tracing. Defaults to True.
        enable_metrics (bool): Whether to enable metrics collection. Defaults to True.

    Raises:
        ValueError: If config contains invalid keys or values.
        RuntimeError: If initialization fails due to system issues.

    Example:
        initialize_observability({"tracing_endpoint": "http://localhost:14268"}, enable_tracing=True)
    """
    try:
        # Validate config if provided
        if config is not None:
            if not isinstance(config, dict):
                raise ValueError("Config must be a dictionary.")
            # Add specific validations as needed, e.g., check for valid keys
            valid_keys = {"tracing_endpoint", "metrics_port", "log_level"}
            for key in config:
                if key not in valid_keys:
                    raise ValueError(f"Invalid config key: {key}")

        # Log initialization start
        logger.info("Initializing observability system.")

        # Setup tracing if enabled
        if enable_tracing and OTEL_AVAILABLE:
            setup_tracing(config=config)
            logger.info("Tracing setup completed.")
        elif enable_tracing and not OTEL_AVAILABLE:
            logger.warning("OpenTelemetry not available, skipping tracing setup.")

        # Setup metrics if enabled
        if enable_metrics:
            # Assuming MetricsCollector has an init method; adjust if needed
            if hasattr(MetricsCollector, 'init'):
                MetricsCollector.init(config=config)
            logger.info("Metrics collection initialized.")

        # Configure logging
        configure_logging(config=config)
        logger.info("Logging configured.")

        logger.info("Observability system initialized successfully.")

    except Exception as e:
        logger.error(f"Failed to initialize observability: {e}")
        raise RuntimeError("Observability initialization failed.") from e
