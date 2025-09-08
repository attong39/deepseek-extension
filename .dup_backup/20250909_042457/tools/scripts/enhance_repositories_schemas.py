#!/usr/bin/env python3
"""
Repository & Schema Enhancement Script

Tạo repository interfaces và API schemas còn thiếu.
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

# Repository Interface Templates
REPOSITORY_TEMPLATES = {
    "zeta_vn/core/interfaces/repositories/agent_repository.py": '''"""Agent repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Agent import Agent


class AgentRepository(ABC):
    """Repository interface for Agent entities."""
    
    @abstractmethod
    async def create(self, agent: Agent) -> Agent:
        """Create new agent."""
        pass
    
    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Get agent by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Agent]:
        """Get all agents for user."""
        pass
    
    @abstractmethod
    async def update(self, agent: Agent) -> Agent:
        """Update agent."""
        pass
    
    @abstractmethod
    async def delete(self, agent_id: UUID) -> None:
        """Delete agent."""
        pass


__all__ = ["AgentRepository"]
''',
    "zeta_vn/core/interfaces/repositories/chat_repository.py": '''"""Chat repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Chat import Chat


class ChatRepository(ABC):
    """Repository interface for Chat entities."""
    
    @abstractmethod
    async def create(self, chat: Chat) -> Chat:
        """Create new chat."""
        pass
    
    @abstractmethod
    async def get_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """Get chat by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Chat]:
        """Get all chats for user."""
        pass
    
    @abstractmethod
    async def update(self, chat: Chat) -> Chat:
        """Update chat."""
        pass
    
    @abstractmethod
    async def delete(self, chat_id: UUID) -> None:
        """Delete chat."""
        pass


__all__ = ["ChatRepository"]
''',
    "zeta_vn/core/interfaces/repositories/message_repository.py": '''"""Message repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Chat import Message


class MessageRepository(ABC):
    """Repository interface for Message entities."""
    
    @abstractmethod
    async def create(self, message: Message) -> Message:
        """Create new message."""
        pass
    
    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get message by ID."""
        pass
    
    @abstractmethod
    async def get_by_chat_id(self, chat_id: UUID) -> List[Message]:
        """Get all messages for chat."""
        pass
    
    @abstractmethod
    async def delete(self, message_id: UUID) -> None:
        """Delete message."""
        pass


__all__ = ["MessageRepository"]
''',
    "zeta_vn/core/interfaces/repositories/memory_repository.py": '''"""Memory repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Memory import Memory


class MemoryRepository(ABC):
    """Repository interface for Memory entities."""
    
    @abstractmethod
    async def create(self, memory: Memory) -> Memory:
        """Create new memory."""
        pass
    
    @abstractmethod
    async def get_by_id(self, memory_id: UUID) -> Optional[Memory]:
        """Get memory by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Memory]:
        """Get all memories for user."""
        pass
    
    @abstractmethod
    async def search_by_content(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Memory]:
        """Search memories by content."""
        pass
    
    @abstractmethod
    async def update(self, memory: Memory) -> Memory:
        """Update memory."""
        pass
    
    @abstractmethod
    async def delete(self, memory_id: UUID) -> None:
        """Delete memory."""
        pass


__all__ = ["MemoryRepository"]
''',
    "zeta_vn/core/interfaces/repositories/document_repository.py": '''"""Document repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Document import Document


class DocumentRepository(ABC):
    """Repository interface for Document entities."""
    
    @abstractmethod
    async def create(self, document: Document) -> Document:
        """Create new document."""
        pass
    
    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        pass
    
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Document]:
        """Get all documents for user."""
        pass
    
    @abstractmethod
    async def search_by_content(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[Document]:
        """Search documents by content."""
        pass
    
    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Update document."""
        pass
    
    @abstractmethod
    async def delete(self, document_id: UUID) -> None:
        """Delete document."""
        pass


__all__ = ["DocumentRepository"]
''',
}

# API Schema Templates
SCHEMA_TEMPLATES = {
    "zeta_vn/app/schemas/agent.py": '''"""Agent API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.core.domain.entities.Agent import Agent


class AgentCreate(BaseModel):
    """Schema for creating agent."""
    
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    system_prompt: str = Field(default="", max_length=2000)
    model_name: str = Field(default="gpt-3.5-turbo")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    capabilities: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentUpdate(BaseModel):
    """Schema for updating agent."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    system_prompt: Optional[str] = Field(None, max_length=2000)
    model_name: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1)
    capabilities: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    """Schema for agent response."""
    
    id: UUID
    user_id: UUID
    name: str
    description: str
    system_prompt: str
    model_name: str
    temperature: float
    max_tokens: Optional[int]
    is_active: bool
    capabilities: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, agent: Agent) -> AgentResponse:
        """Convert from domain entity."""
        return cls(
            id=agent.id,
            user_id=agent.user_id,
            name=agent.name,
            description=agent.description,
            system_prompt=agent.system_prompt,
            model_name=agent.model_name,
            temperature=agent.temperature,
            max_tokens=agent.max_tokens,
            is_active=agent.is_active,
            capabilities=agent.capabilities,
            metadata=agent.metadata,
            created_at=agent.created_at,
            updated_at=agent.updated_at
        )


