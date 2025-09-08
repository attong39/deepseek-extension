#!/usr/bin/env python3
"""
Data restore automation script for Zeta AI.

Handles restoration of PostgreSQL database, Redis cache,
file storage, and configuration data from backups.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

from pydantic import BaseSettings


class RestoreSettings(BaseSettings):
    """Restore configuration settings."""

    # Database settings
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/zeta_db"
    REDIS_URL: str = "redis://localhost:6379"

    # Backup settings
    BACKUP_DIR: str = "./backups"

    # S3 restore settings (optional)
    S3_BUCKET: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    class Config:
        env_file = ".env"


class RestoreManager:
    """Manages all restore operations for Zeta AI."""

    def __init__(self, settings: RestoreSettings):
        self.settings = settings
        self.backup_dir = Path(settings.BACKUP_DIR)
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for restore operations."""
        logger = logging.getLogger("restore_manager")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def list_backups(self, backup_type: str = "all") -> dict[str, list[Path]]:
        """List available backups by type."""
        backups = {}

        if backup_type in ("all", "database"):
            db_dir = self.backup_dir / "database"
            if db_dir.exists():
                backups["database"] = sorted(db_dir.glob("*.sql*"), reverse=True)

        if backup_type in ("all", "redis"):
            redis_dir = self.backup_dir / "redis"
            if redis_dir.exists():
                backups["redis"] = sorted(redis_dir.glob("*.rdb*"), reverse=True)

        if backup_type in ("all", "files"):
            files_dir = self.backup_dir / "files"
            if files_dir.exists():
                backups["files"] = sorted(files_dir.glob("*.tar.gz*"), reverse=True)

        return backups

    def _parse_database_url(self) -> dict[str, str]:
        """Parse database URL into components."""
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

        return {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "database": database,
        }

    async def restore_database(self, backup_file: Path) -> bool:
        """Restore PostgreSQL database from backup file."""
        try:
            self.logger.info(f"Starting database restore from: {backup_file}")

            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_file}")
                return False

            # Decompress if needed
            restore_file = backup_file
            if backup_file.suffix == ".gz":
                self.logger.info("Decompressing backup file...")
                restore_file = backup_file.with_suffix("")

                cmd = ["gunzip", "-c", str(backup_file)]
                with open(restore_file, "wb") as f:
                    process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed*cmd, stdout=f, stderr=asyncio.subprocess.PIPE)
                    _, stderr = await process.communicate()

                    if process.returncode != 0:
                        self.logger.error(f"Decompression failed: {stderr.decode()}")
                        return False

            # Parse database connection
            db_config = self._parse_database_url()

            # Build psql command
            cmd = [
                "psql",
                f"--host={db_config['host']}",
                f"--port={db_config['port']}",
                f"--username={db_config['username']}",
                f"--dbname={db_config['database']}",
                "--no-password",
                f"--file={restore_file}",
            ]

            # Set environment for password
            env = os.environ.copy()
            if db_config["password"]:
                env["PGPASSWORD"] = db_config["password"]

            # Execute restore
            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            _, stderr = await process.communicate()

            # Cleanup temporary decompressed file
            if restore_file != backup_file and restore_file.exists():
                restore_file.unlink()

            if process.returncode == 0:
                self.logger.info("Database restore completed successfully")
                return True
            else:
                self.logger.error(f"Database restore failed: {stderr.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"Database restore error: {e!s}")
            return False

    async def restore_redis(self, backup_file: Path) -> bool:
        """Restore Redis data from backup file."""
        try:
            self.logger.info(f"Starting Redis restore from: {backup_file}")

            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_file}")
                return False

            # Decompress if needed
            restore_file = backup_file
            if backup_file.suffix == ".gz":
                self.logger.info("Decompressing backup file...")
                restore_file = backup_file.with_suffix("")

                cmd = ["gunzip", "-c", str(backup_file)]
                with open(restore_file, "wb") as f:
                    process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed*cmd, stdout=f, stderr=asyncio.subprocess.PIPE)
                    _, stderr = await process.communicate()

                    if process.returncode != 0:
                        self.logger.error(f"Decompression failed: {stderr.decode()}")
                        return False

            # Stop Redis service (might need adjustment for different setups)
            self.logger.info("Stopping Redis service...")
            stop_cmd = ["redis-cli", "SHUTDOWN", "NOSAVE"]

            try:
                process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                    *stop_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                await process.communicate()
            except Exception:
                self.logger.warning("Could not gracefully stop Redis")

            # Copy backup file to Redis data directory
            redis_dump_path = "/var/lib/redis/dump.rdb"  # Default Redis dump path

            import shutil

            if os.path.exists(redis_dump_path):
                # Backup current dump
                backup_current = f"{redis_dump_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(redis_dump_path, backup_current)
                self.logger.info(f"Current Redis data backed up to: {backup_current}")

            # Copy restore file
            shutil.copy2(restore_file, redis_dump_path)

            # Set proper permissions
            os.chmod(redis_dump_path, 0o640)

            # Start Redis service
            self.logger.info("Starting Redis service...")
            start_cmd = ["redis-server", "--daemonize", "yes"]

            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *start_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            _, stderr = await process.communicate()

            # Cleanup temporary decompressed file
            if restore_file != backup_file and restore_file.exists():
                restore_file.unlink()

            if process.returncode == 0:
                self.logger.info("Redis restore completed successfully")
                return True
            else:
                self.logger.error(f"Redis restore failed: {stderr.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"Redis restore error: {e!s}")
            return False

    async def restore_files(self, backup_file: Path, target_dir: str = "./") -> bool:
        """Restore files from backup archive."""
        try:
            self.logger.info(f"Starting file restore from: {backup_file}")

            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_file}")
                return False

            # Create target directory
            Path(target_dir).mkdir(parents=True, exist_ok=True)

            # Extract tar archive
            cmd = ["tar", "-xzf", str(backup_file), "-C", target_dir]

            process = await asyncio.create_subprocess_# SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: # SECURITY: exec() removed) removed) removed) removed) removed) removed) removed
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            _, stderr = await process.communicate()

            if process.returncode == 0:
                self.logger.info(f"File restore completed to: {target_dir}")
                return True
            else:
                self.logger.error(f"File restore failed: {stderr.decode()}")
                return False

        except Exception as e:
            self.logger.error(f"File restore error: {e!s}")
            return False

    def download_from_s3(self, s3_key: str, local_path: Path) -> bool:
        """Download backup file from S3."""
        if not self.settings.S3_BUCKET:
            self.logger.error("S3 not configured")
            return False

        try:
            import boto3

            s3_client = boto3.client(
                "s3",
                aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY,
            )

            # Ensure local directory exists
            local_path.parent.mkdir(parents=True, exist_ok=True)

            s3_client.download_file(self.settings.S3_BUCKET, s3_key, str(local_path))

            self.logger.info(f"Downloaded from S3: {s3_key} -> {local_path}")
            return True

        except Exception as e:
            self.logger.error(f"S3 download error: {e!s}")
            return False

    async def full_restore(self, backup_name: str, restore_config: dict[str, bool] | None = None) -> dict[str, bool]:
        """Perform full system restore."""
        if not restore_config:
            restore_config = {"database": True, "redis": True, "files": True}

        self.logger.info(f"Starting full restore: {backup_name}")

        results = {}

        # Find backup files
        backups = self.list_backups()

        # Restore database
        if restore_config.get("database", True) and "database" in backups:
            db_files = [f for f in backups["database"] if backup_name in f.name]
            if db_files:
                results["database"] = await self.restore_database(db_files[0])
            else:
                self.logger.error(f"Database backup not found for: {backup_name}")
                results["database"] = False

        # Restore Redis
        if restore_config.get("redis", True) and "redis" in backups:
            redis_files = [f for f in backups["redis"] if backup_name in f.name]
            if redis_files:
                results["redis"] = await self.restore_redis(redis_files[0])
            else:
                self.logger.error(f"Redis backup not found for: {backup_name}")
                results["redis"] = False

        # Restore files
        if restore_config.get("files", True) and "files" in backups:
            files_backups = [f for f in backups["files"] if backup_name in f.name]
            if files_backups:
                results["files"] = await self.restore_files(files_backups[0])
            else:
                self.logger.error(f"Files backup not found for: {backup_name}")
                results["files"] = False

        # Summary
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)

        self.logger.info(f"Restore completed: {success_count}/{total_count} operations successful")

        return results


