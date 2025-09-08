"""Archive storage manager for ZETA AI Server.





This module provides functionality for long-term data archival,


compression, and retrieval with lifecycle management.





Features:


- Automated data archival based on age/size policies


- Compression for space optimization


- Metadata tracking and search


- Restoration capabilities


"""

import gzip
import json
import logging
import tarfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import aiofiles
import Exception
import all
import archive_dir
import auto_cleanup
import bool
import chunk
import classmethod
import cls
import compression_level
import created_at
import date_from
import date_to
import default_policy
import dict
import dir_path
import e
import f
import f_in
import f_out
import file_path
import int
import iter
import k
import len
import list
import m
import max_age_days
import max_size_mb
import metadata_file
import open
import original_path
import query
import restore_path
import self
import str
import sum
import tag
import tags
import tar
import v
import x

logger = logging.getLogger(__name__)


class ArchivePolicy:
    """Policy for automatic archival of data."""

    def __init__(
        self,
        max_age_days: int = 90,
        max_size_mb: int = 1000,
        compression_level: int = 6,
        auto_cleanup: bool = True,
    ):
        """Initialize archive policy.





        Args:


            max_age_days: Maximum age before archival (days)


            max_size_mb: Maximum size before archival (MB)


            compression_level: Compression level 1-9


            auto_cleanup: Whether to auto-delete very old archives


        """

        self.max_age_days = max_age_days

        self.max_size_mb = max_size_mb

        self.compression_level = compression_level

        self.auto_cleanup = auto_cleanup


