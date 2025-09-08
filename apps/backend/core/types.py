"""
Core Type Definitions
====================
Unified type definitions for the entire core layer.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Protocol, TypeVar

# Imports from project structure (adjust paths if needed)
from .observability.logging import get_logger  # Standard logger
import ValueError
import bool
import classmethod
import cls
import data
import e
import error
import float
import int
import isinstance
import page
import property
import self
import size
import sort_by
import sort_order
import str
import success
import total

# Global logger instance
logger = get_logger(__name__)

T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
EntityId = str
Timestamp = float
CorrelationId = str
UserId = str
TenantId = str
JSON = Dict[str, Any]
Metadata = Dict[str, Any]


class Result(Generic[T, U]):
    """
    Generic result type for operations.

    Attributes:
        success (bool): Indicates if the operation was successful.
        data (Optional[T]): The data returned if successful.
        error (Optional[U]): The error returned if failed.
    """

    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[U] = None) -> None:
        """
        Initialize the Result.

        Args:
            success (bool): Success status.
            data (Optional[T]): Success data.
            error (Optional[U]): Error data.

        Raises:
            ValueError: If success is True but data is None, or success is False but error is None.
        """
        try:
            if success and data is None:
                raise ValueError("Success result must have data.")
            if not success and error is None:
                raise ValueError("Error result must have error.")
            self.success = success
            self.data = data
            self.error = error
            logger.debug(f"Created Result: success={success}")
        except ValueError as e:
            logger.error(f"Error initializing Result: {e}")
            raise

    @classmethod
    def ok(cls, data: T) -> Result[T, Any]:
        """
        Create a successful result.

        Args:
            data (T): The success data.

        Returns:
            Result[T, Any]: Successful result.
        """
        return cls(True, data=data)

    @classmethod
    def err(cls, error: U) -> Result[Any, U]:
        """
        Create an error result.

        Args:
            error (U): The error data.

        Returns:
            Result[Any, U]: Error result.
        """
        return cls(False, error=error)


class Identifiable(Protocol):
    """
    Protocol for identifiable entities.

    Attributes:
        id (EntityId): Unique identifier.
    """
    id: EntityId


class Timestamped(Protocol):
    """
    Protocol for timestamped entities.

    Attributes:
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Update timestamp.
    """
    created_at: datetime
    updated_at: datetime


class Versioned(Protocol):
    """
    Protocol for versioned entities.

    Attributes:
        version (int): Version number.
    """
    version: int


class Auditable(Protocol):
    """
    Protocol for auditable entities.

    Attributes:
        created_by (Optional[UserId]): Creator user ID.
        updated_by (Optional[UserId]): Updater user ID.
    """
    created_by: Optional[UserId]
    updated_by: Optional[UserId]


class RepositoryProtocol(Protocol[T]):
    """
    Standard repository interface.

    Attributes:
        T: The entity type.
    """

    async def get_by_id(self, id: EntityId) -> Optional[T]:
        """
        Get entity by ID.

        Args:
            id (EntityId): Entity ID.

        Returns:
            Optional[T]: The entity or None if not found.
        """
        ...

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """
        Get all entities with pagination.

        Args:
            limit (int): Maximum number of entities.
            offset (int): Offset for pagination.

        Returns:
            List[T]: List of entities.
        """
        ...

    async def save(self, entity: T) -> T:
        """
        Save entity.

        Args:
            entity (T): Entity to save.

        Returns:
            T: Saved entity.
        """
        ...

    async def delete(self, id: EntityId) -> bool:
        """
        Delete entity by ID.

        Args:
            id (EntityId): Entity ID.

        Returns:
            bool: True if deleted, False otherwise.
        """
        ...

    async def exists(self, id: EntityId) -> bool:
        """
        Check if entity exists.

        Args:
            id (EntityId): Entity ID.

        Returns:
            bool: True if exists, False otherwise.
        """
        ...

    async def count(self) -> int:
        """
        Count total entities.

        Returns:
            int: Total count.
        """
        ...


class QueryableRepositoryProtocol(RepositoryProtocol[T], Protocol):
    """
    Repository with query capabilities.

    Attributes:
        T: The entity type.
    """

    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[T]:
        """
        Find entities by criteria.

        Args:
            criteria (Dict[str, Any]): Search criteria.

        Returns:
            List[T]: List of matching entities.
        """
        ...

    async def find_one_by_criteria(self, criteria: Dict[str, Any]) -> Optional[T]:
        """
        Find one entity by criteria.

        Args:
            criteria (Dict[str, Any]): Search criteria.

        Returns:
            Optional[T]: The entity or None if not found.
        """
        ...


class ServiceProtocol(Protocol[T, U]):
    """
    Standard service interface.

    Attributes:
        T: The request type.
        U: The response type.
    """

    async def execute(self, request: T) -> U:
        """
        Execute service operation.

        Args:
            request (T): Request data.

        Returns:
            U: Response data.
        """
        ...

    async def validate(self, request: T) -> List[str]:
        """
        Validate request.

        Args:
            request (T): Request data.

        Returns:
            List[str]: List of validation errors.
        """
        ...

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get service metrics.

        Returns:
            Dict[str, Any]: Metrics data.
        """
        ...


