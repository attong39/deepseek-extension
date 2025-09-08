"""Memory service implementation (migrated from top-level memory_service.py).

This module contains the MemoryService implementation and is imported by
`core.services.memory.service` which re-exports the class.
"""

from __future__ import annotations

import logging
import threading
import warnings
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from typing import Any, ClassVar
from uuid import UUID

from apps.backend.core.common.base_classes import BaseService
from apps.backend.core.domain.entities.memory import (
import DeprecationWarning
import Exception
import IMPORTANCE_LEVELS
import LABEL_IMPORTANCE_WEIGHTS
import ValueError
import a
import abs
import age_days
import b
import bool
import content
import context
import dict
import enumerate
import exc
import float
import i
import importance
import importance_threshold
import int
import isinstance
import len
import limit
import list
import m
import m1
import m2
import max
import mid
import min
import next
import offset
import query
import round
import self
import set
import str
import sum
import type_counts
import unique_candidates
    Memory,
    MemoryImportance,
    MemoryType,
)
from apps.backend.core.services.memory._helpers import relevance_score

logger = logging.getLogger(__name__)
audit_logger = logging.getLogger("zeta.audit")

# NOTE: this module is an in-memory, synchronous implementation intended
# for tests and lightweight local usage. Production code should prefer the
# repository-backed `MemoryManagerService` found in
# `zeta_vn.core.services.memory_manager_service`.
warnings.warn(
    "core.services.memory._impl is an in-memory test shim; for production use core.services.memory_manager_service",
    DeprecationWarning,
    stacklevel=2,
)


IMPORTANCE_LEVELS: dict[str, int] = {"low": 0, "medium": 1, "high": 2, "critical": 3}
# label -> weight mapping used for importance-based multipliers
LABEL_IMPORTANCE_WEIGHTS: dict[str, float] = {
    "low": 0.2,
    "medium": 0.5,
    "high": 0.8,
    "critical": 1.0,
}


