from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

import strawberry
from app.api.graphql.core.dataloader import get_dataloader_registry
from app.api.graphql.directives import (
import Exception
import bool
import dict
import e
import float
import getattr
import id
import info
import input
import int
import limit
import list
import offset
import owner_id
import self
import status
import str
    cache_field,
    monitor_performance,
    require_auth,
)
from app.api.graphql.resolvers.agent_resolvers import agent_resolvers
from pydantic import BaseModel, Field

"""High-performance GraphQL schema với consolidated types và optimizations.
Consolidated schema để achieve sub-100ms response times với:
- Type-safe definitions với Pydantic v2
- Efficient field resolution
- Smart caching integration
- Performance monitoring
"""


class CreateAgentInput(BaseModel):
    """Validated input for agent creation."""

    name: str = Field(min_length=2, max_length=100, description="Agent name")
    description: str | None = Field(
        default=None, max_length=500, description="Agent description"
    )
    model_type: str = Field(
        pattern=r"^(gpt-4|gpt-3\.5-turbo|claude-3)$", description="AI model type"
    )
    capabilities: list[str] = Field(
        default_factory=list, max_items=10, description="Agent capabilities"
    )


class UpdateAgentInput(BaseModel):
    """Validated input for agent updates."""

    name: str | None = Field(
        default=None, min_length=2, max_length=100, description="Updated name"
    )
    description: str | None = Field(
        default=None, max_length=500, description="Updated description"
    )
    status: str | None = Field(
        default=None,
        pattern=r"^(active|inactive|suspended)$",
        description="Updated status",
    )
    capabilities: list[str] | None = Field(
        default=None, max_items=10, description="Updated capabilities"
    )


@strawberry.input
class CreateAgentInputGQL:
    """GraphQL input for creating agents."""

    name: str
    description: str | None = None
    model_type: str
    capabilities: list[str] = strawberry.field(default_factory=list)


@strawberry.input
class UpdateAgentInputGQL:
    """GraphQL input for updating agents."""

    name: str | None = None
    description: str | None = None
    status: str | None = None
    capabilities: list[str] | None = None


