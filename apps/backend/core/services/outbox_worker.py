"""
Outbox Worker cho ZETA_AI Autonomous System.

Worker này xử lý:
- Domain events từ autonomous operations
- Message publishing to external systems
- Event retry logic
- Dead letter queue handling
- Event ordering và idempotency
"""

from __future__ import annotations

import asyncio
import logging
import time
import uuid
from enum import Enum
from typing import Any

from apps.backend.core.domain.autonomy import AutonomyEvent
from pydantic import BaseModel, Field
import Exception
import NotImplementedError
import batch_size
import bool
import dict
import e
import event
import float
import handler
import int
import len
import list
import max_concurrent_events
import min
import poll_interval
import self
import set
import status
import str
import sum

logger = logging.getLogger(__name__)


class EventStatus(str, Enum):
    """Status của outbox event."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class OutboxEvent(BaseModel):
    """
    Event trong outbox queue.

    Attributes:
        id: Unique event ID
        event_type: Type of domain event
        aggregate_id: ID của aggregate tạo event
        event_data: Payload của event
        status: Current processing status
        created_at: Creation timestamp
        scheduled_at: When to process event
        processed_at: When event was processed
        retry_count: Number of retry attempts
        max_retries: Maximum retry attempts
        error_message: Last error message
        correlation_id: For tracking related events
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    aggregate_id: str
    event_data: dict[str, Any]
    status: EventStatus = EventStatus.PENDING
    created_at: float = Field(default_factory=time.time)
    scheduled_at: float = Field(default_factory=time.time)
    processed_at: float | None = None
    retry_count: int = 0
    max_retries: int = 3
    error_message: str | None = None
    correlation_id: str | None = None


class EventHandler:
    """Base class cho event handlers."""

    def supports_event(self, event_type: str) -> bool:
        """Check if handler supports event type."""
        raise NotImplementedError

    async def handle_event(self, event: OutboxEvent) -> bool:
        """
        Handle event processing.

        Args:
            event: Event to process

        Returns:
            True if successful, False if failed
        """
        raise NotImplementedError


class AutonomousEventHandler(EventHandler):
    """Handler cho autonomous domain events."""

    def __init__(self):
        self._supported_events = {
            "goal_created",
            "goal_updated",
            "goal_completed",
            "goal_failed",
            "plan_created",
            "plan_updated",
            "plan_completed",
            "plan_failed",
            "action_started",
            "action_completed",
            "action_failed",
            "safety_violation",
            "safety_policy_updated",
            "skill_executed",
            "skill_failed",
            "skill_registered",
            "session_started",
            "session_ended",
            "session_paused",
        }

    def supports_event(self, event_type: str) -> bool:
        """Check if event is autonomous-related."""
        return event_type in self._supported_events

    async def handle_event(self, event: OutboxEvent) -> bool:
        """Handle autonomous event."""
        try:
            event_type = event.event_type
            event_data = event.event_data

            logger.info(
                f"Processing autonomous event: {event_type} for {event.aggregate_id}"
            )

            if event_type in ["goal_created", "goal_updated"]:
                await self._handle_goal_event(event_data)
            elif event_type in ["plan_created", "plan_updated"]:
                await self._handle_plan_event(event_data)
            elif event_type in ["action_started", "action_completed", "action_failed"]:
                await self._handle_action_event(event_data)
            elif event_type in ["safety_violation"]:
                await self._handle_safety_event(event_data)
            elif event_type in ["skill_executed", "skill_failed"]:
                await self._handle_skill_event(event_data)
            elif event_type in ["session_started", "session_ended", "session_paused"]:
                await self._handle_session_event(event_data)
            else:
                logger.warning(f"Unknown autonomous event type: {event_type}")

            return True

        except Exception as e:
            logger.error(f"Failed to handle autonomous event {event.id}: {e}")
            return False

    async def _handle_goal_event(self, event_data: dict[str, Any]) -> None:
        """Handle goal-related events."""
        # Example: Update metrics, notify stakeholders, trigger workflows
        goal_id = event_data.get("goal_id")
        logger.debug(f"Handled goal event for goal {goal_id}")

        # Could integrate with:
        # - Metrics collection system
        # - Notification service
        # - Workflow orchestrator
        # - Dashboard updates

    async def _handle_plan_event(self, event_data: dict[str, Any]) -> None:
        """Handle plan-related events."""
        plan_id = event_data.get("plan_id")
        logger.debug(f"Handled plan event for plan {plan_id}")

        # Could integrate with:
        # - Planning analytics
        # - Resource allocation
        # - Timeline estimation

    async def _handle_action_event(self, event_data: dict[str, Any]) -> None:
        """Handle action execution events."""
        action_id = event_data.get("action_id")
        action_name = event_data.get("action_name")
        logger.debug(f"Handled action event: {action_name} ({action_id})")

        # Could integrate with:
        # - Execution monitoring
        # - Performance tracking
        # - Error detection

    async def _handle_safety_event(self, event_data: dict[str, Any]) -> None:
        """Handle safety-related events."""
        violation_type = event_data.get("violation_type")
        severity = event_data.get("severity", "unknown")

        logger.warning(
            f"Safety violation detected: {violation_type} (severity: {severity})"
        )

        # Could integrate with:
        # - Security incident management
        # - Alert systems
        # - Compliance reporting
        # - Emergency response

    async def _handle_skill_event(self, event_data: dict[str, Any]) -> None:
        """Handle skill execution events."""
        skill_name = event_data.get("skill_name")
        logger.debug(f"Handled skill event for skill {skill_name}")

        # Could integrate with:
        # - Skill performance analytics
        # - Learning algorithms
        # - Capability tracking

    async def _handle_session_event(self, event_data: dict[str, Any]) -> None:
        """Handle session lifecycle events."""
        session_id = event_data.get("session_id")
        logger.debug(f"Handled session event for session {session_id}")

        # Could integrate with:
        # - Session management
        # - User analytics
        # - Resource cleanup


