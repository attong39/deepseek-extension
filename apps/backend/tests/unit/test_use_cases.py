import os
from datetime import datetime
import Exception
import ValueError
import all
import bool
import callable
import dict
import expected_agent
import hasattr
import isinstance
import len
import list
import original_agent
import step
import str

"""
🧪 Unit Tests for Use Cases - ZETA AI SERVER
==========================================

Comprehensive unit tests for domain use cases covering:
- Authentication & authorization
- Memory management operations
- Chat functionality & messaging
- Planning & execution workflows
- Agent lifecycle management

These tests validate business logic execution, input validation,
error handling, and proper repository interaction patterns.
"""

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID, uuid4

import pytest

from core.domain.entities.agent import Agent, AgentCapability, AgentConfig, AgentStatus
from core.domain.entities.chat import ChatMessage
from core.domain.entities.memory import Memory, MemoryImportance, MemoryType
from core.domain.entities.plan import Plan, PlanStatus, PlanStep
from core.domain.entities.user import User
from core.domain.value_objects.auth import LoginRequest, TokenResponse
from core.exceptions.auth_exceptions import InvalidCredentialsError
from core.use_cases.agent.create_agent import CreateAgent
from core.use_cases.agent.deploy_agent import DeployAgentUseCase
from core.use_cases.auth.authenticate_user import AuthenticateUser
from core.use_cases.chat.send_message import SendMessageUseCase
from core.use_cases.memory.store_memory import StoreMemory
from core.use_cases.planning.create_plan import CreatePlan


class TestAuthenticationUseCases:
    """Test authentication and authorization use cases."""

    @pytest.fixture
    def mock_user_repo(self) -> Mock:
        """Mock user repository."""
        return Mock()

    @pytest.fixture
    def authenticate_use_case(self, mock_user_repo: Mock) -> AuthenticateUser:
        """Create authenticate user use case."""
        return AuthenticateUser(mock_user_repo)

    @pytest.mark.asyncio
    async def test_authenticate_user_success(
        self,
        authenticate_use_case: AuthenticateUser,
        mock_user_repo: Mock,
    ) -> None:
        """Test successful user authentication."""
        # Arrange
        user_id = str(uuid4())
        user = User(
            id=user_id,
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password_hash="$2b$12$hashed_password",
            is_active=True,
        )

        login_request = LoginRequest(
            email="test@example.com", password=os.getenv("PASSWORD")
        )

        mock_user_repo.get_by_email = AsyncMock(return_value=user)

        with (
            patch("bcrypt.checkpw", return_value=True),
            patch("jwt.encode", return_value="mock_token"),
        ):
            # Act
            _ = await authenticate_use_case(login_request)

            # Assert
            assert isinstance(result, TokenResponse)
            assert result.access_token == "mock_token"
            assert result.token_type == "bearer"
            mock_user_repo.get_by_email.assert_called_once_with("test@example.com")

    @pytest.mark.asyncio
    async def test_authenticate_user_invalid_credentials(
        self,
        authenticate_use_case: AuthenticateUser,
        mock_user_repo: Mock,
    ) -> None:
        """Test authentication with invalid credentials."""
        # Arrange
        login_request = LoginRequest(
            email="test@example.com", password=os.getenv("PASSWORD")
        )

        mock_user_repo.get_by_email = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await authenticate_use_case(login_request)

    @pytest.mark.asyncio
    async def test_authenticate_inactive_user(
        self,
        authenticate_use_case: AuthenticateUser,
        mock_user_repo: Mock,
    ) -> None:
        """Test authentication of inactive user."""
        # Arrange
        user = User(
            id=str(uuid4()),
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            password_hash="$2b$12$hashed_password",
            is_active=False,
        )

        login_request = LoginRequest(
            email="test@example.com", password=os.getenv("PASSWORD")
        )

        mock_user_repo.get_by_email = AsyncMock(return_value=user)

        # Act & Assert
        with pytest.raises(InvalidCredentialsError):
            await authenticate_use_case(login_request)


