"""GraphQL subscriptions implementation for ZETA AI system.





This module provides real-time subscription capabilities using WebSocket


connections for live updates of chat messages, agent status, and system events.


"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from app.api.graphql.schema import AgentType, MemoryType, MessageType
import Exception
import KeyError
import RuntimeError
import agent
import agent_id
import agent_repository
import chat_id
import chat_repository
import content
import dict
import e
import event_type
import event_types
import float
import getattr
import hasattr
import list
import memory
import memory_repository
import message_id
import metadata
import redis_client
import role
import self
import set
import str
import subscriber_id
import subscribers
import timestamp

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    import redis.asyncio as redis
    from apps.backend.core.domain.entities.agent import Agent
    from apps.backend.core.domain.entities.memory import Memory
    from apps.backend.core.interfaces.repositories import (
        AgentRepository,
        ChatRepository,
        MemoryRepository,
    )


logger = logging.getLogger(__name__)


class SubscriptionManager:
    """Manages GraphQL subscriptions and real-time updates."""

    # Declared for static type checkers; initialized in __init__
    _subscribers: dict[str, set[str]]

    def __init__(
        self,
        redis_client: redis.Redis,
        agent_repository: AgentRepository,
        chat_repository: ChatRepository,
        memory_repository: MemoryRepository,
    ):
        self.redis_client = redis_client

        self.agent_repository = agent_repository

        self.chat_repository = chat_repository

        self.memory_repository = memory_repository

        # initialize subscribers mapping
        self._subscribers = {}

    def subscribe_to_channel(
        self,
        channel: str,
        subscriber_id: str,
    ) -> None:
        """Subscribe to a Redis channel for real-time updates."""

        if channel not in self._subscribers:
            self._subscribers[channel] = set()

        self._subscribers[channel].add(subscriber_id)

        logger.info(f"Subscriber {subscriber_id} subscribed to channel {channel}")

    def unsubscribe_from_channel(
        self,
        channel: str,
        subscriber_id: str,
    ) -> None:
        """Unsubscribe from a Redis channel."""

        if channel in self._subscribers:
            self._subscribers[channel].discard(subscriber_id)

            if not self._subscribers[channel]:
                del self._subscribers[channel]

        logger.info(f"Subscriber {subscriber_id} unsubscribed from channel {channel}")

    async def publish_message(
        self,
        channel: str,
        message: dict[str, Any],
    ) -> None:
        """Publish a message to a Redis channel."""

        try:
            await self.redis_client.publish(channel, json.dumps(message, default=str))

            logger.debug(f"Published message to channel {channel}: {message}")

        except Exception as e:
            logger.error(f"Error publishing message to {channel}: {e}")

    async def chat_message_stream(
        self,
        chat_id: UUID,
        subscriber_id: str,
    ) -> AsyncGenerator[MessageType, None]:
        """Stream new messages for a specific chat."""

        channel = f"chat_messages:{chat_id}"

        try:
            self.subscribe_to_channel(channel, subscriber_id)

            # Create Redis subscription

            pubsub = self.redis_client.pubsub()

            await pubsub.subscribe(channel)

            logger.info(f"Started chat message stream for chat {chat_id}")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])

                        # Convert to MessageType

                        yield MessageType(
                            id=UUID(data["id"]),
                            chat_id=UUID(data["chat_id"]),
                            content=data["content"],
                            role=data["role"],
                            timestamp=datetime.fromisoformat(data["timestamp"]),
                            metadata=data.get("metadata"),
                        )  # type: ignore[call-arg]

                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Error parsing chat message: {e}")

                        continue

        except Exception as e:
            logger.error(f"Error in chat message stream: {e}")

            raise

        finally:
            self.unsubscribe_from_channel(channel, subscriber_id)

            await pubsub.unsubscribe(channel)

            await pubsub.close()

    async def agent_status_stream(
        self,
        agent_id: UUID,
        subscriber_id: str,
    ) -> AsyncGenerator[AgentType, None]:
        """Stream agent status updates."""

        channel = f"agent_status:{agent_id}"

        try:
            self.subscribe_to_channel(channel, subscriber_id)

            # Create Redis subscription

            pubsub = self.redis_client.pubsub()

            await pubsub.subscribe(channel)

            logger.info(f"Started agent status stream for agent {agent_id}")

            # Send initial status

            _ = await self.agent_repository.get_by_id(agent_id)

            if agent:
                yield AgentType(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    model_type=getattr(agent, "model_type", "unknown"),
                    status=agent.status.value
                    if hasattr(agent.status, "value")
                    else str(agent.status),
                    capabilities=getattr(agent, "capabilities", []),
                    created_at=agent.created_at,
                    updated_at=agent.updated_at,
                    created_by=getattr(agent, "created_by", "unknown"),
                )  # type: ignore[call-arg]

            # Listen for updates

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])

                        # Convert to AgentType

                        yield AgentType(
                            id=UUID(data["id"]),
                            name=data["name"],
                            description=data.get("description"),
                            model_type=data["model_type"],
                            status=data["status"],
                            capabilities=data.get("capabilities", []),
                            created_at=datetime.fromisoformat(data["created_at"]),
                            updated_at=datetime.fromisoformat(data["updated_at"]),
                            created_by=data["created_by"],
                        )  # type: ignore[call-arg]

                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Error parsing agent status: {e}")

                        continue

        except Exception as e:
            logger.error(f"Error in agent status stream: {e}")

            raise

        finally:
            self.unsubscribe_from_channel(channel, subscriber_id)

            await pubsub.unsubscribe(channel)

            await pubsub.close()

    async def memory_updates_stream(
        self,
        agent_id: UUID,
        subscriber_id: str,
    ) -> AsyncGenerator[MemoryType, None]:
        """Stream new memory updates for an agent."""

        channel = f"memory_updates:{agent_id}"

        try:
            self.subscribe_to_channel(channel, subscriber_id)

            # Create Redis subscription

            pubsub = self.redis_client.pubsub()

            await pubsub.subscribe(channel)

            logger.info(f"Started memory updates stream for agent {agent_id}")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])

                        # Convert to MemoryType

                        yield MemoryType(
                            id=UUID(data["id"]),
                            agent_id=UUID(data["agent_id"]),
                            content=data["content"],
                            memory_type=data["memory_type"],
                            importance_score=float(data["importance_score"]),
                            created_at=datetime.fromisoformat(data["created_at"]),
                            accessed_at=datetime.fromisoformat(data["accessed_at"])
                            if data.get("accessed_at")
                            else None,
                            metadata=data.get("metadata"),
                        )  # type: ignore[call-arg]

                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Error parsing memory update: {e}")

                        continue

        except Exception as e:
            logger.error(f"Error in memory updates stream: {e}")

            raise

        finally:
            self.unsubscribe_from_channel(channel, subscriber_id)

            await pubsub.unsubscribe(channel)

            await pubsub.close()

    async def system_events_stream(
        self,
        subscriber_id: str,
        event_types: list[str] | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Stream system-wide events."""

        channel = "system_events"

        try:
            self.subscribe_to_channel(channel, subscriber_id)

            # Create Redis subscription

            pubsub = self.redis_client.pubsub()

            await pubsub.subscribe(channel)

            logger.info(f"Started system events stream for subscriber {subscriber_id}")

            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        data = json.loads(message["data"])

                        # Filter by event types if specified

                        if event_types and data.get("event_type") not in event_types:
                            continue

                        yield data

                    except (json.JSONDecodeError, KeyError) as e:
                        logger.error(f"Error parsing system event: {e}")

                        continue

        except Exception as e:
            logger.error(f"Error in system events stream: {e}")

            raise

        finally:
            self.unsubscribe_from_channel(channel, subscriber_id)

            await pubsub.unsubscribe(channel)

            await pubsub.close()

    def cleanup_subscriber(self, subscriber_id: str) -> None:
        """Clean up all subscriptions for a subscriber."""

        channels_to_remove = []

        for channel, subscribers in self._subscribers.items():
            if subscriber_id in subscribers:
                subscribers.discard(subscriber_id)

                if not subscribers:
                    channels_to_remove.append(channel)

        for channel in channels_to_remove:
            del self._subscribers[channel]

        logger.info(f"Cleaned up subscriptions for subscriber {subscriber_id}")


