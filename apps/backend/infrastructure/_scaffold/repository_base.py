from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, TypeVar, runtime_checkable
from uuid import UUID
import Exception
import ValueError
import bool
import entity_id
import entity_type
import int
import isinstance
import list
import self
import str
import super
import type

"""Base repository contracts and interfaces.
⚠️  SCAFFOLD CODE - DO NOT AUTO-IMPORT
This module contains safe templates for repository patterns.
Import explicitly when ready to integrate.
"""

EntityT = TypeVar("EntityT")
IdT = TypeVar("IdT", bound=str | int | UUID, contravariant=True)


@runtime_checkable
class Entity(Protocol):
    """Protocol for domain entities."""

    id: Any  # Entity identifier
    created_at: Any  # Creation timestamp
    updated_at: Any  # Last update timestamp


class RepositoryError(Exception):
    """Base exception for repository operations."""


class EntityNotFoundError(RepositoryError):
    """Entity not found in repository."""

    def __init__(self, entity_type: str, entity_id: Any) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} not found")


class DuplicateEntityError(RepositoryError):
    """Entity already exists in repository."""

    def __init__(self, entity_type: str, entity_id: Any) -> None:
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with id {entity_id} already exists")


@runtime_checkable
class Repository(Protocol[EntityT, IdT]):
    """Generic repository protocol.
    Defines the contract that all repositories must implement.
    Type-safe with generic entity and ID types.
    """

    async def get_by_id(self, entity_id: IdT) -> EntityT | None:
        """Get entity by ID.
        Args:
            entity_id: The entity identifier
        Returns:
            Entity if found, None otherwise
        Raises:
            RepositoryError: On database errors
        """
        ...

    async def get_by_id_or_fail(self, entity_id: IdT) -> EntityT:
        """Get entity by ID or raise exception.
        Args:
            entity_id: The entity identifier
        Returns:
            Entity if found
        Raises:
            EntityNotFoundError: If entity not found
            RepositoryError: On database errors
        """
        ...

    async def create(self, entity: EntityT) -> EntityT:
        """Create new entity.
        Args:
            entity: Entity to create
        Returns:
            Created entity with updated fields
        Raises:
            DuplicateEntityError: If entity already exists
            RepositoryError: On database errors
        """
        ...

    async def update(self, entity: EntityT) -> EntityT:
        """Update existing entity.
        Args:
            entity: Entity to update
        Returns:
            Updated entity
        Raises:
            EntityNotFoundError: If entity not found
            RepositoryError: On database errors
        """
        ...

    async def delete(self, entity_id: IdT) -> bool:
        """Delete entity by ID.
        Args:
            entity_id: The entity identifier
        Returns:
            True if deleted, False if not found
        Raises:
            RepositoryError: On database errors
        """
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[EntityT]:
        """List all entities with pagination.
        Args:
            limit: Maximum number of entities to return
            offset: Number of entities to skip
        Returns:
            List of entities
        Raises:
            RepositoryError: On database errors
        """
        ...

    async def count(self) -> int:
        """Count total number of entities.
        Returns:
            Total count of entities
        Raises:
            RepositoryError: On database errors
        """
        ...


class BaseRepository(ABC, Generic[EntityT, IdT]):
    """Abstract base repository implementation.
    Provides common functionality and enforces contract compliance.
    Inherit from this class for concrete repository implementations.
    """

    def __init__(self, entity_type: type[EntityT]) -> None:
        """Initialize repository.
        Args:
            entity_type: The entity class this repository manages
        """
        self.entity_type = entity_type
        self.entity_name = entity_type.__name__

    @abstractmethod
    async def get_by_id(self, entity_id: IdT) -> EntityT | None:
        """Get entity by ID. Must be implemented by subclass."""

    async def get_by_id_or_fail(self, entity_id: IdT) -> EntityT:
        """Get entity by ID or raise exception."""
        entity = await self.get_by_id(entity_id)
        if entity is None:
            raise EntityNotFoundError(self.entity_name, entity_id)
        return entity

    @abstractmethod
    async def create(self, entity: EntityT) -> EntityT:
        """Create new entity. Must be implemented by subclass."""

    @abstractmethod
    async def update(self, entity: EntityT) -> EntityT:
        """Update entity. Must be implemented by subclass."""

    @abstractmethod
    async def delete(self, entity_id: IdT) -> bool:
        """Delete entity. Must be implemented by subclass."""

    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> list[EntityT]:
        """List entities. Must be implemented by subclass."""

    @abstractmethod
    async def count(self) -> int:
        """Count entities. Must be implemented by subclass."""

    def _validate_entity(self, entity: EntityT) -> None:
        """Validate entity before operations.
        Args:
            entity: Entity to validate
        Raises:
            ValueError: If entity is invalid
        """
        if not isinstance(entity, self.entity_type):
            raise ValueError(
                f"Expected {self.entity_name}, got {type(entity).__name__}"
            )


UUIDRepository = Repository[EntityT, UUID]
StringRepository = Repository[EntityT, str]
IntRepository = Repository[EntityT, int]
__all__ = [
    "BaseRepository",
    "DuplicateEntityError",
    "Entity",
    "EntityNotFoundError",
    "EntityT",
    "IdT",
    "IntRepository",
    "Repository",
    "RepositoryError",
    "StringRepository",
    "UUIDRepository",
]
