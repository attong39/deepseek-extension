"""
Business Logic Exception Classes
Handles all domain-specific errors in ZETA AI Server
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from enum import Enum
from typing import Any
import Exception
import agent_id
import context
import current
import details
import dict
import entity
import error_code
import field
import identifier
import int
import job_id
import kwargs
import limit
import list
import message_id
import model_name
import operation
import plan_id
import reason
import resource
import rule
import self
import service
import session_id
import severity
import step
import str
import suggestions
import super
import value
import workflow_id

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BaseBusinessError(Exception):
    """Base business logic error class."""

    def __init__(
        self,
        message: str,
        error_code: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: dict[str, Any] | None = None,
        suggestions: list[str] | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.severity = severity
        self.context = context or {}
        self.suggestions = suggestions or []
        self.timestamp = datetime.now(UTC)

        # Log business errors with appropriate level
        log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL,
        }[severity]

        logger.log(
            log_level,
            "Business Error: %s - %s",
            error_code,
            message,
            extra={
                "error_code": error_code,
                "severity": severity.value,
                "context": self.context,
            },
        )

        super().__init__(message)


# Compatibility aliases
BusinessException = BaseBusinessError


class BusinessLogicError(BaseBusinessError):
    """Base class for business logic violations."""


# Agent-related exceptions
class AgentNotFoundError(BaseBusinessError):
    """Raised when an agent is not found."""

    def __init__(self, agent_id: str, **kwargs: Any) -> None:
        message = f"Agent not found: {agent_id}"
        super().__init__(message, "BIZ_001", **kwargs)
        self.agent_id = agent_id


class AgentCreationError(BaseBusinessError):
    """Raised when agent creation fails."""

    def __init__(self, reason: str, **kwargs: Any) -> None:
        message = f"Failed to create agent: {reason}"
        super().__init__(message, "BIZ_002", ErrorSeverity.HIGH, **kwargs)


class AgentDeploymentError(BaseBusinessError):
    """Raised when agent deployment fails."""

    def __init__(self, agent_id: str, reason: str, **kwargs: Any) -> None:
        message = f"Failed to deploy agent {agent_id}: {reason}"
        super().__init__(message, "BIZ_003", ErrorSeverity.HIGH, **kwargs)


# Chat-related exceptions
class ChatSessionError(BaseBusinessError):
    """Raised for chat session errors."""

    def __init__(self, session_id: str, reason: str, **kwargs: Any) -> None:
        message = f"Chat session error {session_id}: {reason}"
        super().__init__(message, "BIZ_004", **kwargs)


class MessageProcessingError(BaseBusinessError):
    """Raised when message processing fails."""

    def __init__(self, message_id: str, reason: str, **kwargs: Any) -> None:
        message = f"Failed to process message {message_id}: {reason}"
        super().__init__(message, "BIZ_005", **kwargs)


# Memory-related exceptions
class MemoryOperationError(BaseBusinessError):
    """Raised for memory operation failures."""

    def __init__(self, operation: str, reason: str, **kwargs: Any) -> None:
        message = f"Memory operation '{operation}' failed: {reason}"
        super().__init__(message, "BIZ_006", **kwargs)


class VectorEmbeddingError(BaseBusinessError):
    """Raised when vector embedding operations fail."""

    def __init__(self, reason: str, **kwargs: Any) -> None:
        message = f"Vector embedding error: {reason}"
        super().__init__(message, "BIZ_007", **kwargs)


# Planning-related exceptions
class PlanningError(BaseBusinessError):
    """Raised for planning operation failures."""

    def __init__(self, plan_id: str, reason: str, **kwargs: Any) -> None:
        message = f"Planning error for {plan_id}: {reason}"
        super().__init__(message, "BIZ_008", **kwargs)


class WorkflowExecutionError(BaseBusinessError):
    """Raised when workflow execution fails."""

    def __init__(self, workflow_id: str, step: str, reason: str, **kwargs: Any) -> None:
        message = f"Workflow {workflow_id} failed at step '{step}': {reason}"
        super().__init__(message, "BIZ_009", ErrorSeverity.HIGH, **kwargs)


# Training-related exceptions
class TrainingError(BaseBusinessError):
    """Raised for model training failures."""

    def __init__(self, job_id: str, reason: str, **kwargs: Any) -> None:
        message = f"Training job {job_id} failed: {reason}"
        super().__init__(message, "BIZ_010", ErrorSeverity.HIGH, **kwargs)


class ModelLoadError(BaseBusinessError):
    """Raised when model loading fails."""

    def __init__(self, model_name: str, reason: str, **kwargs: Any) -> None:
        message = f"Failed to load model '{model_name}': {reason}"
        super().__init__(message, "BIZ_011", ErrorSeverity.HIGH, **kwargs)


# Validation exceptions
class ValidationError(BaseBusinessError):
    """Raised for data validation failures."""

    def __init__(self, field: str, value: Any, reason: str, **kwargs: Any) -> None:
        message = (
            f"Validation failed for field '{field}' with value '{value}': {reason}"
        )
        super().__init__(message, "BIZ_012", **kwargs)


class BusinessRuleViolationError(BusinessLogicError):
    """Raised when business rules are violated."""

    def __init__(self, rule: str, details: str, **kwargs: Any) -> None:
        message = f"Business rule violation: {rule} - {details}"
        super().__init__(message, "BIZ_013", ErrorSeverity.HIGH, **kwargs)


# Resource-related exceptions
class ResourceLimitExceededError(BaseBusinessError):
    """Raised when resource limits are exceeded."""

    def __init__(self, resource: str, limit: int, current: int, **kwargs: Any) -> None:
        message = f"Resource limit exceeded for {resource}: {current}/{limit}"
        super().__init__(message, "BIZ_014", ErrorSeverity.HIGH, **kwargs)


class ExternalServiceError(BaseBusinessError):
    """Raised when external service calls fail."""

    def __init__(
        self, service: str, operation: str, reason: str, **kwargs: Any
    ) -> None:
        message = (
            f"External service '{service}' operation '{operation}' failed: {reason}"
        )
        super().__init__(message, "BIZ_015", **kwargs)


__all__ = [
    "ErrorSeverity",
    "BaseBusinessError",
    "BusinessException",
    "BusinessLogicError",
    # Common entity error used across services/tests
    "EntityNotFoundError",
    # Agent
    "AgentNotFoundError",
    "AgentCreationError",
    "AgentDeploymentError",
    # Chat
    "ChatSessionError",
    "MessageProcessingError",
    # Memory
    "MemoryOperationError",
    "VectorEmbeddingError",
    # Planning/Workflow
    "PlanningError",
    "WorkflowExecutionError",
    # Training/Model
    "TrainingError",
    "ModelLoadError",
    # Validation/Business rules
    "ValidationError",
    "BusinessRuleViolationError",
    # Resources/External
    "ResourceLimitExceededError",
    "ExternalServiceError",
]


# Backward/compat: some modules expect an EntityNotFoundError in business layer
class EntityNotFoundError(BusinessLogicError):
    """Raised when a requested domain entity cannot be found.

    This mirrors repository-level not-found but is exposed at business layer
    for use in services and use-cases where the abstraction boundary is higher.
    """

    def __init__(self, entity: str, identifier: Any, **kwargs: Any) -> None:  # type: ignore[name-defined]
        message = f"Entity not found: {entity} with id {identifier}"
        super().__init__(message, "BIZ_016", ErrorSeverity.MEDIUM, **kwargs)
