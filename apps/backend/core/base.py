"""
Core Base Classes for zeta-monorepo backend.

This module defines common base classes for core components, including entities,
services, use cases, and domain objects. It ensures type safety, validation,
and error handling with integrated logging.

Auto-fixed by comprehensive_init_fixer.py
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Union

# Imports from project structure (adjust paths if needed)
from zeta_monorepo.apps.backend.core.types import EntityId
from zeta_monorepo.apps.backend.core.utils.error_handler import CoreException
from zeta_monorepo.core.logger import get_logger  # Assumed standard logger
import Exception
import NotImplementedError
import ValueError
import aggregate_id
import bool
import candidate
import correlation_id
import created_at
import created_by
import details
import e
import event_type
import hash
import id
import int
import isinstance
import left
import metadata
import other
import repository
import right
import rule_name
import self
import service
import spec
import str
import super
import type
import updated_at
import updated_by
import user_id
import version

# Global logger instance
logger = get_logger(__name__)


class CoreEntity(ABC):
    """
    Base class for all core entities.

    Provides common attributes like ID, timestamps, and serialization methods.
    Ensures validation and error handling for entity creation.

    Attributes:
        id (str): Unique identifier for the entity.
        created_at (datetime): Timestamp when the entity was created.
        updated_at (datetime): Timestamp when the entity was last updated.
    """

    def __init__(
        self,
        id: Optional[EntityId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize the CoreEntity.

        Args:
            id (Optional[EntityId]): Unique identifier. If None, generates a UUID.
            created_at (Optional[datetime]): Creation timestamp. If None, uses current UTC time.
            updated_at (Optional[datetime]): Update timestamp. If None, uses current UTC time.

        Raises:
            ValueError: If id is not a string or None, or if timestamps are invalid.
        """
        try:
            self.id: str = id or str(uuid.uuid4())
            if not isinstance(self.id, str):
                raise ValueError("Entity ID must be a string.")
            self.created_at: datetime = created_at or datetime.now(UTC)
            self.updated_at: datetime = updated_at or datetime.now(UTC)
            if not isinstance(self.created_at, datetime) or not isinstance(self.updated_at, datetime):
                raise ValueError("Timestamps must be datetime objects.")
            logger.info(f"CoreEntity initialized with ID: {self.id}")
        except Exception as e:
            logger.error(f"Failed to initialize CoreEntity: {e}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert entity to dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the entity.
        """
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update_timestamp(self) -> None:
        """
        Update the updated_at timestamp to current UTC time.
        """
        self.updated_at = datetime.now(UTC)
        logger.debug(f"Updated timestamp for entity ID: {self.id}")

    def __eq__(self, other: Any) -> bool:
        """
        Check equality based on ID.

        Args:
            other (Any): Object to compare.

        Returns:
            bool: True if IDs match, False otherwise.
        """
        if not isinstance(other, CoreEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """
        Hash based on ID for use in sets/dicts.

        Returns:
            int: Hash value.
        """
        return hash(self.id)

    def __repr__(self) -> str:
        """
        String representation of the entity.

        Returns:
            str: Representation string.
        """
        return f"{self.__class__.__name__}(id='{self.id}')"


class VersionedEntity(CoreEntity):
    """
    Base class for versioned entities.

    Extends CoreEntity with version tracking.

    Attributes:
        version (int): Version number of the entity.
    """

    def __init__(
        self,
        id: Optional[EntityId] = None,
        version: int = 1,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize the VersionedEntity.

        Args:
            id (Optional[EntityId]): Unique identifier.
            version (int): Initial version number. Must be positive.
            created_at (Optional[datetime]): Creation timestamp.
            updated_at (Optional[datetime]): Update timestamp.

        Raises:
            ValueError: If version is not a positive integer.
        """
        super().__init__(id, created_at, updated_at)
        if not isinstance(version, int) or version < 1:
            raise ValueError("Version must be a positive integer.")
        self.version: int = version

    def increment_version(self) -> None:
        """
        Increment version number and update timestamp.
        """
        self.version += 1
        self.update_timestamp()
        logger.debug(f"Incremented version to {self.version} for entity ID: {self.id}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with version.

        Returns:
            Dict[str, Any]: Dictionary representation including version.
        """
        data = super().to_dict()
        data["version"] = self.version
        return data


class AuditableEntity(CoreEntity):
    """
    Base class for auditable entities.

    Extends CoreEntity with audit fields for tracking creators/updaters.

    Attributes:
        created_by (Optional[str]): ID of the user who created the entity.
        updated_by (Optional[str]): ID of the user who last updated the entity.
    """

    def __init__(
        self,
        id: Optional[EntityId] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize the AuditableEntity.

        Args:
            id (Optional[EntityId]): Unique identifier.
            created_by (Optional[str]): Creator user ID.
            updated_by (Optional[str]): Updater user ID.
            created_at (Optional[datetime]): Creation timestamp.
            updated_at (Optional[datetime]): Update timestamp.

        Raises:
            ValueError: If user IDs are not strings or None.
        """
        super().__init__(id, created_at, updated_at)
        if created_by is not None and not isinstance(created_by, str):
            raise ValueError("created_by must be a string or None.")
        if updated_by is not None and not isinstance(updated_by, str):
            raise ValueError("updated_by must be a string or None.")
        self.created_by: Optional[str] = created_by
        self.updated_by: Optional[str] = updated_by

    def set_created_by(self, user_id: str) -> None:
        """
        Set created by user.

        Args:
            user_id (str): User ID. Must be a non-empty string.

        Raises:
            ValueError: If user_id is not a string or is empty.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")
        self.created_by = user_id
        logger.debug(f"Set created_by to {user_id} for entity ID: {self.id}")

    def set_updated_by(self, user_id: str) -> None:
        """
        Set updated by user and update timestamp.

        Args:
            user_id (str): User ID. Must be a non-empty string.

        Raises:
            ValueError: If user_id is not a string or is empty.
        """
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("user_id must be a non-empty string.")
        self.updated_by = user_id
        self.update_timestamp()
        logger.debug(f"Set updated_by to {user_id} for entity ID: {self.id}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary with audit info.

        Returns:
            Dict[str, Any]: Dictionary representation including audit fields.
        """
        data = super().to_dict()
        data["created_by"] = self.created_by
        data["updated_by"] = self.updated_by
        return data


class CoreService(ABC):
    """
    Base class for all core services.

    Provides a structure for services with repository integration and metrics.

    Attributes:
        repository (Optional[Any]): Repository instance for data access.
    """

    def __init__(self, repository: Optional[Any] = None) -> None:
        """
        Initialize the CoreService.

        Args:
            repository (Optional[Any]): Repository instance.
        """
        self.repository: Optional[Any] = repository
        logger.info(f"CoreService initialized with repository: {type(repository).__name__ if repository else None}")

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Main service execution method.

        Args:
            *args: Variable positional arguments.
            **kwargs: Variable keyword arguments.

        Returns:
            Any: Result of execution.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement execute method.")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get service metrics.

        Returns:
            Dict[str, Any]: Metrics dictionary.
        """
        return {
            "service_name": self.__class__.__name__,
            "repository_type": type(self.repository).__name__ if self.repository else None,
        }


class UseCase(ABC):
    """
    Base class for use cases.

    Provides a structure for business logic execution with validation.

    Attributes:
        service (Optional[CoreService]): Associated service instance.
    """

    def __init__(self, service: Optional[CoreService] = None) -> None:
        """
        Initialize the UseCase.

        Args:
            service (Optional[CoreService]): Service instance.
        """
        self.service: Optional[CoreService] = service
        logger.info(f"UseCase initialized with service: {type(service).__name__ if service else None}")

    @abstractmethod
    async def execute(self, request: Any) -> Any:
        """
        Execute the use case.

        Args:
            request (Any): Request object.

        Returns:
            Any: Result of execution.

        Raises:
            NotImplementedError: If not implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement execute method.")

    def validate_request(self, request: Any) -> List[str]:
        """
        Validate use case request.

        Args:
            request (Any): Request to validate.

        Returns:
            List[str]: List of validation errors (empty if valid).
        """
        return []


class DomainEvent:
    """
    Base class for domain events.

    Represents events in the domain with metadata.

    Attributes:
        event_type (str): Type of the event.
        aggregate_id (EntityId): ID of the aggregate.
        correlation_id (str): Correlation ID for tracing.
        occurred_at (datetime): Timestamp when the event occurred.
        metadata (Dict[str, Any]): Additional metadata.
    """

    def __init__(
        self,
        event_type: str,
        aggregate_id: EntityId,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the DomainEvent.

        Args:
            event_type (str): Event type. Must be a non-empty string.
            aggregate_id (EntityId): Aggregate ID.
            correlation_id (Optional[str]): Correlation ID. If None, generates a UUID.
            metadata (Optional[Dict[str, Any]]): Metadata dictionary.

        Raises:
            ValueError: If event_type is not a string or is empty.
        """
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type must be a non-empty string.")
        self.event_type: str = event_type
        self.aggregate_id: EntityId = aggregate_id
        self.correlation_id: str = correlation_id or str(uuid.uuid4())
        self.occurred_at: datetime = datetime.now(UTC)
        self.metadata: Dict[str, Any] = metadata or {}
        logger.info(f"DomainEvent created: {self.event_type} for aggregate {self.aggregate_id}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation.
        """
        return {
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "correlation_id": self.correlation_id,
            "occurred_at": self.occurred_at.isoformat(),
            "metadata": self.metadata,
        }

    def __repr__(self) -> str:
        """
        String representation.

        Returns:
            str: Representation string.
        """
        return f"{self.__class__.__name__}(type='{self.event_type}', aggregate='{self.aggregate_id}')"


class ValueObject(ABC):
    """
    Base class for value objects.

    Ensures immutability and equality based on value.
    """

    @abstractmethod
    def equals(self, other: Any) -> bool:
        """
        Check equality with another value object.

        Args:
            other (Any): Object to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement equals method.")

    def __eq__(self, other: Any) -> bool:
        """
        Implement equality.

        Args:
            other (Any): Object to compare.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.equals(other)

    @abstractmethod
    def __hash__(self) -> int:
        """
        Implement hash for use in sets/dicts.

        Returns:
            int: Hash value.
        """
        raise NotImplementedError("Subclasses must implement __hash__ method.")


class Specification(ABC):
    """
    Base class for specifications (business rules).

    Allows combining rules with AND, OR, NOT.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        """
        Check if candidate satisfies the specification.

        Args:
            candidate (Any): Object to check.

        Returns:
            bool: True if satisfied, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement is_satisfied_by method.")

    def and_(self, other: Specification) -> Specification:
        """
        Combine with AND.

        Args:
            other (Specification): Other specification.

        Returns:
            Specification: Combined specification.
        """
        return AndSpecification(self, other)

    def or_(self, other: Specification) -> Specification:
        """
        Combine with OR.

        Args:
            other (Specification): Other specification.

        Returns:
            Specification: Combined specification.
        """
        return OrSpecification(self, other)

    def not_(self) -> Specification:
        """
        Negate specification.

        Returns:
            Specification: Negated specification.
        """
        return NotSpecification(self)


class AndSpecification(Specification):
    """
    AND combination of specifications.
    """

    def __init__(self, left: Specification, right: Specification) -> None:
        """
        Initialize AndSpecification.

        Args:
            left (Specification): Left specification.
            right (Specification): Right specification.
        """
        self.left: Specification = left
        self.right: Specification = right

    def is_satisfied_by(self, candidate: Any) -> bool:
        """
        Check if candidate satisfies both specifications.

        Args:
            candidate (Any): Object to check.

        Returns:
            bool: True if both satisfied, False otherwise.
        """
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)


class OrSpecification(Specification):
    """
    OR combination of specifications.
    """

    def __init__(self, left: Specification, right: Specification) -> None:
        """
        Initialize OrSpecification.

        Args:
            left (Specification): Left specification.
            right (Specification): Right specification.
        """
        self.left: Specification = left
        self.right: Specification = right

    def is_satisfied_by(self, candidate: Any) -> bool:
        """
        Check if candidate satisfies at least one specification.

        Args:
            candidate (Any): Object to check.

        Returns:
            bool: True if at least one satisfied, False otherwise.
        """
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)


class NotSpecification(Specification):
    """
    NOT specification.
    """

    def __init__(self, spec: Specification) -> None:
        """
        Initialize NotSpecification.

        Args:
            spec (Specification): Specification to negate.
        """
        self.spec: Specification = spec

    def is_satisfied_by(self, candidate: Any) -> bool:
        """
        Check if candidate does not satisfy the specification.

        Args:
            candidate (Any): Object to check.

        Returns:
            bool: True if not satisfied, False otherwise.
        """
        return not self.spec.is_satisfied_by(candidate)


class BusinessRuleViolation(CoreException):
    """
    Exception for business rule violations.

    Extends CoreException with rule-specific details.
    """

    def __init__(self, rule_name: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize BusinessRuleViolation.

        Args:
            rule_name (str): Name of the violated rule.
            details (Optional[Dict[str, Any]]): Additional details.
        """
        super().__init__(
            f"Business rule '{rule_name}' violated",
            "BUSINESS_RULE_VIOLATION",
            details or {},
        )
        self.rule_name: str = rule_name


__all__ = [
    "AndSpecification",
    "AuditableEntity",
    "BusinessRuleViolation",
    "CoreEntity",
    "CoreService",
    "DomainEvent",
    "NotSpecification",
    "OrSpecification",
    "Specification",
    "UseCase",
    "ValueObject",
    "VersionedEntity",
]
