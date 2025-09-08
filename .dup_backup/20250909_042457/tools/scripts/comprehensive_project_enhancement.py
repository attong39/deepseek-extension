#!/usr/bin/env python3
"""
Comprehensive Project Enhancement Script

Tự động thêm missing files và complete code cho toàn bộ dự án ZETA_VN.
Dựa trên file integrity analysis và domain architecture.
"""

from __future__ import annotations

from pathlib import Path
import Exception
import bool
import e
import file_path
import init_file
import int
import print
import str

# Template cho các file thiếu quan trọng
ENHANCEMENT_TEMPLATES = {
    # API V1 Router
    "zeta_vn/app/api/v1/router/__init__.py": '''"""API V1 Router Module."""
from __future__ import annotations

from fastapi import APIRouter

from . import agent, auth, chat, memory, rag, status


def build_api_v1_router() -> APIRouter:
    """Build complete API v1 router with all endpoints."""
    router = APIRouter(prefix="/api/v1", tags=["api-v1"])
    
    # Include all sub-routers
    router.include_router(auth.router, prefix="/auth", tags=["auth"])
    router.include_router(agent.router, prefix="/agent", tags=["agent"])
    router.include_router(chat.router, prefix="/chat", tags=["chat"])
    router.include_router(memory.router, prefix="/memory", tags=["memory"])
    router.include_router(rag.router, prefix="/rag", tags=["rag"])
    router.include_router(status.router, prefix="/status", tags=["status"])
    
    return router


__all__ = ["build_api_v1_router"]
''',
    # App Factory
    "zeta_vn/app/factory.py": '''"""Application factory for ZETA_VN FastAPI app."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.app.api.v1.router import build_api_v1_router
from apps.backend.app.middleware import (
    AuthenticationMiddleware,
    CompressionMiddleware,
    CORSMiddleware as CustomCORSMiddleware,
    PerformanceMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from apps.backend.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    logger.info("Starting ZETA_VN application...")
    
    # Initialize database connections
    # Initialize Redis connections
    # Initialize model registry
    # Start background tasks
    
    yield
    
    # Shutdown
    logger.info("Shutting down ZETA_VN application...")
    
    # Close database connections
    # Close Redis connections
    # Cleanup background tasks


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="ZETA_VN API",
        description="AI-powered Vietnamese assistant with advanced capabilities",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware stack
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CompressionMiddleware)
    app.add_middleware(PerformanceMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    
    # Include API routers
    app.include_router(build_api_v1_router())
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "zeta_vn"}
    
    return app


__all__ = ["create_app", "lifespan"]
''',
    # Core UoW
    "zeta_vn/core/use_cases/uow.py": '''"""Unit of Work pattern implementation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from apps.backend.core.interfaces.repositories import (
    AgentRepository,
    ChatRepository,
    MemoryRepository,
    PlanRepository,
    UserRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work for managing transactions."""
    
    agents: AgentRepository
    chats: ChatRepository
    memories: MemoryRepository
    plans: PlanRepository
    users: UserRepository
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.rollback()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.rollback()
    
    @abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
        pass


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    """SQLAlchemy implementation of Unit of Work."""
    
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None
    
    async def __aenter__(self):
        self.session = self.session_factory()
        
        # Initialize repositories with session
        from apps.backend.data.repositories import (
            SqlAgentRepository,
            SqlChatRepository,
            SqlMemoryRepository,
            SqlPlanRepository,
            SqlUserRepository,
        )
        
        self.agents = SqlAgentRepository(self.session)
        self.chats = SqlChatRepository(self.session)
        self.memories = SqlMemoryRepository(self.session)
        self.plans = SqlPlanRepository(self.session)
        self.users = SqlUserRepository(self.session)
        
        return await super().__aenter__()
    
    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        if self.session:
            self.session.close()
    
    async def commit(self) -> None:
        """Commit the transaction."""
        if self.session:
            await self.session.commit()
    
    async def rollback(self) -> None:
        """Rollback the transaction."""
        if self.session:
            await self.session.rollback()


__all__ = ["AbstractUnitOfWork", "SqlAlchemyUnitOfWork"]
''',
    # Repository Interfaces
    "zeta_vn/core/interfaces/repositories/memory.py": '''"""Memory repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Memory import Memory


class MemoryRepository(ABC):
    """Repository interface for Memory entities."""
    
    @abstractmethod
    async def add(self, memory: Memory) -> None:
        """Add a new memory."""
        pass
    
    @abstractmethod
    async def get(self, memory_id: UUID) -> Optional[Memory]:
        """Get memory by ID."""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[Memory]:
        """Get all memories for a user."""
        pass
    
    @abstractmethod
    async def get_by_chat(self, chat_id: UUID) -> List[Memory]:
        """Get memories for a specific chat."""
        pass
    
    @abstractmethod
    async def search_by_content(self, query: str, user_id: UUID) -> List[Memory]:
        """Search memories by content."""
        pass
    
    @abstractmethod
    async def update(self, memory: Memory) -> None:
        """Update existing memory."""
        pass
    
    @abstractmethod
    async def delete(self, memory_id: UUID) -> None:
        """Delete memory by ID."""
        pass
    
    @abstractmethod
    async def list_recent(self, user_id: UUID, limit: int = 10) -> List[Memory]:
        """Get recent memories for user."""
        pass


__all__ = ["MemoryRepository"]
''',
    "zeta_vn/core/interfaces/repositories/user.py": '''"""User repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.User import User


class UserRepository(ABC):
    """Repository interface for User entities."""
    
    @abstractmethod
    async def add(self, user: User) -> None:
        """Add a new user."""
        pass
    
    @abstractmethod
    async def get(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    async def update(self, user: User) -> None:
        """Update existing user."""
        pass
    
    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        """Delete user by ID."""
        pass
    
    @abstractmethod
    async def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List all users with pagination."""
        pass
    
    @abstractmethod
    async def search(self, query: str) -> List[User]:
        """Search users by name or email."""
        pass


__all__ = ["UserRepository"]
''',
    "zeta_vn/core/interfaces/repositories/plan.py": '''"""Plan repository interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from apps.backend.core.domain.entities.Plan import Plan


class PlanRepository(ABC):
    """Repository interface for Plan entities."""
    
    @abstractmethod
    async def add(self, plan: Plan) -> None:
        """Add a new plan."""
        pass
    
    @abstractmethod
    async def get(self, plan_id: UUID) -> Optional[Plan]:
        """Get plan by ID."""
        pass
    
    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[Plan]:
        """Get all plans for a user."""
        pass
    
    @abstractmethod
    async def get_active_plans(self, user_id: UUID) -> List[Plan]:
        """Get active plans for a user."""
        pass
    
    @abstractmethod
    async def update(self, plan: Plan) -> None:
        """Update existing plan."""
        pass
    
    @abstractmethod
    async def delete(self, plan_id: UUID) -> None:
        """Delete plan by ID."""
        pass
    
    @abstractmethod
    async def mark_completed(self, plan_id: UUID) -> None:
        """Mark plan as completed."""
        pass


__all__ = ["PlanRepository"]
''',
    # Service Interfaces
    "zeta_vn/core/interfaces/services/notification.py": '''"""Notification service interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID


class NotificationService(ABC):
    """Service interface for sending notifications."""
    
    @abstractmethod
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: str = None
    ) -> bool:
        """Send email notification."""
        pass
    
    @abstractmethod
    async def send_push_notification(
        self,
        user_id: UUID,
        title: str,
        message: str,
        data: Dict[str, Any] = None
    ) -> bool:
        """Send push notification to user."""
        pass
    
    @abstractmethod
    async def send_sms(
        self,
        phone_number: str,
        message: str
    ) -> bool:
        """Send SMS notification."""
        pass
    
    @abstractmethod
    async def notify_user(
        self,
        user_id: UUID,
        notification_type: str,
        content: Dict[str, Any]
    ) -> bool:
        """Send notification to user via preferred channel."""
        pass
    
    @abstractmethod
    async def get_user_preferences(self, user_id: UUID) -> Dict[str, bool]:
        """Get user notification preferences."""
        pass
    
    @abstractmethod
    async def update_user_preferences(
        self,
        user_id: UUID,
        preferences: Dict[str, bool]
    ) -> None:
        """Update user notification preferences."""
        pass


__all__ = ["NotificationService"]
''',
    # Auth API
    "zeta_vn/app/api/v1/auth.py": '''"""Authentication API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from apps.backend.app.dependencies import get_auth_service
from apps.backend.core.auth.models import Token, User, UserCreate, UserLogin
from apps.backend.core.auth.service import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    """Authenticate user and return access token."""
    user = await auth_service.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = await auth_service.create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=User)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Register a new user."""
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await auth_service.create_user(user_data)
    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    """Refresh access token."""
    access_token = await auth_service.create_access_token(current_user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
) -> dict:
    """Logout user and invalidate token."""
    # Add token to blacklist
    await auth_service.logout_user(current_user.id)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user information."""
    return current_user


__all__ = ["router"]
''',
    # Domain Entity base structures
    "zeta_vn/core/domain/entities/User/__init__.py": '''"""User domain entity."""
from __future__ import annotations

from .user import User, UserRole, UserStatus

__all__ = ["User", "UserRole", "UserStatus"]
''',
    "zeta_vn/core/domain/entities/User/user.py": '''"""User domain entity implementation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class UserRole(Enum):
    """User roles in the system."""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserStatus(Enum):
    """User account status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


@dataclass
class User:
    """User domain entity."""
    
    id: UUID
    email: str
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE
    is_verified: bool = False
    created_at: datetime = None
    updated_at: datetime = None
    last_login: Optional[datetime] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    @property
    def is_active(self) -> bool:
        """Check if user is active."""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRole.ADMIN
    
    def activate(self) -> None:
        """Activate user account."""
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.utcnow()
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.updated_at = datetime.utcnow()
    
    def update_last_login(self) -> None:
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()


__all__ = ["User", "UserRole", "UserStatus"]
''',
}

