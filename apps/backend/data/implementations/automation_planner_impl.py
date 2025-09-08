"""OpenAI-based automation planner implementation.





This module provides an AI-driven automation planner that uses OpenAI's


language models to create and update automation plans from natural language.


"""

from __future__ import annotations

import json
import logging
import random
from typing import TYPE_CHECKING, Any

from openai import AsyncOpenAI
import Exception
import KeyError
import RuntimeError
import ValueError
import api_key
import dict
import e
import enumerate
import error_msg
import float
import guard
import hasattr
import i
import int
import isinstance
import learner
import len
import max
import max_steps
import min
import model
import moe_canary_ratio
import original_plan
import response_content
import screenshot_path
import self
import step_data
import str
import success_msg
import task_description
import tuple

try:  # optional core utility for reward
    from apps.backend.core.services.reward_functions import reward_qa  # type: ignore
except Exception:  # pragma: no cover - optional
    reward_qa = None  # type: ignore

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import AutomationPlan


logger = logging.getLogger(__name__)


class AutomationPlannerImpl:
    """OpenAI-based implementation of automation planner."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        max_steps: int = 10,
        *,
        guard: Any | None = None,
        learner: Any | None = None,
        moe_canary_ratio: float = 0.2,
    ) -> None:
        """Initialize the automation planner.





        Args:


            api_key: OpenAI API key


            model: Model to use for planning


            max_steps: Maximum number of steps in a plan


        """

        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._max_steps = max_steps

        # Optional safety/learning hooks (duck-typed to avoid tight coupling)
        self._guard = guard
        self._learner = learner
        self._moe_canary_ratio = max(0.0, min(1.0, float(moe_canary_ratio)))

        logger.info(f"AutomationPlannerImpl initialized with model: {model}")

    # ================== Helper methods (reduce complexity) ==================
    def _estimate_tokens(self, system_prompt: str, user_message: str) -> int:
        return max(1, (len(system_prompt) + len(user_message)) // 4)

    def _compute_risk(self, user_message: str) -> float:
        try:
            if self._guard and hasattr(self._guard, "score"):
                return float(self._guard.score(user_message))
        except Exception:
            pass
        return 0.0

    def _choose_model(self, estimated_tokens: int, risk: float) -> tuple[str, str]:
        provider = "openai"
        chosen_model = self._model
        try:
            if (
                self._learner
                and hasattr(self._learner, "suggest")
                and random.random() < self._moe_canary_ratio
            ):
                choice = self._learner.suggest(
                    task="automation", context_len=estimated_tokens, risk=risk
                )
                if isinstance(choice, dict):
                    provider = str(choice.get("provider", provider))
                    m = choice.get("model")
                    if isinstance(m, str) and m:
                        chosen_model = m
        except Exception:
            pass
        return provider, chosen_model

    def _log_reward(
        self,
        plan_data: dict[str, Any] | None,
        task_description: str,
        *,
        risk: float,
        provider: str,
        model: str,
    ) -> None:
        try:
            if reward_qa is None:
                return
            goal_text = (
                plan_data.get("goal", task_description)
                if isinstance(plan_data, dict)
                else task_description
            )
            reward = float(
                reward_qa(
                    pred=str(goal_text),
                    ref=str(task_description),
                    citations_ok=True,
                    guard_risk=float(risk),
                )
            )
            if self._learner and hasattr(self._learner, "record_feedback"):
                self._learner.record_feedback(
                    task="automation",
                    provider=provider,
                    model=model,
                    reward=reward,
                )
        except Exception:
            pass

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

        try:
            logger.info(f"Creating plan for task: {task_description[:100]}...")

            # Prepare system prompt

            system_prompt = self._get_system_prompt()

            # Prepare user message

            user_message = self._prepare_user_message(task_description, screenshot_path)

            # Guard + MoE canary routing (optional, non-breaking)
            estimated_tokens = self._estimate_tokens(system_prompt, user_message)
            risk = self._compute_risk(user_message)
            provider, chosen_model = self._choose_model(estimated_tokens, risk)

            # Call OpenAI API
            response = await self._client.chat.completions.create(
                model=chosen_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                max_tokens=2000,
            )

            # Parse response

            plan_data = self._parse_response(response.choices[0].message.content)

            # Convert to automation plan

            plan = self._create_plan_from_data(plan_data, task_description)

            logger.info(f"Created plan with {len(plan.steps)} steps")

            # Post-result reward logging (optional)
            self._log_reward(
                plan_data,
                task_description,
                risk=risk,
                provider=provider,
                model=chosen_model,
            )

            return plan

        except Exception as e:
            logger.error(f"Plan creation failed: {e}")

            raise RuntimeError(f"Failed to create automation plan: {e}") from e

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

        try:
            logger.info(f"Updating plan {plan.id}")

            # Prepare context for update

            context = self._prepare_update_context(plan, error_msg, success_msg)

            # Get system prompt for updates

            system_prompt = self._get_update_system_prompt()

            # Call OpenAI API for plan update

            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context},
                ],
                temperature=0.1,
                max_tokens=1500,
            )

            # Parse updated plan

            updated_data = self._parse_response(response.choices[0].message.content)

            # Create updated plan

            updated_plan = self._update_plan_from_data(plan, updated_data)

            logger.info(f"Updated plan with {len(updated_plan.steps)} steps")

            return updated_plan

        except Exception as e:
            logger.error(f"Plan update failed: {e}")

            # Return original plan on failure

            return plan

    def _get_system_prompt(self) -> str:
        """Get the system prompt for plan creation."""

        return """You are an expert UI automation planner. Your task is to break down user requests into step-by-step automation plans.





