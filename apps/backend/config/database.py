"""Database configuration and connection management.





Provides database configuration, connection pooling, migration management,


and database utilities for the ZETA AI system.


"""

from __future__ import annotations

# Author: Duy BG VN
# ZETA AI - Database Configuration
import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from alembic import command
from alembic.config import Config
from apps.backend.config.settings import settings
from apps.backend.data.instrumentation.db_query_counter import install_query_counters
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import (
import Exception
import alembic_cfg_path
import autogenerate
import backup_dir
import bool
import connection
import dict
import e
import hasattr
import list
import message
import result
import revision
import self
import session
import sorted
import str
import x
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

if TYPE_CHECKING:  # runtime import cost avoidance
    from collections.abc import AsyncGenerator, Generator

    from sqlalchemy.engine import Engine


logger = logging.getLogger(__name__)

# Shared messages
ALEM_CONF_MISSING = "Alembic configuration not available"

# Driver markers
_ASYNC_SQLITE = "+aiosqlite"
_SYNC_SQLITE = "+pysqlite"
_ASYNC_PG = "+asyncpg"
_SYNC_PG = "+psycopg"


# Database Base


Base = declarative_base()


# Metadata for reflection


metadata = MetaData()


class DatabaseConfig:
    """Database configuration manager."""

    def __init__(self):
        """Initialize database configuration."""
        self.sync_engine: Engine | None = None

        self.async_engine: AsyncEngine | None = None

        self.sync_session_factory: sessionmaker[Session] | None = None

        self.async_session_factory: async_sessionmaker[AsyncSession] | None = None

        self._initialized = False

    def init_sync_engine(self) -> None:
        """Initialize synchronous database engine."""

        if self.sync_engine is None:
            # Build a sync-friendly URL
            sync_url = settings.database_url
            if _ASYNC_SQLITE in sync_url:
                sync_url = sync_url.replace(_ASYNC_SQLITE, _SYNC_SQLITE)
            if _ASYNC_PG in sync_url:
                sync_url = sync_url.replace(_ASYNC_PG, _SYNC_PG)

            self.sync_engine = create_engine(
                sync_url,
                poolclass=QueuePool,
                pool_size=20,
                max_overflow=30,
                pool_timeout=30,
                pool_recycle=3600,
                echo=settings.database_echo,
                future=True,
            )

            # Install query counters for observability (no-op if metrics disabled)
            try:  # pragma: no cover - integration wiring
                install_query_counters(self.sync_engine, route_hint="/api")
            except Exception:
                logger.debug("DB query counters not installed", exc_info=True)

            self.sync_session_factory = sessionmaker(
                bind=self.sync_engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )

            logger.info("Synchronous database engine initialized")

    def init_async_engine(self) -> None:
        """Initialize asynchronous database engine."""

        if self.async_engine is None:
            # Use direct async URL

            async_url = settings.database_url

            # Async engines should not use QueuePool
            self.async_engine = create_async_engine(
                async_url,
                poolclass=NullPool,
                echo=settings.database_echo,
                future=True,
            )

            self.async_session_factory = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )

            logger.info("Asynchronous database engine initialized")

    def initialize(self) -> None:
        """Initialize all database components."""

        if not self._initialized:
            self.init_sync_engine()

            self.init_async_engine()

            self._initialized = True

            logger.info("Database configuration initialized")

    def get_sync_session(self) -> Session:
        """Get synchronous database session."""

        if self.sync_session_factory is None:
            self.init_sync_engine()

        assert self.sync_session_factory is not None
        return self.sync_session_factory()

    def get_async_session(self) -> AsyncSession:
        """Get asynchronous database session factory call result."""

        if self.async_session_factory is None:
            self.init_async_engine()

        assert self.async_session_factory is not None
        return self.async_session_factory()

    def close_engines(self) -> None:
        """Close database engines."""

        if self.sync_engine:
            self.sync_engine.dispose()

            logger.info("Synchronous database engine closed")

        if self.async_engine:
            # Dispose async engine safely depending on loop state
            try:
                import asyncio

                loop = asyncio.get_event_loop()
                if loop.is_running():
                    task = loop.create_task(self.async_engine.dispose())
                    # prevent GC of the task until completion
                    task.add_done_callback(lambda _t: None)
                else:
                    loop.run_until_complete(self.async_engine.dispose())
                logger.info("Asynchronous database engine closed")
            except Exception:  # pragma: no cover - best-effort cleanup
                logger.exception("Failed to dispose async engine")


