#!/usr/bin/env python3
"""
Database backup and restore script for ZETA AI Server.

This script provides functionality to backup and restore PostgreSQL databases
with proper error handling and logging.
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from apps.backend.config.settings import get_settings
import Exception
import FileNotFoundError
import OSError
import backup
import backup_dir
import backup_file
import bool
import database_url
import drop_existing
import e
import hasattr
import int
import keep_count
import len
import list
import print
import self
import str
import x

settings = get_settings()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DatabaseBackupManager:
    """Manages database backup and restore operations."""

    def __init__(self, database_url: str, backup_dir: str = "backups"):
        """Initialize the backup manager.

        Args:
            database_url: PostgreSQL connection URL
            backup_dir: Directory to store backup files
        """
        self.database_url = database_url
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)

    def create_backup(self, backup_name: str | None = None) -> Path:
        """Create a database backup.

        Args:
            backup_name: Optional custom backup name

        Returns:
            Path to the created backup file

        Raises:
            subprocess.CalledProcessError: If backup command fails
        """
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"zeta_ai_backup_{timestamp}.sql"

        backup_path = self.backup_dir / backup_name

        logger.info(f"Creating database backup: {backup_path}")

        try:
            # Use pg_dump to create backup
            cmd = [
                "pg_dump",
                self.database_url,
                "--verbose",
                "--clean",
                "--no-owner",
                "--no-privileges",
                "--file",
                str(backup_path),
            ]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            logger.info(f"Backup created successfully: {backup_path}")
            logger.debug(f"pg_dump output: {result.stderr}")

            return backup_path

        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e}")
            logger.error(f"Command output: {e.stderr}")
            raise
        except FileNotFoundError:
            logger.error("pg_dump command not found. Please ensure PostgreSQL client tools are installed.")
            raise

    def restore_backup(self, backup_path: Path, drop_existing: bool = False) -> None:
        """Restore database from backup.

        Args:
            backup_path: Path to backup file
            drop_existing: Whether to drop existing database first

        Raises:
            subprocess.CalledProcessError: If restore command fails
            FileNotFoundError: If backup file doesn't exist
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        logger.info(f"Restoring database from backup: {backup_path}")

        try:
            if drop_existing:
                self._drop_database()
                self._create_database()

            # Use psql to restore backup
            cmd = ["psql", self.database_url, "--file", str(backup_path), "--verbose"]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            logger.info("Database restored successfully")
            logger.debug(f"psql output: {result.stderr}")

        except subprocess.CalledProcessError as e:
            logger.error(f"Restore failed: {e}")
            logger.error(f"Command output: {e.stderr}")
            raise

    def list_backups(self) -> list[Path]:
        """List available backup files.

        Returns:
            List of backup file paths sorted by modification time
        """
        backup_files = list(self.backup_dir.glob("*.sql"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return backup_files

    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        """Remove old backup files, keeping only the most recent ones.

        Args:
            keep_count: Number of recent backups to keep
        """
        backups = self.list_backups()

        if len(backups) <= keep_count:
            logger.info(f"Found {len(backups)} backups, keeping all (limit: {keep_count})")
            return

        to_delete = backups[keep_count:]
        logger.info(f"Removing {len(to_delete)} old backup files")

        for backup_file in to_delete:
            try:
                backup_file.unlink()
                logger.info(f"Deleted old backup: {backup_file.name}")
            except OSError as e:
                logger.error(f"Failed to delete {backup_file.name}: {e}")

    def _drop_database(self) -> None:
        """Drop the existing database."""
        # Extract database name from URL
        # This is a simplified approach - in production, use a proper URL parser
        db_name = self.database_url.split("/")[-1]

        logger.warning(f"Dropping existing database: {db_name}")

        cmd = ["dropdb", "--if-exists", db_name]
        subprocess.run(cmd, check=True, capture_output=True)

    def _create_database(self) -> None:
        """Create a new database."""
        # Extract database name from URL
        db_name = self.database_url.split("/")[-1]

        logger.info(f"Creating new database: {db_name}")

        cmd = ["createdb", db_name]
        subprocess.run(cmd, check=True, capture_output=True)


def main() -> None:
    """Main function for command line interface."""
    parser = argparse.ArgumentParser(description="Database backup and restore utility for ZETA AI Server")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create database backup")
    backup_parser.add_argument("--name", help="Custom backup name (default: auto-generated)")
    backup_parser.add_argument("--dir", default="backups", help="Backup directory (default: backups)")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore database from backup")
    restore_parser.add_argument("backup_file", help="Path to backup file")
    restore_parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing database before restore",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")
    list_parser.add_argument("--dir", default="backups", help="Backup directory (default: backups)")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Remove old backup files")
    cleanup_parser.add_argument(
        "--keep",
        type=int,
        default=10,
        help="Number of recent backups to keep (default: 10)",
    )
    cleanup_parser.add_argument("--dir", default="backups", help="Backup directory (default: backups)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize backup manager
    try:
        backup_manager = DatabaseBackupManager(settings.database_url, args.dir if hasattr(args, "dir") else "backups")
    except Exception as e:
        logger.error(f"Failed to initialize backup manager: {e}")
        sys.exit(1)

    try:
        if args.command == "backup":
            backup_path = backup_manager.create_backup(args.name)
            print(f"Backup created: {backup_path}")

        elif args.command == "restore":
            backup_path = Path(args.backup_file)
            backup_manager.restore_backup(backup_path, args.drop_existing)
            print(f"Database restored from: {backup_path}")

        elif args.command == "list":
            backups = backup_manager.list_backups()
            if backups:
                print("Available backups:")
                for backup in backups:
                    size = backup.stat().st_size / (1024 * 1024)  # MB
                    mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                    print(f"  {backup.name} ({size:.1f} MB, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print("No backups found")

        elif args.command == "cleanup":
            backup_manager.cleanup_old_backups(args.keep)
            print(f"Cleanup completed, keeping {args.keep} most recent backups")

    except Exception as e:
        logger.error(f"Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
