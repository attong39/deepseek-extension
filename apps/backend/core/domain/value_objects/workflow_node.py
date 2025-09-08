"""Workflow Node Value Object - ZETA AI Server.

Value object cho workflow node trong DAG (Directed Acyclic Graph).
Immutable, lightweight, và pure domain concept.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any
import ValueError
import bool
import dict
import int
import len
import list
import outputs
import self
import status
import str

if TYPE_CHECKING:
    from uuid import UUID


class NodeType(str, Enum):
    """Node type trong workflow DAG."""

    TASK = "task"
    DECISION = "decision"
    PARALLEL = "parallel"
    MERGE = "merge"
    START = "start"
    END = "end"
    DELAY = "delay"
    LOOP = "loop"


class NodeStatus(str, Enum):
    """Status của workflow node."""

    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class WorkflowNodeVO:
    """
    Value Object cho workflow node trong DAG system.

    Responsibility:
    - Định nghĩa node trong workflow graph
    - Chứa cấu hình và dependencies
    - Immutable và pure value

    Quan hệ:
    - Thuộc về Workflow entity
    - Có thể reference Task entity qua task_id
    - Kết nối với các nodes khác qua edges
    """

    # Core identification
    id: UUID
    name: str
    description: str | None = None

    # Node definition
    node_type: NodeType = NodeType.TASK
    status: NodeStatus = NodeStatus.PENDING

    # Task reference (if applicable)
    task_id: UUID | None = None
    task_type: str | None = None

    # Configuration
    config: dict[str, Any] | None = None
    inputs: dict[str, Any] | None = None
    outputs: dict[str, Any] | None = None

    # Dependencies & flow
    depends_on: list[UUID] | None = None
    condition: str | None = None  # Conditional logic
    timeout_seconds: int = 300

    # Retry configuration
    max_retries: int = 3
    retry_delay_seconds: int = 60

    # Metadata
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        """Validate node invariants."""
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("WorkflowNode phải có name")

        if len(self.name) > 100:
            raise ValueError("WorkflowNode name không được vượt quá 100 ký tự")

        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds phải > 0")

        if self.max_retries < 0:
            raise ValueError("max_retries phải >= 0")

        if self.retry_delay_seconds < 0:
            raise ValueError("retry_delay_seconds phải >= 0")

    def is_ready(self) -> bool:
        """Check if node is ready for execution."""
        return self.status == NodeStatus.READY

    def is_terminal(self) -> bool:
        """Check if node is terminal (end/completed/failed)."""
        return (
            self.status
            in {
                NodeStatus.COMPLETED,
                NodeStatus.FAILED,
                NodeStatus.CANCELLED,
            }
            or self.node_type == NodeType.END
        )

    def has_dependencies(self) -> bool:
        """Check if node has dependencies."""
        return bool(self.depends_on)

    def has_condition(self) -> bool:
        """Check if node has conditional logic."""
        return bool(self.condition)

    def is_task_node(self) -> bool:
        """Check if this is a task execution node."""
        return self.node_type == NodeType.TASK and self.task_id is not None

    def with_status(self, status: NodeStatus) -> WorkflowNodeVO:
        """Create new instance with updated status."""
        return WorkflowNodeVO(
            id=self.id,
            name=self.name,
            description=self.description,
            node_type=self.node_type,
            status=status,
            task_id=self.task_id,
            task_type=self.task_type,
            config=self.config,
            inputs=self.inputs,
            outputs=self.outputs,
            depends_on=self.depends_on,
            condition=self.condition,
            timeout_seconds=self.timeout_seconds,
            max_retries=self.max_retries,
            retry_delay_seconds=self.retry_delay_seconds,
            tags=self.tags,
            metadata=self.metadata,
        )

    def with_outputs(self, outputs: dict[str, Any]) -> WorkflowNodeVO:
        """Create new instance with updated outputs."""
        merged_outputs = {**(self.outputs or {}), **outputs}
        return WorkflowNodeVO(
            id=self.id,
            name=self.name,
            description=self.description,
            node_type=self.node_type,
            status=self.status,
            task_id=self.task_id,
            task_type=self.task_type,
            config=self.config,
            inputs=self.inputs,
            outputs=merged_outputs,
            depends_on=self.depends_on,
            condition=self.condition,
            timeout_seconds=self.timeout_seconds,
            max_retries=self.max_retries,
            retry_delay_seconds=self.retry_delay_seconds,
            tags=self.tags,
            metadata=self.metadata,
        )
