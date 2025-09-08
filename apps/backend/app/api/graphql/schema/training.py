from __future__ import annotations

import strawberry
import list
import name
import str

"""GraphQL schema for training domain."""


@strawberry.type
class TrainingType:
    """GraphQL type for training entity."""

    id: str
    name: str


@strawberry.type
class TrainingQuery:
    """GraphQL queries for training domain."""

    @strawberry.field
    def list_trainings(self) -> list[TrainingType]:
        """List all trainings."""
        return []


@strawberry.type
class TrainingMutation:
    """GraphQL mutations for training domain."""

    @strawberry.mutation
    def create_training(self, name: str) -> TrainingType:
        """Create a new training."""
        return TrainingType(id="1", name=name)


__all__ = [
    "TrainingMutation",
    "TrainingQuery",
    "TrainingType",
]
