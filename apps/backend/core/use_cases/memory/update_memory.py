"""Update memory use case.





This module implements memory update functionality following Clean Architecture principles.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.memory import (
import Exception
import RuntimeError
import ValueError
import batch_size
import bool
import context_updates
import days
import dict
import dimension
import e
import field
import float
import i
import importance
import int
import isinstance
import len
import link_id
import linked_memory_id
import list
import memory_repository
import merge
import model
import new_content
import operation
import range
import result
import self
import set
import status
import str
import tag
import tags
import update_data
import updates
import value
import vector
    Memory,
    MemoryEmbedding,
    MemoryImportance,
    MemoryStatus,
    MemoryType,
)

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import MemoryRepository


logger = logging.getLogger(__name__)


class UpdateMemoryUseCase:
    """Use case for updating memories in the system."""

    def __init__(self, memory_repository: MemoryRepository) -> None:
        """Initialize the update memory use case.





        Args:


            memory_repository: Repository for memory operations.


        """

        self.memory_repository = memory_repository

    def _get_current_time(self) -> datetime:
        """Get current UTC time."""

        return datetime.now(UTC)

    async def execute(
        self,
        memory_id: UUID,
        updates: dict[str, Any],
    ) -> Memory | None:
        """Update a memory with new data.





        Args:


            memory_id: ID of the memory to update.


            updates: Dictionary of fields to update.


            validate_permissions: Whether to validate user permissions.





        Returns:


            Updated memory entity or None if not found.





        Raises:


            RuntimeError: If update operation fails.


            ValueError: If invalid update data is provided.


        """

        try:
            logger.info(f"Updating memory {memory_id} with {len(updates)} changes")

            # Get existing memory

            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                logger.warning(f"Memory not found for update: {memory_id}")

                return None

            # Check if memory can be updated

            if memory.status == MemoryStatus.DELETED:
                raise ValueError(f"Cannot update deleted memory: {memory_id}")

            # Apply updates

            updated_memory = self._apply_updates(memory, updates)

            # Save to repository

            _ = await self.memory_repository.update(updated_memory)

            logger.info(f"Successfully updated memory: {memory_id}")

            return result

        except Exception as e:
            logger.error(f"Failed to update memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to update memory: {e!s}") from e

    def _apply_updates(self, memory: Memory, updates: dict[str, Any]) -> Memory:
        """Apply updates to a memory entity.





        Args:


            memory: Memory entity to update.


            updates: Dictionary of field updates.





        Returns:


            Updated memory entity.


        """

        for field, value in updates.items():
            if field == "content" and value != memory.content:
                memory.update_content(str(value))

            elif field == "type" and isinstance(value, (str, MemoryType)):
                memory.type = MemoryType(value) if isinstance(value, str) else value

            elif field == "status" and isinstance(value, (str, MemoryStatus)):
                memory.status = MemoryStatus(value) if isinstance(value, str) else value

            elif field == "importance" and isinstance(value, (str, MemoryImportance)):
                memory.importance = (
                    MemoryImportance(value) if isinstance(value, str) else value
                )

            elif field == "tags" and isinstance(value, list):
                memory.tags = value

            elif field == "summary" and isinstance(value, str):
                memory.summary = value

            elif field == "is_public" and isinstance(value, bool):
                memory.is_public = value

            elif field == "expires_at" and (
                value is None or isinstance(value, datetime)
            ):
                memory.expires_at = value

            elif field == "context" and isinstance(value, dict):
                memory.context.update(value)

            elif field == "linked_memories" and isinstance(value, list):
                memory.linked_memories = value

            elif field == "embedding" and isinstance(value, dict):
                memory.update_embedding(MemoryEmbedding(**value))

        # Update timestamp

        memory.updated_at = self._get_current_time()

        return memory

    async def update_content(self, memory_id: UUID, new_content: str) -> Memory | None:
        """Update only the content of a memory.





        Args:


            memory_id: ID of the memory to update.


            new_content: New content for the memory.





        Returns:


            Updated memory or None if not found.


        """

        return await self.execute(memory_id, {"content": new_content})

    async def update_tags(
        self,
        memory_id: UUID,
        tags: list[str],
        operation: str = "replace",
    ) -> Memory | None:
        """Update tags of a memory.





        Args:


            memory_id: ID of the memory to update.


            tags: List of tags.


            operation: 'replace', 'add', or 'remove'.





        Returns:


            Updated memory or None if not found.


        """

        try:
            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                return None

            if operation == "replace":
                new_tags = tags

            elif operation == "add":
                new_tags = list(set(memory.tags + tags))

            elif operation == "remove":
                new_tags = [tag for tag in memory.tags if tag not in tags]

            else:
                raise ValueError(f"Invalid operation: {operation}")

            return await self.execute(memory_id, {"tags": new_tags})

        except Exception as e:
            logger.error(f"Failed to update tags for memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to update memory tags: {e!s}") from e

    async def update_importance(
        self,
        memory_id: UUID,
        importance: MemoryImportance,
    ) -> Memory | None:
        """Update importance level of a memory.





        Args:


            memory_id: ID of the memory to update.


            importance: New importance level.





        Returns:


            Updated memory or None if not found.


        """

        return await self.execute(memory_id, {"importance": importance})

    async def update_status(
        self,
        memory_id: UUID,
        status: MemoryStatus,
    ) -> Memory | None:
        """Update status of a memory.





        Args:


            memory_id: ID of the memory to update.


            status: New status.





        Returns:


            Updated memory or None if not found.


        """

        return await self.execute(memory_id, {"status": status})

    async def add_link(
        self,
        memory_id: UUID,
        linked_memory_id: UUID,
    ) -> Memory | None:
        """Add a link to another memory.





        Args:


            memory_id: ID of the memory to update.


            linked_memory_id: ID of the memory to link to.





        Returns:


            Updated memory or None if not found.


        """

        try:
            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                return None

            # Check if link already exists

            if linked_memory_id not in memory.linked_memories:
                new_links = memory.linked_memories + [linked_memory_id]

                return await self.execute(memory_id, {"linked_memories": new_links})

            return memory

        except Exception as e:
            logger.error(f"Failed to add link to memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to add memory link: {e!s}") from e

    async def remove_link(
        self,
        memory_id: UUID,
        linked_memory_id: UUID,
    ) -> Memory | None:
        """Remove a link to another memory.





        Args:


            memory_id: ID of the memory to update.


            linked_memory_id: ID of the memory to unlink.





        Returns:


            Updated memory or None if not found.


        """

        try:
            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                return None

            # Remove link if it exists

            if linked_memory_id in memory.linked_memories:
                new_links = [
                    link_id
                    for link_id in memory.linked_memories
                    if link_id != linked_memory_id
                ]

                return await self.execute(memory_id, {"linked_memories": new_links})

            return memory

        except Exception as e:
            logger.error(f"Failed to remove link from memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to remove memory link: {e!s}") from e

    async def update_embedding(
        self,
        memory_id: UUID,
        vector: list[float],
        model: str,
        dimension: int,
    ) -> Memory | None:
        """Update embedding for a memory.





        Args:


            memory_id: ID of the memory to update.


            vector: Embedding vector.


            model: Model used to generate the embedding.


            dimension: Dimension of the embedding vector.





        Returns:


            Updated memory or None if not found.


        """

        embedding_data = {
            "vector": vector,
            "model": model,
            "dimension": dimension,
            "created_at": self._get_current_time(),
        }

        return await self.execute(memory_id, {"embedding": embedding_data})

    async def extend_expiry(
        self,
        memory_id: UUID,
        days: int,
    ) -> Memory | None:
        """Extend the expiry date of a memory.





        Args:


            memory_id: ID of the memory to update.


            days: Number of days to extend by.





        Returns:


            Updated memory or None if not found.


        """

        try:
            memory = await self.memory_repository.get_by_id(memory_id)

            if not memory:
                return None

            # Calculate new expiry date

            current_expiry = memory.expires_at or self._get_current_time()

            new_expiry = current_expiry + timedelta(days=days)

            return await self.execute(memory_id, {"expires_at": new_expiry})

        except Exception as e:
            logger.error(f"Failed to extend expiry for memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to extend memory expiry: {e!s}") from e

    async def update_context(
        self,
        memory_id: UUID,
        context_updates: dict[str, Any],
        merge: bool = True,
    ) -> Memory | None:
        """Update context data of a memory.





        Args:


            memory_id: ID of the memory to update.


            context_updates: Context data to update.


            merge: If True, merge with existing context. If False, replace.





        Returns:


            Updated memory or None if not found.


        """

        try:
            if merge:
                return await self.execute(memory_id, {"context": context_updates})

            else:
                memory = await self.memory_repository.get_by_id(memory_id)

                if not memory:
                    return None

                # Replace entire context

                memory.context = context_updates

                memory.updated_at = self._get_current_time()

                return await self.memory_repository.update(memory)

        except Exception as e:
            logger.error(f"Failed to update context for memory {memory_id}: {e}")

            raise RuntimeError(f"Failed to update memory context: {e!s}") from e

    async def bulk_update(
        self,
        updates: list[dict[str, Any]],
        batch_size: int = 10,
    ) -> dict[str, Any]:
        """Update multiple memories in bulk.





        Args:


            updates: List of update dictionaries, each containing 'memory_id' and update fields.


            batch_size: Number of updates to process in each batch.





        Returns:


            Dictionary with update results.


        """

        try:
            logger.info(f"Starting bulk update of {len(updates)} memories")

            total_updated = 0

            total_errors = 0

            batch_results = []

            # Process in batches

            for i in range(0, len(updates), batch_size):
                batch = updates[i : i + batch_size]

                batch_updated = 0

                batch_errors = 0

                for update_data in batch:
                    try:
                        memory_id = update_data.pop("memory_id")

                        _ = await self.execute(memory_id, update_data)

                        if result:
                            batch_updated += 1

                        else:
                            batch_errors += 1

                    except Exception as e:
                        logger.warning(f"Failed to update memory in bulk: {e}")

                        batch_errors += 1

                total_updated += batch_updated

                total_errors += batch_errors

                batch_results.append(
                    {
                        "batch_number": len(batch_results) + 1,
                        "processed": len(batch),
                        "updated": batch_updated,
                        "errors": batch_errors,
                    }
                )

            results = {
                "success": True,
                "total_processed": len(updates),
                "total_updated": total_updated,
                "total_errors": total_errors,
                "batch_results": batch_results,
            }

            logger.info(
                f"Bulk update completed: {total_updated} updated, {total_errors} errors"
            )

            return results

        except Exception as e:
            logger.error(f"Failed to perform bulk update: {e}")

            raise RuntimeError(f"Failed to perform bulk update: {e!s}") from e
