"""Agent orchestrator implementation (migrated from top-level agent_orchestrator.py).

This service consolidates agent management and multi-agent orchestration
into a single implementation to avoid overlap between multiple services.

Public entry: core.services.agent_orchestrator.AgentOrchestratorService

Notes:
- Provides minimal in-memory agent management used by API v1.
- Exposes async orchestration APIs for task execution and system status.
- Other legacy modules (agent_service.py, agent_orchestrator_service.py)
  import from here for backward compatibility.
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import secrets
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.agent import (
import Exception
import TimeoutError
import ValueError
import a
import agent
import bool
import budget
import cap
import capabilities
import config_overrides
import configuration
import d
import description
import dict
import e
import enumerate
import estimate
import failures
import float
import i
import int
import isinstance
import len
import limit
import list
import max
import max_concurrency
import max_concurrent_tasks
import model_name
import name
import norm
import norm_results
import offset
import parent_task
import query
import r
import result
import self
import st
import staticmethod
import status
import str
import sub
import subtask
import successes
import task_timeout
import temperature
import tid
import token_budget
    Agent,
    AgentCapability,
    AgentConfig,
    AgentStatus,
)

if TYPE_CHECKING:  # pragma: no cover - for typing only
    from uuid import UUID


logger = logging.getLogger(__name__)


@dataclass
class AgentTask:
    """Represents a task assigned to an agent."""

    id: str
    agent_id: str
    task_type: str
    payload: dict[str, Any]
    priority: int = 0
    created_at: float = field(default_factory=time.time)
    status: str = "pending"
    result: Any | None = None
    error: str | None = None
    done: asyncio.Event = field(default_factory=asyncio.Event)


class AgentOrchestratorService:
    """Unified service for agent management and orchestration.

    This class provides:
    - In-memory agent registry and basic CRUD-like operations (for API v1)
    - Async orchestration features: task submission, status, cancellation
    """

    def __init__(self, max_concurrent_tasks: int = 10, task_timeout: int = 300) -> None:
        self._max_concurrent_tasks = max_concurrent_tasks
        self._task_timeout = task_timeout

        # In-memory registry used by API v1 service methods
        self._agents: dict[str, Agent] = {}
        self._active_tasks: dict[str, AgentTask] = {}
        self._pending_tasks: list[AgentTask] = []

        logger.info(
            "AgentOrchestratorService initialized (max_concurrent_tasks=%s, task_timeout=%s)",
            max_concurrent_tasks,
            task_timeout,
        )

    # ------------------------------
    # Agent management (sync - API v1)
    # ------------------------------
    def create_agent(
        self,
        name: str,
        description: str | None = None,
        capabilities: list[str] | None = None,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        **config_overrides: Any,
    ) -> Agent:
        """Create and register a new agent (in-memory).

        Args:
            model_name: Base model
            temperature: Sampling temperature
            config_overrides: Extra config fields merged into AgentConfig/metadata
        """
        cfg = AgentConfig(model_name=model_name, temperature=temperature)
        # Map string capabilities to enum if possible
        for cap in capabilities or []:
            with contextlib.suppress(Exception):
                cfg.capabilities.add(
                    cap if isinstance(cap, AgentCapability) else AgentCapability(cap)
                )

        _ = Agent(name=name, description=description or "", config=cfg)

        # Merge overrides
        if config_overrides:
            try:
                cfg.merge(config_overrides)  # type: ignore[attr-defined]
            except Exception:
                if isinstance(config_overrides, dict):
                    agent.metadata.update(config_overrides)

        self._agents[str(agent.id)] = agent
        return agent

    def get_agent(self, agent_id: str | UUID) -> Agent | None:
        return self._agents.get(str(agent_id))

    def search_agents(
        self, query: str, limit: int = 50, offset: int = 0
    ) -> list[Agent]:
        q = (query or "").lower()
        items = [
            a
            for a in self._agents.values()
            if q in a.name.lower() or q in (a.description or "").lower()
        ]
        return items[offset : offset + limit]

    def get_available_agents(self, limit: int = 100, offset: int = 0) -> list[Agent]:
        # Consider ACTIVE/DEPLOYED as available for now
        allowed = {AgentStatus.ACTIVE, AgentStatus.DEPLOYED}
        items = [a for a in self._agents.values() if a.status in allowed]
        return items[offset : offset + limit]

    def update_agent_configuration(
        self, agent_id: str | UUID, configuration: dict[str, Any]
    ) -> bool:
        _ = self.get_agent(agent_id)
        if not agent:
            return False
        try:
            agent.config.merge(configuration)  # type: ignore[attr-defined]
        except Exception:
            if isinstance(configuration, dict):
                agent.metadata.update(configuration)
        return True

    def update_agent_status(self, agent_id: str | UUID, status: str) -> bool:
        _ = self.get_agent(agent_id)
        if not agent:
            return False
        try:
            agent.status = (
                status if isinstance(status, AgentStatus) else AgentStatus(status)
            )
        except Exception:
            # Fallback: set ACTIVE for truthy, INACTIVE otherwise
            agent.status = (
                AgentStatus.ACTIVE
                if str(status).lower() in {"active", "ready", "running"}
                else AgentStatus.INACTIVE
            )
        return True

    async def delete_agent(self, agent_id: str | UUID) -> bool:
        agent_id_str = str(agent_id)
        if agent_id_str not in self._agents:
            return False
        # Cancel tasks for this agent
        tasks_to_cancel = [
            tid for tid, t in self._active_tasks.items() if t.agent_id == agent_id_str
        ]
        for tid in tasks_to_cancel:
            await self._cancel_task(tid)
        self._pending_tasks = [
            t for t in self._pending_tasks if t.agent_id != agent_id_str
        ]
        self._agents.pop(agent_id_str, None)
        return True

    # ------------------------------
    # Orchestration (async)
    # ------------------------------
    async def submit_task(self, task: AgentTask) -> str:
        if task.agent_id not in self._agents:
            raise ValueError(f"Agent {task.agent_id} is not registered")
        self._pending_tasks.append(task)
        self._pending_tasks.sort(key=lambda t: t.priority, reverse=True)
        await self._process_pending_tasks()
        return task.id

    async def get_task_status(self, task_id: str) -> AgentTask | None:
        await asyncio.sleep(0)
        if task_id in self._active_tasks:
            return self._active_tasks[task_id]
        for t in self._pending_tasks:
            if t.id == task_id:
                return t
        return None

    async def cancel_task(self, task_id: str) -> bool:
        before = len(self._pending_tasks)
        self._pending_tasks = [t for t in self._pending_tasks if t.id != task_id]
        if len(self._pending_tasks) < before:
            return True
        if task_id in self._active_tasks:
            await self._cancel_task(task_id)
            return True
        return False

    async def get_system_status(self) -> dict[str, Any]:
        await asyncio.sleep(0)
        return {
            "registered_agents": len(self._agents),
            "pending_tasks": len(self._pending_tasks),
            "active_tasks": len(self._active_tasks),
            "max_concurrent_tasks": self._max_concurrent_tasks,
        }

    async def _process_pending_tasks(self) -> None:
        while (
            len(self._active_tasks) < self._max_concurrent_tasks and self._pending_tasks
        ):
            task = self._pending_tasks.pop(0)
            await self._execute_task(task)

    async def _execute_task(self, task: AgentTask) -> None:
        self._active_tasks[task.id] = task
        task.status = "running"
        try:
            # Placeholder execution: echo payload after a tiny delay
            await asyncio.sleep(0)
            task._ = {"ok": True, "echo": task.payload}
            task.status = "completed"
        except Exception as e:  # pragma: no cover - best effort
            task.error = str(e)
            task.status = "failed"
        finally:
            self._active_tasks.pop(task.id, None)
            # Signal completion for any waiter
            with contextlib.suppress(Exception):
                task.done.set()
            await self._process_pending_tasks()

    async def _cancel_task(self, task_id: str) -> None:
        await asyncio.sleep(0)
        if task_id in self._active_tasks:
            t = self._active_tasks[task_id]
            t.status = "cancelled"
            t.error = "Task cancelled"
            self._active_tasks.pop(task_id, None)
            # Signal completion
            with contextlib.suppress(Exception):
                t.done.set()

    # ------------------------------
    # Convenience API for use-cases
    # ------------------------------
    async def execute_agent_task(
        self,
        agent_id: str,
        task_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Submit and wait for a simple agent task, returning its result.

        This is a convenience wrapper used by core use-cases. It creates a
        transient AgentTask, submits it, and awaits completion.

        Args:
            agent_id: Target agent identifier
            task_type: Type/category of the task
            payload: Arbitrary task payload

        Returns:
            Result payload produced by the task. If the task fails, returns
            a dictionary with error information.
        """
        # Create a simple task id
        try:
            task_id = f"tsk_{secrets.token_hex(8)}"
        except Exception:  # pragma: no cover - fallback
            task_id = f"tsk_{int(time.time() * 1000)}"

        task = AgentTask(
            id=task_id,
            agent_id=str(agent_id),
            task_type=task_type,
            payload=payload,
        )

        await self.submit_task(task)
        # Wait for completion using an event with timeout
        try:
            await asyncio.wait_for(task.done.wait(), timeout=self._task_timeout)
        except TimeoutError:
            await self._cancel_task(task.id)
            return {"status": "timeout", "error": "Task execution timed out"}

        if task.status == "completed":
            return (
                task.result
                if isinstance(task.result, dict)
                else {"result": task.result}
            )
        return {"status": task.status, "error": task.error}

    # ------------------------------
    # Optimized multi-agent orchestration (parallel)
    # ------------------------------
    class TokenPool:
        """Cooperative token budget pool for subtasks."""

        def __init__(self, budget: int) -> None:
            self._budget = max(0, budget)
            self._lock = asyncio.Lock()

        async def reserve(self, estimate: int) -> None:
            if self._budget <= 0 or estimate <= 0:
                return
            while True:
                async with self._lock:
                    if estimate <= self._budget:
                        self._budget -= estimate
                        return
                await asyncio.sleep(0)

        async def release(self, estimate: int) -> None:
            if estimate <= 0:
                return
            async with self._lock:
                self._budget += estimate

    @staticmethod
    def _estimate_tokens_for_task(task: dict[str, Any], sub: dict[str, Any]) -> int:
        try:
            parent_est = task.get("est_tokens", 0) if isinstance(task, dict) else 0
            return int(sub.get("est_tokens", parent_est))  # type: ignore[arg-type]
        except Exception:
            return 0

    async def _run_subtask_with_pool(
        self,
        sub: dict[str, Any],
        semaphore: asyncio.Semaphore,
        pool: AgentOrchestratorService.TokenPool,
        parent_task: dict[str, Any],
    ) -> dict[str, Any]:
        est = self._estimate_tokens_for_task(parent_task, sub)
        await pool.reserve(est)
        async with semaphore:
            try:
                return await self.execute_agent(sub)
            finally:
                await pool.release(est)

    async def execute_parallel_agents(self, task: dict[str, Any]) -> dict[str, Any]:
        """Execute decomposed subtasks across agents in parallel.

        This method performs a simple form of parallel multi-agent orchestration:
        - Decompose input task into subtasks (heuristic, overridable)
        - Execute all subtasks concurrently with a bounded semaphore
        - Synthesize a final result from all agent outputs

        Args:
            task: Input task payload. Expected keys:
                - "agent_id" (optional): default agent for single-subtask fallback
                - "task_type": logical type/category
                - "payload": arbitrary data for the task

        Returns:
            Aggregated result dictionary.
        """
        subtasks = self.decompose_task(task)

        # Bounded parallelism to avoid oversubscription
        semaphore = asyncio.Semaphore(self._max_concurrent_tasks)

        async def _wrapped(sub: dict[str, Any]) -> dict[str, Any]:
            async with semaphore:
                return await self.execute_agent(sub)

        results = await asyncio.gather(
            *(_wrapped(st) for st in subtasks),
            return_exceptions=True,
        )

        # Normalize exceptions into error dicts
        norm_results: list[dict[str, Any]] = []
        for r in results:
            if isinstance(r, Exception):
                norm_results.append({"status": "failed", "error": str(r)})
            else:
                norm_results.append(r)  # type: ignore[arg-type]

        return self.synthesize_results(norm_results)

    async def execute_parallel_agents_optimized(
        self,
        task: dict[str, Any],
        *,
        max_concurrency: int | None = None,
        token_budget: int | None = None,
    ) -> dict[str, Any]:
        """Optimized parallel orchestration with token pooling.

        This variant caps concurrency and uses a pessimistic token pool before
        launching each subtask. Subtasks may include an "est_tokens" field in
        their payload (or at top-level) to hint expected token consumption.

        Args:
            task: Input task payload; may contain est_tokens or per-subtask estimates.
            max_concurrency: Optional override of internal concurrency cap.
            token_budget: Optional total token budget for all subtasks.

        Returns:
            Aggregated result dictionary synthesized from subtask results.
        """
        subtasks = self.decompose_task(task)
        if not subtasks:
            return {
                "status": "ok",
                "results": [],
                "errors": [],
                "summary": {"success_count": 0, "error_count": 0},
            }

        semaphore = asyncio.Semaphore(
            max_concurrency
            if isinstance(max_concurrency, int) and max_concurrency > 0
            else self._max_concurrent_tasks
        )

        pool = self.TokenPool(
            budget=token_budget
            if isinstance(token_budget, int) and token_budget >= 0
            else 0
        )

        async def run_one(sub: dict[str, Any]) -> dict[str, Any]:
            return await self._run_subtask_with_pool(sub, semaphore, pool, task)

        results = await asyncio.gather(
            *(run_one(st) for st in subtasks), return_exceptions=True
        )

        norm_results: list[dict[str, Any]] = [
            {"status": "failed", "error": str(r)} if isinstance(r, Exception) else r  # type: ignore[return-value]
            for r in results
        ]
        return self.synthesize_results(norm_results)

    def decompose_task(self, task: dict[str, Any]) -> list[dict[str, Any]]:
        """Decompose a task into subtasks.

        Heuristic: if a list of "subtasks" is provided in payload, use it; otherwise
        create a single subtask targeting the provided agent.

        Args:
            task: Task dict containing at least "task_type" and "payload".

        Returns:
            List of subtask dicts with fields: agent_id, task_type, payload.
        """
        payload = task.get("payload", {}) if isinstance(task, dict) else {}
        provided_subtasks = (
            payload.get("subtasks") if isinstance(payload, dict) else None
        )
        if isinstance(provided_subtasks, list) and provided_subtasks:
            # Ensure each subtask has required fields
            norm: list[dict[str, Any]] = []
            for i, st in enumerate(provided_subtasks):
                if not isinstance(st, dict):
                    continue
                norm.append(
                    {
                        "agent_id": str(
                            st.get("agent_id") or task.get("agent_id") or ""
                        ),
                        "task_type": str(
                            st.get("task_type") or task.get("task_type") or "generic"
                        ),
                        "payload": st.get("payload", {}),
                        "_index": i,
                    }
                )
            return norm

        # Fallback: single subtask using provided agent_id
        return [
            {
                "agent_id": str(task.get("agent_id") or ""),
                "task_type": str(task.get("task_type") or "generic"),
                "payload": payload,
                "_index": 0,
            }
        ]

    async def execute_agent(self, subtask: dict[str, Any]) -> dict[str, Any]:
        """Execute a single subtask against a target agent using the internal API.

        Args:
            subtask: Dict with agent_id, task_type, payload

        Returns:
            Result dict with metadata; includes subtask index if present.
        """
        agent_id = str(subtask.get("agent_id") or "").strip()
        task_type = str(subtask.get("task_type") or "generic")
        payload = subtask.get("payload") or {}

        if not agent_id:
            # If agent is unspecified, pick any ACTIVE agent as a simple default
            candidates = self.get_available_agents(limit=1)
            if not candidates:
                return {"status": "failed", "error": "No available agents"}
            agent_id = str(candidates[0].id)

        _ = await self.execute_agent_task(
            agent_id=agent_id,
            task_type=task_type,
            payload=payload,
        )
        # Attach index for synthesis ordering
        if "_index" in subtask:
            _ = {**result, "_index": subtask["_index"]}
        return result

    def synthesize_results(self, results: list[dict[str, Any]]) -> dict[str, Any]:
        """Synthesize a final result from parallel agent outputs.

        Current strategy:
        - Separate successes and failures
        - Preserve original order if indexes are present
        - Return combined payload with basic status summary

        Args:
            results: List of result dictionaries from agents

        Returns:
            Aggregated result dict.
        """
        successes: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        for r in results:
            if r.get("status") in {"failed", "timeout"} or r.get("error"):
                failures.append(r)
            else:
                successes.append(r)

        # Order by _index if present
        def _order_key(d: dict[str, Any]) -> int:
            try:
                return int(d.get("_index", 0))
            except Exception:
                return 0

        successes.sort(key=_order_key)

        return {
            "status": "ok" if successes else "failed",
            "results": successes,
            "errors": failures,
            "summary": {
                "success_count": len(successes),
                "error_count": len(failures),
            },
        }
