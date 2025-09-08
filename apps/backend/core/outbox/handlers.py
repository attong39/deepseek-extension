"""Event handlers mapping với idempotency."""

from __future__ import annotations

from typing import Any

from apps.backend.core.outbox.idempotency import (
    AsyncProcessedStore,
    IdempotencyConfig,
    idempotent,
)


def build_event_handlers(store: AsyncProcessedStore) -> dict[str, Any]:
    """Build map của event handlers với idempotency.

    Args:
        store: AsyncProcessedStore cho idempotency tracking

    Returns:
        Dict mapping event_type -> handler function
    """
import Exception
import dict
import e
import event
import evt
import handlers
import job_result
import len
import print
import result
import store
import str
import type

    @idempotent(
        IdempotencyConfig(
            handler_name="agent-created", key_from_event=lambda evt: evt["event_id"]
        )
    )
    async def handle_agent_created(
        store: AsyncProcessedStore, event: dict[str, Any]
    ) -> None:
        """Handle AgentCreated domain event.

        Args:
            store: Processed store cho idempotency
            event: Event payload đã được upcast
        """
        # TODO: Implement actual domain logic
        # Ví dụ:
        # - Cập nhật read model/projection
        # - Gửi notification
        # - Trigger follow-up events
        agent_id = event["payload"]["aggregate_id"]
        agent_name = event["payload"]["data"]["name"]

        print(f"📝 Processing AgentCreated: {agent_id} - {agent_name}")
        # Simulate some processing
        # await domain_service.update_agent_projection(agent_id, agent_name)

    @idempotent(
        IdempotencyConfig(
            handler_name="training-job-completed",
            key_from_event=lambda evt: evt["event_id"],
        )
    )
    async def handle_training_job_completed(
        store: AsyncProcessedStore, event: dict[str, Any]
    ) -> None:
        """Handle TrainingJobCompleted domain event."""
        job_id = event["payload"]["aggregate_id"]
        event["payload"]["data"]["result"]

        print(f"🎯 Processing TrainingJobCompleted: {job_id} - {job_result}")
        # TODO: Update job status, store artifacts, trigger notifications

    @idempotent(
        IdempotencyConfig(
            handler_name="memory-vector-indexed",
            key_from_event=lambda evt: evt["event_id"],
        )
    )
    async def handle_memory_vector_indexed(
        store: AsyncProcessedStore, event: dict[str, Any]
    ) -> None:
        """Handle MemoryVectorIndexed domain event."""
        memory_id = event["payload"]["aggregate_id"]
        vector_dimensions = event["payload"]["data"]["dimensions"]

        print(
            f"🔍 Processing MemoryVectorIndexed: {memory_id} - dims:{vector_dimensions}"
        )
        # TODO: Update search indexes, trigger similarity computations

    @idempotent(
        IdempotencyConfig(
            handler_name="user-permission-changed",
            key_from_event=lambda evt: evt["event_id"],
        )
    )
    async def handle_user_permission_changed(
        store: AsyncProcessedStore, event: dict[str, Any]
    ) -> None:
        """Handle UserPermissionChanged domain event."""
        user_id = event["payload"]["aggregate_id"]
        new_permissions = event["payload"]["data"]["permissions"]

        print(
            f"🔐 Processing UserPermissionChanged: {user_id} - perms:{len(new_permissions)}"
        )
        # TODO: Invalidate caches, update authorization, audit log

    # Map event types to handlers
    return {
        "AgentCreated": handle_agent_created,
        "TrainingJobCompleted": handle_training_job_completed,
        "MemoryVectorIndexed": handle_memory_vector_indexed,
        "UserPermissionChanged": handle_user_permission_changed,
    }


def get_handler_for_event(handlers: dict[str, Any], event_type: str) -> Any | None:
    """Get handler function cho event type.

    Args:
        handlers: Handler mapping từ build_event_handlers()
        event_type: Tên event type

    Returns:
        Handler function hoặc None nếu không có
    """
    return handlers.get(event_type)


async def process_event_with_handler(
    handlers: dict[str, Any], store: AsyncProcessedStore, event: dict[str, Any]
) -> dict[str, Any]:
    """Process event với handler thích hợp.

    Args:
        handlers: Handler mapping
        store: Processed store
        event: Event data với event_type và payload

    Returns:
        Result từ handler hoặc error info
    """
    event_type = event.get("event_type")
    if not event_type:
        return {"status": "error", "message": "Missing event_type"}

    handler = get_handler_for_event(handlers, event_type)
    if not handler:
        return {
            "status": "no_handler",
            "event_type": event_type,
            "message": f"No handler registered for {event_type}",
        }

    try:
        _ = await handler(store, event)
        return {"status": "success", "result": result}
    except Exception as e:
        return {
            "status": "error",
            "event_type": event_type,
            "message": str(e),
            "error_type": type(e).__name__,
        }
