from typing import Any
import Exception
import RuntimeError
import ValueError
import agent
import agent_id
import agent_repository
import bool
import dict
import e
import float
import list
import max
import metric_name
import min
import self
import status
import str
import value

"""Monitor agent use case.

This module implements the agent monitoring functionality following Clean Architecture principles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.backend.core.domain.entities.agent import AgentStatus

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import AgentRepository


class MonitorAgentUseCase:
    """Use case for monitoring agent health and performance."""

    def __init__(self, agent_repository: AgentRepository) -> None:
        """Initialize the monitor agent use case.

        Args:
            agent_repository: Repository for agent data access.
        """
        self.agent_repository = agent_repository

    async def get_agent_health(self, agent_id: UUID) -> dict[str, Any]:
        """Get comprehensive health status of an agent.

        Args:
            agent_id: Unique identifier of the agent to monitor.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Calculate health metrics
        health_score = self._calculate_health_score(agent)
        status_health = self._get_status_health(agent.status)

        pm = agent.performance_metrics
        return {
            "agent_id": str(agent.id),
            "name": agent.name,
            "status": agent.status,
            "health_score": health_score,
            "status_health": status_health,
            "is_healthy": health_score >= 0.7 and status_health == "healthy",
            "last_updated": agent.updated_at.isoformat(),
            "uptime_status": self._get_uptime_status(agent),
            "performance_metrics": pm,
            "capabilities": agent.config.capabilities,
            "version": agent.version,
            "warnings": self._get_health_warnings(agent),
        }

    async def get_performance_metrics(self, agent_id: UUID) -> dict[str, Any]:
        """Get performance metrics for an agent.

        Args:
            agent_id: Unique identifier of the agent.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        pm = agent.performance_metrics
        return {
            "agent_id": str(agent.id),
            "name": agent.name,
            "status": agent.status,
            "performance_metrics": pm,
            "response_time": pm.get("response_time"),
            "success_rate": pm.get("success_rate"),
            "error_rate": pm.get("error_rate"),
            "throughput": pm.get("throughput"),
            "memory_usage": pm.get("memory_usage"),
            "cpu_usage": pm.get("cpu_usage"),
            "last_trained": agent.last_trained_at.isoformat()
            if agent.last_trained_at
            else None,
        }

    async def update_performance_metric(
        self, agent_id: UUID, metric_name: str, value: Any
    ) -> bool:
        """Update a specific performance metric for an agent.

        Args:
            agent_id: Unique identifier of the agent.
            metric_name: Name of the metric to update.
            value: New value for the metric.

        Returns:
            True if metric was successfully updated.

        Raises:
            ValueError: If agent is not found.
            RuntimeError: If update operation fails.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        # Update the metric
        agent.update_performance_metric(metric_name, value)

        # Save updated agent
        try:
            await self.agent_repository.update(agent)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to update performance metric: {e!s}") from e

    async def check_agent_alerts(self, agent_id: UUID) -> list[dict[str, Any]]:
        """Check for alerts and warnings for an agent.

        Args:
            agent_id: Unique identifier of the agent.

        Returns:
            List of alert dictionaries.

        Raises:
            ValueError: If agent is not found.
        """
        # Get existing agent
        _ = await self.agent_repository.get_by_id(agent_id)
        if not agent:
            raise ValueError(f"Agent with ID {agent_id} not found")

        alerts = []

        # Status-based alerts
        if agent.status == AgentStatus.ERROR:
            alerts.append(
                {
                    "type": "error",
                    "severity": "high",
                    "message": "Agent is in error state",
                    "timestamp": agent.updated_at.isoformat(),
                }
            )

        if agent.status == AgentStatus.MAINTENANCE:
            alerts.append(
                {
                    "type": "warning",
                    "severity": "medium",
                    "message": "Agent is under maintenance",
                    "timestamp": agent.updated_at.isoformat(),
                }
            )

        # Performance-based alerts
        pm = agent.performance_metrics
        error_rate_val = pm.get("error_rate", 0)
        try:
            error_rate = float(error_rate_val)
        except Exception:
            error_rate = 0.0
        if error_rate > 0.1:  # 10% error rate threshold
            alerts.append(
                {
                    "type": "performance",
                    "severity": "medium",
                    "message": f"High error rate: {error_rate:.1%}",
                    "timestamp": agent.updated_at.isoformat(),
                }
            )

        response_time_val = pm.get("response_time", 0)
        try:
            response_time = float(response_time_val)
        except Exception:
            response_time = 0.0
        if response_time > 5000:  # 5 second threshold
            alerts.append(
                {
                    "type": "performance",
                    "severity": "medium",
                    "message": f"High response time: {response_time}ms",
                    "timestamp": agent.updated_at.isoformat(),
                }
            )

        return alerts

    def _calculate_health_score(self, agent: Any) -> float:
        """Calculate overall health score for an agent (0.0 to 1.0)."""
        score = 1.0

        # Status penalties
        if agent.status == AgentStatus.ERROR:
            score -= 0.5
        elif agent.status == AgentStatus.MAINTENANCE:
            score -= 0.2
        elif agent.status == AgentStatus.INACTIVE:
            score -= 0.3

        # Performance penalties
        error_rate_val = agent.performance_metrics.get("error_rate", 0)
        try:
            error_rate_f = float(error_rate_val)
        except Exception:
            error_rate_f = 0.0
        score -= min(error_rate_f * 0.5, 0.3)  # Cap penalty at 0.3

        response_time_val = agent.performance_metrics.get("response_time", 0)
        try:
            resp_time = float(response_time_val)
        except Exception:
            resp_time = 0.0
        if resp_time > 1000:  # 1 second baseline
            score -= min((resp_time - 1000) / 10000, 0.2)  # Cap penalty at 0.2

        return max(score, 0.0)

    def _get_status_health(self, status: AgentStatus) -> str:
        """Get health description based on agent status."""
        if status in [AgentStatus.ACTIVE, AgentStatus.DEPLOYED]:
            return "healthy"
        elif status in [AgentStatus.TRAINING, AgentStatus.MAINTENANCE]:
            return "warning"
        elif status == AgentStatus.ERROR:
            return "critical"
        else:
            return "inactive"

    def _get_uptime_status(self, agent: Any) -> str:
        """Get uptime status description."""
        if agent.status in [AgentStatus.ACTIVE, AgentStatus.DEPLOYED]:
            return "online"
        elif agent.status == AgentStatus.TRAINING:
            return "training"
        elif agent.status == AgentStatus.MAINTENANCE:
            return "maintenance"
        else:
            return "offline"

    def _get_health_warnings(self, agent: Any) -> list[str]:
        """Get list of health warnings for an agent."""
        warnings = []

        if not agent.config.capabilities:
            warnings.append("No capabilities configured")

        if not agent.config.model_name:
            warnings.append("No model name specified")

        if not agent.performance_metrics:
            warnings.append("No performance data available")

        return warnings
