"""Domain repository interfaces (ports).

Clean Architecture: Domain layer defines interfaces, infrastructure implements.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar
import Exception
import actual_version
import entity_id
import expected_version
import int
import self
import str
import super

T = TypeVar("T")  # Domain Entity type


class RepositoryError(Exception):
    """Base repository error."""


class NotFoundError(RepositoryError):
    """Entity not found error."""


class ConcurrencyError(RepositoryError):
    """Optimistic locking conflict error."""

    def __init__(self, entity_id: str, expected_version: int, actual_version: int):
        self.entity_id = entity_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Optimistic lock failed for entity {entity_id}: "
            f"expected version {expected_version}, got {actual_version}"
        )


class Repository(Protocol, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    async def get(self, entity_id: str) -> T:
        """Get entity by ID. Raises NotFoundError if not found."""

    @abstractmethod
    async def try_get(self, entity_id: str) -> T | None:
        """Try to get entity by ID. Returns None if not found."""

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add new entity."""

    @abstractmethod
    async def remove(self, entity_id: str) -> None:
        """Remove entity. Raises NotFoundError if not found."""

    @abstractmethod
    async def list(
        self, *, limit: int = 100, offset: int = 0, **filters
    ) -> Iterable[T]:
        """List entities with pagination and filters."""


class VersionedRepository(Repository[T], Protocol, Generic[T]):
    """Repository với optimistic locking support.

    Entity phải có field `version: int`.
    """

    @abstractmethod
    async def update(self, entity: T, *, expected_version: int) -> T:
        """Update entity với version check. Raises ConcurrencyError if version mismatch."""


__all__ = [
    "Repository",
    "VersionedRepository",
    "RepositoryError",
    "NotFoundError",
    "ConcurrencyError",
]
