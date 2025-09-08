"""
Repository and Data Access Exception Classes
Handles all data layer errors in ZETA AI Server
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
import Exception
import actual
import bool
import cache_type
import column
import constraint
import database
import details
import dict
import entity
import error_code
import expected
import field
import identifier
import int
import key
import kwargs
import operation
import parameters
import pool_size
import query
import reason
import retryable
import self
import str
import super
import table
import timeout
import value
import version

logger = logging.getLogger(__name__)


class BaseRepositoryError(Exception):
    """Base repository error class."""

    def __init__(
        self,
        message: str,
        error_code: str,
        query: str | None = None,
        parameters: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.query = query
        self.parameters = parameters
        self.retryable = retryable
        self.timestamp = datetime.now(UTC)

        # Log repository errors
        logger.error(
            "Repository Error: %s - %s",
            error_code,
            message,
            extra={
                "error_code": error_code,
                "query": query,
                "retryable": retryable,
            },
        )

        super().__init__(message)


# Database connection exceptions
class DatabaseConnectionError(BaseRepositoryError):
    """Raised when database connection fails."""

    def __init__(self, database: str, reason: str, **kwargs: Any) -> None:
        message = f"Failed to connect to database '{database}': {reason}"
        super().__init__(message, "REPO_001", retryable=True, **kwargs)


class ConnectionPoolExhaustedError(BaseRepositoryError):
    """Raised when connection pool is exhausted."""

    def __init__(self, pool_size: int, **kwargs: Any) -> None:
        message = f"Connection pool exhausted (size: {pool_size})"
        super().__init__(message, "REPO_002", retryable=True, **kwargs)


# Data integrity exceptions
class DataIntegrityError(BaseRepositoryError):
    """Raised for data integrity violations."""

    def __init__(self, constraint: str, details: str, **kwargs: Any) -> None:
        message = f"Data integrity violation: {constraint} - {details}"
        super().__init__(message, "REPO_003", **kwargs)


class ForeignKeyViolationError(BaseRepositoryError):
    """Raised for foreign key constraint violations."""

    def __init__(self, table: str, column: str, value: Any, **kwargs: Any) -> None:
        message = f"Foreign key violation: {table}.{column} = {value}"
        super().__init__(message, "REPO_004", **kwargs)


# Record operation exceptions
class RecordNotFoundError(BaseRepositoryError):
    """Raised when a record is not found."""

    def __init__(self, entity: str, identifier: Any, **kwargs: Any) -> None:
        message = f"Record not found: {entity} with id {identifier}"
        super().__init__(message, "REPO_005", **kwargs)


class DuplicateRecordError(BaseRepositoryError):
    """Raised when attempting to create duplicate records."""

    def __init__(self, entity: str, key: str, value: Any, **kwargs: Any) -> None:
        message = f"Duplicate record: {entity} with {key} = {value}"
        super().__init__(message, "REPO_006", **kwargs)


# Query execution exceptions
class QueryExecutionError(BaseRepositoryError):
    """Raised when query execution fails."""

    def __init__(self, reason: str, **kwargs: Any) -> None:
        message = f"Query execution failed: {reason}"
        super().__init__(message, "REPO_007", **kwargs)


class QueryTimeoutError(BaseRepositoryError):
    """Raised when query execution times out."""

    def __init__(self, timeout: int, **kwargs: Any) -> None:
        message = f"Query execution timed out after {timeout} seconds"
        super().__init__(message, "REPO_008", retryable=True, **kwargs)


# Transaction exceptions
class TransactionError(BaseRepositoryError):
    """Raised for transaction-related errors."""

    def __init__(self, operation: str, reason: str, **kwargs: Any) -> None:
        message = f"Transaction {operation} failed: {reason}"
        super().__init__(message, "REPO_009", **kwargs)


class DeadlockError(BaseRepositoryError):
    """Raised when database deadlock occurs."""

    def __init__(self, **kwargs: Any) -> None:
        message = "Database deadlock detected"
        super().__init__(message, "REPO_010", retryable=True, **kwargs)


# Vector database exceptions
class VectorDatabaseError(BaseRepositoryError):
    """Raised for vector database operations."""

    def __init__(self, operation: str, reason: str, **kwargs: Any) -> None:
        message = f"Vector database operation '{operation}' failed: {reason}"
        super().__init__(message, "REPO_011", **kwargs)


class EmbeddingDimensionError(BaseRepositoryError):
    """Raised when embedding dimensions don't match."""

    def __init__(self, expected: int, actual: int, **kwargs: Any) -> None:
        message = f"Embedding dimension mismatch: expected {expected}, got {actual}"
        super().__init__(message, "REPO_012", **kwargs)


