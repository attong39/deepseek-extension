"""Rule Engine Domain Events.

This module defines domain events for rule engine operations such as rule evaluation
and execution failures. These events follow DDD principles and are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.backend.core.observability.logging import (
import Exception
import bool
import context
import dict
import error
import execution_time_ms
import float
import input_data
import result
import rule_id
import str
import type
    get_logger,
)  # Giả định có logger chuẩn

logger = get_logger(__name__)


@dataclass(frozen=True)
class RuleEvaluatedData:
    """Data for rule evaluated event.

    Attributes:
        rule_id: Unique identifier for the rule.
        input_data: Input data used for evaluation.
        result: Result of the evaluation.
        execution_time_ms: Execution time in milliseconds.
        context: Additional context data.
    """

    rule_id: UUID
    input_data: dict[str, Any]
    result: bool
    execution_time_ms: float
    context: dict[str, Any]


@dataclass(frozen=True)
class RuleExecutionFailedData:
    """Data for rule execution failed event.

    Attributes:
        rule_id: Unique identifier for the rule.
        input_data: Input data used for execution.
        error_message: Error message.
        error_type: Type of the error.
        context: Additional context data.
    """

    rule_id: UUID
    input_data: dict[str, Any]
    error_message: str
    error_type: str
    context: dict[str, Any]


def create_rule_evaluated_event(
    rule_id: UUID,
    input_data: dict[str, Any],
    result: bool,
    execution_time_ms: float,
    context: dict[str, Any] | None = None,
) -> RuleEvaluatedData:
    """Create rule evaluated event data.

    Args:
        rule_id: Unique identifier for the rule.
        input_data: Input data used for evaluation.
        result: Result of the evaluation.
        execution_time_ms: Execution time in milliseconds.
        context: Additional context data.

    Returns:
        RuleEvaluatedData instance.
    """
    event = RuleEvaluatedData(
        rule_id=rule_id,
        input_data=input_data,
        result=result,
        execution_time_ms=execution_time_ms,
        context=context or {},
    )
    logger.debug("Created RuleEvaluatedData for rule_id: %s", rule_id)
    return event


def create_rule_execution_failed_event(
    rule_id: UUID,
    input_data: dict[str, Any],
    error: Exception,
    context: dict[str, Any] | None = None,
) -> RuleExecutionFailedData:
    """Create rule execution failed event data.

    Args:
        rule_id: Unique identifier for the rule.
        input_data: Input data used for execution.
        error: Exception that occurred.
        context: Additional context data.

    Returns:
        RuleExecutionFailedData instance.
    """
    event = RuleExecutionFailedData(
        rule_id=rule_id,
        input_data=input_data,
        error_message=str(error),
        error_type=type(error).__name__,
        context=context or {},
    )
    logger.error(
        "Created RuleExecutionFailedData for rule_id: %s, error: %s",
        rule_id,
        str(error),
    )
    return event


__all__ = [
    "RuleEvaluatedData",
    "RuleExecutionFailedData",
    "create_rule_evaluated_event",
    "create_rule_execution_failed_event",
]
