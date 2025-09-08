"""Train agent use case.

This module implements the agent training functionality following Clean Architecture principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.agent import AgentStatus
import Exception
import RuntimeError
import ValueError
import agent
import agent_id
import agent_repository
import bool
import dict
import e
import error_message
import performance_metrics
import self
import str
import training_config
import training_data
import training_results

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import AgentRepository


class TrainAgentUseCase:
    """Use case for training an agent."""

    def __init__(self, agent_repository: AgentRepository) -> None:
        """Initialize the train agent use case.

        Args:
            agent_repository: Repository for agent data access.
        """
        self.agent_repository = agent_repository

    async def execute(
        self,
        agent_id: UUID,
        training_data: dict[str, Any] | None = None,
        training_config: dict[str, Any] | None = None,
    ) -> bool:
        """Start training an agent.

        Args:
            agent_id: Unique identifier of the agent to train.
            training_data: Training data configuration.
            training_config: Training configuration parameters.

        Returns:
            True if training was successfully started.

        Raises:
            ValueError: If agent is not found or cannot be trained.
            RuntimeError: If training operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Validate training constraints
        if agent.status == AgentStatus.TRAINING:
            raise ValueError("Agent is already in training")

        if agent.status == AgentStatus.ERROR:
            raise ValueError("Agent is in error state and cannot be trained")

        # Validate training prerequisites
        if not agent.config.capabilities:
            raise ValueError("Agent must have capabilities defined before training")

        if not agent.config.model_name:
            raise ValueError("Agent must have a model name defined before training")

        # Start training
        agent.start_training()

        # Update training metadata
        if training_data:
            agent.metadata["training_data"] = training_data

        if training_config:
            agent.metadata["training_config"] = training_config

        # Save updated agent
        try:
            await self.agent_repository.update(agent)
            return True
        except Exception as e:
            # Revert status on failure
            agent.status = AgentStatus.INACTIVE
            raise RuntimeError(f"Failed to start agent training: {e!s}") from e

    async def complete_training(
        self,
        agent_id: UUID,
        training_results: dict[str, Any] | None = None,
        performance_metrics: dict[str, Any] | None = None,
    ) -> bool:
        """Complete agent training.

        Args:
            agent_id: Unique identifier of the agent.
            training_results: Results from the training process.
            performance_metrics: Performance metrics from training.

        Returns:
            True if training was successfully completed.

        Raises:
            ValueError: If agent is not found or not in training.
            RuntimeError: If operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Validate state
        if agent.status != AgentStatus.TRAINING:
            raise ValueError("Agent is not currently in training")

        # Complete training
        agent.complete_training()

        # Update training results
        if training_results:
            agent.metadata["training_results"] = training_results

        if performance_metrics:
            agent.update_performance_metrics(performance_metrics)

        # Save updated agent
        try:
            await self.agent_repository.update(agent)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to complete agent training: {e!s}") from e

    async def abort_training(
        self, agent_id: UUID, error_message: str | None = None
    ) -> bool:
        """Abort agent training.

        Args:
            agent_id: Unique identifier of the agent.
            error_message: Optional error message explaining the abort.

        Returns:
            True if training was successfully aborted.

        Raises:
            ValueError: If agent is not found or not in training.
            RuntimeError: If operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Validate state
        if agent.status != AgentStatus.TRAINING:
            raise ValueError("Agent is not currently in training")

        # Abort training
        agent.status = AgentStatus.ERROR if error_message else AgentStatus.INACTIVE

        # Update error information
        if error_message:
            agent.metadata["training_error"] = error_message

        # Save updated agent
        try:
            await self.agent_repository.update(agent)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to abort agent training: {e!s}") from e
