from __future__ import annotations

import logging
import traceback
from collections.abc import Callable
from contextlib import contextmanager
from functools import wraps
from typing import Any, TypeVar
import Exception
import action
import args
import bool
import callable
import code
import details
import dict
import e
import error
import exc
import field
import func
import func_name
import hasattr
import int
import kwargs
import max
import message
import operation
import resource
import resource_id
import resource_type
import self
import service_name
import str
import sum
import super
import type
import user_id
import value
import x

"""
Unified Error Handler for Core Layer
====================================
Provides consistent error handling across all core components.
"""
F = TypeVar("F", bound=Callable[..., Any])
logger = logging.getLogger(__name__)


class CoreException(Exception):
    """Base exception for all core layer errors."""

    def __init__(
        self,
        message: str,
        code: str = "CORE_ERROR",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = __import__("time").time()


class ValidationError(CoreException):
    """Validation error for domain/business rules."""

    def __init__(self, message: str, field: str | None = None, value: Any = None):
        super().__init__(message, "VALIDATION_ERROR", {"field": field, "value": value})


class NotFoundError(CoreException):
    """Resource not found error."""

    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            f"{resource_type} with id '{resource_id}' not found",
            "NOT_FOUND",
            {"resource_type": resource_type, "resource_id": resource_id},
        )


class PermissionDeniedError(CoreException):
    """Permission denied error."""

    def __init__(self, action: str, resource: str, user_id: str | None = None):
        super().__init__(
            f"Permission denied for action '{action}' on resource '{resource}'",
            "PERMISSION_DENIED",
            {"action": action, "resource": resource, "user_id": user_id},
        )


class CoreErrorHandler:
    """Unified error handling for core layer components."""

    def __init__(self, service_name: str = "core"):
        self.service_name = service_name
        self.error_counts: dict[str, int] = {}

    def handle_errors(self, func: F) -> F:
        """Decorator for consistent error handling."""

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await self._handle_async_execution(func, *args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return self._handle_sync_execution(func, *args, **kwargs)

        if self._is_async_function(func):
            return async_wrapper
        else:
            return sync_wrapper

    async def _handle_async_execution(self, func: F, *args, **kwargs) -> Any:
        """Handle async function execution with error handling."""
        try:
            result = await func(*args, **kwargs)
            return result
        except CoreException:
            raise
        except Exception as e:
            core_error = self._wrap_exception(e, func.__name__)
            self._log_error(core_error, func.__name__)
            raise core_error

    def _handle_sync_execution(self, func: F, *args, **kwargs) -> Any:
        """Handle sync function execution with error handling."""
        try:
            return func(*args, **kwargs)
        except CoreException:
            raise
        except Exception as e:
            core_error = self._wrap_exception(e, func.__name__)
            self._log_error(core_error, func.__name__)
            raise core_error

    def _wrap_exception(self, exc: Exception, func_name: str) -> CoreException:
        """Wrap a regular exception into a CoreException."""
        error_type = type(exc).__name__
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        return CoreException(
            f"Error in {func_name}: {str(exc)}",
            f"{error_type.upper()}_ERROR",
            {
                "original_error": error_type,
                "function": func_name,
                "traceback": traceback.format_exc(),
            },
        )

    def _log_error(self, error: CoreException, func_name: str):
        """Log error with appropriate level."""
        log_data = {
            "service": self.service_name,
            "function": func_name,
            "error_code": error.code,
            "error_message": str(error),
            "details": error.details,
        }
        if error.code in ["VALIDATION_ERROR", "NOT_FOUND"]:
            logger.warning("Core validation error", extra=log_data)
        else:
            logger.error("Core execution error", extra=log_data)

    def _is_async_function(self, func: Callable) -> bool:
        """Check if function is async."""
        return (
            callable(func)
            and hasattr(func, "__code__")
            and "async" in str(func.__code__.co_flags)
        )

    @contextmanager
    def error_context(self, operation: str):
        """Context manager for error handling."""
        try:
            yield
        except CoreException:
            raise
        except Exception as e:
            core_error = self._wrap_exception(e, operation)
            self._log_error(core_error, operation)
            raise core_error

    def get_error_stats(self) -> dict[str, Any]:
        """Get error statistics."""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_types": self.error_counts.copy(),
            "most_common_error": max(
                self.error_counts.items(), key=lambda x: x[1], default=(None, 0)
            ),
        }


error_handler = CoreErrorHandler("zeta_vn_core")


def handle_core_errors(func: F) -> F:
    """Convenience decorator for core error handling."""
    return error_handler.handle_errors(func)


def with_error_context(operation: str):
    """Convenience context manager for error handling."""
    return error_handler.error_context(operation)


def get_error_stats() -> dict[str, Any]:
    """Convenience function to get error statistics."""
    return error_handler.get_error_stats()


__all__ = [
    "CoreErrorHandler",
    "CoreException",
    "F",
    "NotFoundError",
    "PermissionDeniedError",
    "ValidationError",
    "core_error",
    "error_context",
    "error_handler",
    "error_type",
    "get_error_stats",
    "handle_core_errors",
    "handle_errors",
    "log_data",
    "logger",
    "result",
    "sync_wrapper",
    "with_error_context",
]
