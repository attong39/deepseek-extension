"""Test DTO pattern conversions.

Tests the Data Transfer Object pattern for converting between
SQLAlchemy models and domain entities.
"""

from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import uuid4

from apps.backend.data.dtos import AgentDTO, MemoryDTO, PlanDTO, UserDTO


class TestDTOConversions:
    """Test DTO conversion patterns."""

    def test_agent_dto_from_model(self):
        """Test AgentDTO.from_model conversion."""
        # Mock SQLAlchemy model
        model = Mock()
        model.id = uuid4()
        model.name = "Test Agent"
        model.agent_type = "assistant"
        model.capabilities = ["chat", "search"]
        model.status = "active"
        model.model_config = {"model": "gpt-4"}
        model.metadata = {"version": "1.0"}
        model.created_at = datetime.now(UTC)
        model.updated_at = datetime.now(UTC)

        # Convert using DTO
        dto = AgentDTO.from_model(model)

        # Verify conversion
        assert dto.id == model.id
        assert dto.name == model.name
        assert dto.agent_type == model.agent_type
        assert dto.capabilities == model.capabilities
        assert dto.status == model.status
        assert dto.model_config == model.model_config
        assert dto.metadata == model.metadata
        assert dto.created_at == model.created_at
        assert dto.updated_at == model.updated_at

    def test_user_dto_from_model(self):
        """Test UserDTO.from_model conversion."""
        model = Mock()
        model.id = uuid4()
        model.username = "testuser"
        model.email = "test@example.com"
        model.first_name = "Test"
        model.last_name = "User"
        model.display_name = "Test User"
        model.bio = "Test bio"
        model.avatar_url = "https://example.com/avatar.jpg"
        model.is_active = True
        model.is_verified = False
        model.preferences = {"theme": "dark"}
        model.metadata = {"source": "signup"}
        model.created_at = datetime.now(UTC)
        model.updated_at = datetime.now(UTC)
        model.last_login_at = None

        dto = UserDTO.from_model(model)

        assert dto.id == model.id
        assert dto.username == model.username
        assert dto.email == model.email
        assert dto.first_name == model.first_name
        assert dto.last_name == model.last_name
        assert dto.display_name == model.display_name
        assert dto.bio == model.bio
        assert dto.avatar_url == model.avatar_url
        assert dto.is_active == model.is_active
        assert dto.is_verified == model.is_verified
        assert dto.preferences == model.preferences
        assert dto.metadata == model.metadata

    def test_memory_dto_from_model(self):
        """Test MemoryDTO.from_model conversion."""
        model = Mock()
        model.id = uuid4()
        model.user_id = uuid4()
        model.agent_id = uuid4()
        model.content = "Test memory content"
        model.memory_type = "episodic"
        model.importance = 0.8
        model.context = {"source": "chat"}
        model.metadata = {"tags": ["important"]}
        model.embedding_vector = [0.1, 0.2, 0.3]
        model.access_count = 5
        model.last_accessed_at = datetime.now(UTC)
        model.expires_at = None
        model.created_at = datetime.now(UTC)
        model.updated_at = datetime.now(UTC)

        dto = MemoryDTO.from_model(model)

        assert dto.id == model.id
        assert dto.user_id == model.user_id
        assert dto.agent_id == model.agent_id
        assert dto.content == model.content
        assert dto.memory_type == model.memory_type
        assert dto.importance == model.importance
        assert dto.context == model.context
        assert dto.metadata == model.metadata
        assert dto.embedding_vector == model.embedding_vector
        assert dto.access_count == model.access_count
        assert dto.last_accessed_at == model.last_accessed_at
        assert dto.expires_at == model.expires_at

    def test_plan_dto_from_model(self):
        """Test PlanDTO.from_model conversion."""
        model = Mock()
        model.id = uuid4()
        model.user_id = uuid4()
        model.title = "Test Plan"
        model.description = "Test plan description"
        model.goal = "Complete the test"
        model.plan_type = "goal_oriented"
        model.status = "active"
        model.priority = 5
        model.context = {"domain": "testing"}
        model.constraints = {"time_limit": 3600}
        model.success_criteria = ["All tests pass"]
        model.estimated_duration = 120
        model.actual_duration = None
        model.progress_percentage = 25.0
        model.created_at = datetime.now(UTC)
        model.updated_at = datetime.now(UTC)
        model.completed_at = None

        dto = PlanDTO.from_model(model)

        assert dto.id == model.id
        assert dto.user_id == model.user_id
        assert dto.title == model.title
        assert dto.description == model.description
        assert dto.goal == model.goal
        assert dto.plan_type == model.plan_type
        assert dto.status == model.status
        assert dto.priority == model.priority
        assert dto.context == model.context
        assert dto.constraints == model.constraints
        assert dto.success_criteria == model.success_criteria
        assert dto.estimated_duration == model.estimated_duration
        assert dto.actual_duration == model.actual_duration
        assert dto.progress_percentage == model.progress_percentage

    def test_dto_handles_none_values(self):
        """Test DTO handles None values gracefully."""
        model = Mock()
        model.id = uuid4()
        model.name = "Test Agent"
        model.agent_type = None
        model.capabilities = None
        model.status = None
        model.model_config = None
        model.metadata = None
        model.created_at = datetime.now(UTC)
        model.updated_at = datetime.now(UTC)

        dto = AgentDTO.from_model(model)

        # Should have default values for None fields
        assert dto.agent_type == "assistant"
        assert dto.capabilities == []
        assert dto.status == "inactive"
        assert dto.model_config == {}
        assert dto.metadata == {}