class TestMemoryUseCases:
    """Test memory management use cases."""

    @pytest.fixture
    def mock_memory_repo(self) -> Mock:
        """Mock memory repository."""
        return Mock()

    @pytest.fixture
    def store_memory_use_case(self, mock_memory_repo: Mock) -> StoreMemory:
        """Create store memory use case."""
        return StoreMemory(mock_memory_repo)

    @pytest.mark.asyncio
    async def test_store_memory_success(
        self,
        store_memory_use_case: StoreMemory,
        mock_memory_repo: Mock,
    ) -> None:
        """Test successful memory storage."""
        # Arrange
        memory_id = str(uuid4())
        agent_id = uuid4()
        content = "Important conversation about AI development"
        context = {"conversation_id": "chat_123", "topic": "development"}
        tags = ["ai", "development", "conversation"]

        expected_memory = Memory(
            id=UUID(memory_id),
            content=content,
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.HIGH,
            agent_id=agent_id,
            context=context,
            tags=tags,
            created_at=datetime.now(UTC),
        )

        mock_memory_repo.create = AsyncMock(return_value=expected_memory)

        # Act
        _ = await store_memory_use_case(
            content=content,
            memory_type="conversation",
            importance="high",
            agent_id=agent_id,
            context=context,
            tags=tags,
        )

        # Assert
        assert isinstance(result, Memory)
        assert result.content == content
        assert result.agent_id == agent_id
        assert result.context == context
        assert result.tags == tags
        mock_memory_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_store_memory_with_defaults(
        self,
        store_memory_use_case: StoreMemory,
        mock_memory_repo: Mock,
    ) -> None:
        """Test memory storage with default values."""
        # Arrange
        memory_id = str(uuid4())
        agent_id = uuid4()
        content = "Simple memory content"

        expected_memory = Memory(
            id=UUID(memory_id),
            content=content,
            type=MemoryType.EPISODIC,
            importance=MemoryImportance.MEDIUM,
            agent_id=agent_id,
            context={},
            tags=[],
            created_at=datetime.now(UTC),
        )

        mock_memory_repo.create = AsyncMock(return_value=expected_memory)

        # Act
        _ = await store_memory_use_case(
            content=content,
            memory_type="episodic",
            importance="medium",
            agent_id=agent_id,
            context={},
        )

        # Assert
        assert isinstance(result, Memory)
        assert result.content == content
        assert result.tags == []
        mock_memory_repo.create.assert_called_once()


class TestChatUseCases:
    """Test chat functionality use cases."""

    @pytest.fixture
    def mock_chat_repo(self) -> Mock:
        """Mock chat repository."""
        return Mock()

    @pytest.fixture
    def send_message_use_case(self, mock_chat_repo: Mock) -> SendMessageUseCase:
        """Create send message use case."""
        return SendMessageUseCase(mock_chat_repo)

    @pytest.mark.asyncio
    async def test_send_message_success(
        self,
        send_message_use_case: SendMessageUseCase,
        mock_chat_repo: Mock,
    ) -> None:
        """Test successful message sending."""
        # Arrange
        agent_id = str(uuid4())
        user_id = str(uuid4())
        content = "Hello, how can you help me today?"

        expected_response = ChatMessage(
            id=f"msg_{datetime.now().timestamp()}",
            content="Hello! I'm here to help you with any questions or tasks.",
            sender_type="agent",
            sender_id=agent_id,
            agent_id=agent_id,
            timestamp=datetime.now(UTC),
        )

        mock_chat_repo.send_message = AsyncMock(return_value=expected_response)

        # Act
        result = await send_message_use_case.execute(
            agent_id=agent_id,
            content=content,
            user_id=user_id,
        )

        # Assert
        assert isinstance(result, ChatMessage)
        assert result.content is not None
        assert result.agent_id == agent_id
        assert result.sender_id is not None

    @pytest.mark.asyncio
    async def test_send_empty_message_raises_error(
        self,
        send_message_use_case: SendMessageUseCase,
        mock_chat_repo: Mock,
    ) -> None:
        """Test sending empty message raises validation error."""
        # Arrange
        agent_id = str(uuid4())
        content = "   "  # Empty/whitespace content

        # Act & Assert
        with pytest.raises(ValueError, match="Message content cannot be empty"):
            result = await send_message_use_case.execute(
                agent_id=agent_id,
                content=content,
            )

    @pytest.mark.asyncio
    async def test_send_message_without_agent_id_raises_error(
        self,
        send_message_use_case: SendMessageUseCase,
        mock_chat_repo: Mock,
    ) -> None:
        """Test sending message without agent ID raises validation error."""
        # Arrange
        content = "Valid message content"

        # Act & Assert
        with pytest.raises(ValueError, match="Agent ID is required"):
            result = await send_message_use_case.execute(
                agent_id="",
                content=content,
            )


