#!/usr/bin/env python3
"""
Dependencies & Factory Enhancement Script

Tạo dependencies injection và application factory patterns.
"""

from __future__ import annotations

from pathlib import Path
import Exception
import bool
import content
import e
import file_path
import int
import print
import str

# Dependencies Templates
DEPENDENCY_TEMPLATES = {
    "zeta_vn/app/dependencies.py": '''"""Dependency injection for FastAPI."""
from __future__ import annotations

from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.core.domain.entities.User import User
from apps.backend.core.services.agent_service import AgentService
from apps.backend.core.services.chat_service import ChatService
from apps.backend.core.services.memory_service import MemoryService
from apps.backend.core.services.rag_service import RAGService
from apps.backend.core.services.system_service import SystemService
from apps.backend.data.database.session import get_async_session
from apps.backend.data.repositories.agent_repository_impl import AgentRepositoryImpl
from apps.backend.data.repositories.chat_repository_impl import ChatRepositoryImpl
from apps.backend.data.repositories.message_repository_impl import MessageRepositoryImpl
from apps.backend.data.repositories.memory_repository_impl import MemoryRepositoryImpl
from apps.backend.data.repositories.document_repository_impl import DocumentRepositoryImpl
from apps.backend.data.repositories.user_repository_impl import UserRepositoryImpl

# Security
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """Get current authenticated user."""
    try:
        # TODO: Implement JWT token validation
        # For now, return mock user
        user_repo = UserRepositoryImpl(session)
        user = await user_repo.get_by_id("default-user-id")
        
        if not user:
            # Create default user for development
            user = User(
                id="default-user-id",
                email="dev@zeta.vn",
                username="developer",
                is_active=True
            )
            user = await user_repo.create(user)
        
        return user
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Repository Dependencies
async def get_agent_repository(
    session: AsyncSession = Depends(get_async_session)
) -> AgentRepositoryImpl:
    """Get agent repository."""
    return AgentRepositoryImpl(session)


async def get_chat_repository(
    session: AsyncSession = Depends(get_async_session)
) -> ChatRepositoryImpl:
    """Get chat repository."""
    return ChatRepositoryImpl(session)


async def get_message_repository(
    session: AsyncSession = Depends(get_async_session)
) -> MessageRepositoryImpl:
    """Get message repository."""
    return MessageRepositoryImpl(session)


async def get_memory_repository(
    session: AsyncSession = Depends(get_async_session)
) -> MemoryRepositoryImpl:
    """Get memory repository."""
    return MemoryRepositoryImpl(session)


async def get_document_repository(
    session: AsyncSession = Depends(get_async_session)
) -> DocumentRepositoryImpl:
    """Get document repository."""
    return DocumentRepositoryImpl(session)


# Service Dependencies
async def get_agent_service(
    agent_repo: AgentRepositoryImpl = Depends(get_agent_repository)
) -> AgentService:
    """Get agent service."""
    return AgentService(agent_repo)


async def get_chat_service(
    chat_repo: ChatRepositoryImpl = Depends(get_chat_repository),
    message_repo: MessageRepositoryImpl = Depends(get_message_repository)
) -> ChatService:
    """Get chat service."""
    return ChatService(chat_repo, message_repo)


async def get_memory_service(
    memory_repo: MemoryRepositoryImpl = Depends(get_memory_repository)
) -> MemoryService:
    """Get memory service."""
    return MemoryService(memory_repo)


async def get_rag_service(
    document_repo: DocumentRepositoryImpl = Depends(get_document_repository)
) -> RAGService:
    """Get RAG service."""
    return RAGService(document_repo)


async def get_system_service() -> SystemService:
    """Get system service."""
    return SystemService()


__all__ = [
    "get_current_user",
    "get_agent_service",
    "get_chat_service",
    "get_memory_service",
    "get_rag_service",
    "get_system_service",
]
''',
    "zeta_vn/data/database/session.py": '''"""Database session management."""
from __future__ import annotations

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from apps.backend.config.settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


__all__ = ["get_async_session", "Base", "engine"]
''',
    "zeta_vn/config/settings.py": '''"""Application settings."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "ZETA_VN"
    version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./zeta_vn.db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Models
    openai_api_key: Optional[str] = None
    default_model: str = "gpt-3.5-turbo"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()


__all__ = ["Settings", "get_settings"]
''',
}