class DomainEvent(Protocol):
    """
    Protocol for domain events.

    Attributes:
        event_type (str): Type of the event.
        aggregate_id (EntityId): Aggregate ID.
        occurred_at (datetime): Occurrence timestamp.
        correlation_id (Optional[CorrelationId]): Correlation ID.
    """
    event_type: str
    aggregate_id: EntityId
    occurred_at: datetime
    correlation_id: Optional[CorrelationId]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary.

        Returns:
            Dict[str, Any]: Dictionary representation.
        """
        ...


class DomainEventHandler(Protocol[T]):
    """
    Protocol for domain event handlers.

    Attributes:
        T: The event type.
    """

    async def handle(self, event: T) -> None:
        """
        Handle domain event.

        Args:
            event (T): The event to handle.
        """
        ...


class UseCaseProtocol(Protocol[T, U]):
    """
    Standard use case interface.

    Attributes:
        T: The request type.
        U: The response type.
    """

    async def execute(self, request: T) -> Result[U, str]:
        """
        Execute use case.

        Args:
            request (T): Request data.

        Returns:
            Result[U, str]: Result of execution.
        """
        ...


class ValidatorProtocol(Protocol[T]):
    """
    Standard validator interface.

    Attributes:
        T: The data type to validate.
    """

    def validate(self, data: T) -> List[str]:
        """
        Validate data and return error messages.

        Args:
            data (T): Data to validate.

        Returns:
            List[str]: List of validation errors.
        """
        ...


class CacheProtocol(Protocol[T]):
    """
    Standard cache interface.

    Attributes:
        T: The value type.
    """

    async def get(self, key: str) -> Optional[T]:
        """
        Get value from cache.

        Args:
            key (str): Cache key.

        Returns:
            Optional[T]: Cached value or None.
        """
        ...

    async def set(self, key: str, value: T, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key (str): Cache key.
            value (T): Value to cache.
            ttl (Optional[int]): Time to live in seconds.
        """
        ...

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if deleted, False otherwise.
        """
        ...

    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if exists, False otherwise.
        """
        ...

    async def clear(self) -> None:
        """
        Clear all cache.
        """
        ...


class ConfigProtocol(Protocol):
    """
    Standard configuration interface.
    """

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key (str): Configuration key.
            default (Any): Default value.

        Returns:
            Any: Configuration value.
        """
        ...

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get boolean configuration value.

        Args:
            key (str): Configuration key.
            default (bool): Default value.

        Returns:
            bool: Boolean value.
        """
        ...

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get integer configuration value.

        Args:
            key (str): Configuration key.
            default (int): Default value.

        Returns:
            int: Integer value.
        """
        ...

    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get float configuration value.

        Args:
            key (str): Configuration key.
            default (float): Default value.

        Returns:
            float: Float value.
        """
        ...

    def get_list(self, key: str, default: Optional[List[Any]] = None) -> List[Any]:
        """
        Get list configuration value.

        Args:
            key (str): Configuration key.
            default (Optional[List[Any]]): Default value.

        Returns:
            List[Any]: List value.
        """
        ...