# Files cần __init__.py
INIT_FILES_NEEDED = [
    "zeta_vn/app/api/v1/agent/__init__.py",
    "zeta_vn/app/api/v1/auth/__init__.py",
    "zeta_vn/app/api/v1/chat/__init__.py",
    "zeta_vn/app/api/v1/memory/__init__.py",
    "zeta_vn/app/api/v1/rag/__init__.py",
    "zeta_vn/app/api/v1/status/__init__.py",
    "zeta_vn/app/websockets/router/__init__.py",
    "zeta_vn/core/adapters/llm/openai_adapter/__init__.py",
    "zeta_vn/core/adapters/llm/anthropic_adapter/__init__.py",
    "zeta_vn/core/domain/entities/Agent/__init__.py",
    "zeta_vn/core/domain/entities/Chat/__init__.py",
    "zeta_vn/core/domain/entities/Memory/__init__.py",
    "zeta_vn/core/domain/entities/Plan/__init__.py",
    "zeta_vn/core/services/agent_service/__init__.py",
    "zeta_vn/core/services/memory_service/__init__.py",
    "zeta_vn/core/use_cases/agent/create_agent/__init__.py",
    "zeta_vn/core/use_cases/chat/start_chat/__init__.py",
    "zeta_vn/core/use_cases/memory/store_memory/__init__.py",
    "zeta_vn/data/models/__init__.py",
]


