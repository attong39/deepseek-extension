"""Unified database service for consistent database access.



This service provides a single point of truth for database operations,

replacing the mixed pattern of direct engine access and session injection.

"""


# TODO: Use DatabaseInterface from core.interfaces for DI

from __future__ import annotations

import logging
from functools import lru_cache
from typing import TYPE_CHECKING, TypeVar
import Exception
import RuntimeError
import args
import bool
import conn
import e
import kwargs
import operation
import property
import self
import session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


logger = logging.getLogger(__name__)


T = TypeVar("T")


class DatabaseService:
    """Unified database service for consistent database access across the application."""

    def __init__(self):
        """Initialize database service with lazy loading."""

        self._engine = None

        self._session_maker = None

        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Ensure database is initialized."""

        if not self._initialized:
            self._initialize()

    def _initialize(self) -> None:
        """Initialize database engine and session maker."""

        try:
            from apps.backend.data.models.base import get_engine

            self._engine = get_engine()

            if self._engine is None:
                raise RuntimeError("Database engine could not be initialized")

            # Get the session maker from base module

            from apps.backend.data.models.base import (
                async_session_maker as base_session_maker,
            )

            if base_session_maker is None:
                # Initialize it if not already done

                from apps.backend.data.models.base import initialize_database

                initialize_database()

                from apps.backend.data.models.base import (
                    async_session_maker as base_session_maker,
                )

            self._session_maker = base_session_maker

            self._initialized = True

            logger.info("✅ DatabaseService initialized successfully")

        except Exception as e:
            logger.error(f"❌ DatabaseService initialization failed: {e}")

            raise

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.



        This is the UNIFIED way to get database sessions.

        All repositories and services should use this method.



        Yields:

            AsyncSession: Database session

        """

        self._ensure_initialized()

        if self._session_maker is None:
            raise RuntimeError("Session maker not initialized")

        async with self._session_maker() as session:
            try:
                yield session

            except Exception as e:
                await session.rollback()

                logger.error(f"Database session error: {e}")

                raise

            finally:
                await session.close()

    async def execute_in_session(self, operation, *args, **kwargs):
        """Execute operation in a database session.



        Args:

            operation: Async function to execute with session as first argument

            *args: Additional arguments for operation

            **kwargs: Additional keyword arguments for operation



        Returns:

            Result of operation

        """

        async for session in self.get_session():
            return await operation(session, *args, **kwargs)

    async def health_check(self) -> bool:
        """Check database health.



        Returns:

            True if database is healthy

        """

        try:
            self._ensure_initialized()

            if self._engine is None:
                return False

            from sqlalchemy import text

            async with self._engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            return True

        except Exception as e:
            logger.error(f"Database health check failed: {e}")

            return False

    async def create_tables(self) -> None:
        """Create all database tables."""

        try:
            # Delegate to the initializer to avoid importing Base here

            from apps.backend.config.settings import get_settings
            from apps.backend.data.database_init import DatabaseInitializer

            settings = get_settings()

            initializer = DatabaseInitializer(settings.database_url)

            success = await initializer.create_tables()

            if not success:
                raise RuntimeError("Failed to create tables via initializer")

        except Exception as e:
            logger.error(f"❌ Failed to create database tables: {e}")

            raise

    async def drop_tables(self) -> None:
        """Drop all database tables."""

        try:
            # Delegate to the initializer to avoid importing Base here

            from apps.backend.config.settings import get_settings
            from apps.backend.data.database_init import DatabaseInitializer

            settings = get_settings()

            initializer = DatabaseInitializer(settings.database_url)

            success = await initializer.drop_tables()

            if not success:
                raise RuntimeError("Failed to drop tables via initializer")

        except Exception as e:
            logger.error(f"❌ Failed to drop database tables: {e}")

            raise

    def get_engine(self):
        """Get database engine.



        Note: Prefer using get_session() for most operations.

        Only use direct engine access for advanced operations.



        Returns:

            Database engine

        """

        self._ensure_initialized()

        return self._engine

    @property
    def is_initialized(self) -> bool:
        """Check if database service is initialized."""

        return self._initialized


@lru_cache(maxsize=1)
def get_database_service() -> DatabaseService:
    """Get a process-wide database service singleton.

    Uses an LRU cache instead of a mutable global (avoids PLW0603). Clear via
    ``get_database_service.cache_clear()`` in tests.
    """

    return DatabaseService()


# Convenience function for dependency injection


async def get_db_session_unified() -> AsyncGenerator[AsyncSession, None]:
    """Get database session via unified service.



    This is the recommended way to get database sessions for dependency injection.



    Yields:

        AsyncSession: Database session

    """

    db_service = get_database_service()

    async for session in db_service.get_session():
        yield session
