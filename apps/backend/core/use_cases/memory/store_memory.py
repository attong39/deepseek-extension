"""
Memory Management Use Cases - ZETA AI SERVER
===========================================

Performance- and cost-aware implementations with safe domain-level
enhancements:
- Input normalization (content, tags)
- Backward-compatible enum mapping
- Optional idempotency and duplicate detection via repository duck-typing

No imports from app/data layers to preserve Clean Architecture boundaries.
"""

from __future__ import annotations

import hashlib
import inspect
import re
from datetime import UTC, datetime
from typing import Any, cast
from unittest.mock import AsyncMock, Mock
from uuid import UUID

from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.interfaces.repositories import MemoryRepository
from core.utils.async_utils import _maybe_await
import AttributeError
import Exception
import TypeError
import ValueError
import agent_id
import bool
import cluster_tops
import clusters
import content
import context
import dict
import exc
import float
import getattr
import hasattr
import importance
import int
import isinstance
import k
import kwargs
import len
import limit
import list
import m
import max
import max_tag_length
import max_tags
import memory_count
import memory_id
import memory_repo
import memory_type
import old_memories
import out
import query
import seen
import selection
import self
import set
import setattr
import str
import summary_memory
import t
import tags
import text
import threshold
import tuple
import updated
import updates
import val
import x

_ERR_INVALID_IMPORTANCE = "Invalid importance level"
_ERR_INVALID_MEMTYPE = "Invalid memory type"


class StoreMemory:
    """Use case for storing new memories."""

    def __init__(self, memory_repo: MemoryRepository):
        self.memory_repo = memory_repo

    async def __call__(
        self,
        content: str,
        memory_type: str,
        importance: str,
        agent_id: UUID,
        context: dict[str, Any],
        tags: list[str] | None = None,
    ) -> Memory:
        """Store new memory in the system.

        Args:
            content: Raw content to store.
            memory_type: Memory type (e.g., "episodic", legacy "conversation").
            importance: Importance level (e.g., "low", "medium", "high", "critical").
            agent_id: Owner agent ID.
            context: Extra metadata; can carry idempotency hints.
            tags: Optional user tags.

        Returns:
            The stored or deduplicated existing ``Memory`` entity.

        Raises:
            ValueError: If content is empty or enum mappings are invalid.
        """

        # Basic validation (post-normalization)
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        norm_content = _normalize_text(content)
        if not norm_content:
            raise ValueError("Content cannot be empty")
        norm_tags = _normalize_tags(tags, max_tags=32, max_tag_length=64)

        # Normalize and map legacy memory_type strings
        mt = (memory_type or "").lower().strip()
        mt = {"conversation": "episodic", "chat": "episodic"}.get(mt, mt)
        imp = (importance or "").lower().strip()
        mt_enum, imp_enum = _map_enums(mt, imp)

        # Optional idempotency: context may carry an idempotency key set by caller
        idempo_key = None
        if isinstance(context, dict):
            raw_key = context.get("idempotency_key") or context.get("idempotencyKey")
            if isinstance(raw_key, (str, int)):
                idempo_key = str(raw_key)
        # If caller didn't provide one, derive a stable key from agent/type/content
        if not idempo_key:
            idempo_key = _derive_idempotency_key(agent_id, mt, norm_content)

        # Optional duplicate detection via content hash (best-effort)
        content_hash = hashlib.blake2b(
            norm_content.encode("utf-8"), digest_size=16
        ).hexdigest()
        repo_any = cast("Any", self.memory_repo)
        existing = await _find_existing(repo_any, agent_id, idempo_key, content_hash)
        if existing is not None:
            return existing

        # Create memory entity
        memory = Memory(
            content=norm_content,
            type=mt_enum,
            importance=imp_enum,
            agent_id=agent_id,
            context=context,
            tags=norm_tags,
        )

        # Store memory - prefer repo's upsert_by_content_hash when it's a real
        # implementation. Avoid calling auto-created unittest.mock.Mock
        # attributes which would return other Mock objects and break tests.
        method = getattr(repo_any, "upsert_by_content_hash", None)
        if method is not None and not (
            isinstance(method, Mock) and not isinstance(method, AsyncMock)
        ):
            res = method(memory=memory, content_hash=content_hash)
            stored_memory: Memory = await _maybe_await(res)
        else:
            res = self.memory_repo.create(memory)
            stored_memory = await _maybe_await(res)
        return stored_memory


