"""Backup storage system for ZETA AI Server.





This module provides comprehensive backup functionality including:


- Database backups with transaction consistency


- File system backups with incremental support


- Configuration backups


- Automated backup scheduling and rotation


- Backup verification and restoration


"""

import json
import logging
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import Exception
import all
import backup
import backup_dir
import backup_name
import backup_path
import backup_type
import backups
import bool
import chunk
import classmethod
import cls
import compress
import compressed
import config_dir
import created_at
import db_url
import dict
import e
import enumerate
import exclude_patterns
import f
import file_path
import i
import int
import iter
import k
import len
import limit
import line
import list
import m
import max_backups
import open
import overwrite
import pattern
import restore_path
import result
import retention_days
import self
import str
import sum
import tag
import tags
import tar
import tarinfo
import v
import verify_backups
import x

logger = logging.getLogger(__name__)


class BackupConfig:
    """Configuration for backup operations."""

    def __init__(
        self,
        backup_dir: str | Path,
        retention_days: int = 30,
        max_backups: int = 10,
        compress: bool = True,
        verify_backups: bool = True,
        exclude_patterns: list[str] | None = None,
    ):
        """Initialize backup configuration.





        Args:


            backup_dir: Directory to store backups


            retention_days: Days to keep backups


            max_backups: Maximum number of backups to keep


            compress: Whether to compress backups


            verify_backups: Whether to verify backup integrity


            exclude_patterns: Patterns to exclude from backups


        """

        self.backup_dir = Path(backup_dir)

        self.backup_dir.mkdir(parents=True, exist_ok=True)

        self.retention_days = retention_days

        self.max_backups = max_backups

        self.compress = compress

        self.verify_backups = verify_backups

        self.exclude_patterns = exclude_patterns or [
            "*.pyc",
            "__pycache__",
            ".git",
            "*.log",
            "*.tmp",
            ".env",
        ]


