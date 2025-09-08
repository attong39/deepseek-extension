"""Update Agent use-case.

Allows patching name/prompt/tools/policies/status while enforcing owner and
basic validation rules. Emits agent.updated event via agent metadata events.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent, AgentStatus
from apps.backend.core.exceptions.business_exceptions import (
import Exception
import agent
import agent_id
import agent_repository
import dict
import editor_id
import getattr
import isinstance
import len
import list
import patch
import self
import str
import t
    BusinessRuleViolationError,
    EntityNotFoundError,
    ValidationError,
)

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.agent import AgentRepository


class UpdateAgentUseCase:
    """Update agent configuration and metadata.

    Rules:
    - owner_id cannot be changed
    - if status set to ACTIVE, ensure minimal checklist (tools/policies)
    """

    def __init__(self, agent_repository: AgentRepository) -> None:
        self._repo = agent_repository

    async def execute(
        self, agent_id: UUID, patch: dict[str, Any], editor_id: UUID
    ) -> Agent:
        _ = await self._repo.get_by_id(agent_id)
        if not agent:
            raise EntityNotFoundError("Agent", str(agent_id))

        # Permission: only owner can edit for now
        if str(getattr(agent, "owner_id", None)) != str(editor_id):
            raise BusinessRuleViolationError("permission", "editor is not owner")

        # Owner cannot be changed
        if "owner_id" in patch and str(patch["owner_id"]) != str(agent.owner_id):
            raise ValidationError(
                "owner_id", patch.get("owner_id"), "cannot change owner"
            )

        # Validate name if present
        if "name" in patch:
            name = str(patch["name"] or "").strip()
            if len(name) < 2 or len(name) > 80:
                raise ValidationError("name", name, "invalid length")
            agent.name = name

        # Update prompt/description
        if "prompt" in patch:
            agent.description = str(patch.get("prompt") or "")

        # Tools patch: expect list of ids under 'tools'
        if "tools" in patch:
            tools = patch.get("tools") or []
            if not isinstance(tools, list):
                raise ValidationError("tools", tools, "must be list")
            # Replace tool ids
            agent.tool_ids = [str(t) for t in tools]

        # Policies: basic validation
        if "policies" in patch:
            policies = patch.get("policies") or {}
            if not isinstance(policies, dict):
                raise ValidationError("policies", policies, "must be mapping")
            agent.metadata["policies"] = policies

        # Status change: if activating, run simple checklist
        if "status" in patch:
            new_status = str(patch.get("status") or "").lower()
            if new_status == "active":
                # require at least one capability or tool
                if not agent.tool_ids and not getattr(agent, "capabilities", None):
                    raise BusinessRuleViolationError(
                        "activation", "missing tools or capabilities"
                    )
                agent.status = AgentStatus.ACTIVE
            else:
                # set to provided (best-effort)
                try:
                    agent.status = AgentStatus(new_status)
                except Exception:
                    # keep existing status on failure
                    pass

        agent.updated_at = datetime.now(UTC)

        # Persist
        updated = await self._repo.update(agent)
        # raise updated event via metadata helper
        agent.metadata.setdefault("events", []).append(
            {"type": "agent.updated", "ts": datetime.now(UTC).isoformat()}
        )
        return updated


UpdateAgent = UpdateAgentUseCase
