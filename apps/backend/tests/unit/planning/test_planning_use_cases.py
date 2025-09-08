"""
Tests for Planning Use Cases - ZETA AI
=====================================
"""

import pytest

from core.domain.entities.plan import PlanStatus
from core.use_cases.planning.create_plan import CreatePlan, ExecuteNextStep, ExecutePlan
from data.repositories.plan_repository import InMemoryPlanRepository
import ValueError
import len
import result


class TestCreatePlan:
    """Test cases for CreatePlan use case."""

    @pytest.fixture
    def plan_repo(self):
        """Setup plan repository."""
        return InMemoryPlanRepository()

    @pytest.fixture
    def create_plan_use_case(self, plan_repo):
        """Setup CreatePlan use case."""
        return CreatePlan(plan_repo)

    @pytest.mark.asyncio
    async def test_create_plan_success(self, create_plan_use_case):
        """Test successful plan creation."""
        steps_data = [
            {
                "action": "click",
                "description": "Click on button",
                "parameters": {"x": 100, "y": 200},
            },
            {
                "action": "type",
                "description": "Type text",
                "parameters": {"text": "Hello World"},
            },
        ]

        plan = await create_plan_use_case(
            title="Test Plan",
            description="A test automation plan",
            agent_id="agent_1",
            user_id="user_1",
            steps_data=steps_data,
        )

        assert plan.id == "plan_1"
        assert plan.title == "Test Plan"
        assert plan.description == "A test automation plan"
        assert plan.agent_id == "agent_1"
        assert plan.user_id == "user_1"
        assert plan.status == PlanStatus.DRAFT
        assert len(plan.steps) == 2

        # Check first step
        assert plan.steps[0].action == "click"
        assert plan.steps[0].description == "Click on button"
        assert plan.steps[0].parameters == {"x": 100, "y": 200}
        assert plan.steps[0].order == 1
        assert not plan.steps[0].is_completed


class TestExecutePlan:
    """Test cases for ExecutePlan use case."""

    @pytest.fixture
    def plan_repo(self):
        """Setup plan repository with test data."""
        return InMemoryPlanRepository()

    @pytest.fixture
    async def execute_plan_use_case(self, plan_repo):
        """Setup ExecutePlan use case with test plan."""
        # Create a test plan first
        create_use_case = CreatePlan(plan_repo)
        await create_use_case(
            title="Test Plan",
            description="Test plan",
            agent_id="agent_1",
            user_id="user_1",
            steps_data=[{"action": "test", "description": "test step"}],
        )
        return ExecutePlan(plan_repo)

    @pytest.mark.asyncio
    async def test_execute_plan_success(self, execute_plan_use_case):
        """Test successful plan execution start."""
        plan = await execute_plan_use_case("plan_1")

        assert plan.status == PlanStatus.EXECUTING
        assert plan.updated_at is not None

    @pytest.mark.asyncio
    async def test_execute_nonexistent_plan(self, execute_plan_use_case):
        """Test execution of non-existent plan."""
        with pytest.raises(ValueError, match="Plan nonexistent not found"):
            await execute_plan_use_case("nonexistent")


class TestExecuteNextStep:
    """Test cases for ExecuteNextStep use case."""

    @pytest.fixture
    async def plan_repo_with_plan(self):
        """Setup plan repository with executing plan."""
        repo = InMemoryPlanRepository()
        create_use_case = CreatePlan(repo)

        # Create plan with multiple steps
        steps_data = [
            {"action": "step1", "description": "First step"},
            {"action": "step2", "description": "Second step"},
        ]

        plan = await create_use_case(
            title="Multi-step Plan",
            description="Plan with multiple steps",
            agent_id="agent_1",
            user_id="user_1",
            steps_data=steps_data,
        )

        # Start execution
        execute_use_case = ExecutePlan(repo)
        await execute_use_case(plan.id)

        return repo

    @pytest.fixture
    def execute_step_use_case(self, plan_repo_with_plan):
        """Setup ExecuteNextStep use case."""
        return ExecuteNextStep(plan_repo_with_plan)

    @pytest.mark.asyncio
    async def test_execute_next_step(self, execute_step_use_case):
        """Test executing next step."""
        _ = await execute_step_use_case("plan_1")

        assert result["status"] == "step_completed"
        assert result["step_id"] == "step_1"
        assert "Executed step1" in result["result"]
        assert result["next_step"] == "step2"

    @pytest.mark.asyncio
    async def test_execute_all_steps_completes_plan(self, execute_step_use_case):
        """Test that executing all steps completes the plan."""
        # Execute first step
        await execute_step_use_case("plan_1")

        # Execute second step
        _ = await execute_step_use_case("plan_1")

        assert result["status"] == "completed"
        assert result["message"] == "All steps completed"
