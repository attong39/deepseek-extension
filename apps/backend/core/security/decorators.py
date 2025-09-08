"""Security decorators cho training workflows và background tasks.

Provides decorators để enforce permissions trong Celery workers,
training pipelines, và các background services.
"""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from apps.backend.core.security.context import Environment, Resource, Subject
from apps.backend.core.security.permission_manager import permission_manager
import Exception
import action
import action_name
import any
import args
import bool
import call_history
import call_time
import capture_args
import capture_result
import dict
import e
import float
import int
import isinstance
import key
import kwargs
import len
import list
import max_calls
import per_user
import resource_id
import resource_type
import result
import safe_result
import sensitive
import sensitivity
import service_role
import str
import tenant_id
import time_window
import tuple
import type
import value

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class SecurityDecoratorError(Exception):
    """Exception khi security decorator fails."""


def requires_permission(
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    tenant_id: str | None = None,
    sensitivity: str = "internal",
) -> Callable[[F], F]:
    """Decorator để require permission cho function.

    Args:
        action: Permission action (e.g., "training:start")
        resource_type: Type of resource (e.g., "training_job")
        resource_id: Specific resource ID (default: "*")
        tenant_id: Tenant ID (default: từ subject)
        sensitivity: Data sensitivity level

    Usage:
        @requires_permission("training:start", "training_job")
        def start_training(subject: Subject, ...):
            pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract subject from arguments
            subject = _extract_subject_from_args(*args, **kwargs)
            if subject is None:
                raise SecurityDecoratorError(
                    f"Function {func.__name__} requires Subject as first argument or 'subject' kwarg"
                )

            # Create resource
            resource = Resource(
                type=resource_type,
                id=resource_id or "*",
                tenant_id=tenant_id or subject.tenant_id,
                sensitivity=sensitivity,
            )

            # Create environment (default for worker)
            environment = Environment(
                ip="127.0.0.1",
                user_agent="worker",
                timestamp=None,
                device_trust="high",  # Workers are trusted
            )

            # Check permission
            try:
                permission_manager.ensure(subject, action, resource, environment)
            except Exception as e:
                logger.error(f"Permission denied for {func.__name__}: {e}")
                raise SecurityDecoratorError(f"Permission denied: {e}")

            # Call original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def requires_service_account(service_role: str) -> Callable[[F], F]:
    """Decorator để require service account với specific role.

    Args:
        service_role: Required service role (e.g., "svc_trainer")

    Usage:
        @requires_service_account("svc_trainer")
        def automated_training(subject: Subject, ...):
            pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            subject = _extract_subject_from_args(*args, **kwargs)
            if subject is None:
                raise SecurityDecoratorError(
                    f"Function {func.__name__} requires Subject as first argument"
                )

            # Check if subject has service role
            if service_role not in subject.roles:
                raise SecurityDecoratorError(
                    f"Function {func.__name__} requires service role '{service_role}', "
                    f"got roles: {subject.roles}"
                )

            # Validate service account format
            if not subject.user_id.startswith("svc:"):
                raise SecurityDecoratorError(
                    f"Service account user_id must start with 'svc:', got: {subject.user_id}"
                )

            logger.info(f"Service account {subject.user_id} executing {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def audit_action(
    action_name: str,
    resource_type: str,
    capture_args: bool = False,
    capture_result: bool = False,
) -> Callable[[F], F]:
    """Decorator để audit function calls.

    Args:
        action_name: Name of action for audit log
        resource_type: Type of resource being acted upon
        capture_args: Whether to capture function arguments
        capture_result: Whether to capture function result

    Usage:
        @audit_action("model_training_started", "training_job", capture_args=True)
        def start_training(subject: Subject, model_id: str, ...):
            pass
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args, **kwargs):
            subject = _extract_subject_from_args(*args, **kwargs)

            # Prepare audit data
            audit_data = {
                "action": action_name,
                "function": func.__name__,
                "resource_type": resource_type,
                "user_id": subject.user_id if subject else "unknown",
                "tenant_id": subject.tenant_id if subject else "unknown",
            }

            if capture_args:
                # Capture non-sensitive args
                safe_args = _sanitize_args_for_audit(args, kwargs)
                audit_data["arguments"] = safe_args

            try:
                # Execute function
                _ = func(*args, **kwargs)

                # Capture result if requested
                if capture_result:
                    audit_data["result"] = _sanitize_result_for_audit(result)

                audit_data["status"] = "success"
                logger.info(f"Audit: {audit_data}")

                return result

            except Exception as e:
                audit_data["status"] = "error"
                audit_data["error"] = str(e)
                logger.error(f"Audit: {audit_data}")
                raise

        return wrapper

    return decorator


def rate_limit(
    max_calls: int,
    time_window: int = 3600,  # 1 hour default
    per_user: bool = True,
) -> Callable[[F], F]:
    """Decorator để rate limit function calls.

    Args:
        max_calls: Maximum calls allowed
        time_window: Time window in seconds
        per_user: Whether to apply limit per user or globally

    Usage:
        @rate_limit(max_calls=10, time_window=300)  # 10 calls per 5 minutes
        def expensive_operation(subject: Subject, ...):
            pass
    """

    def decorator(func: F) -> F:
        call_history: dict[str, list] = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            import time  # noqa: PLC0415

            subject = _extract_subject_from_args(*args, **kwargs)

            # Determine rate limit key
            if per_user and subject:
                rate_key = f"{subject.user_id}:{func.__name__}"
            else:
                rate_key = func.__name__

            current_time = time.time()

            # Initialize or clean old entries
            if rate_key not in call_history:
                call_history[rate_key] = []
            else:
                # Remove calls outside time window
                call_history[rate_key] = [
                    call_time
                    for call_time in call_history[rate_key]
                    if current_time - call_time < time_window
                ]

            # Check rate limit
            if len(call_history[rate_key]) >= max_calls:
                raise SecurityDecoratorError(
                    f"Rate limit exceeded: {max_calls} calls per {time_window}s for {rate_key}"
                )

            # Record this call
            call_history[rate_key].append(current_time)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def _extract_subject_from_args(*args, **kwargs) -> Subject | None:
    """Extract Subject from function arguments."""
    # Try first positional argument
    if args and isinstance(args[0], Subject):
        return args[0]

    # Try 'subject' keyword argument
    if "subject" in kwargs and isinstance(kwargs["subject"], Subject):
        return kwargs["subject"]

    # Try 'user' keyword argument (alternative name)
    if "user" in kwargs and isinstance(kwargs["user"], Subject):
        return kwargs["user"]

    return None


def _sanitize_args_for_audit(args: tuple, kwargs: dict) -> dict[str, Any]:
    """Sanitize arguments for audit logging (remove sensitive data)."""
    sensitive_keys = {"password", "secret", "token", "key", "credential"}

    safe_kwargs = {}
    for key, value in kwargs.items():
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            safe_kwargs[key] = "[REDACTED]"
        elif isinstance(value, str | int | float | bool | list):
            safe_kwargs[key] = value
        else:
            safe_kwargs[key] = str(type(value))

    return {"args_count": len(args), "kwargs": safe_kwargs}


def _sanitize_result_for_audit(result: Any) -> Any:
    """Sanitize function result for audit logging."""
    if isinstance(result, str | int | float | bool):
        return result
    elif isinstance(result, list | tuple) and len(result) < 10:
        return result
    elif isinstance(result, dict) and len(result) < 10:
        # Remove sensitive keys
        sensitive_keys = {"password", "secret", "token", "key", "credential"}
        for key, value in result.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                safe_result[key] = "[REDACTED]"
            else:
                safe_result[key] = value
        return safe_result
    else:
        return f"<{type(result).__name__}>"


# Convenience decorators for common use cases
def requires_trainer_permission(action: str) -> Callable[[F], F]:
    """Shortcut for trainer-related permissions."""
    return requires_permission(action, "training_job")


def requires_dataset_permission(action: str) -> Callable[[F], F]:
    """Shortcut for dataset-related permissions."""
    return requires_permission(action, "dataset")


def requires_model_permission(action: str) -> Callable[[F], F]:
    """Shortcut for model-related permissions."""
    return requires_permission(action, "model")


# Combined decorators for common patterns
def secure_training_operation(action: str) -> Callable[[F], F]:
    """Combined decorator for secure training operations."""

    def decorator(func: F) -> F:
        # Apply multiple decorators
        func = requires_trainer_permission(action)(func)
        func = audit_action(f"training_{action}", "training_job", capture_args=True)(
            func
        )
        func = rate_limit(max_calls=50, time_window=3600)(func)  # 50 per hour
        return func

    return decorator


def secure_dataset_operation(action: str) -> Callable[[F], F]:
    """Combined decorator for secure dataset operations."""

    def decorator(func: F) -> F:
        func = requires_dataset_permission(action)(func)
        func = audit_action(f"dataset_{action}", "dataset", capture_args=True)(func)
        func = rate_limit(max_calls=20, time_window=3600)(func)  # 20 per hour
        return func

    return decorator
