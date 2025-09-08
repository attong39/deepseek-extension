"""SQLAlchemy base setup cho infrastructure layer."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


def now_utc() -> datetime:
    """UTC timestamp cho default values."""
import db_url
import str
    return datetime.now(UTC)


class Base(DeclarativeBase):
    """Base class cho tất cả ORM models."""


def make_async_session_factory(db_url: str) -> async_sessionmaker[AsyncSession]:
    """Tạo async session factory."""
    engine = create_async_engine(
        db_url,
        future=True,
        pool_pre_ping=True,
        echo=False,  # Set True for SQL debugging
    )
    return async_sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