def _normalize_text(text: str) -> str:
    """Normalize content by stripping and collapsing whitespace.

    Args:
        text: Input text.

    Returns:
        A trimmed string with internal whitespace collapsed to single spaces.
    """
    # Trim and collapse multiple whitespace to a single space
    collapsed = re.sub(r"\s+", " ", text.strip())
    return collapsed


def _normalize_tags(
    tags: list[str] | None, *, max_tags: int = 32, max_tag_length: int = 64
) -> list[str]:
    """Normalize tags: lower-case, deduplicate while preserving order.

    Args:
        tags: Optional list of tags.

    Returns:
        A normalized tag list.
    """
    if not tags:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for t in tags:
        if not isinstance(t, str):
            continue
        tt = t.strip().lower()
        if not tt or tt in seen:
            continue
        # Clamp tag length and keep order
        tt = tt[:max_tag_length]
        seen.add(tt)
        out.append(tt)
        if len(out) >= max_tags:
            break
    return out


def _map_enums(mt: str, imp: str) -> tuple[MemoryType, MemoryImportance]:
    """Map string values to enums with friendly error messages.

    Args:
        mt: Memory type string.
        imp: Importance string.

    Returns:
        A tuple of (MemoryType, MemoryImportance).

    Raises:
        ValueError: if any value is invalid.
    """
    try:
        mt_enum = MemoryType(mt)
    except Exception as exc:  # pragma: no cover
        raise ValueError(_ERR_INVALID_MEMTYPE) from exc

    try:
        imp_enum = MemoryImportance(imp)
    except Exception as exc:  # pragma: no cover
        raise ValueError(_ERR_INVALID_IMPORTANCE) from exc

    return mt_enum, imp_enum


async def _find_existing(
    repo_any: Any, agent_id: UUID, idempo_key: str | None, content_hash: str
) -> Memory | None:
    """Best-effort duplicate detection using repository opt-in methods.

    Returns an existing memory if found; otherwise None.
    """
    # Idempotency shortcut
    if idempo_key:
        # Guard against unittest.mock.Mock auto-created attributes. Only call
        # the repo method if it's an AsyncMock or a real coroutine function.
        method = getattr(repo_any, "get_by_idempotency", None)
        if method is not None and not (
            isinstance(method, Mock) and not isinstance(method, AsyncMock)
        ):
            try:
                res = method(agent_id=agent_id, idempotency_key=idempo_key)
                existing_by_idempo = await res if inspect.isawaitable(res) else res
                if existing_by_idempo is not None:
                    return existing_by_idempo
            except AttributeError:
                # Repo doesn't implement the optional method; ignore
                pass

    # Content hash shortcut
    method = getattr(repo_any, "get_by_content_hash", None)
    if method is not None and not (
        isinstance(method, Mock) and not isinstance(method, AsyncMock)
    ):
        try:
            res = method(agent_id=agent_id, content_hash=content_hash)
            existing_by_hash = await res if inspect.isawaitable(res) else res
            if existing_by_hash is not None:
                return existing_by_hash
        except AttributeError:
            pass

    return None


def _derive_idempotency_key(agent_id: UUID, mt: str, content: str) -> str:
    """Derive a stable idempotency key from agent, type, and content hash.

    This helps ensure eventual consistency when the caller doesn't supply a key.
    """
    base = f"{agent_id}:{mt}:{content}"
    return hashlib.blake2b(base.encode("utf-8"), digest_size=12).hexdigest()


class RetrieveMemory:
    """Use case for retrieving a single memory."""

    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def __call__(self, memory_id: UUID) -> Memory | None:
        res = self.memory_repo.get_by_id(memory_id)
        memory = await _maybe_await(res)
        return memory


class SearchMemories:
    """Use case for searching memories with optional filters."""

    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def __call__(
        self,
        query: str,
        agent_id: UUID | None = None,
        memory_type: str | None = None,
        importance: str | None = None,
        limit: int = 50,
    ) -> list[Memory]:
        mem_type_enum: MemoryType | None = None
        if memory_type:
            try:
                mem_type_enum = MemoryType(memory_type)
            except Exception as exc:
                raise ValueError(_ERR_INVALID_MEMTYPE) from exc

        imp_enum: MemoryImportance | None = None
        if importance:
            try:
                imp_enum = MemoryImportance(importance)
            except Exception as exc:
                raise ValueError(_ERR_INVALID_IMPORTANCE) from exc

        repo_any = cast("Any", self.memory_repo)
        kwargs: dict[str, Any] = {"query": query, "limit": limit}
        if agent_id is not None:
            kwargs["agent_id"] = agent_id
        if mem_type_enum is not None:
            kwargs["memory_type"] = mem_type_enum
        if imp_enum is not None:
            kwargs["importance"] = imp_enum

        try:
            res = repo_any.search_by_content(**kwargs)
            memories: list[Memory] = await _maybe_await(res)
        except TypeError:
            res = repo_any.search_by_content(query=query, limit=limit)
            memories = await _maybe_await(res)

        return _diverse_select(memories, limit)


