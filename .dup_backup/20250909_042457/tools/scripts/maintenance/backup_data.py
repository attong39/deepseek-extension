import Exception
import FileNotFoundError
import backup
import backup_dir
import bool
import database_path
import dict
import e
import int
import keep_count
import len
import list
import locals
import print
import self
import str
import x
# Author: Duy BG VN
# ZETA AI - Comprehensive Backup System

"""Automated backup system for ZETA AI.

Provides comprehensive backup functionality for database, files, configurations,
and application state with multiple storage backends and retention policies.
"""

import logging
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DatabaseBackup:
    """Database backup and maintenance utilities."""

    def __init__(self, database_path: str, backup_dir: str = "storage/backups/database"):
        self.database_path = Path(database_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> str:
        """Create a backup of the database."""
        if not self.database_path.exists():
            raise FileNotFoundError(f"Database file not found: {self.database_path}")

        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.db"
        backup_path = self.backup_dir / backup_filename

        try:
            # For SQLite, we can use simple file copy
            if self.database_path.suffix == ".db":
                self._backup_sqlite(backup_path)
            else:
                # For other databases, use pg_dump or mysqldump
                self._backup_external_db(backup_path)

            print(f"✅ Database backup created: {backup_path}")
            return str(backup_path)

        except Exception as e:
            print(f"❌ Backup failed: {e}")
            raise

    def _backup_sqlite(self, backup_path: Path) -> None:
        """Backup SQLite database using the backup API."""
        # Use SQLite's backup API for consistency
        source_conn = sqlite3.connect(str(self.database_path))
        backup_conn = sqlite3.connect(str(backup_path))

        try:
            source_conn.backup(backup_conn)
            print(f"SQLite backup completed: {backup_path}")
        finally:
            source_conn.close()
            backup_conn.close()

    def _backup_external_db(self, backup_path: Path) -> None:
        """Backup external database (PostgreSQL, MySQL, etc.)."""
        # This would implement pg_dump, mysqldump, etc.
        # For now, just copy the database file if it exists
        shutil.copy2(self.database_path, backup_path)

    def restore_backup(self, backup_path: str) -> None:
        """Restore database from backup."""
        backup_file = Path(backup_path)

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        # Create backup of current database before restore
        current_backup = self.create_backup()
        print(f"Created safety backup: {current_backup}")

        try:
            # Stop any running applications first
            print("⚠️  Make sure to stop the application before restoring!")

            # Restore the backup
            shutil.copy2(backup_file, self.database_path)
            print(f"✅ Database restored from: {backup_path}")

        except Exception as e:
            print(f"❌ Restore failed: {e}")
            # Try to restore the safety backup
            shutil.copy2(current_backup, self.database_path)
            print("🔄 Restored safety backup")
            raise

    def list_backups(self) -> list[dict[str, Any]]:
        """List available backups."""
        backups = []

        for backup_file in self.backup_dir.glob("backup_*.db"):
            stat = backup_file.stat()
            backups.append(
                {
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime),
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                }
            )

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x["created"], reverse=True)
        return backups

    def cleanup_old_backups(self, keep_count: int = 10) -> None:
        """Remove old backup files, keeping only the most recent ones."""
        backups = self.list_backups()

        if len(backups) <= keep_count:
            print(f"📁 Found {len(backups)} backups, all within keep limit ({keep_count})")
            return

        # Remove oldest backups
        to_remove = backups[keep_count:]
        for backup in to_remove:
            backup_path = Path(backup["path"])
            backup_path.unlink()
            print(f"🗑️  Removed old backup: {backup['filename']}")

        print(f"✅ Cleaned up {len(to_remove)} old backups")

    def verify_backup(self, backup_path: str) -> bool:
        """Verify that a backup file is valid."""
        backup_file = Path(backup_path)

        if not backup_file.exists():
            print(f"❌ Backup file not found: {backup_path}")
            return False

        try:
            # For SQLite, try to open and query
            if backup_file.suffix == ".db":
                return self._verify_sqlite_backup(backup_file)
            else:
                # For other databases, check file integrity
                return backup_file.stat().st_size > 0

        except Exception as e:
            print(f"❌ Backup verification failed: {e}")
            return False

    def _verify_sqlite_backup(self, backup_file: Path) -> bool:
        """Verify SQLite backup integrity."""
        try:
            conn = sqlite3.connect(str(backup_file))
            cursor = conn.cursor()

            # Check database integrity
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()

            if result[0] == "ok":
                print(f"✅ Backup verification successful: {backup_file.name}")
                return True
            else:
                print(f"❌ Backup integrity check failed: {result[0]}")
                return False

        except Exception as e:
            print(f"❌ Backup verification error: {e}")
            return False
        finally:
            if "conn" in locals():
                conn.close()

    def optimize_database(self) -> None:
        """Optimize database performance."""
        if not self.database_path.exists():
            print(f"❌ Database not found: {self.database_path}")
            return

        try:
            if self.database_path.suffix == ".db":
                self._optimize_sqlite()
            else:
                print("Database optimization not implemented for this database type")

        except Exception as e:
            print(f"❌ Database optimization failed: {e}")

    def _optimize_sqlite(self) -> None:
        """Optimize SQLite database."""
        conn = sqlite3.connect(str(self.database_path))
        cursor = conn.cursor()

        try:
            print("🔧 Running SQLite optimization...")

            # Analyze database statistics
            cursor.execute("ANALYZE")

            # Vacuum to reclaim space and defragment
            cursor.execute("VACUUM")

            # Reindex all indexes
            cursor.execute("REINDEX")

            print("✅ SQLite optimization completed")

        finally:
            conn.close()


def main():
    """Main backup script."""
    import argparse

    parser = argparse.ArgumentParser(description="Database backup and maintenance")
    parser.add_argument("--database", default="zeta_vn/database.db", help="Database file path")
    parser.add_argument("--backup-dir", default="storage/backups/database", help="Backup directory")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Backup command
    subparsers.add_parser("backup", help="Create database backup")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore from backup")
    restore_parser.add_argument("backup_file", help="Backup file to restore from")

    # List command
    subparsers.add_parser("list", help="List available backups")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old backups")
    cleanup_parser.add_argument("--keep", type=int, default=10, help="Number of backups to keep")

    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify backup integrity")
    verify_parser.add_argument("backup_file", help="Backup file to verify")

    # Optimize command
    subparsers.add_parser("optimize", help="Optimize database")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize backup manager
    backup_manager = DatabaseBackup(args.database, args.backup_dir)

    try:
        if args.command == "backup":
            backup_path = backup_manager.create_backup()
            print(f"Backup created: {backup_path}")

        elif args.command == "restore":
            backup_manager.restore_backup(args.backup_file)

        elif args.command == "list":
            backups = backup_manager.list_backups()
            if backups:
                print(f"\n📁 Available backups ({len(backups)}):")
                print("-" * 80)
                for backup in backups:
                    size_mb = backup["size"] / (1024 * 1024)
                    print(f"{backup['filename']:<30} {size_mb:>8.2f} MB  {backup['created']}")
                print("-" * 80)
            else:
                print("No backups found")

        elif args.command == "cleanup":
            backup_manager.cleanup_old_backups(args.keep)

        elif args.command == "verify":
            is_valid = backup_manager.verify_backup(args.backup_file)
            if not is_valid:
                sys.exit(1)

        elif args.command == "optimize":
            backup_manager.optimize_database()

    except Exception as e:
        print(f"❌ Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
