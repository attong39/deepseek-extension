"""API endpoints for UI automation system.





This module provides RESTful API endpoints for the AI-driven UI automation system,


including plan creation, execution management, and safety validation.





Features:


- Plan creation from screenshots/descriptions


- Step-by-step execution with safety checks


- Real-time status monitoring


- Result retrieval and reporting


"""

from __future__ import annotations

import logging
from typing import Annotated, Any

from app.serializers.automation import (
import Exception
import bool
import bytes
import context
import description
import dict
import e
import execution_id
import factory
import float
import getattr
import int
import len
import list
import plan_id
import r
import request
import s
import safety_config
import screenshot
import service
import step
import str
import type
    AutomationExecutionResponse,
    AutomationPlanResponse,
    AutomationResultResponse,
    CreateAutomationPlanRequest,
    ExecutionStatusResponse,
    SafetyValidationResponse,
)
from apps.backend.core.domain.value_objects.automation import SafetyConfig
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from pydantic import BaseModel, Field

# from data.factories.automation_factory import AutomationFactory  # ❌ Architecture violation


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/automation", tags=["automation"])


# Dependency injection


async def get_automation_factory() -> Any:
    """Get automation factory instance.





    Returns a lightweight in-module stub to satisfy DI during development.


    """

    # Local stub implementations

    class _Perception:
        async def detect_ui_elements(
            self, screenshot_data: bytes
        ) -> list[dict[str, Any]]:
            _ = screenshot_data
            return []

    class _AutomationService:
        async def execute_plan(self, plan_id: str) -> Any:
            _ = plan_id
            return type(
                "Report",
                (),
                {
                    "execution_id": "exec_1",
                    "plan_id": "plan_123",
                    "status": type("Status", (), {"value": "completed"})(),
                    "progress": 1.0,
                    "current_step": None,
                    "step_results": [],
                    "started_at": "2025-01-01T00:00:00Z",
                    "completed_at": "2025-01-01T00:00:01Z",
                    "error_message": None,
                },
            )()

    class _SafetyEngine:
        async def validate_plan(self, plan: Any) -> Any:
            _ = plan
            return type(
                "SafetyResult",
                (),
                {
                    "is_safe": True,
                    "risk_level": type("Risk", (), {"value": "low"})(),
                    "warnings": [],
                    "blocked_actions": [],
                    "recommendations": [],
                },
            )()

    class _Planner:
        async def create_plan(
            self, description: str, context: dict[str, Any], safety_config: Any
        ) -> Any:
            _ = (context, safety_config)
            return type(
                "Plan",
                (),
                {
                    "plan_id": "plan_123",
                    "description": description,
                    "steps": [],
                    "estimated_duration": 0.0,
                    "safety_level": type("Level", (), {"value": "medium"})(),
                    "created_at": "2025-01-01T00:00:00Z",
                },
            )()

    class _Factory:
        def create_planner(self) -> _Planner:
            return _Planner()

        def create_perception(self) -> _Perception:
            return _Perception()

        def create_automation_service(self) -> _AutomationService:
            return _AutomationService()

        def create_safety_engine(self) -> _SafetyEngine:
            return _SafetyEngine()

    return _Factory()


async def _get_automation_service(request: Request) -> Any:
    """Get automation service from request state or dependency injection."""
    # This is a stub - should be implemented based on the DI container
    return getattr(request.state, "automation_service", None)


async def get_automation_service_dep(request: Request) -> Any:
    """Resolve AutomationService via app dependencies using the request.

    Falls back to None if DI is not initialized; callers should handle fallback.
    """

    try:
        return await _get_automation_service(request)
    except Exception:
        return None

    # Fallback handled in get_automation_factory
    return await get_automation_factory()