class PaginationParams:
    """
    Standard pagination parameters.

    Attributes:
        page (int): Current page number.
        size (int): Page size.
        sort_by (Optional[str]): Sort field.
        sort_order (str): Sort order.
    """

    def __init__(
        self,
        page: int = 1,
        size: int = 20,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> None:
        """
        Initialize PaginationParams.

        Args:
            page (int): Page number. Must be >= 1.
            size (int): Page size. Must be between 1 and 100.
            sort_by (Optional[str]): Sort field.
            sort_order (str): Sort order ('asc' or 'desc').

        Raises:
            ValueError: If parameters are invalid.
        """
        try:
            if not isinstance(page, int) or page < 1:
                raise ValueError("page must be an integer >= 1.")
            if not isinstance(size, int) or size < 1 or size > 100:
                raise ValueError("size must be an integer between 1 and 100.")
            if sort_order.lower() not in ("asc", "desc"):
                raise ValueError("sort_order must be 'asc' or 'desc'.")
            self.page = page
            self.size = size
            self.sort_by = sort_by
            self.sort_order = sort_order.lower()
            logger.debug(f"Created PaginationParams: page={page}, size={size}")
        except ValueError as e:
            logger.error(f"Error initializing PaginationParams: {e}")
            raise

    @property
    def offset(self) -> int:
        """
        Calculate offset for database queries.

        Returns:
            int: Offset value.
        """
        return (self.page - 1) * self.size


class PaginatedResult(Generic[T]):
    """
    Standard paginated result.

    Attributes:
        items (List[T]): List of items.
        total (int): Total number of items.
        page (int): Current page.
        size (int): Page size.
        total_pages (int): Total number of pages.
    """

    def __init__(self, items: List[T], total: int, page: int, size: int) -> None:
        """
        Initialize PaginatedResult.

        Args:
            items (List[T]): List of items.
            total (int): Total number of items.
            page (int): Current page.
            size (int): Page size.

        Raises:
            ValueError: If parameters are invalid.
        """
        try:
            if not isinstance(total, int) or total < 0:
                raise ValueError("total must be a non-negative integer.")
            if not isinstance(page, int) or page < 1:
                raise ValueError("page must be an integer >= 1.")
            if not isinstance(size, int) or size < 1:
                raise ValueError("size must be an integer >= 1.")
            self.items = items
            self.total = total
            self.page = page
            self.size = size
            self.total_pages = (total + size - 1) // size  # Ceiling division
            logger.debug(f"Created PaginatedResult: total={total}, page={page}, size={size}")
        except ValueError as e:
            logger.error(f"Error initializing PaginatedResult: {e}")
            raise

    @property
    def has_next(self) -> bool:
        """
        Check if there are more pages.

        Returns:
            bool: True if there are more pages, False otherwise.
        """
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        """
        Check if there are previous pages.

        Returns:
            bool: True if there are previous pages, False otherwise.
        """
        return self.page > 1


# Additional type aliases for flexibility
StringOrNone = Optional[str]
IntOrNone = Optional[int]
BoolOrNone = Optional[bool]
DictOrNone = Optional[Dict[str, Any]]
ListOrNone = Optional[List[Any]]

# Configurable constants (can be overridden via environment variables for no hard-coding)
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 20))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", 100))
DEFAULT_CACHE_TTL = int(os.getenv("DEFAULT_CACHE_TTL", 300))  # 5 minutes

__all__ = [
    "Auditable",
    "BoolOrNone",
    "CacheProtocol",
    "ConfigProtocol",
    "CorrelationId",
    "DEFAULT_CACHE_TTL",
    "DEFAULT_PAGE_SIZE",
    "DictOrNone",
    "DomainEvent",
    "DomainEventHandler",
    "EntityId",
    "Identifiable",
    "IntOrNone",
    "JSON",
    "ListOrNone",
    "MAX_PAGE_SIZE",
    "Metadata",
    "PaginatedResult",
    "PaginationParams",
    "QueryableRepositoryProtocol",
    "RepositoryProtocol",
    "Result",
    "ServiceProtocol",
    "StringOrNone",
    "T",
    "TenantId",
    "Timestamp",
    "Timestamped",
    "U",
    "UseCaseProtocol",
    "UserId",
    "V",
    "ValidatorProtocol",
    "Versioned",
]