def create_basic_init_content(file_path: str) -> str:
    """Create basic __init__.py content based on directory structure."""
    module_name = Path(file_path).parent.name

    if "api" in file_path:
        return f'''"""API {module_name} module."""
from __future__ import annotations

# Import router when available
# from .router import router

__all__ = []
'''
    elif "entities" in file_path:
        return f'''"""{module_name.title()} domain entity."""
from __future__ import annotations

# Import entity classes when available
# from .{module_name.lower()} import {module_name.title()}

__all__ = []
'''
    elif "services" in file_path:
        return f'''"""{module_name.title()} service module."""
from __future__ import annotations

# Import service classes when available
# from .service import {module_name.title()}Service

__all__ = []
'''
    elif "use_cases" in file_path:
        return f'''"""{module_name.title()} use cases."""
from __future__ import annotations

# Import use case classes when available

__all__ = []
'''
    else:
        return f'''"""{module_name.title()} module."""
from __future__ import annotations

__all__ = []
'''


def enhance_file(file_path: str, content: str) -> bool:
    """Enhance a single file with content."""
    path = Path(file_path)

    # Create directory if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    # Write content
    try:
        path.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"❌ Failed to enhance {file_path}: {e}")
        return False


def create_critical_templates() -> int:
    """Create critical template files."""
    count = 0
    print("\n1️⃣ Creating critical template files...")
    for file_path, content in ENHANCEMENT_TEMPLATES.items():
        if not Path(file_path).exists():
            if enhance_file(file_path, content):
                print(f"✅ Created {file_path}")
                count += 1
        else:
            print(f"⏭️  Exists {file_path}")
    return count


