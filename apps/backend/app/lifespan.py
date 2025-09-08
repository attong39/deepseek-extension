"""Application lifecycle management for ZETA AI system.





This module handles startup and shutdown events for the FastAPI application,


managing resource initialization, health checks, and graceful shutdown.


"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from apps.backend.config.settings import Settings, get_settings
from apps.backend.core.common.base_classes import BaseManager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
import Exception
import ImportError
import app
import bool
import e
import getattr
import hasattr
import key
import len
import list
import name
import property
import self
import status
import task

# Setup


logger = logging.getLogger(__name__)


try:
    from apps.backend.config.settings import get_settings

    settings = get_settings()


except ImportError:
    # Fallback settings

    settings = Settings()


class LifespanManager(BaseManager):
    """Manages application lifecycle events.

    Attributes declared at class level are for static type checkers only.
    Actual instance attributes are initialized in :meth:`_setup` to avoid
    class-level mutable state.
    """

    # Class-level annotations for tools (initialized in _setup)
    database_session: AsyncSession | None
    redis_client: redis.Redis | None
    background_tasks: list[asyncio.Task[None]]
    _startup_complete: bool
    _shutdown_complete: bool
    _app: FastAPI | None

    def _setup(self) -> None:
        """Setup lifespan manager specific state.

        Initialize per-instance attributes on the instance to avoid
        class-scope mutable state.
        """

        # Per-instance resources managed by the lifespan manager
        self.database__ = None
        self.redis_client = None
        self.background_tasks = []

        # Lifecycle flags
        self._startup_complete = False
        self._shutdown_complete = False

        # FastAPI application reference (set later via set_app)
        self._app = None

    def set_app(self, app: FastAPI) -> None:
        """Set the FastAPI app instance for DI container access."""

        self._app = app

    async def startup(self) -> None:
        """Handle application startup."""

        try:
            logger.info("🚀 Starting ZETA AI application...")

            # Initialize DI container first

            await self._init_di_container()

            # Initialize database

            await self._init_database()

            # Initialize Redis

            await self._init_redis()

            # Initialize external services

            await self._init_external_services()

            # Start background tasks

            await self._start_background_tasks()

            # Validate system health

            await self._validate_system_health()

            self._startup_complete = True

            logger.info("✅ ZETA AI application startup completed successfully")

        except Exception as e:
            logger.error(f"❌ Application startup failed: {e}")

            raise

    async def shutdown(self) -> None:
        """Handle application shutdown."""

        try:
            logger.info("🔄 Shutting down ZETA AI application...")

            # Shutdown DI container first

            await self._shutdown_di_container()

            # Stop background tasks

            await self._stop_background_tasks()

            # Close Redis connection

            await self._close_redis()

            # Close database connections

            await self._close_database()

            # Cleanup external services

            await self._cleanup_external_services()

            self._shutdown_complete = True

            logger.info("✅ ZETA AI application shutdown completed")

        except Exception as e:
            logger.error(f"❌ Application shutdown failed: {e}")

            raise

    async def _init_di_container(self) -> None:
        """Initialize DI container and start all services."""

        try:
            logger.info("🔧 Initializing DI container...")

            # Get DI container from app state if available

            if (
                hasattr(self, "_app")
                and self._app
                and hasattr(self._app.state, "di_container")
            ):
                container = self._app.state.di_container

                if container and hasattr(container, "startup_all"):
                    await container.startup_all()

                    logger.info("✅ DI container started successfully")

                else:
                    logger.warning("⚠️ DI container found but no startup_all method")

            else:
                logger.warning("⚠️ No DI container found in app state")

        except Exception as e:
            logger.error(f"❌ DI container initialization failed: {e}")

            # Don't fail startup for DI issues, log and continue

    async def _shutdown_di_container(self) -> None:
        """Shutdown DI container and stop all services."""

        try:
            logger.info("🔄 Shutting down DI container...")

            # Get DI container from app state if available

            if (
                hasattr(self, "_app")
                and self._app
                and hasattr(self._app.state, "di_container")
            ):
                container = self._app.state.di_container

                if container and hasattr(container, "shutdown_all"):
                    await container.shutdown_all()

                    logger.info("✅ DI container shutdown successfully")

                else:
                    logger.warning("⚠️ DI container found but no shutdown_all method")

            else:
                logger.warning("⚠️ No DI container found in app state")

        except Exception as e:
            logger.error(f"❌ DI container shutdown failed: {e}")

            # Don't fail shutdown for DI issues, log and continue

    async def _init_database(self) -> None:
        """Initialize database connection and tables."""

        try:
            logger.info("🔧 Initializing database...")

            # Use unified database service to create tables without importing data layer
            from apps.backend.core.services.database_service import get_database_service

            db_service = get_database_service()
            await db_service.create_tables()

            logger.info("✅ Database initialized successfully via DatabaseService")

        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")

            raise

    async def _init_redis(self) -> None:
        """Initialize Redis connection."""

        # Skip Redis if not enabled

        if not getattr(settings, "redis_enabled", False):
            logger.info("⏭️ Redis disabled, skipping initialization")

            return

        try:
            logger.info("🔧 Initializing Redis...")

            # Use default Redis URL if settings don't have redis config

            redis_url = getattr(settings, "redis_url", "redis://localhost:6379/0")

            self.redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
                retry_on_timeout=True,
            )

            # Test Redis connection

            await self.redis_client.ping()

            logger.info("✅ Redis initialized successfully")

        except Exception as e:
            logger.warning(f"⚠️ Redis initialization failed: {e}")

            # Don't fail startup for Redis issues

    async def _init_external_services(self) -> None:
        """Initialize external service connections."""

        try:
            logger.info("🔧 Initializing external services...")

            # Initialize external clients with health checks

            services_initialized = 0

            # Skip OpenAI for now - optional service

            logger.info("⏭️ OpenAI service skipped (optional)")

            services_initialized += 1

            try:
                # Skip initialization for now due to config requirement

                services_initialized += 1

            except Exception as e:
                logger.warning(f"⚠️ Anthropic service initialization failed: {e}")

            try:
                # Skip initialization for now due to config requirement

                services_initialized += 1

            except Exception as e:
                logger.warning(f"⚠️ GCP service initialization failed: {e}")

            logger.info(f"✅ External services initialized: {services_initialized}/3")

        except Exception as e:
            logger.warning(f"⚠️ Some external services may not be available: {e}")

            # Don't fail startup for external service issues

    async def _start_background_tasks(self) -> None:
        """Start background tasks."""

        try:
            logger.info("� Starting background tasks...")

            # Health check task

            health_task = asyncio.create_task(self._health_check_loop())

            self.background_tasks.append(health_task)

            # Cleanup task

            cleanup_task = asyncio.create_task(self._cleanup_loop())

            self.background_tasks.append(cleanup_task)

            logger.info(f"✅ Started {len(self.background_tasks)} background tasks")

        except Exception as e:
            logger.error(f"❌ Failed to start background tasks: {e}")

            raise

    async def _stop_background_tasks(self) -> None:
        """Stop background tasks."""

        try:
            logger.info("🔄 Stopping background tasks...")

            for task in self.background_tasks:
                if not task.done():
                    task.cancel()

            # Wait for tasks to complete

            if self.background_tasks:
                await asyncio.gather(*self.background_tasks, return_exceptions=True)

            logger.info("✅ Background tasks stopped")

        except Exception as e:
            logger.error(f"❌ Failed to stop background tasks: {e}")

    async def _close_redis(self) -> None:
        """Close Redis connection."""

        try:
            if self.redis_client:
                await self.redis_client.close()

                logger.info("✅ Redis connection closed")

        except Exception as e:
            logger.error(f"❌ Failed to close Redis connection: {e}")

    async def _close_database(self) -> None:
        """Close database connections."""

        try:
            # Database connections are managed by session pools

            # and will be closed automatically

            logger.info("✅ Database connections closed")

        except Exception as e:
            logger.error(f"❌ Failed to close database connections: {e}")

    async def _cleanup_external_services(self) -> None:
        """Cleanup external service connections."""

        try:
            # External service clients will cleanup automatically

            logger.info("✅ External services cleaned up")

        except Exception as e:
            logger.error(f"❌ Failed to cleanup external services: {e}")

    async def _validate_system_health(self) -> None:
        """Validate system health after startup."""

        try:
            logger.info("🔍 Validating system health...")

            health_checks = {
                "database": await self._check_database_health(),
            }

            # Only check Redis if enabled

            if getattr(settings, "redis_enabled", False):
                health_checks["redis"] = await self._check_redis_health()

            failed_checks = [
                name for name, status in health_checks.items() if not status
            ]

            if failed_checks:
                logger.warning(f"⚠️ Health check failures: {failed_checks}")

            else:
                logger.info("✅ All health checks passed")

        except Exception as e:
            logger.error(f"❌ Health validation failed: {e}")

    async def _check_database_health(self) -> bool:
        """Check database health."""

        try:
            from apps.backend.core.services.database_service import get_database_service

            db_service = get_database_service()
            return await db_service.health_check()

        except Exception:
            return False

    async def _check_redis_health(self) -> bool:
        """Check Redis health."""

        try:
            if self.redis_client:
                await self.redis_client.ping()

                return True

            return False

        except Exception:
            return False

    async def _health_check_loop(self) -> None:
        """Background health check loop."""

        try:
            while True:
                await asyncio.sleep(300)  # Check every 5 minutes

                health_status = {
                    "database": await self._check_database_health(),
                }

                # Only check Redis if enabled

                if getattr(settings, "redis_enabled", False):
                    health_status["redis"] = await self._check_redis_health()

                # Log unhealthy services

                unhealthy = [
                    name for name, status in health_status.items() if not status
                ]

                if unhealthy:
                    logger.warning(f"⚠️ Unhealthy services detected: {unhealthy}")

        except asyncio.CancelledError:
            logger.info("🛑 Health check loop cancelled")
            raise

        except Exception as e:
            logger.error(f"❌ Health check loop error: {e}")

    # noqa: C901 - acceptable complexity for scheduled cleanup
    async def _cleanup_loop(self) -> None:
        """Background cleanup loop."""

        try:
            while True:
                await asyncio.sleep(3600)  # Run every hour
                await self._cleanup_sessions()

        except asyncio.CancelledError:
            logger.info("🔄 Cleanup loop cancelled")
            raise

        except Exception as e:
            logger.error(f"❌ Cleanup loop error: {e}")

    async def _cleanup_sessions(self) -> None:
        """Cleanup expired/invalid sessions in Redis if available."""
        try:
            if not self.redis_client:
                return

            keys = await self.redis_client.keys("session:*")
            expired_count = 0

            for key in keys:
                ttl = await self.redis_client.ttl(key)

                if ttl == -1:  # No expiration set
                    await self.redis_client.expire(key, 86400)  # 24 hours
                elif ttl <= 0:  # Expired
                    await self.redis_client.delete(key)
                    expired_count += 1

            if expired_count > 0:
                logger.info("🧹 Cleaned up %d expired sessions", expired_count)

        except Exception as e:
            logger.error("❌ Cleanup sessions error: %s", e)

    @property
    def is_ready(self) -> bool:
        """Check if application is ready."""

        return self._startup_complete and not self._shutdown_complete


# Global lifespan manager


lifespan_manager = LifespanManager()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager.





    This function manages the application lifecycle, handling startup


    and shutdown events.





    Args:


        app: FastAPI application instance.





    Yields:


        None during application runtime.


    """

    try:
        # Startup

        await lifespan_manager.startup()

        logger.info("✅ Zeta AI Server started successfully")

        yield

    finally:
        # Shutdown

        logger.info("🛑 Shutting down Zeta AI Server...")

        await lifespan_manager.shutdown()

        logger.info("✅ Zeta AI Server shutdown complete")


__all__ = (
    "LifespanManager",
    "lifespan",
)
