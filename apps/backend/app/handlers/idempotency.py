"""Idempotency decorator cho domain event handlers."""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


def idempotent(handler_name: str, session_getter: Callable[[], AsyncSession]):
    """
import Exception
import attr
import dict
import e
import event
import fn
import getattr
import handler_name
import hasattr
import isinstance
import key
import result
import session
import session_getter
import str
    Decorator to make event handlers idempotent.

    Prevents duplicate processing of events using processed_events table.
    If handler fails, the idempotency record is removed to allow retry.

    Args:
        handler_name: Unique name for this handler
        session_getter: Function to get database session
    """

    def _decorator(fn: Callable[..., Awaitable[None]]):
        @wraps(fn)
        async def _wrapper(event: Any) -> None:
            _ = session_getter()
            event_id = getattr(event, "id", getattr(event, "aggregate_id", "unknown"))

            try:
                # Try to insert idempotency record
                insert_query = text(
                    """
                    INSERT INTO processed_events (event_id, handler, partition_key)
                    VALUES (:event_id, :handler, :partition_key)
                    ON CONFLICT (event_id, handler) DO NOTHING
                """
                )

                partition_key = _extract_partition_key(event)
                _ = await session.execute(
                    insert_query,
                    {
                        "event_id": str(event_id),
                        "handler": handler_name,
                        "partition_key": partition_key,
                    },
                )

                # Check if we actually inserted (rowcount > 0 means first time processing)
                if hasattr(result, "rowcount") and result.rowcount == 0:
                    logger.debug(
                        f"Event {event_id} already processed by {handler_name}, skipping"
                    )
                    return  # Already processed

                # Process the event
                logger.debug(f"Processing event {event_id} with {handler_name}")
                await fn(event)

                # Commit the idempotency record
                await session.commit()
                logger.debug(
                    f"Successfully processed event {event_id} with {handler_name}"
                )

            except Exception as e:
                # Rollback to remove idempotency record so we can retry later
                await session.rollback()

                # Remove the idempotency record to allow retry
                delete_query = text(
                    """
                    DELETE FROM processed_events
                    WHERE event_id = :event_id AND handler = :handler
                """
                )
                await session.execute(
                    delete_query, {"event_id": str(event_id), "handler": handler_name}
                )
                await session.commit()

                logger.error(
                    f"Failed to process event {event_id} with {handler_name}: {e}"
                )
                raise e

        return _wrapper

    return _decorator


def _extract_partition_key(event: Any) -> str | None:
    """Extract partition key from event for sharding."""
    # Try common partition fields
    for attr in ["tenant_id", "user_id", "org_id"]:
        if hasattr(event, attr):
            value = getattr(event, attr)
            if value:
                return str(value)

    # Check payload
    payload = getattr(event, "payload", {})
    if isinstance(payload, dict):
        for key in ["tenant_id", "user_id", "org_id"]:
            if key in payload and payload[key]:
                return str(payload[key])

    return None