@strawberry.type
class AgentType:
    """High-performance Agent GraphQL type với optimized field resolution."""

    id: UUID
    name: str
    description: str | None
    model_type: str
    status: str
    capabilities: list[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    @cache_field(ttl=60)
    @monitor_performance(warn_threshold=50)
    async def conversations(self, info: strawberry.Info) -> list[ConversationType]:
        """Get agent conversations với caching và performance monitoring.
        Returns:
            List of conversations for this agent
        """
        registry = get_dataloader_registry()
        conversation_loader = registry.get_or_create(
            "conversations_by_agent",
            lambda agent_ids: [],  # Placeholder - sẽ implement actual batch loader
        )
        return await conversation_loader.load(str(self.id))

    @strawberry.field
    @cache_field(ttl=300)
    async def owner(self, info: strawberry.Info) -> UserType | None:
        """Get agent owner với efficient loading.
        Returns:
            Owner user information
        """
        registry = get_dataloader_registry()
        user_loader = registry.get_or_create(
            "users_by_id",
            lambda user_ids: [],  # Placeholder
        )
        return await user_loader.load(self.owner_id)

    @strawberry.field
    @monitor_performance(warn_threshold=30)
    async def usage_stats(self, info: strawberry.Info) -> AgentUsageStats:
        """Get agent usage statistics.
        Returns:
            Usage statistics for this agent
        """
        return AgentUsageStats(
            total_conversations=0,
            total_messages=0,
            last_used=None,
            avg_response_time=0.0,
        )


@strawberry.type
class ConversationType:
    """Conversation entity với efficient field resolution."""

    id: UUID
    title: str
    status: str
    agent_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    @cache_field(ttl=30)
    async def messages(
        self, info: strawberry.Info, limit: int = 50
    ) -> list[MessageType]:
        """Get conversation messages với pagination.
        Args:
            limit: Maximum messages to return
        Returns:
            List of messages trong conversation
        """
        return []

    @strawberry.field
    @cache_field(ttl=60)
    async def agent(self, info: strawberry.Info) -> AgentType | None:
        """Get associated agent.
        Returns:
            Agent that owns this conversation
        """
        registry = get_dataloader_registry()
        agent_loader = registry.get_or_create(
            "agents_by_id",
            lambda agent_ids: [],
        )
        return await agent_loader.load(self.agent_id)


@strawberry.type
class MessageType:
    """Message entity với optimized loading."""

    id: UUID
    content: str
    role: str  # user, assistant, system
    conversation_id: str
    created_at: datetime
    metadata: dict[str, Any] = strawberry.field(default_factory=dict)


@strawberry.type
class UserType:
    """User entity với efficient field resolution."""

    id: str
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    @strawberry.field
    @cache_field(ttl=120)
    async def agents(self, info: strawberry.Info) -> list[AgentType]:
        """Get user's agents.
        Returns:
            List of agents owned by user
        """
        return []


@strawberry.type
class AgentUsageStats:
    """Agent usage statistics."""

    total_conversations: int
    total_messages: int
    last_used: datetime | None
    avg_response_time: float


@strawberry.type
class SystemStats:
    """System-wide statistics."""

    total_agents: int
    total_conversations: int
    total_messages: int
    active_users: int
    avg_response_time: float
    cache_hit_rate: float


@strawberry.type
class GraphQLError:
    """Structured error type."""

    message: str
    code: str
    field: str | None = None
    details: dict[str, Any] = strawberry.field(default_factory=dict)


@strawberry.type
class AgentResult:
    """Agent mutation result với error handling."""

    agent: AgentType | None = None
    errors: list[GraphQLError] = strawberry.field(default_factory=list)
    success: bool = True


@strawberry.type
class ConversationResult:
    """Conversation mutation result."""

    conversation: ConversationType | None = None
    errors: list[GraphQLError] = strawberry.field(default_factory=list)
    success: bool = True


@strawberry.type
class Query:
    """Optimized GraphQL queries với performance monitoring."""

    @strawberry.field
    @require_auth()
    @monitor_performance(warn_threshold=100)
    async def agents(
        self,
        info: strawberry.Info,
        limit: int = 10,
        offset: int = 0,
        status: str | None = None,
        owner_id: str | None = None,
    ) -> list[AgentType]:
        """Get paginated agents với filtering."""
        return await agent_resolvers.agents(info, limit, offset, status, owner_id)

    @strawberry.field
    @require_auth()
    @monitor_performance(warn_threshold=50)
    async def agent(self, info: strawberry.Info, id: UUID) -> AgentType | None:
        """Get single agent by ID."""
        return await agent_resolvers.agent(info, id)

    @strawberry.field
    @require_auth()
    @cache_field(ttl=30)
    async def me(self, info: strawberry.Info) -> UserType | None:
        """Get current user information."""
        current_user = info.context.get("current_user")
        if not current_user:
            return None
        return UserType(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            is_admin=getattr(current_user, "is_admin", False),
            created_at=current_user.created_at,
        )

    @strawberry.field
    @require_auth(roles=["admin"])
    @cache_field(ttl=60)
    async def system_stats(self, info: strawberry.Info) -> SystemStats:
        """Get system statistics (admin only)."""
        return SystemStats(
            total_agents=0,
            total_conversations=0,
            total_messages=0,
            active_users=0,
            avg_response_time=0.0,
            cache_hit_rate=0.0,
        )


@strawberry.type
class Mutation:
    """Optimized GraphQL mutations với validation và error handling."""

    @strawberry.mutation
    @require_auth()
    @monitor_performance(warn_threshold=200)
    async def create_agent(
        self, info: strawberry.Info, input: CreateAgentInputGQL
    ) -> AgentResult:
        """Create new agent với comprehensive validation."""
        try:
            create_input = CreateAgentInput(
                name=input.name,
                description=input.description,
                model_type=input.model_type,
                capabilities=input.capabilities,
            )
            agent = await agent_resolvers.create_agent(create_input, info)
            return AgentResult(agent=agent, success=True)
        except Exception as e:
            error = GraphQLError(
                message=str(e),
                code="CREATION_FAILED",
                field="input",
            )
            return AgentResult(errors=[error], success=False)

    @strawberry.mutation
    @require_auth()
    @monitor_performance(warn_threshold=150)
    async def update_agent(
        self,
        info: strawberry.Info,
        id: UUID,
        input: UpdateAgentInputGQL,
    ) -> AgentResult:
        """Update existing agent."""
        try:
            update_input = UpdateAgentInput(
                name=input.name,
                description=input.description,
                status=input.status,
                capabilities=input.capabilities,
            )
            agent = await agent_resolvers.update_agent(id, update_input, info)
            if agent is None:
                error = GraphQLError(
                    message="Agent not found",
                    code="NOT_FOUND",
                    field="id",
                )
                return AgentResult(errors=[error], success=False)
            return AgentResult(agent=agent, success=True)
        except Exception as e:
            error = GraphQLError(
                message=str(e),
                code="UPDATE_FAILED",
                field="input",
            )
            return AgentResult(errors=[error], success=False)

    @strawberry.mutation
    @require_auth()
    @monitor_performance(warn_threshold=100)
    async def delete_agent(self, info: strawberry.Info, id: UUID) -> bool:
        """Delete agent."""
        return await agent_resolvers.delete_agent(id, info)


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    schema_directives=[],
    extensions=[],
)
__all__ = [
    "AgentResult",
    "AgentType",
    "ConversationResult",
    "ConversationType",
    "CreateAgentInputGQL",
    "GraphQLError",
    "MessageType",
    "Mutation",
    "Query",
    "SystemStats",
    "UpdateAgentInputGQL",
    "UserType",
    "schema",
]
