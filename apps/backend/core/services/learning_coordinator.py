"""Learning Coordinator Service.





This module provides the learning coordination service for managing


AI agent learning processes, model updates, and knowledge integration.


"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent
from apps.backend.core.domain.entities.memory import Memory
from apps.backend.core.exceptions.business_exceptions import (
import Exception
import agent
import agent_id
import agent_repository
import any
import bool
import data
import dict
import e
import enabled
import experience_type
import feedback
import float
import hasattr
import int
import len
import list
import memories
import memory
import memory_repository
import metric_name
import metrics
import min
import name
import optimization_type
import outcomes
import p
import priority
import recommendation
import self
import session
import session_type
import setattr
import start_time
import str
import strategy
import strategy_type
import sum
import value
    BusinessException,
    EntityNotFoundError,
)
from apps.backend.core.interfaces.repositories import AgentRepository, MemoryRepository

logger = logging.getLogger(__name__)


class LearningMetrics:
    """Metrics for learning performance tracking."""

    def __init__(self) -> None:
        """Initialize learning metrics."""

        self.accuracy: float = 0.0

        self.response_time: float = 0.0

        self.user_satisfaction: float = 0.0

        self.task_completion_rate: float = 0.0

        self.error_rate: float = 0.0

        self.learning_rate: float = 0.0

        self.knowledge_retention: float = 0.0

        self.adaptation_speed: float = 0.0

    def to_dict(self) -> dict[str, float]:
        """Convert metrics to dictionary."""

        return {
            "accuracy": self.accuracy,
            "response_time": self.response_time,
            "user_satisfaction": self.user_satisfaction,
            "task_completion_rate": self.task_completion_rate,
            "error_rate": self.error_rate,
            "learning_rate": self.learning_rate,
            "knowledge_retention": self.knowledge_retention,
            "adaptation_speed": self.adaptation_speed,
        }


class LearningStrategy:
    """Learning strategy configuration."""

    def __init__(
        self,
        strategy_type: str,
        parameters: dict[str, Any],
        priority: int = 1,
        enabled: bool = True,
    ) -> None:
        """Initialize learning strategy.





        Args:


            strategy_type: Type of learning strategy.


            parameters: Strategy parameters.


            priority: Strategy priority.


            enabled: Whether strategy is enabled.


        """

        self.strategy_type = strategy_type

        self.parameters = parameters

        self.priority = priority

        self.enabled = enabled


class LearningSession:
    """Learning session tracking."""

    def __init__(
        self,
        agent_id: UUID,
        session_type: str,
        start_time: datetime | None = None,
    ) -> None:
        """Initialize learning session.





        Args:


            agent_id: ID of the learning agent.


            session_type: Type of learning session.


            start_time: Session start time.


        """

        self.agent_id = agent_id

        self.session_type = session_type

        self.start_time = start_time or datetime.now(UTC)

        self.end_time: datetime | None = None

        self.metrics = LearningMetrics()

        self.experiences: list[dict[str, Any]] = []

        self.outcomes: dict[str, Any] = {}

        self.status = "active"

    def add_experience(self, experience: dict[str, Any]) -> None:
        """Add learning experience to session."""

        experience["timestamp"] = datetime.now(UTC).isoformat()

        self.experiences.append(experience)

    def complete_session(self, outcomes: dict[str, Any]) -> None:
        """Complete the learning session."""

        self.end_time = datetime.now(UTC)

        self.outcomes = outcomes

        self.status = "completed"

    def get_duration(self) -> timedelta:
        """Get session duration."""

        end_time = self.end_time or datetime.now(UTC)

        return end_time - self.start_time


class LearningCoordinator:
    """Service for coordinating AI agent learning processes."""

    def __init__(
        self,
        agent_repository: AgentRepository,
        memory_repository: MemoryRepository,
    ) -> None:
        """Initialize learning coordinator.





        Args:


            agent_repository: Repository for agent management.


            memory_repository: Repository for memory management.


        """

        self.agent_repository = agent_repository

        self.memory_repository = memory_repository

        self.active_sessions: dict[UUID, LearningSession] = {}

        self.learning_strategies: dict[str, LearningStrategy] = {}

        self._initialize_default_strategies()

    def _get_current_time(self) -> datetime:
        """Get current UTC time."""

        return datetime.now(UTC)

    def _initialize_default_strategies(self) -> None:
        """Initialize default learning strategies."""

        self.learning_strategies = {
            "reinforcement": LearningStrategy(
                strategy_type="reinforcement",
                parameters={
                    "learning_rate": 0.1,
                    "discount_factor": 0.99,
                    "exploration_rate": 0.1,
                },
            ),
            "supervised": LearningStrategy(
                strategy_type="supervised",
                parameters={
                    "batch_size": 32,
                    "epochs": 10,
                    "validation_split": 0.2,
                },
            ),
            "unsupervised": LearningStrategy(
                strategy_type="unsupervised",
                parameters={
                    "clustering_method": "kmeans",
                    "num_clusters": 5,
                    "feature_extraction": "pca",
                },
            ),
            "online": LearningStrategy(
                strategy_type="online",
                parameters={
                    "update_frequency": "real_time",
                    "memory_window": 1000,
                    "adaptation_threshold": 0.05,
                },
            ),
        }

    async def start_learning_session(
        self,
        agent_id: UUID,
        session_type: str,
        strategy: str | None = None,
        parameters: dict[str, Any] | None = None,
    ) -> LearningSession:
        """Start a new learning session for an agent.





        Args:


            agent_id: ID of the agent to train.


            session_type: Type of learning session.


            strategy: Learning strategy to use.


            parameters: Additional parameters.





        Returns:


            Created learning session.





        Raises:


            EntityNotFoundError: If agent not found.


            ValidationError: If invalid parameters.


        """

        try:
            logger.info(f"Starting learning session for agent {agent_id}")

            # Validate agent exists

            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise EntityNotFoundError(f"Agent not found: {agent_id}")

            # Check if agent already has active session

            if agent_id in self.active_sessions:
                logger.warning(f"Agent {agent_id} already has active learning session")

                self.end_learning_session(agent_id)

            # Create new learning session

            _ = LearningSession(
                agent_id=agent_id,
                session_type=session_type,
            )

            # Configure learning strategy

            if strategy and strategy in self.learning_strategies:
                strategy_config = self.learning_strategies[strategy]

                session.outcomes["strategy"] = {
                    "type": strategy_config.strategy_type,
                    "parameters": strategy_config.parameters,
                }

            # Apply custom parameters

            if parameters:
                session.outcomes.setdefault("parameters", {}).update(parameters)

            self.active_sessions[agent_id] = session

            logger.info(
                f"Started learning session: {session_type} for agent {agent_id}"
            )

            return session

        except Exception as e:
            logger.error(f"Failed to start learning session: {e}")

            raise BusinessException(f"Failed to start learning session: {e!s}") from e

    def end_learning_session(
        self,
        agent_id: UUID,
        outcomes: dict[str, Any] | None = None,
    ) -> LearningSession | None:
        """End an active learning session.





        Args:


            agent_id: ID of the agent.


            outcomes: Session outcomes and results.





        Returns:


            Completed learning session or None if no active session.


        """

        try:
            if agent_id not in self.active_sessions:
                logger.warning(f"No active learning session for agent {agent_id}")

                return None

            _ = self.active_sessions[agent_id]

            session.complete_session(outcomes or {})

            # Remove from active sessions

            del self.active_sessions[agent_id]

            # Log session completion

            duration = session.get_duration()

            logger.info(
                f"Completed learning session for agent {agent_id}: "
                f"{session.session_type} (duration: {duration})"
            )

            # Store session results

            self._store_learning_results(session)

            return session

        except Exception as e:
            logger.error(f"Failed to end learning session: {e}")

            raise BusinessException(f"Failed to end learning session: {e!s}") from e

    def add_learning_experience(
        self,
        agent_id: UUID,
        experience_type: str,
        data: dict[str, Any],
        feedback: dict[str, Any] | None = None,
    ) -> bool:
        """Add a learning experience to an active session.





        Args:


            agent_id: ID of the agent.


            experience_type: Type of experience.


            data: Experience data.


            feedback: Optional feedback data.





        Returns:


            True if experience was added successfully.


        """

        try:
            if agent_id not in self.active_sessions:
                logger.warning(f"No active learning session for agent {agent_id}")

                return False

            _ = self.active_sessions[agent_id]

            experience = {
                "type": experience_type,
                "data": data,
                "feedback": feedback,
                "session_type": session.session_type,
            }

            session.add_experience(experience)

            logger.debug(
                f"Added learning experience for agent {agent_id}: {experience_type}"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to add learning experience: {e}")

            return False

    def update_learning_metrics(
        self,
        agent_id: UUID,
        metrics: dict[str, float],
    ) -> bool:
        """Update learning metrics for an active session.





        Args:


            agent_id: ID of the agent.


            metrics: Metrics to update.





        Returns:


            True if metrics were updated successfully.


        """

        try:
            if agent_id not in self.active_sessions:
                logger.warning(f"No active learning session for agent {agent_id}")

                return False

            _ = self.active_sessions[agent_id]

            # Update session metrics

            for metric_name, value in metrics.items():
                if hasattr(session.metrics, metric_name):
                    setattr(session.metrics, metric_name, value)

            logger.debug(f"Updated learning metrics for agent {agent_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to update learning metrics: {e}")

            return False

    def get_learning_progress(
        self,
        agent_id: UUID,
    ) -> dict[str, Any] | None:
        """Get learning progress for an agent.





        Args:


            agent_id: ID of the agent.





        Returns:


            Learning progress data or None if no active session.


        """

        try:
            if agent_id not in self.active_sessions:
                return None

            _ = self.active_sessions[agent_id]

            progress = {
                "agent_id": str(agent_id),
                "session_type": session.session_type,
                "status": session.status,
                "start_time": session.start_time.isoformat(),
                "duration": str(session.get_duration()),
                "metrics": session.metrics.to_dict(),
                "experience_count": len(session.experiences),
                "outcomes": session.outcomes,
            }

            return progress

        except Exception as e:
            logger.error(f"Failed to get learning progress: {e}")

            return None

    async def optimize_agent_performance(
        self,
        agent_id: UUID,
        optimization_type: str = "automatic",
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Optimize agent performance based on learning data.





        Args:


            agent_id: ID of the agent to optimize.


            optimization_type: Type of optimization.


            parameters: Optimization parameters.





        Returns:


            Optimization results.





        Raises:


            EntityNotFoundError: If agent not found.


        """

        try:
            logger.info(f"Optimizing agent performance: {agent_id}")

            # Get agent

            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise EntityNotFoundError(f"Agent not found: {agent_id}")

            # Get recent memories for analysis

            recent_memories = await self.memory_repository.list_by_agent(
                agent_id=agent_id,
                limit=100,
            )

            # Analyze performance patterns

            analysis = self._analyze_performance_patterns(agent, recent_memories)

            # Generate optimization recommendations

            recommendations = self._generate_optimization_recommendations(
                agent,
                analysis,
                parameters or {},
            )

            # Apply optimizations if automatic

            if optimization_type == "automatic":
                await self._apply_optimizations(agent, recommendations)

            results = {
                "agent_id": str(agent_id),
                "optimization_type": optimization_type,
                "analysis": analysis,
                "recommendations": recommendations,
                "applied": optimization_type == "automatic",
                "timestamp": self._get_current_time().isoformat(),
            }

            logger.info(f"Completed agent optimization: {agent_id}")

            return results

        except Exception as e:
            logger.error(f"Failed to optimize agent performance: {e}")

            raise BusinessException(f"Failed to optimize agent: {e!s}") from e

    def _analyze_performance_patterns(
        self,
        agent: Agent,
        memories: list[Memory],
    ) -> dict[str, Any]:
        """Analyze agent performance patterns."""

        try:
            # Calculate basic metrics

            total_interactions = len(memories)

            if total_interactions == 0:
                return {
                    "total_interactions": 0,
                    "patterns": [],
                    "issues": [],
                    "strengths": [],
                }

            # Analyze response patterns

            response_times = []

            error_count = 0

            success_count = 0

            for memory in memories:
                # Use context instead of metadata for performance data

                context = memory.context

                if "response_time" in context:
                    response_times.append(context["response_time"])

                if "error" in context:
                    error_count += 1

                else:
                    success_count += 1

            # Calculate metrics

            avg_response_time = (
                sum(response_times) / len(response_times) if response_times else 0
            )

            error_rate = error_count / total_interactions

            success_rate = success_count / total_interactions

            # Identify patterns

            patterns = []

            if avg_response_time > 5.0:
                patterns.append("slow_response_times")

            if error_rate > 0.1:
                patterns.append("high_error_rate")

            if success_rate > 0.9:
                patterns.append("high_success_rate")

            return {
                "total_interactions": total_interactions,
                "avg_response_time": avg_response_time,
                "error_rate": error_rate,
                "success_rate": success_rate,
                "patterns": patterns,
                "issues": patterns
                if any(
                    p in ["slow_response_times", "high_error_rate"] for p in patterns
                )
                else [],
                "strengths": patterns if "high_success_rate" in patterns else [],
            }

        except Exception as e:
            logger.error(f"Failed to analyze performance patterns: {e}")

            return {"error": str(e)}

    def _generate_optimization_recommendations(
        self,
        agent: Agent,
        analysis: dict[str, Any],
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Generate optimization recommendations."""

        try:
            recommendations = []

            # Response time optimization

            if analysis.get("avg_response_time", 0) > 3.0:
                recommendations.append(
                    {
                        "type": "response_time",
                        "priority": "high",
                        "action": "optimize_model_parameters",
                        "description": "Reduce model complexity to improve response times",
                        "parameters": {
                            "max_tokens": min(agent.config.max_tokens, 500),
                            "temperature": 0.7,
                        },
                    }
                )

            # Error rate optimization

            if analysis.get("error_rate", 0) > 0.05:
                recommendations.append(
                    {
                        "type": "error_reduction",
                        "priority": "high",
                        "action": "improve_error_handling",
                        "description": "Enhance error handling and validation",
                        "parameters": {
                            "retry_attempts": 3,
                            "validation_strict": True,
                        },
                    }
                )

            # Memory optimization

            recommendations.append(
                {
                    "type": "memory_optimization",
                    "priority": "medium",
                    "action": "optimize_memory_usage",
                    "description": "Optimize memory retrieval and storage",
                    "parameters": {
                        "memory_limit": 1000,
                        "cleanup_threshold": 0.8,
                    },
                }
            )

            return recommendations

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")

            return []

    async def _apply_optimizations(
        self,
        agent: Agent,
        recommendations: list[dict[str, Any]],
    ) -> None:
        """Apply optimization recommendations to agent."""

        try:
            for recommendation in recommendations:
                action = recommendation.get("action")

                parameters = recommendation.get("parameters", {})

                if action == "optimize_model_parameters":
                    # Update agent model parameters

                    agent.config.max_tokens = parameters.get(
                        "max_tokens", agent.config.max_tokens
                    )

                    agent.config.temperature = parameters.get(
                        "temperature", agent.config.temperature
                    )

                elif action == "improve_error_handling":
                    # Update error handling in metadata

                    agent.metadata.setdefault("error_handling", {}).update(parameters)

                elif action == "optimize_memory_usage":
                    # Update memory configuration in metadata

                    agent.metadata.setdefault("memory", {}).update(parameters)

            # Save updated agent

            await self.agent_repository.update(agent)

            logger.info(
                f"Applied {len(recommendations)} optimizations to agent {agent.id}"
            )

        except Exception as e:
            logger.error(f"Failed to apply optimizations: {e}")

            raise

    def _store_learning_results(self, session: LearningSession) -> None:
        """Store learning session results."""

        try:
            # Create analytics record for the learning session

            analytics_data = {
                "event_type": "learning_session_completed",
                "agent_id": str(session.agent_id),
                "session_type": session.session_type,
                "duration": str(session.get_duration()),
                "metrics": session.metrics.to_dict(),
                "experience_count": len(session.experiences),
                "outcomes": session.outcomes,
            }

            # Note: This would typically store to analytics repository

            # For now, just log the results

            logger.info(
                f"Learning session results: {json.dumps(analytics_data, indent=2)}"
            )

        except Exception as e:
            logger.error(f"Failed to store learning results: {e}")

    def get_active_sessions(self) -> dict[UUID, dict[str, Any]]:
        """Get all active learning sessions.





        Returns:


            Dictionary of active learning sessions.


        """

        return {
            agent_id: {
                "session_type": session.session_type,
                "start_time": session.start_time.isoformat(),
                "duration": str(session.get_duration()),
                "experience_count": len(session.experiences),
                "status": session.status,
            }
            for agent_id, session in self.active_sessions.items()
        }

    def add_learning_strategy(
        self,
        name: str,
        strategy: LearningStrategy,
    ) -> None:
        """Add a new learning strategy.





        Args:


            name: Strategy name.


            strategy: Learning strategy configuration.


        """

        self.learning_strategies[name] = strategy

        logger.info(f"Added learning strategy: {name}")

    def get_learning_strategies(self) -> dict[str, dict[str, Any]]:
        """Get all available learning strategies.





        Returns:


            Dictionary of learning strategies.


        """

        return {
            name: {
                "type": strategy.strategy_type,
                "parameters": strategy.parameters,
                "priority": strategy.priority,
                "enabled": strategy.enabled,
            }
            for name, strategy in self.learning_strategies.items()
        }
