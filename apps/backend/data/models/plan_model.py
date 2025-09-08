"""Plan model for AI agent planning and task management."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from apps.backend.data.models.base import Base
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Constants
CASCADE = "CASCADE"
SET_NULL = "SET NULL"

# Table name constants
PLANS_TABLE = "plans.id"
TASKS_TABLE = "tasks.id"

# Plan type constants
PLAN_GOAL_ORIENTED = "goal_oriented"
PLAN_REACTIVE = "reactive"
PLAN_HIERARCHICAL = "hierarchical"
PLAN_TEMPORAL = "temporal"
PLAN_RESOURCE_BASED = "resource_based"

# Plan status constants
STATUS_DRAFT = "draft"
STATUS_ACTIVE = "active"
STATUS_PAUSED = "paused"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_CANCELLED = "cancelled"

# Task status constants
TASK_PENDING = "pending"
TASK_IN_PROGRESS = "in_progress"
TASK_BLOCKED = "blocked"
TASK_COMPLETED = "completed"
TASK_FAILED = "failed"
TASK_SKIPPED = "skipped"

# Task priority constants
PRIORITY_LOW = 1
PRIORITY_NORMAL = 5
PRIORITY_HIGH = 8
PRIORITY_CRITICAL = 10

# Execution strategy constants
STRATEGY_SEQUENTIAL = "sequential"
STRATEGY_PARALLEL = "parallel"
STRATEGY_CONDITIONAL = "conditional"
STRATEGY_ADAPTIVE = "adaptive"


class Plan(Base):
    """
