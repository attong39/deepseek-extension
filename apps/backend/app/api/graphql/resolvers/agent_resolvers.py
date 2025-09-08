"""GraphQL resolvers cho Agent operations.

Production-ready resolvers với comprehensive error handling,
validation, và performance optimization.
"""

from __future__ import annotations

import logging
from uuid import UUID

import strawberry
from app.api.graphql.schema import (
import Exception
import PermissionError
import ValueError
import bool
import e
import id
import info
import input
import int
import len
import limit
import list
import offset
import owner_id
import status
import str
    AgentType,
    CreateAgentInput,
    UpdateAgentInput,
)
from apps.backend.core.exceptions.validation_exceptions import ValidationError
from apps.backend.core.use_cases.agent.create_agent import CreateAgent
from apps.backend.core.use_cases.agent.get_agent import GetAgent
from apps.backend.core.use_cases.agent.update_agent import UpdateAgent

logger = logging.getLogger(__name__)


@strawberry.type
class AgentResolvers:
    """GraphQL resolvers cho Agent-related operations."""

    @strawberry.mutation
    async def create_agent(
        self,
        input: CreateAgentInput,
        info: strawberry.Info,
    ) -> AgentType:
        """Create a new agent với validation và error handling.

        Args:
            input: Agent creation input
            info: GraphQL resolver info

        Returns:
            Created agent

        Raises:
            ValidationError: If input validation fails
            PermissionError: If user lacks create permissions
        """
        try:
            # Get dependencies from context
            container = info.context.get("container")
            if not container:
                raise ValueError("Missing dependency container")

            current_user = current_user = info.context.get("current_user")
            if not current_user:
                raise PermissionError("Authentication required")

            # Validate input
            if not input.name or len(input.name) < 2:
                raise ValidationError("Agent name must be at least 2 characters")

            if input.model_type not in ["gpt-4", "gpt-3.5-turbo", "claude-3"]:
                raise ValidationError(f"Unsupported model type: {input.model_type}")

            # Get use case
            agent_repo = await container.get_agent_repository()
            create_agent_use_case = CreateAgent(agent_repo)

            # Execute use case
            agent_data = {
                "name": input.name,
                "description": input.description,
                "model_type": input.model_type,
                "capabilities": input.capabilities,
                "owner_id": current_user.id,
                "status": "active",
            }

            created_agent = await create_agent_use_case.execute(agent_data)

            # Convert to GraphQL type
            return AgentType(
                id=created_agent.id,
                name=created_agent.name,
                description=created_agent.description,
                model_type=created_agent.model_type,
                capabilities=created_agent.capabilities,
                status=created_agent.status,
                owner_id=created_agent.owner_id,
                created_at=created_agent.created_at,
                updated_at=created_agent.updated_at,
            )

        except ValidationError as e:
            logger.warning(f"Agent creation validation error: {e}")
            raise

        except PermissionError as e:
            logger.warning(f"Agent creation permission error: {e}")
            raise

        except Exception as e:
            logger.error(f"Agent creation error: {e}")
            raise ValueError(f"Failed to create agent: {str(e)}")

    @strawberry.mutation
    async def update_agent(
        self,
        id: UUID,
        input: UpdateAgentInput,
        info: strawberry.Info,
    ) -> AgentType | None:
        """Update an existing agent.

        Args:
            id: Agent ID to update
            input: Update input data
            info: GraphQL resolver info

        Returns:
            Updated agent or None if not found

        Raises:
            ValidationError: If input validation fails
            PermissionError: If user lacks update permissions
        """
        try:
            # Get dependencies
            container = info.context.get("container")
            current_user = info.context.get("current_user")

            if not container or not current_user:
                raise PermissionError("Authentication required")

            # Get repositories and use cases
            agent_repo = await container.get_agent_repository()
            get_agent_use_case = GetAgent(agent_repo)
            update_agent_use_case = UpdateAgent(agent_repo)

            # Check if agent exists and user has permission
            existing_agent = await get_agent_use_case.execute(str(id))
            if not existing_agent:
                return None

            if existing_agent.owner_id != current_user.id and not current_user.is_admin:
                raise PermissionError("You can only update your own agents")

            # Validate input
            update_data = {}
            if input.name is not None:
                if len(input.name) < 2:
                    raise ValidationError("Agent name must be at least 2 characters")
                update_data["name"] = input.name

            if input.description is not None:
                update_data["description"] = input.description

            if input.status is not None:
                if input.status not in ["active", "inactive", "suspended"]:
                    raise ValidationError(f"Invalid status: {input.status}")
                update_data["status"] = input.status

            if input.capabilities is not None:
                update_data["capabilities"] = input.capabilities

            # Execute update
            updated_agent = await update_agent_use_case.execute(str(id), update_data)

            return AgentType(
                id=updated_agent.id,
                name=updated_agent.name,
                description=updated_agent.description,
                model_type=updated_agent.model_type,
                capabilities=updated_agent.capabilities,
                status=updated_agent.status,
                owner_id=updated_agent.owner_id,
                created_at=updated_agent.created_at,
                updated_at=updated_agent.updated_at,
            )

        except ValidationError as e:
            logger.warning(f"Agent update validation error: {e}")
            raise

        except PermissionError as e:
            logger.warning(f"Agent update permission error: {e}")
            raise

        except Exception as e:
            logger.error(f"Agent update error: {e}")
            raise ValueError(f"Failed to update agent: {str(e)}")

    @strawberry.mutation
    async def delete_agent(
        self,
        id: UUID,
        info: strawberry.Info,
    ) -> bool:
        """Delete an agent (soft delete).

        Args:
            id: Agent ID to delete
            info: GraphQL resolver info

        Returns:
            True if successfully deleted, False if not found

        Raises:
            PermissionError: If user lacks delete permissions
        """
        try:
            # Get dependencies
            container = info.context.get("container")
            current_user = info.context.get("current_user")

            if not container or not current_user:
                raise PermissionError("Authentication required")

            # Get repositories and use cases
            agent_repo = await container.get_agent_repository()
            get_agent_use_case = GetAgent(agent_repo)

            # Check if agent exists and user has permission
            _existing_agent = await get_agent_use_case.execute(str(id))
            existing_agent = _existing_agent
            if not existing_agent:
                return False

            if existing_agent.owner_id != current_user.id and not current_user.is_admin:
                raise PermissionError("You can only delete your own agents")

            # Soft delete
            await agent_repo.delete(str(id))

            logger.info(f"Agent {id} deleted by user {current_user.id}")
            return True

        except PermissionError as e:
            logger.warning(f"Agent deletion permission error: {e}")
            raise

        except Exception as e:
            logger.error(f"Agent deletion error: {e}")
            return False

    @strawberry.field
    async def agents(
        self,
        info: strawberry.Info,
        limit: int = 10,
        offset: int = 0,
        status: str | None = None,
        owner_id: str | None = None,
    ) -> list[AgentType]:
        """Get list of agents với filtering và pagination.

        Args:
            info: GraphQL resolver info
            limit: Maximum number of agents to return
            offset: Number of agents to skip
            status: Filter by status
            owner_id: Filter by owner

        Returns:
            List of agents matching criteria
        """
        try:
            # Get dependencies
            container = info.context.get("container")
            current_user = info.context.get("current_user")

            if not container or not current_user:
                return []

            # Get repository
            agent_repo = await container.get_agent_repository()

            # Build filters
            filters = {}
            if status:
                filters["status"] = status
            if owner_id:
                filters["owner_id"] = owner_id
            elif not current_user.is_admin:
                # Non-admin users can only see their own agents
                filters["owner_id"] = current_user.id

            # Fetch agents
            agents = await agent_repo.get_all(skip=offset, limit=limit, filters=filters)

            # Convert to GraphQL types
            return [
                AgentType(
                    id=agent.id,
                    name=agent.name,
                    description=agent.description,
                    model_type=agent.model_type,
                    capabilities=agent.capabilities,
                    status=agent.status,
                    owner_id=agent.owner_id,
                    created_at=agent.created_at,
                    updated_at=agent.updated_at,
                )
                for agent in agents
            ]

        except Exception as e:
            logger.error(f"Error fetching agents: {e}")
            return []

    @strawberry.field
    async def agent(
        self,
        info: strawberry.Info,
        id: UUID,
    ) -> AgentType | None:
        """Get single agent by ID.

        Args:
            info: GraphQL resolver info
            id: Agent ID

        Returns:
            Agent if found and accessible, None otherwise
        """
        try:
            # Get dependencies
            container = info.context.get("container")
            current_user = info.context.get("current_user")

            if not container or not current_user:
                return None

            # Get use case
            agent_repo = await container.get_agent_repository()
            get_agent_use_case = GetAgent(agent_repo)

            # Fetch agent
            agent = await get_agent_use_case.execute(str(id))
            if not agent:
                return None

            # Check permissions
            if agent.owner_id != current_user.id and not current_user.is_admin:
                return None  # Don't reveal existence of other users' agents

            return AgentType(
                id=agent.id,
                name=agent.name,
                description=agent.description,
                model_type=agent.model_type,
                capabilities=agent.capabilities,
                status=agent.status,
                owner_id=agent.owner_id,
                created_at=agent.created_at,
                updated_at=agent.updated_at,
            )

        except Exception as e:
            logger.error(f"Error fetching agent {id}: {e}")
            return None


# Singleton instance
agent_resolvers = AgentResolvers()


__all__ = ["AgentResolvers", "agent_resolvers"]
