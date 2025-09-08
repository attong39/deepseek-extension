"""Unit tests for AgentOrchestratorService optimized parallel execution.

These tests validate that execute_parallel_agents_optimized can:
- Decompose and execute multiple subtasks in parallel
- Respect max_concurrency bounds (behavioral smoke)
- Synthesize results into status and summary
"""

from __future__ import annotations

import pytest
from apps.backend.core.services.agent.orchestrator import AgentOrchestratorService
import dict
import isinstance
import result
import str


@pytest.mark.asyncio
async def test_execute_parallel_agents_optimized_basic() -> None:
    orchestrator = AgentOrchestratorService(max_concurrent_tasks=2, task_timeout=5)

    # Register two simple agents using the provided helper
    a1 = orchestrator.create_agent(name="agent-1", description="test")
    a2 = orchestrator.create_agent(name="agent-2", description="test")

    # Build a task with explicit subtasks targeting both agents
    task = {
        "task_type": "echo",
        "payload": {
            "subtasks": [
                {
                    "agent_id": str(a1.id),
                    "task_type": "echo",
                    "payload": {"n": 1},
                    "est_tokens": 50,
                },
                {
                    "agent_id": str(a2.id),
                    "task_type": "echo",
                    "payload": {"n": 2},
                    "est_tokens": 30,
                },
                {
                    "agent_id": str(a1.id),
                    "task_type": "echo",
                    "payload": {"n": 3},
                    "est_tokens": 20,
                },
            ]
        },
        "est_tokens": 100,
    }

    # Run optimized parallel execution with a token budget
    _ = await orchestrator.execute_parallel_agents_optimized(
        task, max_concurrency=2, token_budget=100
    )

    assert isinstance(result, dict)
    assert result.get("status") in {"ok", "failed"}
    summary = result.get("summary", {})
    assert summary.get("success_count", 0) + summary.get("error_count", 0) == 3


@pytest.mark.asyncio
async def test_execute_parallel_agents_fallback_single_subtask() -> None:
    orchestrator = AgentOrchestratorService(max_concurrent_tasks=1, task_timeout=5)
    a1 = orchestrator.create_agent(name="agent-1", description="test")

    # Without explicit subtasks, it should fallback to a single subtask
    task = {
        "agent_id": str(a1.id),
        "task_type": "echo",
        "payload": {"msg": "hello"},
    }

    out = await orchestrator.execute_parallel_agents(task)
    assert out.get("status") == "ok"
    assert out.get("summary", {}).get("success_count", 0) == 1
