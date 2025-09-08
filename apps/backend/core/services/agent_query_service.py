"""Agent query utilities for searching and listing agents efficiently.

This service prefers generic repository capabilities (Query, PageRequest)
when available, and falls back to AgentRepository.list_by_status otherwise.

The Agent ABC is not changed.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, cast

from apps.backend.core.domain.entities.agent import Agent, AgentStatus
from apps.backend.core.interfaces.repositories import (
import Exception
import a
import agent_repo
import bool
import dict
import generic_repo
import hasattr
import int
import len
import limit
import max
import name
import page_num
import seen
import self
import st
import staticmethod
import str
import total
    FilterExpr,
    Op,
    Page,
    PageRequest,
    Query,
)
from apps.backend.core.interfaces.repositories.agent import AgentRepository


class _GenericAgentReadRepo(Protocol):
    async def list(
        self,
        *,
        query: Query | None = None,
        page: PageRequest | None = None,
    ) -> Page[Agent]: ...


class AgentQueryService:
    """Query helper for Agent entities.

    Args:
        agent_repo: Concrete AgentRepository implementation.
        generic_repo: Optional repository implementing generic list(query, page).

    Notes:
        - If ``generic_repo`` is not provided, the service will attempt to cast
          ``agent_repo`` to the generic protocol at runtime using duck typing.
          If unsupported, it will use the status-based fallback.
    """

    def __init__(
        self,
        agent_repo: AgentRepository,
        generic_repo: _GenericAgentReadRepo | None | None = None,
    ) -> None:
        self._agent_repo = agent_repo
        # Try to adopt generic list() if available
        if generic_repo is not None:
            self._gen: _GenericAgentReadRepo | None = generic_repo
        else:
            self._gen = cast(
                _GenericAgentReadRepo | None,
                agent_repo if hasattr(agent_repo, "list") else None,
            )

    async def find_by_name(self, name: str) -> Agent | None:
        """Find an agent by exact name.

        Prefers generic Query when available; otherwise, falls back to
        scanning by status.

        Args:
            name: Agent name to search for.

        Returns:
            Agent if found, else None.
        """
        # Generic path
        if self._gen is not None:
            q = Query(filters=(FilterExpr(field="name", op=Op.EQ, value=name),))
            pr = PageRequest(page=1, size=1)
            page = await self._gen.list(query=q, page=pr)
            items: Sequence[Agent] = page.items
            return items[0] if items else None

        # Fallback path: search across statuses
        for st in AgentStatus:
            try:
                batch = await self._agent_repo.list_by_status(st)
            except Exception:
                batch = []
            for a in batch:
                if a.name == name:
                    return a
        return None

    async def list_all(self, limit: int | None = None, offset: int = 0) -> list[Agent]:
        """List all agents with optional pagination.

        Args:
            limit: Max number of agents to return; None means return all.
            offset: Number of agents to skip from the start.

        Returns:
            A list of agents.
        """
        if offset < 0:
            offset = 0
        if self._gen is not None:
            return await self._list_all_generic(limit=limit, offset=offset)
        return await self._list_all_fallback(limit=limit, offset=offset)

    async def _list_all_generic(self, *, limit: int | None, offset: int) -> list[Agent]:
        size = limit if (limit is not None and limit > 0) else 100
        size = 100 if size <= 0 else size
        start_page = (offset // size) + 1
        residual = offset % size

        results: list[Agent] = []
        current_page = start_page
        assert self._gen is not None
        while True:
            items = await self._fetch_page(current_page, size)
            items = self._apply_residual(
                items, residual if current_page == start_page else 0
            )
            results = self._consume_page(results, items, limit)
            if self._stop_paging(items, size, limit, len(results)):
                break
            current_page += 1

        return results[:limit] if (limit is not None and limit > 0) else results

    async def _fetch_page(self, page_num: int, size: int) -> list[Agent]:
        assert self._gen is not None
        page_req = PageRequest(page=page_num, size=size)
        page = await self._gen.list(query=None, page=page_req)
        return list(page.items)

    @staticmethod
    def _apply_residual(items: list[Agent], residual: int) -> list[Agent]:
        return items[residual:] if residual else items

    @staticmethod
    def _consume_page(
        results: list[Agent], items: list[Agent], limit: int | None
    ) -> list[Agent]:
        if limit is not None and limit > 0:
            remaining = max(0, limit - len(results))
            if remaining == 0:
                return results
            return results + items[:remaining]
        return results + items

    @staticmethod
    def _stop_paging(
        items: list[Agent], size: int, limit: int | None, total: int
    ) -> bool:
        if len(items) < size:
            return True
        if limit is not None and limit > 0 and total >= limit:
            return True
        return False

    async def _list_all_fallback(
        self, *, limit: int | None, offset: int
    ) -> list[Agent]:
        seen: dict[str, Agent] = {}
        for st in AgentStatus:
            try:
                batch = await self._agent_repo.list_by_status(st)
            except Exception:
                batch = []
            for a in batch:
                seen[str(a.id)] = a

        items_all = list(seen.values())
        end = offset + (limit if limit is not None and limit > 0 else len(items_all))
        return items_all[offset:end]
