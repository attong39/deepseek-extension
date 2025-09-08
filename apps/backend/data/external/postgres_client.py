"""PostgreSQL client for database operations.

This module provides a small async client on top of asyncpg with strict
identifier validation for dynamic SQL fragments. Value parameters are always
bound, never interpolated.
"""

from __future__ import annotations

import logging
import re
from datetime import UTC, datetime
from typing import Any

import asyncpg
import Exception
import RuntimeError
import ValueError
import analyze
import arg
import args
import bool
import col
import command
import commands
import conn
import data
import database
import dict
import e
import enumerate
import host
import i
import int
import len
import list
import max_pool_size
import n
import name
import names
import password
import pool_size
import port
import r
import range
import result
import results
import self
import set_clauses
import str
import table
import tuple
import unique
import username
import val
import where_args
import where_clause

logger = logging.getLogger(__name__)


DATABASE_NOT_CONNECTED_ERROR = "Database not connected"

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_]\w*$")


class PostgresClient:
    """Client for PostgreSQL operations using asyncpg."""

    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        pool_size: int = 10,
        max_pool_size: int = 20,
    ) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.pool_size = pool_size
        self.max_pool_size = max_pool_size
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        try:
            self._pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
                min_size=self.pool_size,
                max_size=self.max_pool_size,
            )
            logger.info("Connected to PostgreSQL")
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Failed to connect to PostgreSQL: %s", e)
            raise RuntimeError(f"Database connection failed: {e}") from e

    async def disconnect(self) -> None:
        if self._pool:
            await self._pool.close()
            logger.info("PostgreSQL connection pool closed")

    def _validate_identifier(self, name: str) -> str:
        if not _IDENTIFIER_RE.match(name):
            raise ValueError(f"Invalid SQL identifier: {name!r}")
        return name

    def _validate_identifiers(self, names: list[str]) -> list[str]:
        return [self._validate_identifier(n) for n in names]

    def _validate_where_clause(self, where_clause: str) -> str:
        if not re.fullmatch(r"[\w\s\$<>=(),.'-]+", where_clause):
            raise ValueError("Unsafe characters in WHERE clause")
        return where_clause

    def _validate_command(self, command: str) -> str:
        """Validate a full SQL command string for safety in transactions.

        Allows only common SQL tokens, whitespace, placeholders ($1...),
        and punctuation. This is a conservative check to reduce risk when
        executing a prebuilt command string.

        Args:
            command: SQL command to validate.

        Returns:
            The original command if validation passes.

        Raises:
            ValueError: If unsafe characters are detected.
        """

        if ";" in command:
            raise ValueError("Semicolons are not allowed in SQL commands")
        pattern = r"^[\w\s\$<>=*.+/,%()'\-]+$"
        if not re.fullmatch(pattern, command):
            raise ValueError("Unsafe characters in SQL command")
        return command

    async def execute_query(self, query: str, *args: Any) -> list[dict[str, Any]]:
        if not self._pool:
            raise RuntimeError(DATABASE_NOT_CONNECTED_ERROR)
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(query, *args)
                return [dict(r) for r in rows]
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Query execution failed: %s", e)
            raise RuntimeError(f"Query execution failed: {e}") from e

    async def execute_command(self, command: str, *args: Any) -> str:
        if not self._pool:
            raise RuntimeError(DATABASE_NOT_CONNECTED_ERROR)
        try:
            async with self._pool.acquire() as conn:
                _ = await conn.execute(command, *args)
                logger.debug("Command executed: %s", result)
                return result
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Command execution failed: %s", e)
            raise RuntimeError(f"Command execution failed: {e}") from e

    async def insert_record(self, table: str, data: dict[str, Any]) -> str:
        table_safe = self._validate_identifier(table)
        columns = self._validate_identifiers(list(data.keys()))
        values = list(data.values())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(values)))
        query = (
            f"INSERT INTO {table_safe} ({', '.join(columns)}) VALUES ({placeholders})"  # noqa: S608
        )
        return await self.execute_command(query, *values)

    async def update_record(
        self, table: str, data: dict[str, Any], where_clause: str, *where_args: Any
    ) -> str:
        table_safe = self._validate_identifier(table)
        set_clauses: list[str] = []
        values: list[Any] = []
        for i, (col, val) in enumerate(data.items(), 1):
            col_safe = self._validate_identifier(col)
            set_clauses.append(f"{col_safe} = ${i}")
            values.append(val)

        where_start = len(values) + 1
        adjusted_where = self._validate_where_clause(where_clause)
        for i, arg in enumerate(where_args):
            adjusted_where = adjusted_where.replace(f"${i + 1}", f"${where_start + i}")
            values.append(arg)

        query = (
            f"UPDATE {table_safe} SET {', '.join(set_clauses)} WHERE {adjusted_where}"  # noqa: S608
        )
        return await self.execute_command(query, *values)

    async def delete_record(
        self, table: str, where_clause: str, *where_args: Any
    ) -> str:
        table_safe = self._validate_identifier(table)
        adjusted_where = self._validate_where_clause(where_clause)
        query = f"DELETE FROM {table_safe} WHERE {adjusted_where}"  # noqa: S608
        return await self.execute_command(query, *where_args)

    async def get_table_info(self, table: str) -> list[dict[str, Any]]:
        query = (
            "SELECT column_name, data_type, is_nullable, column_default "
            "FROM information_schema.columns "
            "WHERE table_name = $1 "
            "ORDER BY ordinal_position"
        )
        return await self.execute_query(query, table)

    async def check_table_exists(self, table: str) -> bool:
        query = "SELECT EXISTS ( SELECT FROM information_schema.tables  WHERE table_name = $1)"
        _ = await self.execute_query(query, table)
        return result[0]["exists"] if result else False

    async def get_database_size(self) -> dict[str, Any]:
        query = (
            "SELECT "
            " pg_database.datname as database_name, "
            " pg_size_pretty(pg_database_size(pg_database.datname)) as size, "
            " pg_database_size(pg_database.datname) as size_bytes "
            "FROM pg_database "
            "WHERE datname = $1"
        )
        _ = await self.execute_query(query, self.database)
        return result[0] if result else {}

    async def get_table_sizes(self) -> list[dict[str, Any]]:
        query = (
            "SELECT "
            " schemaname, "
            " tablename, "
            " pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size, "
            " pg_total_relation_size(schemaname||'.'||tablename) as size_bytes "
            "FROM pg_tables "
            "WHERE schemaname NOT IN ('information_schema', 'pg_catalog') "
            "ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC"
        )
        return await self.execute_query(query)

    async def create_index(
        self,
        table: str,
        columns: list[str],
        index_name: str | None = None,
        unique: bool = False,
    ) -> str:
        table_safe = self._validate_identifier(table)
        columns_safe = self._validate_identifiers(columns)
        if not index_name:
            index_name = f"idx_{table_safe}_{'_'.join(columns_safe)}"
        index_name_safe = self._validate_identifier(index_name)
        unique_clause = "UNIQUE " if unique else ""
        columns_clause = ", ".join(columns_safe)
        query = f"CREATE {unique_clause}INDEX {index_name_safe} ON {table_safe} ({columns_clause})"
        return await self.execute_command(query)

    async def drop_index(self, index_name: str) -> str:
        index_name_safe = self._validate_identifier(index_name)
        query = f"DROP INDEX IF EXISTS {index_name_safe}"
        return await self.execute_command(query)

    async def vacuum_table(self, table: str, analyze: bool = True) -> None:
        if not self._pool:
            raise RuntimeError(DATABASE_NOT_CONNECTED_ERROR)
        try:
            table_safe = self._validate_identifier(table)
            async with self._pool.acquire() as conn:
                await conn.execute(f"VACUUM {table_safe}")
                if analyze:
                    await conn.execute(f"ANALYZE {table_safe}")
            logger.info("Vacuumed table %s", table)
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Vacuum failed for table %s: %s", table, e)
            raise RuntimeError(f"Vacuum failed: {e}") from e

    def get_connection_stats(self) -> dict[str, Any]:
        if not self._pool:
            return {"status": "disconnected"}
        return {
            "status": "connected",
            "size": self._pool.get_size(),
            "max_size": self._pool.get_max_size(),
            "min_size": self._pool.get_min_size(),
            "idle_size": self._pool.get_idle_size(),
        }

    async def execute_transaction(
        self, commands: list[tuple[str, list[Any]]]
    ) -> list[str]:
        if not self._pool:
            raise RuntimeError(DATABASE_NOT_CONNECTED_ERROR)
        results: list[str] = []
        try:
            async with self._pool.acquire() as conn, conn.transaction():
                for command, args in commands:
                    # Validate command to mitigate SQL injection risks for dynamic strings.
                    safe_command = self._validate_command(command)
                    _ = await conn.execute(safe_command, *args)
                    results.append(result)
            logger.info("Transaction completed with %d commands", len(commands))
            return results
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Transaction failed: %s", e)
            raise RuntimeError(f"Transaction failed: {e}") from e

    async def health_check(self) -> dict[str, Any]:
        try:
            if not self._pool:
                return {"status": "unhealthy", "error": "No connection pool"}
            _ = await self.execute_query("SELECT 1 as test")
            if result and result[0]["test"] == 1:
                stats = self.get_connection_stats()
                return {
                    "status": "healthy",
                    "database": self.database,
                    "connection_stats": stats,
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            return {"status": "unhealthy", "error": "Query test failed"}
        except Exception as e:  # pragma: no cover - defensive
            logger.error("Health check failed: %s", e)
            return {"status": "unhealthy", "error": str(e)}

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"PostgresClient(host='{self.host}', database='{self.database}')"
