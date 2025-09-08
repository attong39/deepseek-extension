"""
Optimized Database Configuration for High Performance.

Implements database connection pooling and performance optimizations
following the COMPREHENSIVE_UPGRADE_PLAN.md guidelines.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
import Exception
import dict
import e
import hasattr
import int
import print
import result
import self
import session
import str
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool


class OptimizedDatabaseConfig:
    """Database configuration with performance optimizations."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def create_engine(self) -> AsyncEngine:
        """Create optimized async engine with performance tuning."""
        database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./zeta.db")

        # Performance-optimized pool configuration
        pool_size = int(os.getenv("DB_POOL_SIZE", "20"))
        max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "30"))
        pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "1800"))

        engine = create_async_engine(
            database_url,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            future=True,
        )

        return engine

    def get_engine(self) -> AsyncEngine:
        """Get or create the database engine."""
        if self._engine is None:
            self._engine = self.create_engine()
        return self._engine

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create the session factory."""
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=True,
                autocommit=False,
            )
        return self._session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session with proper cleanup."""
        session_factory = self.get_session_factory()
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def health_check(self) -> dict[str, Any]:
        """Perform database health check."""
        try:
            async with self.get_session() as session:
                _ = await session.execute(text("SELECT 1"))
                result.fetchone()

            engine = self.get_engine()
            pool = engine.pool

            # Basic pool stats (some methods may not be available on all pool types)
            pool_stats = {}
            try:
                if hasattr(pool, "size"):
                    pool_stats["pool_size"] = pool.size()
                if hasattr(pool, "checkedin"):
                    pool_stats["checked_in"] = pool.checkedin()
                if hasattr(pool, "checkedout"):
                    pool_stats["checked_out"] = pool.checkedout()
                if hasattr(pool, "overflow"):
                    pool_stats["overflow"] = pool.overflow()
            except Exception:
                pool_stats = {"error": "Pool stats unavailable"}

            return {
                "status": "healthy",
                "pool_stats": pool_stats,
                "engine_info": {
                    "dialect": engine.dialect.name
                    if hasattr(engine, "dialect")
                    else "unknown",
                },
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "pool_stats": None,
            }

    async def close(self) -> None:
        """Close all database connections."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None


# Global instance
db_config = OptimizedDatabaseConfig()


# FastAPI dependencies
async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get database session."""
    async with db_config.get_session() as session:
        yield session


def get_database_engine() -> AsyncEngine:
    """FastAPI dependency to get database engine."""
    return db_config.get_engine()


# Lifecycle management
def startup_database() -> None:
    """Initialize database connections on application startup."""
    db_config.get_engine()
    print("✅ Database connection pool initialized")


async def shutdown_database() -> None:
    """Clean up database connections on application shutdown."""
    await db_config.close()
    print("✅ Database connections closed")


def get_database_config() -> dict[str, Any]:
    """Get current database configuration."""
    return {
        "pool_size": int(os.getenv("DB_POOL_SIZE", "20")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "30")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
        "database_url": os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./zeta.db"),
    }