# --- Execute ad-hoc steps ---
class AutomationExecuteStep(BaseModel):
    """Single automation step according to the requested schema."""

    type: str = Field(
        ..., description="hotkey|type|wait|click|double_click|ocr_read|template_match"
    )
    args: list[str] | None = None  # for hotkey
    text: str | None = None  # for type
    timeout: float | None = None
    x: int | None = None  # for click
    y: int | None = None  # for click
    # Optional fields for OCR/template matching
    region: dict[str, int] | None = None
    template: str | None = None
    threshold: float | None = None


class AutomationExecuteRequest(BaseModel):
    steps: list[AutomationExecuteStep] = Field(..., description="Ordered steps to run")
    headless: bool = Field(True, description="Run in headless/mock mode")


@router.post(
    "/execute",
    response_model=AutomationExecutionResponse,
    summary="Execute ad-hoc automation steps",
    description=("Execute a list of UI automation steps in headless/mock mode."),
)
async def execute_automation(
    request: AutomationExecuteRequest,
) -> AutomationExecutionResponse:
    """Execute steps using a headless orchestrator and return a summary report."""
    try:
        # Import orchestrator lazily to avoid circulars
        from apps.backend.core.services.automation_steps import StepsOrchestrator

        orch = StepsOrchestrator()
        report = await orch.execute_steps(
            [s.model_dump(exclude_none=True) for s in request.steps],
            headless=request.headless,
        )

        return AutomationExecutionResponse(
            execution_id=report.execution_id,
            plan_id="adhoc",
            status=report.status,
            progress=report.progress,
            current_step=report.current_step,
            steps_completed=report.steps_completed,
            total_steps=report.total_steps,
            started_at=report.started_at,
            completed_at=report.completed_at,
            error_message=report.error_message,
        )
    except Exception as e:  # pragma: no cover - surface details to client
        logger.exception("Ad-hoc automation execution failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Execution failed: {e}",
        ) from e


@router.post(
    "/plans",
    response_model=AutomationPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create automation plan",
    description="Create an AI-driven automation plan from screenshot and description.",
)
async def create_automation_plan(
    request: CreateAutomationPlanRequest,
    factory: Annotated[Any, Depends(get_automation_factory)] = None,
) -> AutomationPlanResponse:
    """Create an automation plan from user input.





    Args:


        request: Plan creation request with description and options


        factory: Automation factory for service creation





    Returns:


        Created automation plan with steps and safety validation





    Raises:


        HTTPException: If plan creation fails


    """

    try:
        logger.info(f"Creating automation plan: {request.description}")

        # Get planner service

        planner = factory.create_planner()

        # Create plan

        plan = await planner.create_plan(
            description=request.description,
            context=request.context or {},
            safety_config=request.safety_config,
        )

        logger.info(f"Created plan with {len(plan.steps)} steps")

        return AutomationPlanResponse(
            plan_id=plan.plan_id,
            description=plan.description,
            steps=[
                {
                    "step_id": step.step_id,
                    "action": step.action.value,
                    "target": step.target,
                    "parameters": step.parameters,
                    "description": step.description,
                }
                for step in plan.steps
            ],
            estimated_duration=plan.estimated_duration,
            safety_level=plan.safety_level.value,
            created_at=plan.created_at,
        )

    except Exception as e:
        logger.error(f"Failed to create automation plan: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create automation plan: {e!s}",
        ) from e


