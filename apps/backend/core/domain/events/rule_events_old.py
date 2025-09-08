"""Rule Engine Domain Events.

This module defines domain events for rule engine operations such as rule evaluation
and execution failures. These events follow DDD principles and are immutable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from apps.backend.core.observability.logging import get_logger

from .base import DomainEvent, EventMeta, register_event
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
import staticmethod
import str
import type

logger = get_logger(__name__)


@register_event("RuleEvaluated")
@dataclass(frozen=True)
class RuleEvaluatedPayload:
    """Payload for rule evaluated event."""

    rule_id: UUID
    input_data: dict[str, Any]
    result: bool
    execution_time_ms: float
    context: dict[str, Any]


@register_event("RuleExecutionFailed")
@dataclass(frozen=True)
class RuleExecutionFailedPayload:
    """Payload for rule execution failed event."""

    rule_id: UUID
    input_data: dict[str, Any]
    error_message: str
    error_type: str
    context: dict[str, Any]


class RuleEvaluated:
    """Factory for rule evaluated events."""

    @staticmethod
    def create(
        rule_id: UUID,
        input_data: dict[str, Any],
        result: bool,
        execution_time_ms: float,
        context: dict[str, Any] | None = None,
    ) -> DomainEvent[RuleEvaluatedPayload]:
        """Create rule evaluated event.

        Args:
            rule_id: Unique identifier for the rule.
            input_data: Input data used for evaluation.
            result: Result of the evaluation.
            execution_time_ms: Execution time in milliseconds.
            context: Additional context data.

        Returns:
            RuleEvaluated domain event.
        """
        payload = RuleEvaluatedPayload(
            rule_id=rule_id,
            input_data=input_data,
            result=result,
            execution_time_ms=execution_time_ms,
            context=context or {},
        )
        return DomainEvent(
            type="RuleEvaluated",
            meta=EventMeta(),
            data=payload,
        )


class RuleExecutionFailed:
    """Factory for rule execution failed events."""

    @staticmethod
    def create(
        rule_id: UUID,
        input_data: dict[str, Any],
        error: Exception,
        context: dict[str, Any] | None = None,
    ) -> DomainEvent[RuleExecutionFailedPayload]:
        """Create rule execution failed event.

        Args:
            rule_id: Unique identifier for the rule.
            input_data: Input data used for execution.
            error: Exception that occurred.
            context: Additional context data.

        Returns:
            RuleExecutionFailed domain event.
        """
        payload = RuleExecutionFailedPayload(
            rule_id=rule_id,
            input_data=input_data,
            error_message=str(error),
            error_type=type(error).__name__,
            context=context or {},
        )
        return DomainEvent(
            type="RuleExecutionFailed",
            meta=EventMeta(),
            data=payload,
        )


__all__ = [
    "RuleEvaluated",
    "RuleEvaluatedPayload",
    "RuleExecutionFailed",
    "RuleExecutionFailedPayload",
]