# Cache exceptions
class CacheError(BaseRepositoryError):
    """Raised for cache operation failures."""

    def __init__(self, operation: str, key: str, reason: str, **kwargs: Any) -> None:
        message = f"Cache operation '{operation}' failed for key '{key}': {reason}"
        super().__init__(message, "REPO_013", retryable=True, **kwargs)


class CacheConnectionError(BaseRepositoryError):
    """Raised when cache connection fails."""

    def __init__(self, cache_type: str, reason: str, **kwargs: Any) -> None:
        message = f"Failed to connect to {cache_type} cache: {reason}"
        super().__init__(message, "REPO_014", retryable=True, **kwargs)


# Migration exceptions
class MigrationError(BaseRepositoryError):
    """Raised for database migration failures."""

    def __init__(self, version: str, reason: str, **kwargs: Any) -> None:
        message = f"Migration to version {version} failed: {reason}"
        super().__init__(message, "REPO_015", **kwargs)


# Backup/Restore exceptions
class BackupError(BaseRepositoryError):
    """Raised for backup operation failures."""

    def __init__(self, operation: str, reason: str, **kwargs: Any) -> None:
        message = f"Backup operation '{operation}' failed: {reason}"
        super().__init__(message, "REPO_016", **kwargs)


# Input/validation exceptions
class ValidationError(BaseRepositoryError):
    """Raised for invalid input or payloads at the repository boundary.

    This is intentionally separate from business-layer validation. Use this
    when a repository method receives invalid parameters (e.g., malformed
    filters) or detects schema-level violations prior to persistence.
    """

    def __init__(
        self,
        field: str | None = None,
        value: Any | None = None,
        reason: str = "invalid",
        **kwargs: Any,
    ) -> None:
        detail = f"{field}={value} - {reason}" if field is not None else reason
        message = f"Validation error: {detail}"
        super().__init__(message, "REPO_017", **kwargs)


# ---------------------------------------------------------------------------
# Compatibility aliases for legacy names used in the codebase
# ---------------------------------------------------------------------------
RepositoryError = BaseRepositoryError
ConnectionError = DatabaseConnectionError
EntityNotFoundError = RecordNotFoundError
DuplicateEntityError = DuplicateRecordError


__all__ = [
    # Base
    "BaseRepositoryError",
    "RepositoryError",
    # Connection
    "DatabaseConnectionError",
    "ConnectionPoolExhaustedError",
    # Integrity
    "DataIntegrityError",
    "ForeignKeyViolationError",
    # Records
    "RecordNotFoundError",
    "DuplicateRecordError",
    # Query
    "QueryExecutionError",
    "QueryTimeoutError",
    # Txn
    "TransactionError",
    "DeadlockError",
    # Vector
    "VectorDatabaseError",
    "EmbeddingDimensionError",
    # Cache
    "CacheError",
    "CacheConnectionError",
    # Migration/Backup
    "MigrationError",
    "BackupError",
    # Validation
    "ValidationError",
    # Legacy aliases
    "ConnectionError",
    "EntityNotFoundError",
    "DuplicateEntityError",
]