class SubscriptionEventPublisher:
    """Publishes events to subscription channels."""

    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    async def publish_chat_message(
        self,
        chat_id: UUID,
        message_id: UUID,
        content: str,
        role: str,
        timestamp: datetime,
        metadata: str | None = None,
    ) -> None:
        """Publish a new chat message."""

        channel = f"chat_messages:{chat_id}"

        message = {
            "id": str(message_id),
            "chat_id": str(chat_id),
            "content": content,
            "role": role,
            "timestamp": timestamp.isoformat(),
            "metadata": metadata,
        }

        await self._publish(channel, message)

    async def publish_agent_status_update(
        self,
        agent: Agent,
    ) -> None:
        """Publish agent status update."""

        channel = f"agent_status:{agent.id}"

        message = {
            "id": str(agent.id),
            "name": agent.name,
            "description": agent.description,
            "model_type": getattr(agent, "model_type", "unknown"),
            "status": agent.status.value
            if hasattr(agent.status, "value")
            else str(agent.status),
            "capabilities": getattr(agent, "capabilities", []),
            "created_at": agent.created_at.isoformat(),
            "updated_at": agent.updated_at.isoformat(),
            "created_by": getattr(agent, "created_by", "unknown"),
        }

        await self._publish(channel, message)

    async def publish_memory_update(
        self,
        memory: Memory,
    ) -> None:
        """Publish memory update."""

        channel = f"memory_updates:{getattr(memory, 'agent_id', 'unknown')}"

        message = {
            "id": str(memory.id),
            "agent_id": str(getattr(memory, "agent_id", "unknown")),
            "content": memory.content,
            "memory_type": getattr(memory, "memory_type", "unknown"),
            "importance_score": getattr(memory, "importance_score", 0.5),
            "created_at": memory.created_at.isoformat(),
            "accessed_at": getattr(memory, "accessed_at", datetime.now()).isoformat(),
            "metadata": getattr(memory, "metadata", None),
        }

        await self._publish(channel, message)

    async def publish_system_event(
        self,
        event_type: str,
        data: dict[str, Any],
    ) -> None:
        """Publish system event."""

        channel = "system_events"

        message = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
        }

        await self._publish(channel, message)

    async def _publish(self, channel: str, message: dict[str, Any]) -> None:
        """Internal method to publish to Redis."""

        try:
            await self.redis_client.publish(channel, json.dumps(message, default=str))

            logger.debug(f"Published to {channel}: {message}")

        except Exception as e:
            logger.error(f"Error publishing to {channel}: {e}")


