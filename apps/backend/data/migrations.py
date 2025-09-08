"""Async-friendly Alembic helpers for database migrations.

This module wraps Alembic commands and SQLAlchemy async engine utilities to:
- Check migration status
- Run upgrade/downgrade
- Validate schema quickly
- Backup/restore metadata (lightweight)

Notes
- Designed for SQLAlchemy AsyncEngine; sync work is delegated via run_sync or threads.
- Keep this file minimal; domain logic must stay out of data layer.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncEngine
import Exception
import FileNotFoundError
import RuntimeError
import alembic_cfg_path
import backup_path
import bool
import conn
import dict
import e
import engine
import getattr
import int
import len
import list
import object
import pending
import result
import rev
import self
import staticmethod
import str
import sync_conn
import t
import target

try:  # Alembic is optional at runtime
    from alembic import command
    from alembic.config import Config as AlembicConfig  # type: ignore
    from alembic.script import ScriptDirectory  # type: ignore
except Exception:  # pragma: no cover - optional dep envs
    command = None  # type: ignore[assignment]
    AlembicConfig = object  # type: ignore[misc,assignment]
    ScriptDirectory = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class MigrationStatus:
    current_revision: str | None
    head_revision: str | None
    is_up_to_date: bool
    pending_migrations: list[dict[str, str]]
    pending_count: int
    checked_at: str


class DatabaseMigrator:
    """Alembic migration helper bound to an AsyncEngine."""

    def __init__(self, engine: AsyncEngine, alembic_cfg_path: str | Path) -> None:
        self.engine = engine
        self.alembic_cfg = self._load_config(alembic_cfg_path)

    # ------------------------
    # Config
    # ------------------------
    @staticmethod
    def _load_config(path: str | Path) -> Any:
        if command is None:  # alembic missing
            raise RuntimeError("Alembic is not installed in this environment")
        try:
            cfg: Any = AlembicConfig(str(path))  # type: ignore[call-arg]
        except Exception:  # pragma: no cover
            cfg = AlembicConfig()  # type: ignore[call-arg]
            cfg.config_file_name = str(path)
        return cfg

    # ------------------------
    # Core helpers
    # ------------------------
    async def get_current_revision(self) -> str | None:
        """Return current DB revision by querying alembic_version table."""
        try:
            async with self.engine.begin() as conn:
                _ = await conn.execute(text("SELECT version_num FROM alembic_version"))
                row = result.first()
                return row[0] if row else None
        except Exception:
            # Table may not exist yet; treat as uninitialized
            return None

    async def check_migration_status(self) -> dict[str, Any]:
        """Return migration status with pending revisions list."""
        current_rev = await self.get_current_revision()
        if command is None or ScriptDirectory is None:
            return {
                "current_revision": current_rev,
                "head_revision": None,
                "is_up_to_date": True,
                "pending_migrations": [],
                "pending_count": 0,
                "checked_at": datetime.now(UTC).isoformat(),
                "warning": "alembic_not_installed",
            }

        script_dir = ScriptDirectory.from_config(self.alembic_cfg)  # type: ignore[union-attr]
        head_rev = script_dir.get_current_head()  # type: ignore[union-attr]

        pending: list[dict[str, str]] = []
        if current_rev != head_rev and head_rev:
            base_rev = current_rev or "base"
            for rev in script_dir.walk_revisions(head_rev, base_rev):  # type: ignore[union-attr]
                if rev.revision != current_rev:
                    pending.append({"revision": rev.revision, "message": rev.doc or ""})

        status = MigrationStatus(
            current_revision=current_rev,
            head_revision=head_rev,
            is_up_to_date=(current_rev == head_rev),
            pending_migrations=pending,
            pending_count=len(pending),
            checked_at=datetime.now(UTC).isoformat(),
        )
        logger.info("Migration status: %s pending", status.pending_count)
        return status.__dict__

    async def upgrade(self, target: str = "head") -> None:
        if command is None:
            raise RuntimeError("Alembic not available: cannot run upgrade")

        def _run() -> None:
            command.upgrade(self.alembic_cfg, target)  # type: ignore[union-attr]

        await asyncio.to_thread(_run)

    async def downgrade(self, target: str) -> None:
        if command is None:
            raise RuntimeError("Alembic not available: cannot run downgrade")

        def _run() -> None:
            command.downgrade(self.alembic_cfg, target)  # type: ignore[union-attr]

        await asyncio.to_thread(_run)

    # ------------------------
    # Schema utilities
    # ------------------------
    async def validate_schema(self) -> dict[str, Any]:
        """Simple schema validation: list tables/views and check required set."""
        try:
            async with self.engine.begin() as conn:

                def _inspect(sync_conn):
                    insp = inspect(sync_conn)
                    return {
                        "tables": insp.get_table_names(),
                        "views": insp.get_view_names(),
                        "schemas": insp.get_schema_names(),
                    }

                info = await conn.run_sync(_inspect)

            required = ["agents", "memories", "conversations", "users"]
            missing = [t for t in required if t not in info["tables"]]

            _ = {
                "is_valid": len(missing) == 0,
                "tables_count": len(info["tables"]),
                "views_count": len(info.get("views", [])),
                "missing_tables": missing,
                "required_tables": required,
                "all_tables": info["tables"],
                "validated_at": datetime.now(UTC).isoformat(),
            }
            if result["is_valid"]:
                logger.info("Schema validation passed")
            else:
                logger.warning("Schema validation failed, missing: %s", missing)
            return result
        except Exception as e:  # pragma: no cover - best effort
            logger.error("Schema validation failed: %s", e)
            return {
                "is_valid": False,
                "error": str(e),
                "validated_at": datetime.now(UTC).isoformat(),
            }

    async def backup_schema(self, backup_path: str | Path) -> bool:
        """Lightweight backup: store table list and basic metadata as JSON."""
        try:
            async with self.engine.begin() as conn:
                _ = await conn.execute(
                    text(
                        """
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        ORDER BY table_name
                        """
                    )
                )
                tables = [row[0] for row in result.fetchall()]

            data = {
                "backup_date": datetime.now(UTC).isoformat(),
                "tables": tables,
                "table_count": len(tables),
                "engine": str(self.engine.url).split("@")[-1],  # hide creds
            }

            path = Path(backup_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            async def _write() -> None:
                import json as _json

                await asyncio.to_thread(
                    path.write_text, _json.dumps(data, indent=2), encoding="utf-8"
                )

            await _write()
            logger.info("Schema backup written to %s", path)
            return True
        except Exception as e:  # pragma: no cover
            logger.error("Schema backup failed: %s", e)
            return False

    async def restore_from_backup(self, backup_path: str | Path) -> bool:
        """Validate backup file exists and can be read (no DDL execution in demo)."""
        try:
            path = Path(backup_path)
            if not path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            import json as _json

            data = await asyncio.to_thread(path.read_text, encoding="utf-8")
            _ = _json.loads(data)  # ensure parseable
            logger.warning("Restore operation not implemented (metadata verified)")
            return True
        except Exception as e:  # pragma: no cover
            logger.error("Restore failed: %s", e)
            return False

    async def initialize_database(self) -> bool:
        """Stamp head if not initialized."""
        try:
            current = await self.get_current_revision()
            if current:
                logger.info("Database already initialized (rev=%s)", current)
                return True

            if command is None:
                logger.warning("Alembic not available; cannot initialize")
                return False

            def _stamp() -> None:
                command.stamp(self.alembic_cfg, "head")  # type: ignore[union-attr]

            await asyncio.to_thread(_stamp)
            logger.info("Database initialized (stamped head)")
            return True
        except Exception as e:  # pragma: no cover
            logger.error("Database initialization failed: %s", e)
            return False

    async def get_database_info(self) -> dict[str, Any]:
        """Basic DB info and pool stats (if available)."""
        try:
            async with self.engine.begin() as conn:
                version = (await conn.execute(text("SELECT version()"))).scalar()
                count = (
                    await conn.execute(
                        text(
                            """
                            SELECT COUNT(*)
                            FROM information_schema.tables
                            WHERE table_schema = 'public'
                            """
                        )
                    )
                ).scalar()

            pool_size = None
            checked_out = None
            try:
                pool = self.engine.sync_engine.pool  # type: ignore[attr-defined]
                pool_size = getattr(pool, "size", lambda: None)()
                checked_out = getattr(pool, "checkedout", lambda: None)()
            except Exception:
                pass

            return {
                "database_version": version,
                "table_count": count,
                "engine_url": str(self.engine.url).split("@")[-1],
                "pool_size": pool_size,
                "checked_out": checked_out,
                "retrieved_at": datetime.now(UTC).isoformat(),
            }
        except Exception as e:  # pragma: no cover
            logger.error("Failed to get database info: %s", e)
            return {"error": str(e), "retrieved_at": datetime.now(UTC).isoformat()}


# Utility functions
async def create_migrator(
    engine: AsyncEngine, alembic_cfg_path: str | Path | None = None
) -> DatabaseMigrator:
    return DatabaseMigrator(engine, alembic_cfg_path or "alembic.ini")


async def run_migrations(engine: AsyncEngine, target: str = "head") -> bool:
    try:
        migrator = await create_migrator(engine)
        await migrator.upgrade(target)
        return True
    except Exception as e:  # pragma: no cover
        logger.error("Migration run failed: %s", e)
        return False


async def check_database_health(engine: AsyncEngine) -> dict[str, Any]:
    try:
        # Basic connectivity check first
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        schema_validation = await DatabaseMigrator(
            engine, "alembic.ini"
        ).validate_schema()

        # Try to gather migration status; if alembic is missing or misconfigured,
        # treat migrations info as unavailable but do not fail the whole check.
        migration_status = None
        try:
            migrator = await create_migrator(engine)
            migration_status = await migrator.check_migration_status()
        except Exception:
            logger.info(
                "Alembic/migration status unavailable; continuing with schema check"
            )

        status = {
            "status": "healthy",
            "connection": "ok",
            "migrations": migration_status,
            "schema": schema_validation,
            "checked_at": datetime.now(UTC).isoformat(),
        }
        return status
    except Exception as e:  # pragma: no cover
        logger.error("Database health check failed: %s", e)
        return {
            "status": "unhealthy",
            "error": str(e),
            "checked_at": datetime.now(UTC).isoformat(),
        }


# Public exports
__all__ = [
    "DatabaseMigrator",
    "MigrationStatus",
    "create_migrator",
    "run_migrations",
    "check_database_health",
]