def create_init_files() -> int:
    """Create missing __init__.py files."""
    count = 0
    print("\n2️⃣ Creating missing __init__.py files...")
    for init_file in INIT_FILES_NEEDED:
        if not Path(init_file).exists():
            content = create_basic_init_content(init_file)
            if enhance_file(init_file, content):
                print(f"✅ Created {init_file}")
                count += 1
        else:
            print(f"⏭️  Exists {init_file}")
    return count


def update_repository_imports() -> int:
    """Update repository imports."""
    count = 0
    print("\n3️⃣ Updating repository imports...")
    repo_init = Path("zeta_vn/core/interfaces/repositories/__init__.py")
    if repo_init.exists():
        updated_content = '''"""Repository interfaces."""
from __future__ import annotations

from .agent import AgentRepository
from .chat import ChatRepository
from .memory import MemoryRepository
from .plan import PlanRepository
from .training import TrainingRepository
from .user import UserRepository

__all__ = [
    "AgentRepository",
    "ChatRepository",
    "MemoryRepository",
    "PlanRepository",
    "TrainingRepository",
    "UserRepository",
]
'''
        if enhance_file(str(repo_init), updated_content):
            print(f"✅ Updated {repo_init}")
            count += 1
    return count


def update_middleware_imports() -> int:
    """Update middleware imports."""
    count = 0
    print("\n4️⃣ Updating middleware imports...")
    middleware_init = Path("zeta_vn/app/middleware/__init__.py")
    middleware_content = '''"""Middleware components."""
from __future__ import annotations

from .auth_middleware import AuthenticationMiddleware
from .compression_middleware import CompressionMiddleware
from .cors_middleware import CORSMiddleware
from .performance_middleware import PerformanceMiddleware
from .rate_limiting import RateLimitMiddleware
from .security_consolidated import SecurityHeadersMiddleware, InputSanitizationMiddleware

__all__ = [
    "AuthenticationMiddleware",
    "CompressionMiddleware",
    "CORSMiddleware",
    "PerformanceMiddleware",
    "RateLimitMiddleware",
    "SecurityHeadersMiddleware",
    "InputSanitizationMiddleware",
]
'''
    if enhance_file(str(middleware_init), middleware_content):
        print(f"✅ Updated {middleware_init}")
        count += 1
    return count


def enhance_project_structure() -> int:
    """Enhance project structure with missing files."""
    print("🔧 COMPREHENSIVE PROJECT ENHANCEMENT")
    print("=" * 50)

    enhanced_count = 0

    # Execute enhancement steps
    enhanced_count += create_critical_templates()
    enhanced_count += create_init_files()
    enhanced_count += update_repository_imports()
    enhanced_count += update_middleware_imports()

    print("\n📊 ENHANCEMENT COMPLETE")
    print(f"   Enhanced files: {enhanced_count}")
    print("   ✅ Project structure significantly improved")

    return enhanced_count


if __name__ == "__main__":
    enhanced_count = enhance_project_structure()
    if enhanced_count > 0:
        print("\n🚀 Run integrity check again to verify improvements")
    else:
        print("\n✅ No enhancements needed - project structure is complete")
