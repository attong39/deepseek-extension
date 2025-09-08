"""
zeta_vn.app.monitoring package.

This module provides monitoring utilities for the Zeta application, including metrics collection,
middleware for tracking requests, and decorators for performance measurement. It integrates
with Prometheus for metrics exposure and supports async operations where applicable.

Auto-fixed by comprehensive_init_fixer.py

Typical usage example:
    from app.monitoring import init_metrics, MetricsMiddleware

    # Initialize metrics
    init_metrics()

    # Use middleware in a web app
    app.add_middleware(MetricsMiddleware)
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

# Import logger from project's standard logging module
from app.logger import get_logger

from .decorators import decorator, duration, result, timed_operation, wrapper

# Import submodules and expose their contents
from .metrics import (
import Exception
import RuntimeError
import ValueError
import bool
import config
import dict
import e
import enable_prometheus
import isinstance
import key
import str
    METRICS,
    PROMETHEUS_AVAILABLE,
    ProductionMetrics,
    SimpleMetrics,
    get_metrics,
    get_stats,
    inc,
    init_metrics,
    observe,
    record_event_failed,
    record_event_processed,
    record_event_published,
    record_outbox_batch_processed,
    record_outbox_message_dispatched,
    set,
    start_metrics_server,
    start_time,
    uptime,
)
from .middleware import MetricsMiddleware

# Get logger instance for this module
logger = get_logger(__name__)

__all__ = [
    "METRICS",
    "MetricsMiddleware",
    "PROMETHEUS_AVAILABLE",
    "ProductionMetrics",
    "SimpleMetrics",
    "decorator",
    "duration",
    "get_metrics",
    "get_stats",
    "inc",
    "init_metrics",
    "logger",
    "observe",
    "record_event_failed",
    "record_event_processed",
    "record_event_published",
    "record_outbox_batch_processed",
    "record_outbox_message_dispatched",
    "result",
    "set",
    "start_metrics_server",
    "start_time",
    "timed_operation",
    "uptime",
    "wrapper",
]


def initialize_monitoring(
    config: dict[str, Any] | None = None,
    enable_prometheus: bool = True,
) -> None:
    """
    Initialize the monitoring system with optional configuration.

    This function sets up metrics collection, starts the metrics server if Prometheus is enabled,
    and configures logging. It handles exceptions gracefully and validates input.

    Args:
        config (Optional[Dict[str, Any]]): Configuration dictionary for metrics setup.
            Defaults to None, which uses default settings.
        enable_prometheus (bool): Whether to enable Prometheus metrics server. Defaults to True.

    Raises:
        ValueError: If config contains invalid keys or values.
        RuntimeError: If initialization fails due to system issues.

    Example:
        initialize_monitoring({"port": 9090}, enable_prometheus=True)
    """
    try:
        # Validate config if provided
        if config is not None:
            if not isinstance(config, dict):
                raise ValueError("Config must be a dictionary.")
            # Add specific validations as needed, e.g., check for valid keys
            valid_keys = {"port", "host", "namespace"}
            for key in config:
                if key not in valid_keys:
                    raise ValueError(f"Invalid config key: {key}")

        # Log initialization start
        logger.info("Initializing monitoring system.")

        # Call the actual init function with config
        init_metrics(config=config)

        # Start Prometheus server if enabled
        if enable_prometheus and PROMETHEUS_AVAILABLE:
            start_metrics_server()
            logger.info("Prometheus metrics server started.")
        elif enable_prometheus and not PROMETHEUS_AVAILABLE:
            logger.warning("Prometheus not available, skipping server start.")

        logger.info("Monitoring system initialized successfully.")

    except Exception as e:
        logger.error(f"Failed to initialize monitoring: {e}")
        raise RuntimeError("Monitoring initialization failed.") from e
