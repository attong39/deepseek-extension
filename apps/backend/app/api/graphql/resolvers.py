"""GraphQL resolvers for ZETA AI system.





This module implements the actual business logic for GraphQL operations,


connecting the schema to the domain services and use cases.


"""

from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast
from uuid import UUID

from app.api.graphql.schema import (
import Exception
import ValueError
import agent_id
import agent_repository
import bool
import callable
import chat_id
import chat_repository
import current_user_id
import dict
import e
import exc
import filters
import float
import getattr
import id
import info
import input
import int
import is_active
import limit
import list
import m
import memory_repository
import memory_type
import offset
import query
import self
import set
import staticmethod
import status
import str
import u
import updated_agent
import user_id
import user_repository
    AgentType,
    ChatType,
    CreateAgentInput,
    CreateChatInput,
    CreateMemoryInput,
    MemoryType,
    MessageType,
    SendMessageInput,
    UpdateAgentInput,
    UserType,
)
from apps.backend.core.domain.entities.agent import AgentStatus
from apps.backend.core.domain.entities.chat import ChatStatus
from apps.backend.core.domain.entities.memory import MemoryType as DomainMemoryType
from apps.backend.core.domain.entities.user import UserStatus
from apps.backend.core.use_cases.agent.create_agent import CreateAgentUseCase
from apps.backend.core.use_cases.chat.send_message import SendMessageUseCase
from apps.backend.core.use_cases.memory.store_memory import (
    SearchMemories as SearchMemoriesUseCase,
)
from apps.backend.core.use_cases.memory.store_memory import (
    StoreMemory as StoreMemoryUseCase,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from apps.backend.core.domain.entities.agent import Agent
    from apps.backend.core.domain.entities.chat import Chat
    from apps.backend.core.domain.entities.memory import Memory
    from apps.backend.core.domain.entities.user import User
    from apps.backend.core.interfaces.repositories import (
        AgentRepository,
        ChatRepository,
        MemoryRepository,
        UserRepository,
    )
    from strawberry.types import Info


logger = logging.getLogger(__name__)


class GraphQLContext:
    """GraphQL context containing dependencies."""

    def __init__(
        self,
        agent_repository: AgentRepository,
        chat_repository: ChatRepository,
        memory_repository: MemoryRepository,
        user_repository: UserRepository,
        current_user_id: str | None = None,
    ):
        self.agent_repository = agent_repository

        self.chat_repository = chat_repository

        self.memory_repository = memory_repository

        self.user_repository = user_repository

        self.current_user_id = current_user_id


def _convert_agent_to_graphql(agent: Agent) -> AgentType:
    """Convert domain Agent to GraphQL AgentType."""

    return AgentType(
        id=agent.id,
        name=agent.name,
        description=getattr(agent, "description", None),
        model_type=getattr(agent, "model", "unknown"),
        status=agent.status.value,
        capabilities=list(getattr(agent, "capabilities", [])),
        created_at=agent.created_at,
        updated_at=agent.updated_at,
        created_by=str(getattr(agent, "owner_id", "system")),
    )  # type: ignore[call-arg]


def _convert_chat_to_graphql(chat: Chat) -> ChatType:
    """Convert domain Chat to GraphQL ChatType."""

    return ChatType(
        id=chat.id,
        agent_id=chat.agent_id or UUID(int=0),
        user_id=str(chat.user_id) if chat.user_id else "",
        title=chat.title,
        status=chat.status.value,
        created_at=chat.created_at,
        updated_at=chat.updated_at,
    )  # type: ignore[call-arg]


def _convert_memory_to_graphql(memory: Memory) -> MemoryType:
    """Convert domain Memory to GraphQL MemoryType."""

    def _importance_to_score(importance: Any) -> float:
        try:
            val = getattr(importance, "value", importance)
            mapping = {
                "low": 0.25,
                "medium": 0.5,
                "high": 0.75,
                "critical": 0.95,
            }
            return float(mapping.get(str(val), 0.5))
        except Exception:
            return 0.5

    import json as _json  # noqa: PLC0415

    return MemoryType(
        id=memory.id,
        agent_id=memory.agent_id or UUID(int=0),
        content=memory.content,
        memory_type=memory.type.value,
        importance_score=_importance_to_score(getattr(memory, "importance", None)),
        created_at=memory.created_at,
        accessed_at=getattr(memory, "last_accessed", None),
        metadata=_json.dumps(getattr(memory, "context", {}))
        if getattr(memory, "context", None)
        else None,
    )  # type: ignore[call-arg]


def _convert_user_to_graphql(user: User) -> UserType:
    """Convert domain User to GraphQL UserType."""

    # Determine active status robustly across legacy variants
    active = False
    try:
        if callable(getattr(user, "is_active", None)):
            active = bool(user.is_active())  # type: ignore[misc]
    except Exception:
        active = False
    if not active:
        try:
            active = getattr(user, "status", None) == UserStatus.ACTIVE
        except Exception:
            active = False

    return UserType(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=active,
        created_at=user.created_at,
        last_login=user.last_login,
    )  # type: ignore[call-arg]


class QueryResolver:
    """Resolver for GraphQL queries."""

    @staticmethod
    async def agents(
        info: Info[GraphQLContext, Any],
        limit: int = 10,
        offset: int = 0,
        status: str | None = None,
    ) -> list[AgentType]:
        """Get list of agents."""

        try:
            context = info.context

            agents: list[Agent] = []
            if status:
                try:
                    agents = await context.agent_repository.list_by_status(  # type: ignore[arg-type]
                        AgentStatus(status)
                    )
                except Exception:
                    agents = []
            else:
                # Try dynamic list_all if repository supports it
                repo_any = cast("Any", context.agent_repository)
                try:
                    agents = await repo_any.list_all(offset=offset, limit=limit)
                except Exception:
                    # Fallback: if current user available, try get_by_owner
                    try:
                        if context.current_user_id:
                            agents = await context.agent_repository.get_by_owner(
                                UUID(str(context.current_user_id))
                            )
                    except Exception:
                        agents = []

            return [_convert_agent_to_graphql(agent) for agent in agents]

        except Exception as e:
            logger.error(f"Error fetching agents: {e}")

            raise

    @staticmethod
    async def agent(
        info: Info[GraphQLContext, Any],
        id: UUID,
    ) -> AgentType | None:
        """Get agent by ID."""

        try:
            context = info.context

            _ = await context.agent_repository.get_by_id(id)

            if not agent:
                return None

            return _convert_agent_to_graphql(agent)

        except Exception as e:
            logger.error(f"Error fetching agent {id}: {e}")

            raise

    @staticmethod
    async def chats(
        info: Info[GraphQLContext, Any],
        agent_id: UUID | None = None,
        user_id: str | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[ChatType]:
        """Get list of chats."""

        try:
            context = info.context

            chats: list[Chat] = []
            if agent_id:
                try:
                    chats = await context.chat_repository.get_by_agent(agent_id)
                except Exception:
                    chats = []
            else:
                repo_any = cast("Any", context.chat_repository)
                # Try dynamic list_all with optional filters
                try:
                    filters: dict[str, Any] = {}
                    if user_id:
                        filters["user_id"] = user_id
                    chats = await repo_any.list_all(
                        offset=offset, limit=limit, filters=filters
                    )
                except Exception:
                    # Try get_by_user if available
                    try:
                        if user_id:
                            chats = await repo_any.get_by_user(user_id)
                    except Exception:
                        chats = []

            return [_convert_chat_to_graphql(chat) for chat in chats]

        except Exception as e:
            logger.error(f"Error fetching chats: {e}")

            raise

    @staticmethod
    async def chat(
        info: Info[GraphQLContext, Any],
        id: UUID,
    ) -> ChatType | None:
        """Get chat by ID."""

        try:
            context = info.context

            chat = await context.chat_repository.get_by_id(id)

            if not chat:
                return None

            return _convert_chat_to_graphql(chat)

        except Exception as e:
            logger.error(f"Error fetching chat {id}: {e}")

            raise

    @staticmethod
    async def memories(
        info: Info[GraphQLContext, Any],
        agent_id: UUID,
        memory_type: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[MemoryType]:
        """Get agent memories."""

        try:
            context = info.context

            # Use supported repository API: get_by_agent, then filter by type if provided
            try:
                memories = await context.memory_repository.get_by_agent(agent_id)
            except Exception:
                # Dynamic fallback to list_all if available
                repo_any = cast("Any", context.memory_repository)
                try:
                    memories = await repo_any.list_all(
                        offset=offset, limit=limit, filters={"agent_id": agent_id}
                    )
                except Exception:
                    memories = []

            if memory_type:
                try:
                    mt = DomainMemoryType(memory_type)
                    memories = [m for m in memories if getattr(m, "type", None) == mt]
                except Exception as exc:
                    logger.debug("Invalid memory_type filter %s: %s", memory_type, exc)

            # Apply offset/limit manually if needed
            sliced = memories[offset : offset + limit]
            return [_convert_memory_to_graphql(memory) for memory in sliced]

        except Exception as e:
            logger.error(f"Error fetching memories for agent {agent_id}: {e}")

            raise

    @staticmethod
    async def search_memories(
        info: Info[GraphQLContext, Any],
        agent_id: UUID,
        query: str,
        limit: int = 10,
    ) -> list[MemoryType]:
        """Search memories by content."""

        try:
            context = info.context

            # Use SearchMemories use case to be compatible with varying repos
            search_uc = SearchMemoriesUseCase(context.memory_repository)
            memories = await search_uc(query=query, agent_id=agent_id, limit=limit)
            return [_convert_memory_to_graphql(memory) for memory in memories]

        except Exception as e:
            logger.error(f"Error searching memories for agent {agent_id}: {e}")

            raise

    @staticmethod
    async def users(
        info: Info[GraphQLContext, Any],
        limit: int = 10,
        offset: int = 0,
        is_active: bool | None = None,
    ) -> list[UserType]:
        """Get list of users."""

        try:
            context = info.context

            users: list[User] = []
            repo_any = cast("Any", context.user_repository)
            try:
                users = await repo_any.list_all(offset=offset, limit=limit)
            except Exception:
                users = []

            if is_active is not None:
                users = [
                    u
                    for u in users
                    if (
                        u.is_active()
                        if callable(getattr(u, "is_active", None))
                        else False
                    )
                    == is_active
                ]

            return [_convert_user_to_graphql(user) for user in users]

        except Exception as e:
            logger.error(f"Error fetching users: {e}")

            raise

    @staticmethod
    async def user(
        info: Info[GraphQLContext, Any],
        id: str,
    ) -> UserType | None:
        """Get user by ID."""

        try:
            context = info.context

            _ = None
            uid: UUID | None = None
            try:
                uid = UUID(str(id))
            except Exception:
                uid = None
            try:
                if uid is not None:
                    _ = await context.user_repository.get_by_id(uid)
                else:
                    # Fallback to dynamic repo accepting string ids
                    repo_any = cast("Any", context.user_repository)
                    _ = await repo_any.get_by_id(id)
            except Exception:
                _ = None

            if not user:
                return None

            return _convert_user_to_graphql(user)

        except Exception as e:
            logger.error(f"Error fetching user {id}: {e}")

            raise


class MutationResolver:
    """Resolver for GraphQL mutations."""

    @staticmethod
    async def create_agent(
        info: Info[GraphQLContext, Any],
        input: CreateAgentInput,
    ) -> AgentType:
        """Create a new agent."""

        try:
            context = info.context

            # Use CreateAgentUseCase with explicit parameters
            use_case = CreateAgentUseCase(context.agent_repository)

            owner_uuid = None
            try:
                if context.current_user_id:
                    owner_uuid = UUID(str(context.current_user_id))
            except Exception:
                owner_uuid = None

            _ = await use_case.execute(
                name=input.name,
                description=input.description,
                config={},
                owner_id=owner_uuid,
                capabilities=input.capabilities,
            )

            return _convert_agent_to_graphql(agent)

        except Exception as e:
            logger.error(f"Error creating agent: {e}")

            raise

    @staticmethod
    async def update_agent(
        info: Info[GraphQLContext, Any],
        id: UUID,
        input: UpdateAgentInput,
    ) -> AgentType | None:
        """Update an existing agent."""

        try:
            context = info.context

            # Get existing agent

            _ = await context.agent_repository.get_by_id(id)

            if not agent:
                return None

            # Update fields

            if input.name is not None:
                agent.name = input.name

            if input.description is not None:
                agent.description = input.description

            if input.status is not None:
                agent.status = AgentStatus(input.status)

            if input.capabilities is not None:
                agent.capabilities = set(input.capabilities)

            # Save changes

            await context.agent_repository.update(agent)

            return _convert_agent_to_graphql(updated_agent)

        except Exception as e:
            logger.error(f"Error updating agent {id}: {e}")

            raise

    @staticmethod
    async def delete_agent(
        info: Info[GraphQLContext, Any],
        id: UUID,
    ) -> bool:
        """Delete an agent."""

        try:
            context = info.context

            # Repository may return Any; ensure boolean for GraphQL contract
            return bool(await context.agent_repository.delete(id))

        except Exception as e:
            logger.error(f"Error deleting agent {id}: {e}")

            raise

    @staticmethod
    async def create_chat(
        info: Info[GraphQLContext, Any],
        input: CreateChatInput,
    ) -> ChatType:
        """Create a new chat."""

        try:
            context = info.context

            # Create chat directly using repository interface
            from uuid import uuid4  # noqa: PLC0415

            from apps.backend.core.domain.entities.chat import Chat  # noqa: PLC0415

            user_uuid: UUID | None = None
            try:
                if context.current_user_id:
                    user_uuid = UUID(str(context.current_user_id))
            except Exception:
                user_uuid = None

            chat = Chat(
                id=uuid4(),
                agent_id=input.agent_id,
                user_id=user_uuid,
                title=input.title or "",
                status=ChatStatus.ACTIVE,
            )

            created = await context.chat_repository.create(chat)
            return _convert_chat_to_graphql(created)

        except Exception as e:
            logger.error(f"Error creating chat: {e}")

            raise

    @staticmethod
    async def send_message(
        info: Info[GraphQLContext, Any],
        input: SendMessageInput,
    ) -> MessageType:
        """Send a message in a chat."""

        try:
            context = info.context

            # Resolve chat to get agent_id, then send message
            chat = await context.chat_repository.get_by_id(input.chat_id)
            if not chat:
                raise ValueError(f"Chat not found: {input.chat_id}")

            use_case = SendMessageUseCase(context.chat_repository)
            message = await use_case.execute(
                agent_id=str(chat.agent_id or ""),
                content=input.content,
                user_id=context.current_user_id,
            )

            import json as _json  # noqa: PLC0415

            return MessageType(
                id=message.id,
                chat_id=message.chat_id,
                content=message.content,
                role=getattr(message.role, "value", str(message.role)),
                timestamp=getattr(message, "timestamp", message.created_at),
                metadata=_json.dumps(message.metadata)
                if getattr(message, "metadata", None)
                else None,
            )  # type: ignore[call-arg]

        except Exception as e:
            logger.error(f"Error sending message: {e}")

            raise

    @staticmethod
    async def create_memory(
        info: Info[GraphQLContext, Any],
        input: CreateMemoryInput,
    ) -> MemoryType:
        """Create a new memory."""

        try:
            context = info.context

            # Use StoreMemoryUseCase
            use_case = StoreMemoryUseCase(context.memory_repository)

            # Map numeric importance_score to categorical importance
            score = input.importance_score or 0.5
            if score >= 0.9:
                importance = "critical"
            elif score >= 0.75:
                importance = "high"
            elif score >= 0.5:
                importance = "medium"
            else:
                importance = "low"

            memory = await use_case(
                content=input.content,
                memory_type=input.memory_type,
                importance=importance,
                agent_id=input.agent_id,
                context={},
                tags=None,
            )

            return _convert_memory_to_graphql(memory)

        except Exception as e:
            logger.error(f"Error creating memory: {e}")

            raise

    @staticmethod
    async def delete_memory(
        info: Info[GraphQLContext, Any],
        id: UUID,
    ) -> bool:
        """Delete a memory."""

        try:
            context = info.context

            # Repository may return Any; ensure boolean for GraphQL contract
            return bool(await context.memory_repository.delete(id))

        except Exception as e:
            logger.error(f"Error deleting memory {id}: {e}")

            raise


class SubscriptionResolver:
    """Resolver for GraphQL subscriptions."""

    @staticmethod
    async def chat_messages(
        info: Info[GraphQLContext, Any],
        chat_id: UUID,
    ) -> AsyncGenerator[MessageType, None]:
        """Subscribe to new messages in a chat."""

        try:
            # In a real implementation, this would connect to a message broker

            # or WebSocket stream to get real-time updates

            # Mock implementation - yield periodic updates

            # touch context so 'info' isn't unused
            _ = info.context

            while True:
                await asyncio.sleep(1)

                # In reality, you'd check for new messages and yield them

                # This is just a placeholder

                yield MessageType(
                    id=UUID("00000000-0000-0000-0000-000000000000"),
                    chat_id=chat_id,
                    content="Real-time message update",
                    role="assistant",
                    timestamp=datetime.now(UTC),
                    metadata=None,
                )  # type: ignore[call-arg]

        except Exception as e:
            logger.error(f"Error in chat messages subscription: {e}")

            raise

    @staticmethod
    async def agent_status(
        info: Info[GraphQLContext, Any],
        agent_id: UUID,
    ) -> AsyncGenerator[AgentType, None]:
        """Subscribe to agent status changes."""

        try:
            # Mock implementation

            while True:
                await asyncio.sleep(5)

                # Get current agent status

                context = info.context

                _ = await context.agent_repository.get_by_id(agent_id)

                if agent:
                    yield _convert_agent_to_graphql(agent)

        except Exception as e:
            logger.error(f"Error in agent status subscription: {e}")

            raise

    @staticmethod
    async def memory_updates(
        info: Info[GraphQLContext, Any],
        agent_id: UUID,
    ) -> AsyncGenerator[MemoryType, None]:
        """Subscribe to new memories for an agent."""

        try:
            # Mock implementation

            # touch context so 'info' isn't unused
            _ = info.context

            while True:
                await asyncio.sleep(10)

                # In reality, you'd listen for new memory events

                yield MemoryType(
                    id=UUID("00000000-0000-0000-0000-000000000000"),
                    agent_id=agent_id,
                    content="New memory created",
                    memory_type="episodic",
                    importance_score=0.5,
                    created_at=datetime.now(UTC),
                    accessed_at=None,
                    metadata=None,
                )  # type: ignore[call-arg]

        except Exception as e:
            logger.error(f"Error in memory updates subscription: {e}")

            raise


# Export resolvers


query_resolver = QueryResolver()


mutation_resolver = MutationResolver()


subscription_resolver = SubscriptionResolver()


__all__ = [
    "GraphQLContext",
    "MutationResolver",
    "QueryResolver",
    "SubscriptionResolver",
    "mutation_resolver",
    "query_resolver",
    "subscription_resolver",
]
