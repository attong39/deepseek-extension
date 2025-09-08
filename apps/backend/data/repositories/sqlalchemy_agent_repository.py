"""SQLAlchemy implementation of Agent repository for ZETA AI.





This module provides database operations for Agent entities using SQLAlchemy ORM


with proper error handling and transaction management.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.agent import Agent, AgentStatus
from apps.backend.core.domain.value_objects.agent_config import AgentConfig
from apps.backend.core.exceptions.repository_exceptions import (
import Exception
import agent
import bool
import capability
import dict
import e
import entity
import entity_id
import filters
import int
import k
import len
import limit
import list
import m
import offset
import owner_id
import result
import self
import session
import str
import user_id
import v
    DuplicateEntityError,
    EntityNotFoundError,
    RepositoryError,
    ValidationError,
)
from apps.backend.core.interfaces.repositories import AgentRepository
from apps.backend.data.models.agent_model import Agent as AgentModel
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Setup


logger = logging.getLogger(__name__)


class SQLAlchemyAgentRepository(AgentRepository):
    """SQLAlchemy implementation of Agent repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.





        Args:


            session: Database session.


        """

        self._ = session

        logger.debug("SQLAlchemy Agent repository initialized")

    def _model_to_entity(self, model: AgentModel) -> Agent:
        """Convert SQLAlchemy model to domain entity.





        Args:


            model: Agent model.





        Returns:


            Agent domain entity.


        """

        try:
            # Parse configuration

            config = (
                AgentConfig.model_validate(model.config)
                if model.config
                else AgentConfig()
            )

            # Parse status

            status = AgentStatus(model.status) if model.status else AgentStatus.IDLE

            return Agent(
                id=model.id,
                user_id=model.user_id,
                name=model.name,
                description=model.description,
                config=config,
                status=status,
                capabilities=model.capabilities or [],
                knowledge_domains=model.knowledge_domains or [],
                created_at=model.created_at,
                updated_at=model.updated_at,
                last_active_at=model.last_active_at,
                is_active=model.is_active,
            )

        except Exception as e:
            logger.error(f"Failed to convert model to entity: {e}")

            raise ValidationError(f"Invalid agent data: {e}")

    def _entity_to_model_data(self, entity: Agent) -> dict[str, Any]:
        """Convert domain entity to model data.





        Args:


            entity: Agent domain entity.





        Returns:


            Model data dictionary.


        """

        try:
            return {
                "id": entity.id,
                "user_id": entity.user_id,
                "name": entity.name,
                "description": entity.description,
                "config": entity.config.model_dump() if entity.config else {},
                "status": entity.status.value
                if entity.status
                else AgentStatus.IDLE.value,
                "capabilities": entity.capabilities or [],
                "knowledge_domains": entity.knowledge_domains or [],
                "created_at": entity.created_at,
                "updated_at": entity.updated_at,
                "last_active_at": entity.last_active_at,
                "is_active": entity.is_active,
            }

        except Exception as e:
            logger.error(f"Failed to convert entity to model data: {e}")

            raise ValidationError(f"Invalid entity data: {e}")

    async def create(self, entity: Agent) -> Agent:
        """Create a new agent.





        Args:


            entity: Agent to create.





        Returns:


            Created agent with assigned ID.





        Raises:


            DuplicateEntityError: If agent already exists.


            RepositoryError: If creation fails.


        """

        try:
            # Generate ID if not provided

            if entity.id is None:
                entity.id = uuid4()

            # Set timestamps

            now = datetime.now(UTC)

            entity.created_at = now

            entity.updated_at = now

            # Convert to model data

            model_data = self._entity_to_model_data(entity)

            # Create model instance

            model = AgentModel(**model_data)

            # Add to session

            self.session.add(model)

            await self.session.flush()  # Get the ID

            logger.info(f"Created agent {entity.id} for user {entity.user_id}")

            return self._model_to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()

            logger.error(f"Agent creation failed due to constraint violation: {e}")

            raise DuplicateEntityError(f"Agent already exists: {e}")

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during agent creation: {e}")

            raise RepositoryError(f"Failed to create agent: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during agent creation: {e}")

            raise RepositoryError(f"Agent creation failed: {e}")

    async def get_by_id(self, entity_id: UUID) -> Agent | None:
        """Get agent by ID.





        Args:


            entity_id: Agent ID.





        Returns:


            Agent if found, None otherwise.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = select(AgentModel).where(AgentModel.id == entity_id)

            _ = await self.session.execute(stmt)

            model = result.scalar_one_or_none()

            if model is None:
                logger.debug(f"Agent {entity_id} not found")

                return None

            logger.debug(f"Retrieved agent {entity_id}")

            return self._model_to_entity(model)

        except SQLAlchemyError as e:
            logger.error(f"Database error during agent retrieval: {e}")

            raise RepositoryError(f"Failed to get agent: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during agent retrieval: {e}")

            raise RepositoryError(f"Agent retrieval failed: {e}")

    async def get_by_user_id(self, user_id: UUID) -> list[Agent]:
        """Get all agents for a user.





        Args:


            user_id: User ID.





        Returns:


            List of user's agents.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = (
                select(AgentModel)
                .where(AgentModel.user_id == user_id)
                .order_by(AgentModel.created_at.desc())
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            agents = [self._model_to_entity(model) for model in models]

            logger.debug(f"Retrieved {len(agents)} agents for user {user_id}")

            return agents

        except SQLAlchemyError as e:
            logger.error(f"Database error during agent retrieval by user: {e}")

            raise RepositoryError(f"Failed to get agents by user: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during agent retrieval by user: {e}")

            raise RepositoryError(f"Agent retrieval by user failed: {e}")

    async def get_by_owner(self, owner_id: UUID) -> list[Agent]:
        """Get all agents owned by the specified user.





        This is an alias to get_by_user_id to comply with the interface.





        Args:


            owner_id: Owner (user) ID.





        Returns:


            List of agents owned by the user.


        """

        return await self.get_by_user_id(owner_id)

    async def list_by_status(self, status: AgentStatus) -> list[Agent]:
        """List agents by status.





        Args:


            status: Agent status filter.





        Returns:


            List of agents with the given status.


        """

        try:
            stmt = (
                select(AgentModel)
                .where(AgentModel.status == status.value)
                .order_by(AgentModel.created_at.desc())
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            return [self._model_to_entity(m) for m in models]

        except SQLAlchemyError as e:
            logger.error(f"Database error during list_by_status: {e}")

            raise RepositoryError(f"Failed to list agents by status: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during list_by_status: {e}")

            raise RepositoryError(f"List by status failed: {e}")

    async def get_active_agents(self, user_id: UUID | None = None) -> list[Agent]:
        """Get all active agents, optionally filtered by user.





        Args:


            user_id: Optional user ID filter.





        Returns:


            List of active agents.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = select(AgentModel).where(AgentModel.is_active.is_(True))

            if user_id:
                stmt = stmt.where(AgentModel.user_id == user_id)

            stmt = stmt.order_by(AgentModel.last_active_at.desc().nullslast())

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            agents = [self._model_to_entity(model) for model in models]

            logger.debug(f"Retrieved {len(agents)} active agents")

            return agents

        except SQLAlchemyError as e:
            logger.error(f"Database error during active agent retrieval: {e}")

            raise RepositoryError(f"Failed to get active agents: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during active agent retrieval: {e}")

            raise RepositoryError(f"Active agent retrieval failed: {e}")

    async def get_by_capability(self, capability: str) -> list[Agent]:
        """Get agents with a specific capability.





        Args:


            capability: Capability to search for.





        Returns:


            List of agents with the capability.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            # Use JSON contains for PostgreSQL or similar for other databases

            stmt = select(AgentModel).where(
                AgentModel.capabilities.contains([capability])
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            agents = [self._model_to_entity(model) for model in models]

            logger.debug(
                f"Retrieved {len(agents)} agents with capability '{capability}'"
            )

            return agents

        except SQLAlchemyError as e:
            logger.error(f"Database error during capability search: {e}")

            raise RepositoryError(f"Failed to search by capability: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during capability search: {e}")

            raise RepositoryError(f"Capability search failed: {e}")

    async def update(self, entity: Agent) -> Agent:
        """Update an agent.





        Args:


            entity: Agent to update.





        Returns:


            Updated agent.





        Raises:


            EntityNotFoundError: If agent doesn't exist.


            RepositoryError: If update fails.


        """

        try:
            if entity.id is None:
                raise ValidationError("Cannot update agent without ID")

            # Update timestamp

            entity.updated_at = datetime.now(UTC)

            # Convert to model data

            model_data = self._entity_to_model_data(entity)

            # Remove ID and timestamps that shouldn't be updated

            update_data = {
                k: v for k, v in model_data.items() if k not in ["id", "created_at"]
            }

            # Execute update

            stmt = (
                update(AgentModel)
                .where(AgentModel.id == entity.id)
                .values(**update_data)
                .returning(AgentModel)
            )

            _ = await self.session.execute(stmt)

            updated_model = result.scalar_one_or_none()

            if updated_model is None:
                raise EntityNotFoundError(f"Agent {entity.id} not found")

            await self.session.flush()

            logger.info(f"Updated agent {entity.id}")

            return self._model_to_entity(updated_model)

        except EntityNotFoundError:
            raise

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during agent update: {e}")

            raise RepositoryError(f"Failed to update agent: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during agent update: {e}")

            raise RepositoryError(f"Agent update failed: {e}")

    async def delete(self, entity_id: UUID) -> bool:
        """Delete an agent.





        Args:


            entity_id: Agent ID to delete.





        Returns:


            True if deleted, False if not found.





        Raises:


            RepositoryError: If deletion fails.


        """

        try:
            stmt = delete(AgentModel).where(AgentModel.id == entity_id)

            _ = await self.session.execute(stmt)

            deleted = result.rowcount > 0

            if deleted:
                logger.info(f"Deleted agent {entity_id}")

            else:
                logger.debug(f"Agent {entity_id} not found for deletion")

            return deleted

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during agent deletion: {e}")

            raise RepositoryError(f"Failed to delete agent: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during agent deletion: {e}")

            raise RepositoryError(f"Agent deletion failed: {e}")

    def _build_filter_conditions(self, filters: dict[str, Any]) -> list[Any]:
        """Build filter conditions from filters dictionary.





        Args:


            filters: Filters to apply.





        Returns:


            List of SQLAlchemy conditions.


        """

        conditions = []

        if "user_id" in filters:
            conditions.append(AgentModel.user_id == filters["user_id"])

        if "status" in filters:
            conditions.append(AgentModel.status == filters["status"])

        if "is_active" in filters:
            conditions.append(AgentModel.is_active == filters["is_active"])

        if "capability" in filters:
            conditions.append(AgentModel.capabilities.contains([filters["capability"]]))

        if "knowledge_domain" in filters:
            conditions.append(
                AgentModel.knowledge_domains.contains([filters["knowledge_domain"]])
            )

        if "name_contains" in filters:
            conditions.append(AgentModel.name.ilike(f"%{filters['name_contains']}%"))

        return conditions

    async def list_all(
        self, offset: int = 0, limit: int = 100, filters: dict[str, Any] | None = None
    ) -> list[Agent]:
        """List all agents with pagination and optional filtering.





        Args:


            offset: Number of records to skip.


            limit: Maximum number of records to return.


            filters: Optional filters to apply.





        Returns:


            List of agents.





        Raises:


            RepositoryError: If listing fails.


        """

        try:
            stmt = select(AgentModel)

            # Apply filters

            if filters:
                conditions = self._build_filter_conditions(filters)

                if conditions:
                    stmt = stmt.where(and_(*conditions))

            # Apply ordering, offset, and limit

            stmt = (
                stmt.order_by(AgentModel.created_at.desc()).offset(offset).limit(limit)
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            agents = [self._model_to_entity(model) for model in models]

            logger.debug(
                f"Listed {len(agents)} agents (offset={offset}, limit={limit})"
            )

            return agents

        except SQLAlchemyError as e:
            logger.error(f"Database error during agent listing: {e}")

            raise RepositoryError(f"Failed to list agents: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during agent listing: {e}")

            raise RepositoryError(f"Agent listing failed: {e}")

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count agents with optional filtering.





        Args:


            filters: Optional filters to apply.





        Returns:


            Number of matching agents.





        Raises:


            RepositoryError: If counting fails.


        """

        try:
            stmt = select(func.count(AgentModel.id))

            # Apply filters using the same helper method

            if filters:
                conditions = self._build_filter_conditions(filters)

                if conditions:
                    stmt = stmt.where(and_(*conditions))

            _ = await self.session.execute(stmt)

            count = result.scalar_one()

            logger.debug(f"Counted {count} agents")

            return count

        except SQLAlchemyError as e:
            logger.error(f"Database error during agent counting: {e}")

            raise RepositoryError(f"Failed to count agents: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during agent counting: {e}")

            raise RepositoryError(f"Agent counting failed: {e}")

    async def update_status(self, entity_id: UUID, status: AgentStatus) -> bool:
        """Update agent status.





        Args:


            entity_id: Agent ID.


            status: New status.





        Returns:


            True if updated, False if not found.





        Raises:


            RepositoryError: If update fails.


        """

        try:
            now = datetime.now(UTC)

            stmt = (
                update(AgentModel)
                .where(AgentModel.id == entity_id)
                .values(
                    status=status.value,
                    updated_at=now,
                    last_active_at=now
                    if status != AgentStatus.IDLE
                    else AgentModel.last_active_at,
                )
            )

            _ = await self.session.execute(stmt)

            updated = result.rowcount > 0

            if updated:
                logger.info(f"Updated agent {entity_id} status to {status.value}")

            else:
                logger.debug(f"Agent {entity_id} not found for status update")

            return updated

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during status update: {e}")

            raise RepositoryError(f"Failed to update agent status: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during status update: {e}")

            raise RepositoryError(f"Agent status update failed: {e}")

    async def update_last_active(self, entity_id: UUID) -> bool:
        """Update agent's last active timestamp.





        Args:


            entity_id: Agent ID.





        Returns:


            True if updated, False if not found.





        Raises:


            RepositoryError: If update fails.


        """

        try:
            now = datetime.now(UTC)

            stmt = (
                update(AgentModel)
                .where(AgentModel.id == entity_id)
                .values(last_active_at=now, updated_at=now)
            )

            _ = await self.session.execute(stmt)

            updated = result.rowcount > 0

            if updated:
                logger.debug(f"Updated agent {entity_id} last active timestamp")

            return updated

        except SQLAlchemyError as e:
            logger.error(f"Database error during last active update: {e}")

            raise RepositoryError(f"Failed to update last active: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during last active update: {e}")

            raise RepositoryError(f"Last active update failed: {e}")

    async def get_with_memories(self, entity_id: UUID) -> Agent | None:
        """Get agent with its memories loaded.





        Args:


            entity_id: Agent ID.





        Returns:


            Agent with memories if found, None otherwise.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = (
                select(AgentModel)
                .options(selectinload(AgentModel.memories))
                .where(AgentModel.id == entity_id)
            )

            _ = await self.session.execute(stmt)

            model = result.scalar_one_or_none()

            if model is None:
                return None

            _ = self._model_to_entity(model)

            logger.debug(
                f"Retrieved agent {entity_id} with {len(model.memories)} memories"
            )

            return agent

        except SQLAlchemyError as e:
            logger.error(f"Database error during agent with memories retrieval: {e}")

            raise RepositoryError(f"Failed to get agent with memories: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during agent with memories retrieval: {e}")

            raise RepositoryError(f"Agent with memories retrieval failed: {e}")

    async def get_with_conversations(self, entity_id: UUID) -> Agent | None:
        """Get agent with its conversations loaded.





        Args:


            entity_id: Agent ID.





        Returns:


            Agent with conversations if found, None otherwise.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = (
                select(AgentModel)
                .options(selectinload(AgentModel.conversations))
                .where(AgentModel.id == entity_id)
            )

            _ = await self.session.execute(stmt)

            model = result.scalar_one_or_none()

            if model is None:
                return None

            _ = self._model_to_entity(model)

            logger.debug(
                f"Retrieved agent {entity_id} with {len(model.conversations)} conversations"
            )

            return agent

        except SQLAlchemyError as e:
            logger.error(
                f"Database error during agent with conversations retrieval: {e}"
            )

            raise RepositoryError(f"Failed to get agent with conversations: {e}")

        except Exception as e:
            logger.error(
                f"Unexpected error during agent with conversations retrieval: {e}"
            )

            raise RepositoryError(f"Agent with conversations retrieval failed: {e}")
