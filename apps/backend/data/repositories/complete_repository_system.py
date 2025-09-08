"""Complete repository pattern implementation for ZETA AI."""

from __future__ import annotations

import logging
from abc import ABC
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar
from uuid import UUID

from apps.backend.core.exceptions.repository_exceptions import RepositoryError
from apps.backend.data.models.agent_model import Agent
from apps.backend.data.models.audit_model import AuditLog
from apps.backend.data.models.chat_model import Conversation as ChatModel
from apps.backend.data.models.chat_model import Message as MessageModel
from apps.backend.data.models.config_model import ConfigurationSetting
from apps.backend.data.models.file_model import File
from apps.backend.data.models.memory_model import Memory as MemoryModel
from apps.backend.data.models.plan_model import Plan, Task
from apps.backend.data.models.user_model import User
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

# Temporarily comment out missing models to get server running


# from data.models import (


#     AuditLog,


#     BackupModel,


#     BlobStorageModel,


#     ConfigurationModel,


#     MessageModel,


#     MetricsModel,


#     NotificationModel,


#     Plan,


#     Task,


# )


logger = logging.getLogger(__name__)


T = TypeVar("T")


ModelType = TypeVar("ModelType")


class BaseRepository(ABC, Generic[ModelType]):
    """Base repository with common operations."""
