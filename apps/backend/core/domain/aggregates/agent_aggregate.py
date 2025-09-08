from __future__ import annotations

from typing import Any, ClassVar

from apps.backend.core.domain.aggregates.base import AggregateRoot, DomainEvent, ensure
import cap
import config_updates
import dataset_id
import dict
import getattr
import list
import params
import reason
import self
import str


class AgentAggregate(AggregateRoot):
    """
    Aggregate for AI Agent lifecycle + capabilities/config.

    Invariants:
    - name non-empty
    - status transitions must be valid
    """

    AGG: ClassVar[str] = "agent"

    # -------- commands --------
    def activate(self) -> None:
        current_status = getattr(self.entity, "status", None)
        ensure(current_status != "ACTIVE", "Agent already active.")
        self._replace(status="ACTIVE")
        self._record(DomainEvent.make("AgentActivated", self.AGG, self.id))

    def deactivate(self) -> None:
        current_status = getattr(self.entity, "status", None)
        ensure(current_status != "INACTIVE", "Agent already inactive.")
        self._replace(status="INACTIVE")
        self._record(DomainEvent.make("AgentDeactivated", self.AGG, self.id))

    def start_training(
        self, dataset_id: str, params: dict[str, Any] | None = None
    ) -> None:
        current_status = getattr(self.entity, "status", None)
        ensure(current_status != "TRAINING", "Agent is already training.")
        self._replace(status="TRAINING")
        self._record(
            DomainEvent.make(
                "AgentTrainingStarted",
                self.AGG,
                self.id,
                dataset_id=dataset_id,
                params=params or {},
            )
        )

    def mark_error(self, reason: str) -> None:
        self._replace(status="ERROR")
        self._record(DomainEvent.make("AgentErrored", self.AGG, self.id, reason=reason))

    def update_config(self, config_updates: dict[str, Any]) -> None:
        current_config = getattr(self.entity, "configuration", {}) or {}
        merged = {**current_config, **(config_updates or {})}
        self._replace(configuration=merged)
        self._record(
            DomainEvent.make(
                "AgentConfigUpdated",
                self.AGG,
                self.id,
                keys=list(config_updates.keys()),
            )
        )

    def add_capability(self, cap: str) -> None:
        current_caps = getattr(self.entity, "capabilities", []) or []
        caps = list(current_caps)
        ensure(cap not in caps, f"Capability '{cap}' already exists.")
        caps.append(cap)
        self._replace(capabilities=caps)
        self._record(
            DomainEvent.make("AgentCapabilityAdded", self.AGG, self.id, capability=cap)
        )

    def remove_capability(self, cap: str) -> None:
        current_caps = getattr(self.entity, "capabilities", []) or []
        caps = list(current_caps)
        ensure(cap in caps, f"Capability '{cap}' not found.")
        caps.remove(cap)
        self._replace(capabilities=caps)
        self._record(
            DomainEvent.make(
                "AgentCapabilityRemoved", self.AGG, self.id, capability=cap
            )
        )