# Repository Implementation Templates
REPO_IMPL_TEMPLATES = {
    "zeta_vn/data/repositories/agent_repository_impl.py": '''"""Agent repository implementation."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.backend.core.interfaces.repositories.agent_repository import AgentRepository
from apps.backend.core.domain.entities.Agent import Agent
from apps.backend.data.models.agent_model import AgentModel


class AgentRepositoryImpl(AgentRepository):
    """SQLAlchemy implementation of Agent repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, agent: Agent) -> Agent:
        """Create new agent."""
        model = AgentModel.from_entity(agent)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Get agent by ID."""
        stmt = select(AgentModel).where(AgentModel.id == agent_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Agent]:
        """Get all agents for user."""
        stmt = select(AgentModel).where(AgentModel.user_id == user_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def update(self, agent: Agent) -> Agent:
        """Update agent."""
        model = await self._session.get(AgentModel, agent.id)
        if model:
            model.update_from_entity(agent)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Agent {agent.id} not found")
    
    async def delete(self, agent_id: UUID) -> None:
        """Delete agent."""
        model = await self._session.get(AgentModel, agent_id)
        if model:
            await self._session.delete(model)


__all__ = ["AgentRepositoryImpl"]
''',
    "zeta_vn/data/repositories/chat_repository_impl.py": '''"""Chat repository implementation."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.backend.core.interfaces.repositories.chat_repository import ChatRepository
from apps.backend.core.domain.entities.Chat import Chat
from apps.backend.data.models.chat_model import ChatModel


class ChatRepositoryImpl(ChatRepository):
    """SQLAlchemy implementation of Chat repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, chat: Chat) -> Chat:
        """Create new chat."""
        model = ChatModel.from_entity(chat)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """Get chat by ID."""
        stmt = select(ChatModel).where(ChatModel.id == chat_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Chat]:
        """Get all chats for user."""
        stmt = select(ChatModel).where(ChatModel.user_id == user_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def update(self, chat: Chat) -> Chat:
        """Update chat."""
        model = await self._session.get(ChatModel, chat.id)
        if model:
            model.update_from_entity(chat)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Chat {chat.id} not found")
    
    async def delete(self, chat_id: UUID) -> None:
        """Delete chat."""
        model = await self._session.get(ChatModel, chat_id)
        if model:
            await self._session.delete(model)


__all__ = ["ChatRepositoryImpl"]
''',
    "zeta_vn/data/repositories/message_repository_impl.py": '''"""Message repository implementation."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.backend.core.interfaces.repositories.message_repository import MessageRepository
from apps.backend.core.domain.entities.Chat import Message
from apps.backend.data.models.message_model import MessageModel


class MessageRepositoryImpl(MessageRepository):
    """SQLAlchemy implementation of Message repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, message: Message) -> Message:
        """Create new message."""
        model = MessageModel.from_entity(message)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get message by ID."""
        stmt = select(MessageModel).where(MessageModel.id == message_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_chat_id(self, chat_id: UUID) -> List[Message]:
        """Get all messages for chat."""
        stmt = select(MessageModel).where(MessageModel.chat_id == chat_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def delete(self, message_id: UUID) -> None:
        """Delete message."""
        model = await self._session.get(MessageModel, message_id)
        if model:
            await self._session.delete(model)


__all__ = ["MessageRepositoryImpl"]
''',
    "zeta_vn/data/repositories/memory_repository_impl.py": '''"""Memory repository implementation."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from apps.backend.core.interfaces.repositories.memory_repository import MemoryRepository
from apps.backend.core.domain.entities.Memory import Memory
from apps.backend.data.models.memory_model import MemoryModel


class MemoryRepositoryImpl(MemoryRepository):
    """SQLAlchemy implementation of Memory repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, memory: Memory) -> Memory:
        """Create new memory."""
        model = MemoryModel.from_entity(memory)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, memory_id: UUID) -> Optional[Memory]:
        """Get memory by ID."""
        stmt = select(MemoryModel).where(MemoryModel.id == memory_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Memory]:
        """Get all memories for user."""
        stmt = select(MemoryModel).where(MemoryModel.user_id == user_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def search_by_content(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Memory]:
        """Search memories by content."""
        stmt = (
            select(MemoryModel)
            .where(
                and_(
                    MemoryModel.user_id == user_id,
                    MemoryModel.content.contains(query)
                )
            )
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def update(self, memory: Memory) -> Memory:
        """Update memory."""
        model = await self._session.get(MemoryModel, memory.id)
        if model:
            model.update_from_entity(memory)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Memory {memory.id} not found")
    
    async def delete(self, memory_id: UUID) -> None:
        """Delete memory."""
        model = await self._session.get(MemoryModel, memory_id)
        if model:
            await self._session.delete(model)


__all__ = ["MemoryRepositoryImpl"]
''',
    "zeta_vn/data/repositories/document_repository_impl.py": '''"""Document repository implementation."""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from apps.backend.core.interfaces.repositories.document_repository import DocumentRepository
from apps.backend.core.domain.entities.Document import Document
from apps.backend.data.models.document_model import DocumentModel


class DocumentRepositoryImpl(DocumentRepository):
    """SQLAlchemy implementation of Document repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, document: Document) -> Document:
        """Create new document."""
        model = DocumentModel.from_entity(document)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        stmt = select(DocumentModel).where(DocumentModel.id == document_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_user_id(self, user_id: UUID) -> List[Document]:
        """Get all documents for user."""
        stmt = select(DocumentModel).where(DocumentModel.user_id == user_id)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def search_by_content(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Document]:
        """Search documents by content."""
        stmt = (
            select(DocumentModel)
            .where(
                and_(
                    DocumentModel.user_id == user_id,
                    DocumentModel.content.contains(query)
                )
            )
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [model.to_entity() for model in models]
    
    async def update(self, document: Document) -> Document:
        """Update document."""
        model = await self._session.get(DocumentModel, document.id)
        if model:
            model.update_from_entity(document)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"Document {document.id} not found")
    
    async def delete(self, document_id: UUID) -> None:
        """Delete document."""
        model = await self._session.get(DocumentModel, document_id)
        if model:
            await self._session.delete(model)


__all__ = ["DocumentRepositoryImpl"]
''',
    "zeta_vn/data/repositories/user_repository_impl.py": '''"""User repository implementation."""
from __future__ import annotations

from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from apps.backend.core.interfaces.repositories.user_repository import UserRepository
from apps.backend.core.domain.entities.User import User
from apps.backend.data.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """SQLAlchemy implementation of User repository."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def create(self, user: User) -> User:
        """Create new user."""
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model.to_entity()
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def update(self, user: User) -> User:
        """Update user."""
        model = await self._session.get(UserModel, user.id)
        if model:
            model.update_from_entity(user)
            await self._session.flush()
            await self._session.refresh(model)
            return model.to_entity()
        raise ValueError(f"User {user.id} not found")
    
    async def delete(self, user_id: str) -> None:
        """Delete user."""
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)


__all__ = ["UserRepositoryImpl"]
''',
}


