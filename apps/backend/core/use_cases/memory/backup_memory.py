"""Backup memory use case for creating and restoring memory backups."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)


class BackupMemoryUseCase:
    """Use case for backing up and restoring memory data."""
import Exception
import RuntimeError
import ValueError
import b
import base_backup_id
import bool
import compress
import compression_service
import dict
import e
import hasattr
import include_metadata
import len
import max
import memory
import memory_repository
import overwrite_existing
import r
import record
import self
import storage_result
import storage_service
import str
import sum
import target_user_id
import user_id
import x

    def __init__(
        self,
        memory_repository: Any,
        storage_service: Any,
        compression_service: Any | None = None,
    ):
        """Initialize the backup memory use case.





        Args:


            memory_repository: Repository for memory operations


            storage_service: Service for file storage operations


            compression_service: Optional service for data compression


        """

        self.memory_repository = memory_repository

        self.storage_service = storage_service

        self.compression_service = compression_service

    async def create_full_backup(
        self,
        user_id: str | None = None,
        include_metadata: bool = True,
        compress: bool = True,
    ) -> dict[str, Any]:
        """Create a full backup of all memory data.





        Args:


            user_id: Optional user ID to filter memories


            include_metadata: Whether to include memory metadata


            compress: Whether to compress the backup





        Returns:


            Dict containing backup information





        Raises:


            RuntimeError: If backup creation fails


        """

        try:
            timestamp = datetime.now(UTC).isoformat()

            backup_id = f"full_backup_{timestamp.replace(':', '-').replace('.', '-')}"

            if user_id:
                backup_id = f"user_{user_id}_{backup_id}"

            # Retrieve all memories

            if user_id:
                memories = await self.memory_repository.get_memories_by_user(user_id)

            else:
                memories = await self.memory_repository.get_all_memories()

            if not memories:
                logger.warning("No memories found for backup")

                return {
                    "success": True,
                    "backup_id": backup_id,
                    "memory_count": 0,
                    "message": "No memories to backup",
                }

            # Prepare backup data

            backup_data = {
                "backup_info": {
                    "id": backup_id,
                    "created_at": timestamp,
                    "user_id": user_id,
                    "memory_count": len(memories),
                    "include_metadata": include_metadata,
                    "compressed": compress,
                },
                "memories": [],
            }

            # Serialize memories

            for memory in memories:
                memory_data = {
                    "id": memory.id,
                    "content": memory.content,
                    "created_at": memory.created_at.isoformat()
                    if hasattr(memory, "created_at")
                    else timestamp,
                    "updated_at": memory.updated_at.isoformat()
                    if hasattr(memory, "updated_at")
                    else timestamp,
                }

                if include_metadata and hasattr(memory, "metadata"):
                    memory_data["metadata"] = memory.metadata

                if hasattr(memory, "user_id"):
                    memory_data["user_id"] = memory.user_id

                if hasattr(memory, "memory_type"):
                    memory_data["memory_type"] = memory.memory_type

                backup_data["memories"].append(memory_data)

            # Convert to JSON

            backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)

            # Compress if requested

            if compress and self.compression_service:
                backup_content = await self.compression_service.compress_text(
                    backup_json
                )

                backup_filename = f"{backup_id}.json.gz"

            else:
                backup_content = backup_json.encode("utf-8")

                backup_filename = f"{backup_id}.json"

            # Store backup

            backup_path = f"backups/memory/{backup_filename}"

            await self.storage_service.store_file(
                backup_path,
                backup_content,
                metadata={
                    "backup_id": backup_id,
                    "user_id": user_id,
                    "memory_count": len(memories),
                    "compressed": compress,
                    "created_at": timestamp,
                },
            )

            # Record backup metadata in memory system

            backup_memory = {
                "type": "backup_record",
                "backup_id": backup_id,
                "user_id": user_id,
                "memory_count": len(memories),
                "backup_path": backup_path,
                "compressed": compress,
                "size_bytes": len(backup_content),
                "created_at": timestamp,
            }

            await self.memory_repository.store_memory(backup_memory)

            logger.info(
                f"Created memory backup {backup_id} with {len(memories)} memories"
            )

            return {
                "success": True,
                "backup_id": backup_id,
                "memory_count": len(memories),
                "backup_path": backup_path,
                "size_bytes": len(backup_content),
                "compressed": compress,
                "storage_url": storage_result.get("url"),
            }

        except Exception as e:
            logger.error(f"Failed to create memory backup: {e}")

            raise RuntimeError(f"Backup creation failed: {e}") from e

    async def create_incremental_backup(
        self, base_backup_id: str, user_id: str | None = None
    ) -> dict[str, Any]:
        """Create an incremental backup since the last backup.





        Args:


            base_backup_id: ID of the base backup


            user_id: Optional user ID to filter memories





        Returns:


            Dict containing incremental backup information


        """

        try:
            # Get base backup info

            base_backup = await self.memory_repository.get_memories_by_type(
                "backup_record"
            )

            base_backup = [
                b for b in base_backup if b.metadata.get("backup_id") == base_backup_id
            ]

            if not base_backup:
                raise ValueError(f"Base backup {base_backup_id} not found")

            base_backup = base_backup[0]

            base_timestamp = base_backup.metadata.get("created_at")

            # Get memories created/updated since base backup

            if user_id:
                all_memories = await self.memory_repository.get_memories_by_user(
                    user_id
                )

            else:
                all_memories = await self.memory_repository.get_all_memories()

            # Filter for memories newer than base backup

            incremental_memories = []

            for memory in all_memories:
                memory_timestamp = (
                    memory.created_at.isoformat()
                    if hasattr(memory, "created_at")
                    else None
                )

                updated_timestamp = (
                    memory.updated_at.isoformat()
                    if hasattr(memory, "updated_at")
                    else None
                )

                if (memory_timestamp and memory_timestamp > base_timestamp) or (
                    updated_timestamp and updated_timestamp > base_timestamp
                ):
                    incremental_memories.append(memory)

            if not incremental_memories:
                return {
                    "success": True,
                    "backup_id": f"incremental_{base_backup_id}_{datetime.now(UTC).isoformat()}",
                    "memory_count": 0,
                    "message": "No new memories since base backup",
                }

            # Create incremental backup

            timestamp = datetime.now(UTC).isoformat()

            incremental_id = f"incremental_{base_backup_id}_{timestamp.replace(':', '-').replace('.', '-')}"

            backup_data = {
                "backup_info": {
                    "id": incremental_id,
                    "type": "incremental",
                    "base_backup_id": base_backup_id,
                    "created_at": timestamp,
                    "user_id": user_id,
                    "memory_count": len(incremental_memories),
                },
                "memories": [],
            }

            # Serialize incremental memories

            for memory in incremental_memories:
                memory_data = {
                    "id": memory.id,
                    "content": memory.content,
                    "created_at": memory.created_at.isoformat()
                    if hasattr(memory, "created_at")
                    else timestamp,
                    "updated_at": memory.updated_at.isoformat()
                    if hasattr(memory, "updated_at")
                    else timestamp,
                }

                if hasattr(memory, "metadata"):
                    memory_data["metadata"] = memory.metadata

                backup_data["memories"].append(memory_data)

            # Store incremental backup

            backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)

            backup_content = backup_json.encode("utf-8")

            backup_path = f"backups/memory/incremental/{incremental_id}.json"

            await self.storage_service.store_file(backup_path, backup_content)

            # Record incremental backup

            backup_memory = {
                "type": "backup_record",
                "backup_id": incremental_id,
                "backup_type": "incremental",
                "base_backup_id": base_backup_id,
                "user_id": user_id,
                "memory_count": len(incremental_memories),
                "backup_path": backup_path,
                "size_bytes": len(backup_content),
                "created_at": timestamp,
            }

            await self.memory_repository.store_memory(backup_memory)

            logger.info(
                f"Created incremental backup {incremental_id} with {len(incremental_memories)} new memories"
            )

            return {
                "success": True,
                "backup_id": incremental_id,
                "base_backup_id": base_backup_id,
                "memory_count": len(incremental_memories),
                "backup_path": backup_path,
                "size_bytes": len(backup_content),
            }

        except Exception as e:
            logger.error(f"Failed to create incremental backup: {e}")

            raise RuntimeError(f"Incremental backup creation failed: {e}") from e

    async def restore_backup(
        self,
        backup_id: str,
        target_user_id: str | None = None,
        overwrite_existing: bool = False,
    ) -> dict[str, Any]:
        """Restore memories from a backup.





        Args:


            backup_id: ID of the backup to restore


            target_user_id: Optional target user ID for restoration


            overwrite_existing: Whether to overwrite existing memories





        Returns:


            Dict containing restoration results


        """

        try:
            # Find backup record

            backup_records = await self.memory_repository.get_memories_by_type(
                "backup_record"
            )

            backup_record = None

            for record in backup_records:
                if record.metadata.get("backup_id") == backup_id:
                    backup_record = record

                    break

            if not backup_record:
                raise ValueError(f"Backup {backup_id} not found")

            backup_path = backup_record.metadata.get("backup_path")

            is_compressed = backup_record.metadata.get("compressed", False)

            # Load backup data

            backup_content = await self.storage_service.load_file(backup_path)

            if is_compressed and self.compression_service:
                backup_json = await self.compression_service.decompress_text(
                    backup_content
                )

            else:
                backup_json = backup_content.decode("utf-8")

            backup_data = json.loads(backup_json)

            # Validate backup data

            if "memories" not in backup_data:
                raise ValueError("Invalid backup format: missing memories")

            memories_to_restore = backup_data["memories"]

            restored_count = 0

            skipped_count = 0

            error_count = 0

            # Restore memories

            for memory_data in memories_to_restore:
                try:
                    memory_id = memory_data.get("id")

                    # Check if memory already exists

                    if not overwrite_existing:
                        existing_memory = await self.memory_repository.get_by_id(
                            memory_id
                        )

                        if existing_memory:
                            skipped_count += 1

                            continue

                    # Prepare memory for restoration

                    restore_memory = {
                        "id": memory_id,
                        "content": memory_data.get("content"),
                        "metadata": memory_data.get("metadata", {}),
                        "user_id": target_user_id or memory_data.get("user_id"),
                        "memory_type": memory_data.get("memory_type", "restored"),
                    }

                    # Add restoration metadata

                    restore_memory["metadata"]["restored_from"] = backup_id

                    restore_memory["metadata"]["restored_at"] = datetime.now(
                        UTC
                    ).isoformat()

                    # Store restored memory

                    await self.memory_repository.store_memory(restore_memory)

                    restored_count += 1

                except Exception as e:
                    logger.warning(
                        f"Failed to restore memory {memory_data.get('id', 'unknown')}: {e}"
                    )

                    error_count += 1

                    continue

            # Record restoration event

            restoration_record = {
                "type": "restoration_record",
                "backup_id": backup_id,
                "target_user_id": target_user_id,
                "restored_count": restored_count,
                "skipped_count": skipped_count,
                "error_count": error_count,
                "overwrite_existing": overwrite_existing,
                "restored_at": datetime.now(UTC).isoformat(),
            }

            await self.memory_repository.store_memory(restoration_record)

            logger.info(f"Restored {restored_count} memories from backup {backup_id}")

            return {
                "success": True,
                "backup_id": backup_id,
                "target_user_id": target_user_id,
                "restored_count": restored_count,
                "skipped_count": skipped_count,
                "error_count": error_count,
                "total_memories": len(memories_to_restore),
            }

        except Exception as e:
            logger.error(f"Failed to restore backup {backup_id}: {e}")

            raise RuntimeError(f"Backup restoration failed: {e}") from e

    async def list_backups(self, user_id: str | None = None) -> dict[str, Any]:
        """List available backups.





        Args:


            user_id: Optional user ID to filter backups





        Returns:


            Dict containing backup list


        """

        try:
            backup_records = await self.memory_repository.get_memories_by_type(
                "backup_record"
            )

            if user_id:
                backup_records = [
                    r for r in backup_records if r.metadata.get("user_id") == user_id
                ]

            backups = []

            for record in backup_records:
                backup_info = {
                    "backup_id": record.metadata.get("backup_id"),
                    "backup_type": record.metadata.get("backup_type", "full"),
                    "user_id": record.metadata.get("user_id"),
                    "memory_count": record.metadata.get("memory_count", 0),
                    "size_bytes": record.metadata.get("size_bytes", 0),
                    "compressed": record.metadata.get("compressed", False),
                    "created_at": record.metadata.get("created_at"),
                }

                if record.metadata.get("backup_type") == "incremental":
                    backup_info["base_backup_id"] = record.metadata.get(
                        "base_backup_id"
                    )

                backups.append(backup_info)

            # Sort by creation date (newest first)

            backups.sort(key=lambda x: x.get("created_at", ""), reverse=True)

            return {
                "success": True,
                "backups": backups,
                "total_count": len(backups),
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to list backups: {e}")

            raise RuntimeError(f"Failed to list backups: {e}") from e

    async def delete_backup(self, backup_id: str) -> dict[str, Any]:
        """Delete a backup.





        Args:


            backup_id: ID of the backup to delete





        Returns:


            Dict containing deletion results


        """

        try:
            # Find backup record

            backup_records = await self.memory_repository.get_memories_by_type(
                "backup_record"
            )

            backup_record = None

            for record in backup_records:
                if record.metadata.get("backup_id") == backup_id:
                    backup_record = record

                    break

            if not backup_record:
                raise ValueError(f"Backup {backup_id} not found")

            backup_path = backup_record.metadata.get("backup_path")

            # Delete backup file

            await self.storage_service.delete_file(backup_path)

            # Delete backup record

            await self.memory_repository.delete_memory(backup_record.id)

            logger.info(f"Deleted backup {backup_id}")

            return {
                "success": True,
                "backup_id": backup_id,
                "message": "Backup deleted successfully",
            }

        except Exception as e:
            logger.error(f"Failed to delete backup {backup_id}: {e}")

            raise RuntimeError(f"Backup deletion failed: {e}") from e

    async def get_backup_statistics(self, user_id: str | None = None) -> dict[str, Any]:
        """Get backup statistics.





        Args:


            user_id: Optional user ID to filter statistics





        Returns:


            Dict containing backup statistics


        """

        try:
            backup_records = await self.memory_repository.get_memories_by_type(
                "backup_record"
            )

            if user_id:
                backup_records = [
                    r for r in backup_records if r.metadata.get("user_id") == user_id
                ]

            if not backup_records:
                return {
                    "total_backups": 0,
                    "full_backups": 0,
                    "incremental_backups": 0,
                    "total_memories_backed_up": 0,
                    "total_storage_bytes": 0,
                    "user_id": user_id,
                }

            # Calculate statistics

            full_backups = sum(
                1
                for r in backup_records
                if r.metadata.get("backup_type", "full") == "full"
            )

            incremental_backups = sum(
                1
                for r in backup_records
                if r.metadata.get("backup_type") == "incremental"
            )

            total_memories = sum(
                r.metadata.get("memory_count", 0) for r in backup_records
            )

            total_storage = sum(r.metadata.get("size_bytes", 0) for r in backup_records)

            # Find latest backup

            latest_backup = max(
                backup_records,
                key=lambda r: r.metadata.get("created_at", ""),
                default=None,
            )

            return {
                "total_backups": len(backup_records),
                "full_backups": full_backups,
                "incremental_backups": incremental_backups,
                "total_memories_backed_up": total_memories,
                "total_storage_bytes": total_storage,
                "latest_backup_id": latest_backup.metadata.get("backup_id")
                if latest_backup
                else None,
                "latest_backup_date": latest_backup.metadata.get("created_at")
                if latest_backup
                else None,
                "user_id": user_id,
            }

        except Exception as e:
            logger.error(f"Failed to get backup statistics: {e}")

            raise RuntimeError(f"Failed to get backup statistics: {e}") from e
