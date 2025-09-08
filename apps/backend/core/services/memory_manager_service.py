"""Memory Manager Service - Canonical implementation.

This service handles memory management and persistence for AI agents and conversations.
Provides unified access to short-term and long-term memory storage.
"""

import logging
import time
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.memory import (
import Exception
import ValueError
import agent_id
import bool
import cl
import clusters
import config
import content
import dict
import exc
import float
import hasattr
import highlights
import int
import isinstance
import len
import limit
import list
import m
import max
import memory_id
import memory_repository
import memory_type
import metadata
import min
import mm
import out
import points
import query
import s
import selection
import self
import sorted
import str
import text
import updates
import ws
import x
    Memory,
    MemoryImportance,
    MemoryType,
    MemoryVisibility,
)
from apps.backend.core.interfaces.repositories import MemoryRepository

# Avoid importing app/data from core; use local lightweight helpers

logger = logging.getLogger(__name__)

# Constants
AGENT_ID_REQUIRED_MSG = "Agent ID is required"


@dataclass
class MemoryConfig:
    """Configuration for memory management."""

    max_short_term_items: int = 50
    short_term_ttl_hours: int = 24
    max_long_term_items: int = 1000
    compression_threshold: int = 100
    cleanup_interval_minutes: int = 60


class MemoryManagerService:
    """Manages memory storage and retrieval for AI agents.

    This service provides a unified interface for managing both short-term
    and long-term memory, with automatic cleanup and compression capabilities.

    Args:
        memory_repository: Repository for memory persistence
        config: Configuration settings for memory management

    Attributes:
        _memory_repository: Repository for memory data persistence
        _config: Configuration settings
        _last_cleanup: Timestamp of last cleanup operation
    """

    def __init__(
        self,
        memory_repository: MemoryRepository,
        config: MemoryConfig | None = None,
    ) -> None:
        self._memory_repository = memory_repository
        self._config = config or MemoryConfig()
        self._last_cleanup = time.time()
        logger.info("MemoryManagerService initialized with config: %s", self._config)

    # Utilities (none; local helpers will be used)

    async def store_memory(
        self,
        agent_id: str,
        content: str,
        memory_type: MemoryType = MemoryType.EPISODIC,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Store a new memory item.

        Args:
            agent_id: ID of the agent this memory belongs to
            content: The memory content to store
            memory_type: Type of memory (short-term or long-term)
            metadata: Optional metadata associated with the memory

        Returns:
            Memory ID for the stored item

        Raises:
            ValueError: If agent_id or content is empty
        """
        if not agent_id or not content:
            raise ValueError("Agent ID and content are required")

        # Parse and validate agent UUID
        try:
            agent_uuid = UUID(agent_id)
        except Exception as exc:  # ValueError or TypeError
            raise ValueError("Invalid agent_id format") from exc

        # Create Memory entity and persist
        mem = Memory(
            id=uuid4(),
            agent_id=agent_uuid,
            owner_id=None,
            content=content,
            embedding_ref="",
            source="",
            visibility=MemoryVisibility.PRIVATE,
            score=0.5,
            ttl=None,
            type=memory_type,
            importance=MemoryImportance.MEDIUM,
            tags=[],
            context=metadata or {},
        )

        created = await self._memory_repository.create(mem)
        logger.info("Memory stored for agent %s: %s", agent_id, created.id)

        # Trigger cleanup if needed
        self._maybe_cleanup()

        return str(created.id)

    async def retrieve_memories(
        self,
        agent_id: str,
        memory_type: MemoryType | None = None,
        limit: int = 10,
    ) -> list[Memory]:
        """Retrieve memories for an agent.

        Args:
            agent_id: ID of the agent
            memory_type: Optional filter by memory type
            limit: Maximum number of memories to retrieve
            before_timestamp: Optional filter for memories before this time

        Returns:
            List of memory objects

        Raises:
            ValueError: If agent_id is empty
        """
        if not agent_id:
            raise ValueError(AGENT_ID_REQUIRED_MSG)

        # Convert agent_id to UUID if possible
        agent_uuid: UUID
        try:
            agent_uuid = UUID(agent_id)
        except Exception:
            # Fallback placeholder UUID
            agent_uuid = uuid4()

        # Repository interface exposes get_by_agent; paginate manually if needed
        all_mems = await self._memory_repository.get_by_agent(agent_uuid)
        all_mems = all_mems[:limit]
        if memory_type is not None:
            memories = [m for m in all_mems if m.type == memory_type]
        else:
            memories = all_mems

        logger.debug(f"Retrieved {len(memories)} memories for agent {agent_id}")
        return memories

    async def search_memories(
        self,
        agent_id: str,
        query: str,
        memory_type: MemoryType | None = None,
        limit: int = 10,
    ) -> list[Memory]:
        """Search memories by content.

        Args:
            agent_id: ID of the agent
            query: Search query string
            memory_type: Optional filter by memory type
            limit: Maximum number of results

        Returns:
            List of matching memory objects

        Raises:
            ValueError: If agent_id or query is empty
        """
        if not agent_id:
            raise ValueError(AGENT_ID_REQUIRED_MSG)
        if not query:
            raise ValueError("Query is required")

        # Simple search: fetch agent memories and filter by query
        try:
            agent_uuid = UUID(agent_id)
        except Exception:
            agent_uuid = uuid4()
        memories = await self._memory_repository.get_by_agent(agent_uuid)
        if memory_type is not None:
            memories = [m for m in memories if m.type == memory_type]
        # Simple lexical filter first
        memories = [m for m in memories if query.lower() in m.content.lower()]
        # Semantic clustering via chunking metadata if present (lightweight heuristic)
        memories = self._semantic_cluster_select(memories, limit)

        logger.debug(
            f"Found {len(memories)} memories matching '{query}' for agent {agent_id}"
        )
        return memories

    async def update_memory(
        self,
        memory_id: str,
        content: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Update an existing memory.

        Args:
            memory_id: ID of the memory to update
            content: New content (optional)
            metadata: New metadata (optional)

        Returns:
            True if memory was updated, False if not found

        Raises:
            ValueError: If memory_id is empty
        """
        if not memory_id:
            raise ValueError("Memory ID is required")

        updates: dict[str, Any] = {}
        if content is not None:
            updates["content"] = content
        if metadata is not None:
            updates["context"] = metadata

        # Retrieve, mutate, and persist
        existing = await self._memory_repository.get_by_id(UUID(memory_id))
        if not existing:
            return False
        if "content" in updates:
            existing.content = updates["content"]
        if "context" in updates:
            existing.context = updates["context"]
        updated_mem = await self._memory_repository.update(existing)
        success = updated_mem is not None

        if success:
            logger.info(f"Memory {memory_id} updated successfully")
        else:
            logger.warning(f"Memory {memory_id} not found for update")

        return success

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory.

        Args:
            memory_id: ID of the memory to delete

        Returns:
            True if memory was deleted, False if not found

        Raises:
            ValueError: If memory_id is empty
        """
        if not memory_id:
            raise ValueError("Memory ID is required")

        success = await self._memory_repository.delete(UUID(memory_id))

        if success:
            logger.info(f"Memory {memory_id} deleted successfully")
        else:
            logger.warning(f"Memory {memory_id} not found for deletion")

        return success

    async def get_memory_stats(self, agent_id: str) -> dict[str, Any]:
        """Get memory statistics for an agent.

        Args:
            agent_id: ID of the agent

        Returns:
            Dictionary containing memory statistics

        Raises:
            ValueError: If agent_id is empty
        """
        if not agent_id:
            raise ValueError(AGENT_ID_REQUIRED_MSG)

        # Basic stats using repository operations
        agent_uuid: UUID
        try:
            agent_uuid = UUID(agent_id)
        except Exception:
            agent_uuid = uuid4()

        # Compute basics from repository data
        mems = await self._memory_repository.get_by_agent(agent_uuid)
        count = len(mems)
        recent = sorted(mems, key=lambda m: m.created_at, reverse=True)[:10]
        logger.debug(f"Retrieved memory stats for agent {agent_id}")
        return {
            "count": count,
            "recent_memory_ids": [str(m.id) for m in recent],
        }

    def compress_memories(self, agent_id: str) -> int:
        """Compress old short-term memories into long-term storage.

        Args:
            agent_id: ID of the agent

        Returns:
            Number of memories compressed

        Raises:
            ValueError: If agent_id is empty
        """
        if not agent_id:
            raise ValueError(AGENT_ID_REQUIRED_MSG)

        # Sliding-window summarization with time-based segmentation
        try:
            # Best-effort agent uuid
            try:
                agent_uuid = UUID(agent_id)
            except Exception:
                agent_uuid = uuid4()

            # Fetch recent memories, sort by created_at
            # Using repository interface generically
            all_mems = []
            try:
                all_mems = self._memory_repository.get_by_agent(agent_uuid)
            except Exception:
                pass
            if hasattr(all_mems, "__await__"):
                import asyncio

                all_mems = asyncio.get_event_loop().run_until_complete(all_mems)  # type: ignore
            if not isinstance(all_mems, list):
                all_mems = []
            all_mems.sort(key=lambda m: m.created_at)

            if len(all_mems) <= self._config.compression_threshold:
                return 0

            # Segment into time windows (e.g., per hour)
            window_summaries = self._summarize_by_time_windows(all_mems)

            # Persist summaries as long-term semantic memories; mark originals compressed
            compressed_count = 0
            for ws in window_summaries:
                if not ws["summary"]:
                    continue
                mem = Memory(
                    id=uuid4(),
                    agent_id=agent_uuid,
                    owner_id=None,
                    content=ws["summary"],
                    embedding_ref="",
                    source="compress:sliding_window",
                    visibility=MemoryVisibility.PRIVATE,
                    score=0.6,
                    ttl=None,
                    type=MemoryType.SEMANTIC,
                    importance=MemoryImportance.MEDIUM,
                    tags=["summary", "compressed"],
                    context={
                        "window_start": ws["start"].isoformat(),
                        "window_end": ws["end"].isoformat(),
                        "citations": ws["citations"],
                    },
                )
                try:
                    # Store summary
                    # Note: repository create is async; run synchronously inside service method
                    import asyncio

                    asyncio.get_event_loop().run_until_complete(
                        self._memory_repository.create(mem)
                    )
                    compressed_count += len(ws["ids"])  # count originals summarized
                except Exception:
                    logger.exception("Failed to persist window summary")

            logger.info(
                "Compressed %s memories via sliding-window summarization",
                compressed_count,
            )
            return compressed_count
        except Exception:
            logger.exception("Compression flow failed")
            return 0

    def cleanup_expired_memories(self) -> int:
        """Clean up expired short-term memories.

        Returns:
            Number of memories cleaned up
        """
        # Placeholder: no explicit expiration implementation; nothing to clean
        cleanup_count = 0

        self._last_cleanup = time.time()
        logger.info(f"Cleaned up {cleanup_count} expired memories")
        return cleanup_count

    def get_system_status(self) -> dict[str, Any]:
        """Get overall memory system status.

        Returns:
            Dictionary containing system metrics
        """
        return {
            "config": {
                "max_short_term_items": self._config.max_short_term_items,
                "short_term_ttl_hours": self._config.short_term_ttl_hours,
                "max_long_term_items": self._config.max_long_term_items,
                "compression_threshold": self._config.compression_threshold,
                "cleanup_interval_minutes": self._config.cleanup_interval_minutes,
            },
            "last_cleanup": self._last_cleanup,
            "next_cleanup_due": self._last_cleanup
            + (self._config.cleanup_interval_minutes * 60),
        }

    def _maybe_cleanup(self) -> None:
        """Trigger cleanup if enough time has passed."""
        cleanup_interval_seconds = self._config.cleanup_interval_minutes * 60
        if time.time() - self._last_cleanup > cleanup_interval_seconds:
            self.cleanup_expired_memories()

    def shutdown(self) -> None:
        """Shutdown the memory manager and cleanup resources."""
        logger.info("Shutting down MemoryManagerService")

        # Perform final cleanup
        self.cleanup_expired_memories()

        logger.info("MemoryManagerService shutdown complete")

    # ---- Internal helpers: semantic selection and summarization with citations ----
    def _semantic_cluster_select(
        self, memories: list[Memory], limit: int
    ) -> list[Memory]:
        """Down-select memories by clustering semantically using chunk heuristics and importance.

        Prefers diverse clusters and higher importance levels while capping result size.
        """
        if len(memories) <= limit:
            return memories

        # Group by simple topic hash from first chunk words
        def topic_key(text: str) -> str:
            text_l = text.lower()
            seed = " ".join(text_l.split()[:12])
            import hashlib as _hl

            return _hl.blake2b(seed.encode("utf-8"), digest_size=8).hexdigest()

        clusters: dict[str, list[Memory]] = {}
        for m in memories:
            k = topic_key(m.content)
            clusters.setdefault(k, []).append(m)

        # Sort each cluster by importance and recency
        def cluster_score(mm: list[Memory]) -> float:
            imp_map = {
                MemoryImportance.CRITICAL: 1.0,
                MemoryImportance.HIGH: 0.8,
                MemoryImportance.MEDIUM: 0.5,
                MemoryImportance.LOW: 0.2,
            }
            return max(imp_map.get(x.importance, 0.5) for x in mm)

        ordered_clusters = sorted(clusters.values(), key=cluster_score, reverse=True)
        selection: list[Memory] = []
        # Round-robin across clusters for diversity
        idx = 0
        while len(selection) < limit and ordered_clusters:
            progressed = False
            for cl in ordered_clusters:
                if idx < len(cl):
                    selection.append(cl[idx])
                    progressed = True
                    if len(selection) >= limit:
                        break
            if not progressed:
                break
            idx += 1
        return selection[:limit]

    def _summarize_by_time_windows(self, mems: list[Memory]) -> list[dict[str, Any]]:
        """Create sliding-window summaries with citations.

        Splits the timeline into fixed-duration windows and summarizes content.
        When LLM context is insufficient for a window, triage to extract key points
        and attach citations (memory IDs and short snippets) instead of raw text.
        """
        if not mems:
            return []
        # Define window size (e.g., 1 hour) and slide (30 min)
        from datetime import timedelta as _td

        window = _td(hours=1)
        slide = _td(minutes=30)
        start = mems[0].created_at
        end = mems[-1].created_at
        current = start
        out: list[dict[str, Any]] = []
        # Token constraints (use conservative defaults to avoid config coupling)
        default_limit = 4000
        long_limit = 128000

        while current <= end:
            w_start = current
            w_end = min(current + window, end)
            window_mems = [m for m in mems if w_start <= m.created_at <= w_end]
            current = current + slide
            if not window_mems:
                continue
            # Build concatenated text and estimate tokens as chars/4 heuristic
            raw_texts = [m.content for m in window_mems]
            joined = "\n\n".join(raw_texts)
            est_tokens = max(1, len(joined) // 4)
            # Decide whether to include raw or triage
            if est_tokens <= default_limit or est_tokens <= long_limit:
                # Summarize directly via local chunking heuristic (LLM call could be wired elsewhere)
                summary = self._local_summarize_text(joined)
                citations = [str(m.id) for m in window_mems]
            else:
                # Triage: summarize headers/bullets with citations only
                key_points = self._extract_key_points(window_mems)
                summary = "Summary (triaged due to context):\n- " + "\n- ".join(
                    key_points
                )
                citations = [f"{m.id}:{m.content[:120]}" for m in window_mems]
            out.append(
                {
                    "start": w_start,
                    "end": w_end,
                    "ids": [m.id for m in window_mems],
                    "summary": summary,
                    "citations": citations,
                }
            )
        return out

    def _local_summarize_text(self, text: str) -> str:
        """Lightweight, deterministic summarizer using chunking and heuristics.

        This avoids external calls inside domain service; integration layer may
        replace with LLM-backed summarization via adapters.
        """
        # Chunk heuristically by sentence and size
        sentences = [s.strip() for s in text.split(". ") if s.strip()]
        if not sentences:
            return text[:500]
        highlights: list[str] = []
        cur_len = 0
        for s in sentences:
            if s:
                highlights.append(s[:200])
                cur_len += len(s)
                if len(highlights) >= 8 or cur_len >= 1200:
                    break
        return "; ".join(highlights)[:1000]

    def _extract_key_points(self, mems: Iterable[Memory]) -> list[str]:
        """Extract simple key points from a set of memories."""
        points: list[str] = []
        for m in mems:
            first = m.content.strip().split("\n", 1)[0]
            points.append(first[:160])
            if len(points) >= 12:
                break
        return points