Available actions:


- MOVE: Move mouse to coordinates


- CLICK: Click at coordinates


- DOUBLE_CLICK: Double-click at coordinates


- RIGHT_CLICK: Right-click at coordinates


- TYPE: Type text


- HOTKEY: Press key combinations (e.g., "ctrl+c")


- WAIT: Wait for specified milliseconds


- SCREENSHOT: Take a screenshot


- DRAG: Drag from start to end coordinates


- SCROLL: Scroll at position





Always respond with valid JSON in this format:


{


  "goal": "Clear description of what we're trying to achieve",


  "context": "Any relevant context or assumptions",


  "steps": [


    {


      "action": "ACTION_TYPE",


      "description": "What this step does",


      "target": "Target element or coordinates",


      "parameters": {"param1": "value1"},


      "sleep_ms": 500


    }


  ]


}





Guidelines:


- Keep steps atomic and clear


- Add appropriate delays between actions


- Include error handling considerations


- Be specific about coordinates when possible


- Consider screen size variations"""

    def _get_update_system_prompt(self) -> str:
        """Get the system prompt for plan updates."""

        return """You are updating an existing automation plan based on execution results.





Your task is to:


1. Analyze what went wrong (if error provided)


2. Adjust the plan to handle the situation


3. Add recovery steps if needed


4. Maintain the original goal





Respond with updated JSON in the same format as the original plan.


Focus on practical solutions and error recovery."""

    def _prepare_user_message(
        self, task_description: str, screenshot_path: str | None
    ) -> str:
        """Prepare the user message for OpenAI."""

        message = f"Create an automation plan for this task:\n\n{task_description}"

        if screenshot_path:
            message += f"\n\nScreenshot context available at: {screenshot_path}"

            message += "\nAnalyze the screenshot to determine specific coordinates and elements."

        message += f"\n\nMaximum {self._max_steps} steps allowed."

        return message

    def _prepare_update_context(
        self, plan: AutomationPlan, error_msg: str | None, success_msg: str | None
    ) -> str:
        """Prepare context for plan updates."""

        context = f"Original plan goal: {plan.goal}\n"

        context += f"Current steps: {len(plan.steps)}\n\n"

        if error_msg:
            context += f"Error encountered: {error_msg}\n"

            context += "Please adjust the plan to handle this error.\n"

        if success_msg:
            context += f"Success: {success_msg}\n"

            context += "Continue with remaining steps or mark as complete.\n"

        # Add plan summary

        context += "\nCurrent plan steps:\n"

        for i, step in enumerate(plan.steps):
            context += f"{i + 1}. {step.action.value}: {step.description}\n"

        return context

    def _parse_response(self, response_content: str | None) -> dict[str, Any]:
        """Parse OpenAI response into plan data."""

        if not response_content:
            raise ValueError("Empty response from OpenAI")

        try:
            # Extract JSON from response (handle markdown code blocks)

            content = response_content.strip()

            if content.startswith("```json"):
                content = content[7:]

            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content.strip())

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response: {e}")

            logger.error(f"Response content: {response_content}")

            raise ValueError(f"Invalid JSON response: {e}") from e

    def _create_plan_from_data(
        self, plan_data: dict[str, Any], task_description: str
    ) -> AutomationPlan:
        """Create AutomationPlan from parsed data."""

        from apps.backend.core.domain.value_objects.automation import (
            ActionType,
            AutomationPlan,
            AutomationStep,
            Point,
        )

        # Create steps

        steps = []

        for step_data in plan_data.get("steps", []):
            try:
                action = ActionType(step_data["action"].lower())

                # Parse parameters

                params = step_data.get("parameters", {})

                target_point = None

                # Extract coordinates if present

                if "x" in params and "y" in params:
                    target_point = Point(x=int(params["x"]), y=int(params["y"]))

                step = AutomationStep.create(
                    action=action,
                    description=step_data.get("description", ""),
                    target=step_data.get("target", ""),
                    parameters=params,
                    sleep_ms=step_data.get("sleep_ms", 500),
                    target_point=target_point,
                )

                steps.append(step)

            except (KeyError, ValueError) as e:
                logger.warning(f"Skipping invalid step: {e}")

                continue

        # Create plan

        return AutomationPlan.create(
            goal=plan_data.get("goal", task_description),
            context=plan_data.get("context", ""),
            steps=steps,
            safety_mode="strict",
        )

    def _update_plan_from_data(
        self, original_plan: AutomationPlan, updated_data: dict[str, Any]
    ) -> AutomationPlan:
        """Update existing plan with new data."""

        # Create new plan with updated data but preserve ID and metadata

        updated_plan = self._create_plan_from_data(updated_data, original_plan.goal)

        # Preserve original metadata

        updated_plan.id = original_plan.id

        updated_plan.created_at = original_plan.created_at

        return updated_plan