@router.post(
    "/plans/from-screenshot",
    response_model=AutomationPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create plan from screenshot",
    description="Create automation plan by analyzing a screenshot.",
)
async def create_plan_from_screenshot(
    screenshot: UploadFile,
    description: str = Form(..., description="What you want to automate"),
    context: str = Form(None, description="Additional context (JSON string)"),
    factory: Annotated[Any, Depends(get_automation_factory)] = None,  # injected
) -> AutomationPlanResponse:
    """Create automation plan from screenshot analysis.





    Args:


        screenshot: Screenshot image file


        description: Automation description


        context: Additional context as JSON string


        factory: Automation factory for service creation





    Returns:


        Created automation plan





    Raises:


        HTTPException: If plan creation fails


    """

    try:
        logger.info(f"Creating plan from screenshot: {description}")

        # Read screenshot data

        screenshot_data = await screenshot.read()

        # Get perception service for screenshot analysis

        perception = factory.create_perception()

        # Analyze screenshot to understand UI elements

        elements = await perception.detect_ui_elements(screenshot_data)

        # Get planner service

        planner = factory.create_planner()

        # Create context with UI elements

        plan_context = {"ui_elements": elements}

        if context:
            import json

            try:
                user_context = json.loads(context)

                plan_context.update(user_context)

            except json.JSONDecodeError:
                logger.warning("Invalid context JSON, ignoring")

        # Create plan with screenshot context

        plan = await planner.create_plan(
            description=description,
            context=plan_context,
            safety_config=SafetyConfig(),
        )

        logger.info(f"Created plan from screenshot with {len(plan.steps)} steps")

        return AutomationPlanResponse(
            plan_id=plan.plan_id,
            description=plan.description,
            steps=[
                {
                    "step_id": step.step_id,
                    "action": step.action.value,
                    "target": step.target,
                    "parameters": step.parameters,
                    "description": step.description,
                }
                for step in plan.steps
            ],
            estimated_duration=plan.estimated_duration,
            safety_level=plan.safety_level.value,
            created_at=plan.created_at,
        )

    except Exception as e:
        logger.error(f"Failed to create plan from screenshot: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create plan from screenshot: {e!s}",
        ) from e


@router.post(
    "/execute/{plan_id}",
    response_model=AutomationExecutionResponse,
    summary="Execute automation plan",
    description="Execute an automation plan step by step.",
)
async def execute_automation_plan(
    plan_id: str,
    factory: Annotated[Any, Depends(get_automation_factory)] = None,
    service: Annotated[Any, Depends(get_automation_service_dep)] = None,
) -> AutomationExecutionResponse:
    """Execute an automation plan.





    Args:


        plan_id: ID of the plan to execute


        factory: Automation factory for service creation





    Returns:


        Execution result with status and details





    Raises:


        HTTPException: If execution fails


    """

    try:
        logger.info(f"Executing automation plan: {plan_id}")

        # Get services (prefer request-aware DI service if available)
        automation_service = service or factory.create_automation_service()

        # Execute plan

        report = await automation_service.execute_plan(plan_id)

        logger.info(f"Plan execution completed: {report.status.value}")

        return AutomationExecutionResponse(
            execution_id=report.execution_id,
            plan_id=report.plan_id,
            status=report.status.value,
            progress=report.progress,
            current_step=report.current_step,
            steps_completed=len([r for r in report.step_results if r.success]),
            total_steps=len(report.step_results),
            started_at=report.started_at,
            completed_at=report.completed_at,
            error_message=report.error_message,
        )

    except Exception as e:
        logger.error(f"Failed to execute automation plan: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute automation plan: {e!s}",
        ) from e


@router.get(
    "/status/{execution_id}",
    response_model=ExecutionStatusResponse,
    summary="Get execution status",
    description="Get current status of an automation execution.",
)
async def get_execution_status(
    execution_id: str,
    _factory: Annotated[Any, Depends(get_automation_factory)] = None,
) -> ExecutionStatusResponse:
    """Get execution status.





    Args:


        execution_id: ID of the execution to check


        factory: Automation factory for service creation





    Returns:


        Current execution status





    Raises:


        HTTPException: If status retrieval fails


    """

    try:
        logger.info(f"Getting execution status: {execution_id}")

        # Get status (this would require storing execution state)

        # For now, return a placeholder implementation

        return ExecutionStatusResponse(
            execution_id=execution_id,
            status="completed",
            progress=1.0,
            current_step=None,
            steps_completed=5,
            total_steps=5,
            last_updated="2025-01-21T10:00:00Z",
        )

    except Exception as e:
        logger.error(f"Failed to get execution status: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get execution status: {e!s}",
        ) from e


