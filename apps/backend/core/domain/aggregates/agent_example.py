"""
Example Agent Aggregate using composition events pattern
"""

from __future__ import annotations

from apps.backend.core.domain.aggregates.base import AggregateRoot
from apps.backend.core.domain.events.base import make_event
from apps.backend.core.domain.events.types import AgentActivated, AgentCreated
import ValueError
import agent_id
import classmethod
import cls
import list
import name
import self
import str
import tag
import tags


class AgentAggregate(AggregateRoot):
    """Agent aggregate với event composition pattern."""

    name: str
    status: str = "INACTIVE"
    tags: list[str] = []

    @classmethod
    def create(
        cls, agent_id: str, name: str, tags: list[str] | None = None
    ) -> AgentAggregate:
        """Tạo agent mới và phát AgentCreated event."""
        agg = cls(id=agent_id, name=name, tags=tags or [], version=0)

        # Tạo event bằng composition thay vì inheritance
        ev = make_event(
            "AgentCreated", AgentCreated(agent_id=agent_id, name=name, tags=tags or [])
        )
        agg._raise(ev)
        return agg

    def activate(self) -> AgentAggregate:
        """Activate agent và phát AgentActivated event."""
        if self.status == "ACTIVE":
            raise ValueError("Agent already active")

        # Tạo bản sao mới với status updated (immutability)
        updated = self.model_copy(
            update={"status": "ACTIVE", "version": self._next_version()}
        )

        # Raise event
        ev = make_event("AgentActivated", AgentActivated(agent_id=self.id))
        updated._raise(ev)

        return updated

    def add_tag(self, tag: str) -> AgentAggregate:
        """Thêm tag mới."""
        if tag in self.tags:
            return self  # No change

        new_tags = [*self.tags, tag]
        return self.model_copy(
            update={"tags": new_tags, "version": self._next_version()}
        )


__all__ = ["AgentAggregate"]
