#!/usr/bin/env python3
"""
Data backup automation script for Zeta AI.

Handles automated backup of PostgreSQL database, Redis cache,
file storage, and configuration data.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import redis
from pydantic import BaseSettings


class BackupSettings(BaseSettings):
    """Backup configuration settings."""

    # Database settings
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/zeta_db"
    REDIS_URL: str = "redis://localhost:6379"

    # Backup settings
    BACKUP_DIR: str = "./backups"
    RETENTION_DAYS: int = 30
    COMPRESSION_ENABLED: bool = True

    # S3 backup settings (optional)
    S3_BUCKET: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    class Config:
        env_file = ".env"


class BackupManager:
    """Manages all backup operations for Zeta AI."""

    def __init__(self, settings: BackupSettings):
        self.settings = settings
        self.backup_dir = Path(settings.BACKUP_DIR)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for backup operations."""
        logger = logging.getLogger("backup_manager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    async def backup_database(self, backup_name: str) -> bool:
        """Backup PostgreSQL database using pg_dump."""
        try:
            self.logger.info(f"Starting database backup: {backup_name}")

            # Create backup directory
            db_backup_dir = self.backup_dir / "database"
            db_backup_dir.mkdir(parents=True, exist_ok=True)

            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = db_backup_dir / f"{backup_name}_{timestamp}.sql"

            # Parse database URL
            db_url = self.settings.DATABASE_URL
            if "postgresql://" in db_url:
                db_url = db_url.replace("postgresql://", "")

            # Extract connection details
            if "@" in db_url:
                auth, host_db = db_url.split("@", 1)
                if ":" in auth:
                    username, password = auth.split(":", 1)
                else:
                    username, password = auth, ""

                if "/" in host_db:
                    host_port, database = host_db.split("/", 1)
                else:
                    host_port, database = host_db, "postgres"

                if ":" in host_port:
                    host, port = host_port.split(":", 1)
                else:
                    host, port = host_port, "5432"
            else:
                raise ValueError("Invalid database URL format")

            # Build pg_dump command
            cmd = [
                "pg_dump",
                f"--host={host}",
                f"--port={port}",
                f"--username={username}",
                f"--dbname={database}",
                "--no-password",
                "--verbose",
                "--clean",
                "--no-owner",
                "--no-privileges",
                f"--file={backup_file}",
            ]

            # Set environment for password
            env = os.environ.copy()
            if password:
                env["PGPASSWORD"] = password

            # Execute backup
            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                self.logger.info(f"Database backup completed: {backup_file}")

                # Compress if enabled
                if self.settings.COMPRESSION_ENABLED:
                    await self._compress_file(backup_file)

                return True
            else:
                self.logger.error(f"Database backup failed: {stderr.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"Database backup error: {e!s}")
            return False

    async def backup_redis(self, backup_name: str) -> bool:
        """Backup Redis data using BGSAVE."""
        try:
            self.logger.info(f"Starting Redis backup: {backup_name}")

            # Connect to Redis
            redis_client = redis.from_url(self.settings.REDIS_URL)

            # Trigger background save
            redis_client.bgsave()

            # Wait for save to complete
            while redis_client.lastsave() == redis_client.lastsave():
                await asyncio.sleep(1)

            # Create backup directory
            redis_backup_dir = self.backup_dir / "redis"
            redis_backup_dir.mkdir(parents=True, exist_ok=True)

            # Copy dump file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = redis_backup_dir / f"{backup_name}_{timestamp}.rdb"

            # Get Redis data directory (this might need adjustment)
            redis_dump_path = "/var/lib/redis/dump.rdb"  # Default Redis dump path

            if os.path.exists(redis_dump_path):
                import shutil

                shutil.copy2(redis_dump_path, backup_file)

                if self.settings.COMPRESSION_ENABLED:
                    await self._compress_file(backup_file)

                self.logger.info(f"Redis backup completed: {backup_file}")
                return True
            else:
                self.logger.warning("Redis dump file not found, using Redis SAVE command")
                redis_client.save()
                self.logger.info("Redis backup completed using SAVE command")
                return True

        except Exception as e:
            self.logger.error(f"Redis backup error: {e!s}")
            return False

    async def backup_files(self, backup_name: str, source_dirs: list[str]) -> bool:
        """Backup file storage directories."""
        try:
            self.logger.info(f"Starting file backup: {backup_name}")

            # Create backup directory
            files_backup_dir = self.backup_dir / "files"
            files_backup_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = files_backup_dir / f"{backup_name}_{timestamp}.tar.gz"

            # Create tar archive
            cmd = ["tar", "-czf", str(backup_file)]

            # Add source directories
            for source_dir in source_dirs:
                if os.path.exists(source_dir):
                    cmd.append(source_dir)
                else:
                    self.logger.warning(f"Source directory not found: {source_dir}")

            if len(cmd) > 3:  # Has source directories
                process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                    *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )

                stdout, stderr = await process.communicate()

                if process.returncode == 0:
                    self.logger.info(f"File backup completed: {backup_file}")
                    return True
                else:
                    self.logger.error(f"File backup failed: {stderr.decode()}")
                    return False
            else:
                self.logger.warning("No valid source directories found for backup")
                return False

        except Exception as e:
            self.logger.error(f"File backup error: {e!s}")
            return False

    async def _compress_file(self, file_path: Path) -> bool:
        """Compress a file using gzip."""
        try:
            cmd = ["gzip", str(file_path)]
            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                self.logger.info(f"File compressed: {file_path}.gz")
                return True
            else:
                self.logger.error(f"Compression failed: {stderr.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"Compression error: {e!s}")
            return False

    async def cleanup_old_backups(self) -> bool:
        """Remove backups older than retention period."""
        try:
            self.logger.info("Starting backup cleanup")

            cutoff_time = datetime.now().timestamp() - (self.settings.RETENTION_DAYS * 24 * 3600)

            for backup_type in ["database", "redis", "files"]:
                backup_dir = self.backup_dir / backup_type
                if backup_dir.exists():
                    for backup_file in backup_dir.iterdir():
                        if backup_file.is_file() and backup_file.stat().st_mtime < cutoff_time:
                            backup_file.unlink()
                            self.logger.info(f"Removed old backup: {backup_file}")

            self.logger.info("Backup cleanup completed")
            return True

        except Exception as e:
            self.logger.error(f"Cleanup error: {e!s}")
            return False

    async def upload_to_s3(self, backup_files: list[Path]) -> bool:
        """Upload backup files to S3 (optional)."""
        if not self.settings.S3_BUCKET:
            self.logger.info("S3 backup not configured, skipping upload")
            return True

        try:
            import boto3

            s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
            )

            for backup_file in backup_files:
                if backup_file.exists():
                    s3_key = f"zeta-ai-backups/{backup_file.name}"
                    s3_client.upload_file(str(backup_file), self.settings.S3_BUCKET, s3_key)
                    self.logger.info(f"Uploaded to S3: {s3_key}")

            return True

        except Exception as e:
            self.logger.error(f"S3 upload error: {e!s}")
            return False

    async def full_backup(self, backup_name: str | None = None) -> dict[str, bool]:
        """Perform full system backup."""
        if not backup_name:
            backup_name = f"zeta_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.logger.info(f"Starting full backup: {backup_name}")

        results = {}

        # Backup database
        results["database"] = await self.backup_database(backup_name)

        # Backup Redis
        results["redis"] = await self.backup_redis(backup_name)

        # Backup files
        file_dirs = ["./storage", "./logs", "./config", "./.env"]
        results["files"] = await self.backup_files(backup_name, file_dirs)

        # Cleanup old backups
        results["cleanup"] = await self.cleanup_old_backups()

        # Upload to S3 if configured
        if self.settings.S3_BUCKET:
            backup_files = []
            for backup_type in ["database", "redis", "files"]:
                backup_dir = self.backup_dir / backup_type
                if backup_dir.exists():
                    backup_files.extend(backup_dir.glob(f"{backup_name}*"))

            results["s3_upload"] = await self.upload_to_s3(backup_files)

        # Summary
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)

        self.logger.info(f"Backup completed: {success_count}/{total_count} operations successful")

        return results


async def main():
    """Main backup execution function."""
    try:
        settings = BackupSettings()
        backup_manager = BackupManager(settings)

        # Parse command line arguments
        import argparse

        parser = argparse.ArgumentParser(description="Zeta AI Backup Script")
        parser.add_argument("--name", help="Backup name", default=None)
        parser.add_argument("--database-only", action="store_true", help="Backup database only")
        parser.add_argument("--redis-only", action="store_true", help="Backup Redis only")
        parser.add_argument("--files-only", action="store_true", help="Backup files only")

        args = parser.parse_args()

        if args.database_only:
            result = await backup_manager.backup_database(args.name or "database_backup")
            sys.exit(0 if result else 1)
        elif args.redis_only:
            result = await backup_manager.backup_redis(args.name or "redis_backup")
            sys.exit(0 if result else 1)
        elif args.files_only:
            result = await backup_manager.backup_files(
                args.name or "files_backup",
                ["./storage", "./logs", "./config", "./.env"],
            )
            sys.exit(0 if result else 1)
        else:
            # Full backup
            results = await backup_manager.full_backup(args.name)
            success = all(results.values())
            sys.exit(0 if success else 1)

    except Exception as e:
        logging.error(f"Backup script error: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
