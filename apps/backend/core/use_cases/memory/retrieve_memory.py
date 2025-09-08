"""Retrieve memory use case.





This module implements memory retrieval functionality following Clean Architecture principles.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.memory import (
import Exception
import RuntimeError
import agent_id
import all
import bool
import days
import dict
import e
import importance
import int
import len
import limit
import list
import m
import match_all
import memory_id
import memory_repository
import memory_type
import offset
import result
import self
import status
import str
import tag
import tags
import user_id
    Memory,
    MemoryImportance,
    MemoryStatus,
    MemoryType,
)

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import MemoryRepository


logger = logging.getLogger(__name__)


class RetrieveMemoryUseCase:
    """Use case for retrieving memories from the system."""

    def __init__(self, memory_repository: MemoryRepository) -> None:
        """Initialize the retrieve memory use case.





        Args:


            memory_repository: Repository for memory operations.


        """

        self.memory_repository = memory_repository

    def _get_current_time(self) -> datetime:
        """Get current UTC time."""

        return datetime.now(UTC)

    async def execute(self, memory_id: UUID) -> Memory | None:
        """Retrieve a memory by its ID.





        Args:


            memory_id: Unique identifier of the memory to retrieve.





        Returns:


            Memory entity if found and accessible, None otherwise.





        Raises:


            RuntimeError: If retrieval operation fails.


        """

        try:
            logger.info(f"Retrieving memory with ID: {memory_id}")

            # Get memory from repository

            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                logger.warning(f"Memory not found: {memory_id}")

                return None

            # Check if memory is accessible (not deleted)

            if memory.status == MemoryStatus.DELETED:
                logger.warning(f"Attempted to retrieve deleted memory: {memory_id}")

                return None

            # Update access metrics

            memory.access()

            # Update memory in repository to save access metrics

            await self.memory_repository.update(memory)

            logger.info(f"Successfully retrieved memory: {memory_id}")

            return memory

        except Exception as e:
            logger.error(f"Failed to retrieve memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to retrieve memory: {e!s}") from e

    async def get_by_agent(
        self,
        agent_id: UUID,
        limit: int = 50,
        offset: int = 0,
        status: MemoryStatus | None = None,
    ) -> list[Memory]:
        """Retrieve memories associated with a specific agent.





        Args:


            agent_id: Agent's unique identifier.


            limit: Maximum number of memories to retrieve.


            offset: Number of memories to skip for pagination.


            status: Optional status filter.





        Returns:


            List of memories associated with the agent.


        """

        try:
            logger.info(
                f"Retrieving memories for agent {agent_id} (limit={limit}, offset={offset})"
            )

            # Get memories from repository

            memories = await self.memory_repository.list_by_agent(
                agent_id=agent_id, limit=limit, offset=offset
            )

            # Apply status filter if specified

            if status:
                memories = [m for m in memories if m.status == status]

            logger.info(f"Retrieved {len(memories)} memories for agent {agent_id}")

            return memories

        except Exception as e:
            logger.error(f"Failed to retrieve memories for agent {agent_id}: {e}")

            raise RuntimeError(f"Failed to retrieve agent memories: {e!s}") from e

    async def get_by_user(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
        memory_type: MemoryType | None = None,
    ) -> list[Memory]:
        """Retrieve memories associated with a specific user.





        Args:


            user_id: User's unique identifier.


            limit: Maximum number of memories to retrieve.


            offset: Number of memories to skip for pagination.


            memory_type: Optional memory type filter.





        Returns:


            List of memories associated with the user.


        """

        try:
            logger.info(
                f"Retrieving memories for user {user_id} (limit={limit}, offset={offset})"
            )

            # Get memories from repository

            memories = await self.memory_repository.list_by_user(
                user_id=user_id, limit=limit, offset=offset
            )

            # Apply type filter if specified

            if memory_type:
                memories = [m for m in memories if m.type == memory_type]

            logger.info(f"Retrieved {len(memories)} memories for user {user_id}")

            return memories

        except Exception as e:
            logger.error(f"Failed to retrieve memories for user {user_id}: {e}")

            raise RuntimeError(f"Failed to retrieve user memories: {e!s}") from e

    async def get_by_type(
        self,
        memory_type: MemoryType,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Memory]:
        """Retrieve memories of a specific type.





        Args:


            memory_type: Type of memories to retrieve.


            limit: Maximum number of memories to retrieve.


            offset: Number of memories to skip for pagination.





        Returns:


            List of memories of the specified type.


        """

        try:
            logger.info(
                f"Retrieving memories of type {memory_type.value} (limit={limit}, offset={offset})"
            )

            # Get memories from repository

            memories = await self.memory_repository.list_by_type(
                memory_type=memory_type, limit=limit, offset=offset
            )

            logger.info(
                f"Retrieved {len(memories)} memories of type {memory_type.value}"
            )

            return memories

        except Exception as e:
            logger.error(
                f"Failed to retrieve memories of type {memory_type.value}: {e}"
            )

            raise RuntimeError(f"Failed to retrieve memories by type: {e!s}") from e

    async def get_by_importance(
        self,
        importance: MemoryImportance,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Memory]:
        """Retrieve memories of a specific importance level.





        Args:


            importance: Importance level of memories to retrieve.


            limit: Maximum number of memories to retrieve.


            offset: Number of memories to skip for pagination.





        Returns:


            List of memories of the specified importance level.


        """

        try:
            logger.info(
                f"Retrieving memories of importance {importance.value} (limit={limit}, offset={offset})"
            )

            # Get memories from repository

            memories = await self.memory_repository.list_by_importance(
                importance=importance, limit=limit, offset=offset
            )

            logger.info(
                f"Retrieved {len(memories)} memories of importance {importance.value}"
            )

            return memories

        except Exception as e:
            logger.error(
                f"Failed to retrieve memories of importance {importance.value}: {e}"
            )

            raise RuntimeError(
                f"Failed to retrieve memories by importance: {e!s}"
            ) from e

    async def get_by_tags(
        self,
        tags: list[str],
        limit: int = 50,
        offset: int = 0,
        match_all: bool = False,
    ) -> list[Memory]:
        """Retrieve memories that have specific tags.





        Args:


            tags: List of tags to search for.


            limit: Maximum number of memories to retrieve.


            offset: Number of memories to skip for pagination.


            match_all: If True, memory must have all tags. If False, any tag.





        Returns:


            List of memories matching the tag criteria.


        """

        try:
            logger.info(f"Retrieving memories with tags {tags} (match_all={match_all})")

            # Get memories from repository

            memories = await self.memory_repository.list_by_tags(
                tags=tags, limit=limit, offset=offset
            )

            # Apply additional filtering based on match_all parameter

            if match_all:
                # Memory must have all specified tags

                memories = [m for m in memories if all(tag in m.tags for tag in tags)]

            logger.info(f"Retrieved {len(memories)} memories matching tag criteria")

            return memories

        except Exception as e:
            logger.error(f"Failed to retrieve memories by tags {tags}: {e}")

            raise RuntimeError(f"Failed to retrieve memories by tags: {e!s}") from e

    async def get_linked_memories(self, memory_id: UUID) -> list[Memory]:
        """Retrieve memories linked to a specific memory.





        Args:


            memory_id: ID of the memory to find links for.





        Returns:


            List of memories linked to the specified memory.


        """

        try:
            logger.info(f"Retrieving memories linked to {memory_id}")

            # Get linked memories from repository

            linked_memories = await self.memory_repository.list_linked(memory_id)

            logger.info(f"Retrieved {len(linked_memories)} linked memories")

            return linked_memories

        except Exception as e:
            logger.error(f"Failed to retrieve linked memories for {memory_id}: {e}")

            raise RuntimeError(f"Failed to retrieve linked memories: {e!s}") from e

    async def get_recent_memories(
        self,
        days: int = 7,
        limit: int = 20,
        memory_type: MemoryType | None = None,
        user_id: UUID | None = None,
    ) -> list[Memory]:
        """Retrieve recent memories within a specified time period.





        Args:


            days: Number of days to look back.


            limit: Maximum number of memories to retrieve.


            memory_type: Optional memory type filter.


            user_id: Optional user ID filter.





        Returns:


            List of recent memories sorted by creation time (newest first).


        """

        try:
            logger.info(f"Retrieving memories from last {days} days")

            # Calculate cutoff date

            cutoff_date = self._get_current_time() - timedelta(days=days)

            # Get memories based on user filter

            if user_id:
                memories = await self.memory_repository.list_by_user(
                    user_id=user_id,
                    limit=limit * 2,  # Get more to allow for filtering
                )

            else:
                # Get memories by type or general expired list as fallback

                if memory_type:
                    memories = await self.memory_repository.list_by_type(
                        memory_type=memory_type, limit=limit * 2
                    )

                else:
                    memories = await self.memory_repository.list_expired(
                        limit=limit * 2
                    )

            # Filter by date and type

            recent_memories = []

            for memory in memories:
                if memory.created_at >= cutoff_date:
                    if memory_type is None or memory.type == memory_type:
                        recent_memories.append(memory)

            # Sort by creation time (newest first) and limit results

            recent_memories.sort(key=lambda m: m.created_at, reverse=True)

            _ = recent_memories[:limit]

            logger.info(f"Retrieved {len(result)} recent memories")

            return result

        except Exception as e:
            logger.error(f"Failed to retrieve recent memories: {e}")

            raise RuntimeError(f"Failed to retrieve recent memories: {e!s}") from e

    async def get_memory_summary(self, memory_id: UUID) -> dict[str, Any] | None:
        """Get a summary of memory information including metadata.





        Args:


            memory_id: ID of the memory to summarize.





        Returns:


            Dictionary with memory summary or None if not found.


        """

        try:
            memory = await self.execute(memory_id)

            if not memory:
                return None

            return {
                "id": str(memory.id),
                "type": memory.type.value,
                "status": memory.status.value,
                "importance": memory.importance.value,
                "summary": memory.summary,
                "tags": memory.tags,
                "created_at": memory.created_at.isoformat(),
                "updated_at": memory.updated_at.isoformat(),
                "access_count": memory.metrics.access_count,
                "last_accessed": memory.metrics.last_accessed.isoformat()
                if memory.metrics.last_accessed
                else None,
                "content_length": len(memory.content),
                "linked_count": len(memory.linked_memories),
                "is_public": memory.is_public,
                "expires_at": memory.expires_at.isoformat()
                if memory.expires_at
                else None,
            }

        except Exception as e:
            logger.error(f"Failed to get memory summary for {memory_id}: {e}")

            raise RuntimeError(f"Failed to get memory summary: {e!s}") from e