__all__ = ["AgentCreate", "AgentUpdate", "AgentResponse"]
''',
    "zeta_vn/app/schemas/chat.py": '''"""Chat API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.core.domain.entities.Chat import Chat, Message


class ChatCreate(BaseModel):
    """Schema for creating chat."""
    
    agent_id: Optional[UUID] = None
    title: str = Field(min_length=1, max_length=200)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageCreate(BaseModel):
    """Schema for creating message."""
    
    role: str = Field(regex=r"^(user|assistant|system)$")
    content: str = Field(min_length=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MessageResponse(BaseModel):
    """Schema for message response."""
    
    id: UUID
    chat_id: UUID
    role: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    
    @classmethod
    def from_entity(cls, message: Message) -> MessageResponse:
        """Convert from domain entity."""
        return cls(
            id=message.id,
            chat_id=message.chat_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata,
            created_at=message.created_at
        )


class ChatResponse(BaseModel):
    """Schema for chat response."""
    
    id: UUID
    user_id: UUID
    agent_id: Optional[UUID]
    title: str
    is_active: bool
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, chat: Chat) -> ChatResponse:
        """Convert from domain entity."""
        return cls(
            id=chat.id,
            user_id=chat.user_id,
            agent_id=chat.agent_id,
            title=chat.title,
            is_active=chat.is_active,
            metadata=chat.metadata,
            created_at=chat.created_at,
            updated_at=chat.updated_at
        )


__all__ = ["ChatCreate", "MessageCreate", "MessageResponse", "ChatResponse"]
''',
    "zeta_vn/app/schemas/memory.py": '''"""Memory API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.core.domain.entities.Memory import Memory


class MemoryCreate(BaseModel):
    """Schema for creating memory."""
    
    content: str = Field(min_length=1)
    content_type: str = Field(default="text")
    tags: List[str] = Field(default_factory=list)
    importance: float = Field(default=1.0, ge=0.0, le=10.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MemorySearch(BaseModel):
    """Schema for searching memories."""
    
    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=100)


class MemoryResponse(BaseModel):
    """Schema for memory response."""
    
    id: UUID
    user_id: UUID
    content: str
    content_type: str
    tags: List[str]
    importance: float
    metadata: Dict[str, Any]
    created_at: datetime
    accessed_at: datetime
    access_count: int
    
    @classmethod
    def from_entity(cls, memory: Memory) -> MemoryResponse:
        """Convert from domain entity."""
        return cls(
            id=memory.id,
            user_id=memory.user_id,
            content=memory.content,
            content_type=memory.content_type,
            tags=memory.tags,
            importance=memory.importance,
            metadata=memory.metadata,
            created_at=memory.created_at,
            accessed_at=memory.accessed_at,
            access_count=memory.access_count
        )


__all__ = ["MemoryCreate", "MemorySearch", "MemoryResponse"]
''',
    "zeta_vn/app/schemas/rag.py": '''"""RAG API schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from apps.backend.core.domain.entities.Document import Document


class DocumentCreate(BaseModel):
    """Schema for creating document."""
    
    filename: str = Field(min_length=1)
    content: str = Field(min_length=1)
    content_type: str = Field(default="text/plain")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DocumentResponse(BaseModel):
    """Schema for document response."""
    
    id: UUID
    user_id: UUID
    filename: str
    content_type: str
    file_size: int
    chunks_count: int
    is_processed: bool
    metadata: Dict[str, Any]
    created_at: datetime
    processed_at: Optional[datetime]
    
    @classmethod
    def from_entity(cls, document: Document) -> DocumentResponse:
        """Convert from domain entity."""
        return cls(
            id=document.id,
            user_id=document.user_id,
            filename=document.filename,
            content_type=document.content_type,
            file_size=document.file_size,
            chunks_count=document.chunks_count,
            is_processed=document.is_processed,
            metadata=document.metadata,
            created_at=document.created_at,
            processed_at=document.processed_at
        )


class QueryRequest(BaseModel):
    """Schema for RAG query request."""
    
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class QueryResult(BaseModel):
    """Schema for single query result."""
    
    document_id: str
    filename: str
    content: str
    score: float


class QueryResponse(BaseModel):
    """Schema for RAG query response."""
    
    query: str
    results: List[QueryResult]
    total_results: int


__all__ = [
    "DocumentCreate", "DocumentResponse",
    "QueryRequest", "QueryResult", "QueryResponse"
]
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


def enhance_repositories_and_schemas() -> int:
    """Enhance repositories and schemas."""
    print("🔧 REPOSITORIES & SCHEMAS ENHANCEMENT")
    print("=" * 50)

    enhanced_count = 0

    # Create repository interfaces
    print("\n1️⃣ Creating repository interfaces...")
    for file_path, content in REPOSITORY_TEMPLATES.items():
        if not Path(file_path).exists():
            if enhance_file(file_path, content):
                print(f"✅ Created {file_path}")
                enhanced_count += 1
        else:
            print(f"⏭️  Exists {file_path}")

    # Create API schemas
    print("\n2️⃣ Creating API schemas...")
    for file_path, content in SCHEMA_TEMPLATES.items():
        if not Path(file_path).exists():
            if enhance_file(file_path, content):
                print(f"✅ Created {file_path}")
                enhanced_count += 1
        else:
            print(f"⏭️  Exists {file_path}")

    print("\n📊 REPOSITORIES & SCHEMAS COMPLETE")
    print(f"   Enhanced files: {enhanced_count}")

    return enhanced_count


if __name__ == "__main__":
    enhanced_count = enhance_repositories_and_schemas()
    if enhanced_count > 0:
        print("\n🚀 Repositories and schemas enhanced successfully!")
    else:
        print("\n✅ Repositories and schemas already complete")