async def main():
    """Main restore execution function."""
    try:
        settings = RestoreSettings()
        restore_manager = RestoreManager(settings)

        # Parse command line arguments
        import argparse

        parser = argparse.ArgumentParser(description="Zeta AI Restore Script")
        parser.add_argument("--list", action="store_true", help="List available backups")
        parser.add_argument("--backup-name", help="Backup name to restore")
        parser.add_argument("--database-file", help="Specific database backup file")
        parser.add_argument("--redis-file", help="Specific Redis backup file")
        parser.add_argument("--files-archive", help="Specific files backup archive")
        parser.add_argument("--target-dir", default="./", help="Target directory for file restore")

        args = parser.parse_args()

        if args.list:
            backups = restore_manager.list_backups()
            print("\n=== Available Backups ===")
            for backup_type, files in backups.items():
                print(f"\n{backup_type.upper()}:")
                for file in files[:10]:  # Show last 10 backups
                    print(f"  {file.name}")
            return

        if args.database_file:
            result = await restore_manager.restore_database(Path(args.database_file))
            sys.exit(0 if result else 1)
        elif args.redis_file:
            result = await restore_manager.restore_redis(Path(args.redis_file))
            sys.exit(0 if result else 1)
        elif args.files_archive:
            result = await restore_manager.restore_files(Path(args.files_archive), args.target_dir)
            sys.exit(0 if result else 1)
        elif args.backup_name:
            results = await restore_manager.full_restore(args.backup_name)
            success = all(results.values())
            sys.exit(0 if success else 1)
        else:
            parser.print_help()
            sys.exit(1)

    except Exception as e:
        logging.error(f"Restore script error: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