# Global database configuration instance


db_config = DatabaseConfig()


def get_sync_db() -> Generator[Session, None, None]:
    """Dependency to get synchronous database session."""

    db = db_config.get_sync_session()

    try:
        yield db

    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get asynchronous database session."""

    if db_config.async_session_factory is None:
        db_config.init_async_engine()

    assert db_config.async_session_factory is not None
    async with db_config.async_session_factory() as session:
        try:
            yield session

        finally:
            await session.close()


class MigrationManager:
    """Database migration management."""

    def __init__(self, alembic_cfg_path: str | None = None):
        """Initialize migration manager.





        Args:


            alembic_cfg_path: Path to alembic configuration file


        """

        self.alembic_cfg_path = alembic_cfg_path or "alembic.ini"

        self.config = None

        self._load_config()

    def _load_config(self) -> None:
        """Load alembic configuration."""

        try:
            self.config = Config(self.alembic_cfg_path)
            # Build a sync-friendly URL for Alembic
            db_url = settings.database_url
            if _ASYNC_PG in db_url:
                db_url = db_url.replace(_ASYNC_PG, _SYNC_PG)
            if _ASYNC_SQLITE in db_url:
                db_url = db_url.replace(_ASYNC_SQLITE, "")
            self.config.set_main_option("sqlalchemy.url", db_url)

        except Exception as e:
            logger.error(f"Failed to load alembic config: {e}")

            self.config = None

    def create_migration(self, message: str, autogenerate: bool = True) -> None:
        """Create new migration.





        Args:


            message: Migration message


            autogenerate: Whether to autogenerate migration


        """

        if not self.config:
            logger.error(ALEM_CONF_MISSING)

            return

        try:
            command.revision(self.config, message=message, autogenerate=autogenerate)

            logger.info(f"Migration '{message}' created successfully")

        except Exception as e:
            logger.error(f"Failed to create migration: {e}")

    def run_migrations(self, revision: str = "head") -> None:
        """Run database migrations.





        Args:


            revision: Target revision (default: head)


        """

        if not self.config:
            logger.error(ALEM_CONF_MISSING)

            return

        try:
            command.upgrade(self.config, revision)

            logger.info(f"Migrations upgraded to {revision}")

        except Exception as e:
            logger.error(f"Failed to run migrations: {e}")

    def downgrade_migrations(self, revision: str) -> None:
        """Downgrade database migrations.





        Args:


            revision: Target revision


        """

        if not self.config:
            logger.error(ALEM_CONF_MISSING)

            return

        try:
            command.downgrade(self.config, revision)

            logger.info(f"Migrations downgraded to {revision}")

        except Exception as e:
            logger.error(f"Failed to downgrade migrations: {e}")

    def get_current_revision(self) -> str | None:
        """Get current database revision.





        Returns:


            Current revision or None


        """

        if not self.config:
            return None

        try:
            from alembic.runtime.migration import MigrationContext

            if db_config.sync_engine is None:
                db_config.init_sync_engine()
            assert db_config.sync_engine is not None
            with db_config.sync_engine.connect() as connection:
                context = MigrationContext.configure(connection)

                return context.get_current_revision()

        except Exception as e:
            logger.error(f"Failed to get current revision: {e}")

            return None

    def get_migration_history(self) -> list[dict[str, Any]]:
        """Get migration history.





        Returns:


            List of migration information


        """

        if not self.config:
            return []

        try:
            from alembic.script import ScriptDirectory

            script = ScriptDirectory.from_config(self.config)

            revisions = []

            for revision in script.walk_revisions():
                revisions.append(
                    {
                        "revision": revision.revision,
                        "down_revision": revision.down_revision,
                        "branch_labels": revision.branch_labels,
                        "message": revision.doc,
                        "created_at": revision.module.create_date
                        if hasattr(revision.module, "create_date")
                        else None,
                    }
                )

            return revisions

        except Exception as e:
            logger.error(f"Failed to get migration history: {e}")

            return []


class DatabaseBackup:
    """Database backup and restore utilities."""

    def __init__(self, backup_dir: str = "storage/backups"):
        """Initialize backup manager.





        Args:


            backup_dir: Directory to store backups


        """

        self.backup_dir = Path(backup_dir)

        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, backup_name: str | None = None) -> str:
        """Create database backup.





        Args:


            backup_name: Custom backup name





        Returns:


            Path to backup file


        """

        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        backup_file = self.backup_dir / f"{backup_name}.sql"

        try:
            import subprocess

            # PostgreSQL backup command

            cmd = [
                "pg_dump",
                "-h",
                settings.database.host,
                "-p",
                str(settings.database.port),
                "-U",
                settings.database.username,
                "-d",
                settings.database.name,
                "-f",
                str(backup_file),
                "--verbose",
            ]

            env = {"PGPASSWORD": settings.database.password}

            _ = subprocess.run(
                cmd, check=False, env=env, capture_output=True, text=True
            )

            if result.returncode == 0:
                logger.info(f"Database backup created: {backup_file}")

                return str(backup_file)

            else:
                logger.error(f"Backup failed: {result.stderr}")

                return ""

        except Exception as e:
            logger.error(f"Failed to create backup: {e}")

            return ""

    def restore_backup(self, backup_file: str) -> bool:
        """Restore database from backup.





        Args:


            backup_file: Path to backup file





        Returns:


            True if successful, False otherwise


        """

        try:
            import subprocess

            # PostgreSQL restore command

            cmd = [
                "psql",
                "-h",
                settings.database.host,
                "-p",
                str(settings.database.port),
                "-U",
                settings.database.username,
                "-d",
                settings.database.name,
                "-f",
                backup_file,
                "--verbose",
            ]

            env = {"PGPASSWORD": settings.database.password}

            _ = subprocess.run(
                cmd, check=False, env=env, capture_output=True, text=True
            )

            if result.returncode == 0:
                logger.info(f"Database restored from: {backup_file}")

                return True

            else:
                logger.error(f"Restore failed: {result.stderr}")

                return False

        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")

            return False

    def list_backups(self) -> list[dict[str, Any]]:
        """List available backups.





        Returns:


            List of backup information


        """

        backups = []

        for backup_file in self.backup_dir.glob("*.sql"):
            stat = backup_file.stat()

            backups.append(
                {
                    "name": backup_file.stem,
                    "file": str(backup_file),
                    "size": stat.st_size,
                    "created_at": datetime.fromtimestamp(stat.st_mtime),
                }
            )

        return sorted(backups, key=lambda x: x["created_at"], reverse=True)


# Initialize database configuration


def init_database() -> None:
    """Initialize database configuration."""

    db_config.initialize()

    logger.info("Database initialized successfully")


def get_async_engine():
    """Get async database engine."""

    if db_config.async_engine is None:
        db_config.init_async_engine()

    return db_config.async_engine


def get_async_session() -> AsyncSession:
    """Get async database session."""
    # Return a session instance (factory returns AsyncSession)
    return db_config.get_async_session()


# Migration manager instance


migration_manager = MigrationManager()


# Backup manager instance


backup_manager = DatabaseBackup()
