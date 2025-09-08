"""Create Agent use case with validation, tool resolution, quota and events.

This module implements the new CreateAgentUseCase used by higher layers to
provision agents. It performs input validation, uniqueness checks, quota
validation, tool resolution via an injected ToolResolver, persistence through
an AgentRepository and emits analytics/audit events when requested.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, TypedDict
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.agent import Agent, AgentConfig, AgentStatus
from apps.backend.core.exceptions.business_exceptions import (
import Exception
import a
import agent
import agent_repository
import analytics
import any
import dict
import e
import idempotency_key
import int
import isinstance
import kind
import len
import list
import max_agents_per_owner
import name
import owner_id
import policies
import prompt
import self
import str
import t
import tid
import tool_resolver
import tools
    AgentCreationError,
    ExternalServiceError,
    ResourceLimitExceededError,
    ValidationError,
)

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.agent import AgentRepository

    class ToolSpec(TypedDict, total=False):  # pragma: no cover - typing shim
        id: str
        name: str
        version: str | None

    class PolicySet(TypedDict, total=False):
        policies: dict[str, Any]

    # AnalyticsService is intentionally not imported for TYPE_CHECKING here to avoid import cycles

    class ToolResolver:  # minimal interface used by this use case
        async def resolve_many(
            self, specs: list[ToolSpec]
        ) -> list[str]:  # returns list of tool ids
            ...


class CreateAgentUseCase:
    """Create an Agent with validation, tool resolution and event tracking.

    Contract (summary):
    - Input: name, kind, prompt, tools, policies, owner_id, idempotency_key?
    - Output: created Agent domain entity
    - Side-effects: persists via AgentRepository, calls ToolResolver, emits analytics
    """

    def __init__(
        self,
        agent_repository: AgentRepository,
        tool_resolver: Any = None,
        analytics: Any = None,
        max_agents_per_owner: int = 20,
    ) -> None:
        self._repo = agent_repository
        self._tools = tool_resolver
        self._analytics = analytics
        self._max_agents_per_owner = int(max_agents_per_owner)

    async def execute(
        self,
        *,
        name: str,
        kind: str,
        prompt: str,
        tools: list[dict[str, Any]] | None,
        policies: dict[str, Any] | None,
        owner_id: UUID,
        idempotency_key: str | None = None,
    ) -> Agent:
        """Create a new Agent.

        Raises:
            ValidationError: on invalid input
            AgentCreationError: on name conflict or repo failures
            ResourceLimitExceededError: if owner quota exceeded
            ExternalServiceError: on tool resolution failure
        """
        # Basic validation
        if not name or not name.strip():
            raise ValidationError("name", name, "must be a non-empty string")
        if len(name) > 80:
            raise ValidationError("name", name, "max length is 80 chars")
        if kind not in {"assistant", "tool", "workflow"}:
            raise ValidationError("kind", kind, "invalid kind")
        if not isinstance(owner_id, UUID):
            raise ValidationError("owner_id", owner_id, "must be UUID")

        # Check uniqueness per owner and idempotency
        try:
            existing = await self._repo.get_by_owner(owner_id)
        except Exception as e:
            raise AgentCreationError(str(e)) from e

        # Idempotency: if key provided and agent exists with same idempotency key, return it
        if idempotency_key:
            for a in existing:
                if a.metadata.get("idempotency_key") == idempotency_key:
                    return a

        # Name uniqueness
        for a in existing:
            if a.name == name and a.owner_id == owner_id:
                raise AgentCreationError("Agent name already exists for owner")

        # Quota check
        if len(existing) >= self._max_agents_per_owner:
            raise ResourceLimitExceededError(
                resource="agents",
                limit=self._max_agents_per_owner,
                current=len(existing),
            )

        # Resolve tools (best-effort)
        resolved_tool_ids = await self._resolve_tools(tools)

        # Validate tool compatibility (simple heuristic)
        if kind == "assistant" and any(
            t.startswith("worker_") for t in resolved_tool_ids
        ):
            raise ValidationError(
                "tools", resolved_tool_ids, "incompatible tools for assistant"
            )

        # Build Agent entity
        now = datetime.now(UTC)
        _ = Agent(
            id=uuid4(),
            name=name.strip(),
            description=prompt or "",
            owner_id=owner_id,
            config=AgentConfig(),
            status=AgentStatus.INACTIVE,
            created_at=now,
            updated_at=now,
            metadata={"policies": policies or {}, "idempotency_key": idempotency_key},
        )

        # Attach tools
        for tid in resolved_tool_ids:
            agent.attach_tool(tid)

        # Persist
        try:
            created = await self._repo.create(agent)
        except Exception as e:
            raise AgentCreationError(str(e)) from e

        # Emit analytics/audit event if analytics service available
        try:
            if self._analytics:
                await self._analytics.track_event(
                    "agent.created",
                    user_id=str(owner_id),
                    agent_id=str(created.id),
                    metadata={"kind": kind, "tools": resolved_tool_ids},
                )
        except Exception:
            # Do not fail creation on analytics failure; log via ExternalServiceError
            raise ExternalServiceError(
                "analytics", "track_event", "failed to record event"
            )

        return created

    async def _resolve_tools(self, tools: list[dict[str, Any]] | None) -> list[str]:
        """Resolve tool specs to tool ids using the injected resolver or basic heuristics.

        Returns list of resolved tool ids; does not raise unless input is malformed or
        external resolver fails.
        """
        resolved_tool_ids: list[str] = []
        if not tools:
            return resolved_tool_ids

        if not self._tools:
            try:
                return [t["id"] for t in tools if "id" in t]
            except Exception as e:
                raise ValidationError("tools", tools, "invalid tool spec") from e

        try:
            return await self._tools.resolve_many(tools)  # type: ignore[attr-defined]
        except Exception as e:
            raise ExternalServiceError("ToolResolver", "resolve_many", str(e)) from e


# Backward compatible alias
CreateAgent = CreateAgentUseCase