class WebSocketEventHandler(EventHandler):
    """Handler để broadcast events qua WebSocket."""

    def __init__(self):
        self._supported_events = {
            "goal_updated",
            "plan_completed",
            "action_completed",
            "safety_violation",
            "skill_executed",
            "session_status_changed",
        }

    def supports_event(self, event_type: str) -> bool:
        """Check if event should be broadcasted via WebSocket."""
        return event_type in self._supported_events

    async def handle_event(self, event: OutboxEvent) -> bool:
        """Broadcast event via WebSocket."""
        try:
            # Import here to avoid circular imports
            from app.websockets.security import (
                get_autonomous_websocket_manager,
            )

            manager = get_autonomous_websocket_manager()

            # Prepare WebSocket message
            ws_message = {
                "type": "domain_event",
                "event_type": event.event_type,
                "event_id": event.id,
                "aggregate_id": event.aggregate_id,
                "data": event.event_data,
                "timestamp": event.created_at,
            }

            # Determine broadcast target
            session_id = event.event_data.get("session_id")
            user_id = event.event_data.get("user_id")

            sent_count = 0

            if session_id:
                # Broadcast to specific session
                sent_count = await manager.broadcast_to_session(session_id, ws_message)
            elif event.event_type == "safety_violation":
                # Broadcast safety violations to relevant users
                sent_count = await manager.broadcast_safety_alert(
                    event.event_data, target_user_id=user_id
                )
            else:
                # General broadcast based on user_id
                if user_id:
                    # Would need to implement user-specific broadcast
                    logger.debug(f"Would broadcast to user {user_id}")
                    sent_count = 1  # Placeholder

            logger.debug(
                f"Broadcasted event {event.id} to {sent_count} WebSocket connections"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to broadcast event {event.id}: {e}")
            return False


class OutboxWorker:
    """
    Worker để xử lý outbox events.

    Features:
    - Event polling và processing
    - Retry logic với exponential backoff
    - Dead letter queue handling
    - Event ordering preservation
    - Handler registration
    """

    def __init__(
        self,
        poll_interval: float = 1.0,
        batch_size: int = 10,
        max_concurrent_events: int = 5,
    ):
        self.poll_interval = poll_interval
        self.batch_size = batch_size
        self.max_concurrent_events = max_concurrent_events

        # Event storage (in production, use database)
        self._events: dict[str, OutboxEvent] = {}
        self._processing_events: set[str] = set()

        # Event handlers
        self._handlers: list[EventHandler] = []

        # Worker state
        self._running = False
        self._worker_task: asyncio.Task | None = None

        # Register default handlers
        self.register_handler(AutonomousEventHandler())
        self.register_handler(WebSocketEventHandler())

    def register_handler(self, handler: EventHandler) -> None:
        """Register event handler."""
        self._handlers.append(handler)
        logger.info(f"Registered event handler: {handler.__class__.__name__}")

    async def add_event(self, event: AutonomyEvent) -> str:
        """
        Add domain event to outbox.

        Args:
            event: Domain event to add

        Returns:
            Event ID
        """
        outbox_event = OutboxEvent(
            event_type=event.event_type,
            aggregate_id=event.aggregate_id,
            event_data=event.event_data,
            correlation_id=event.correlation_id,
        )

        self._events[outbox_event.id] = outbox_event

        logger.debug(
            f"Added event to outbox: {outbox_event.event_type} ({outbox_event.id})"
        )
        return outbox_event.id

    async def start(self) -> None:
        """Start outbox worker."""
        if self._running:
            logger.warning("Outbox worker already running")
            return

        self._running = True
        self._worker_task = asyncio.create_task(self._worker_loop())

        logger.info("Outbox worker started")

    async def stop(self) -> None:
        """Stop outbox worker."""
        if not self._running:
            return

        self._running = False

        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass

        logger.info("Outbox worker stopped")

    async def _worker_loop(self) -> None:
        """Main worker loop."""
        logger.info("Outbox worker loop started")

        try:
            while self._running:
                await self._process_batch()
                await asyncio.sleep(self.poll_interval)
        except asyncio.CancelledError:
            logger.info("Outbox worker loop cancelled")
            raise
        except Exception as e:
            logger.error(f"Outbox worker error: {e}")
            raise

    async def _process_batch(self) -> None:
        """Process batch of pending events."""
        # Get pending events
        pending_events = [
            event
            for event in self._events.values()
            if (
                event.status == EventStatus.PENDING
                and event.scheduled_at <= time.time()
                and event.id not in self._processing_events
            )
        ]

        # Sort by creation time for ordering
        pending_events.sort(key=lambda e: e.created_at)

        # Limit batch size and concurrent processing
        batch = pending_events[: self.batch_size]
        concurrent_limit = min(len(batch), self.max_concurrent_events)

        if not batch:
            return

        logger.debug(f"Processing batch of {len(batch)} events")

        # Process events concurrently with limit
        semaphore = asyncio.Semaphore(concurrent_limit)
        tasks = [
            self._process_event_with_semaphore(semaphore, event) for event in batch
        ]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _process_event_with_semaphore(
        self, semaphore: asyncio.Semaphore, event: OutboxEvent
    ) -> None:
        """Process event with concurrency control."""
        async with semaphore:
            await self._process_event(event)

    async def _process_event(self, event: OutboxEvent) -> None:
        """Process single event."""
        event_id = event.id

        try:
            # Mark as processing
            self._processing_events.add(event_id)
            event.status = EventStatus.PROCESSING

            logger.debug(f"Processing event: {event.event_type} ({event_id})")

            # Find handlers for event
            handlers = [
                handler
                for handler in self._handlers
                if handler.supports_event(event.event_type)
            ]

            if not handlers:
                logger.warning(f"No handlers found for event type: {event.event_type}")
                event.status = EventStatus.COMPLETED
                event.processed_at = time.time()
                return

            # Process with all applicable handlers
            all_successful = True

            for handler in handlers:
                try:
                    success = await handler.handle_event(event)
                    if not success:
                        all_successful = False
                        logger.warning(
                            f"Handler {handler.__class__.__name__} failed for event {event_id}"
                        )
                except Exception as e:
                    all_successful = False
                    logger.error(
                        f"Handler {handler.__class__.__name__} error for event {event_id}: {e}"
                    )

            # Update event status
            if all_successful:
                event.status = EventStatus.COMPLETED
                event.processed_at = time.time()
                logger.debug(f"Event processed successfully: {event_id}")
            else:
                await self._handle_event_failure(event)

        except Exception as e:
            logger.error(f"Unexpected error processing event {event_id}: {e}")
            await self._handle_event_failure(event)

        finally:
            # Remove from processing set
            self._processing_events.discard(event_id)

    async def _handle_event_failure(self, event: OutboxEvent) -> None:
        """Handle event processing failure."""
        event.retry_count += 1

        if event.retry_count >= event.max_retries:
            # Move to dead letter queue
            event.status = EventStatus.DEAD_LETTER
            event.processed_at = time.time()
            logger.error(f"Event moved to dead letter queue: {event.id}")
        else:
            # Schedule retry with exponential backoff
            backoff_seconds = 2**event.retry_count
            event.status = EventStatus.PENDING
            event.scheduled_at = time.time() + backoff_seconds

            logger.warning(
                f"Event retry scheduled: {event.id} "
                f"(attempt {event.retry_count}/{event.max_retries}) "
                f"in {backoff_seconds}s"
            )

    def get_stats(self) -> dict[str, Any]:
        """Get worker statistics."""
        status_counts = {}
        for status in EventStatus:
            status_counts[status.value] = sum(
                1 for event in self._events.values() if event.status == status
            )

        return {
            "total_events": len(self._events),
            "processing_events": len(self._processing_events),
            "registered_handlers": len(self._handlers),
            "status_counts": status_counts,
            "worker_running": self._running,
        }


# Global worker instance
_outbox_worker: OutboxWorker | None = None


def get_outbox_worker() -> OutboxWorker:
    """Get global outbox worker instance."""
    global _outbox_worker  # noqa: PLW0603
    if _outbox_worker is None:
        _outbox_worker = OutboxWorker()
    return _outbox_worker


async def publish_event(event: AutonomyEvent) -> str:
    """
    Publish domain event to outbox.

    Args:
        event: Domain event to publish

    Returns:
        Event ID
    """
    worker = get_outbox_worker()
    return await worker.add_event(event)


async def start_outbox_worker() -> None:
    """Start global outbox worker."""
    worker = get_outbox_worker()
    await worker.start()


async def stop_outbox_worker() -> None:
    """Stop global outbox worker."""
    worker = get_outbox_worker()
    await worker.stop()
