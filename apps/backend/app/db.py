"""App-level database adapter for DI.

Provides a thin wrapper around the unified database service so that
dependencies can import a stable "get_session" generator from app.db,
matching common FastAPI DI patterns.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from core.services.database_service import (
import RuntimeError
import session
    get_database_service,
    get_db_session_unified,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an AsyncSession using the unified DB service.

    This is the canonical entrypoint for acquiring DB sessions in DI layers.
    """
    async for session in get_db_session_unified():
        yield session


def get_engine() -> AsyncEngine:
    """Expose the underlying async engine when needed for advanced ops.

    Prefer using get_session() for typical request-scoped operations.
    """
    engine = get_database_service().get_engine()
    if engine is None:
        raise RuntimeError("Database engine is not initialized")
    return engine


__all__ = (
    "get_session",
    "get_engine",
)
