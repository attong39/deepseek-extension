from __future__ import annotations

from datetime import UTC, datetime

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.aggregates.base import AggregateRoot, DomainEvent, ensure
import ValueError
import all
import context
import dict
import getattr
import list
import metadata
import name
import outputs
import reason
import s
import self
import step_id
import str


def utcnow():
    return datetime.now(UTC)


class WorkflowAggregate(AggregateRoot[DomainModel]):
    """
    Aggregate for orchestrating multi-step workflows (plans/runs).

    Lifecycle: create → start → (advance/fail)* → complete
    """

    AGG = "workflow"

    # commands
    def create(self, name: str, context: dict | None = None) -> None:
        ensure(name.strip() != "", "name required.")
        self._replace(name=name, status="created", context=context or {}, steps=[])
        self._record(DomainEvent.make("WorkflowCreated", self.AGG, self.id, name=name))

    def add_step(self, step_id: str, name: str, metadata: dict | None = None) -> None:
        current_steps = getattr(self.entity, "steps", []) or []
        steps: list[dict] = list(current_steps)
        ensure(all(s["id"] != step_id for s in steps), f"Step '{step_id}' exists.")
        steps.append(
            dict(id=step_id, name=name, status="pending", metadata=metadata or {})
        )
        self._replace(steps=steps)
        self._record(
            DomainEvent.make("WorkflowStepAdded", self.AGG, self.id, step_id=step_id)
        )

    def start(self) -> None:
        current_status = getattr(self.entity, "status", None)
        ensure(current_status in {None, "created"}, "Workflow not in creatable state.")
        self._replace(status="running", started_at=utcnow())
        self._record(DomainEvent.make("WorkflowStarted", self.AGG, self.id))

    def advance_step(self, step_id: str) -> None:
        current_steps = getattr(self.entity, "steps", []) or []
        steps = list(current_steps)
        for s in steps:
            if s["id"] == step_id:
                ensure(s["status"] in {"pending", "failed"}, "Step not startable.")
                s["status"] = "running"
                s["started_at"] = utcnow()
                self._replace(steps=steps)
                self._record(
                    DomainEvent.make(
                        "WorkflowStepRunning", self.AGG, self.id, step_id=step_id
                    )
                )
                return
        raise ValueError(f"Step '{step_id}' not found.")

    def complete_step(self, step_id: str, outputs: dict | None = None) -> None:
        current_steps = getattr(self.entity, "steps", []) or []
        steps = list(current_steps)
        for s in steps:
            if s["id"] == step_id:
                ensure(s["status"] == "running", "Step must be running to complete.")
                s["status"] = "done"
                s["ended_at"] = utcnow()
                if outputs:
                    s.setdefault("metadata", {}).update({"outputs": outputs})
                self._replace(steps=steps)
                self._record(
                    DomainEvent.make(
                        "WorkflowStepCompleted", self.AGG, self.id, step_id=step_id
                    )
                )
                return
        raise ValueError(f"Step '{step_id}' not found.")

    def fail_step(self, step_id: str, reason: str) -> None:
        current_steps = getattr(self.entity, "steps", []) or []
        steps = list(current_steps)
        for s in steps:
            if s["id"] == step_id:
                ensure(s["status"] in {"running", "pending"}, "Invalid step status.")
                s["status"] = "failed"
                s["ended_at"] = utcnow()
                s.setdefault("metadata", {}).update({"error": reason})
                self._replace(steps=steps)
                self._record(
                    DomainEvent.make(
                        "WorkflowStepFailed",
                        self.AGG,
                        self.id,
                        step_id=step_id,
                        reason=reason,
                    )
                )
                return
        raise ValueError(f"Step '{step_id}' not found.")

    def complete(self) -> None:
        current_status = getattr(self.entity, "status", None)
        current_steps = getattr(self.entity, "steps", []) or []
        ensure(current_status == "running", "Workflow must be running.")
        steps = list(current_steps)
        ensure(all(s["status"] == "done" for s in steps), "Not all steps completed.")
        self._replace(status="completed", ended_at=utcnow())
        self._record(DomainEvent.make("WorkflowCompleted", self.AGG, self.id))
