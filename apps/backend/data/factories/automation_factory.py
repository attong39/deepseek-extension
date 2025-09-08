"""Dependency injection factory for automation module.





This module provides factory functions to create and wire up all


automation components with proper dependency injection.


"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any
import dict
import float
import guard
import learner
import list
import max
import min
import moe_canary_ratio
import ocr_languages
import openai_api_key
import openai_model
import self
import str

if TYPE_CHECKING:
    from apps.backend.core.interfaces.automation import (
        AutomationExecutor,
        AutomationPlanner,
        SafetyEngine,
    )
    from apps.backend.core.interfaces.input_control import InputController
    from apps.backend.core.interfaces.perception import OcrEngine, ScreenPerception
    from apps.backend.core.services.automation_service import AutomationService


logger = logging.getLogger(__name__)


class AutomationFactory:
    """Factory for creating automation components with dependency injection."""

    def __init__(
        self,
        openai_api_key: str,
        openai_model: str = "gpt-4o",
        ocr_languages: list[str] | None = None,
        *,
        guard: Any | None = None,
        learner: Any | None = None,
        moe_canary_ratio: float = 0.2,
    ) -> None:
        """Initialize the automation factory.





        Args:
            openai_api_key: OpenAI API key for AI planner
            openai_model: OpenAI model to use
            ocr_languages: Languages for OCR engine

        """

        self._openai_api_key = openai_api_key
        self._openai_model = openai_model
        self._ocr_languages = ocr_languages or ["en"]
        # Optional safety/learning hooks for planner
        self._guard = guard
        self._learner = learner
        self._moe_canary_ratio = max(0.0, min(1.0, float(moe_canary_ratio)))

        logger.info("AutomationFactory initialized")

    def create_screen_perception(self) -> ScreenPerception:
        """Create screen perception implementation."""

        from apps.backend.data.implementations.perception_impl import (
            ScreenPerceptionImpl,
        )

        return ScreenPerceptionImpl()

    def create_ocr_engine(self) -> OcrEngine:
        """Create OCR engine implementation."""

        from apps.backend.data.implementations.perception_impl import OcrEngineImpl

        return OcrEngineImpl(languages=self._ocr_languages)

    def create_input_controller(self) -> InputController:
        """Create input controller implementation."""

        from apps.backend.data.implementations.input_control_impl import (
            InputControllerImpl,
        )

        return InputControllerImpl()

    def create_automation_planner(self) -> AutomationPlanner:
        """Create automation planner implementation."""

        from apps.backend.data.implementations.automation_planner_impl import (
            AutomationPlannerImpl,
        )

        return AutomationPlannerImpl(
            api_key=self._openai_api_key,
            model=self._openai_model,
            guard=self._guard,
            learner=self._learner,
            moe_canary_ratio=self._moe_canary_ratio,
        )

    def create_automation_executor(
        self,
        input_controller: InputController | None = None,
        screen_perception: ScreenPerception | None = None,
    ) -> AutomationExecutor:
        """Create automation executor implementation.





        Args:


            input_controller: Optional input controller (creates new if None)


            screen_perception: Optional screen perception (creates new if None)


        """

        from apps.backend.data.implementations.automation_executor_impl import (
            AutomationExecutorImpl,
        )

        input_ctrl = input_controller or self.create_input_controller()

        screen_perc = screen_perception or self.create_screen_perception()

        return AutomationExecutorImpl(
            input_controller=input_ctrl, screen_perception=screen_perc
        )

    def create_safety_engine(self) -> SafetyEngine:
        """Create safety engine implementation."""

        from apps.backend.data.implementations.safety_engine_impl import (
            SafetyEngineImpl,
        )

        return SafetyEngineImpl()

    def create_automation_service(self) -> AutomationService:
        """Create complete automation service with all dependencies."""

        from apps.backend.core.services.automation_service import AutomationService

        # Create all components

        screen_perception = self.create_screen_perception()

        input_controller = self.create_input_controller()

        ocr_engine = self.create_ocr_engine()

        planner = self.create_automation_planner()

        executor = self.create_automation_executor(
            input_controller=input_controller, screen_perception=screen_perception
        )

        safety_engine = self.create_safety_engine()

        # Wire them together

        service = AutomationService(
            screen_perception=screen_perception,
            input_controller=input_controller,
            ocr_engine=ocr_engine,
            planner=planner,
            executor=executor,
            safety_engine=safety_engine,
        )

        logger.info("Automation service created with all dependencies")

        return service


def create_automation_service(
    openai_api_key: str,
    openai_model: str = "gpt-4o",
    ocr_languages: list[str] | None = None,
    *,
    guard: Any | None = None,
    learner: Any | None = None,
    moe_canary_ratio: float = 0.2,
) -> AutomationService:
    """Convenience function to create automation service.





    Args:


        openai_api_key: OpenAI API key


        openai_model: OpenAI model to use


        ocr_languages: Languages for OCR





    Returns:


        Fully configured automation service


    """

    factory = AutomationFactory(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        ocr_languages=ocr_languages,
        guard=guard,
        learner=learner,
        moe_canary_ratio=moe_canary_ratio,
    )

    return factory.create_automation_service()


def create_automation_components(
    openai_api_key: str,
    openai_model: str = "gpt-4o",
    ocr_languages: list[str] | None = None,
) -> dict[str, Any]:
    """Create all automation components separately.





    Args:


        openai_api_key: OpenAI API key


        openai_model: OpenAI model to use


        ocr_languages: Languages for OCR





    Returns:


        Dictionary with all components


    """

    factory = AutomationFactory(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        ocr_languages=ocr_languages,
    )

    return {
        "screen_perception": factory.create_screen_perception(),
        "input_controller": factory.create_input_controller(),
        "ocr_engine": factory.create_ocr_engine(),
        "planner": factory.create_automation_planner(),
        "executor": factory.create_automation_executor(),
        "safety_engine": factory.create_safety_engine(),
        "service": factory.create_automation_service(),
    }
