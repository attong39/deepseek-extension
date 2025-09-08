from __future__ import annotations

import asyncio
import logging
from typing import Any
import Exception
import RuntimeError
import SystemExit
import bool
import conn
import dict
import exc
import int
import result
import str

try:  # Optional rich initializer
    from apps.backend.config.settings import get_settings  # type: ignore
    from apps.backend.data.database_init import DatabaseInitializer  # type: ignore
except Exception:  # noqa: BLE001
    DatabaseInitializer = None  # type: ignore[assignment]
    get_settings = None  # type: ignore[assignment]

try:  # Base/engine fallback
    from apps.backend.data.models.base import Base, get_engine  # type: ignore
except Exception:  # noqa: BLE001
    Base = None  # type: ignore[assignment]
    get_engine = None  # type: ignore[assignment]

logger = logging.getLogger("db_migrate")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


async def _try_database_initializer() -> bool:
    """Attempt to initialize DB using DatabaseInitializer if available."""
    try:
        if DatabaseInitializer is None or get_settings is None:
            raise RuntimeError("DatabaseInitializer not available")
        settings = get_settings()
        initializer = DatabaseInitializer(settings.database_url)
        # Create tables and optionally seed minimal data
        result: dict[str, Any] = await initializer.initialize_database(
            recreate=False, seed_data=True, seed_test_data_flag=False
        )
        logger.info("Database initialized via DatabaseInitializer: %s", result)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.info("DatabaseInitializer path not used: %s", exc)
        return False


async def _create_all_via_base() -> bool:
    """Fallback: use models.base to create all tables from metadata."""
    try:
        if Base is None or get_engine is None:
            raise RuntimeError("Base/get_engine not available")
        engine = get_engine()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created via Base.metadata.create_all")
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to create tables via Base: %s", exc)
        return False


async def main() -> int:
    # Try the richer initializer first
    if await _try_database_initializer():
        return 0

    # Fallback to simple Base.metadata.create_all
    if await _create_all_via_base():
        return 0

    logger.error("No migration path succeeded. Ensure DATABASE_URL is set and drivers installed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
