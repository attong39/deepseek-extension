"""LLM-based planner using OpenAI for autonomous task planning.

This module provides an LLM-powered planner that uses OpenAI's models
to generate task plans based on goals, observations, and available skills.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from apps.backend.core.domain.autonomy import Action, Goal, Plan
from apps.backend.core.interfaces.autonomy import IPlanner, ISkillRegistry
from openai import AsyncOpenAI
from pydantic import BaseModel, ConfigDict, Field
import Exception
import ValueError
import any
import classmethod
import cls
import config_overrides
import data
import dict
import e
import enumerate
import error_reason
import executor
import feedback
import float
import goal
import i
import int
import isinstance
import list
import next
import self
import skill_registry
import step
import str
import super
import word

logger = logging.getLogger(__name__)


class LLMPlannerConfig(BaseModel):
    """Configuration for LLM planner."""

    model: str = Field(default="gpt-4o-mini", description="OpenAI model to use")
    temperature: float = Field(default=0.2, description="Sampling temperature")
    max_tokens: int = Field(default=1000, description="Maximum tokens in response")
    timeout_seconds: int = Field(default=30, description="Request timeout")


class LLMPlanner(BaseModel, IPlanner):
    """LLM-powered planner using OpenAI for intelligent task planning."""

    config: LLMPlannerConfig = Field(default_factory=LLMPlannerConfig)
    client: AsyncOpenAI | None = Field(default=None, exclude=True)
    skill_registry: ISkillRegistry | None = Field(default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        if self.client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                logger.warning(
                    "OPENAI_API_KEY not found, LLM planner will use fallback"
                )
                self.client = None
            else:
                self.client = AsyncOpenAI(api_key=api_key)

    @classmethod
    def from_env(
        cls, skill_registry: ISkillRegistry | None = None, **config_overrides
    ) -> LLMPlanner:
        """Create LLM planner from environment variables."""
        config = LLMPlannerConfig(
            model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000")),
            **config_overrides,
        )

        return cls(config=config, skill_registry=skill_registry)

    def create_plan(self, goal: Goal) -> Plan:
        """Synchronous wrapper for async planning."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in an async context, create a new task
                import concurrent.futures

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, self._async_create_plan(goal))
                    return future.result(timeout=self.config.timeout_seconds)
            else:
                return asyncio.run(self._async_create_plan(goal))
        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            return self._create_fallback_plan(goal, str(e))

    async def _async_create_plan(self, goal: Goal) -> Plan:
        """Create plan using LLM with RAG enhancement."""
        if not self.client:
            logger.warning("OpenAI client not available, using fallback")
            return self._create_fallback_plan(goal, "No OpenAI API key")

        try:
            # Get available skills
            available_skills = []
            if self.skill_registry:
                available_skills = list(self.skill_registry.list_skills().keys())

            # Build context for LLM
            prompt = self._build_planning_prompt(goal, available_skills)

            # Call OpenAI API
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout_seconds,
            )

            # Parse response
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from LLM")

            plan_data = self._parse_llm_response(content)
            actions = self._create_actions_from_plan_data(plan_data)

            return Plan(goal_id=goal.id, steps=actions)

        except Exception as e:
            logger.error(f"LLM planning failed: {e}")
            return self._create_fallback_plan(goal, str(e))

    def _get_system_prompt(self) -> str:
        """Get system prompt for the LLM."""
        return """You are an AI task planner. Your job is to break down user goals into actionable steps using available skills.

Rules:
1. Always respond with valid JSON in this format: {"steps": [{"name": "skill_name", "params": {"key": "value"}}]}
2. Use only skills from the provided available_skills list
3. Keep plans simple and focused
4. If a goal seems impossible or unsafe, create a plan with a single "log" action explaining why
5. Prioritize safety and user privacy
6. Break complex goals into smaller, manageable steps

Example response:
{"steps": [
    {"name": "web_search", "params": {"query": "Python tutorial"}},
    {"name": "open_url", "params": {"url": "https://python.org"}},
    {"name": "log", "params": {"message": "Opened Python tutorial website"}}
]}"""

    def _build_planning_prompt(self, goal: Goal, available_skills: list[str]) -> str:
        """Build the planning prompt for the LLM."""
        skills_text = (
            ", ".join(available_skills)
            if available_skills
            else "log, web_search, open_url"
        )

        observation_text = ""
        if goal.observation:
            observation_text = f"\nCurrent observation: {goal.observation.text[:200]}"

        return f"""Goal: {goal.description}
User ID: {goal.user_id}
Budget: {goal.budget_seconds} seconds{observation_text}

Available skills: {skills_text}

Create a step-by-step plan to achieve this goal using the available skills.
Respond with JSON only - no additional text or explanation."""

    def _parse_llm_response(self, content: str) -> dict[str, Any]:
        """Parse LLM response and extract plan data."""
        try:
            # Try to find JSON in response
            content = content.strip()

            # Look for JSON block
            if "```json" in content:
                start = content.find("```json") + 7
                end = content.find("```", start)
                content = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                content = content[start:end].strip()

            # Parse JSON
            plan_data = json.loads(content)

            # Validate structure
            if not isinstance(plan_data, dict) or "steps" not in plan_data:
                raise ValueError("Invalid plan structure")

            if not isinstance(plan_data["steps"], list):
                raise ValueError("Steps must be a list")

            return plan_data

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            logger.debug(f"Raw content: {content}")
            raise ValueError(f"Invalid JSON response: {e}")

    def _create_actions_from_plan_data(self, plan_data: dict[str, Any]) -> list[Action]:
        """Create Action objects from parsed plan data."""
        actions = []

        for i, step in enumerate(plan_data["steps"]):
            try:
                if not isinstance(step, dict):
                    logger.warning(f"Step {i} is not a dict: {step}")
                    continue

                name = step.get("name", "log")
                params = step.get("params", {})

                if not isinstance(params, dict):
                    logger.warning(f"Params for step {i} not a dict: {params}")
                    params = {"message": str(params)}

                action = Action(name=name, params=params)
                actions.append(action)

            except Exception as e:
                logger.error(f"Failed to create action from step {i}: {e}")
                # Add fallback action
                actions.append(
                    Action(
                        name="log",
                        params={"message": f"Failed to parse step {i}: {step}"},
                    )
                )

        if not actions:
            # Ensure we always have at least one action
            actions.append(
                Action(
                    name="log",
                    params={"message": "No valid actions generated from plan"},
                )
            )

        return actions

    def _create_fallback_plan(self, goal: Goal, error_reason: str) -> Plan:
        """Create a fallback plan when LLM planning fails."""
        logger.info(f"Creating fallback plan for goal: {goal.description}")

        # Simple rule-based fallback
        description_lower = goal.description.lower()

        actions = []

        if any(word in description_lower for word in ["search", "find", "look up"]):
            # Search-related goal
            query = (
                goal.description.replace("search for", "").replace("find", "").strip()
            )
            actions.append(Action(name="web_search", params={"query": query}))
        elif any(word in description_lower for word in ["open", "visit", "go to"]):
            # URL-related goal
            if "http" in description_lower:
                # Extract URL if present
                words = goal.description.split()
                url = next(
                    (word for word in words if word.startswith("http")),
                    "https://google.com",
                )
                actions.append(Action(name="open_url", params={"url": url}))
            else:
                actions.append(
                    Action(name="web_search", params={"query": goal.description})
                )
        else:
            # Generic fallback
            actions.append(
                Action(
                    name="log",
                    params={
                        "message": f"Fallback plan for: {goal.description}. Reason: {error_reason}"
                    },
                )
            )

        return Plan(goal_id=goal.id, steps=actions)

    def analyze_feedback(self, plan: Plan, feedback: dict[str, Any]) -> dict[str, Any]:
        """Analyze execution feedback for plan improvement."""
        return {
            "success_rate": feedback.get("success_rate", 0.0),
            "failed_actions": feedback.get("failed_actions", []),
            "suggestions": [
                "Consider breaking complex actions into smaller steps",
                "Add error handling for network-related actions",
                "Validate input parameters before execution",
            ],
        }
