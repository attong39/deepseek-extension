from __future__ import annotations

import logging
import sys

import structlog
from apps.backend.core.observability.logging import get_logger
import action
import allowed
import bool
import dict
import duration_ms
import error
import event_type
import float
import kwargs
import operation
import resource
import str
import success
import tenant_id
import token_hash
import user_id

"""Logging configuration với structlog cho audit và monitoring.
Module này cấu hình:
- Structured logging với structlog
- Audit logging cho security events
- Performance monitoring
"""


def configure_structlog():
    """Configure structlog cho structured logging."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


security_logger = get_logger("zeta.auth.security")


def log_auth_event(
    event_type: str,
    user_id: str = None,
    tenant_id: str = None,
    success: bool = True,
    **kwargs,
):
    """Log authentication/authorization event.
    Args:
        event_type: Type of event (login, logout, access_denied, etc.)
        user_id: User ID if available
        tenant_id: Tenant ID if available
        success: Whether the event was successful
        **kwargs: Additional context
    """
    event_data = {
        "event_type": event_type,
        "user_id": user_id or "anonymous",
        "tenant_id": tenant_id or "unknown",
        "success": success,
        "timestamp": kwargs.get(
            "timestamp", "2025-08-16T06:00:00Z"
        ),  # Use actual timestamp
        **kwargs,
    }
    if success:
        security_logger.info(f"Auth event: {event_type}", **event_data)
    else:
        security_logger.warning(f"Auth event failed: {event_type}", **event_data)


def log_jwt_event(
    event_type: str,
    token_hash: str = None,
    user_id: str = None,
    error: str = None,
    **kwargs,
):
    """Log JWT-related event.
    Args:
        event_type: Type of JWT event (decode, validate, expire, etc.)
        token_hash: Hash of token for tracking
        user_id: User ID from token
        error: Error message if any
        **kwargs: Additional context
    """
    event_data = {
        "event_type": f"jwt:{event_type}",
        "token_hash": token_hash,
        "user_id": user_id,
        "error": error,
        **kwargs,
    }
    if error:
        security_logger.warning(f"JWT event: {event_type}", **event_data)
    else:
        security_logger.info(f"JWT event: {event_type}", **event_data)


def log_permission_event(
    event_type: str, user_id: str, resource: str, action: str, allowed: bool, **kwargs
):
    """Log permission check event.
    Args:
        event_type: Type of permission event
        user_id: User ID
        resource: Resource being accessed
        action: Action being performed
        allowed: Whether access was allowed
        **kwargs: Additional context
    """
    event_data = {
        "event_type": f"permission:{event_type}",
        "user_id": user_id,
        "resource": resource,
        "action": action,
        "allowed": allowed,
        **kwargs,
    }
    if allowed:
        security_logger.info(
            f"Permission granted: {action} on {resource}", **event_data
        )
    else:
        security_logger.warning(
            f"Permission denied: {action} on {resource}", **event_data
        )


perf_logger = get_logger("zeta.auth.performance")


def log_performance_metric(
    operation: str, duration_ms: float, success: bool = True, **kwargs
):
    """Log performance metric.
    Args:
        operation: Operation name
        duration_ms: Duration in milliseconds
        success: Whether operation succeeded
        **kwargs: Additional context
    """
    event_data = {
        "operation": operation,
        "duration_ms": duration_ms,
        "success": success,
        **kwargs,
    }
    if success:
        perf_logger.info(f"Performance: {operation}", **event_data)
    else:
        perf_logger.warning(f"Performance failed: {operation}", **event_data)


configure_structlog()
__all__ = [
    "configure_structlog",
    "event_data",
    "log_auth_event",
    "log_jwt_event",
    "log_performance_metric",
    "log_permission_event",
    "perf_logger",
    "security_logger",
]
