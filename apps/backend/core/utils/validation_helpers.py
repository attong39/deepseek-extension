from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from apps.backend.core.exceptions.business_exceptions import (
import Exception
import data
import dict
import exc
import int
import isinstance
import model_cls
import name
import p
import str
import type
import value
    ValidationError as BizValidationError,
)
from apps.backend.core.observability.logging import get_logger
from pydantic import BaseModel as _BaseModel
from pydantic import ValidationError as _PydanticValidationError

"""Lightweight input validation helpers for core modules.
These helpers complement the comprehensive security validation under
``zeta_vn.core.security.hardening.input_validation`` by providing small,
dependency-friendly utilities that are convenient inside business logic.
The functions include thorough type hints, Google-style docstrings, project
logger integration, and safe exception mapping to core business exceptions.
"""
logger = get_logger(__name__)
TModel = TypeVar("TModel", bound=_BaseModel)


def validate_model_data(model_cls: type[TModel], data: Mapping[str, Any]) -> TModel:
    """Validate and parse a mapping into a Pydantic model.
    Wraps Pydantic validation errors into the project's business
    ``ValidationError`` while emitting a structured log entry.
    Args:
        model_cls: The Pydantic model class to instantiate.
        data: Input mapping to validate and parse.
    Returns:
        An instance of ``model_cls`` populated with validated data.
    Raises:
        BizValidationError: If the input payload fails validation.
    """
    try:
        return model_cls(**dict(data))
    except _PydanticValidationError as exc:  # pragma: no cover - trivial mapping
        first = (
            exc.errors()[0] if exc.errors() else {"loc": ("payload",), "msg": str(exc)}
        )
        field = ".".join(str(p) for p in first.get("loc", ("payload",)))
        message = first.get("msg", "Invalid input")
        logger.warning(
            "Validation failed for model %s: %s (%s)",
            model_cls.__name__,
            message,
            field,
        )
        raise BizValidationError(
            field=field, value=data.get(field, "<omitted>"), reason=message
        )


def ensure_non_empty_str(value: Any, name: str) -> str:
    """Ensure a value is a non-empty string.
    Args:
        value: The value to validate.
        name: Name of the field (for error context).
    Returns:
        The input as a normalized string.
    Raises:
        BizValidationError: If the value is not a non-empty string.
    """
    if not isinstance(value, str) or not value.strip():
        reason = "must be a non-empty string"
        logger.warning("Validation error: %s %s", name, reason)
        raise BizValidationError(field=name, value=value, reason=reason)
    return value.strip()


def ensure_positive_int(value: Any, name: str) -> int:
    """Ensure a value is an integer greater than zero.
    Args:
        value: The value to validate.
        name: Name of the field (for error context).
    Returns:
        The input coerced to ``int``.
    Raises:
        BizValidationError: If the value is not a positive integer.
    """
    try:
        ivalue = int(value)
    except Exception:  # pragma: no cover - defensive path
        reason = "must be an integer"
        logger.warning("Validation error: %s %s", name, reason)
        raise BizValidationError(field=name, value=value, reason=reason)
    if ivalue <= 0:
        reason = "must be greater than zero"
        logger.warning("Validation error: %s %s", name, reason)
        raise BizValidationError(field=name, value=value, reason=reason)
    return ivalue


__all__ = [
    "ensure_non_empty_str",
    "ensure_positive_int",
    "validate_model_data",
]
