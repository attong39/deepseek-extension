"""Temporary storage manager for ZETA AI Server.





This module provides temporary file and data storage with automatic cleanup:


- Temporary file creation and management


- Session-based temporary storage


- Automatic cleanup based on age and size


- Safe temporary directory management


- Cleanup scheduling and monitoring


"""

import logging
import os
import shutil
import tempfile
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import Exception
import OSError
import auto_cleanup
import base_dir
import bool
import bytes
import cleanup_interval_minutes
import content
import dict
import e
import encoding
import f
import fd
import float
import int
import isinstance
import item
import item_type
import len
import list
import max_age_minutes
import max_size_mb
import metadata
import property
import purpose
import self
import str
import suffix
import x

logger = logging.getLogger(__name__)


class TempStorageConfig:
    """Configuration for temporary storage."""

    def __init__(
        self,
        base_dir: str | Path | None = None,
        max_age_minutes: int = 60,
        max_size_mb: int = 1024,  # 1GB
        cleanup_interval_minutes: int = 15,
        auto_cleanup: bool = True,
        prefix: str = "zeta_temp_",
    ):
        """Initialize temp storage configuration.





        Args:


            base_dir: Base directory for temporary files (uses system temp if None)


            max_age_minutes: Maximum age of temp files before cleanup


            max_size_mb: Maximum total size of temp storage


            cleanup_interval_minutes: How often to run cleanup


            auto_cleanup: Whether to automatically cleanup old files


            prefix: Prefix for temporary files and directories


        """

        if base_dir:
            self.base_dir = Path(base_dir)

        else:
            self.base_dir = Path(tempfile.gettempdir()) / "zeta_ai_temp"

        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.max_age_minutes = max_age_minutes

        self.max_size_mb = max_size_mb

        self.cleanup_interval_minutes = cleanup_interval_minutes

        self.auto_cleanup = auto_cleanup

        self.prefix = prefix


