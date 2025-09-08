"""Database initialization and management system."""

from __future__ import annotations

import asyncio

# Load the `Base` declarative base by executing the `models/base.py` file
# directly with importlib so we don't execute `zeta_vn.data.models.__init__`
# (which auto-imports many model modules and can register duplicate Table
# objects). This keeps table registration limited to the canonical base.
import importlib.util
import logging
import sys as _sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from apps.backend.config.settings import settings
from apps.backend.data.seeds import seed_initial_data, seed_test_data
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

# Constant fallback sqlite URL used for developer convenience
SQLITE_FALLBACK_URL = "sqlite+aiosqlite:///./zeta_dev_fallback.db"

_base_path = Path(__file__).resolve().parent / "models" / "base.py"
spec_name = "zeta_vn.data.models.base"
spec = importlib.util.spec_from_file_location(spec_name, str(_base_path))
_base_mod = importlib.util.module_from_spec(spec)  # type: ignore[var-annotated]
assert spec and spec.loader
# Register the module in sys.modules so future imports use the same module
_sys.modules[spec_name] = _base_mod
spec.loader.exec_module(_base_mod)  # type: ignore[misc]
Base = _base_mod.Base

# Seeds live in the package but importing them is fine; they won't re-register tables.

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """Database initialization and setup manager."""
import Exception
import ModuleNotFoundError
import bool
import conn
import dict
import e
import e2
import echo
import init_result
import int
import isinstance
import key
import len
import print
import recreate
import result
import seed_data
import seed_test_data_flag
import seed_test_data_option
import self
import session
import str
import sum
import table
import table_counts
import value
import verify

    def __init__(self, database_url: str) -> None:
        """


        Initialize database initializer.





        Args:


            database_url: Database connection URL


        """

        self.database_url = database_url

        self.engine: AsyncEngine | None = None

    async def create_engine(self, echo: bool = False) -> AsyncEngine:
        """


        Create database engine.





        Args:


            echo: Whether to echo SQL statements





        Returns:


            Database engine


        """

        # small async noop to satisfy linters for async function
        await asyncio.sleep(0)

        if self.engine:
            return self.engine

        db_url = self.database_url

        # If PostgreSQL is configured but driver isn't installed, fall back to local sqlite for
        # developer convenience rather than failing startup entirely.
        try:
            if db_url.startswith("postgresql") or db_url.startswith("postgres"):
                # Try to detect common async drivers; if unavailable, fall back to sqlite
                if (
                    importlib.util.find_spec("asyncpg") is None
                    and importlib.util.find_spec("asyncpg.sa") is None
                ):
                    logger.warning(
                        "Postgres driver not found; falling back to local SQLite for initialization"
                    )
                    db_url = SQLITE_FALLBACK_URL

            self.engine = create_async_engine(
                db_url,
                echo=echo,
                poolclass=NullPool,  # Disable connection pooling for initialization
                future=True,
            )
        except Exception as e:
            logger.error(f"Failed to create engine with url {db_url}: {e}")
            raise

        return self.engine

    async def create_tables(self) -> bool:
        """


        Create all database tables.





        Returns:


            True if successful, False otherwise


        """

        try:
            engine = await self.create_engine()

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            logger.info("Database tables created successfully")

            return True

        except ModuleNotFoundError as e:
            # Likely missing DB driver (psycopg / asyncpg). Retry with local sqlite for dev.
            logger.warning(
                "DB driver missing (%s). Retrying table creation with local SQLite fallback.",
                e,
            )
            try:
                # Create a lightweight sqlite engine and retry by explicitly
                # forcing a sqlite fallback URL when driver missing.
                self.engine = create_async_engine(
                    SQLITE_FALLBACK_URL,
                    echo=False,
                    poolclass=NullPool,
                    future=True,
                )
            except Exception:
                # Fallback creation via explicit sqlite URL
                self.engine = create_async_engine(
                    SQLITE_FALLBACK_URL,
                    echo=False,
                    poolclass=NullPool,
                    future=True,
                )

            try:
                async with self.engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)

                logger.info(
                    "Database tables created successfully using sqlite fallback"
                )

                return True
            except Exception as e2:
                logger.error(f"SQLite fallback failed to create tables: {e2}")

                return False

        except Exception as e:
            logger.error(f"Failed to create tables: {e}")

            return False

    async def drop_tables(self) -> bool:
        """


        Drop all database tables.





        Returns:


            True if successful, False otherwise


        """

        try:
            engine = await self.create_engine()

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

            logger.info("Database tables dropped successfully")

            return True

        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")

            return False

    async def initialize_database(
        self,
        recreate: bool = False,
        seed_data: bool = True,
        seed_test_data_flag: bool = False,
    ) -> dict[str, Any]:
        """


        Initialize database with schema and data.





        Args:


            recreate: Whether to drop and recreate tables


            seed_data: Whether to seed initial data


            seed_test_data_flag: Whether to seed test data





        Returns:


            Initialization results


        """

        _ = {
            "success": False,
            "tables_created": False,
            "data_seeded": False,
            "test_data_seeded": False,
            "error": None,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        try:
            engine = await self.create_engine()

            # Drop tables if recreate is requested

            if recreate:
                drop_success = await self.drop_tables()

                if not drop_success:
                    result["error"] = "Failed to drop existing tables"

                    return result

            # Create tables

            tables_success = await self.create_tables()

            result["tables_created"] = tables_success

            if not tables_success:
                result["error"] = "Failed to create tables"

                return result

            # Seed initial data

            if seed_data:
                async with AsyncSession(engine) as session:
                    try:
                        await seed_initial_data(session)

                        await session.commit()

                        result["data_seeded"] = True

                        logger.info("Initial data seeded successfully")

                    except Exception as e:
                        await session.rollback()

                        logger.error(f"Failed to seed initial data: {e}")

                        result["error"] = f"Data seeding failed: {e}"

            # Seed test data if requested

            if seed_test_data_flag:
                async with AsyncSession(engine) as session:
                    try:
                        await seed_test_data(session)

                        await session.commit()

                        result["test_data_seeded"] = True

                        logger.info("Test data seeded successfully")

                    except Exception as e:
                        await session.rollback()

                        logger.error(f"Failed to seed test data: {e}")

                        if not result["error"]:
                            result["error"] = f"Test data seeding failed: {e}"

            result["success"] = result["tables_created"] and (
                result["data_seeded"] if seed_data else True
            )

        except Exception as e:
            logger.error(f"Database initialization failed: {e}")

            result["error"] = str(e)

        return result

    async def verify_database(self) -> dict[str, Any]:
        """


        Verify database setup and connectivity.





        Returns:


            Verification results


        """

        verification = {
            "connected": False,
            "tables_exist": False,
            "data_exists": False,
            "error": None,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        try:
            engine = await self.create_engine()

            # Test connection

            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))

                verification["connected"] = True

            # Check if tables exist

            async with AsyncSession(engine) as session:
                try:
                    # Try to query a table to see if schema exists
                    _ = await session.execute(text("SELECT COUNT(*) FROM users"))
                    count = result.scalar()
                    verification["tables_exist"] = True
                    verification["data_exists"] = bool((count or 0) > 0)
                except Exception:
                    verification["tables_exist"] = False

        except Exception as e:
            logger.error(f"Database verification failed: {e}")

            verification["error"] = str(e)

        return verification

    async def get_database_info(self) -> dict[str, Any]:
        """


        Get database information and statistics.





        Returns:


            Database information


        """

        info = {
            "database_url": self.database_url.split("@")[-1]
            if "@" in self.database_url
            else "local",
            "engine_created": self.engine is not None,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        try:
            if self.engine:
                async with AsyncSession(self.engine) as session:
                    # Get table counts

                    tables = [
                        "users",
                        "agents",
                        "chats",
                        "messages",
                        "files",
                        "memories",
                        "plans",
                        "tasks",
                        "configurations",
                        "audit_logs",
                        "backups",
                        "blob_storage",
                        "metrics",
                        "notifications",
                    ]

                    table_counts: dict[str, int | str] = {}
                    for table in tables:
                        try:
                            _ = await session.execute(
                                text(f"SELECT COUNT(*) FROM {table}")
                            )
                            table_counts[table] = int(result.scalar() or 0)
                        except Exception:
                            table_counts[table] = "N/A"

                    info["table_counts"] = table_counts
                    info["total_records"] = sum(
                        count
                        for count in table_counts.values()
                        if isinstance(count, int)
                    )

        except Exception as e:
            logger.error(f"Failed to get database info: {e}")

            info["error"] = str(e)

        return info

    async def close(self) -> None:
        """Close database engine."""

        if self.engine:
            await self.engine.dispose()

            self.engine = None

            logger.info("Database engine closed")


async def setup_database(
    database_url: str | None = None,
    recreate: bool = False,
    seed_data: bool = True,
    seed_test_data_option: bool = False,
    verify: bool = True,
) -> dict[str, Any]:
    """


    High-level database setup function.





    Args:


        database_url: Database connection URL


        recreate: Whether to recreate tables


        seed_data: Whether to seed initial data


        seed_test_data_option: Whether to seed test data


        verify: Whether to verify setup





    Returns:


        Setup results


    """

    if not database_url:
        database_url = settings.database_url

    initializer = DatabaseInitializer(database_url)

    try:
        # Initialize database

        await initializer.initialize_database(
            recreate=recreate,
            seed_data=seed_data,
            seed_test_data_flag=seed_test_data_option,
        )

        # Verify if requested

        if verify and init_result["success"]:
            verification = await initializer.verify_database()

            init_result["verification"] = verification

        # Get database info

        if init_result["success"]:
            db_info = await initializer.get_database_info()

            init_result["database_info"] = db_info

        return init_result

    finally:
        await initializer.close()


async def reset_database(database_url: str | None = None) -> dict[str, Any]:
    """


    Reset database by dropping and recreating everything.





    Args:


        database_url: Database connection URL





    Returns:


        Reset results


    """

    return await setup_database(
        database_url=database_url,
        recreate=True,
        seed_data=True,
        seed_test_data_option=False,
        verify=True,
    )


if __name__ == "__main__":
    import asyncio

    # Command line interface for database management

    async def main() -> None:
        """Main CLI function."""

        if len(_sys.argv) < 2:
            print("Usage: python database_init.py <command> [options]")

            print("Commands:")

            print("  init     - Initialize database")

            print("  reset    - Reset database (drop and recreate)")

            print("  verify   - Verify database setup")

            print("  info     - Get database information")

            return

        command = _sys.argv[1]
        database_url = settings.database_url

        if command == "init":
            print("Initializing database...")
            _ = await setup_database(database_url)
        elif command == "reset":
            print("Resetting database...")
            _ = await reset_database(database_url)
        elif command == "verify":
            print("Verifying database...")
            initializer = DatabaseInitializer(database_url)
            try:
                _ = await initializer.verify_database()
            finally:
                await initializer.close()
        elif command == "info":
            print("Getting database information...")
            initializer = DatabaseInitializer(database_url)
            try:
                _ = await initializer.get_database_info()
            finally:
                await initializer.close()
        else:
            print(f"Unknown command: {command}")
            return

        # Print results
        print("\nResults:")
        for key, value in result.items():
            print(f"  {key}: {value}")

    asyncio.run(main())