import abs
import agent_id
import all
import bool
import completed_task_ids
import criterion
import default
import dep_id
import description
import dict
import event_data
import event_type
import float
import include_logs
import include_tasks
import int
import key
import kwargs
import len
import list
import max
import min
import name
import objective
import parent_plan_id
import percentage
import plan_id
import plan_type
import reason
import result
import self
import sorted
import str
import success
import sum
import super
import t
import tag
import task_id
import task_type
import template_id
import time
import tool
import value
    Plan model for AI agent planning and execution management.

    Represents a comprehensive plan that can contain multiple tasks,
    dependencies, resources, and execution strategies.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "plans"

    # Plan identification
    agent_id: Mapped[UUID] = mapped_column(
        ForeignKey("agents.id", ondelete=CASCADE), nullable=False
    )
    plan_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=PLAN_GOAL_ORIENTED
    )

    # Plan content
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    objective: Mapped[str] = mapped_column(Text, nullable=False)

    # Plan classification
    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general"
    )
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Plan hierarchy
    parent_plan_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(PLANS_TABLE, ondelete=SET_NULL), nullable=True
    )
    is_template: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    template_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(PLANS_TABLE, ondelete=SET_NULL), nullable=True
    )

    # Planning metadata
    planning_strategy: Mapped[str] = mapped_column(
        String(50), nullable=False, default="forward_chaining"
    )
    execution_strategy: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STRATEGY_SEQUENTIAL
    )
    replanning_threshold: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.3
    )

    # Status and progress
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=STATUS_DRAFT
    )
    progress_percentage: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    completion_estimate: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Hours

    # Temporal information
    planned_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    planned_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Priority and importance
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=PRIORITY_NORMAL
    )
    importance_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    urgency_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)

    # Success criteria
    success_criteria: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    success_threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    quality_metrics: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Resources and constraints
    required_resources: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    resource_constraints: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    time_constraints: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Risk and contingency
    risk_assessment: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    contingency_plans: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False, default=[]
    )
    fallback_strategy: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Execution context
    execution_context: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    environment_requirements: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Monitoring and feedback
    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    feedback_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )
    adaptive_replanning: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Version control
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    previous_version_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(PLANS_TABLE, ondelete=SET_NULL), nullable=True
    )

    # Plan metadata
    plan_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    execution_logs: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False, default=[]
    )

    # Relationships
    # agent: Mapped["Agent"] = relationship("Agent", back_populates="plans")  # TODO: Add when Agent model exists
    parent_plan: Mapped[Plan | None] = relationship(
        "Plan",
        remote_side="Plan.id",
        back_populates="child_plans",
        foreign_keys=[parent_plan_id],
    )
    child_plans: Mapped[list[Plan]] = relationship(
        "Plan",
        back_populates="parent_plan",
        foreign_keys=lambda: [Plan.parent_plan_id],
    )
    template_plan: Mapped[Plan | None] = relationship(
        "Plan",
        remote_side="Plan.id",
        foreign_keys=[template_id],
    )
    tasks: Mapped[list[Task]] = relationship(
        "Task",
        back_populates="plan",
        cascade="all, delete-orphan",
        order_by="Task.order_index",
    )

    def __init__(
        self,
        agent_id: UUID,
        name: str,
        objective: str,
        plan_type: str = PLAN_GOAL_ORIENTED,
        **kwargs: Any,
    ) -> None:
        """
        Initialize plan.

        Args:
            agent_id: ID of the agent owning this plan
            name: Plan name
            objective: Plan objective
            plan_type: Type of plan
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.name = name
        self.objective = objective
        self.plan_type = plan_type

    def start_execution(self) -> None:
        """Start plan execution."""
        self.status = STATUS_ACTIVE
        self.actual_start = datetime.now(UTC)
        self.log_execution_event(
            "plan_started", {"timestamp": self.actual_start.isoformat()}
        )

    def pause_execution(self) -> None:
        """Pause plan execution."""
        if self.status == STATUS_ACTIVE:
            self.status = STATUS_PAUSED
            self.log_execution_event(
                "plan_paused", {"timestamp": datetime.now(UTC).isoformat()}
            )

    def resume_execution(self) -> None:
        """Resume plan execution."""
        if self.status == STATUS_PAUSED:
            self.status = STATUS_ACTIVE
            self.log_execution_event(
                "plan_resumed", {"timestamp": datetime.now(UTC).isoformat()}
            )

    def complete_execution(self, success: bool = True) -> None:
        """Complete plan execution."""
        self.status = STATUS_COMPLETED if success else STATUS_FAILED
        self.actual_end = datetime.now(UTC)
        self.progress_percentage = 100.0 if success else self.progress_percentage
        self.log_execution_event(
            "plan_completed" if success else "plan_failed",
            {
                "timestamp": self.actual_end.isoformat(),
                "success": success,
                "final_progress": self.progress_percentage,
            },
        )

    def cancel_execution(self, reason: str | None = None) -> None:
        """Cancel plan execution."""
        self.status = STATUS_CANCELLED
        self.actual_end = datetime.now(UTC)
        self.log_execution_event(
            "plan_cancelled",
            {
                "timestamp": self.actual_end.isoformat(),
                "reason": reason,
                "progress_at_cancellation": self.progress_percentage,
            },
        )

    def update_progress(self) -> None:
        """Update plan progress based on task completion."""
        if not self.tasks:
            return

        completed_tasks = sum(1 for task in self.tasks if task.is_completed())
        total_tasks = len(self.tasks)

        if total_tasks > 0:
            self.progress_percentage = (completed_tasks / total_tasks) * 100.0

        # Check if plan is complete
        if self.progress_percentage >= 100.0 and self.status == STATUS_ACTIVE:
            self.complete_execution(success=True)

    def calculate_priority_score(self) -> float:
        """Calculate overall priority score combining priority, importance, and urgency."""
        # Normalize priority to 0-1 scale
        priority_normalized = self.priority / 10.0

        # Weighted combination
        return (
            (priority_normalized * 0.4)
            + (self.importance_score * 0.3)
            + (self.urgency_score * 0.3)
        )

    def add_task(
        self,
        name: str,
        description: str | None = None,
        task_type: str = "action",
        **kwargs: Any,
    ) -> Task:
        """Add a new task to the plan."""
        order_index = len(self.tasks) if self.tasks else 0

        task = Task(
            plan_id=self.id,
            name=name,
            description=description,
            task_type=task_type,
            order_index=order_index,
            **kwargs,
        )

        if self.tasks is None:
            self.tasks = []
        self.tasks.append(task)

        return task

    def get_next_task(self) -> Task | None:
        """Get the next task to execute."""
        if not self.tasks:
            return None

        # Find first pending or in-progress task
        for task in sorted(self.tasks, key=lambda t: t.order_index):
            if task.status in [TASK_PENDING, TASK_IN_PROGRESS]:
                return task

        return None

    def get_blocked_tasks(self) -> list[Task]:
        """Get list of blocked tasks."""
        return [task for task in self.tasks if task.status == TASK_BLOCKED]

    def get_completed_tasks(self) -> list[Task]:
        """Get list of completed tasks."""
        return [task for task in self.tasks if task.is_completed()]

    def can_start(self) -> bool:
        """Check if plan can be started."""
        return self.status == STATUS_DRAFT and bool(self.tasks)

    def should_replan(self) -> bool:
        """Check if plan should be replanned based on threshold."""
        if not self.adaptive_replanning:
            return False

        # Calculate deviation from expected progress
        if self.planned_start and self.planned_end:
            total_duration = (self.planned_end - self.planned_start).total_seconds()
            elapsed_time = (
                (datetime.now(UTC) - self.actual_start).total_seconds()
                if self.actual_start
                else 0
            )

            expected_progress = (
                (elapsed_time / total_duration) * 100.0 if total_duration > 0 else 0
            )
            progress_deviation = (
                abs(expected_progress - self.progress_percentage) / 100.0
            )

            return progress_deviation > self.replanning_threshold

        return False

    def estimate_completion_time(self) -> float | None:
        """Estimate remaining completion time in hours."""
        if not self.tasks or self.progress_percentage >= 100.0:
            return 0.0

        # Simple estimation based on average task completion time
        completed_tasks = self.get_completed_tasks()
        if not completed_tasks:
            return None

        # Filter out None values and calculate sum
        valid_times = [
            time
            for time in [task.get_execution_time() for task in completed_tasks]
            if time is not None
        ]

        if not valid_times:
            return None

        total_completed_time = sum(valid_times)
        avg_task_time = total_completed_time / len(completed_tasks)
        remaining_tasks = len(self.tasks) - len(completed_tasks)

        return remaining_tasks * avg_task_time

    def add_tag(self, tag: str) -> None:
        """Add tag to plan."""
        if self.tags is None:
            self.tags = []
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove tag from plan."""
        if self.tags and tag in self.tags:
            self.tags.remove(tag)

    def set_success_criterion(self, name: str, criterion: Any) -> None:
        """Set success criterion."""
        if self.success_criteria is None:
            self.success_criteria = {}
        self.success_criteria[name] = criterion

    def get_success_criterion(self, name: str, default: Any = None) -> Any:
        """Get success criterion."""
        return (
            self.success_criteria.get(name, default)
            if self.success_criteria
            else default
        )

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        if self.plan_metadata is None:
            self.plan_metadata = {}
        self.plan_metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.plan_metadata.get(key, default) if self.plan_metadata else default

    def log_execution_event(self, event_type: str, event_data: dict[str, Any]) -> None:
        """Log execution event."""
        if self.execution_logs is None:
            self.execution_logs = []

        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "data": event_data,
        }

        self.execution_logs.append(event)

    def is_active(self) -> bool:
        """Check if plan is active."""
        return self.status == STATUS_ACTIVE

    def is_completed(self) -> bool:
        """Check if plan is completed."""
        return self.status == STATUS_COMPLETED

    def is_failed(self) -> bool:
        """Check if plan has failed."""
        return self.status == STATUS_FAILED

    def is_overdue(self) -> bool:
        """Check if plan is overdue."""
        if not self.planned_end or self.is_completed():
            return False
        return datetime.now(UTC) > self.planned_end

    def to_dict(
        self, include_tasks: bool = False, include_logs: bool = False
    ) -> dict[str, Any]:
        """
        Convert plan to dictionary.

        Args:
            include_tasks: Whether to include task details
            include_logs: Whether to include execution logs

        Returns:
            Dictionary representation of the plan
        """
        _ = {
            "id": str(self.id),
            "agent_id": str(self.agent_id),
            "name": self.name,
            "description": self.description,
            "objective": self.objective,
            "plan_type": self.plan_type,
            "category": self.category,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "priority": self.priority,
            "priority_score": self.calculate_priority_score(),
            "importance_score": self.importance_score,
            "urgency_score": self.urgency_score,
            "planning_strategy": self.planning_strategy,
            "execution_strategy": self.execution_strategy,
            "is_template": self.is_template,
            "version": self.version,
            "tags": self.tags,
            "success_criteria": self.success_criteria,
            "success_threshold": self.success_threshold,
            "completion_estimate": self.completion_estimate,
            "estimated_remaining_time": self.estimate_completion_time(),
            "planned_start": self.planned_start.isoformat()
            if self.planned_start
            else None,
            "planned_end": self.planned_end.isoformat() if self.planned_end else None,
            "actual_start": self.actual_start.isoformat()
            if self.actual_start
            else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_tasks and self.tasks:
            result["tasks"] = [task.to_dict() for task in self.tasks]
            result["task_count"] = len(self.tasks)
            result["completed_task_count"] = len(self.get_completed_tasks())
            result["blocked_task_count"] = len(self.get_blocked_tasks())

        if include_logs and self.execution_logs:
            result["execution_logs"] = self.execution_logs

        return result

    def __repr__(self) -> str:
        """String representation of plan."""
        return f"<Plan(id={self.id}, name='{self.name}', status={self.status}, progress={self.progress_percentage:.1f}%)>"


class Task(Base):
    """
    Task model for individual tasks within plans.

    Represents atomic units of work that can be executed,
    monitored, and tracked within the context of a plan.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        return "tasks"

    # Task identification
    plan_id: Mapped[UUID] = mapped_column(
        ForeignKey(PLANS_TABLE, ondelete=CASCADE), nullable=False
    )
    task_type: Mapped[str] = mapped_column(String(50), nullable=False, default="action")

    # Task content
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Task classification
    category: Mapped[str] = mapped_column(
        String(100), nullable=False, default="general"
    )
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Task hierarchy and dependencies
    parent_task_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(TASKS_TABLE, ondelete=SET_NULL), nullable=True
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    dependencies: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=[]
    )  # Task IDs

    # Status and progress
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=TASK_PENDING
    )
    progress_percentage: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )

    # Priority and effort
    priority: Mapped[int] = mapped_column(
        Integer, nullable=False, default=PRIORITY_NORMAL
    )
    estimated_effort: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Hours
    actual_effort: Mapped[float | None] = mapped_column(Float, nullable=True)  # Hours

    # Temporal information
    planned_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    planned_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_start: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Execution details
    execution_method: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # manual, automated, ai_agent
    execution_context: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    required_tools: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=[])

    # Results and feedback
    result: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_data: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Error handling
    max_retries: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Resource requirements
    required_resources: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    allocated_resources: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )

    # Validation and success criteria
    validation_criteria: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    success_threshold: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)

    # Monitoring
    checkpoint_data: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    monitoring_enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Task metadata
    task_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False, default={}
    )
    execution_logs: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, nullable=False, default=[]
    )

    # Relationships
    plan: Mapped[Plan] = relationship("Plan", back_populates="tasks")
    parent_task: Mapped[Task | None] = relationship(
        "Task", remote_side="Task.id", back_populates="subtasks"
    )
    subtasks: Mapped[list[Task]] = relationship("Task", back_populates="parent_task")

    def __init__(
        self,
        plan_id: UUID,
        name: str,
        task_type: str = "action",
        order_index: int = 0,
        **kwargs: Any,
    ) -> None:
        """
        Initialize task.

        Args:
            plan_id: ID of the parent plan
            name: Task name
            task_type: Type of task
            order_index: Order in execution sequence
            **kwargs: Additional model arguments
        """
        super().__init__(**kwargs)
        self.plan_id = plan_id
        self.name = name
        self.task_type = task_type
        self.order_index = order_index

    def start_execution(self) -> None:
        """Start task execution."""
        self.status = TASK_IN_PROGRESS
        start_time = datetime.now(UTC)
        self.actual_start = start_time
        self.log_execution_event("task_started", {"timestamp": start_time.isoformat()})

    def complete_execution(
        self, success: bool = True, result: str | None = None
    ) -> None:
        """Complete task execution."""
        self.status = TASK_COMPLETED if success else TASK_FAILED
        end_time = datetime.now(UTC)
        self.actual_end = end_time
        self.progress_percentage = 100.0 if success else self.progress_percentage

        if result:
            self._ = result

        # Calculate actual effort
        if self.actual_start:
            duration = (end_time - self.actual_start).total_seconds() / 3600  # Hours
            self.actual_effort = duration

        self.log_execution_event(
            "task_completed" if success else "task_failed",
            {
                "timestamp": end_time.isoformat(),
                "success": success,
                "result": result,
                "effort": self.actual_effort,
            },
        )

    def block_execution(self, reason: str) -> None:
        """Block task execution."""
        self.status = TASK_BLOCKED
        self.error_message = reason
        self.log_execution_event(
            "task_blocked",
            {"reason": reason, "timestamp": datetime.now(UTC).isoformat()},
        )

    def retry_execution(self) -> bool:
        """Retry task execution if retries available."""
        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.status = TASK_PENDING
            self.error_message = None
            self.log_execution_event(
                "task_retry",
                {
                    "retry_count": self.retry_count,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )
            return True
        return False

    def skip_execution(self, reason: str) -> None:
        """Skip task execution."""
        self.status = TASK_SKIPPED
        end_time = datetime.now(UTC)
        self.actual_end = end_time
        self.log_execution_event(
            "task_skipped", {"reason": reason, "timestamp": end_time.isoformat()}
        )

    def update_progress(self, percentage: float) -> None:
        """Update task progress."""
        self.progress_percentage = max(0.0, min(100.0, percentage))

        if self.progress_percentage >= 100.0 and self.status == TASK_IN_PROGRESS:
            self.complete_execution(success=True)

    def add_dependency(self, task_id: str) -> None:
        """Add task dependency."""
        if self.dependencies is None:
            self.dependencies = []
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)

    def remove_dependency(self, task_id: str) -> None:
        """Remove task dependency."""
        if self.dependencies and task_id in self.dependencies:
            self.dependencies.remove(task_id)

    def can_start(self, completed_task_ids: list[str]) -> bool:
        """Check if task can start based on dependencies."""
        if self.status != TASK_PENDING:
            return False

        # Check if all dependencies are completed
        if self.dependencies:
            return all(dep_id in completed_task_ids for dep_id in self.dependencies)

        return True

    def get_execution_time(self) -> float | None:
        """Get actual execution time in hours."""
        if self.actual_start and self.actual_end:
            duration = (self.actual_end - self.actual_start).total_seconds() / 3600
            return duration
        return None

    def set_validation_criterion(self, name: str, criterion: Any) -> None:
        """Set validation criterion."""
        if self.validation_criteria is None:
            self.validation_criteria = {}
        self.validation_criteria[name] = criterion

    def get_validation_criterion(self, name: str, default: Any = None) -> Any:
        """Get validation criterion."""
        return (
            self.validation_criteria.get(name, default)
            if self.validation_criteria
            else default
        )

    def add_required_tool(self, tool: str) -> None:
        """Add required tool."""
        if self.required_tools is None:
            self.required_tools = []
        if tool not in self.required_tools:
            self.required_tools.append(tool)

    def set_execution_context(self, key: str, value: Any) -> None:
        """Set execution context value."""
        if self.execution_context is None:
            self.execution_context = {}
        self.execution_context[key] = value

    def get_execution_context(self, key: str, default: Any = None) -> Any:
        """Get execution context value."""
        return (
            self.execution_context.get(key, default)
            if self.execution_context
            else default
        )

    def set_result_data(self, key: str, value: Any) -> None:
        """Set result data."""
        if self.result_data is None:
            self.result_data = {}
        self.result_data[key] = value

    def get_result_data(self, key: str, default: Any = None) -> Any:
        """Get result data."""
        return self.result_data.get(key, default) if self.result_data else default

    def log_execution_event(self, event_type: str, event_data: dict[str, Any]) -> None:
        """Log execution event."""
        if self.execution_logs is None:
            self.execution_logs = []

        event = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            "data": event_data,
        }

        self.execution_logs.append(event)

    def is_pending(self) -> bool:
        """Check if task is pending."""
        return self.status == TASK_PENDING

    def is_in_progress(self) -> bool:
        """Check if task is in progress."""
        return self.status == TASK_IN_PROGRESS

    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == TASK_COMPLETED

    def is_failed(self) -> bool:
        """Check if task has failed."""
        return self.status == TASK_FAILED

    def is_blocked(self) -> bool:
        """Check if task is blocked."""
        return self.status == TASK_BLOCKED

    def is_skipped(self) -> bool:
        """Check if task was skipped."""
        return self.status == TASK_SKIPPED

    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.planned_end or self.is_completed():
            return False
        return datetime.now(UTC) > self.planned_end

    def to_dict(self, include_logs: bool = False) -> dict[str, Any]:
        """
        Convert task to dictionary.

        Args:
            include_logs: Whether to include execution logs

        Returns:
            Dictionary representation of the task
        """
        _ = {
            "id": str(self.id),
            "plan_id": str(self.plan_id),
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "task_type": self.task_type,
            "category": self.category,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "priority": self.priority,
            "order_index": self.order_index,
            "estimated_effort": self.estimated_effort,
            "actual_effort": self.actual_effort,
            "execution_time": self.get_execution_time(),
            "quality_score": self.quality_score,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "error_message": self.error_message,
            "success_threshold": self.success_threshold,
            "execution_method": self.execution_method,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "required_tools": self.required_tools,
            "validation_criteria": self.validation_criteria,
            "result": self.result,
            "result_data": self.result_data,
            "planned_start": self.planned_start.isoformat()
            if self.planned_start
            else None,
            "planned_end": self.planned_end.isoformat() if self.planned_end else None,
            "actual_start": self.actual_start.isoformat()
            if self.actual_start
            else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_logs and self.execution_logs:
            result["execution_logs"] = self.execution_logs

        return result

    def __repr__(self) -> str:
        """String representation of task."""
        return f"<Task(id={self.id}, name='{self.name}', status={self.status}, progress={self.progress_percentage:.1f}%)>"
