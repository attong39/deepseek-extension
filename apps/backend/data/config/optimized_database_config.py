"""
Database Configuration with Optimized Connection Pooling.

High-performance database configuration implementing the patterns from
COMPREHENSIVE_UPGRADE_PLAN.md Phase 1.1.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import urlparse

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
import Exception
import connect_args
import dict
import e
import engine_config
import int
import max
import pool_config
import print
import result
import round
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
    """High-performance database configuration with connection pooling optimization."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def create_optimized_engine(self) -> AsyncEngine:
        """Create optimized async engine with performance tuning.

        Performance optimizations:
        - AsyncAdaptedQueuePool for better concurrency
        - Optimized pool sizing for high throughput
        - Connection health checks and recycling
        - Query timeout and retry policies

        Returns:
            Configured async SQLAlchemy engine.
        """
        database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./zeta.db")

        # Parse database URL to determine specific optimizations
        parsed_url = urlparse(database_url)
        is_postgres = parsed_url.scheme.startswith("postgresql")

        # Pool configuration optimized for high throughput
        pool_config: dict[str, Any] = {
            "poolclass": AsyncAdaptedQueuePool,
            "pool_size": int(os.getenv("DB_POOL_SIZE", "20")),  # Base pool size
            "max_overflow": int(
                os.getenv("DB_MAX_OVERFLOW", "30")
            ),  # Additional connections
            "pool_timeout": int(
                os.getenv("DB_POOL_TIMEOUT", "30")
            ),  # Wait time for connection
            "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),  # 30 min recycle
            "pool_pre_ping": True,  # Health check before use
        }

        # Additional engine configuration
        engine_config: dict[str, Any] = {
            "echo": os.getenv("DB_ECHO", "false").lower() == "true",
            "echo_pool": os.getenv("DB_ECHO_POOL", "false").lower() == "true",
            "future": True,  # Use SQLAlchemy 2.0 API
        }

        # PostgreSQL-specific optimizations
        if is_postgres:
            connect_args: dict[str, Any] = {
                "server_settings": {
                    "statement_timeout": "30000",  # 30 second query timeout
                    "idle_in_transaction_session_timeout": "300000",  # 5 min idle timeout
                    "application_name": "zeta_ai_app",
                }
            }
            engine_config["connect_args"] = connect_args

        # Create engine with all optimizations
        engine = create_async_engine(
            database_url,
            **pool_config,
            **engine_config,
        )

        # Add event listeners for monitoring
        self._setup_engine_events(engine)

        return engine

    def _setup_engine_events(self, engine: AsyncEngine) -> None:
        """Setup engine event listeners for monitoring and debugging."""

        @event.listens_for(engine.sync_engine, "connect")
        def on_connect(dbapi_connection: Any, connection_record: Any) -> None:
            """Event fired when a new connection is created."""
            # Add any connection-level settings here

        @event.listens_for(engine.sync_engine, "checkout")
        def on_checkout(
            dbapi_connection: Any, connection_record: Any, connection_proxy: Any
        ) -> None:
            """Event fired when a connection is checked out from the pool."""
            # Monitor connection checkout for performance metrics

        @event.listens_for(engine.sync_engine, "checkin")
        def on_checkin(dbapi_connection: Any, connection_record: Any) -> None:
            """Event fired when a connection is returned to the pool."""
            # Monitor connection checkin for performance metrics

    def get_engine(self) -> AsyncEngine:
        """Get or create the database engine."""
        if self._engine is None:
            self._engine = self.create_optimized_engine()
        return self._engine

    async def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create the session factory."""
        if self._session_factory is None:
            engine = await self.get_engine()
            self._session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,  # Keep objects usable after commit
                autoflush=True,  # Auto-flush before queries
                autocommit=False,  # Explicit transaction control
            )
        return self._session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session with proper cleanup.

        Usage:
            async with db_config.get_session() as session:
                # Use session here
                pass
        """
        session_factory = await self.get_session_factory()
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self) -> None:
        """Close all database connections."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None

    async def health_check(self) -> dict[str, Any]:
        """Perform database health check with connection pool stats.

        Returns:
            Dictionary with health status and pool statistics.
        """
        try:
            engine = await self.get_engine()

            # Test basic connectivity
            async with self.get_session() as session:
                _ = await session.execute("SELECT 1")
                await result.fetchone()

            # Get pool statistics
            pool = engine.pool
            pool_stats = {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "total_connections": pool.size() + pool.overflow(),
            }

            return {
                "status": "healthy",
                "pool_stats": pool_stats,
                "engine_info": {
                    "url": str(engine.url).replace(engine.url.password or "", "***"),
                    "dialect": engine.dialect.name,
                    "driver": engine.dialect.driver,
                },
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "pool_stats": None,
                "engine_info": None,
            }

    async def get_performance_metrics(self) -> dict[str, Any]:
        """Get detailed performance metrics for monitoring.

        Returns:
            Dictionary with performance metrics for monitoring dashboards.
        """
        health_data = await self.health_check()

        if health_data["status"] == "healthy":
            pool_stats = health_data["pool_stats"]

            # Calculate utilization percentages
            total_available = pool_stats["pool_size"] + pool_stats["overflow"]
            utilization = (pool_stats["checked_out"] / max(total_available, 1)) * 100

            return {
                "connection_utilization_percent": round(utilization, 2),
                "active_connections": pool_stats["checked_out"],
                "idle_connections": pool_stats["checked_in"],
                "total_pool_capacity": total_available,
                "overflow_connections": pool_stats["overflow"],
                "pool_efficiency": round(
                    (pool_stats["pool_size"] / max(total_available, 1)) * 100, 2
                ),
            }
        else:
            return {
                "connection_utilization_percent": 0,
                "active_connections": 0,
                "idle_connections": 0,
                "total_pool_capacity": 0,
                "overflow_connections": 0,
                "pool_efficiency": 0,
            }


# Global instance for application use
db_config = OptimizedDatabaseConfig()


# Dependency injection functions for FastAPI
async def get_database_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to get database session."""
    async with db_config.get_session() as session:
        yield session


async def get_database_engine() -> AsyncEngine:
    """FastAPI dependency to get database engine."""
    return await db_config.get_engine()


# Lifecycle management functions
async def startup_database() -> None:
    """Initialize database connections on application startup."""
    # Pre-warm the connection pool
    await db_config.get_engine()
    print("✅ Database connection pool initialized")


async def shutdown_database() -> None:
    """Clean up database connections on application shutdown."""
    await db_config.close()
    print("✅ Database connections closed")


# Configuration validation
def validate_database_config() -> dict[str, Any]:
    """Validate database configuration and return status.

    Returns:
        Configuration validation status and recommendations.
    """
    config = {
        "pool_size": int(os.getenv("DB_POOL_SIZE", "20")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "30")),
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
    }

    recommendations = []

    # Check pool sizing
    total_connections = config["pool_size"] + config["max_overflow"]
    if total_connections < 10:
        recommendations.append("Consider increasing pool size for better concurrency")
    elif total_connections > 100:
        recommendations.append("Pool size may be too large, monitor for resource usage")

    # Check timeouts
    if config["pool_timeout"] < 10:
        recommendations.append("Pool timeout may be too short for high load")
    elif config["pool_timeout"] > 60:
        recommendations.append("Pool timeout may be too long, causing delays")

    return {
        "config": config,
        "recommendations": recommendations,
        "status": "valid" if not recommendations else "needs_review",
    }
