"""
Async database configuration for ZETA_VN.

Features:
- AsyncPG connection pooling
- Prepared statement support
- Connection health checks
- Query performance monitoring
- Integrated logging for monitoring and debugging
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.pool import QueuePool
import Exception
import RuntimeError
import ValueError
import bool
import database_url
import e
import echo
import float
import int
import isinstance
import max_overflow
import pool_size
import pool_timeout
import self
import str

# Assuming project's standard logger; adjust if different
logger = logging.getLogger(__name__)


class AsyncDatabaseConfig:
    """
    Asynchronous database configuration for ZETA_VN.

    This class handles the setup and management of an asynchronous database engine
    using SQLAlchemy, with features like connection pooling, health checks, and
    performance monitoring.

    Attributes:
        database_url (str): The database connection URL.
        engine (AsyncEngine | None): The SQLAlchemy async engine instance.
        session_factory (async_sessionmaker[AsyncSession] | None): Factory for creating async sessions.
    """

    def __init__(self, database_url: str) -> None:
        """
        Initialize the AsyncDatabaseConfig with a database URL.

        Args:
            database_url (str): The database connection URL. Must be a valid URL string.

        Raises:
            ValueError: If database_url is empty or invalid.
        """
        if not database_url or not isinstance(database_url, str):
            raise ValueError("database_url must be a non-empty string")
        self.database_url = database_url
        self.engine: AsyncEngine | None = None
        self.session_factory: async_sessionmaker[AsyncSession] | None = None
        logger.info("AsyncDatabaseConfig initialized with database URL")

    def init_engine(
        self,
        pool_size: int = 20,
        max_overflow: int = 20,
        pool_timeout: float = 30.0,
        echo: bool = False,
    ) -> None:
        """
        Initialize the asynchronous database engine.

        Args:
            pool_size (int): Number of permanent connections in the pool. Defaults to 20.
            max_overflow (int): Maximum number of temporary connections beyond pool_size. Defaults to 20.
            pool_timeout (float): Seconds to wait before giving up on getting a connection. Defaults to 30.0.
            echo (bool): If True, log all SQL statements to stdout for debugging. Defaults to False.

        Raises:
            ValueError: If pool_size or max_overflow are negative, or pool_timeout is non-positive.
        """
        if pool_size < 0 or max_overflow < 0:
            raise ValueError("pool_size and max_overflow must be non-negative")
        if pool_timeout <= 0:
            raise ValueError("pool_timeout must be positive")

        try:
            self.engine = create_async_engine(
                self.database_url,
                poolclass=QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_pre_ping=True,  # Check connection health before use
                pool_recycle=3600,   # Recycle connections after 1 hour to prevent stale connections
                echo=echo,
            )
            self.session_factory = async_sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )
            logger.info("Database engine initialized successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """
        Get an asynchronous database session as a context manager.

        This method provides a session that automatically handles commit and rollback
        on exit, ensuring safe transaction management.

        Yields:
            AsyncSession: An asynchronous database session.

        Raises:
            RuntimeError: If the engine has not been initialized.

        Example:
            async with db.get_session() as session:
                result = await session.execute(query)
                await session.commit()  # Optional, as it's handled automatically
        """
        if self.session_factory is None:
            raise RuntimeError("Database engine not initialized. Call init_engine() first")

        session = self.session_factory()
        logger.debug("Database session created")
        try:
            yield session
            await session.commit()
            logger.debug("Database session committed successfully")
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rolled back due to error: {e}")
            raise
        finally:
            await session.close()
            logger.debug("Database session closed")

    async def dispose_engine(self) -> None:
        """
        Dispose of the database engine and clean up resources.

        This method should be called when the application is shutting down
        to ensure all connections are properly closed.

        Raises:
            RuntimeError: If the engine has not been initialized.
        """
        if self.engine is None:
            raise RuntimeError("Database engine not initialized")
        try:
            await self.engine.dispose()
            logger.info("Database engine disposed successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to dispose database engine: {e}")
            raise