def enhance_file(file_path: str, content: str) -> bool:
    """Enhance a file with content."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"❌ Failed to enhance {file_path}: {e}")
        return False


def enhance_dependencies_and_repos() -> int:
    """Enhance dependencies and repository implementations."""
    print("🔧 DEPENDENCIES & REPOSITORIES ENHANCEMENT")
    print("=" * 50)

    enhanced_count = 0

    # Create dependencies
    print("\n1️⃣ Creating dependencies...")
    for file_path, content in DEPENDENCY_TEMPLATES.items():
        if not Path(file_path).exists():
            if enhance_file(file_path, content):
                print(f"✅ Created {file_path}")
                enhanced_count += 1
        else:
            print(f"⏭️  Exists {file_path}")

    # Create repository implementations
    print("\n2️⃣ Creating repository implementations...")
    for file_path, content in REPO_IMPL_TEMPLATES.items():
        if not Path(file_path).exists():
            if enhance_file(file_path, content):
                print(f"✅ Created {file_path}")
                enhanced_count += 1
        else:
            print(f"⏭️  Exists {file_path}")

    print("\n📊 DEPENDENCIES & REPOSITORIES COMPLETE")
    print(f"   Enhanced files: {enhanced_count}")

    return enhanced_count


if __name__ == "__main__":
    enhanced_count = enhance_dependencies_and_repos()
    if enhanced_count > 0:
        print("\n🚀 Dependencies and repositories enhanced successfully!")
    else:
        print("\n✅ Dependencies and repositories already complete")