class BackupMetadata:
    """Metadata for backup operations."""

    def __init__(
        self,
        backup_id: str,
        backup_type: str,
        source_path: str,
        backup_path: str,
        created_at: datetime,
        size: int,
        checksum: str,
        compressed: bool = False,
        verified: bool = False,
        tags: list[str] | None = None,
    ):
        """Initialize backup metadata.





        Args:


            backup_id: Unique backup identifier


            backup_type: Type of backup (database, files, config)


            source_path: Original source path


            backup_path: Path to backup file


            created_at: When backup was created


            size: Backup size in bytes


            checksum: Backup checksum for verification


            compressed: Whether backup is compressed


            verified: Whether backup was verified


            tags: Optional tags for categorization


        """

        self.backup_id = backup_id

        self.backup_type = backup_type

        self.source_path = source_path

        self.backup_path = backup_path

        self.created_at = created_at

        self.size = size

        self.checksum = checksum

        self.compressed = compressed

        self.verified = verified

        self.tags = tags or []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""

        return {
            "backup_id": self.backup_id,
            "backup_type": self.backup_type,
            "source_path": self.source_path,
            "backup_path": self.backup_path,
            "created_at": self.created_at.isoformat(),
            "size": self.size,
            "checksum": self.checksum,
            "compressed": self.compressed,
            "verified": self.verified,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BackupMetadata":
        """Create from dictionary."""

        return cls(
            backup_id=data["backup_id"],
            backup_type=data["backup_type"],
            source_path=data["source_path"],
            backup_path=data["backup_path"],
            created_at=datetime.fromisoformat(data["created_at"]),
            size=data["size"],
            checksum=data["checksum"],
            compressed=data.get("compressed", False),
            verified=data.get("verified", False),
            tags=data.get("tags", []),
        )


class BackupStorage:
    """Comprehensive backup storage manager."""

    def __init__(self, config: BackupConfig):
        """Initialize backup storage.





        Args:


            config: Backup configuration


        """

        self.config = config

        self.metadata_file = self.config.backup_dir / "backup_metadata.json"

        self._metadata: dict[str, BackupMetadata] = {}

        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load backup metadata from file."""

        try:
            if self.metadata_file.exists():
                with open(self.metadata_file, encoding="utf-8") as f:
                    data = json.load(f)

                    self._metadata = {
                        k: BackupMetadata.from_dict(v) for k, v in data.items()
                    }

        except Exception as e:
            logger.error(f"Failed to load backup metadata: {e}")

            self._metadata = {}

    def _save_metadata(self) -> None:
        """Save backup metadata to file."""

        try:
            data = {k: v.to_dict() for k, v in self._metadata.items()}

            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"Failed to save backup metadata: {e}")

    def _generate_backup_id(self, backup_type: str) -> str:
        """Generate unique backup ID."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        return f"{backup_type}_{timestamp}"

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum for verification."""

        import hashlib

        hash_sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()

    def backup_database(
        self,
        db_url: str,
        backup_name: str | None = None,
        tags: list[str] | None = None,
    ) -> BackupMetadata | None:
        """Create database backup.





        Args:


            db_url: Database connection URL


            backup_name: Custom backup name


            tags: Tags for categorization





        Returns:


            Backup metadata if successful


        """

        try:
            backup_id = backup_name or self._generate_backup_id("database")

            backup_file = self.config.backup_dir / f"{backup_id}.sql"

            if self.config.compress:
                backup_file = backup_file.with_suffix(".sql.gz")

            # Create database dump

            # Note: This is a simplified example - actual implementation would

            # depend on the database type (PostgreSQL, MySQL, SQLite, etc.)

            if "sqlite" in db_url.lower():
                # SQLite backup

                import sqlite3

                db_path = db_url.replace("sqlite:///", "").replace("sqlite://", "")

                source_db = sqlite3.connect(db_path)

                if self.config.compress:
                    import gzip

                    with gzip.open(backup_file, "wt") as f:
                        for line in source_db.iterdump():
                            f.write(f"{line}\n")

                else:
                    with open(backup_file, "w") as f:
                        for line in source_db.iterdump():
                            f.write(f"{line}\n")

                source_db.close()

            elif "postgresql" in db_url.lower():
                # PostgreSQL backup using pg_dump

                cmd = ["pg_dump", db_url]

                if self.config.compress:
                    cmd.extend(["-Z", "9"])  # Max compression

                with open(backup_file, "wb") as f:
                    _ = subprocess.run(
                        cmd, check=False, stdout=f, stderr=subprocess.PIPE
                    )

                    if result.returncode != 0:
                        logger.error(f"pg_dump failed: {result.stderr.decode()}")

                        return None

            else:
                logger.error(f"Unsupported database type: {db_url}")

                return None

            # Calculate metadata

            size = backup_file.stat().st_size

            checksum = self._calculate_checksum(backup_file)

            # Verify backup if enabled

            verified = False

            if self.config.verify_backups:
                verified = self._verify_database_backup(backup_file)

            # Create metadata

            metadata = BackupMetadata(
                backup_id=backup_id,
                backup_type="database",
                source_path=db_url,
                backup_path=str(backup_file),
                created_at=datetime.now(),
                size=size,
                checksum=checksum,
                compressed=self.config.compress,
                verified=verified,
                tags=tags or [],
            )

            # Store metadata

            self._metadata[backup_id] = metadata

            self._save_metadata()

            logger.info(f"Database backup created: {backup_file}")

            return metadata

        except Exception as e:
            logger.error(f"Failed to backup database: {e}")

            return None

    def backup_files(
        self,
        source_path: str | Path,
        backup_name: str | None = None,
        incremental: bool = False,
        tags: list[str] | None = None,
    ) -> BackupMetadata | None:
        """Create file system backup.





        Args:


            source_path: Path to backup


            backup_name: Custom backup name


            incremental: Whether to create incremental backup


            tags: Tags for categorization





        Returns:


            Backup metadata if successful


        """

        try:
            source_path = Path(source_path)

            if not source_path.exists():
                logger.error(f"Source path not found: {source_path}")

                return None

            backup_id = backup_name or self._generate_backup_id("files")

            backup_file = self.config.backup_dir / f"{backup_id}.tar"

            if self.config.compress:
                backup_file = backup_file.with_suffix(".tar.gz")

            # Create exclude file for patterns

            exclude_file = None

            if self.config.exclude_patterns:
                exclude_file = tempfile.NamedTemporaryFile(mode="w", delete=False)

                for pattern in self.config.exclude_patterns:
                    exclude_file.write(f"{pattern}\n")

                exclude_file.close()

            try:
                # Create tar archive

                import tarfile

                mode = "w:gz" if self.config.compress else "w"

                with tarfile.open(backup_file, mode) as tar:
                    if exclude_file:
                        # Use filter to exclude patterns

                        def exclude_filter(tarinfo):
                            for pattern in self.config.exclude_patterns:
                                if pattern in tarinfo.name:
                                    return None

                            return tarinfo

                        tar.add(
                            source_path, arcname=source_path.name, filter=exclude_filter
                        )

                    else:
                        tar.add(source_path, arcname=source_path.name)

            finally:
                # Clean up exclude file

                if exclude_file:
                    Path(exclude_file.name).unlink(missing_ok=True)

            # Calculate metadata

            size = backup_file.stat().st_size

            checksum = self._calculate_checksum(backup_file)

            # Verify backup if enabled

            verified = False

            if self.config.verify_backups:
                verified = self._verify_file_backup(backup_file)

            # Create metadata

            metadata = BackupMetadata(
                backup_id=backup_id,
                backup_type="files",
                source_path=str(source_path),
                backup_path=str(backup_file),
                created_at=datetime.now(),
                size=size,
                checksum=checksum,
                compressed=self.config.compress,
                verified=verified,
                tags=tags or [],
            )

            # Store metadata

            self._metadata[backup_id] = metadata

            self._save_metadata()

            logger.info(f"File backup created: {backup_file}")

            return metadata

        except Exception as e:
            logger.error(f"Failed to backup files: {e}")

            return None

    def backup_config(
        self,
        config_dir: str | Path,
        backup_name: str | None = None,
        tags: list[str] | None = None,
    ) -> BackupMetadata | None:
        """Create configuration backup.





        Args:


            config_dir: Configuration directory to backup


            backup_name: Custom backup name


            tags: Tags for categorization





        Returns:


            Backup metadata if successful


        """

        return self.backup_files(
            source_path=config_dir,
            backup_name=backup_name or self._generate_backup_id("config"),
            tags=(tags or []) + ["config"],
        )

    def restore_backup(
        self,
        backup_id: str,
        restore_path: str | Path | None = None,
        overwrite: bool = False,
    ) -> bool:
        """Restore a backup.





        Args:


            backup_id: ID of backup to restore


            restore_path: Where to restore (optional)


            overwrite: Whether to overwrite existing files





        Returns:


            True if successful, False otherwise


        """

        try:
            metadata = self._metadata.get(backup_id)

            if not metadata:
                logger.error(f"Backup not found: {backup_id}")

                return False

            backup_file = Path(metadata.backup_path)

            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_file}")

                return False

            # Verify backup before restore

            if not self._verify_backup_integrity(metadata):
                logger.error(f"Backup integrity check failed: {backup_id}")

                return False

            # Determine restore location

            if restore_path:
                target_path = Path(restore_path)

            else:
                target_path = Path(metadata.source_path)

            # Check if target exists and handle overwrite

            if target_path.exists() and not overwrite:
                logger.error(f"Target exists and overwrite=False: {target_path}")

                return False

            # Restore based on backup type

            if metadata.backup_type == "database":
                return self._restore_database_backup(metadata, target_path)

            elif metadata.backup_type in ["files", "config"]:
                return self._restore_file_backup(metadata, target_path)

            else:
                logger.error(f"Unknown backup type: {metadata.backup_type}")

                return False

        except Exception as e:
            logger.error(f"Failed to restore backup {backup_id}: {e}")

            return False

    def _verify_database_backup(self, backup_file: Path) -> bool:
        """Verify database backup integrity."""

        try:
            # Basic verification - check if file is readable

            if backup_file.suffix == ".gz":
                import gzip

                with gzip.open(backup_file, "rt") as f:
                    # Try to read first few lines

                    for i, line in enumerate(f):
                        if i > 10:  # Check first 10 lines
                            break

            else:
                with open(backup_file) as f:
                    for i, line in enumerate(f):
                        if i > 10:
                            break

            return True

        except Exception as e:
            logger.error(f"Database backup verification failed: {e}")

            return False

    def _verify_file_backup(self, backup_file: Path) -> bool:
        """Verify file backup integrity."""

        try:
            import tarfile

            # Try to open and list contents

            with tarfile.open(backup_file, "r:*") as tar:
                tar.getnames()  # This will fail if archive is corrupted

            return True

        except Exception as e:
            logger.error(f"File backup verification failed: {e}")

            return False

    def _verify_backup_integrity(self, metadata: BackupMetadata) -> bool:
        """Verify backup integrity using checksum."""

        try:
            backup_file = Path(metadata.backup_path)

            current_checksum = self._calculate_checksum(backup_file)

            return current_checksum == metadata.checksum

        except Exception as e:
            logger.error(f"Integrity verification failed: {e}")

            return False

    def _restore_database_backup(
        self, metadata: BackupMetadata, target_path: Path
    ) -> bool:
        """Restore database backup."""

        try:
            backup_file = Path(metadata.backup_path)

            # Implementation depends on database type

            # This is a simplified example

            if "sqlite" in metadata.source_path.lower():
                import sqlite3

                # Remove existing database if overwrite

                if target_path.exists():
                    target_path.unlink()

                # Restore from SQL dump

                conn = sqlite3.connect(target_path)

                if backup_file.suffix == ".gz":
                    import gzip

                    with gzip.open(backup_file, "rt") as f:
                        sql_content = f.read()

                else:
                    with open(backup_file) as f:
                        sql_content = f.read()

                conn.executescript(sql_content)

                conn.close()

                logger.info(f"Database restored: {target_path}")

                return True

            else:
                logger.error(
                    f"Unsupported database type for restore: {metadata.source_path}"
                )

                return False

        except Exception as e:
            logger.error(f"Database restore failed: {e}")

            return False

    def _restore_file_backup(self, metadata: BackupMetadata, target_path: Path) -> bool:
        """Restore file backup."""

        try:
            import tarfile

            backup_file = Path(metadata.backup_path)

            # Extract tar archive

            with tarfile.open(backup_file, "r:*") as tar:
                tar.extractall(path=target_path.parent)

            logger.info(f"Files restored: {target_path}")

            return True

        except Exception as e:
            logger.error(f"File restore failed: {e}")

            return False

    def list_backups(
        self,
        backup_type: str | None = None,
        tags: list[str] | None = None,
        limit: int | None = None,
    ) -> list[BackupMetadata]:
        """List available backups.





        Args:


            backup_type: Filter by backup type


            tags: Filter by tags


            limit: Maximum number of results





        Returns:


            List of backup metadata


        """

        results = []

        for metadata in self._metadata.values():
            # Filter by type

            if backup_type and metadata.backup_type != backup_type:
                continue

            # Filter by tags

            if tags and not all(tag in metadata.tags for tag in tags):
                continue

            results.append(metadata)

        # Sort by creation date (newest first)

        results.sort(key=lambda x: x.created_at, reverse=True)

        # Apply limit

        if limit:
            results = results[:limit]

        return results

    def cleanup_old_backups(self) -> int:
        """Remove old backups based on retention policy.





        Returns:


            Number of backups removed


        """

        cutoff_date = datetime.now() - timedelta(days=self.config.retention_days)

        removed_count = 0

        # Sort backups by type and date

        backups_by_type = {}

        for metadata in self._metadata.values():
            if metadata.backup_type not in backups_by_type:
                backups_by_type[metadata.backup_type] = []

            backups_by_type[metadata.backup_type].append(metadata)

        to_remove = []

        for backup_type, backups in backups_by_type.items():
            # Sort by date (newest first)

            backups.sort(key=lambda x: x.created_at, reverse=True)

            # Remove backups exceeding max count

            if len(backups) > self.config.max_backups:
                to_remove.extend(backups[self.config.max_backups :])

            # Remove backups older than retention period

            for backup in backups:
                if backup.created_at < cutoff_date and backup not in to_remove:
                    to_remove.append(backup)

        # Remove files and metadata

        for metadata in to_remove:
            try:
                backup_file = Path(metadata.backup_path)

                backup_file.unlink(missing_ok=True)

                del self._metadata[metadata.backup_id]

                removed_count += 1

                logger.info(f"Removed old backup: {metadata.backup_id}")

            except Exception as e:
                logger.error(f"Failed to remove backup {metadata.backup_id}: {e}")

        if to_remove:
            self._save_metadata()

        return removed_count

    def get_backup_stats(self) -> dict[str, Any]:
        """Get backup storage statistics.





        Returns:


            Dictionary with backup statistics


        """

        total_backups = len(self._metadata)

        total_size = sum(m.size for m in self._metadata.values())

        # Group by type

        by_type = {}

        for metadata in self._metadata.values():
            if metadata.backup_type not in by_type:
                by_type[metadata.backup_type] = {"count": 0, "size": 0}

            by_type[metadata.backup_type]["count"] += 1

            by_type[metadata.backup_type]["size"] += metadata.size

        # Calculate disk usage

        actual_disk_usage = sum(
            Path(metadata.backup_path).stat().st_size
            for metadata in self._metadata.values()
            if Path(metadata.backup_path).exists()
        )

        return {
            "total_backups": total_backups,
            "total_size": total_size,
            "actual_disk_usage": actual_disk_usage,
            "by_type": by_type,
            "backup_directory": str(self.config.backup_dir),
            "retention_days": self.config.retention_days,
            "max_backups": self.config.max_backups,
        }


# Convenience functions for quick backup operations


def create_backup_storage(backup_dir: str | Path) -> BackupStorage:
    """Create backup storage with default configuration.





    Args:


        backup_dir: Directory for backups





    Returns:


        BackupStorage instance


    """

    config = BackupConfig(backup_dir)

    return BackupStorage(config)


def quick_database_backup(
    db_url: str, backup_dir: str | Path, tags: list[str] | None = None
) -> BackupMetadata | None:
    """Quick database backup with minimal setup.





    Args:


        db_url: Database URL to backup


        backup_dir: Backup directory


        tags: Optional tags





    Returns:


        Backup metadata if successful


    """

    storage = create_backup_storage(backup_dir)

    return storage.backup_database(db_url, tags=tags)


def quick_file_backup(
    source_path: str | Path,
    backup_dir: str | Path,
    tags: list[str] | None = None,
) -> BackupMetadata | None:
    """Quick file backup with minimal setup.





    Args:


        source_path: Path to backup


        backup_dir: Backup directory


        tags: Optional tags





    Returns:


        Backup metadata if successful


    """

    storage = create_backup_storage(backup_dir)

    return storage.backup_files(source_path, tags=tags)
