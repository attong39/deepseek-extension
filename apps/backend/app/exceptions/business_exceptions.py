"""Business-level exceptions for the interface layer.

These exceptions represent boundary validations and business rule violations
detected at the API layer. For domain-specific errors, import from core.exceptions.
"""

from __future__ import annotations

# Re-export core business exceptions for backward compatibility
from apps.backend.core.exceptions import (
    BusinessException,
    BusinessLogicError,
    PermissionDeniedError,
    ValidationError,
)
from apps.backend.core.exceptions.business_exceptions import (
    EntityNotFoundError,
    ResourceLimitExceededError,
)

__all__ = [
    "BusinessException",
    "BusinessLogicError",
    "EntityNotFoundError",
    "PermissionDeniedError",
    "ResourceLimitExceededError",
    "ResourceQuotaExceededError",
    "ValidationError",
    # Backward-compat alias expected by some modules
    "BusinessRuleViolationError",
    "OperationNotAllowedError",
]


# Backward-compat: alias BusinessLogicError as BusinessRuleViolationError
BusinessRuleViolationError = BusinessLogicError

# Backward-compat: alias quota name to limit error
ResourceQuotaExceededError = ResourceLimitExceededError


class OperationNotAllowedError(BusinessLogicError):
    """Backward-compat exception for operation not allowed cases."""
