"""Generic in-memory repository base for simple CRUD in tests/dev.

This utility provides a typed, minimal repository for entities identified by
string IDs. It is intentionally simple and should not be used in production.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar
import bool
import dict
import entity
import int
import key_fn
import limit
import list
import offset
import prefix
import self
import str
import tuple

T = TypeVar("T")


class BaseInMemoryRepository(Generic[T]):
    """A simple, generic in-memory repository.

    Notes:
        - Not thread-safe.
        - No persistence across process restarts.
    """

    def __init__(self, key_fn: Callable[[T], str] | None = None) -> None:
        """Initialize repository.

        Args:
            key_fn: Optional function to extract the string id from an entity.
                    If not provided, manual create_with_id must be used.
        """
        self._store: dict[str, T] = {}
        self._counter: int = 0
        self._key_fn = key_fn

    def _next_id(self, prefix: str = "item") -> str:
        self._counter += 1
        return f"{prefix}_{self._counter}"

    async def get_by_id(self, entity_id: str) -> T | None:
        return self._store.get(entity_id)

    async def create_with_id(self, entity_id: str, entity: T) -> T:
        self._store[entity_id] = entity
        return entity

    async def create(self, entity: T) -> tuple[str, T]:
        """Create an entity, inferring id via key_fn or auto id.

        Returns:
            A tuple of (entity_id, entity)
        """
        if self._key_fn is not None:
            entity_id = self._key_fn(entity)
        else:
            entity_id = self._next_id()
        self._store[entity_id] = entity
        return entity_id, entity

    async def update_by_id(self, entity_id: str, entity: T) -> T:
        """Update an existing entity by id.

        Args:
            entity_id: The string identifier of the entity.
            entity: The entity to store.

        Returns:
            The stored entity.
        """

        return await self.create_with_id(entity_id, entity)

    async def list_all(self) -> list[T]:
        return list(self._store.values())

    async def list_paginated(self, limit: int = 100, offset: int = 0) -> list[T]:
        items = list(self._store.values())
        return items[offset : offset + limit]

    async def delete_by_id(self, entity_id: str) -> bool:
        return self._store.pop(entity_id, None) is not None

    async def exists(self, entity_id: str) -> bool:
        return entity_id in self._store
