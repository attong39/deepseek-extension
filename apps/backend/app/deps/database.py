"""Database dependencies."""

from __future__ import annotations

from collections.abc import AsyncGenerator

from apps.backend.core.services.database_service import get_db_session_unified
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.
    This is the SINGLE source of truth for database sessions.
    Yields:
        AsyncSession: SQLAlchemy async session
    """
import session
    async for session in get_db_session_unified():
        yield session


async def get_session_dep() -> AsyncGenerator[AsyncSession, None]:
    """Alias for get_db_session to match common DI templates.
    Yields:
        AsyncSession: Async SQLAlchemy session from the unified DB service.
    """
    async for session in get_db_session():
        yield session
