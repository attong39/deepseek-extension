from __future__ import annotations

import strawberry
import list
import name
import str

"""GraphQL schema for memory domain."""


@strawberry.type
class MemoryType:
    """GraphQL type for memory entity."""

    id: str
    name: str


@strawberry.type
class MemoryQuery:
    """GraphQL queries for memory domain."""

    @strawberry.field
    def list_memorys(self) -> list[MemoryType]:
        """List all memorys."""
        return []


@strawberry.type
class MemoryMutation:
    """GraphQL mutations for memory domain."""

    @strawberry.mutation
    def create_memory(self, name: str) -> MemoryType:
        """Create a new memory."""
        return MemoryType(id="1", name=name)


__all__ = [
    "MemoryMutation",
    "MemoryQuery",
    "MemoryType",
]
