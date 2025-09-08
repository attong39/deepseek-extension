"""Step-by-step automation executor implementation.





This module provides the execution engine for automation plans,


coordinating between input control and perception systems.


"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING
from uuid import uuid4
import Exception
import ValueError
import bool
import default_timeout
import e
import enumerate
import float
import height
import i
import input_controller
import int
import isinstance
import len
import plan
import point_key
import result
import screen_perception
import self
import step
import step_result
import str
import width

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import (
        AutomationPlan,
        AutomationStep,
        ExecutionReport,
        Point,
        StepResult,
    )
    from apps.backend.core.interfaces.input_control import InputController
    from apps.backend.core.interfaces.perception import ScreenPerception


logger = logging.getLogger(__name__)


class AutomationExecutorImpl:
    """Implementation of automation executor for step-by-step execution."""

    def __init__(
        self,
        input_controller: InputController,
        screen_perception: ScreenPerception,
        default_timeout: float = 30.0,
    ) -> None:
        """Initialize the automation executor.





        Args:


            input_controller: Input control implementation


            screen_perception: Screen perception implementation


            default_timeout: Default timeout for operations in seconds


        """

        self._input_controller = input_controller

        self._screen_perception = screen_perception

        self._default_timeout = default_timeout

        logger.info("AutomationExecutorImpl initialized")

    async def execute_step(self, step: AutomationStep) -> StepResult:
        """Execute a single automation step.





        Args:


            step: Step to execute





        Returns:


            Execution result


        """

        start_time = time.time()

        try:
            logger.debug(f"Executing step: {step.action.value} - {step.description}")

            # Execute based on action type

            success = await self._execute_action(step)

            # Add sleep if specified

            if step.sleep_ms > 0:
                await asyncio.sleep(step.sleep_ms / 1000.0)

            execution_time = int((time.time() - start_time) * 1000)

            from apps.backend.core.domain.value_objects.automation import StepResult

            _ = StepResult.create(
                step_id=step.id,
                success=success,
                execution_time_ms=execution_time,
                output_data={"action": step.action.value, "completed": True},
            )

            logger.debug(f"Step completed successfully in {execution_time}ms")

            return result

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)

            error_message = str(e)

            logger.error(f"Step failed: {error_message}")

            from apps.backend.core.domain.value_objects.automation import StepResult

            _ = StepResult.create(
                step_id=step.id,
                success=False,
                execution_time_ms=execution_time,
                error_message=error_message,
                output_data={"action": step.action.value, "error": error_message},
            )

            return result

    async def execute_plan(self, plan: AutomationPlan) -> ExecutionReport:
        """Execute a complete automation plan.





        Args:


            plan: Plan to execute





        Returns:


            Complete execution report


        """

        session_id = uuid4()

        try:
            logger.info(f"Executing plan {plan.id} with {len(plan.steps)} steps")

            from apps.backend.core.domain.value_objects.automation import (
                ExecutionReport,
            )

            report = ExecutionReport.create(plan=plan, session_id=session_id)

            # Execute each step

            for i, step in enumerate(plan.steps):
                logger.info(
                    f"Executing step {i + 1}/{len(plan.steps)}: {step.description}"
                )

                await self.execute_step(step)

                report.add_result(step_result)

                # Stop on failure if in strict mode

                if not step_result.success and plan.safety_mode == "strict":
                    logger.warning(
                        f"Stopping execution due to step failure: {step_result.error_message}"
                    )

                    break

                # Small delay between steps for stability

                await asyncio.sleep(0.1)

            # Mark as completed

            report.complete()

            logger.info(
                f"Plan execution completed. Success rate: {report.success_rate:.2%}"
            )

            return report

        except Exception as e:
            logger.error(f"Plan execution failed: {e}")

            # Create error report

            from apps.backend.core.domain.value_objects.automation import (
                ExecutionReport,
            )

            error_report = ExecutionReport.create(
                plan=plan,
                session_id=session_id,
                safety_violations=[f"Execution error: {e}"],
            )

            error_report.complete()

            return error_report

    async def _execute_action(self, step: AutomationStep) -> bool:
        """Execute a specific action based on step type.





        Args:


            step: Step to execute





        Returns:


            True if action succeeded


        """

        from apps.backend.core.domain.value_objects.automation import ActionType

        try:
            if step.action == ActionType.MOVE:
                await self._execute_move(step)

            elif step.action == ActionType.CLICK:
                await self._execute_click(step)

            elif step.action == ActionType.DOUBLE_CLICK:
                await self._execute_double_click(step)

            elif step.action == ActionType.RIGHT_CLICK:
                await self._execute_right_click(step)

            elif step.action == ActionType.TYPE:
                await self._execute_type(step)

            elif step.action == ActionType.HOTKEY:
                await self._execute_hotkey(step)

            elif step.action == ActionType.WAIT:
                await self._execute_wait(step)

            elif step.action == ActionType.SCREENSHOT:
                await self._execute_screenshot(step)

            elif step.action == ActionType.DRAG:
                await self._execute_drag(step)

            elif step.action == ActionType.SCROLL:
                await self._execute_scroll(step)

            else:
                raise ValueError(f"Unsupported action: {step.action}")

            return True

        except Exception as e:
            logger.error(f"Action execution failed: {e}")

            return False

    async def _execute_move(self, step: AutomationStep) -> None:
        """Execute move action."""

        target_point = await self._resolve_target_point(step)

        await self._input_controller.move_to(target_point)

    async def _execute_click(self, step: AutomationStep) -> None:
        """Execute click action."""

        target_point = await self._resolve_target_point(step)

        await self._input_controller.click(target_point, button="left")

    async def _execute_double_click(self, step: AutomationStep) -> None:
        """Execute double-click action."""

        target_point = await self._resolve_target_point(step)

        await self._input_controller.click(target_point, button="left", double=True)

    async def _execute_right_click(self, step: AutomationStep) -> None:
        """Execute right-click action."""

        target_point = await self._resolve_target_point(step)

        await self._input_controller.click(target_point, button="right")

    async def _execute_type(self, step: AutomationStep) -> None:
        """Execute type action."""

        text = step.parameters.get("text", step.target)

        if not text:
            raise ValueError("No text specified for type action")

        interval = step.parameters.get("interval", 0.05)

        await self._input_controller.type_text(text, interval)

    async def _execute_hotkey(self, step: AutomationStep) -> None:
        """Execute hotkey action."""

        keys = step.parameters.get("keys", step.target)

        if not keys:
            raise ValueError("No keys specified for hotkey action")

        await self._input_controller.key_press(keys)

    async def _execute_wait(self, step: AutomationStep) -> None:
        """Execute wait action."""

        wait_ms = step.parameters.get("duration_ms", step.sleep_ms)

        await asyncio.sleep(wait_ms / 1000.0)

    async def _execute_screenshot(self, step: AutomationStep) -> None:
        """Execute screenshot action."""

        save_path = step.parameters.get("save_path")

        await self._screen_perception.screenshot(save_path)

    async def _execute_drag(self, step: AutomationStep) -> None:
        """Execute drag action."""

        start_point = await self._resolve_target_point(step, "start")

        end_point = await self._resolve_target_point(step, "end")

        duration = step.parameters.get("duration", 1.0)

        await self._input_controller.drag(start_point, end_point, duration)

    async def _execute_scroll(self, step: AutomationStep) -> None:
        """Execute scroll action."""

        target_point = await self._resolve_target_point(step)

        direction = step.parameters.get("direction", "down")

        clicks = step.parameters.get("clicks", 3)

        await self._input_controller.scroll(target_point, direction, clicks)

    async def _resolve_target_point(
        self, step: AutomationStep, point_key: str = "target"
    ) -> Point:
        """Resolve target point from step parameters.





        Args:


            step: Automation step


            point_key: Key to look for in parameters





        Returns:


            Resolved point coordinates


        """

        from apps.backend.core.domain.value_objects.automation import Point

        # Check if point is directly specified

        if step.target_point:
            return step.target_point

        # Check parameters for coordinates

        if point_key == "start":
            x = step.parameters.get("start_x")

            y = step.parameters.get("start_y")

        elif point_key == "end":
            x = step.parameters.get("end_x")

            y = step.parameters.get("end_y")

        else:
            x = step.parameters.get("x")

            y = step.parameters.get("y")

        if x is not None and y is not None:
            return Point(x=int(x), y=int(y))

        # Try to find text on screen

        if step.target and isinstance(step.target, str):
            found_point = await self._screen_perception.find_text(step.target)

            if found_point:
                return found_point

        # Try template matching if template path provided

        template_path = step.parameters.get("template_path")

        if template_path:
            found_point = await self._screen_perception.find_template(template_path)

            if found_point:
                return found_point

        # Default to center of screen

        width, height = await self._screen_perception.get_screen_size()

        return Point(x=width // 2, y=height // 2)
