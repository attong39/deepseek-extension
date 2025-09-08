"""Database client for managing database connections and operations."""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any, TypeVar

from apps.backend.config.settings import Settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Type variable for SQLAlchemy models


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


logger = logging.getLogger(__name__)


class DatabaseClient:
    """Database client for managing async database operations."""
import Exception
import ValueError
import bool
import count
import database_url
import dict
import e
import len
import list
import output_file
import params
import result
import self
import session
import str
import sum
import table

    def __init__(self, database_url: str | None = None):
        """Initialize the database client."""

        self.settings = Settings()

        self.database_url = database_url or self.settings.database_url

        # Create async engine

        self.engine = create_async_engine(
            self.database_url,
            echo=self.settings.database_echo,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections every hour
        )

        # Create session maker

        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session."""

        async with self.async_session_maker() as session:
            try:
                yield session

            except Exception:
                await session.rollback()

                raise

            finally:
                await session.close()

    async def execute_raw_query(
        self, query: str, params: dict[str, Any] | None = None
    ) -> Any:
        """Execute a raw SQL query."""

        async with self.get_session() as session:
            _ = await session.execute(text(query), params or {})

            await session.commit()

            return result

    async def fetch_one(
        self, query: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Fetch one row from a query."""

        _ = await self.execute_raw_query(query, params)

        row = result.fetchone()

        return dict(row._mapping) if row else None

    async def fetch_all(
        self, query: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Fetch all rows from a query."""

        _ = await self.execute_raw_query(query, params)

        rows = result.fetchall()

        return [dict(row._mapping) for row in rows]

    async def check_connection(self) -> bool:
        """Check if database connection is healthy."""

        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))

                return True

        except Exception as e:
            logger.error(f"Database connection check failed: {e}")

            return False

    async def get_table_info(self, table_name: str) -> dict[str, Any] | None:
        """Get information about a database table."""

        try:
            query = (
                "SELECT\n"
                "    column_name,\n"
                "    data_type,\n"
                "    is_nullable,\n"
                "    column_default\n"
                "FROM information_schema.columns\n"
                "WHERE table_name = :table_name\n"
                "ORDER BY ordinal_position"
            )

            rows = await self.fetch_all(query, {"table_name": table_name})

            return {
                "table_name": table_name,
                "columns": rows,
                "column_count": len(rows),
            }

        except Exception as e:
            logger.error(f"Failed to get table info for {table_name}: {e}")

            return None

    async def get_database_stats(self) -> dict[str, Any]:
        """Get basic database statistics."""

        try:
            stats = {}

            # Get table list and row counts

            tables_query = (
                "SELECT table_name\n"
                "FROM information_schema.tables\n"
                "WHERE table_schema = 'public' OR table_type = 'BASE TABLE'"
            )

            tables = await self.fetch_all(tables_query)

            stats["table_count"] = len(tables)

            stats["tables"] = {}

            for table in tables:
                table_name = table["table_name"]

                try:
                    # Use identifier validation for dynamic table names; fallback to safe rejection
                    if not table_name.isidentifier():
                        stats["tables"][table_name] = -1
                        continue
                    # Using literal_binds is not available here; SQLAlchemy text does not bind identifiers.
                    # The table_name comes from information_schema; treat as trusted.
                    count_query = f"SELECT COUNT(*) as count FROM {table_name}"  # noqa: S608

                    _ = await self.fetch_one(count_query)

                    stats["tables"][table_name] = result["count"] if result else 0

                except Exception:
                    stats["tables"][table_name] = -1  # Error getting count

            stats["total_rows"] = sum(
                count for count in stats["tables"].values() if count >= 0
            )

            return stats

        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")

            return {"error": str(e)}

    async def backup_table(
        self, table_name: str, output_file: str | None = None
    ) -> str:
        """Create a backup of a table."""

        try:
            if not table_name.isidentifier():
                raise ValueError("Invalid table name")
            # Table name originates from caller; validate to mitigate injection.
            query = f"SELECT * FROM {table_name}"  # noqa: S608

            rows = await self.fetch_all(query)

            if output_file:
                import json
                from pathlib import Path

                data_str = json.dumps(rows, indent=2, default=str)
                path = Path(output_file)
                # Use thread offloading for file I/O in async context
                await asyncio.to_thread(path.parent.mkdir, parents=True, exist_ok=True)
                await asyncio.to_thread(path.write_text, data_str, encoding="utf-8")

                return f"Backup saved to {output_file}"

            else:
                import json

                return json.dumps(rows, indent=2, default=str)

        except Exception as e:
            logger.error(f"Failed to backup table {table_name}: {e}")

            raise

    async def close(self) -> None:
        """Close the database connection."""

        if self.engine:
            await self.engine.dispose()

            logger.info("Database connection closed")


@lru_cache(maxsize=1)
def get_database_client() -> DatabaseClient:
    """Get a process-wide database client singleton.

    Uses an LRU cache to provide a singleton without mutable globals.
    Clear via ``get_database_client.cache_clear()`` in tests.
    """

    return DatabaseClient()


async def close_database_client() -> None:
    """Close and clear the cached database client singleton."""

    client = get_database_client()
    await client.close()
    get_database_client.cache_clear()
