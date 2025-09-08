"""Backup service for data protection and recovery.





This service provides automated backup, restore, and data protection


capabilities for the AI system.


"""

from __future__ import annotations

import asyncio
import gzip
import json
import logging
import time
from collections.abc import Callable
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4
import Exception
import RuntimeError
import b
import backup
import backup_directory
import backup_file
import backup_schedule_hours
import backup_type
import bool
import compression_enabled
import description
import dict
import e
import f
import hasattr
import int
import len
import limit
import list
import max
import max_concurrent_backups
import open
import retention_days
import self
import set
import sorted
import str
import t
import target_name
import targets
import x

logger = logging.getLogger(__name__)


class BackupType(Enum):
    """Types of backups that can be performed."""

    FULL = "full"

    INCREMENTAL = "incremental"

    DIFFERENTIAL = "differential"

    SNAPSHOT = "snapshot"


class BackupStatus(Enum):
    """Backup operation status."""

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


class BackupService:
    """Service for managing backups and data protection."""

    def __init__(
        self,
        backup_directory: str = "./backups",
        retention_days: int = 30,
        compression_enabled: bool = True,
        max_concurrent_backups: int = 2,
        backup_schedule_hours: int = 24,
    ) -> None:
        """Initialize the backup service.





        Args:


            backup_directory: Directory to store backups.


            retention_days: Number of days to retain backups.


            compression_enabled: Whether to compress backup files.


            max_concurrent_backups: Maximum concurrent backup operations.


            backup_schedule_hours: Hours between scheduled backups.


        """

        self.backup_directory = Path(backup_directory)

        self.retention_days = retention_days

        self.compression_enabled = compression_enabled

        self.max_concurrent_backups = max_concurrent_backups

        self.backup_schedule_hours = backup_schedule_hours

        # Ensure backup directory exists

        self.backup_directory.mkdir(parents=True, exist_ok=True)

        # Backup tracking

        self._backup_jobs: dict[str, dict[str, Any]] = {}

        self._backup_history: list[dict[str, Any]] = []

        self._running_backups: set[str] = set()

        # Backup targets and handlers

        self._backup_targets: dict[str, Callable[[], dict[str, Any]]] = {}

        self._restore_handlers: dict[str, Callable[[dict[str, Any]], bool]] = {}

        # Background tasks

        self._scheduler_task: asyncio.Task[None] | None = None

        self._cleanup_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start backup service background tasks."""

        self._scheduler_task = asyncio.create_task(self._backup_scheduler())

        self._cleanup_task = asyncio.create_task(self._cleanup_old_backups())

        logger.info("Backup service background tasks started")

    async def stop(self) -> None:
        """Stop backup service background tasks."""

        if self._scheduler_task:
            self._scheduler_task.cancel()

            try:
                await self._scheduler_task

            except asyncio.CancelledError:
                logger.debug("Backup scheduler task cancelled")

                raise

        if self._cleanup_task:
            self._cleanup_task.cancel()

            try:
                await self._cleanup_task

            except asyncio.CancelledError:
                logger.debug("Backup cleanup task cancelled")

                raise

        # Wait for running backups to complete

        if self._running_backups:
            logger.info(
                f"Waiting for {len(self._running_backups)} running backups to complete..."
            )

            while self._running_backups:
                await asyncio.sleep(1)

        logger.info("Backup service background tasks stopped")

    def register_backup_target(
        self,
        target_name: str,
        backup_handler: Callable[[], dict[str, Any]],
        restore_handler: Callable[[dict[str, Any]], bool] | None = None,
    ) -> None:
        """Register a backup target with its handlers.





        Args:


            target_name: Name of the backup target.


            backup_handler: Function to extract data for backup.


            restore_handler: Function to restore data from backup.


        """

        self._backup_targets[target_name] = backup_handler

        if restore_handler:
            self._restore_handlers[target_name] = restore_handler

        logger.info(f"Registered backup target: {target_name}")

    async def create_backup(
        self,
        backup_type: BackupType = BackupType.FULL,
        targets: list[str] | None = None,
        description: str | None = None,
    ) -> str:
        """Create a backup.





        Args:


            backup_type: Type of backup to create.


            targets: Specific targets to backup (None for all).


            description: Optional backup description.





        Returns:


            Backup job ID.


        """

        # Check concurrent backup limit

        if len(self._running_backups) >= self.max_concurrent_backups:
            raise RuntimeError("Maximum concurrent backups reached")

        job_id = str(uuid4())

        backup_job = {
            "job_id": job_id,
            "backup_type": backup_type.value,
            "targets": targets or list(self._backup_targets.keys()),
            "description": description,
            "status": BackupStatus.PENDING.value,
            "created_at": time.time(),
            "started_at": None,
            "completed_at": None,
            "file_path": None,
            "file_size": None,
            "error_message": None,
            "metadata": {},
        }

        self._backup_jobs[job_id] = backup_job

        # Start backup task

        # Keep reference to the background task to avoid GC and enable optional tracking
        task = asyncio.create_task(self._perform_backup(job_id))
        if not hasattr(self, "_pending_tasks"):
            self._pending_tasks: set[asyncio.Task[None]] = set()
        self._pending_tasks.add(task)
        task.add_done_callback(lambda t: self._pending_tasks.discard(t))

        logger.info(f"Created backup job {job_id} ({backup_type.value})")

        return job_id

    async def restore_backup(
        self, backup_file: str, targets: list[str] | None = None
    ) -> bool:
        """Restore from a backup file.





        Args:


            backup_file: Path to backup file.


            targets: Specific targets to restore (None for all).





        Returns:


            True if restore was successful.


        """

        backup_path = self.backup_directory / backup_file

        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_file}")

            return False

        try:
            # Load backup data

            backup_data = await self._load_backup_file(backup_path)

            if not backup_data:
                logger.error(f"Failed to load backup data from {backup_file}")

                return False

            # Restore targets

            restore_targets = targets or list(backup_data.get("data", {}).keys())

            success_count = 0

            for target_name in restore_targets:
                if target_name not in backup_data.get("data", {}):
                    logger.warning(f"Target {target_name} not found in backup")

                    continue

                if target_name not in self._restore_handlers:
                    logger.warning(f"No restore handler for target {target_name}")

                    continue

                try:
                    target_data = backup_data["data"][target_name]

                    restore_handler = self._restore_handlers[target_name]

                    if asyncio.iscoroutinefunction(restore_handler):
                        success = await restore_handler(target_data)

                    else:
                        success = restore_handler(target_data)

                    if success:
                        success_count += 1

                        logger.info(f"Successfully restored target: {target_name}")

                    else:
                        logger.error(f"Failed to restore target: {target_name}")

                except Exception as e:
                    logger.error(f"Error restoring target {target_name}: {e}")

            logger.info(
                f"Restore completed: {success_count}/{len(restore_targets)} targets successful"
            )

            return success_count == len(restore_targets)

        except Exception as e:
            logger.error(f"Error during restore operation: {e}")

            return False

    async def get_backup_status(self, job_id: str) -> dict[str, Any] | None:
        """Get backup job status.





        Args:


            job_id: Backup job ID.





        Returns:


            Backup job status or None if not found.


        """

        return (
            self._backup_jobs.get(job_id, {}).copy()
            if job_id in self._backup_jobs
            else None
        )

    async def list_backups(self, limit: int = 50) -> list[dict[str, Any]]:
        """List available backups.





        Args:


            limit: Maximum number of backups to return.





        Returns:


            List of backup information.


        """

        backups = []

        # Get backups from history

        for backup in sorted(
            self._backup_history, key=lambda x: x["created_at"], reverse=True
        ):
            if len(backups) >= limit:
                break

            backup_info = backup.copy()

            # Check if file still exists

            if backup_info.get("file_path"):
                file_path = Path(backup_info["file_path"])

                backup_info["file_exists"] = file_path.exists()

                if backup_info["file_exists"] and not backup_info.get("file_size"):
                    backup_info["file_size"] = file_path.stat().st_size

            backups.append(backup_info)

        return backups

    async def delete_backup(self, backup_file: str) -> bool:
        """Delete a backup file.





        Args:


            backup_file: Backup file name.





        Returns:


            True if deletion was successful.


        """

        backup_path = self.backup_directory / backup_file

        try:
            if backup_path.exists():
                backup_path.unlink()

                # Remove from history

                self._backup_history = [
                    b
                    for b in self._backup_history
                    if b.get("file_path") != str(backup_path)
                ]

                logger.info(f"Deleted backup file: {backup_file}")

                return True

            else:
                logger.warning(f"Backup file not found: {backup_file}")

                return False

        except Exception as e:
            logger.error(f"Error deleting backup {backup_file}: {e}")

            return False

    async def get_backup_statistics(self) -> dict[str, Any]:
        """Get backup statistics.





        Returns:


            Backup statistics and metrics.


        """

        # Count backups by status

        status_counts = {}

        for job in self._backup_jobs.values():
            status = job["status"]

            status_counts[status] = status_counts.get(status, 0) + 1

        # Calculate total backup size

        total_size = 0

        successful_backups = 0

        for backup in self._backup_history:
            if backup["status"] == BackupStatus.COMPLETED.value and backup.get(
                "file_size"
            ):
                total_size += backup["file_size"]

                successful_backups += 1

        # Get recent backup info

        recent_backups = sorted(
            [
                b
                for b in self._backup_history
                if b["status"] == BackupStatus.COMPLETED.value
            ],
            key=lambda x: x["created_at"],
            reverse=True,
        )[:5]

        return {
            "total_backups": len(self._backup_history),
            "successful_backups": successful_backups,
            "running_backups": len(self._running_backups),
            "status_counts": status_counts,
            "total_backup_size_bytes": total_size,
            "registered_targets": len(self._backup_targets),
            "recent_backups": recent_backups,
            "retention_days": self.retention_days,
            "compression_enabled": self.compression_enabled,
        }

    async def _perform_backup(self, job_id: str) -> None:
        """Perform the actual backup operation.





        Args:


            job_id: Backup job ID.


        """

        job = self._backup_jobs.get(job_id)

        if not job:
            return

        self._running_backups.add(job_id)

        try:
            job["status"] = BackupStatus.RUNNING.value

            job["started_at"] = time.time()

            # Collect data from all targets

            backup_data = {
                "metadata": {
                    "job_id": job_id,
                    "backup_type": job["backup_type"],
                    "created_at": job["created_at"],
                    "targets": job["targets"],
                    "description": job["description"],
                    "version": "1.0",
                },
                "data": {},
            }

            for target_name in job["targets"]:
                if target_name not in self._backup_targets:
                    logger.warning(f"Backup target {target_name} not found")

                    continue

                try:
                    backup_handler = self._backup_targets[target_name]

                    if asyncio.iscoroutinefunction(backup_handler):
                        target_data = await backup_handler()

                    else:
                        target_data = backup_handler()

                    backup_data["data"][target_name] = target_data

                    logger.debug(f"Collected backup data for target: {target_name}")

                except Exception as e:
                    logger.error(f"Error backing up target {target_name}: {e}")

                    job["error_message"] = f"Failed to backup target {target_name}: {e}"

            # Save backup to file

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"backup_{timestamp}_{job_id[:8]}.json"

            if self.compression_enabled:
                filename += ".gz"

            backup_path = self.backup_directory / filename

            await self._save_backup_file(backup_data, backup_path)

            # Update job status

            job["status"] = BackupStatus.COMPLETED.value

            job["completed_at"] = time.time()

            job["file_path"] = str(backup_path)

            job["file_size"] = backup_path.stat().st_size

            # Add to history

            self._backup_history.append(job.copy())

            logger.info(f"Backup job {job_id} completed successfully: {filename}")

        except Exception as e:
            job["status"] = BackupStatus.FAILED.value

            job["error_message"] = str(e)

            job["completed_at"] = time.time()

            logger.error(f"Backup job {job_id} failed: {e}")

        finally:
            self._running_backups.discard(job_id)

    async def _save_backup_file(
        self, backup_data: dict[str, Any], file_path: Path
    ) -> None:
        """Save backup data to file.





        Args:


            backup_data: Data to backup.


            file_path: File path to save to.


        """

        json_data = json.dumps(backup_data, indent=2, default=str)

        if self.compression_enabled and file_path.suffix == ".gz":
            # Save compressed

            with gzip.open(file_path, "wt", encoding="utf-8") as f:
                f.write(json_data)

        else:
            # Save uncompressed

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(json_data)

    async def _load_backup_file(self, file_path: Path) -> dict[str, Any] | None:
        """Load backup data from file.





        Args:


            file_path: File path to load from.





        Returns:


            Backup data or None if failed.


        """

        try:
            if file_path.suffix == ".gz":
                # Load compressed

                with gzip.open(file_path, "rt", encoding="utf-8") as f:
                    return json.load(f)

            else:
                # Load uncompressed

                with open(file_path, encoding="utf-8") as f:
                    return json.load(f)

        except Exception as e:
            logger.error(f"Error loading backup file {file_path}: {e}")

            return None

    async def _backup_scheduler(self) -> None:
        """Background task for scheduled backups."""

        while True:
            try:
                # Check if it's time for a scheduled backup

                now = time.time()

                last_backup_time = 0

                # Find last successful backup

                successful_backups = [
                    b
                    for b in self._backup_history
                    if b["status"] == BackupStatus.COMPLETED.value
                ]

                if successful_backups:
                    last_backup_time = max(b["created_at"] for b in successful_backups)

                # Check if backup is due

                time_since_last = now - last_backup_time

                if time_since_last >= (self.backup_schedule_hours * 3600):
                    logger.info("Starting scheduled backup")

                    await self.create_backup(
                        backup_type=BackupType.INCREMENTAL,
                        description="Scheduled automatic backup",
                    )

                # Sleep for 1 hour

                await asyncio.sleep(3600)

            except asyncio.CancelledError:
                logger.debug("Backup scheduler task cancelled")

                raise

            except Exception as e:
                logger.error(f"Error in backup scheduler: {e}")

                await asyncio.sleep(1800)  # Wait 30 minutes before retry

    async def _cleanup_old_backups(self) -> None:
        """Background task to clean up old backups."""

        while True:
            try:
                cutoff_time = time.time() - (self.retention_days * 24 * 3600)

                # Find old backups to delete

                old_backups = [
                    backup
                    for backup in self._backup_history
                    if backup["created_at"] < cutoff_time
                ]

                for backup in old_backups:
                    if backup.get("file_path"):
                        file_path = Path(backup["file_path"])

                        if file_path.exists():
                            try:
                                file_path.unlink()

                                logger.info(f"Deleted old backup: {file_path.name}")

                            except Exception as e:
                                logger.error(
                                    f"Error deleting old backup {file_path}: {e}"
                                )

                # Remove from history

                self._backup_history = [
                    backup
                    for backup in self._backup_history
                    if backup["created_at"] >= cutoff_time
                ]

                if old_backups:
                    logger.info(f"Cleaned up {len(old_backups)} old backups")

                # Sleep for 24 hours

                await asyncio.sleep(24 * 3600)

            except asyncio.CancelledError:
                logger.debug("Backup cleanup task cancelled")

                raise

            except Exception as e:
                logger.error(f"Error in backup cleanup: {e}")

                await asyncio.sleep(3600)  # Wait 1 hour before retry
