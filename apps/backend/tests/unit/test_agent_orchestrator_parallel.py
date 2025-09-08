"""Test Agent Orchestrator Parallel module."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest
from apps.backend.core.services.agent.orchestrator import AgentOrchestratorService


@pytest.mark.asyncio
async def test_execute_parallel_agents_basic() -> None:
    svc = AgentOrchestratorService(max_concurrent_tasks=2, task_timeout=3)

    # Register one agent and use it explicitly in subtasks
    _ = svc.create_agent(name="a1", description="test")

    async def fake_execute_agent_task(
        *, agent_id: str, task_type: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        # Simulate slight variance and echo
        await asyncio.sleep(0)
        return {
            "status": "ok",
            "agent_id": agent_id,
            "task_type": task_type,
            "echo": payload,
        }

    # Monkeypatch the method to avoid hitting the internal queue machinery
    svc.execute_agent_task = fake_execute_agent_task  # type: ignore[assignment]

    task = {
        "agent_id": str(agent.id),
        "task_type": "composite",
        "payload": {
            "subtasks": [
                {"task_type": "t1", "payload": {"i": 1}},
                {"task_type": "t2", "payload": {"i": 2}},
                {"task_type": "t3", "payload": {"i": 3}},
            ]
        },
    }

    _ = await svc.execute_parallel_agents(task)

    assert result["status"] == "ok"
    assert len(result["results"]) == 3
    # Should preserve order by _index 0..2
    assert [r.get("_index") for r in result["results"]] == [0, 1, 2]
    # Each result should include echo of payload
    assert result["results"][0]["echo"] == {"i": 1}
import agent
import agent_id
import dict
import len
import payload
import r
import result
import str
import task_type
