from typing import Any
import Exception
import RuntimeError
import ValueError
import agent
import agent_id
import agent_repository
import auto_activate
import bool
import deployment_config
import dict
import e
import self
import str

"""Deploy agent use case.

This module implements the agent deployment functionality following Clean Architecture principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.backend.core.domain.entities.agent import AgentStatus

from core.utils.async_utils import _maybe_await

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import AgentRepository


class DeployAgentUseCase:
    """Use case for deploying an agent."""

    def __init__(self, agent_repository: AgentRepository) -> None:
        """Initialize the deploy agent use case.

        Args:
            agent_repository: Repository for agent data access.
        """
        self.agent_repository = agent_repository

    async def execute(
        self,
        agent_id: UUID,
        deployment_config: dict[str, Any] | None = None,
        auto_activate: bool = True,
    ) -> bool:
        """Deploy an agent.

        Args:
            agent_id: Unique identifier of the agent to deploy.
            deployment_config: Deployment configuration parameters.
            auto_activate: Whether to automatically activate the agent after deployment.

        Returns:
            True if agent was successfully deployed.

        Raises:
            ValueError: If agent is not found or cannot be deployed.
            RuntimeError: If deployment operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Validate deployment readiness
        if not agent.is_ready_for_deployment():
            raise ValueError(
                "Agent is not ready for deployment. "
                "Ensure it has capabilities and a valid model name."
            )

        # Validate current status
        if agent.status == AgentStatus.DEPLOYED:
            raise ValueError("Agent is already deployed")

        if agent.status == AgentStatus.TRAINING:
            raise ValueError("Cannot deploy agent while training is in progress")

        if agent.status == AgentStatus.ERROR:
            raise ValueError("Cannot deploy agent in error state")

        # Set deployment status
        agent.status = AgentStatus.DEPLOYED

        # Update deployment metadata
        if deployment_config:
            agent.metadata["deployment_config"] = deployment_config

        agent.metadata["deployment_timestamp"] = str(agent.updated_at)

        # Auto-activate if requested
        if auto_activate:
            agent.activate()

        # Save updated agent
        try:
            res = self.agent_repository.update(agent)
            await _maybe_await(res)
            return True
        except Exception as e:
            # Revert status on failure
            agent.status = AgentStatus.INACTIVE
            raise RuntimeError(f"Failed to deploy agent: {e!s}") from e

    async def undeploy(self, agent_id: UUID) -> bool:
        """Undeploy an agent.

        Args:
            agent_id: Unique identifier of the agent to undeploy.

        Returns:
            True if agent was successfully undeployed.

        Raises:
            ValueError: If agent is not found or not deployed.
            RuntimeError: If undeploy operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Validate current status
        if agent.status != AgentStatus.DEPLOYED:
            raise ValueError("Agent is not currently deployed")

        # Deactivate and set to inactive
        agent.deactivate()

        # Remove deployment metadata
        agent.metadata.pop("deployment_config", None)
        agent.metadata.pop("deployment_timestamp", None)

        # Save updated agent
        try:
            res = self.agent_repository.update(agent)
            await _maybe_await(res)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to undeploy agent: {e!s}") from e

    async def check_deployment_status(self, agent_id: UUID) -> dict[str, Any]:
        """Check the deployment status of an agent.

        Args:
            agent_id: Unique identifier of the agent.

        Returns:
            Dictionary containing deployment status information.

        Raises:
            ValueError: If agent is not found.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        return {
            "agent_id": str(agent.id),
            "name": agent.name,
            "status": agent.status,
            "is_deployed": agent.status == AgentStatus.DEPLOYED,
            "is_active": agent.status == AgentStatus.ACTIVE,
            "is_ready_for_deployment": agent.is_ready_for_deployment(),
            "deployment_config": agent.metadata.get("deployment_config"),
            "deployment_timestamp": agent.metadata.get("deployment_timestamp"),
            "capabilities": agent.config.capabilities,
            "version": agent.version,
            "performance_metrics": agent.performance_metrics,
        }
