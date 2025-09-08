#!/usr/bin/env python3
"""
🤖 Planner Service Implementation

Concrete implementation của IPlanner cho Autonomous system:
- RuleBasedPlanner: Rule-based planner tối giản cho demo
- RAGEnhancedPlanner: Planner tích hợp RAG (future)
- HybridPlanner: Kết hợp rule-based + RAG + LLM
- LLMPlanner: AI-powered planner using OpenAI

Tuân thủ: fallback safety, deterministic demo, extensible architecture
"""

from __future__ import annotations

import logging
import os
import re
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.autonomy import Action, Goal, Observation, Plan
from apps.backend.core.interfaces.autonomy import PlannerError
import Exception
import ImportError
import any
import best_pattern
import bool
import context
import description
import dict
import e
import fallback_planner
import fb
import feedback
import float
import goal
import keyword
import len
import list
import llm_planner
import min
import mode
import observation
import pattern
import rag_service
import result
import rule_planner
import self
import set
import similar_plan
import skill_name
import str
import word
import x

if TYPE_CHECKING:
    from apps.backend.core.services.planner_llm import LLMPlanner


logger = logging.getLogger(__name__)


class RuleBasedPlanner:
    """
    Rule-based planner đơn giản cho demo.

    Chuyển đổi goal text thành sequence of actions dựa trên patterns.
    Deterministic và testable - thích hợp cho MVP.
    """

    def __init__(self) -> None:
        self.goal_patterns = self._load_goal_patterns()
        self.skill_mapping = self._load_skill_mapping()

    def _load_goal_patterns(self) -> list[dict[str, Any]]:
        """Load patterns để nhận diện goals."""
        return [
            {
                "keywords": ["mở", "open", "browse", "trang", "website", "url"],
                "intent": "open_website",
                "skills": ["open_url"],
                "confidence": 0.8,
            },
            {
                "keywords": [
                    "ghi",
                    "write",
                    "tạo",
                    "create",
                    "file",
                    "note",
                    "document",
                ],
                "intent": "create_document",
                "skills": ["write_file"],
                "confidence": 0.7,
            },
            {
                "keywords": ["search", "tìm", "tìm kiếm", "find", "query"],
                "intent": "search_information",
                "skills": ["web_search", "rag_query"],
                "confidence": 0.6,
            },
            {
                "keywords": ["email", "mail", "gửi", "send"],
                "intent": "send_communication",
                "skills": ["compose_email"],
                "confidence": 0.5,
            },
            {
                "keywords": ["screenshot", "capture", "chụp", "màn hình"],
                "intent": "capture_screen",
                "skills": ["take_screenshot"],
                "confidence": 0.7,
            },
            {
                "keywords": ["đọc", "read", "parse", "extract"],
                "intent": "read_content",
                "skills": ["read_file", "extract_text"],
                "confidence": 0.6,
            },
        ]

    def _load_skill_mapping(self) -> dict[str, dict[str, Any]]:
        """Mapping từ skill name → metadata."""
        return {
            "open_url": {
                "description": "Mở URL trong browser",
                "params": {"url": "string"},
                "safety_level": "medium",
            },
            "write_file": {
                "description": "Ghi nội dung vào file",
                "params": {"path": "string", "content": "string"},
                "safety_level": "high",
            },
            "web_search": {
                "description": "Tìm kiếm trên web",
                "params": {"query": "string"},
                "safety_level": "low",
            },
            "rag_query": {
                "description": "Query RAG knowledge base",
                "params": {"query": "string", "k": "int"},
                "safety_level": "low",
            },
            "compose_email": {
                "description": "Soạn email",
                "params": {"to": "string", "subject": "string", "body": "string"},
                "safety_level": "high",
            },
            "take_screenshot": {
                "description": "Chụp màn hình",
                "params": {"save_path": "string"},
                "safety_level": "medium",
            },
            "read_file": {
                "description": "Đọc nội dung file",
                "params": {"path": "string"},
                "safety_level": "medium",
            },
            "extract_text": {
                "description": "Trích xuất text từ document",
                "params": {"source": "string", "format": "string"},
                "safety_level": "low",
            },
            "log_action": {
                "description": "Log thông tin (fallback)",
                "params": {"message": "string"},
                "safety_level": "low",
            },
        }

    def create_plan(
        self,
        goal: Goal,
        observation: Observation | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """
        Tạo plan từ goal text dựa trên rules.

        Algorithm:
        1. Parse goal text để tìm intent
        2. Map intent → skills
        3. Extract parameters từ text
        4. Tạo sequence of actions
        5. Add fallback nếu không match
        """
        try:
            goal_text = goal.description.lower().strip()
            logger.info(f"Planning for goal: {goal_text}")

            # 1. Find matching patterns
            matched_patterns = []
            for pattern in self.goal_patterns:
                score = self._calculate_pattern_score(goal_text, pattern)
                if score > 0.3:  # threshold
                    matched_patterns.append((pattern, score))

            # Sort by confidence score
            matched_patterns.sort(key=lambda x: x[1], reverse=True)

            # 2. Generate actions từ best pattern
            actions: list[Action] = []

            if matched_patterns:
                best_pattern, score = matched_patterns[0]
                logger.info(
                    f"Matched pattern: {best_pattern['intent']} (score={score:.2f})"
                )

                for skill_name in best_pattern["skills"]:
                    if skill_name in self.skill_mapping:
                        # Extract parameters for this skill
                        params = self._extract_skill_params(
                            goal_text, skill_name, observation
                        )

                        action = Action(
                            name=skill_name,
                            params=params,
                        )
                        actions.append(action)

            # 3. Fallback nếu không có pattern match
            if not actions:
                logger.warning("No patterns matched, adding fallback action")
                actions.append(
                    Action(
                        name="log_action",
                        params={"message": f"Goal received: {goal.description}"},
                    )
                )

            # 4. Tạo plan
            plan = Plan(
                goal_id=goal.id,
                steps=actions,
                estimated_duration_seconds=min(goal.budget_seconds, len(actions) * 10),
            )

            logger.info(f"Created plan with {len(actions)} actions")
            return plan

        except Exception as e:
            logger.error(f"Planning failed: {e}")
            raise PlannerError(f"Cannot create plan: {e}")

    async def refine_plan(
        self,
        plan: Plan,
        feedback: list[dict[str, Any]],
    ) -> Plan:
        """
        Tinh chỉnh plan dựa trên feedback.

        Simple implementation: remove failed actions, add retry logic.
        """
        if not feedback:
            return plan

        # Analyze feedback
        failed_skills = set()
        for fb in feedback:
            if not fb.get("success", True):
                action_name = fb.get("action", "")
                if action_name:
                    failed_skills.add(action_name)

        # Remove failed skills from future plans
        if failed_skills:
            plan.steps = [
                action for action in plan.steps if action.name not in failed_skills
            ]
            logger.info(f"Refined plan: removed {len(failed_skills)} failed skills")

        return plan

    def _calculate_pattern_score(
        self, goal_text: str, pattern: dict[str, Any]
    ) -> float:
        """Tính điểm match giữa goal text và pattern."""
        keywords = pattern["keywords"]
        base_confidence = pattern.get("confidence", 0.5)

        # Count keyword matches
        matched_keywords = 0
        for keyword in keywords:
            if keyword.lower() in goal_text:
                matched_keywords += 1

        if not keywords:
            return 0.0

        # Calculate score
        keyword_score = matched_keywords / len(keywords)
        final_score = keyword_score * base_confidence

        return final_score

    def _extract_skill_params(
        self,
        goal_text: str,
        skill_name: str,
        observation: Observation | None,
    ) -> dict[str, Any]:
        """Extract parameters cho skill từ goal text và observation."""
        params: dict[str, Any] = {}

        if skill_name == "open_url":
            # Try to extract URL from text
            url_match = re.search(r"https?://[^\s]+", goal_text)
            if url_match:
                params["url"] = url_match.group(0)
            else:
                # Default URL or extract from keywords
                if any(word in goal_text for word in ["google", "search"]):
                    params["url"] = "https://google.com"
                else:
                    params["url"] = "https://example.org"

        elif skill_name == "write_file":
            # Extract filename and content
            if "note" in goal_text:
                params["path"] = "note.txt"
            elif "file" in goal_text:
                params["path"] = "output.txt"
            else:
                params["path"] = "document.txt"

            params["content"] = goal_text  # Use goal as content

        elif skill_name == "web_search":
            # Extract search query
            query = goal_text.replace("tìm", "").replace("search", "").strip()
            params["query"] = query or "information"

        elif skill_name == "rag_query":
            query = goal_text.replace("query", "").replace("hỏi", "").strip()
            params["query"] = query or goal_text
            params["k"] = 5

        elif skill_name == "take_screenshot":
            params["save_path"] = "screenshot.png"

        elif skill_name == "log_action":
            params["message"] = goal_text

        # Add observation context if available
        if observation and observation.text:
            params["context"] = observation.text[:200]  # truncated

        return params


class RAGEnhancedPlanner:
    """
    Planner tích hợp RAG cho planning thông minh hơn.

    Sử dụng RAG để tìm similar goals và successful plans từ history.
    """

    def __init__(
        self,
        rag_service: Any,  # RAGService từ existing implementation
        fallback_planner: RuleBasedPlanner | None = None,
    ) -> None:
        self.rag_service = rag_service
        self.fallback_planner = fallback_planner or RuleBasedPlanner()

    async def create_plan(
        self,
        goal: Goal,
        observation: Observation | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """
        Tạo plan với RAG enhancement.

        1. Query RAG cho similar goals/plans
        2. Adapt successful patterns
        3. Fallback to rule-based nếu RAG không có kết quả tốt
        """
        try:
            # Query RAG for similar goals
            similar_plans = await self._query_similar_plans(goal.description)

            if similar_plans:
                logger.info(f"Found {len(similar_plans)} similar plans from RAG")
                # Adapt best similar plan
                plan = await self._adapt_similar_plan(
                    goal, similar_plans[0], observation
                )
                return plan
            else:
                logger.info("No similar plans found, using fallback planner")
                return await self.fallback_planner.create_plan(
                    goal, observation, context
                )

        except Exception as e:
            logger.warning(f"RAG planning failed, using fallback: {e}")
            return await self.fallback_planner.create_plan(goal, observation, context)

    async def refine_plan(
        self,
        plan: Plan,
        feedback: list[dict[str, Any]],
    ) -> Plan:
        """Refine plan với RAG feedback."""
        # Combine RAG insight với fallback logic
        return await self.fallback_planner.refine_plan(plan, feedback)

    async def _query_similar_plans(self, goal_text: str) -> list[dict[str, Any]]:
        """Query RAG cho similar successful plans."""
        try:
            # Use existing RAG service
            results = await self.rag_service.query(goal_text, k=3)

            # Filter for plan-related results
            similar_plans = []
            for result in results:
                if "plan" in result.get("content", "").lower():
                    similar_plans.append(result)

            return similar_plans

        except Exception as e:
            logger.warning(f"RAG query failed: {e}")
            return []

    async def _adapt_similar_plan(
        self,
        goal: Goal,
        similar_plan: dict[str, Any],
        observation: Observation | None,
    ) -> Plan:
        """Adapt similar plan cho current goal."""
        # Simple adaptation: extract actions from similar plan content
        content = similar_plan.get("content", "")

        # Parse actions from content (simplified)
        actions = []
        if "open_url" in content:
            actions.append(
                Action(name="open_url", params={"url": "https://example.org"})
            )
        if "write_file" in content:
            actions.append(
                Action(
                    name="write_file",
                    params={"path": "adapted.txt", "content": goal.description},
                )
            )

        # Fallback action
        if not actions:
            actions.append(
                Action(
                    name="log_action",
                    params={
                        "message": f"Adapted from similar plan: {goal.description}"
                    },
                )
            )

        return Plan(
            goal_id=goal.id,
            steps=actions,
            estimated_duration_seconds=goal.budget_seconds,
        )


class HybridPlanner:
    """
    Hybrid planner với khả năng chuyển đổi giữa rule-based và LLM mode.

    Modes:
    - rule: Rule-based planning (default, fast, deterministic)
    - llm: LLM-powered planning (smart, context-aware)
    - hybrid: Combine both approaches
    """

    def __init__(
        self,
        rule_planner: RuleBasedPlanner | None = None,
        llm_planner: LLMPlanner | None = None,
        mode: str = "rule",
    ) -> None:
        self.rule_planner = rule_planner or RuleBasedPlanner()
        self.llm_planner = llm_planner
        self.mode = os.getenv("PLANNER_MODE", mode).lower()

        # Initialize LLM planner if needed
        if self.mode in ["llm", "hybrid"] and self.llm_planner is None:
            try:
                from apps.backend.core.services.planner_llm import LLMPlanner

                self.llm_planner = LLMPlanner.from_env()
                logger.info(f"Initialized LLM planner for mode: {self.mode}")
            except ImportError as e:
                logger.warning(f"Could not import LLM planner: {e}")
                self.mode = "rule"  # Fallback to rule-based
            except Exception as e:
                logger.warning(f"Failed to initialize LLM planner: {e}")
                self.mode = "rule"  # Fallback to rule-based

    def create_plan(
        self,
        goal: Goal,
        observation: Observation | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """Create plan using the configured mode."""
        try:
            if self.mode == "llm" and self.llm_planner:
                logger.info(f"Using LLM planning for goal: {goal.description}")
                return self.llm_planner.create_plan(goal)

            elif self.mode == "hybrid" and self.llm_planner:
                logger.info(f"Using hybrid planning for goal: {goal.description}")
                return self._create_hybrid_plan(goal, observation, context)

            else:
                logger.info(f"Using rule-based planning for goal: {goal.description}")
                return self.rule_planner.create_plan(goal, observation, context)

        except Exception as e:
            logger.error(f"Planning failed with mode {self.mode}: {e}")
            # Always fallback to rule-based planning
            logger.info("Falling back to rule-based planning")
            return self.rule_planner.create_plan(goal, observation, context)

    def _create_hybrid_plan(
        self,
        goal: Goal,
        observation: Observation | None = None,
        context: dict[str, Any] | None = None,
    ) -> Plan:
        """Create plan using hybrid approach."""
        try:
            # Try LLM first for complex goals
            if self._is_complex_goal(goal.description):
                logger.debug("Complex goal detected, trying LLM planning")
                llm_plan = self.llm_planner.create_plan(goal)

                # Validate LLM plan with rule-based knowledge
                if self._validate_plan_with_rules(llm_plan):
                    logger.info("LLM plan validated, using hybrid approach")
                    return llm_plan
                else:
                    logger.warning("LLM plan failed validation, using rule-based")

            # Fallback to rule-based
            return self.rule_planner.create_plan(goal, observation, context)

        except Exception as e:
            logger.error(f"Hybrid planning failed: {e}")
            return self.rule_planner.create_plan(goal, observation, context)

    def _is_complex_goal(self, description: str) -> bool:
        """Determine if goal is complex enough to benefit from LLM."""
        complex_indicators = [
            len(description.split()) > 10,  # Long description
            any(
                word in description.lower()
                for word in [
                    "analyze",
                    "compare",
                    "research",
                    "investigate",
                    "understand",
                    "explain",
                    "summarize",
                    "complex",
                ]
            ),
            "and" in description.lower() or "&" in description,  # Multiple sub-goals
            "?" in description,  # Questions
        ]

        return any(complex_indicators)

    def _validate_plan_with_rules(self, plan: Plan) -> bool:
        """Validate LLM-generated plan using rule-based knowledge."""
        try:
            if not plan.steps:
                return False

            # Check if all skills exist in rule planner's mapping
            known_skills = set(self.rule_planner.skill_mapping.keys())
            plan_skills = {action.name for action in plan.steps}

            # Allow plan if most skills are known
            known_ratio = len(plan_skills.intersection(known_skills)) / len(plan_skills)

            return known_ratio >= 0.7  # At least 70% known skills

        except Exception as e:
            logger.error(f"Plan validation failed: {e}")
            return False

    def set_mode(self, mode: str) -> None:
        """Change planning mode at runtime."""
        if mode.lower() in ["rule", "llm", "hybrid"]:
            self.mode = mode.lower()
            logger.info(f"Planning mode changed to: {self.mode}")
        else:
            logger.warning(f"Invalid mode: {mode}, keeping current mode: {self.mode}")

    def get_capabilities(self) -> dict[str, Any]:
        """Get current planner capabilities."""
        return {
            "mode": self.mode,
            "rule_planner_available": self.rule_planner is not None,
            "llm_planner_available": self.llm_planner is not None,
            "supported_modes": ["rule", "llm", "hybrid"]
            if self.llm_planner
            else ["rule"],
            "skill_count": len(self.rule_planner.skill_mapping)
            if self.rule_planner
            else 0,
        }
