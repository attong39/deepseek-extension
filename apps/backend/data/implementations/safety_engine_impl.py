"""Rule-based safety engine implementation.





This module provides safety monitoring and validation for automation


actions to prevent dangerous or unintended operations.


"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING
import Exception
import action_type
import area
import bool
import config
import e
import isinstance
import key
import pattern
import self
import step
import str
import target
import value
import x
import y
import zone

if TYPE_CHECKING:
    from apps.backend.core.domain.value_objects.automation import (
        AutomationStep,
        SafetyConfig,
        SafetyResult,
    )


logger = logging.getLogger(__name__)


class SafetyEngineImpl:
    """Rule-based implementation of automation safety engine."""

    def __init__(self) -> None:
        """Initialize the safety engine."""

        self._dangerous_patterns = [
            r"format\s+c:",
            r"del\s+/[sS]",
            r"rm\s+-rf\s+/",
            r"shutdown",
            r"reboot",
            r"taskkill",
            r"kill\s+-9",
            r"sudo\s+rm",
            r"registry\s+delete",
        ]

        self._system_areas = [
            # Windows system areas (approximate)
            {"x1": 0, "y1": 0, "x2": 100, "y2": 50},  # Top-left corner
            {"x1": 0, "y1": 0, "x2": 1920, "y2": 40},  # Taskbar area
        ]

        logger.info("SafetyEngineImpl initialized")

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

        try:
            logger.debug(f"Checking safety for step: {step.action.value}")

            violations = []

            warnings = []

            # Check action rate limits

            if not await self._check_rate_limits(step, config):
                violations.append("Action rate limit exceeded")

            # Check dangerous content

            dangerous_content = self._check_dangerous_content(step)

            if dangerous_content:
                violations.append(f"Dangerous content detected: {dangerous_content}")

            # Check system areas

            if self._check_system_areas(step, config):
                warnings.append("Action targets system area")

            # Check application restrictions

            if not self._check_allowed_apps(step, config):
                violations.append("Action targets restricted application")

            # Check confirmation requirements

            if self._requires_confirmation(step, config):
                warnings.append("Action requires user confirmation")

            # Create result

            from apps.backend.core.domain.value_objects.automation import SafetyResult

            if violations:
                return SafetyResult.unsafe(
                    violations=violations, recommended_action="abort"
                )

            else:
                return SafetyResult.safe(warnings=warnings)

        except Exception as e:
            logger.error(f"Safety check failed: {e}")

            from apps.backend.core.domain.value_objects.automation import SafetyResult

            return SafetyResult.unsafe(
                violations=[f"Safety check error: {e}"], recommended_action="abort"
            )

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

        try:
            # Always allow basic actions

            safe_actions = {"move", "screenshot", "wait"}

            if action_type.lower() in safe_actions:
                return True

            # Check target for dangerous patterns if provided

            if target:
                for pattern in self._dangerous_patterns:
                    if re.search(pattern, target, re.IGNORECASE):
                        logger.warning(
                            f"Dangerous pattern detected in target: {pattern}"
                        )

                        return False

            # Default to allowing most actions with warnings

            return True

        except Exception as e:
            logger.error(f"Action check failed: {e}")

            return False

    async def _check_rate_limits(
        self, step: AutomationStep, config: SafetyConfig
    ) -> bool:
        """Check if action respects rate limits."""

        # TODO: Implement actual rate limiting with time tracking

        # For now, just check if the configured limit is reasonable

        return config.max_actions_per_minute <= 60

    def _check_dangerous_content(self, step: AutomationStep) -> str | None:
        """Check for dangerous content in step parameters.





        Returns:


            Description of dangerous content if found, None otherwise


        """

        # Check target text

        if step.target:
            for pattern in self._dangerous_patterns:
                if re.search(pattern, step.target, re.IGNORECASE):
                    return f"Pattern '{pattern}' in target"

        # Check parameters

        for key, value in step.parameters.items():
            if isinstance(value, str):
                for pattern in self._dangerous_patterns:
                    if re.search(pattern, value, re.IGNORECASE):
                        return f"Pattern '{pattern}' in {key}"

        return None

    def _check_system_areas(self, step: AutomationStep, config: SafetyConfig) -> bool:
        """Check if action targets system areas.





        Returns:


            True if action targets system area


        """

        if not step.target_point:
            return False

        x, y = step.target_point.x, step.target_point.y

        # Check configured danger zones

        for zone in config.danger_zones:
            if zone.x <= x <= zone.x + zone.w and zone.y <= y <= zone.y + zone.h:
                return True

        # Check predefined system areas

        for area in self._system_areas:
            if area["x1"] <= x <= area["x2"] and area["y1"] <= y <= area["y2"]:
                return True

        return False

    def _check_allowed_apps(self, step: AutomationStep, config: SafetyConfig) -> bool:
        """Check if action targets allowed applications.





        Returns:


            True if action is allowed for target application


        """

        # If no app restrictions configured, allow all

        if not config.allowed_apps:
            return True

        # TODO: Implement actual window detection to check current app

        # For now, always allow if restrictions are configured

        return True

    def _requires_confirmation(
        self, step: AutomationStep, config: SafetyConfig
    ) -> bool:
        """Check if action requires user confirmation.





        Returns:


            True if confirmation is required


        """

        if not config.require_confirmation_for:
            return False

        return step.action in config.require_confirmation_for