class TempFile:
    """Represents a temporary file with metadata."""

    def __init__(
        self,
        file_path: Path,
        session_id: str | None = None,
        purpose: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Initialize temporary file.





        Args:


            file_path: Path to temporary file


            session_id: Session ID associated with file


            purpose: Purpose/description of file


            metadata: Additional metadata


        """

        self.file_path = file_path

        self.session_id = session_id

        self.purpose = purpose

        self.metadata = metadata or {}

        self.created_at = datetime.now()

    @property
    def exists(self) -> bool:
        """Check if file exists."""

        return self.file_path.exists()

    @property
    def size(self) -> int:
        """Get file size in bytes."""

        try:
            return self.file_path.stat().st_size if self.exists else 0

        except OSError:
            return 0

    @property
    def age_minutes(self) -> float:
        """Get file age in minutes."""

        return (datetime.now() - self.created_at).total_seconds() / 60

    def read_text(self, encoding: str = "utf-8") -> str:
        """Read file as text."""

        return self.file_path.read_text(encoding=encoding)

    def read_bytes(self) -> bytes:
        """Read file as bytes."""

        return self.file_path.read_bytes()

    def write_text(self, content: str, encoding: str = "utf-8") -> None:
        """Write text to file."""

        self.file_path.write_text(content, encoding=encoding)

    def write_bytes(self, content: bytes) -> None:
        """Write bytes to file."""

        self.file_path.write_bytes(content)

    def delete(self) -> bool:
        """Delete the temporary file."""

        try:
            if self.exists:
                self.file_path.unlink()

            return True

        except Exception as e:
            logger.error(f"Failed to delete temp file {self.file_path}: {e}")

            return False


class TempDirectory:
    """Represents a temporary directory with metadata."""

    def __init__(
        self,
        dir_path: Path,
        session_id: str | None = None,
        purpose: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        """Initialize temporary directory.





        Args:


            dir_path: Path to temporary directory


            session_id: Session ID associated with directory


            purpose: Purpose/description of directory


            metadata: Additional metadata


        """

        self.dir_path = dir_path

        self.session_id = session_id

        self.purpose = purpose

        self.metadata = metadata or {}

        self.created_at = datetime.now()

    @property
    def exists(self) -> bool:
        """Check if directory exists."""

        return self.dir_path.exists() and self.dir_path.is_dir()

    @property
    def size(self) -> int:
        """Get total size of directory in bytes."""

        if not self.exists:
            return 0

        total_size = 0

        try:
            for file_path in self.dir_path.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size

        except OSError:
            pass

        return total_size

    @property
    def age_minutes(self) -> float:
        """Get directory age in minutes."""

        return (datetime.now() - self.created_at).total_seconds() / 60

    def list_files(self) -> list[Path]:
        """List all files in directory."""

        if not self.exists:
            return []

        return [f for f in self.dir_path.rglob("*") if f.is_file()]

    def delete(self) -> bool:
        """Delete the temporary directory and all contents."""

        try:
            if self.exists:
                shutil.rmtree(self.dir_path)

            return True

        except Exception as e:
            logger.error(f"Failed to delete temp directory {self.dir_path}: {e}")

            return False


class TempStorage:
    """Temporary storage manager."""

    def __init__(self, config: TempStorageConfig):
        """Initialize temporary storage.





        Args:


            config: Temporary storage configuration


        """

        self.config = config

        self._files: dict[str, TempFile] = {}

        self._directories: dict[str, TempDirectory] = {}

        self._cleanup_thread: threading.Thread | None = None

        self._stop_cleanup = threading.Event()

        # Start cleanup thread if auto cleanup is enabled

        if self.config.auto_cleanup:
            self._start_cleanup_thread()

    def _start_cleanup_thread(self) -> None:
        """Start the automatic cleanup thread."""

        if self._cleanup_thread and self._cleanup_thread.is_alive():
            return

        self._stop_cleanup.clear()

        self._cleanup_thread = threading.Thread(
            target=self._cleanup_worker, daemon=True
        )

        self._cleanup_thread.start()

        logger.info("Started temp storage cleanup thread")

    def _cleanup_worker(self) -> None:
        """Worker function for automatic cleanup."""

        while not self._stop_cleanup.is_set():
            try:
                self.cleanup_old_files()

            except Exception as e:
                logger.error(f"Error in temp storage cleanup: {e}")

            # Wait for next cleanup interval

            self._stop_cleanup.wait(self.config.cleanup_interval_minutes * 60)

    def stop_cleanup(self) -> None:
        """Stop the automatic cleanup thread."""

        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._stop_cleanup.set()

            self._cleanup_thread.join(timeout=5)

            logger.info("Stopped temp storage cleanup thread")

    def create_temp_file(
        self,
        suffix: str = "",
        prefix: str | None = None,
        session_id: str | None = None,
        purpose: str | None = None,
        content: str | bytes | None = None,
    ) -> TempFile:
        """Create a temporary file.





        Args:


            suffix: File suffix/extension


            prefix: File prefix (uses config prefix if None)


            session_id: Session ID to associate with file


            purpose: Purpose/description of file


            content: Initial content to write





        Returns:


            TempFile instance


        """

        prefix = prefix or self.config.prefix

        # Create temporary file

        fd, file_path = tempfile.mkstemp(
            suffix=suffix, prefix=prefix, dir=self.config.base_dir
        )

        os.close(fd)  # Close the file descriptor

        file_path = Path(file_path)

        # Create TempFile instance

        temp_file = TempFile(
            file_path=file_path, session_id=session_id, purpose=purpose
        )

        # Write initial content if provided

        if content is not None:
            if isinstance(content, str):
                temp_file.write_text(content)

            else:
                temp_file.write_bytes(content)

        # Store in registry

        file_id = str(file_path)

        self._files[file_id] = temp_file

        logger.debug(f"Created temp file: {file_path}")

        return temp_file

    def create_temp_directory(
        self,
        prefix: str | None = None,
        session_id: str | None = None,
        purpose: str | None = None,
    ) -> TempDirectory:
        """Create a temporary directory.





        Args:


            prefix: Directory prefix (uses config prefix if None)


            session_id: Session ID to associate with directory


            purpose: Purpose/description of directory





        Returns:


            TempDirectory instance


        """

        prefix = prefix or self.config.prefix

        # Create temporary directory

        dir_path = Path(tempfile.mkdtemp(prefix=prefix, dir=self.config.base_dir))

        # Create TempDirectory instance

        temp_dir = TempDirectory(
            dir_path=dir_path, session_id=session_id, purpose=purpose
        )

        # Store in registry

        dir_id = str(dir_path)

        self._directories[dir_id] = temp_dir

        logger.debug(f"Created temp directory: {dir_path}")

        return temp_dir

    def get_temp_files(
        self, session_id: str | None = None, purpose: str | None = None
    ) -> list[TempFile]:
        """Get temporary files matching criteria.





        Args:


            session_id: Filter by session ID


            purpose: Filter by purpose





        Returns:


            List of matching TempFile instances


        """

        results = []

        for temp_file in self._files.values():
            if session_id and temp_file.session_id != session_id:
                continue

            if purpose and temp_file.purpose != purpose:
                continue

            results.append(temp_file)

        return results

    def get_temp_directories(
        self, session_id: str | None = None, purpose: str | None = None
    ) -> list[TempDirectory]:
        """Get temporary directories matching criteria.





        Args:


            session_id: Filter by session ID


            purpose: Filter by purpose





        Returns:


            List of matching TempDirectory instances


        """

        results = []

        for temp_dir in self._directories.values():
            if session_id and temp_dir.session_id != session_id:
                continue

            if purpose and temp_dir.purpose != purpose:
                continue

            results.append(temp_dir)

        return results

    def cleanup_session(self, session_id: str) -> int:
        """Clean up all temporary files/directories for a session.





        Args:


            session_id: Session ID to clean up





        Returns:


            Number of items cleaned up


        """

        cleaned_count = 0

        # Clean up files

        files_to_remove = []

        for file_id, temp_file in self._files.items():
            if temp_file.session_id == session_id:
                if temp_file.delete():
                    files_to_remove.append(file_id)

                    cleaned_count += 1

        for file_id in files_to_remove:
            del self._files[file_id]

        # Clean up directories

        dirs_to_remove = []

        for dir_id, temp_dir in self._directories.items():
            if temp_dir.session_id == session_id:
                if temp_dir.delete():
                    dirs_to_remove.append(dir_id)

                    cleaned_count += 1

        for dir_id in dirs_to_remove:
            del self._directories[dir_id]

        logger.info(f"Cleaned up {cleaned_count} temp items for session {session_id}")

        return cleaned_count

    def cleanup_old_files(self) -> int:
        """Clean up old temporary files based on age and size limits.





        Returns:


            Number of items cleaned up


        """

        cleaned_count = 0

        # Get all items sorted by age (oldest first)

        all_items = []

        for temp_file in self._files.values():
            if temp_file.exists:
                all_items.append(("file", temp_file))

        for temp_dir in self._directories.values():
            if temp_dir.exists:
                all_items.append(("dir", temp_dir))

        # Sort by age (oldest first)

        all_items.sort(key=lambda x: x[1].created_at)

        # Remove items that are too old

        cutoff_time = datetime.now() - timedelta(minutes=self.config.max_age_minutes)

        for item_type, item in all_items:
            if item.created_at < cutoff_time:
                if item.delete():
                    cleaned_count += 1

                    # Remove from registry

                    if item_type == "file":
                        self._files.pop(str(item.file_path), None)

                    else:
                        self._directories.pop(str(item.dir_path), None)

        # Check total size and remove oldest if over limit

        total_size = self.get_total_size()

        max_size_bytes = self.config.max_size_mb * 1024 * 1024

        if total_size > max_size_bytes:
            # Remove oldest items until under limit

            remaining_items = [
                (item_type, item)
                for item_type, item in all_items
                if item.exists  # Only items that still exist
            ]

            for item_type, item in remaining_items:
                if self.get_total_size() <= max_size_bytes:
                    break

                if item.delete():
                    cleaned_count += 1

                    # Remove from registry

                    if item_type == "file":
                        self._files.pop(str(item.file_path), None)

                    else:
                        self._directories.pop(str(item.dir_path), None)

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old temp items")

        return cleaned_count

    def get_total_size(self) -> int:
        """Get total size of all temporary storage in bytes.





        Returns:


            Total size in bytes


        """

        total_size = 0

        for temp_file in self._files.values():
            total_size += temp_file.size

        for temp_dir in self._directories.values():
            total_size += temp_dir.size

        return total_size

    def get_stats(self) -> dict[str, Any]:
        """Get temporary storage statistics.





        Returns:


            Dictionary with storage statistics


        """

        total_files = len(self._files)

        total_dirs = len(self._directories)

        total_size = self.get_total_size()

        # Count by session

        session_stats = {}

        for temp_file in self._files.values():
            session_id = temp_file.session_id or "no_session"

            if session_id not in session_stats:
                session_stats[session_id] = {"files": 0, "dirs": 0, "size": 0}

            session_stats[session_id]["files"] += 1

            session_stats[session_id]["size"] += temp_file.size

        for temp_dir in self._directories.values():
            session_id = temp_dir.session_id or "no_session"

            if session_id not in session_stats:
                session_stats[session_id] = {"files": 0, "dirs": 0, "size": 0}

            session_stats[session_id]["dirs"] += 1

            session_stats[session_id]["size"] += temp_dir.size

        return {
            "total_files": total_files,
            "total_directories": total_dirs,
            "total_size": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "base_directory": str(self.config.base_dir),
            "max_age_minutes": self.config.max_age_minutes,
            "max_size_mb": self.config.max_size_mb,
            "auto_cleanup": self.config.auto_cleanup,
            "session_stats": session_stats,
        }

    def clear_all(self) -> int:
        """Clear all temporary files and directories.





        Returns:


            Number of items cleared


        """

        cleared_count = 0

        # Clear files

        for temp_file in self._files.values():
            if temp_file.delete():
                cleared_count += 1

        self._files.clear()

        # Clear directories

        for temp_dir in self._directories.values():
            if temp_dir.delete():
                cleared_count += 1

        self._directories.clear()

        logger.info(f"Cleared all {cleared_count} temp items")

        return cleared_count


# Global temp storage instance for convenience


_global_temp_storage: TempStorage | None = None


def get_temp_storage() -> TempStorage:
    """Get or create global temp storage instance.





    Returns:


        Global TempStorage instance


    """

    global _global_temp_storage

    if _global_temp_storage is None:
        config = TempStorageConfig()

        _global_temp_storage = TempStorage(config)

    return _global_temp_storage


# Convenience functions for quick temp operations


def create_temp_file(
    suffix: str = "",
    content: str | bytes | None = None,
    session_id: str | None = None,
    purpose: str | None = None,
) -> TempFile:
    """Create temporary file with global storage.





    Args:


        suffix: File suffix/extension


        content: Initial content


        session_id: Session ID


        purpose: Purpose description





    Returns:


        TempFile instance


    """

    storage = get_temp_storage()

    return storage.create_temp_file(
        suffix=suffix, content=content, session_id=session_id, purpose=purpose
    )


def create_temp_directory(
    session_id: str | None = None, purpose: str | None = None
) -> TempDirectory:
    """Create temporary directory with global storage.





    Args:


        session_id: Session ID


        purpose: Purpose description





    Returns:


        TempDirectory instance


    """

    storage = get_temp_storage()

    return storage.create_temp_directory(session_id=session_id, purpose=purpose)


def cleanup_session_temp(session_id: str) -> int:
    """Clean up temporary files for a session.





    Args:


        session_id: Session ID to clean up





    Returns:


        Number of items cleaned up


    """

    storage = get_temp_storage()

    return storage.cleanup_session(session_id)
