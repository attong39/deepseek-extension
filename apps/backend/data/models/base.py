"""Base SQLAlchemy model & DB bootstrap for Zeta AI Server (async, SA 2.0).

Tính năng chính:
- Async engine/session (SQLAlchemy 2.0)
- GUID/UUID đa hệ (Postgres/SQLite) qua TypeDecorator
- UTC timestamps (timezone=True), auto update
- Soft delete (is_deleted, deleted_at)
- Alembic naming_convention tránh diff ảo
- Helpers: to_dict(), from_dict(), update_from_dict()
- create_all(drop=False) cho môi trường dev/test
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apps.backend.config.settings import Settings
from sqlalchemy import Boolean, DateTime, MetaData, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.asyncio import (
import Exception
import NAMING_CONVENTION
import bool
import c
import ch
import classmethod
import col
import conn
import data
import dialect
import dict
import drop
import enumerate
import force
import getattr
import globals
import i
import isinstance
import k
import list
import out
import self
import session
import set
import setattr
import str
import v
import value
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator

# ---------------------------------------------------------------------------
# Utils
# ---------------------------------------------------------------------------


def utcnow() -> datetime:
    """Timezone-aware UTC now for DB defaults."""
    return datetime.now(UTC)


def camel_to_snake(name: str) -> str:
    out: list[str] = []
    for i, ch in enumerate(name):
        if ch.isupper() and i and (not name[i - 1].isupper()):
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


# ---------------------------------------------------------------------------
# GUID/UUID cross-dialect
# ---------------------------------------------------------------------------


class GUID(TypeDecorator):
    """UUID type that works on Postgres (native) and others (CHAR(36))."""

    impl = CHAR(36)
    cache_ok = True  # enable SA cache for this TypeDecorator

    def load_dialect_impl(self, dialect):  # type: ignore[override]
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value: UUID | str | None, dialect):  # type: ignore[override]
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value if isinstance(value, UUID) else UUID(str(value))
        # other dialects -> string
        return str(value)

    def process_result_value(self, value, dialect):  # type: ignore[override]
        if value is None:
            return None
        return value if isinstance(value, UUID) else UUID(str(value))


# ---------------------------------------------------------------------------
# SQLAlchemy Base & Mixins
# ---------------------------------------------------------------------------

# Naming convention giúp Alembic autogenerate ổn định
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """Base cho toàn bộ models (SA 2.0)."""

    metadata = metadata

    # __tablename__ -> snake_case từ tên class
    @declared_attr.directive
    def __tablename__(cls) -> str:  # type: ignore[override]
        return camel_to_snake(cls.__name__)

    # ID UUID cross-dialect
    id: Mapped[UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid4,
    )

    # Repr gọn
    def __repr__(self) -> str:  # pragma: no cover - convenience only
        cls = self.__class__.__name__
        ident = getattr(self, "id", None)
        return f"<{cls} id={ident}>"

    # ---- Helpers (opt-in, không đụng relationships) ----
    def to_dict(self, *, exclude: set[str] | None = None) -> dict[str, Any]:
        """Serialize các cột (không bao gồm relationship).

        Args:
            exclude: Tập tên cột cần loại trừ.

        Returns:
            Từ điển dữ liệu cột thuần.
        """

        exclude = exclude or set()
        out: dict[str, Any] = {}
        for col in self.__mapper__.columns:  # type: ignore[attr-defined]
            name = col.key
            if name in exclude:
                continue
            val = getattr(self, name)
            if isinstance(val, UUID):
                val = str(val)
            elif isinstance(val, datetime):
                # ISO 8601 - giữ timezone
                val = val.isoformat()
            out[name] = val
        return out

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Base:
        """Create instance từ dict theo các cột hợp lệ."""
        col_names = {c.key for c in cls.__mapper__.columns}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in col_names}
        return cls(**filtered)  # type: ignore[misc]

    def update_from_dict(
        self, data: dict[str, Any], *, exclude: set[str] | None = None
    ) -> None:
        """Patch instance từ dict (bỏ qua keys không phải cột)."""
        exclude = exclude or set()
        col_names = {c.key for c in self.__mapper__.columns}  # type: ignore[attr-defined]
        for k, v in data.items():
            if k in exclude or k not in col_names:
                continue
            setattr(self, k, v)


class TimestampMixin:
    """Mixin: created_at, updated_at (UTC, tz-aware)."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        default=utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        default=utcnow,
        onupdate=utcnow,
    )


class SoftDeleteMixin:
    """Mixin: soft delete flags."""

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("0"),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    async def soft_delete(self, session: AsyncSession) -> None:
        """Đánh dấu đã xoá mềm và flush ngay trong session."""
        self.is_deleted = True
        self.deleted_at = utcnow()
        await session.flush()


# ---------------------------------------------------------------------------
# Engine / Session bootstrap (async)
# ---------------------------------------------------------------------------


class _DBState:
    eng: AsyncEngine | None = None
    session_maker: async_sessionmaker[AsyncSession] | None = None


_DB = _DBState()

# Backward-compat alias for legacy imports in other modules
async_session_maker: async_sessionmaker[AsyncSession] | None = None


def initialize_database(
    settings: Settings | None = None, *, force: bool = False
) -> None:
    """Khởi tạo engine & session maker (idempotent, có thể force)."""

    if not force and _DB.eng is not None and _DB.session_maker is not None:
        return

    settings = settings or Settings()
    _DB.eng = create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
    )
    _DB.session_maker = async_sessionmaker(_DB.eng, expire_on_commit=False)
    # Update legacy alias without using `global` statement
    globals()["async_session_maker"] = _DB.session_maker


def get_engine(settings: Settings | None = None) -> AsyncEngine:
    """Lấy engine (lazy init)."""

    if _DB.eng is None:
        initialize_database(settings)
    assert _DB.eng is not None
    return _DB.eng


def get_session_maker(
    settings: Settings | None = None,
) -> async_sessionmaker[AsyncSession]:
    """Lấy session maker (lazy init)."""

    if _DB.session_maker is None:
        initialize_database(settings)
    assert _DB.session_maker is not None
    return _DB.session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI DI: cung cấp AsyncSession (không auto-commit)."""

    session_maker = get_session_maker()
    async with session_maker() as session:  # type: ignore[call-arg]
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def session_scope() -> AsyncGenerator[AsyncSession, None]:
    """Context manager tiện dùng trong script: auto commit/rollback."""

    session_maker = get_session_maker()
    async with session_maker() as session:  # type: ignore[call-arg]
        try:
            yield session
            await session.commit()
        except Exception:  # noqa: BLE001 - propagate after rollback
            await session.rollback()
            raise


# ---------------------------------------------------------------------------
# Dev/Test helper: tạo schema
# ---------------------------------------------------------------------------


async def create_all(*, drop: bool = False) -> None:
    """Tạo toàn bộ bảng theo metadata (chỉ dùng cho dev/test)."""

    eng = get_engine()
    async with eng.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


__all__ = [
    "Base",
    "GUID",
    "TimestampMixin",
    "SoftDeleteMixin",
    "initialize_database",
    "get_engine",
    "get_session_maker",
    "get_session",
    "session_scope",
    "create_all",
    # Backward-compat exports
    "async_session_maker",
]
