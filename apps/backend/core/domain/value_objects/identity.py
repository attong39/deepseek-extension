"""
Identity Value Objects - UUID-based strong typing.

Cung cấp type-safe identities cho các domain entities.
Mỗi ID có type riêng để tránh nhầm lẫn (Agent ID != User ID).
"""

from __future__ import annotations

from uuid import UUID, uuid4

from app._base_model import DomainModel
from pydantic import Field
import hash
import int
import self
import str


class AgentId(DomainModel):
    """
    Strongly-typed identifier cho Agent entities.

    Đảm bảo type safety và tránh truyền nhầm ID types.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Agent"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class UserId(DomainModel):
    """
    Strongly-typed identifier cho User entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho User"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class MemoryId(DomainModel):
    """
    Strongly-typed identifier cho Memory entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Memory"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class PlanId(DomainModel):
    """
    Strongly-typed identifier cho Plan entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Plan"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class TaskId(DomainModel):
    """
    Strongly-typed identifier cho Task entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Task"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class ConversationId(DomainModel):
    """
    Strongly-typed identifier cho Conversation entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Conversation"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


class SessionId(DomainModel):
    """
    Strongly-typed identifier cho Session entities.
    """

    value: UUID = Field(
        default_factory=uuid4, description="UUID unique identifier cho Session"
    )

    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(self.value)


__all__ = [
    "AgentId",
    "UserId",
    "MemoryId",
    "PlanId",
    "TaskId",
    "ConversationId",
    "SessionId",
]