class MemoryService(BaseService):
    """Service for memory-related business operations.

    In-memory focused implementation originally contained in
    `core.services.memory_service.py`. This is the canonical implementation
    migrated into the `memory` subpackage.
    """

    _THRESHOLD_LEVELS: ClassVar[dict[str, int]] = IMPORTANCE_LEVELS.copy()

    def _setup(self) -> None:
        """Initialize in-memory storage structures for this service."""

        # Maps memory_id (str) -> Memory
        self._memories: dict[str, Memory] = {}

        # Indexes by agent_id (stringified UUID) and chat_id/source
        self._agent_memories: dict[str, list[str]] = {}
        self._chat_memories: dict[str, list[str]] = {}

        # Protect mutations for thread-safety (in-memory store)
        self._lock = threading.RLock()

    # --- helpers ---
    def _coerce_agent_uuid(self, agent_id: str | UUID | None) -> UUID | None:
        """Coerce agent_id to UUID if possible, or return None.

        Raises ValueError on invalid string input.
        """
        if agent_id is None:
            return None
        if isinstance(agent_id, UUID):
            return agent_id
        try:
            return UUID(agent_id)
        except Exception as exc:  # invalid uuid string
            raise ValueError(f"invalid agent_id UUID: {agent_id}") from exc

    def _similarity(self, a: Memory, b: Memory) -> float:
        """Compute simple word-overlap similarity between two memories."""

        wa = set(a.content.lower().split())
        wb = set(b.content.lower().split())
        union = len(wa | wb)
        if union == 0:
            return 0.0
        return len(wa & wb) / union

    def _combined_importance(self, a: Memory, b: Memory) -> str:
        """Pick the higher importance label between two memories."""
        v = max(
            LABEL_IMPORTANCE_WEIGHTS.get(a.importance.value, 0.5),
            LABEL_IMPORTANCE_WEIGHTS.get(b.importance.value, 0.5),
        )
        if v >= 1.0:
            return "critical"
        if v >= 0.8:
            return "high"
        if v >= 0.5:
            return "medium"
        return "low"

    def create_memory(
        self,
        content: str,
        memory_type: str,
        agent_id: str | UUID | None = None,
        chat_id: str | None = None,
        importance: str = "medium",
        context: dict[str, Any] | None = None,
    ) -> Memory:
        """Create a new memory.

        Args:
            content: Content of the memory.
            memory_type: Type of memory (episodic, semantic, etc.).
            agent_id: ID of the agent this memory belongs to.
            chat_id: ID of the chat this memory relates to.
            importance: Importance level (low, medium, high, critical).
            context: Additional context for the memory.

        Returns:
            Created memory entity.
        """

        # Validate / coerce agent id safely
        agent_uuid = self._coerce_agent_uuid(agent_id) if agent_id is not None else None

        # domain Memory currently expects source: str so default to empty string
        source_value = chat_id or ""

        memory = Memory(
            content=content,
            type=MemoryType(memory_type),
            agent_id=agent_uuid,
            source=source_value,
            importance=MemoryImportance(importance),
            context=context or {},
        )

        memory_id = str(memory.id)
        agent_key = str(agent_uuid) if agent_uuid is not None else None

        with self._lock:
            self._memories[memory_id] = memory

            if agent_key:
                if agent_key not in self._agent_memories:
                    self._agent_memories[agent_key] = []
                self._agent_memories[agent_key].append(memory_id)

            if chat_id:
                if chat_id not in self._chat_memories:
                    self._chat_memories[chat_id] = []
                self._chat_memories[chat_id].append(memory_id)

        audit_logger.info(
            "memory.created",
            extra={"memory_id": memory_id, "agent_id": agent_key, "type": memory_type},
        )
        logger.info("Created %s memory %s", memory_type, memory_id)
        return memory

    def get_memory(self, memory_id: str | UUID) -> Memory | None:
        """Get a memory by ID."""
        return self._memories.get(str(memory_id))

    def get_agent_memories(
        self,
        agent_id: str | UUID,
        memory_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Memory]:
        """Get memories for a specific agent."""

        # normalize agent key to stringified UUID
        agent_key = str(agent_id)
        memory_ids = self._agent_memories.get(agent_key, [])
        memories = [self._memories[mid] for mid in memory_ids if mid in self._memories]

        if memory_type:
            memories = [m for m in memories if m.type.value == memory_type]

        memories.sort(
            key=lambda m: (m.importance.value, m.created_at),
            reverse=True,
        )

        return memories[offset : offset + limit]

    def get_chat_memories(
        self,
        chat_id: str,
        memory_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Memory]:
        """Get memories for a specific chat."""

        memory_ids = self._chat_memories.get(chat_id, [])
        memories = [self._memories[mid] for mid in memory_ids if mid in self._memories]

        if memory_type:
            memories = [m for m in memories if m.type.value == memory_type]

        memories.sort(key=lambda m: m.created_at, reverse=True)
        return memories[offset : offset + limit]

    def search_memories(
        self,
        query: str,
        agent_id: str | None = None,
        chat_id: str | None = None,
        memory_type: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Memory]:
        """Search memories by content."""

        query_lower = query.lower()

        if agent_id:
            candidates = self.get_agent_memories(agent_id, limit=1000)
        elif chat_id:
            candidates = self.get_chat_memories(chat_id, limit=1000)
        else:
            candidates = list(self._memories.values())

        matching_memories: list[Memory] = []
        for memory in candidates:
            if query_lower in memory.content.lower():
                matching_memories.append(memory)

        if memory_type:
            matching_memories = [
                m for m in matching_memories if m.type.value == memory_type
            ]

        def relevance_score(memory: Memory) -> float:
            content_lower = memory.content.lower()
            score = LABEL_IMPORTANCE_WEIGHTS.get(memory.importance.value, 0.5)
            if content_lower.startswith(query_lower):
                score += 0.3
            elif query_lower in content_lower[:100]:
                score += 0.2
            elif query_lower in content_lower:
                score += 0.1
            return score

        matching_memories.sort(key=relevance_score, reverse=True)
        return matching_memories[offset : offset + limit]

    def update_memory(
        self,
        memory_id: str | UUID,
        content: str | None = None,
        importance: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> bool:
        """Update an existing memory."""

        memory = self.get_memory(memory_id)
        if not memory:
            return False

        if content is not None:
            memory.update_content(content)

        if importance is not None:
            memory.importance = MemoryImportance(importance)

        if context is not None:
            memory.context = context

        memory.updated_at = datetime.now(UTC)
        audit_logger.info("memory.updated", extra={"memory_id": str(memory.id)})
        logger.info("Updated memory %s", memory_id)
        return True

    def delete_memory(self, memory_id: str | UUID) -> bool:
        """Delete a memory."""

        memory_id_str = str(memory_id)
        memory = self.get_memory(memory_id_str)
        if not memory:
            return False

        with self._lock:
            self._memories.pop(memory_id_str, None)

            if memory.agent_id:
                agent_id = str(memory.agent_id)
                if agent_id in self._agent_memories:
                    self._agent_memories[agent_id] = [
                        mid
                        for mid in self._agent_memories[agent_id]
                        if mid != memory_id_str
                    ]

            if memory.source:
                chat_id = memory.source
                if chat_id in self._chat_memories:
                    self._chat_memories[chat_id] = [
                        mid
                        for mid in self._chat_memories[chat_id]
                        if mid != memory_id_str
                    ]

        audit_logger.info("memory.deleted", extra={"memory_id": memory_id_str})
        logger.info("Deleted memory %s", memory_id)
        return True

    def consolidate_memories(
        self,
        agent_id: str,
        importance_threshold: str = "high",
    ) -> int:
        """Consolidate important memories for an agent.

        Finds pairs with high content similarity and merges them by
        concatenating content and keeping the higher importance.
        """

        memories = self.get_agent_memories(agent_id, limit=1000)
        threshold_value = self._THRESHOLD_LEVELS.get(importance_threshold, 2)

        important = [
            m
            for m in memories
            if self._THRESHOLD_LEVELS.get(m.importance.value, 1) >= threshold_value
        ]

        if len(important) < 2:
            return 0

        consolidated = 0
        with self._lock:
            for i, m1 in enumerate(important):
                match = next(
                    (m2 for m2 in important[i + 1 :] if self._similarity(m1, m2) > 0.6),
                    None,
                )
                if not match:
                    continue
                combined_content = f"{m1.content} {match.content}"
                self.update_memory(
                    m1.id,
                    content=combined_content,
                    importance=self._combined_importance(m1, match),
                )
                self.delete_memory(match.id)
                consolidated += 1

        if consolidated:
            audit_logger.info(
                "memory.consolidated",
                extra={"agent_id": str(agent_id), "count": consolidated},
            )
            logger.info("Consolidated %d memories for agent %s", consolidated, agent_id)
        return consolidated

    def forget_memories(
        self,
        agent_id: str,
        importance_threshold: str = "low",
        age_days: int = 30,
    ) -> int:
        """Forget old or unimportant memories for an agent."""

        memories = self.get_agent_memories(agent_id, limit=1000)
        cutoff_time = datetime.now(UTC) - timedelta(days=age_days)
        forgotten_count = 0
        threshold_value = IMPORTANCE_LEVELS.get(importance_threshold, 0)

        with self._lock:
            for memory in memories:
                memory_importance_level = IMPORTANCE_LEVELS.get(
                    memory.importance.value, 1
                )
                if (
                    memory_importance_level <= threshold_value
                    and memory.created_at <= cutoff_time
                ):
                    self.delete_memory(memory.id)
                    forgotten_count += 1

        if forgotten_count > 0:
            audit_logger.info(
                "memory.forgotten",
                extra={"agent_id": str(agent_id), "count": forgotten_count},
            )
            logger.info("Forgot %d memories for agent %s", forgotten_count, agent_id)
        return forgotten_count

    def get_memory_statistics(self, agent_id: str) -> dict[str, Any]:
        """Get memory statistics for an agent."""

        memories = self.get_agent_memories(agent_id, limit=1000)
        if not memories:
            return {
                "agent_id": agent_id,
                "total_memories": 0,
                "by_type": {},
                "avg_importance": 0.0,
                "oldest_memory": None,
                "newest_memory": None,
            }

        type_counts: dict[str, int] = {}
        for memory in memories:
            memory_type = memory.type.value
            type_counts[memory_type] = type_counts.get(memory_type, 0) + 1

        avg_importance = sum(
            LABEL_IMPORTANCE_WEIGHTS.get(m.importance.value, 0.5) for m in memories
        ) / len(memories)

        oldest_memory = min(memories, key=lambda m: m.created_at)
        newest_memory = max(memories, key=lambda m: m.created_at)

        return {
            "agent_id": agent_id,
            "total_memories": len(memories),
            "by_type": type_counts,
            "avg_importance": round(avg_importance, 3),
            "oldest_memory": oldest_memory.created_at.isoformat(),
            "newest_memory": newest_memory.created_at.isoformat(),
        }

    def export_agent_memories(self, agent_id: str) -> dict[str, Any]:
        """Export all memories for an agent."""

        memories = self.get_agent_memories(agent_id, limit=10000)
        return {
            "agent_id": agent_id,
            "export_timestamp": datetime.now(UTC).isoformat(),
            "total_memories": len(memories),
            "memories": [
                {
                    "id": str(memory.id),
                    "content": memory.content,
                    "memory_type": memory.type.value,
                    "importance": memory.importance.value,
                    "created_at": memory.created_at.isoformat(),
                    "updated_at": memory.updated_at.isoformat()
                    if memory.updated_at
                    else None,
                    "source": memory.source or None,
                    "context": memory.context,
                }
                for memory in memories
            ],
            "statistics": self.get_memory_statistics(agent_id),
        }

    def get_related_memories(
        self,
        memory_id: str | UUID,
        limit: int = 10,
    ) -> Sequence[Memory]:
        """Get memories related to a specific memory."""

        reference_memory = self.get_memory(memory_id)
        if not reference_memory:
            return []

        candidates: list[Memory] = []
        if reference_memory.agent_id:
            candidates.extend(
                self.get_agent_memories(str(reference_memory.agent_id), limit=1000)
            )
        if reference_memory.source:
            candidates.extend(
                self.get_chat_memories(reference_memory.source, limit=1000)
            )

        unique_candidates: list[Memory] = []
        seen_ids = {str(reference_memory.id)}
        for memory in candidates:
            memory_id_str = str(memory.id)
            if memory_id_str not in seen_ids:
                unique_candidates.append(memory)
                seen_ids.add(memory_id_str)

        def relatedness_score(memory: Memory) -> float:
            # lightweight lexical similarity
            ref_words = set(reference_memory.content.lower().split())
            mem_words = set(memory.content.lower().split())
            overlap = len(ref_words.intersection(mem_words))
            total_words = len(ref_words.union(mem_words))
            similarity = overlap / total_words if total_words > 0 else 0.0
            # importance mapped to 0..1
            importance_weight = LABEL_IMPORTANCE_WEIGHTS.get(
                memory.importance.value, 0.5
            )
            # recency in days
            time_diff = abs(
                (memory.created_at - reference_memory.created_at).total_seconds()
            )
            recency_days = time_diff / 86400.0
            # approximate source quality placeholder (1.0 if same chat/source else 0.5)
            source_quality = (
                1.0
                if memory.source and memory.source == reference_memory.source
                else 0.5
            )
            # combine using common helper
            return relevance_score(
                similarity * importance_weight, recency_days, source_quality
            )

        unique_candidates.sort(key=relatedness_score, reverse=True)
        return unique_candidates[:limit]
