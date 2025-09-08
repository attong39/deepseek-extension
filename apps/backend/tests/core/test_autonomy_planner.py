"""
Tests cho Autonomous Planning System.

Kiểm tra:
- HybridPlanner mode switching
- LLM integration
- Rule-based fallback
- Safety validation
"""

from unittest.mock import Mock, patch

import pytest
from apps.backend.core.domain.autonomy import Action, Goal, Plan
from apps.backend.core.services.autonomy_planner import (
import Exception
import ImportError
import action
import any
import description
import dict
import isinstance
import len
import mock_llm_class
import name
import result
    HybridPlanner,
    RAGEnhancedPlanner,
    RuleBasedPlanner,
)


class TestRuleBasedPlanner:
    """Test rule-based planning functionality."""

    def test_create_simple_plan(self) -> None:
        """Test creating simple plan from goal."""
        planner = RuleBasedPlanner()
        goal = Goal(
            user_id="test_user",
            description="write hello world to file",
            budget_seconds=60,
        )

        plan = planner.create_plan(goal)

        assert plan.goal_id == goal.id
        assert len(plan.steps) > 0
        assert plan.estimated_duration_seconds == 60

        # Should include write_file action
        action_names = [action.name for action in plan.steps]
        assert "write_file" in action_names

    def test_create_complex_plan(self) -> None:
        """Test creating plan for complex goal."""
        planner = RuleBasedPlanner()
        goal = Goal(
            user_id="test_user",
            description="research AI and create summary report",
            budget_seconds=300,
        )

        plan = planner.create_plan(goal)

        assert plan.goal_id == goal.id
        assert len(plan.steps) > 1  # Should have multiple steps

        # Should include research and writing actions
        action_names = [action.name for action in plan.steps]
        assert any("search" in name or "research" in name for name in action_names)
        assert any("write" in name for name in action_names)

    def test_empty_goal_fallback(self) -> None:
        """Test fallback for unclear goals."""
        planner = RuleBasedPlanner()
        goal = Goal(user_id="test_user", description="", budget_seconds=30)

        plan = planner.create_plan(goal)

        assert plan.goal_id == goal.id
        assert len(plan.steps) == 1  # Should have fallback action
        assert plan.steps[0].name == "log_action"


class TestRAGEnhancedPlanner:
    """Test RAG-enhanced planning."""

    @pytest.mark.asyncio
    async def test_adapt_similar_plan(self) -> None:
        """Test adapting from similar successful plan."""
        mock_rag_service = Mock()
        planner = RAGEnhancedPlanner(rag_service=mock_rag_service)
        goal = Goal(
            user_id="test_user",
            description="open website and write summary",
            budget_seconds=120,
        )

        plan = await planner.create_plan(goal)

        assert plan.goal_id == goal.id
        assert len(plan.steps) > 0

        # Should have actions for both opening URL and writing
        action_names = [action.name for action in plan.steps]
        assert any("url" in name for name in action_names)
        assert any("write" in name for name in action_names)


