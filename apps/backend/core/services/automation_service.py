"""Core automation service for orchestrating UI automation tasks.





This service provides the main entry point for automation functionality,


coordinating between perception, planning, execution, and safety systems.


"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING
import Exception
import RuntimeError
import bool
import config
import e
import executor
import id
import input_controller
import len
import ocr_engine
import planner
import safety_engine
import safety_result
import screen_perception
import screenshot_context
import self
import step
import str
import task_description

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import (
        AutomationPlan,
        ExecutionReport,
        SafetyConfig,
    )
    from apps.backend.core.interfaces.automation import (
        AutomationExecutor,
        AutomationPlanner,
        SafetyEngine,
    )
    from apps.backend.core.interfaces.input_control import InputController
    from apps.backend.core.interfaces.perception import OcrEngine, ScreenPerception


logger = logging.getLogger(__name__)


class AutomationService:
    """Core service for UI automation tasks."""

    def __init__(
        self,
        screen_perception: ScreenPerception,
        input_controller: InputController,
        ocr_engine: OcrEngine,
        planner: AutomationPlanner,
        executor: AutomationExecutor,
        safety_engine: SafetyEngine,
    ) -> None:
        """Initialize the automation service.





        Args:


            screen_perception: Screen capture and vision service


            input_controller: Mouse and keyboard control service


            ocr_engine: Text recognition service


            planner: AI planning service


            executor: Step execution service


            safety_engine: Safety monitoring service


        """

        self._screen_perception = screen_perception

        self._input_controller = input_controller

        self._ocr_engine = ocr_engine

        self._planner = planner

        self._executor = executor

        self._safety_engine = safety_engine

    async def execute_task(
        self,
        task_description: str,
        screenshot_context: bool = True,
    ) -> ExecutionReport:
        """Execute a complete automation task.





        Args:


            task_description: Natural language description of the task


            screenshot_context: Whether to include screenshot for planning





        Returns:


            Complete execution report





        Raises:


            ValueError: If task description is invalid


            RuntimeError: If execution fails critically


        """

        logger.info(f"Starting automation task: {task_description}")

        try:
            # Capture screenshot for context if requested

            screenshot_path = None

            if screenshot_context:
                import tempfile

                screenshot_path = str(
                    Path(tempfile.gettempdir()) / f"automation_context_{id(self)}.png"
                )

                await self._screen_perception.screenshot(screenshot_path)

                logger.debug(f"Captured context screenshot: {screenshot_path}")

            # Create execution plan

            plan = await self._planner.create_plan(
                task_description=task_description,
                screenshot_path=screenshot_path,
            )

            logger.info(f"Created plan with {len(plan.steps)} steps")

            # Execute the plan

            report = await self._executor.execute_plan(plan)

            logger.info(f"Task completed. Success: {report.all_success}")

            return report

        except Exception as e:
            logger.error(f"Task execution failed: {e}", exc_info=True)

            raise RuntimeError(f"Automation task failed: {e}") from e

    async def plan_task(
        self,
        task_description: str,
        screenshot_context: bool = True,
    ) -> AutomationPlan:
        """Plan an automation task without executing it.





        Args:


            task_description: Natural language description of the task


            screenshot_context: Whether to include screenshot for planning





        Returns:


            Generated automation plan


        """

        logger.info(f"Planning automation task: {task_description}")

        # Capture screenshot for context if requested

        screenshot_path = None

        if screenshot_context:
            import tempfile

            screenshot_path = str(
                Path(tempfile.gettempdir()) / f"automation_plan_{id(self)}.png"
            )

            await self._screen_perception.screenshot(screenshot_path)

        # Create execution plan

        plan = await self._planner.create_plan(
            task_description=task_description,
            screenshot_path=screenshot_path,
        )

        logger.info(f"Created plan with {len(plan.steps)} steps")

        return plan

    async def validate_safety(
        self,
        plan: AutomationPlan,
        config: SafetyConfig,
    ) -> bool:
        """Validate that a plan is safe to execute.





        Args:


            plan: Plan to validate


            config: Safety configuration





        Returns:


            True if plan is safe to execute


        """

        logger.info(f"Validating safety for plan with {len(plan.steps)} steps")

        for step in plan.steps:
            await self._safety_engine.check_safety(step, config)

            if not safety_result.is_safe:
                logger.warning(f"Unsafe step detected: {safety_result.violations}")

                return False

        logger.info("Plan validated as safe")

        return True