# Global subscription manager instance (will be initialized in app startup)


subscription_manager: SubscriptionManager | None = None


event_publisher: SubscriptionEventPublisher | None = None


def get_subscription_manager() -> SubscriptionManager:
    """Get the global subscription manager."""

    if subscription_manager is None:
        raise RuntimeError("Subscription manager not initialized")

    return subscription_manager


def get_event_publisher() -> SubscriptionEventPublisher:
    """Get the global event publisher."""

    if event_publisher is None:
        raise RuntimeError("Event publisher not initialized")

    return event_publisher


def initialize_subscriptions(
    redis_client: redis.Redis,
    agent_repository: AgentRepository,
    chat_repository: ChatRepository,
    memory_repository: MemoryRepository,
) -> None:
    """Initialize global subscription manager and event publisher."""

    global subscription_manager, event_publisher

    subscription_manager = SubscriptionManager(
        redis_client=redis_client,
        agent_repository=agent_repository,
        chat_repository=chat_repository,
        memory_repository=memory_repository,
    )

    event_publisher = SubscriptionEventPublisher(redis_client)

    logger.info("GraphQL subscriptions initialized")


def cleanup_subscriptions() -> None:
    """Clean up subscription resources."""

    global subscription_manager, event_publisher

    subscription_manager = None

    event_publisher = None

    logger.info("GraphQL subscriptions cleaned up")


__all__ = [
    "SubscriptionEventPublisher",
    "SubscriptionManager",
    "cleanup_subscriptions",
    "get_event_publisher",
    "get_subscription_manager",
    "initialize_subscriptions",
]
