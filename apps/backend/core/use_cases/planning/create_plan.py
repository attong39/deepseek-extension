"""
Planning Use Cases - ZETA AI SERVER
==================================
"""

from datetime import UTC, datetime
from typing import Any

from apps.backend.core.domain.entities.plan import Plan, PlanStatus, PlanStep
from apps.backend.core.interfaces.repositories import PlanRepository
import ValueError
import agent_id
import description
import dict
import enumerate
import i
import list
import plan_id
import plan_repo
import result
import self
import step_data
import steps_data
import str
import title
import user_id


class CreatePlan:
    """Use case for creating execution plans."""

    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    async def __call__(
        self,
        title: str,
        description: str,
        agent_id: str,
        user_id: str,
        steps_data: list[dict[str, Any]],
    ) -> Plan:
        """Create new execution plan."""

        # Create plan steps
        steps = []
        for i, step_data in enumerate(steps_data):
            step = PlanStep(
                id=f"step_{i + 1}",
                action=step_data["action"],
                description=step_data["description"],
                parameters=step_data.get("parameters", {}),
                order=i + 1,
            )
            steps.append(step)

        # Create plan
        plan = Plan(
            id="",  # Will be set by repository
            title=title,
            description=description,
            agent_id=agent_id,
            user_id=user_id,
            steps=steps,
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        # Save plan
        created_plan = await self.plan_repo.create(plan)
        return created_plan


class ExecutePlan:
    """Use case for executing plans step by step."""

    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    async def __call__(self, plan_id: str) -> Plan:
        """Start plan execution."""
        plan = await self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} not found")

        # Update status to executing
        plan.status = PlanStatus.EXECUTING
        plan.updated_at = datetime.now(UTC)

        await self.plan_repo.update(plan)
        return plan


class ExecuteNextStep:
    """Use case for executing next step in plan."""

    def __init__(self, plan_repo: PlanRepository):
        self.plan_repo = plan_repo

    async def __call__(self, plan_id: str) -> dict[str, Any]:
        """Execute next step in plan."""
        plan = await self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} not found")

        next_step = plan.get_next_step()
        if not next_step:
            # Plan completed
            plan.status = PlanStatus.COMPLETED
            plan.completed_at = datetime.now(UTC)
            await self.plan_repo.update(plan)
            return {"status": "completed", "message": "All steps completed"}

        # Simulate step execution
        _ = f"Executed {next_step.action} with params {next_step.parameters}"
        # Ensure step id is present (PlanStepVO auto-generates id if missing)
        if next_step.id is None:
            raise ValueError("Next step has no id")
        plan.mark_step_completed(next_step.id, result)
        plan.updated_at = datetime.now(UTC)

        # If there is no next step after this execution, consider plan completed
        next_after = plan.get_next_step()
        await self.plan_repo.update(plan)

        if next_after is None:
            plan.status = PlanStatus.COMPLETED
            plan.completed_at = datetime.now(UTC)
            await self.plan_repo.update(plan)
            return {"status": "completed", "message": "All steps completed"}

        return {
            "status": "step_completed",
            "step_id": next_step.id,
            "result": result,
            "next_step": next_after.action,
        }
