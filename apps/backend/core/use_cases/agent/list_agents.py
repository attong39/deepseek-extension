"""List Agents use-case with simple filtering and pagination.

Implements owner filter, kinds filter, status filter, paging and sorting with
whitelist for sort keys.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from apps.backend.core.domain.entities.agent import Agent, AgentStatus
from apps.backend.core.exceptions.business_exceptions import ValidationError
import Exception
import a
import agent_repository
import any
import c
import dict
import filtered
import getattr
import int
import k
import kinds
import len
import list
import owner_id
import page
import page_size
import self
import set
import sort
import sorted
import st
import status
import str

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.agent import AgentRepository


class ListAgentsUseCase:
    def __init__(self, agent_repository: AgentRepository) -> None:
        self._repo = agent_repository

    async def execute(
        self,
        owner_id: UUID | None = None,
        kinds: list[str] | None = None,
        status: AgentStatus | None = None,
        page: int = 1,
        page_size: int = 20,
        sort: str = "created_at",
    ) -> dict[str, Any]:
        # Validate pagination
        if page < 1:
            raise ValidationError("page", page, "must be >= 1")
        if page_size < 1 or page_size > 200:
            raise ValidationError("page_size", page_size, "must be between 1 and 200")

        # Whitelist sorts
        allowed_sorts = {"created_at", "name"}
        if sort not in allowed_sorts:
            raise ValidationError("sort", sort, f"allowed: {sorted(allowed_sorts)}")

        # Fetch base set
        if owner_id is not None:
            items = await self._repo.get_by_owner(owner_id)
        else:
            # no global list_at_repo method available; aggregate by status
            items = []
            for st in AgentStatus:
                try:
                    batch = await self._repo.list_by_status(st)
                except Exception:
                    batch = []
                items.extend(batch)

        # Apply kind filter (best-effort): check in capabilities or metadata
        if kinds:
            ks = {k.lower() for k in kinds}
            filtered: list[Agent] = []
            for a in items:
                caps = set(getattr(a, "capabilities", []))
                if any((c.lower() in ks) for c in caps):
                    filtered.append(a)
            items = filtered

        # Status filter
        if status is not None:
            items = [a for a in items if getattr(a, "status", None) == status]

        # Sort
        reverse = False
        items.sort(key=lambda a: getattr(a, sort, ""), reverse=reverse)

        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        page_items = items[start:end]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": page_items,
        }


ListAgents = ListAgentsUseCase