class ArchiveMetadata:
    """Metadata for archived items."""

    def __init__(
        self,
        original_path: str,
        archive_path: str,
        created_at: datetime,
        original_size: int,
        compressed_size: int,
        checksum: str,
        tags: list[str] | None = None,
    ):
        """Initialize archive metadata.





        Args:


            original_path: Original file/directory path


            archive_path: Path to archived file


            created_at: When archive was created


            original_size: Original size in bytes


            compressed_size: Compressed size in bytes


            checksum: Archive checksum for integrity


            tags: Optional tags for categorization


        """

        self.original_path = original_path

        self.archive_path = archive_path

        self.created_at = created_at

        self.original_size = original_size

        self.compressed_size = compressed_size

        self.checksum = checksum

        self.tags = tags or []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""

        return {
            "original_path": self.original_path,
            "archive_path": self.archive_path,
            "created_at": self.created_at.isoformat(),
            "original_size": self.original_size,
            "compressed_size": self.compressed_size,
            "checksum": self.checksum,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArchiveMetadata":
        """Create from dictionary."""

        return cls(
            original_path=data["original_path"],
            archive_path=data["archive_path"],
            created_at=datetime.fromisoformat(data["created_at"]),
            original_size=data["original_size"],
            compressed_size=data["compressed_size"],
            checksum=data["checksum"],
            tags=data.get("tags", []),
        )


class ArchiveStorage:
    """Advanced archive storage manager."""

    def __init__(
        self,
        archive_dir: str | Path,
        metadata_file: str | Path | None = None,
        default_policy: ArchivePolicy | None = None,
    ):
        """Initialize archive storage.





        Args:


            archive_dir: Directory for storing archives


            metadata_file: File for storing archive metadata


            default_policy: Default archival policy


        """

        self.archive_dir = Path(archive_dir)

        self.archive_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = Path(metadata_file or self.archive_dir / "metadata.json")

        self.default_policy = default_policy or ArchivePolicy()

        self._metadata: dict[str, ArchiveMetadata] = {}

        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load archive metadata from file."""

        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, encoding="utf-8") as f:
                    data = json.load(f)

                    self._metadata = {
                        k: ArchiveMetadata.from_dict(v) for k, v in data.items()
                    }

        except Exception as e:
            logger.error(f"Failed to load archive metadata: {e}")

            self._metadata = {}

    def _save_metadata(self) -> None:
        """Save archive metadata to file."""

        try:
            data = {k: v.to_dict() for k, v in self._metadata.items()}

            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save archive metadata: {e}")

    def archive_file(
        self,
        file_path: str | Path,
        archive_name: str | None = None,
        tags: list[str] | None = None,
    ) -> ArchiveMetadata | None:
        """Archive a single file.





        Args:


            file_path: Path to file to archive


            archive_name: Custom archive name (optional)


            tags: Tags for categorization





        Returns:


            Archive metadata if successful, None otherwise


        """

        try:
            source_path = Path(file_path)

            if not source_path.exists():
                logger.error(f"Source file not found: {file_path}")

                return None

            # Generate archive name

            if not archive_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                archive_name = f"{source_path.stem}_{timestamp}.gz"

            archive_path = self.archive_dir / archive_name

            # Compress file

            original_size = source_path.stat().st_size

            with open(source_path, "rb") as f_in:
                content = f_in.read()

            with gzip.open(
                archive_path, "wb", compresslevel=self.default_policy.compression_level
            ) as f_out:
                f_out.write(content)

            compressed_size = archive_path.stat().st_size

            # Calculate checksum

            import hashlib

            checksum = hashlib.sha256(content).hexdigest()

            # Create metadata

            metadata = ArchiveMetadata(
                original_path=str(source_path),
                archive_path=str(archive_path),
                created_at=datetime.now(),
                original_size=original_size,
                compressed_size=compressed_size,
                checksum=checksum,
                tags=tags or [],
            )

            # Store metadata

            self._metadata[str(archive_path)] = metadata

            self._save_metadata()

            logger.info(
                f"Archived {file_path} -> {archive_path} (compression: {compressed_size / original_size:.2%})"
            )

            return metadata

        except Exception as e:
            logger.error(f"Failed to archive {file_path}: {e}")

            return None

    def archive_directory(
        self,
        dir_path: str | Path,
        archive_name: str | None = None,
        tags: list[str] | None = None,
    ) -> ArchiveMetadata | None:
        """Archive a directory as tar.gz.





        Args:


            dir_path: Path to directory to archive


            archive_name: Custom archive name (optional)


            tags: Tags for categorization





        Returns:


            Archive metadata if successful, None otherwise


        """

        try:
            source_path = Path(dir_path)

            if not source_path.exists() or not source_path.is_dir():
                logger.error(f"Source directory not found: {dir_path}")

                return None

            # Generate archive name

            if not archive_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                archive_name = f"{source_path.name}_{timestamp}.tar.gz"

            archive_path = self.archive_dir / archive_name

            # Calculate original size

            original_size = sum(
                f.stat().st_size for f in source_path.rglob("*") if f.is_file()
            )

            # Create tar.gz archive

            with tarfile.open(
                archive_path,
                "w:gz",
                compresslevel=self.default_policy.compression_level,
            ) as tar:
                tar.add(source_path, arcname=source_path.name)

            compressed_size = archive_path.stat().st_size

            # Calculate checksum

            import hashlib

            hash_sha256 = hashlib.sha256()

            with open(archive_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)

            checksum = hash_sha256.hexdigest()

            # Create metadata

            metadata = ArchiveMetadata(
                original_path=str(source_path),
                archive_path=str(archive_path),
                created_at=datetime.now(),
                original_size=original_size,
                compressed_size=compressed_size,
                checksum=checksum,
                tags=tags or [],
            )

            # Store metadata

            self._metadata[str(archive_path)] = metadata

            self._save_metadata()

            logger.info(
                f"Archived directory {dir_path} -> {archive_path} (compression: {compressed_size / original_size:.2%})"
            )

            return metadata

        except Exception as e:
            logger.error(f"Failed to archive directory {dir_path}: {e}")

            return None

    async def restore_archive(
        self,
        archive_path: str | Path,
        restore_path: str | Path | None = None,
    ) -> bool:
        """Restore an archive to specified location.





        Args:


            archive_path: Path to archive file


            restore_path: Where to restore (optional, uses original path)





        Returns:


            True if successful, False otherwise


        """

        try:
            archive_path = Path(archive_path)

            if not archive_path.exists():
                logger.error(f"Archive not found: {archive_path}")

                return False

            # Get metadata

            metadata = self._metadata.get(str(archive_path))

            if not metadata:
                logger.warning(f"No metadata found for archive: {archive_path}")

            # Determine restore path

            if restore_path:
                target_path = Path(restore_path)

            elif metadata:
                target_path = Path(metadata.original_path)

            else:
                # Default to archive name without extension

                target_path = archive_path.parent / archive_path.stem

            # Restore based on archive type

            if archive_path.suffix == ".gz" and not archive_path.name.endswith(
                ".tar.gz"
            ):
                # Single file gzip

                with gzip.open(archive_path, "rb") as f_in:
                    content = f_in.read()

                async with aiofiles.open(target_path, "wb") as f_out:
                    await f_out.write(content)

            elif archive_path.name.endswith(".tar.gz"):
                # Directory tar.gz

                with tarfile.open(archive_path, "r:gz") as tar:
                    tar.extractall(path=target_path.parent)

            else:
                logger.error(f"Unsupported archive format: {archive_path}")

                return False

            logger.info(f"Restored archive {archive_path} -> {target_path}")

            return True

        except Exception as e:
            logger.error(f"Failed to restore archive {archive_path}: {e}")

            return False

    def search_archives(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[ArchiveMetadata]:
        """Search archives by criteria.





        Args:


            query: Text query for original path


            tags: Required tags


            date_from: Minimum creation date


            date_to: Maximum creation date





        Returns:


            List of matching archive metadata


        """

        results = []

        for metadata in self._metadata.values():
            # Check query

            if query and query.lower() not in metadata.original_path.lower():
                continue

            # Check tags

            if tags and not all(tag in metadata.tags for tag in tags):
                continue

            # Check date range

            if date_from and metadata.created_at < date_from:
                continue

            if date_to and metadata.created_at > date_to:
                continue

            results.append(metadata)

        # Sort by creation date (newest first)

        results.sort(key=lambda x: x.created_at, reverse=True)

        return results

    def cleanup_old_archives(self, max_age_days: int = 365) -> int:
        """Remove archives older than specified age.





        Args:


            max_age_days: Maximum age in days





        Returns:


            Number of archives removed


        """

        cutoff_date = datetime.now() - timedelta(days=max_age_days)

        removed_count = 0

        to_remove = []

        for archive_path, metadata in self._metadata.items():
            if metadata.created_at < cutoff_date:
                try:
                    Path(archive_path).unlink(missing_ok=True)

                    to_remove.append(archive_path)

                    removed_count += 1

                    logger.info(f"Removed old archive: {archive_path}")

                except Exception as e:
                    logger.error(f"Failed to remove archive {archive_path}: {e}")

        # Update metadata

        for archive_path in to_remove:
            del self._metadata[archive_path]

        if to_remove:
            self._save_metadata()

        return removed_count

    def get_storage_stats(self) -> dict[str, Any]:
        """Get archive storage statistics.





        Returns:


            Dictionary with storage statistics


        """

        total_archives = len(self._metadata)

        total_original_size = sum(m.original_size for m in self._metadata.values())

        total_compressed_size = sum(m.compressed_size for m in self._metadata.values())

        compression_ratio = (
            total_compressed_size / total_original_size
            if total_original_size > 0
            else 0
        )

        # Calculate disk usage

        actual_disk_usage = sum(
            Path(archive_path).stat().st_size
            for archive_path in self._metadata.keys()
            if Path(archive_path).exists()
        )

        return {
            "total_archives": total_archives,
            "total_original_size": total_original_size,
            "total_compressed_size": total_compressed_size,
            "actual_disk_usage": actual_disk_usage,
            "compression_ratio": compression_ratio,
            "space_saved": total_original_size - total_compressed_size,
            "archive_directory": str(self.archive_dir),
        }


# Convenience functions for common operations


def create_archive_storage(archive_dir: str | Path) -> ArchiveStorage:
    """Create archive storage instance with default settings.





    Args:


        archive_dir: Directory for storing archives





    Returns:


        ArchiveStorage instance


    """

    return ArchiveStorage(archive_dir)


def quick_archive_file(
    file_path: str | Path,
    archive_dir: str | Path,
    tags: list[str] | None = None,
) -> ArchiveMetadata | None:
    """Quick file archival with minimal setup.





    Args:


        file_path: File to archive


        archive_dir: Archive directory


        tags: Optional tags





    Returns:


        Archive metadata if successful


    """

    storage = create_archive_storage(archive_dir)

    return storage.archive_file(file_path, tags=tags)


def quick_archive_directory(
    dir_path: str | Path,
    archive_dir: str | Path,
    tags: list[str] | None = None,
) -> ArchiveMetadata | None:
    """Quick directory archival with minimal setup.





    Args:


        dir_path: Directory to archive


        archive_dir: Archive directory


        tags: Optional tags





    Returns:


        Archive metadata if successful


    """

    storage = create_archive_storage(archive_dir)

    return storage.archive_directory(dir_path, tags=tags)
