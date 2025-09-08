"""Automation interfaces for planning and execution.

This module defines the protocols for automation planning, execution,
and safety monitoring.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol
import bool
import str

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import (
        AutomationPlan,
        AutomationStep,
        ExecutionReport,
        SafetyConfig,
        SafetyResult,
        StepResult,
    )


class AutomationPlanner(Protocol):
    """Protocol for AI-driven automation planning."""

    async def create_plan(
        self, task_description: str, screenshot_path: str | None = None
    ) -> AutomationPlan:
        """Create an automation plan from a task description.

        Args:
            task_description: Natural language description of the task
            screenshot_path: Optional screenshot for context

        Returns:
            Generated automation plan
        """
        ...

    async def update_plan(
        self,
        plan: AutomationPlan,
        error_msg: str | None = None,
        success_msg: str | None = None,
    ) -> AutomationPlan:
        """Update a plan based on execution results.

        Args:
            plan: Current automation plan
            error_msg: Error message if step failed
            success_msg: Success message if step succeeded

        Returns:
            Updated automation plan
        """
        ...


class AutomationExecutor(Protocol):
    """Protocol for executing automation plans."""

    async def execute_step(self, step: AutomationStep) -> StepResult:
        """Execute a single automation step.

        Args:
            step: Step to execute

        Returns:
            Execution result
        """
        ...

    async def execute_plan(self, plan: AutomationPlan) -> ExecutionReport:
        """Execute a complete automation plan.

        Args:
            plan: Plan to execute

        Returns:
            Complete execution report
        """
        ...


class SafetyEngine(Protocol):
    """Protocol for automation safety monitoring."""

    async def check_safety(
        self, step: AutomationStep, config: SafetyConfig
    ) -> SafetyResult:
        """Check if a step is safe to execute.

        Args:
            step: Step to check
            config: Safety configuration

        Returns:
            Safety check result
        """
        ...

    async def is_allowed_action(
        self, action_type: str, target: str | None = None
    ) -> bool:
        """Check if an action type is allowed.

        Args:
            action_type: Type of action to check
            target: Optional target (file path, URL, etc.)

        Returns:
            True if action is allowed
        """
        ...
