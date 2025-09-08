"""Dependency injection container"""

from __future__ import annotations

from typing import Any

from apps.backend.core.interfaces.repositories.agent_repository import (
    AgentRepositoryInterface,
)
from apps.backend.core.interfaces.repositories.user_repository import (
    UserRepositoryInterface,
)
from apps.backend.core.interfaces.services.ai_service import AIServiceInterface

# Import implementations
try:
    from apps.backend.core.services.ai.orchestrator import AIOrchestrator
    from apps.backend.data.repositories.agent_repository import AgentRepository
    from apps.backend.data.repositories.user_repository import UserRepository
except ImportError:
    # Fallback if implementations don't exist
    UserRepository = None
    AgentRepository = None
    AIOrchestrator = None

# Import new AI engines with fallback
try:
    from .ai.rag_service import RagService
    from .ai.asr_service import ASRService
    from .ai.ocr_service import OCRService
    from .ai.embedder import Embedder
    from .ai.llm import LLMClient
except ImportError:
    # Fallback if engines not available
    RagService = None
    ASRService = None
    OCRService = None
    Embedder = None
    LLMClient = None


class DIContainer:
    """Simple dependency injection container"""
import ImportError
import actor_id
import agent_id
import credentials
import current_user
import dict
import float
import getattr
import hash
import instance
import int
import list
import plan
import request
import required_permissions
import self
import service_name
import session
import set
import str
import updates
import vo

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup service bindings"""

        # Repositories
        if UserRepository:
            self._services["user_repository"] = UserRepository()

        if AgentRepository:
            self._services["agent_repository"] = AgentRepository()

        # Services
        if AIOrchestrator:
            self._services["ai_service"] = AIOrchestrator()

        # AI Engines (One-Click Learning)
        if RagService:
            self._services["rag_service"] = RagService(data_dir="data")
        
        if ASRService:
            self._services["asr_service"] = ASRService()
        
        if OCRService:
            self._services["ocr_service"] = OCRService()
        
        if Embedder:
            self._services["embedder"] = Embedder()
            
        if LLMClient:
            self._services["llm_client"] = LLMClient()

    def get(self, service_name: str) -> Any:
        """Get service instance"""
        return self._services.get(service_name)

    def register(self, service_name: str, instance: Any) -> None:
        """Register service instance"""
        self._services[service_name] = instance


# Global container instance
container = DIContainer()


def get_user_repository() -> UserRepositoryInterface:
    """Get user repository"""
    return container.get("user_repository")


def get_agent_repository() -> AgentRepositoryInterface:
    """Get agent repository"""
    return container.get("agent_repository")


def get_ai_service() -> AIServiceInterface:
    """Get AI service"""
    return container.get("ai_service")


# -------------------------------------------------------------------------
# Clean DI Architecture Extensions (for zeta_vn clean architecture)
# -------------------------------------------------------------------------
from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


# Mock implementations for the clean DI architecture
class MockDatabaseSession:
    """Mock database session - replace with real SQLAlchemy session."""
    
    def __init__(self):
        self.is_active = True
        
    async def close(self):
        self.is_active = False
        
    async def commit(self):
        pass
        
    async def rollback(self):
        pass


async def get_db_session() -> MockDatabaseSession:
    """Return a fresh database session for clean DI."""
    return MockDatabaseSession()


# Authentication for clean DI
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Extract and validate user from JWT token (clean DI version)."""
    # Mock implementation - replace with real auth
    if credentials.credentials == "valid-token":
        from apps.backend.core.domain.entities.user import User
        return User(
            id="user-123",
            username="testuser", 
            email="test@example.com",
            scopes=["agent:read", "agent:create", "plan:read", "plan:create"]
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_permissions(*required_permissions: str) -> Callable:
    """RBAC dependency factory – creates a dependency that checks user permissions."""
    
    async def permission_checker(current_user = Depends(get_current_user)):
        user_permissions = set(getattr(current_user, 'scopes', []) or [])
        
        # Admin wildcard permission grants everything
        if "admin:*" in user_permissions:
            return current_user
            
        # Check specific permissions
        missing_permissions = set(required_permissions) - user_permissions
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        
        return current_user
    
    return permission_checker


# Clean DI repository factories
async def get_agent_repository_clean_di(session = Depends(get_db_session)):
    """Factory for AgentRepository (clean DI version)."""
    # Mock implementation
    class MockAgentRepository:
        def __init__(self, session):
            self.session = session
            
        async def get_by_id(self, agent_id: str):
            # Return mock agent
            from datetime import datetime
            class MockAgent:
                def __init__(self):
                    self.id = agent_id
                    self.name = f"Agent {agent_id}"
                    self.description = "Mock agent"
                    self.owner_id = "user-123"
                    self.created_at = datetime.utcnow()
                    self.updated_at = None
            return MockAgent()
            
        async def get_by_owner(self, owner_id: str, skip=0, limit=100):
            return []
            
        async def list_all(self, skip=0, limit=100):
            return []
            
        async def delete(self, agent_id: str):
            return True
            
    return MockAgentRepository(session)


async def get_plan_repository_clean_di(session = Depends(get_db_session)):
    """Factory for PlanRepository (clean DI version)."""
    # Mock implementation
    class MockPlanRepository:
        def __init__(self, session):
            self.session = session
            
        async def get_by_id(self, plan_id: str):
            return None
            
        async def get_by_user(self, user_id: str, skip=0, limit=100, status=None):
            return []
            
        async def list_all(self, skip=0, limit=100, status=None):
            return []
            
        async def update(self, plan):
            return plan
            
        async def delete(self, plan_id: str):
            return True
            
    return MockPlanRepository(session)


async def get_audit_service_clean_di(session = Depends(get_db_session)):
    """Factory for AuditService (clean DI version)."""
    class MockAuditService:
        def __init__(self, session):
            self.session = session
            
        async def log_action(self, actor_id: str, action: str, resource_type: str, 
                           resource_id: str, context: dict, details: dict = None):
            # Mock audit logging
            pass
            
    return MockAuditService(session)


async def get_audit_context(request: Request) -> dict:
    """Extract audit context from request."""
    return {
        "ip_address": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "endpoint": str(request.url.path),
        "method": request.method,
    }


# Mock Use Cases for clean DI
class MockCreateAgentUC:
    async def execute(self, vo: dict, audit_context: dict):
        from datetime import datetime
        class MockAgent:
            def __init__(self):
                self.id = f"agent-{hash(vo['name'])}"
                self.name = vo["name"]
                self.description = vo.get("description")
                self.owner_id = vo["owner_id"]
                self.created_at = datetime.utcnow()
                self.updated_at = None
        return MockAgent()


class MockUpdateAgentUC:
    async def execute(self, agent_id: str, updates: dict, actor_id: str, audit_context: dict):
        from datetime import datetime
        class MockAgent:
            def __init__(self):
                self.id = agent_id
                self.name = updates.get("name", "Updated Agent")
                self.description = updates.get("description")
                self.owner_id = actor_id
                self.created_at = datetime.utcnow()
                self.updated_at = datetime.utcnow()
        return MockAgent()


async def get_create_agent_uc():
    return MockCreateAgentUC()


async def get_update_agent_uc():
    return MockUpdateAgentUC()


async def get_create_plan_uc():
    class MockCreatePlanUC:
        async def execute(self, vo: dict, audit_context: dict):
            return None  # Mock implementation
    return MockCreatePlanUC()


async def get_approve_plan_uc():
    class MockApprovePlanUC:
        async def execute(self, plan_id: str, approved_by: str, audit_context: dict):
            return None  # Mock implementation
    return MockApprovePlanUC()


async def get_execute_plan_uc():
    class MockExecutePlanUC:
        async def execute(self, plan_id: str, executor_id: str, audit_context: dict):
            return None  # Mock implementation
    return MockExecutePlanUC()


# Type aliases for cleaner signatures
CurrentUserDep = Annotated[Any, Depends(get_current_user)]
CreateAgentUC = Annotated[Any, Depends(get_create_agent_uc)]
UpdateAgentUC = Annotated[Any, Depends(get_update_agent_uc)]
CreatePlanUC = Annotated[Any, Depends(get_create_plan_uc)]
ApprovePlanUC = Annotated[Any, Depends(get_approve_plan_uc)]
ExecutePlanUC = Annotated[Any, Depends(get_execute_plan_uc)]
AuditContextDep = Annotated[dict, Depends(get_audit_context)]


# ── One-Click Learning Dependencies ──────────────────────────

async def get_rag_engine():
    """Get RAG engine instance."""
    container_service = container.get("rag_service")
    if container_service is None:
        # Fallback: create a simple mock
        class MockRAGEngine:
            def search(self, query: str, k: int = 5, score_threshold: float = 0.1):
                return []
            def add_documents(self, texts: list[str], metadata: list[dict] = None):
                pass
        return MockRAGEngine()
    return container_service


async def get_asr_engine():
    """Get ASR engine instance."""
    container_service = container.get("asr_service") 
    if container_service is None:
        # Fallback: create a simple mock
        class MockASREngine:
            def transcribe(self, audio_path: str, **kwargs):
                return {"text": "Mock transcription", "language": "en"}
        return MockASREngine()
    return container_service


async def get_ocr_engine():
    """Get OCR engine instance."""
    container_service = container.get("ocr_service")
    if container_service is None:
        # Fallback: create a simple mock
        class MockOCREngine:
            def extract_text(self, image_path: str, **kwargs):
                return {"text": "Mock OCR text", "backend": "mock"}
        return MockOCREngine()
    return container_service


async def get_current_user_websocket(websocket) -> Any:
    """Get current user for WebSocket connections (simplified for demo)."""
    # In production, implement proper WebSocket auth
    # For now, return a mock user
    class MockUser:
        def __init__(self):
            self.id = "ws_user_123"
            self.username = "websocket_user"
            self.email = "ws@example.com"
    
    return MockUser()


# Additional type aliases for One-Click Learning
RAGEngineDep = Annotated[Any, Depends(get_rag_engine)]
ASREngineDep = Annotated[Any, Depends(get_asr_engine)]
OCREngineDep = Annotated[Any, Depends(get_ocr_engine)]


# ---- AI Factories cho One-Click Learning ---- #
def get_embedder():
    """Get embedder service instance."""
    from .ai.embedder import Embedder
    return Embedder()

def get_rag_service():
    """Get RAG service instance."""
    from .ai.rag_service import RagService
    return RagService(data_dir="data")

def get_llm_client():
    """Get LLM client instance.""" 
    from .ai.llm import LLMClient
    return LLMClient()

def get_asr_service():
    """Get ASR service instance."""
    from .ai.asr_service import ASRService
    return ASRService()

def get_ocr_service():
    """Get OCR service instance."""
    from .ai.ocr_service import OCRService
    return OCRService()


# ---- Singleton instances for performance ---- #
_embedder_instance = None
_rag_service_instance = None
_llm_client_instance = None
_asr_service_instance = None
_ocr_service_instance = None

def get_embedder_singleton():
    """Get singleton embedder instance."""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = get_embedder()
    return _embedder_instance

def get_rag_service_singleton():
    """Get singleton RAG service instance."""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = get_rag_service()
    return _rag_service_instance

def get_llm_client_singleton():
    """Get singleton LLM client instance."""
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = get_llm_client()
    return _llm_client_instance

def get_asr_service_singleton():
    """Get singleton ASR service instance."""
    global _asr_service_instance
    if _asr_service_instance is None:
        _asr_service_instance = get_asr_service()
    return _asr_service_instance

def get_ocr_service_singleton():
    """Get singleton OCR service instance."""
    global _ocr_service_instance
    if _ocr_service_instance is None:
        _ocr_service_instance = get_ocr_service()
    return _ocr_service_instance
