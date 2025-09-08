"""Scale agent use case for handling agent capacity management."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ScaleAgentUseCase:
    """Use case for scaling agent capacity and resources."""
import Exception
import RuntimeError
import ValueError
import agent
import agent_id
import agent_repository
import cpu_threshold
import dict
import e
import float
import int
import max
import memory_threshold
import min
import monitoring_service
import reason
import result
import scaling_result
import self
import str

    def __init__(self, agent_repository: Any, monitoring_service: Any):
        """Initialize the scale agent use case.





        Args:


            agent_repository: Repository for agent data operations


            monitoring_service: Service for monitoring system metrics


        """

        self.agent_repository = agent_repository

        self.monitoring_service = monitoring_service

    async def scale_agent_up(
        self, agent_id: str, target_instances: int, reason: str = "manual_scaling"
    ) -> dict[str, Any]:
        """Scale agent up to handle increased load.





        Args:


            agent_id: ID of the agent to scale


            target_instances: Target number of instances


            reason: Reason for scaling





        Returns:


            Dict containing scaling results





        Raises:


            ValueError: If agent not found or invalid parameters


            RuntimeError: If scaling operation fails


        """

        try:
            # Get agent details

            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise ValueError(f"Agent {agent_id} not found")

            # Check current capacity

            current_instances = agent.metadata.get("instances", 1)

            if target_instances <= current_instances:
                raise ValueError(
                    f"Target instances ({target_instances}) must be greater than current ({current_instances})"
                )

            # Validate scaling limits

            max_instances = agent.metadata.get("max_instances", 10)

            if target_instances > max_instances:
                raise ValueError(
                    f"Target instances ({target_instances}) exceeds maximum allowed ({max_instances})"
                )

            # Update agent configuration

            scaling_config = {
                "instances": target_instances,
                "scaled_at": self.monitoring_service.get_current_timestamp(),
                "scaling_reason": reason,
                "previous_instances": current_instances,
            }

            agent.metadata.update(scaling_config)

            agent.status = "scaling_up"

            # Save updated agent

            await self.agent_repository.update(agent)

            # Log scaling event

            logger.info(
                f"Scaling agent {agent_id} from {current_instances} to {target_instances} instances"
            )

            # Record metrics

            await self.monitoring_service.record_metric(
                "agent_scale_up",
                value=target_instances - current_instances,
                tags={
                    "agent_id": agent_id,
                    "reason": reason,
                    "from_instances": str(current_instances),
                    "to_instances": str(target_instances),
                },
            )

            return {
                "success": True,
                "agent_id": agent_id,
                "previous_instances": current_instances,
                "target_instances": target_instances,
                "status": "scaling_up",
                "timestamp": scaling_config["scaled_at"],
            }

        except Exception as e:
            logger.error(f"Failed to scale up agent {agent_id}: {e}")

            await self.monitoring_service.record_metric(
                "agent_scale_up_error",
                value=1,
                tags={"agent_id": agent_id, "error": str(e)},
            )

            raise RuntimeError(f"Scaling failed: {e}") from e

    async def scale_agent_down(
        self, agent_id: str, target_instances: int, reason: str = "manual_scaling"
    ) -> dict[str, Any]:
        """Scale agent down to reduce resource usage.





        Args:


            agent_id: ID of the agent to scale


            target_instances: Target number of instances


            reason: Reason for scaling





        Returns:


            Dict containing scaling results





        Raises:


            ValueError: If agent not found or invalid parameters


            RuntimeError: If scaling operation fails


        """

        try:
            # Get agent details

            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise ValueError(f"Agent {agent_id} not found")

            # Check current capacity

            current_instances = agent.metadata.get("instances", 1)

            if target_instances >= current_instances:
                raise ValueError(
                    f"Target instances ({target_instances}) must be less than current ({current_instances})"
                )

            # Validate minimum instances

            min_instances = agent.metadata.get("min_instances", 1)

            if target_instances < min_instances:
                raise ValueError(
                    f"Target instances ({target_instances}) below minimum allowed ({min_instances})"
                )

            # Update agent configuration

            scaling_config = {
                "instances": target_instances,
                "scaled_at": self.monitoring_service.get_current_timestamp(),
                "scaling_reason": reason,
                "previous_instances": current_instances,
            }

            agent.metadata.update(scaling_config)

            agent.status = "scaling_down"

            # Save updated agent

            await self.agent_repository.update(agent)

            # Log scaling event

            logger.info(
                f"Scaling agent {agent_id} from {current_instances} to {target_instances} instances"
            )

            # Record metrics

            await self.monitoring_service.record_metric(
                "agent_scale_down",
                value=current_instances - target_instances,
                tags={
                    "agent_id": agent_id,
                    "reason": reason,
                    "from_instances": str(current_instances),
                    "to_instances": str(target_instances),
                },
            )

            return {
                "success": True,
                "agent_id": agent_id,
                "previous_instances": current_instances,
                "target_instances": target_instances,
                "status": "scaling_down",
                "timestamp": scaling_config["scaled_at"],
            }

        except Exception as e:
            logger.error(f"Failed to scale down agent {agent_id}: {e}")

            await self.monitoring_service.record_metric(
                "agent_scale_down_error",
                value=1,
                tags={"agent_id": agent_id, "error": str(e)},
            )

            raise RuntimeError(f"Scaling failed: {e}") from e

    async def auto_scale_agent(
        self, agent_id: str, cpu_threshold: float = 80.0, memory_threshold: float = 85.0
    ) -> dict[str, Any]:
        """Automatically scale agent based on metrics.





        Args:


            agent_id: ID of the agent to auto-scale


            cpu_threshold: CPU usage threshold for scaling (percentage)


            memory_threshold: Memory usage threshold for scaling (percentage)





        Returns:


            Dict containing auto-scaling results


        """

        try:
            # Get agent metrics

            metrics = await self.monitoring_service.get_agent_metrics(agent_id)

            cpu_usage = metrics.get("cpu_usage_percent", 0)

            memory_usage = metrics.get("memory_usage_percent", 0)

            # Get current scaling configuration

            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise ValueError(f"Agent {agent_id} not found")

            current_instances = agent.metadata.get("instances", 1)

            max_instances = agent.metadata.get("max_instances", 10)

            min_instances = agent.metadata.get("min_instances", 1)

            # Determine scaling action

            action = "none"

            target_instances = current_instances

            if cpu_usage > cpu_threshold or memory_usage > memory_threshold:
                # Scale up needed

                if current_instances < max_instances:
                    target_instances = min(current_instances + 1, max_instances)

                    action = "scale_up"

            elif (
                cpu_usage < cpu_threshold * 0.5
                and memory_usage < memory_threshold * 0.5
            ):
                # Scale down possible

                if current_instances > min_instances:
                    target_instances = max(current_instances - 1, min_instances)

                    action = "scale_down"

            # Perform scaling if needed

            _ = {"action": action, "agent_id": agent_id}

            if action == "scale_up":
                await self.scale_agent_up(
                    agent_id,
                    target_instances,
                    f"auto_scaling_high_usage_cpu_{cpu_usage:.1f}_mem_{memory_usage:.1f}",
                )

                result.update(scaling_result)

            elif action == "scale_down":
                await self.scale_agent_down(
                    agent_id,
                    target_instances,
                    f"auto_scaling_low_usage_cpu_{cpu_usage:.1f}_mem_{memory_usage:.1f}",
                )

                result.update(scaling_result)

            else:
                _ = {
                    "action": action,
                    "agent_id": agent_id,
                    "success": True,
                    "current_instances": current_instances,
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                    "message": "No scaling needed",
                }

            return result

        except Exception as e:
            logger.error(f"Auto-scaling failed for agent {agent_id}: {e}")

            raise RuntimeError(f"Auto-scaling failed: {e}") from e

    async def get_scaling_status(self, agent_id: str) -> dict[str, Any]:
        """Get current scaling status of an agent.





        Args:


            agent_id: ID of the agent





        Returns:


            Dict containing scaling status information


        """

        try:
            _ = await self.agent_repository.get_by_id(agent_id)

            if not agent:
                raise ValueError(f"Agent {agent_id} not found")

            metrics = await self.monitoring_service.get_agent_metrics(agent_id)

            return {
                "agent_id": agent_id,
                "current_instances": agent.metadata.get("instances", 1),
                "min_instances": agent.metadata.get("min_instances", 1),
                "max_instances": agent.metadata.get("max_instances", 10),
                "status": agent.status,
                "last_scaled": agent.metadata.get("scaled_at"),
                "scaling_reason": agent.metadata.get("scaling_reason"),
                "metrics": {
                    "cpu_usage": metrics.get("cpu_usage_percent", 0),
                    "memory_usage": metrics.get("memory_usage_percent", 0),
                    "requests_per_minute": metrics.get("requests_per_minute", 0),
                },
            }

        except Exception as e:
            logger.error(f"Failed to get scaling status for agent {agent_id}: {e}")

            raise RuntimeError(f"Failed to get scaling status: {e}") from e