class TestPlanningUseCases:
    """Test planning and execution use cases."""

    @pytest.fixture
    def mock_plan_repo(self) -> Mock:
        """Mock plan repository."""
        return Mock()

    @pytest.fixture
    def create_plan_use_case(self, mock_plan_repo: Mock) -> CreatePlan:
        """Create plan use case."""
        return CreatePlan(mock_plan_repo)

    @pytest.mark.asyncio
    async def test_create_plan_success(
        self,
        create_plan_use_case: CreatePlan,
        mock_plan_repo: Mock,
    ) -> None:
        """Test successful plan creation."""
        # Arrange
        plan_id = str(uuid4())
        title = "AI Model Training Plan"
        description = "Comprehensive plan for training a new AI model"
        agent_id = str(uuid4())
        user_id = str(uuid4())

        steps_data = [
            {
                "action": "prepare_data",
                "description": "Prepare and clean training data",
                "parameters": {"dataset_size": 10000, "validation_split": 0.2},
            },
            {
                "action": "train_model",
                "description": "Train the AI model with prepared data",
                "parameters": {"epochs": 100, "batch_size": 32},
            },
            {
                "action": "evaluate_model",
                "description": "Evaluate model performance on test set",
                "parameters": {"metrics": ["accuracy", "precision", "recall"]},
            },
        ]

        expected_plan = Plan(
            id=plan_id,
            title=title,
            description=description,
            agent_id=agent_id,
            user_id=user_id,
            steps=[
                PlanStep(
                    id="step_1",
                    action="prepare_data",
                    description="Prepare and clean training data",
                    parameters={"dataset_size": 10000, "validation_split": 0.2},
                    order=1,
                ),
                PlanStep(
                    id="step_2",
                    action="train_model",
                    description="Train the AI model with prepared data",
                    parameters={"epochs": 100, "batch_size": 32},
                    order=2,
                ),
                PlanStep(
                    id="step_3",
                    action="evaluate_model",
                    description="Evaluate model performance on test set",
                    parameters={"metrics": ["accuracy", "precision", "recall"]},
                    order=3,
                ),
            ],
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        mock_plan_repo.create = AsyncMock(return_value=expected_plan)

        # Act
        _ = await create_plan_use_case(
            title=title,
            description=description,
            agent_id=agent_id,
            user_id=user_id,
            steps_data=steps_data,
        )

        # Assert
        assert isinstance(result, Plan)
        assert result.title == title
        assert result.description == description
        assert result.agent_id == agent_id
        assert result.user_id == user_id
        assert len(result.steps) == 3
        assert result.status == PlanStatus.DRAFT
        assert all(isinstance(step, PlanStep) for step in result.steps)
        mock_plan_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_plan_with_empty_steps(
        self,
        create_plan_use_case: CreatePlan,
        mock_plan_repo: Mock,
    ) -> None:
        """Test creating plan with empty steps list."""
        # Arrange
        title = "Simple Plan"
        description = "A plan with no steps"
        agent_id = str(uuid4())
        user_id = str(uuid4())
        steps_data: list[dict[str, Any]] = []

        expected_plan = Plan(
            id=str(uuid4()),
            title=title,
            description=description,
            agent_id=agent_id,
            user_id=user_id,
            steps=[],
            status=PlanStatus.DRAFT,
            created_at=datetime.now(UTC),
        )

        mock_plan_repo.create = AsyncMock(return_value=expected_plan)

        # Act
        _ = await create_plan_use_case(
            title=title,
            description=description,
            agent_id=agent_id,
            user_id=user_id,
            steps_data=steps_data,
        )

        # Assert
        assert isinstance(result, Plan)
        assert len(result.steps) == 0
        mock_plan_repo.create.assert_called_once()


class TestAgentUseCases:
    """Test agent lifecycle management use cases."""

    @pytest.fixture
    def mock_agent_repo(self) -> Mock:
        """Mock agent repository."""
        return Mock()

    @pytest.fixture
    def create_agent_use_case(self, mock_agent_repo: Mock) -> CreateAgent:
        """Create agent use case."""
        return CreateAgent(mock_agent_repo)

    @pytest.fixture
    def deploy_agent_use_case(self, mock_agent_repo: Mock) -> DeployAgentUseCase:
        """Deploy agent use case."""
        return DeployAgentUseCase(mock_agent_repo)

    @pytest.mark.asyncio
    async def test_create_agent_success(
        self,
        create_agent_use_case: CreateAgent,
        mock_agent_repo: Mock,
    ) -> None:
        """Test successful agent creation."""
        # Arrange
        agent_id = str(uuid4())
        name = "CodeAssistant"
        description = "AI assistant specialized in code generation and review"
        capabilities = ["coding"]

        Agent(
            id=UUID(agent_id),
            name=name,
            description=description,
            config=AgentConfig(capabilities=[AgentCapability.CODING]),
            version="1.0.0",
            created_at=datetime.now(UTC),
        )

        mock_agent_repo.create = AsyncMock(return_value=expected_agent)

        # Act
        _ = await create_agent_use_case(
            name=name,
            description=description,
            capabilities=capabilities,
            config_data={},
        )

        # Assert
        assert isinstance(result, Agent)
        assert result.name == name
        assert result.description == description
        assert AgentCapability.CODING in result.config.capabilities
        assert result.status == AgentStatus.INACTIVE
        mock_agent_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_deploy_agent_success(
        self,
        deploy_agent_use_case: DeployAgentUseCase,
        mock_agent_repo: Mock,
    ) -> None:
        """Test successful agent deployment."""
        # Arrange
        agent_id = UUID(str(uuid4()))
        deployment_config = {
            "instance_type": "gpu_optimized",
            "max_memory": "8GB",
            "timeout": 30,
            "auto_scale": True,
        }

        Agent(
            id=agent_id,
            name="TestAgent",
            description="Test agent for deployment",
            status=AgentStatus.INACTIVE,
            config=AgentConfig(),
        )

        mock_agent_repo.get_by_id = AsyncMock(return_value=original_agent)

        # Act
        result = await deploy_agent_use_case.execute(
            agent_id=agent_id,
            deployment_config=deployment_config,
        )

        # Assert
        assert isinstance(result, bool)
        assert result is True
        mock_agent_repo.get_by_id.assert_called_once_with(agent_id)


class TestUseCaseBusinessLogic:
    """Test use case business logic and validation."""

    def test_use_case_dependency_injection(self) -> None:
        """Test use cases accept repository dependencies correctly."""
        # Arrange
        mock_repo = Mock()

        # Act & Assert - Use cases should accept repository dependencies
        auth_use_case = AuthenticateUser(mock_repo)
        memory_use_case = StoreMemory(mock_repo)
        chat_use_case = SendMessageUseCase(mock_repo)
        plan_use_case = CreatePlan(mock_repo)
        create_agent_use_case = CreateAgent(mock_repo)

        assert auth_use_case.user_repo == mock_repo
        assert memory_use_case.memory_repo == mock_repo
        assert chat_use_case._chat_repository == mock_repo
        assert plan_use_case.plan_repo == mock_repo
        assert create_agent_use_case.agent_repo == mock_repo

    def test_use_case_method_signatures(self) -> None:
        """Test use cases have correct method signatures."""
        # Arrange
        mock_repo = Mock()

        # Act & Assert - Use cases should have callable interface
        auth_use_case = AuthenticateUser(mock_repo)
        memory_use_case = StoreMemory(mock_repo)
        plan_use_case = CreatePlan(mock_repo)

        # Check use cases are callable (have __call__ or execute methods)
        assert callable(auth_use_case)
        assert callable(memory_use_case)
        assert callable(plan_use_case)
        assert hasattr(SendMessageUseCase(mock_repo), "execute")

    @pytest.mark.asyncio
    async def test_use_case_error_propagation(self) -> None:
        """Test use cases properly propagate repository errors."""
        # Arrange
        mock_repo = Mock()
        mock_repo.create = AsyncMock(
            side_effect=Exception("Database connection failed")
        )

        memory_use_case = StoreMemory(mock_repo)

        # Act & Assert
        with pytest.raises(Exception, match="Database connection failed"):
            await memory_use_case(
                content="test content",
                memory_type="episodic",
                importance="medium",
                agent_id=uuid4(),
                context={},
            )
