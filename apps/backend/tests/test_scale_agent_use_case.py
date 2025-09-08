from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from apps.backend.core.use_cases.agent.scale_agent import ScaleAgentUseCase
import ValueError

"""Unit test skeleton cho ScaleAgentUseCase (chuẩn pytest, mypy, ruff).
- Kiểm thử các hàm scale_agent_up, scale_agent_down, auto_scale_agent, get_scaling_status
- Mock repository, monitoring_service, metrics
"""


@pytest.mark.asyncio
class TestScaleAgentUseCase:
    async def test_scale_agent_up_success(self):
        repo = AsyncMock()
        monitoring = MagicMock()
        metrics = AsyncMock()
        agent_id = uuid4()
        agent = MagicMock()
        agent.config.instances = 1
        agent.config.max_instances = 5
        repo.get_by_id.return_value = agent
        monitoring.get_current_timestamp.return_value = "2025-09-02T12:00:00Z"
        use_case = ScaleAgentUseCase(repo, monitoring, metrics)
        result = await use_case.scale_agent_up(agent_id, 2, reason="test")
        assert result["success"] is True
        assert result["target_instances"] == 2

    async def test_scale_agent_up_invalid(self):
        repo = AsyncMock()
        monitoring = MagicMock()
        use_case = ScaleAgentUseCase(repo, monitoring)
        with pytest.raises(ValueError):
            await use_case.scale_agent_up("", 0)


__all__ = [
    "TestScaleAgentUseCase",
    "agent",
    "agent_id",
    "metrics",
    "monitoring",
    "repo",
    "result",
    "use_case",
]
