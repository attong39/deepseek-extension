"""SQLAlchemy implementation of Memory repository for ZETA AI.





This module provides database operations for Memory entities using SQLAlchemy ORM


with proper error handling and transaction management.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apps.backend.core.domain.entities.memory import Memory, MemoryType
from apps.backend.core.exceptions.repository_exceptions import (
import Exception
import bool
import dict
import e
import entity
import entity_id
import filters
import hours
import int
import isinstance
import k
import len
import limit
import list
import offset
import query
import result
import self
import session
import str
import total_result
import v
    DuplicateEntityError,
    EntityNotFoundError,
    RepositoryError,
    ValidationError,
)
from apps.backend.data.models.memory_model import Memory as MemoryModel
from sqlalchemy import and_, delete, desc, func, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# Setup


logger = logging.getLogger(__name__)


class SQLAlchemyMemoryRepository:
    """SQLAlchemy implementation of Memory repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository.





        Args:


            session: Database session.


        """

        self._ = session

        logger.debug("SQLAlchemy Memory repository initialized")

    def _model_to_entity(self, model: MemoryModel) -> Memory:
        """Convert SQLAlchemy model to domain entity.





        Args:


            model: Memory model.





        Returns:


            Memory domain entity.


        """

        try:
            # Convert string UUID to UUID object if needed

            agent_id = None

            if model.agent_id:
                agent_id = (
                    UUID(model.agent_id)
                    if isinstance(model.agent_id, str)
                    else model.agent_id
                )

            # Convert string MemoryType back to enum

            memory_type = (
                MemoryType(model.memory_type)
                if model.memory_type
                else MemoryType.EPISODIC
            )

            return Memory(
                id=model.id,
                agent_id=agent_id,
                content=model.content,
                type=memory_type,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )

        except Exception as e:
            logger.error(f"Failed to convert model to entity: {e}")

            raise ValidationError(f"Invalid memory data: {e}")

    def _entity_to_model_data(self, entity: Memory) -> dict[str, Any]:
        """Convert domain entity to model data.





        Args:


            entity: Memory domain entity.





        Returns:


            Model data dictionary.


        """

        try:
            # Convert UUID to string for database storage

            agent_id_str = str(entity.agent_id) if entity.agent_id else None

            return {
                "id": entity.id,
                "agent_id": agent_id_str,
                "content": entity.content,
                "memory_type": entity.type.value if entity.type else "episodic",
                "created_at": entity.created_at,
                "updated_at": entity.updated_at,
            }

        except Exception as e:
            logger.error(f"Failed to convert entity to model data: {e}")

            raise ValidationError(f"Invalid entity data: {e}")

    async def create(self, entity: Memory) -> Memory:
        """Create a new memory.





        Args:


            entity: Memory to create.





        Returns:


            Created memory with assigned ID.





        Raises:


            DuplicateEntityError: If memory already exists.


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

            model = MemoryModel(**model_data)

            # Add to session

            self.session.add(model)

            await self.session.flush()  # Get the ID

            logger.info(f"Created memory {entity.id} for agent {entity.agent_id}")

            return self._model_to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()

            logger.error(f"Memory creation failed due to constraint violation: {e}")

            raise DuplicateEntityError(f"Memory already exists: {e}")

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during memory creation: {e}")

            raise RepositoryError(f"Failed to create memory: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during memory creation: {e}")

            raise RepositoryError(f"Memory creation failed: {e}")

    async def get_by_id(self, entity_id: UUID) -> Memory | None:
        """Get memory by ID.





        Args:


            entity_id: Memory ID.





        Returns:


            Memory if found, None otherwise.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = select(MemoryModel).where(MemoryModel.id == entity_id)

            _ = await self.session.execute(stmt)

            model = result.scalar_one_or_none()

            if model is None:
                logger.debug(f"Memory {entity_id} not found")

                return None

            logger.debug(f"Retrieved memory {entity_id}")

            return self._model_to_entity(model)

        except SQLAlchemyError as e:
            logger.error(f"Database error during memory retrieval: {e}")

            raise RepositoryError(f"Failed to get memory: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during memory retrieval: {e}")

            raise RepositoryError(f"Memory retrieval failed: {e}")

    async def get_by_agent_id(self, agent_id: UUID, limit: int = 100) -> list[Memory]:
        """Get memories for an agent.





        Args:


            agent_id: Agent ID.


            limit: Maximum number of memories to return.





        Returns:


            List of agent's memories.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            stmt = (
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id)
                .order_by(desc(MemoryModel.created_at))
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            memories = [self._model_to_entity(model) for model in models]

            logger.debug(f"Retrieved {len(memories)} memories for agent {agent_id}")

            return memories

        except SQLAlchemyError as e:
            logger.error(f"Database error during memory retrieval by agent: {e}")

            raise RepositoryError(f"Failed to get memories by agent: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during memory retrieval by agent: {e}")

            raise RepositoryError(f"Memory retrieval by agent failed: {e}")

    async def update(self, entity: Memory) -> Memory:
        """Update a memory.





        Args:


            entity: Memory to update.





        Returns:


            Updated memory.





        Raises:


            EntityNotFoundError: If memory doesn't exist.


            RepositoryError: If update fails.


        """

        try:
            if entity.id is None:
                raise ValidationError("Cannot update memory without ID")

            # Update timestamp

            entity.updated_at = datetime.now(UTC)

            # Convert to model data

            model_data = self._entity_to_model_data(entity)

            # Remove ID and created_at that shouldn't be updated

            update_data = {
                k: v for k, v in model_data.items() if k not in ["id", "created_at"]
            }

            # Execute update

            stmt = (
                update(MemoryModel)
                .where(MemoryModel.id == entity.id)
                .values(**update_data)
                .returning(MemoryModel)
            )

            _ = await self.session.execute(stmt)

            updated_model = result.scalar_one_or_none()

            if updated_model is None:
                raise EntityNotFoundError(f"Memory {entity.id} not found")

            await self.session.flush()

            logger.info(f"Updated memory {entity.id}")

            return self._model_to_entity(updated_model)

        except EntityNotFoundError:
            raise

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during memory update: {e}")

            raise RepositoryError(f"Failed to update memory: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during memory update: {e}")

            raise RepositoryError(f"Memory update failed: {e}")

    async def delete(self, entity_id: UUID) -> bool:
        """Delete a memory.





        Args:


            entity_id: Memory ID to delete.





        Returns:


            True if deleted, False if not found.





        Raises:


            RepositoryError: If deletion fails.


        """

        try:
            stmt = delete(MemoryModel).where(MemoryModel.id == entity_id)

            _ = await self.session.execute(stmt)

            deleted = result.rowcount > 0

            if deleted:
                logger.info(f"Deleted memory {entity_id}")

            else:
                logger.debug(f"Memory {entity_id} not found for deletion")

            return deleted

        except SQLAlchemyError as e:
            await self.session.rollback()

            logger.error(f"Database error during memory deletion: {e}")

            raise RepositoryError(f"Failed to delete memory: {e}")

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Unexpected error during memory deletion: {e}")

            raise RepositoryError(f"Memory deletion failed: {e}")

    async def search_by_content(
        self, agent_id: UUID, query: str, limit: int = 50
    ) -> list[Memory]:
        """Search memories by content.





        Args:


            agent_id: Agent ID.


            query: Search query.


            limit: Maximum number of results.





        Returns:


            List of matching memories.





        Raises:


            RepositoryError: If search fails.


        """

        try:
            stmt = (
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id)
                .where(MemoryModel.content.ilike(f"%{query}%"))
                .order_by(desc(MemoryModel.created_at))
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            memories = [self._model_to_entity(model) for model in models]

            logger.debug(
                f"Found {len(memories)} memories matching '{query}' for agent {agent_id}"
            )

            return memories

        except SQLAlchemyError as e:
            logger.error(f"Database error during memory search: {e}")

            raise RepositoryError(f"Failed to search memories: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during memory search: {e}")

            raise RepositoryError(f"Memory search failed: {e}")

    async def get_recent_memories(
        self, agent_id: UUID, hours: int = 24, limit: int = 50
    ) -> list[Memory]:
        """Get recent memories for an agent.





        Args:


            agent_id: Agent ID.


            hours: Number of hours to look back.


            limit: Maximum number of results.





        Returns:


            List of recent memories.





        Raises:


            RepositoryError: If retrieval fails.


        """

        try:
            from datetime import timedelta

            cutoff_time = datetime.now(UTC) - timedelta(hours=hours)

            stmt = (
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id)
                .where(MemoryModel.created_at >= cutoff_time)
                .order_by(desc(MemoryModel.created_at))
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            memories = [self._model_to_entity(model) for model in models]

            logger.debug(
                f"Retrieved {len(memories)} recent memories from last {hours} hours"
            )

            return memories

        except SQLAlchemyError as e:
            logger.error(f"Database error during recent memory retrieval: {e}")

            raise RepositoryError(f"Failed to get recent memories: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during recent memory retrieval: {e}")

            raise RepositoryError(f"Recent memory retrieval failed: {e}")

    async def get_memory_statistics(self, agent_id: UUID) -> dict[str, Any]:
        """Get memory statistics for an agent.





        Args:


            agent_id: Agent ID.





        Returns:


            Memory statistics.





        Raises:


            RepositoryError: If statistics retrieval fails.


        """

        try:
            # Total count

            total_stmt = select(func.count(MemoryModel.id)).where(
                MemoryModel.agent_id == agent_id
            )

            await self.session.execute(total_stmt)

            total_count = total_result.scalar_one()

            statistics = {
                "total_memories": total_count,
                "agent_id": str(agent_id),
                "generated_at": datetime.now(UTC).isoformat(),
            }

            logger.debug(f"Generated memory statistics for agent {agent_id}")

            return statistics

        except SQLAlchemyError as e:
            logger.error(f"Database error during statistics generation: {e}")

            raise RepositoryError(f"Failed to get memory statistics: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during statistics generation: {e}")

            raise RepositoryError(f"Memory statistics generation failed: {e}")

    async def list_all(
        self, offset: int = 0, limit: int = 100, filters: dict[str, Any] | None = None
    ) -> list[Memory]:
        """List all memories with pagination and optional filtering.





        Args:


            offset: Number of records to skip.


            limit: Maximum number of records to return.


            filters: Optional filters to apply.





        Returns:


            List of memories.





        Raises:


            RepositoryError: If listing fails.


        """

        try:
            stmt = select(MemoryModel)

            # Apply filters

            if filters:
                conditions = []

                if "agent_id" in filters:
                    conditions.append(MemoryModel.agent_id == filters["agent_id"])

                if "content_contains" in filters:
                    conditions.append(
                        MemoryModel.content.ilike(f"%{filters['content_contains']}%")
                    )

                if conditions:
                    stmt = stmt.where(and_(*conditions))

            # Apply ordering, offset, and limit

            stmt = (
                stmt.order_by(desc(MemoryModel.created_at)).offset(offset).limit(limit)
            )

            _ = await self.session.execute(stmt)

            models = result.scalars().all()

            memories = [self._model_to_entity(model) for model in models]

            logger.debug(
                f"Listed {len(memories)} memories (offset={offset}, limit={limit})"
            )

            return memories

        except SQLAlchemyError as e:
            logger.error(f"Database error during memory listing: {e}")

            raise RepositoryError(f"Failed to list memories: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during memory listing: {e}")

            raise RepositoryError(f"Memory listing failed: {e}")

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count memories with optional filtering.





        Args:


            filters: Optional filters to apply.





        Returns:


            Number of matching memories.





        Raises:


            RepositoryError: If counting fails.


        """

        try:
            stmt = select(func.count(MemoryModel.id))

            # Apply same filters as list_all

            if filters:
                conditions = []

                if "agent_id" in filters:
                    conditions.append(MemoryModel.agent_id == filters["agent_id"])

                if "content_contains" in filters:
                    conditions.append(
                        MemoryModel.content.ilike(f"%{filters['content_contains']}%")
                    )

                if conditions:
                    stmt = stmt.where(and_(*conditions))

            _ = await self.session.execute(stmt)

            count = result.scalar_one()

            logger.debug(f"Counted {count} memories")

            return count

        except SQLAlchemyError as e:
            logger.error(f"Database error during memory counting: {e}")

            raise RepositoryError(f"Failed to count memories: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during memory counting: {e}")

            raise RepositoryError(f"Memory counting failed: {e}")