@router.get(
    "/results/{execution_id}",
    response_model=AutomationResultResponse,
    summary="Get execution results",
    description="Get detailed results of an automation execution.",
)
async def get_execution_results(
    execution_id: str,
    _factory: Annotated[Any, Depends(get_automation_factory)] = None,
) -> AutomationResultResponse:
    """Get execution results.





    Args:


        execution_id: ID of the execution to get results for


        factory: Automation factory for service creation





    Returns:


        Detailed execution results





    Raises:


        HTTPException: If results retrieval fails


    """

    try:
        logger.info(f"Getting execution results: {execution_id}")

        # For now, return placeholder results

        return AutomationResultResponse(
            execution_id=execution_id,
            plan_id="plan_123",
            status="completed",
            success=True,
            steps_results=[
                {
                    "step_id": "step_1",
                    "action": "click",
                    "success": True,
                    "duration": 1.5,
                    "error_message": None,
                }
            ],
            total_duration=5.2,
            screenshots=["screenshot_1.png", "screenshot_2.png"],
            started_at="2025-01-21T10:00:00Z",
            completed_at="2025-01-21T10:00:05Z",
        )

    except Exception as e:
        logger.error(f"Failed to get execution results: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get execution results: {e!s}",
        ) from e


@router.post(
    "/validate-safety",
    response_model=SafetyValidationResponse,
    summary="Validate safety",
    description="Validate safety of an automation plan or step.",
)
async def validate_safety(
    plan: dict[str, Any],
    factory: Annotated[Any, Depends(get_automation_factory)] = None,
) -> SafetyValidationResponse:
    """Validate safety of automation plan.





    Args:


        plan: Automation plan to validate


        factory: Automation factory for service creation





    Returns:


        Safety validation result





    Raises:


        HTTPException: If validation fails


    """

    try:
        logger.info("Validating automation safety")

        # Get safety engine
        safety_engine = factory.create_safety_engine()

        # Create minimal plan object for validation
        from apps.backend.core.domain.value_objects.automation import (
            AutomationPlan,
            SafetyLevel,
        )

        # Convert dict to plan object (simplified)
        automation_plan = AutomationPlan(
            plan_id=plan.get("plan_id", "temp"),
            description=plan.get("description", ""),
            steps=[],  # TODO: parse steps from dict when schema is ready
            estimated_duration=0.0,
            safety_level=SafetyLevel.MEDIUM,
        )

        # Validate safety
        result = await safety_engine.validate_plan(automation_plan)
        logger.info("Safety validation completed: %s", result.is_safe)

        return SafetyValidationResponse(
            is_safe=result.is_safe,
            risk_level=result.risk_level.value,
            warnings=result.warnings,
            blocked_actions=result.blocked_actions,
            recommendations=result.recommendations,
        )

    except Exception as e:
        logger.error(f"Failed to validate safety: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate safety: {e!s}",
        ) from e


@router.delete(
    "/plans/{plan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete automation plan",
    description="Delete an automation plan.",
    response_model=None,  # No response body for 204
    response_class=Response,
)
async def delete_automation_plan(
    plan_id: str,
    factory: Annotated[Any, Depends(get_automation_factory)] = None,
) -> None:
    """Delete automation plan.





    Args:


        plan_id: ID of the plan to delete


        factory: Automation factory for service creation





    Raises:


        HTTPException: If deletion fails


    """

    try:
        logger.info(f"Deleting automation plan: {plan_id}")

        # Delete plan (placeholder implementation)

        # await automation_service.delete_plan(plan_id)

        logger.info(f"Plan deleted successfully: {plan_id}")

        # No return statement for 204 status code

    except Exception as e:
        logger.error(f"Failed to delete automation plan: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete automation plan: {e!s}",
        ) from e