class TestHybridPlanner:
    """Test hybrid planning system."""

    def test_initialization_rule_mode(self) -> None:
        """Test hybrid planner initialization in rule mode."""
        planner = HybridPlanner(mode="rule")

        assert planner.mode == "rule"
        assert planner.rule_planner is not None
        assert planner.llm_planner is None

    @patch.dict("os.environ", {"PLANNER_MODE": "llm"})
    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_initialization_llm_mode(self, mock_llm_class) -> None:
        """Test hybrid planner initialization in LLM mode."""
        mock_llm_instance = Mock()
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner()

        assert planner.mode == "llm"
        assert planner.llm_planner == mock_llm_instance
        mock_llm_class.from_env.assert_called_once()

    @patch.dict("os.environ", {"PLANNER_MODE": "hybrid"})
    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_initialization_hybrid_mode(self, mock_llm_class) -> None:
        """Test hybrid planner initialization in hybrid mode."""
        mock_llm_instance = Mock()
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner()

        assert planner.mode == "hybrid"
        assert planner.llm_planner == mock_llm_instance

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_llm_import_failure_fallback(self, mock_llm_class) -> None:
        """Test fallback to rule mode when LLM import fails."""
        mock_llm_class.from_env.side_effect = ImportError("OpenAI not available")

        planner = HybridPlanner(mode="llm")

        # Should fallback to rule mode
        assert planner.mode == "rule"
        assert planner.llm_planner is None

    def test_rule_mode_planning(self) -> None:
        """Test planning in rule mode."""
        planner = HybridPlanner(mode="rule")
        goal = Goal(user_id="test_user", description="simple task", budget_seconds=30)

        plan = planner.create_plan(goal)

        assert plan.goal_id == goal.id
        assert len(plan.steps) > 0

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_llm_mode_planning(self, mock_llm_class) -> None:
        """Test planning in LLM mode."""
        # Setup LLM mock
        mock_llm_instance = Mock()
        mock_plan = Plan(
            goal_id="test-goal",
            steps=[Action(name="llm_action", params={"test": "value"})],
            estimated_duration_seconds=60,
        )
        mock_llm_instance.create_plan.return_value = mock_plan
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner(mode="llm")
        goal = Goal(
            user_id="test_user", description="complex analysis task", budget_seconds=60
        )

        plan = planner.create_plan(goal)

        assert plan == mock_plan
        mock_llm_instance.create_plan.assert_called_once_with(goal)

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_llm_failure_fallback(self, mock_llm_class) -> None:
        """Test fallback to rule planning when LLM fails."""
        # Setup LLM mock to fail
        mock_llm_instance = Mock()
        mock_llm_instance.create_plan.side_effect = Exception("LLM service unavailable")
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner(mode="llm")
        goal = Goal(user_id="test_user", description="test goal", budget_seconds=30)

        plan = planner.create_plan(goal)

        # Should fallback to rule-based planning
        assert plan.goal_id == goal.id
        assert len(plan.steps) > 0
        # Should be rule-based plan (simple action)
        assert plan.steps[0].name in ["log_action", "write_file", "open_url"]

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_hybrid_mode_simple_goal(self, mock_llm_class) -> None:
        """Test hybrid mode with simple goal (should use rule-based)."""
        mock_llm_instance = Mock()
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner(mode="hybrid")
        goal = Goal(
            user_id="test_user",
            description="simple",  # Short, simple goal
            budget_seconds=30,
        )

        plan = planner.create_plan(goal)

        # Should use rule-based for simple goal
        assert plan.goal_id == goal.id
        # LLM should not be called for simple goals
        mock_llm_instance.create_plan.assert_not_called()

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_hybrid_mode_complex_goal(self, mock_llm_class) -> None:
        """Test hybrid mode with complex goal (should try LLM first)."""
        # Setup LLM mock
        mock_llm_instance = Mock()
        mock_plan = Plan(
            goal_id="test-goal",
            steps=[Action(name="complex_action", params={"analysis": "deep"})],
            estimated_duration_seconds=180,
        )
        mock_llm_instance.create_plan.return_value = mock_plan
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner(mode="hybrid")
        goal = Goal(
            user_id="test_user",
            description=(
                "analyze complex data patterns and create detailed research report "
                "with multiple sections"
            ),
            budget_seconds=180,
        )

        plan = planner.create_plan(goal)

        # Should use LLM for complex goal
        assert plan == mock_plan
        mock_llm_instance.create_plan.assert_called_once_with(goal)

    def test_set_mode_valid(self) -> None:
        """Test changing planner mode at runtime."""
        planner = HybridPlanner(mode="rule")

        planner.set_mode("hybrid")
        assert planner.mode == "hybrid"

        planner.set_mode("llm")
        assert planner.mode == "llm"

        planner.set_mode("rule")
        assert planner.mode == "rule"

    def test_set_mode_invalid(self) -> None:
        """Test invalid mode change."""
        planner = HybridPlanner(mode="rule")
        original_mode = planner.mode

        planner.set_mode("invalid_mode")

        # Mode should remain unchanged
        assert planner.mode == original_mode

    def test_get_capabilities(self) -> None:
        """Test getting planner capabilities."""
        planner = HybridPlanner(mode="rule")

        capabilities = planner.get_capabilities()

        assert isinstance(capabilities, dict)
        assert "mode" in capabilities
        assert "rule_planner_available" in capabilities
        assert "llm_planner_available" in capabilities
        assert "supported_modes" in capabilities
        assert "skill_count" in capabilities

        assert capabilities["mode"] == "rule"
        assert capabilities["rule_planner_available"] is True
        assert capabilities["llm_planner_available"] is False
        assert "rule" in capabilities["supported_modes"]

    @patch("zeta_vn.core.services.autonomy_planner.LLMPlanner")
    def test_get_capabilities_with_llm(self, mock_llm_class) -> None:
        """Test capabilities when LLM is available."""
        mock_llm_instance = Mock()
        mock_llm_class.from_env.return_value = mock_llm_instance

        planner = HybridPlanner(mode="llm")
        capabilities = planner.get_capabilities()

        assert capabilities["llm_planner_available"] is True
        assert "llm" in capabilities["supported_modes"]
        assert "hybrid" in capabilities["supported_modes"]


class TestComplexityDetection:
    """Test goal complexity detection logic."""

    def test_is_complex_goal_long_description(self) -> None:
        """Test complexity detection for long descriptions."""
        planner = HybridPlanner(mode="hybrid")

        # Long description should be considered complex
        _ = planner._is_complex_goal(
            "This is a very long and detailed description that contains many words and concepts"
        )
        assert result is True

    def test_is_complex_goal_analysis_keywords(self) -> None:
        """Test complexity detection for analysis keywords."""
        planner = HybridPlanner(mode="hybrid")

        analysis_descriptions = [
            "analyze the data patterns",
            "compare different approaches",
            "research the topic thoroughly",
            "investigate the root cause",
            "understand the implications",
            "explain the complex relationships",
        ]

        for description in analysis_descriptions:
            _ = planner._is_complex_goal(description)
            assert result is True, f"'{description}' should be complex"

    def test_is_complex_goal_multiple_tasks(self) -> None:
        """Test complexity detection for multiple tasks."""
        planner = HybridPlanner(mode="hybrid")

        multi_task_descriptions = [
            "read file and write summary",
            "download data & analyze results",
            "research topic and create report",
        ]

        for description in multi_task_descriptions:
            _ = planner._is_complex_goal(description)
            assert result is True, f"'{description}' should be complex"

    def test_is_complex_goal_questions(self) -> None:
        """Test complexity detection for questions."""
        planner = HybridPlanner(mode="hybrid")

        question_descriptions = [
            "What are the implications?",
            "How does this work?",
            "Why did this happen?",
        ]

        for description in question_descriptions:
            _ = planner._is_complex_goal(description)
            assert result is True, f"'{description}' should be complex"

    def test_is_complex_goal_simple_tasks(self) -> None:
        """Test complexity detection for simple tasks."""
        planner = HybridPlanner(mode="hybrid")

        simple_descriptions = ["write file", "open URL", "simple task", "log message"]

        for description in simple_descriptions:
            _ = planner._is_complex_goal(description)
            assert result is False, f"'{description}' should be simple"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
