"""Delete memory use case.





This module implements memory deletion functionality following Clean Architecture principles.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from apps.backend.core.domain.entities.memory import Memory, MemoryStatus, MemoryType
from apps.backend.core.exceptions.business_exceptions import BusinessException
import Exception
import RuntimeError
import TypeError
import ValueError
import any
import batch_size
import bool
import dict
import e
import hard_delete
import i
import importance_below
import importance_threshold
import int
import len
import list
import m
import max
import memory_id
import memory_repository
import min
import older_than_days
import owner_id
import range
import self
import str
import tag
import tags

if TYPE_CHECKING:
    from uuid import UUID

    from apps.backend.core.interfaces.repositories import MemoryRepository


logger = logging.getLogger(__name__)


class DeleteMemoryUseCase:
    """Use case for deleting memories."""

    def __init__(self, memory_repository: MemoryRepository) -> None:
        """Initialize the delete memory use case.





        Args:


            memory_repository: Repository for memory data access.


        """

        self.memory_repository = memory_repository

    async def execute(self, memory_id: UUID, hard_delete: bool = False) -> bool:
        """Delete a memory.





        Args:


            memory_id: Unique identifier of the memory to delete.


            hard_delete: Whether to permanently delete or soft delete.





        Returns:


            True if memory was successfully deleted.





        Raises:


            ValueError: If memory is not found.


            RuntimeError: If deletion operation fails.


        """

        # Get the memory

        memory = await self.memory_repository.get_by_id(memory_id)

        if not memory:
            raise ValueError(f"Memory with ID {memory_id} not found")

        try:
            if hard_delete:
                # Permanent deletion

                deleted = await self.memory_repository.delete(memory_id)

                return deleted

            else:
                # Soft deletion - mark as deleted

                memory.status = MemoryStatus.DELETED

                memory.context["deleted_at"] = self._get_current_time().isoformat()

                memory.context["deletion_type"] = "soft"

                updated_memory = await self.memory_repository.update(memory)

                return updated_memory is not None

        except Exception as e:
            raise RuntimeError(f"Failed to delete memory: {e!s}") from e

    async def delete_by_criteria(
        self,
        owner_id: UUID | None = None,
        memory_type: str | None = None,
        older_than_days: int | None = None,
        importance_below: str | None = None,
        hard_delete: bool = False,
    ) -> dict[str, Any]:
        """Delete memories based on criteria.





        Args:


            owner_id: Delete memories belonging to this owner.


            memory_type: Delete memories of this type.


            older_than_days: Delete memories older than this many days.


            importance_below: Delete memories with importance below this level.


            hard_delete: Whether to permanently delete or soft delete.





        Returns:


            Dictionary with deletion statistics.


        """

        filters = {}

        if owner_id:
            filters["owner_id"] = owner_id

        if memory_type:
            filters["type"] = memory_type

        try:
            # Get memories matching criteria - use appropriate repository methods

            if owner_id and memory_type:
                # Filter by both user and type

                user_memories = await self.memory_repository.list_by_user(owner_id)

                memories = [m for m in user_memories if m.type == memory_type]

            elif owner_id:
                memories = await self.memory_repository.list_by_user(owner_id)

            elif memory_type:
                memories = await self.memory_repository.list_by_type(memory_type)

            else:
                # Need to get memories by agent or raise an error

                raise ValueError(
                    "Must specify at least owner_id or memory_type for deletion criteria"
                )

            # Apply additional filters

            memories_to_delete = []

            current_time = self._get_current_time()

            for memory in memories:
                # Skip already deleted memories

                if memory.status == MemoryStatus.DELETED:
                    continue

                should_delete = True

                # Check age filter

                if older_than_days:
                    age_days = (current_time - memory.created_at).days

                    if age_days < older_than_days:
                        should_delete = False

                # Check importance filter

                if importance_below and should_delete:
                    importance_order = ["low", "medium", "high", "critical"]

                    if (
                        memory.importance.value in importance_order
                        and importance_below in importance_order
                    ):
                        memory_importance_index = importance_order.index(
                            memory.importance.value
                        )

                        threshold_index = importance_order.index(importance_below)

                        if memory_importance_index >= threshold_index:
                            should_delete = False

                if should_delete:
                    memories_to_delete.append(memory)

            # Perform deletions

            results = {
                "total_found": len(memories),
                "total_deleted": 0,
                "total_failed": 0,
                "deleted_ids": [],
                "errors": [],
            }

            for memory in memories_to_delete:
                try:
                    success = await self.execute(memory.id, hard_delete=hard_delete)

                    if success:
                        results["total_deleted"] += 1

                        results["deleted_ids"].append(str(memory.id))

                    else:
                        results["total_failed"] += 1

                        results["errors"].append(f"Failed to delete memory {memory.id}")

                except Exception as e:
                    results["total_failed"] += 1

                    results["errors"].append(
                        f"Error deleting memory {memory.id}: {e!s}"
                    )

            return results

        except Exception as e:
            raise BusinessException(
                "Failed to delete memories by criteria",
                error_code="MEMORY_BULK_DELETE_FAILED",
            ) from e

    async def restore_memory(self, memory_id: UUID) -> bool:
        """Restore a soft-deleted memory.





        Args:


            memory_id: Unique identifier of the memory to restore.





        Returns:


            True if memory was successfully restored.





        Raises:


            ValueError: If memory is not found or not soft-deleted.


            RuntimeError: If restoration operation fails.


        """

        # Get the memory

        memory = await self.memory_repository.get_by_id(memory_id)

        if not memory:
            raise ValueError(f"Memory with ID {memory_id} not found")

        if memory.status != MemoryStatus.DELETED:
            raise ValueError("Memory is not in deleted status")

        try:
            # Restore the memory

            memory.status = MemoryStatus.ACTIVE

            memory.context.pop("deleted_at", None)

            memory.context.pop("deletion_type", None)

            memory.context["restored_at"] = self._get_current_time().isoformat()

            updated_memory = await self.memory_repository.update(memory)

            return updated_memory is not None

        except Exception as e:
            raise RuntimeError(f"Failed to restore memory: {e!s}") from e

    async def purge_deleted_memories(self, older_than_days: int = 30) -> dict[str, Any]:
        """Permanently delete soft-deleted memories older than specified days.





        Args:


            older_than_days: Delete memories that were soft-deleted more than this many days ago.





        Returns:


            Dictionary with purge statistics.


        """

        try:
            # Get all memories to check for soft-deleted ones

            # Since we don't have a direct status filter, we need to get all memories

            # For this demo, we'll assume we have an agent_id context available

            all_memories = await self.memory_repository.list_by_user(
                user_id=UUID("00000000-0000-0000-0000-000000000000"),  # Placeholder
                limit=10000,  # Large limit for checking all memories
            )

            deleted_memories = [
                m for m in all_memories if m.status == MemoryStatus.DELETED
            ]

            current_time = self._get_current_time()

            memories_to_purge = []

            for memory in deleted_memories:
                deleted_at_str = memory.context.get("deleted_at")

                if deleted_at_str:
                    try:
                        deleted_at = datetime.fromisoformat(
                            deleted_at_str.replace("Z", "+00:00")
                        )

                        days_since_deletion = (current_time - deleted_at).days

                        if days_since_deletion >= older_than_days:
                            memories_to_purge.append(memory)

                    except (ValueError, TypeError):
                        # If we can't parse the deletion date, include it for purging

                        memories_to_purge.append(memory)

            # Perform permanent deletions

            results = {
                "total_deleted_memories": len(deleted_memories),
                "total_purged": 0,
                "total_failed": 0,
                "purged_ids": [],
                "errors": [],
            }

            for memory in memories_to_purge:
                try:
                    success = await self.memory_repository.delete(memory.id)

                    if success:
                        results["total_purged"] += 1

                        results["purged_ids"].append(str(memory.id))

                    else:
                        results["total_failed"] += 1

                        results["errors"].append(f"Failed to purge memory {memory.id}")

                except Exception as e:
                    results["total_failed"] += 1

                    results["errors"].append(f"Error purging memory {memory.id}: {e!s}")

            return results

        except Exception as e:
            raise RuntimeError(f"Failed to purge deleted memories: {e!s}") from e

    async def get_deletion_stats(self, owner_id: UUID | None = None) -> dict[str, Any]:
        """Get statistics about deleted memories.





        Args:


            owner_id: Optional owner ID to filter by.





        Returns:


            Dictionary with deletion statistics.


        """

        try:
            # Get deleted memories by filtering from all memories

            if owner_id:
                all_memories = await self.memory_repository.list_by_user(owner_id)

            else:
                # Get expired memories as a proxy for getting all memories

                all_memories = await self.memory_repository.list_expired(limit=10000)

            deleted_memories = [
                m for m in all_memories if m.status == MemoryStatus.DELETED
            ]

            stats = {
                "total_deleted": len(deleted_memories),
                "by_type": {},
                "by_importance": {},
                "oldest_deletion": None,
                "newest_deletion": None,
                "total_size_bytes": 0,
            }

            if not deleted_memories:
                return stats

            deletion_dates = []

            for memory in deleted_memories:
                # Count by type

                memory_type = memory.type.value

                stats["by_type"][memory_type] = stats["by_type"].get(memory_type, 0) + 1

                # Count by importance

                importance = memory.importance.value

                stats["by_importance"][importance] = (
                    stats["by_importance"].get(importance, 0) + 1
                )

                # Track deletion dates

                deleted_at_str = memory.context.get("deleted_at")

                if deleted_at_str:
                    try:
                        deleted_at = datetime.fromisoformat(
                            deleted_at_str.replace("Z", "+00:00")
                        )

                        deletion_dates.append(deleted_at)

                    except (ValueError, TypeError):
                        pass

                # Calculate total size

                # Calculate size if available in context

                size_bytes = memory.context.get("size_bytes", 0)

                if size_bytes:
                    stats["total_size_bytes"] += size_bytes

            if deletion_dates:
                stats["oldest_deletion"] = min(deletion_dates).isoformat()

                stats["newest_deletion"] = max(deletion_dates).isoformat()

            return stats

        except Exception as e:
            raise RuntimeError(f"Failed to get deletion stats: {e!s}") from e

    async def _get_memories_by_criteria(
        self, owner_id: UUID | None, memory_type: str | None
    ) -> list[Memory]:
        """Get memories matching the basic criteria."""

        if owner_id and memory_type:
            # Filter by both user and type

            user_memories = await self.memory_repository.list_by_user(owner_id)

            return [m for m in user_memories if m.type.value == memory_type]

        elif owner_id:
            return await self.memory_repository.list_by_user(owner_id)

        elif memory_type:
            # Convert string to MemoryType enum

            try:
                memory_type_enum = MemoryType(memory_type)

                return await self.memory_repository.list_by_type(memory_type_enum)

            except ValueError:
                return []

        else:
            raise ValueError(
                "Must specify at least owner_id or memory_type for deletion criteria"
            )

    def _filter_memories_for_deletion(
        self,
        memories: list[Memory],
        older_than_days: int | None,
        importance_threshold: str | None,
        tags: list[str] | None,
    ) -> list[Memory]:
        """Filter memories based on additional criteria."""

        memories_to_delete = []

        current_time = self._get_current_time()

        for memory in memories:
            # Skip already deleted memories

            if memory.status == MemoryStatus.DELETED:
                continue

            # Apply age filter

            if older_than_days:
                age_days = (current_time - memory.created_at).days

                if age_days < older_than_days:
                    continue

            # Apply importance filter

            if importance_threshold:
                importance_levels = ["low", "medium", "high", "critical"]

                min_level_index = importance_levels.index(importance_threshold.lower())

                memory_level_index = importance_levels.index(
                    memory.importance.value.lower()
                )

                if memory_level_index > min_level_index:
                    continue  # Memory is more important than threshold

            # Apply tags filter

            if tags and not any(tag in memory.tags for tag in tags):
                continue

            memories_to_delete.append(memory)

        return memories_to_delete

    async def _delete_memories_in_batches(
        self, memories_to_delete: list[Memory], batch_size: int
    ) -> dict[str, Any]:
        """Delete memories in batches and return results."""

        total_deleted = 0

        total_errors = 0

        batch_results = []

        for i in range(0, len(memories_to_delete), batch_size):
            batch = memories_to_delete[i : i + batch_size]

            batch_deleted = 0

            batch_errors = 0

            for memory in batch:
                try:
                    success = await self.execute(memory.id)

                    if success:
                        batch_deleted += 1

                    else:
                        batch_errors += 1

                except Exception as e:
                    logger.warning(f"Failed to delete memory {memory.id}: {e}")

                    batch_errors += 1

            total_deleted += batch_deleted

            total_errors += batch_errors

            batch_results.append(
                {
                    "batch_number": len(batch_results) + 1,
                    "processed": len(batch),
                    "deleted": batch_deleted,
                    "errors": batch_errors,
                }
            )

        return {
            "success": True,
            "total_processed": len(memories_to_delete),
            "total_deleted": total_deleted,
            "total_errors": total_errors,
            "batch_results": batch_results,
        }

    def _get_current_time(self):
        """Get current UTC time."""

        return datetime.now(UTC)