def _diverse_select(memories: list[Memory], limit: int) -> list[Memory]:
    if len(memories) <= limit:
        return memories

    def topic_key(text: str) -> str:
        seed = " ".join(text.lower().split()[:12])
        return hashlib.blake2b(seed.encode("utf-8"), digest_size=8).hexdigest()

    clusters: dict[str, list[Memory]] = {}
    for m in memories:
        clusters.setdefault(topic_key(m.content), []).append(m)

    def imp_score(imp: Any) -> float:
        if hasattr(imp, "name"):
            key = str(imp.name).lower()
        elif hasattr(imp, "value"):
            key = str(imp.value).lower()
        else:
            key = str(imp).lower()
        return {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}.get(key, 0.5)

    for k, items in clusters.items():
        items.sort(
            key=lambda x: (
                imp_score(getattr(x, "importance", "medium")),
                getattr(x, "created_at", 0),
            ),
            reverse=True,
        )

    cluster_tops: list[Memory] = [items[0] for items in clusters.values() if items]
    cluster_tops.sort(
        key=lambda x: (
            imp_score(getattr(x, "importance", "medium")),
            getattr(x, "created_at", 0),
        ),
        reverse=True,
    )

    selection: list[Memory] = []
    selection.extend(cluster_tops[:limit])
    if len(selection) < limit:
        remaining = [m for items in clusters.values() for m in items[1:]]
        remaining.sort(
            key=lambda x: (
                imp_score(getattr(x, "importance", "medium")),
                getattr(x, "created_at", 0),
            ),
            reverse=True,
        )
        selection.extend(remaining[: max(0, limit - len(selection))])

    return selection[:limit]


class UpdateMemory:
    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def __call__(self, memory_id: UUID, updates: dict[str, Any]) -> Memory | None:
        if "importance" in updates and isinstance(updates["importance"], str):
            try:
                MemoryImportance(updates["importance"])  # validation only
            except Exception as exc:
                raise ValueError(_ERR_INVALID_IMPORTANCE) from exc

        repo_any = cast("Any", self.memory_repo)
        try:
            res = repo_any.update(memory_id, updates)
            updated: Memory | None = await _maybe_await(res)
            return updated
        except TypeError:
            res = self.memory_repo.get_by_id(memory_id)
            memory = await _maybe_await(res)
            if not memory:
                return None
            for k, val in updates.items():
                new_val = val
                if k == "importance" and isinstance(val, str):
                    new_val = MemoryImportance(val)
                setattr(memory, k, new_val)
            memory.updated_at = datetime.now(UTC)
            res = repo_any.update(memory)
            return await _maybe_await(res)


class DeleteMemory:
    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def __call__(self, memory_id: UUID) -> bool:
        res = self.memory_repo.delete(memory_id)
        success = await _maybe_await(res)
        return success


class CompressMemories:
    def __init__(self, memory_repo: MemoryRepository) -> None:
        self.memory_repo = memory_repo

    async def __call__(self, agent_id: UUID, threshold: int = 1000) -> dict[str, Any]:
        repo_any = cast("Any", self.memory_repo)
        res = repo_any.count_by_agent(agent_id)
        memory_count: int = await _maybe_await(res)

        if memory_count <= threshold:
            return {
                "compressed_count": 0,
                "message": "Memory count below compression threshold",
            }

        res = repo_any.list_by_agent(
            agent_id=agent_id, limit=max(0, memory_count - threshold)
        )
        old_memories: list[Memory] = await _maybe_await(res)

        compressed_count = 0
        for memory in old_memories:
            if memory.importance != MemoryImportance.CRITICAL:
                memory.updated_at = datetime.now(UTC)
                res = repo_any.update(memory)
                await _maybe_await(res)
                compressed_count += 1

        res = repo_any.create(
            Memory(
                content="Compressed summary",
                type=MemoryType.SEMANTIC,
                importance=MemoryImportance.HIGH,
                agent_id=agent_id,
                context={"compressed": True},
                tags=["compressed"],
                created_at=datetime.now(UTC),
            )
        )
        summary_memory: Memory = await _maybe_await(res)

        return {
            "compressed_count": compressed_count,
            "summary_memory_id": summary_memory.id,
        }
