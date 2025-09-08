"""Search memory use case.





This module implements memory search functionality following Clean Architecture principles.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.memory import (
import Exception
import RuntimeError
import any
import content_query
import date_from
import date_to
import dict
import e
import end_date
import float
import importance
import int
import len
import limit
import list
import m
import max
import memory
import memory_id
import memory_repository
import memory_type
import offset
import query
import round
import self
import start_date
import str
import sum
import tag
import tags
import user_id
import vector
    Memory,
    MemoryImportance,
    MemoryStatus,
    MemoryType,
)

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import MemoryRepository


logger = logging.getLogger(__name__)


class SearchMemoryUseCase:
    """Use case for searching memories in the system."""

    def __init__(self, memory_repository: MemoryRepository) -> None:
        """Initialize the search memory use case.





        Args:


            memory_repository: Repository for memory operations.


        """

        self.memory_repository = memory_repository

    def _get_current_time(self) -> datetime:
        """Get current UTC time."""

        return datetime.now(UTC)

    async def search_by_content(
        self,
        query: str,
        limit: int = 20,
        user_id: UUID | None = None,
        memory_type: MemoryType | None = None,
        importance: MemoryImportance | None = None,
    ) -> list[Memory]:
        """Search memories by content text.





        Args:


            query: Search query string.


            limit: Maximum number of results to return.


            user_id: Optional user ID to filter results.


            memory_type: Optional memory type filter.


            importance: Optional importance level filter.





        Returns:


            List of memories matching the search criteria.





        Raises:


            RuntimeError: If search operation fails.


        """

        try:
            logger.info(f"Searching memories by content: '{query}' (limit={limit})")

            # Validate query

            if not query.strip():
                logger.warning("Empty search query provided")

                return []

            # Search using repository

            memories = await self.memory_repository.search_by_content(
                query=query.strip(),
                limit=limit * 2,  # Get more results for filtering
            )

            # Apply additional filters

            filtered_memories = []

            for memory in memories:
                # Skip deleted memories

                if memory.status == MemoryStatus.DELETED:
                    continue

                # Apply user filter

                if user_id and memory.user_id != user_id:
                    continue

                # Apply type filter

                if memory_type and memory.type != memory_type:
                    continue

                # Apply importance filter

                if importance and memory.importance != importance:
                    continue

                filtered_memories.append(memory)

                # Stop when we have enough results

                if len(filtered_memories) >= limit:
                    break

            logger.info(
                f"Found {len(filtered_memories)} memories matching content search"
            )

            return filtered_memories

        except Exception as e:
            logger.error(f"Failed to search memories by content '{query}': {e}")

            raise RuntimeError(f"Failed to search memories by content: {e!s}") from e

    async def search_by_vector(
        self,
        vector: list[float],
        threshold: float = 0.8,
        limit: int = 20,
        user_id: UUID | None = None,
        memory_type: MemoryType | None = None,
    ) -> list[Memory]:
        """Search memories by vector similarity.





        Args:


            vector: Query vector for similarity search.


            threshold: Minimum similarity threshold (0.0 to 1.0).


            limit: Maximum number of results to return.


            user_id: Optional user ID to filter results.


            memory_type: Optional memory type filter.





        Returns:


            List of memories similar to the query vector.





        Raises:


            RuntimeError: If vector search operation fails.


        """

        try:
            logger.info(
                f"Searching memories by vector similarity (threshold={threshold}, limit={limit})"
            )

            # Validate input

            if not vector:
                logger.warning("Empty vector provided for search")

                return []

            if not 0.0 <= threshold <= 1.0:
                logger.warning(f"Invalid threshold {threshold}, using 0.8")

                threshold = 0.8

            # Search using repository

            memories = await self.memory_repository.search_by_vector(
                vector=vector,
                threshold=threshold,
                limit=limit * 2,  # Get more results for filtering
            )

            # Apply additional filters

            filtered_memories = []

            for memory in memories:
                # Skip deleted memories

                if memory.status == MemoryStatus.DELETED:
                    continue

                # Skip memories without embeddings

                if not memory.embedding:
                    continue

                # Apply user filter

                if user_id and memory.user_id != user_id:
                    continue

                # Apply type filter

                if memory_type and memory.type != memory_type:
                    continue

                filtered_memories.append(memory)

                # Stop when we have enough results

                if len(filtered_memories) >= limit:
                    break

            logger.info(
                f"Found {len(filtered_memories)} memories matching vector search"
            )

            return filtered_memories

        except Exception as e:
            logger.error(f"Failed to search memories by vector: {e}")

            raise RuntimeError(f"Failed to search memories by vector: {e!s}") from e

    async def search_advanced(
        self,
        content_query: str | None = None,
        tags: list[str] | None = None,
        memory_type: MemoryType | None = None,
        importance: MemoryImportance | None = None,
        user_id: UUID | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Perform advanced search with multiple criteria.





        Args:


            content_query: Text content to search for.


            tags: List of tags to filter by.


            memory_type: Memory type filter.


            importance: Importance level filter.


            user_id: User ID filter.


            date_from: Start date for filtering.


            date_to: End date for filtering.


            limit: Maximum number of results.


            offset: Number of results to skip.





        Returns:


            Dictionary containing search results and metadata.


        """

        try:
            logger.info("Performing advanced search with multiple criteria")

            # Start with all memories from a source

            if user_id:
                candidate_memories = await self.memory_repository.list_by_user(
                    user_id=user_id,
                    limit=1000,  # Large initial set for filtering
                )

            elif memory_type:
                candidate_memories = await self.memory_repository.list_by_type(
                    memory_type=memory_type, limit=1000
                )

            elif tags:
                candidate_memories = await self.memory_repository.list_by_tags(
                    tags=tags, limit=1000
                )

            else:
                # Use content search as primary filter if available

                if content_query:
                    candidate_memories = await self.memory_repository.search_by_content(
                        query=content_query, limit=1000
                    )

                else:
                    # Fallback to expired memories list

                    candidate_memories = await self.memory_repository.list_expired(
                        limit=1000
                    )

            # Apply all filters

            filtered_memories = self._apply_advanced_filters(
                memories=candidate_memories,
                content_query=content_query,
                tags=tags,
                memory_type=memory_type,
                importance=importance,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
            )

            # Sort by relevance (access count and last accessed)

            filtered_memories.sort(
                key=lambda m: (
                    m.metrics.access_count,
                    m.metrics.last_accessed or datetime.min.replace(tzinfo=UTC),
                ),
                reverse=True,
            )

            # Apply pagination

            total_count = len(filtered_memories)

            paginated_memories = filtered_memories[offset : offset + limit]

            # Prepare results

            results = {
                "memories": paginated_memories,
                "total_count": total_count,
                "offset": offset,
                "limit": limit,
                "has_more": offset + limit < total_count,
                "search_criteria": {
                    "content_query": content_query,
                    "tags": tags,
                    "memory_type": memory_type.value if memory_type else None,
                    "importance": importance.value if importance else None,
                    "user_id": str(user_id) if user_id else None,
                    "date_from": date_from.isoformat() if date_from else None,
                    "date_to": date_to.isoformat() if date_to else None,
                },
                "statistics": self._calculate_search_statistics(paginated_memories),
            }

            logger.info(
                f"Advanced search returned {len(paginated_memories)} of {total_count} results"
            )

            return results

        except Exception as e:
            logger.error(f"Failed to perform advanced search: {e}")

            raise RuntimeError(f"Failed to perform advanced search: {e!s}") from e

    def _apply_advanced_filters(
        self,
        memories: list[Memory],
        content_query: str | None,
        tags: list[str] | None,
        memory_type: MemoryType | None,
        importance: MemoryImportance | None,
        user_id: UUID | None,
        date_from: datetime | None,
        date_to: datetime | None,
    ) -> list[Memory]:
        """Apply advanced filters to a list of memories."""

        filtered_memories = []

        for memory in memories:
            # Skip deleted memories

            if memory.status == MemoryStatus.DELETED:
                continue

            # Content query filter (case-insensitive)

            if content_query:
                query_lower = content_query.lower()

                if (
                    query_lower not in memory.content.lower()
                    and query_lower not in memory.summary.lower()
                ):
                    continue

            # Tags filter (must have at least one matching tag)

            if tags and not any(tag in memory.tags for tag in tags):
                continue

            # Type filter

            if memory_type and memory.type != memory_type:
                continue

            # Importance filter

            if importance and memory.importance != importance:
                continue

            # User filter

            if user_id and memory.user_id != user_id:
                continue

            # Date range filters

            if date_from and memory.created_at < date_from:
                continue

            if date_to and memory.created_at > date_to:
                continue

            filtered_memories.append(memory)

        return filtered_memories

    def _calculate_search_statistics(self, memories: list[Memory]) -> dict[str, Any]:
        """Calculate statistics for search results."""

        if not memories:
            return {
                "total_memories": 0,
                "by_type": {},
                "by_importance": {},
                "by_status": {},
                "average_access_count": 0,
                "most_accessed": None,
            }

        # Count by type

        type_counts = {}

        for memory in memories:
            type_name = memory.type.value

            type_counts[type_name] = type_counts.get(type_name, 0) + 1

        # Count by importance

        importance_counts = {}

        for memory in memories:
            importance_name = memory.importance.value

            importance_counts[importance_name] = (
                importance_counts.get(importance_name, 0) + 1
            )

        # Count by status

        status_counts = {}

        for memory in memories:
            status_name = memory.status.value

            status_counts[status_name] = status_counts.get(status_name, 0) + 1

        # Calculate access statistics

        access_counts = [memory.metrics.access_count for memory in memories]

        average_access = sum(access_counts) / len(access_counts) if access_counts else 0

        # Find most accessed memory

        most_accessed = max(
            memories, key=lambda m: m.metrics.access_count, default=None
        )

        return {
            "total_memories": len(memories),
            "by_type": type_counts,
            "by_importance": importance_counts,
            "by_status": status_counts,
            "average_access_count": round(average_access, 2),
            "most_accessed": {
                "id": str(most_accessed.id),
                "summary": most_accessed.summary,
                "access_count": most_accessed.metrics.access_count,
            }
            if most_accessed
            else None,
        }

    async def search_similar(
        self,
        memory_id: UUID,
        limit: int = 10,
        threshold: float = 0.7,
    ) -> list[Memory]:
        """Find memories similar to a given memory.





        Args:


            memory_id: ID of the reference memory.


            limit: Maximum number of similar memories to return.


            threshold: Similarity threshold.





        Returns:


            List of similar memories.


        """

        try:
            logger.info(f"Searching for memories similar to {memory_id}")

            # Get the reference memory

            reference_memory = await self.memory_repository.get_by_id(memory_id)

            if not reference_memory:
                logger.warning(f"Reference memory not found: {memory_id}")

                return []

            if not reference_memory.embedding:
                logger.warning(f"Reference memory has no embedding: {memory_id}")

                return []

            # Search by vector similarity

            similar_memories = await self.search_by_vector(
                vector=reference_memory.embedding.vector,
                threshold=threshold,
                limit=limit + 1,  # +1 to account for the reference memory itself
            )

            # Remove the reference memory from results

            similar_memories = [m for m in similar_memories if m.id != memory_id]

            # Limit to requested number

            similar_memories = similar_memories[:limit]

            logger.info(f"Found {len(similar_memories)} similar memories")

            return similar_memories

        except Exception as e:
            logger.error(f"Failed to search for similar memories to {memory_id}: {e}")

            raise RuntimeError(f"Failed to search for similar memories: {e!s}") from e

    async def search_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        memory_type: MemoryType | None = None,
        limit: int = 100,
    ) -> list[Memory]:
        """Search memories within a specific date range.





        Args:


            start_date: Start of the date range.


            end_date: End of the date range.


            memory_type: Optional memory type filter.


            limit: Maximum number of results.





        Returns:


            List of memories within the date range.


        """

        try:
            logger.info(f"Searching memories from {start_date} to {end_date}")

            # Validate date range

            if start_date >= end_date:
                logger.warning("Invalid date range: start_date >= end_date")

                return []

            # Get candidate memories

            if memory_type:
                candidate_memories = await self.memory_repository.list_by_type(
                    memory_type=memory_type, limit=limit * 2
                )

            else:
                candidate_memories = await self.memory_repository.list_expired(
                    limit=limit * 2
                )

            # Filter by date range

            filtered_memories = []

            for memory in candidate_memories:
                if memory.status == MemoryStatus.DELETED:
                    continue

                if start_date <= memory.created_at <= end_date:
                    filtered_memories.append(memory)

                    if len(filtered_memories) >= limit:
                        break

            # Sort by creation date (newest first)

            filtered_memories.sort(key=lambda m: m.created_at, reverse=True)

            logger.info(f"Found {len(filtered_memories)} memories in date range")

            return filtered_memories

        except Exception as e:
            logger.error(f"Failed to search memories by date range: {e}")

            raise RuntimeError(f"Failed to search memories by date range: {e!s}") from e
