from __future__ import annotations

from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Protocol, TypeVar, runtime_checkable
import BaseException
import Exception
import bool
import dict
import exc_type
import property
import repo_type
import self
import super
import type

"""Unit of Work pattern contracts and implementation.
⚠️  SCAFFOLD CODE - DO NOT AUTO-IMPORT
This module contains safe templates for UoW patterns.
Import explicitly when ready to integrate.
"""
UoWType = TypeVar("UoWType", bound="UnitOfWork")


class UnitOfWorkError(Exception):
    """Base exception for Unit of Work operations."""


class TransactionError(UnitOfWorkError):
    """Transaction-related errors."""


class CommitError(TransactionError):
    """Error during commit operation."""


class RollbackError(TransactionError):
    """Error during rollback operation."""


@runtime_checkable
class UnitOfWork(Protocol):
    """Unit of Work protocol.
    Manages database transactions and repository access.
    Ensures data consistency across multiple repository operations.
    """

    async def __aenter__(self) -> UnitOfWork:
        """Enter async context manager.
        Returns:
            The UoW instance
        Raises:
            UnitOfWorkError: On setup errors
        """
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager.
        Args:
            exc_type: Exception type if any
            exc_val: Exception value if any
            exc_tb: Exception traceback if any
        Raises:
            UnitOfWorkError: On cleanup errors
        """
        ...

    async def commit(self) -> None:
        """Commit the current transaction.
        Raises:
            CommitError: If commit fails
            UnitOfWorkError: On other errors
        """
        ...

    async def rollback(self) -> None:
        """Rollback the current transaction.
        Raises:
            RollbackError: If rollback fails
            UnitOfWorkError: On other errors
        """
        ...

    async def flush(self) -> None:
        """Flush pending changes without committing.
        Useful for getting auto-generated IDs before commit.
        Raises:
            UnitOfWorkError: On flush errors
        """
        ...

    def is_active(self) -> bool:
        """Check if transaction is active.
        Returns:
            True if transaction is active
        """
        ...


@runtime_checkable
class RepositoryProvider(Protocol):
    """Protocol for providing repository access within UoW.
    UoW implementations should inherit from this to provide
    type-safe repository access.
    """

    def get_repository(self, repo_type: type[Any]) -> Any:
        """Get repository instance by type.
        Args:
            repo_type: Repository class to get
        Returns:
            Repository instance
        Raises:
            ValueError: If repository type not supported
            UnitOfWorkError: On access errors
        """
        ...


class BaseUnitOfWork(ABC):
    """Abstract base implementation of Unit of Work.
    Provides common functionality and transaction management.
    Subclasses must implement the abstract methods.
    """

    def __init__(self) -> None:
        """Initialize Unit of Work."""
        self._is_active = False
        self._repositories: dict[type[Any], Any] = {}

    async def __aenter__(self) -> BaseUnitOfWork:
        """Enter async context and start transaction."""
        await self._begin()
        self._is_active = True
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context and handle transaction cleanup."""
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            self._is_active = False
            await self._cleanup()

    @abstractmethod
    async def _begin(self) -> None:
        """Begin transaction. Must be implemented by subclass."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction. Must be implemented by subclass."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction. Must be implemented by subclass."""

    @abstractmethod
    async def flush(self) -> None:
        """Flush changes. Must be implemented by subclass."""

    @abstractmethod
    async def _cleanup(self) -> None:
        """Cleanup resources. Must be implemented by subclass."""

    def is_active(self) -> bool:
        """Check if transaction is active."""
        return self._is_active

    def get_repository(self, repo_type: type[Any]) -> Any:
        """Get repository instance by type.
        Args:
            repo_type: Repository class to get
        Returns:
            Repository instance
        Raises:
            ValueError: If repository type not supported
            UnitOfWorkError: If UoW not active
        """
        if not self._is_active:
            raise UnitOfWorkError("Unit of Work is not active")
        if repo_type not in self._repositories:
            repository = self._create_repository(repo_type)
            self._repositories[repo_type] = repository
        return self._repositories[repo_type]

    @abstractmethod
    def _create_repository(self, repo_type: type[Any]) -> Any:
        """Create repository instance. Must be implemented by subclass.
        Args:
            repo_type: Repository class to create
        Returns:
            Repository instance
        """


class MockUnitOfWork(BaseUnitOfWork):
    """Mock implementation for testing.
    Does not perform actual database operations.
    Useful for testing business logic without database.
    """

    def __init__(self) -> None:
        super().__init__()
        self._committed = False
        self._rolled_back = False

    async def _begin(self) -> None:
        """Begin mock transaction."""

    async def commit(self) -> None:
        """Mock commit."""
        if not self._is_active:
            raise CommitError("No active transaction to commit")
        self._committed = True

    async def rollback(self) -> None:
        """Mock rollback."""
        if not self._is_active:
            raise RollbackError("No active transaction to rollback")
        self._rolled_back = True

    async def flush(self) -> None:
        """Mock flush."""

    async def _cleanup(self) -> None:
        """Mock cleanup."""

    def _create_repository(self, repo_type: type[Any]) -> Any:
        """Create mock repository."""

        class MockRepository:
            def __init__(self, repo_type: type[Any]) -> None:
                self.repo_type = repo_type

        return MockRepository(repo_type)

    @property
    def committed(self) -> bool:
        """Check if transaction was committed."""
        return self._committed

    @property
    def rolled_back(self) -> bool:
        """Check if transaction was rolled back."""
        return self._rolled_back


__all__ = [
    "BaseUnitOfWork",
    "CommitError",
    "MockUnitOfWork",
    "RepositoryProvider",
    "RollbackError",
    "TransactionError",
    "UnitOfWork",
    "UnitOfWorkError",
    "UoWType",
]
