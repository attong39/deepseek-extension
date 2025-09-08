"""Unit of Work pattern interface.

Ensures transaction boundaries and consistency across repositories.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Protocol


class UnitOfWork(Protocol):
    """Unit of Work pattern cho transaction management."""

    @abstractmethod
    async def __aenter__(self) -> UnitOfWork:
        """Async context manager entry."""

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction."""


__all__ = ["UnitOfWork"]