import Exception
import action
import agent_id
import bool
import category
import chat_id
import config_key
import dict
import e
import email
import entity_id
import entity_type
import file_hash
import filters
import getattr
import hasattr
import int
import key
import kwargs
import limit
import list
import metadata
import model_class
import new_values
import offset
import old_values
import order_by
import owner_id
import plan_id
import query
import result
import self
import session
import str
import super
import type
import user_id
import username
import value

    def __init__(self, session: AsyncSession, model_class: type[ModelType]) -> None:
        """


        Initialize repository.





        Args:


            session: Database session


            model_class: SQLAlchemy model class


        """

        self._ = session

        self.model_class = model_class

    async def create(self, **kwargs: Any) -> ModelType:
        """


        Create new entity.





        Args:


            **kwargs: Entity data





        Returns:


            Created entity


        """

        try:
            entity = self.model_class(**kwargs)

            self.session.add(entity)

            await self.session.flush()

            await self.session.refresh(entity)

            return entity

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Failed to create {self.model_class.__name__}: {e}")

            raise RepositoryError(f"Creation failed: {e}") from e

    async def get_by_id(self, entity_id: UUID) -> ModelType | None:
        """


        Get entity by ID.





        Args:


            entity_id: Entity ID





        Returns:


            Entity or None if not found


        """

        try:
            stmt = select(self.model_class).where(self.model_class.id == entity_id)

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get {self.model_class.__name__} by ID: {e}")

            raise RepositoryError(f"Retrieval failed: {e}") from e

    async def update(self, entity_id: UUID, **kwargs: Any) -> ModelType | None:
        """


        Update entity.





        Args:


            entity_id: Entity ID


            **kwargs: Update data





        Returns:


            Updated entity or None if not found


        """

        try:
            stmt = (
                update(self.model_class)
                .where(self.model_class.id == entity_id)
                .values(**kwargs)
                .returning(self.model_class)
            )

            _ = await self.session.execute(stmt)

            await self.session.commit()

            return result.scalar_one_or_none()

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Failed to update {self.model_class.__name__}: {e}")

            raise RepositoryError(f"Update failed: {e}") from e

    async def delete(self, entity_id: UUID) -> bool:
        """


        Delete entity.





        Args:


            entity_id: Entity ID





        Returns:


            True if deleted, False if not found


        """

        try:
            stmt = delete(self.model_class).where(self.model_class.id == entity_id)

            _ = await self.session.execute(stmt)

            await self.session.commit()

            return result.rowcount > 0

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Failed to delete {self.model_class.__name__}: {e}")

            raise RepositoryError(f"Deletion failed: {e}") from e

    async def list_all(
        self, limit: int = 100, offset: int = 0, order_by: str = "created_at"
    ) -> list[ModelType]:
        """


        List all entities with pagination.





        Args:


            limit: Maximum number of results


            offset: Number of results to skip


            order_by: Field to order by





        Returns:


            List of entities


        """

        try:
            order_field = getattr(
                self.model_class, order_by, self.model_class.created_at
            )

            stmt = (
                select(self.model_class)
                .order_by(order_field.desc())
                .limit(limit)
                .offset(offset)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to list {self.model_class.__name__}: {e}")

            raise RepositoryError(f"Listing failed: {e}") from e

    async def count(self, **filters: Any) -> int:
        """


        Count entities with optional filters.





        Args:


            **filters: Filter criteria





        Returns:


            Number of entities


        """

        try:
            stmt = select(func.count(self.model_class.id))

            if filters:
                conditions = [
                    getattr(self.model_class, key) == value
                    for key, value in filters.items()
                    if hasattr(self.model_class, key)
                ]

                if conditions:
                    stmt = stmt.where(and_(*conditions))

            _ = await self.session.execute(stmt)

            return result.scalar() or 0

        except Exception as e:
            logger.error(f"Failed to count {self.model_class.__name__}: {e}")

            raise RepositoryError(f"Count failed: {e}") from e


class UserRepository(BaseRepository[User]):
    """Repository for user operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user repository."""

        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        """


        Get user by email.





        Args:


            email: User email





        Returns:


            User or None if not found


        """

        try:
            stmt = select(User).where(User.email == email)

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get user by email: {e}")

            raise RepositoryError(f"User retrieval failed: {e}") from e

    async def get_by_username(self, username: str) -> User | None:
        """


        Get user by username.





        Args:


            username: Username





        Returns:


            User or None if not found


        """

        try:
            stmt = select(User).where(User.username == username)

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get user by username: {e}")

            raise RepositoryError(f"User retrieval failed: {e}") from e

    async def update_last_login(self, user_id: UUID) -> None:
        """


        Update user's last login timestamp.





        Args:


            user_id: User ID


        """

        try:
            stmt = (
                update(User)
                .where(User.id == user_id)
                .values(last_login=datetime.now(UTC))
            )

            await self.session.execute(stmt)

            await self.session.commit()

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Failed to update last login: {e}")

            raise RepositoryError(f"Last login update failed: {e}") from e


class AgentRepository(BaseRepository[Agent]):
    """Repository for agent operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize agent repository."""

        super().__init__(session, Agent)

    async def get_by_owner(self, owner_id: UUID, limit: int = 50) -> list[Agent]:
        """


        Get agents by owner.





        Args:


            owner_id: Owner user ID


            limit: Maximum number of results





        Returns:


            List of agents


        """

        try:
            stmt = (
                select(Agent)
                .where(Agent.owner_id == owner_id)
                .order_by(Agent.created_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get agents by owner: {e}")

            raise RepositoryError(f"Agent retrieval failed: {e}") from e

    async def get_active_agents(self) -> list[Agent]:
        """


        Get all active agents.





        Returns:


            List of active agents


        """

        try:
            stmt = (
                select(Agent)
                .where(and_(Agent.is_active.is_(True), Agent.status == "active"))
                .order_by(Agent.created_at.desc())
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get active agents: {e}")

            raise RepositoryError(f"Active agents retrieval failed: {e}") from e


class ChatRepository(BaseRepository[ChatModel]):
    """Repository for chat operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize chat repository."""

        super().__init__(session, ChatModel)

    async def get_by_user(self, user_id: UUID, limit: int = 50) -> list[ChatModel]:
        """


        Get chats by user.





        Args:


            user_id: User ID


            limit: Maximum number of results





        Returns:


            List of chats


        """

        try:
            stmt = (
                select(ChatModel)
                .where(ChatModel.user_id == user_id)
                .order_by(ChatModel.updated_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get chats by user: {e}")

            raise RepositoryError(f"Chat retrieval failed: {e}") from e

    async def get_with_messages(self, chat_id: UUID) -> ChatModel | None:
        """


        Get chat with all messages.





        Args:


            chat_id: Chat ID





        Returns:


            Chat with messages or None if not found


        """

        try:
            stmt = (
                select(ChatModel)
                .options(selectinload(ChatModel.messages))
                .where(ChatModel.id == chat_id)
            )

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get chat with messages: {e}")

            raise RepositoryError(f"Chat retrieval failed: {e}") from e


class MessageRepository(BaseRepository[MessageModel]):
    """Repository for message operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize message repository."""

        super().__init__(session, MessageModel)

    async def get_by_chat(
        self, chat_id: UUID, limit: int = 100, offset: int = 0
    ) -> list[MessageModel]:
        """


        Get messages by chat.





        Args:


            chat_id: Chat ID


            limit: Maximum number of results


            offset: Number of results to skip





        Returns:


            List of messages


        """

        try:
            stmt = (
                select(MessageModel)
                .where(MessageModel.chat_id == chat_id)
                .order_by(MessageModel.created_at.asc())
                .limit(limit)
                .offset(offset)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get messages by chat: {e}")

            raise RepositoryError(f"Message retrieval failed: {e}") from e


class FileRepository(BaseRepository[File]):
    """Repository for file operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize file repository."""

        super().__init__(session, File)

    async def get_by_owner(self, owner_id: UUID, limit: int = 50) -> list[File]:
        """


        Get files by owner.





        Args:


            owner_id: Owner user ID


            limit: Maximum number of results





        Returns:


            List of files


        """

        try:
            stmt = (
                select(File)
                .where(File.owner_id == owner_id)
                .order_by(File.created_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get files by owner: {e}")

            raise RepositoryError(f"File retrieval failed: {e}") from e

    async def get_by_hash(self, file_hash: str) -> File | None:
        """


        Get file by hash.





        Args:


            file_hash: File hash





        Returns:


            File or None if not found


        """

        try:
            stmt = select(File).where(File.file_hash == file_hash)

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get file by hash: {e}")

            raise RepositoryError(f"File retrieval failed: {e}") from e


class MemoryRepository(BaseRepository[MemoryModel]):
    """Repository for memory operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize memory repository."""

        super().__init__(session, MemoryModel)

    async def get_by_agent(self, agent_id: UUID, limit: int = 100) -> list[MemoryModel]:
        """


        Get memories by agent.





        Args:


            agent_id: Agent ID


            limit: Maximum number of results





        Returns:


            List of memories


        """

        try:
            stmt = (
                select(MemoryModel)
                .where(MemoryModel.agent_id == agent_id)
                .order_by(MemoryModel.importance.desc(), MemoryModel.created_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get memories by agent: {e}")

            raise RepositoryError(f"Memory retrieval failed: {e}") from e

    async def search_by_content(
        self, query: str, agent_id: UUID | None = None, limit: int = 20
    ) -> list[MemoryModel]:
        """


        Search memories by content.





        Args:


            query: Search query


            agent_id: Optional agent ID filter


            limit: Maximum number of results





        Returns:


            List of matching memories


        """

        try:
            stmt = select(MemoryModel).where(MemoryModel.content.ilike(f"%{query}%"))

            if agent_id:
                stmt = stmt.where(MemoryModel.agent_id == agent_id)

            stmt = stmt.order_by(MemoryModel.importance.desc()).limit(limit)

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to search memories: {e}")

            raise RepositoryError(f"Memory search failed: {e}") from e


class PlanRepository(BaseRepository[Plan]):
    """Repository for plan operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize plan repository."""

        super().__init__(session, Plan)

    async def get_by_user(self, user_id: UUID, limit: int = 50) -> list[Plan]:
        """


        Get plans by user.





        Args:


            user_id: User ID


            limit: Maximum number of results





        Returns:


            List of plans


        """

        try:
            stmt = (
                select(Plan)
                .where(Plan.user_id == user_id)
                .order_by(Plan.created_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get plans by user: {e}")

            raise RepositoryError(f"Plan retrieval failed: {e}") from e

    async def get_with_tasks(self, plan_id: UUID) -> Plan | None:
        """


        Get plan with all tasks.





        Args:


            plan_id: Plan ID





        Returns:


            Plan with tasks or None if not found


        """

        try:
            stmt = (
                select(Plan).options(selectinload(Plan.tasks)).where(Plan.id == plan_id)
            )

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get plan with tasks: {e}")

            raise RepositoryError(f"Plan retrieval failed: {e}") from e


class TaskRepository(BaseRepository[Task]):
    """Repository for task operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize task repository."""

        super().__init__(session, Task)

    async def get_by_plan(self, plan_id: UUID) -> list[Task]:
        """


        Get tasks by plan.





        Args:


            plan_id: Plan ID





        Returns:


            List of tasks ordered by order


        """

        try:
            stmt = (
                select(Task).where(Task.plan_id == plan_id).order_by(Task.order.asc())
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get tasks by plan: {e}")

            raise RepositoryError(f"Task retrieval failed: {e}") from e

    async def get_pending_tasks(self, plan_id: UUID) -> list[Task]:
        """


        Get pending tasks for a plan.





        Args:


            plan_id: Plan ID





        Returns:


            List of pending tasks


        """

        try:
            stmt = (
                select(Task)
                .where(and_(Task.plan_id == plan_id, Task.status == "pending"))
                .order_by(Task.order.asc())
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get pending tasks: {e}")

            raise RepositoryError(f"Task retrieval failed: {e}") from e


class ConfigurationRepository(BaseRepository[ConfigurationSetting]):
    """Repository for configuration operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize configuration repository."""

        super().__init__(session, ConfigurationSetting)

    async def get_by_key(self, config_key: str) -> ConfigurationSetting | None:
        """


        Get configuration by key.





        Args:


            config_key: Configuration key





        Returns:


            Configuration or None if not found


        """

        try:
            stmt = select(ConfigurationSetting).where(
                ConfigurationSetting.key == config_key
            )

            _ = await self.session.execute(stmt)

            return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"Failed to get configuration by key: {e}")

            raise RepositoryError(f"Configuration retrieval failed: {e}") from e

    async def get_by_category(self, category: str) -> list[ConfigurationSetting]:
        """


        Get configurations by category.





        Args:


            category: Configuration category





        Returns:


            List of configurations


        """

        try:
            stmt = (
                select(ConfigurationSetting)
                .where(ConfigurationSetting.category == category)
                .order_by(ConfigurationSetting.key.asc())
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get configurations by category: {e}")

            raise RepositoryError(f"Configuration retrieval failed: {e}") from e


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for audit log operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize audit log repository."""

        super().__init__(session, AuditLog)

    async def get_by_entity(
        self, entity_type: str, entity_id: str, limit: int = 50
    ) -> list[AuditLog]:
        """


        Get audit logs by entity.





        Args:


            entity_type: Entity type


            entity_id: Entity ID


            limit: Maximum number of results





        Returns:


            List of audit logs


        """

        try:
            stmt = (
                select(AuditLog)
                .where(
                    and_(
                        AuditLog.entity_type == entity_type,
                        AuditLog.entity_id == entity_id,
                    )
                )
                .order_by(AuditLog.created_at.desc())
                .limit(limit)
            )

            _ = await self.session.execute(stmt)

            return list(result.scalars().all())

        except Exception as e:
            logger.error(f"Failed to get audit logs: {e}")

            raise RepositoryError(f"Audit log retrieval failed: {e}") from e

    async def create_audit_log(
        self,
        entity_type: str,
        entity_id: str,
        action: str,
        old_values: dict[str, Any] | None = None,
        new_values: dict[str, Any] | None = None,
        user_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        """


        Create audit log entry.





        Args:


            entity_type: Entity type


            entity_id: Entity ID


            action: Action performed


            old_values: Previous values


            new_values: New values


            user_id: User who performed action


            metadata: Additional metadata





        Returns:


            Created audit log


        """

        try:
            audit_log = AuditLog(
                entity_type=entity_type,
                entity_id=entity_id,
                action=action,
                old_values=old_values,
                new_values=new_values,
                user_id=user_id,
                metadata=metadata or {},
            )

            self.session.add(audit_log)

            await self.session.flush()

            await self.session.refresh(audit_log)

            return audit_log

        except Exception as e:
            await self.session.rollback()

            logger.error(f"Failed to create audit log: {e}")

            raise RepositoryError(f"Audit log creation failed: {e}") from e


# Utility repositories for system management


# TODO: Implement BackupModel first


# class BackupRepository(BaseRepository[BackupModel]):


#     """Repository for backup operations."""


#     def __init__(self, session: AsyncSession) -> None:


#         """Initialize backup repository."""


#         super().__init__(session, BackupModel)


# TODO: Implement BlobStorageModel first


# class BlobStorageRepository(BaseRepository[BlobStorageModel]):


#     """Repository for blob storage operations."""


#     def __init__(self, session: AsyncSession) -> None:


#         """Initialize blob storage repository."""


#         super().__init__(session, BlobStorageModel)


# TODO: Implement MetricsModel first


# class MetricsRepository(BaseRepository[MetricsModel]):


#     """Repository for metrics operations."""


#     def __init__(self, session: AsyncSession) -> None:


#         """Initialize metrics repository."""


#         super().__init__(session, MetricsModel)


# TODO: Implement NotificationModel first


# class NotificationRepository(BaseRepository[NotificationModel]):


#     """Repository for notification operations."""


#     def __init__(self, session: AsyncSession) -> None:


#         """Initialize notification repository."""


#         super().__init__(session, NotificationModel)
