"""Agent domain specifications (placeholder)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.backend.core.domain.entities.agent import Agent


class Specification(ABC):
    """Base specification interface."""
import agent
import bool
import list
import object
import required_capabilities
import self
import status
import str

    @abstractmethod
    def is_satisfied_by(self, candidate: object) -> bool:
        """Check if specification is satisfied."""


class AgentCapabilitySpecification(Specification):
    """Specification cho Agent capabilities."""

    def __init__(self, required_capabilities: list[str]):
        self.required_capabilities = required_capabilities

    def is_satisfied_by(self, agent: Agent) -> bool:
        return agent.require(*self.required_capabilities)


class AgentStatusSpecification(Specification):
    """Specification cho Agent status."""

    def __init__(self, status: str):
        self.status = status

    def is_satisfied_by(self, agent: Agent) -> bool:
        return agent.status.value == self.status
