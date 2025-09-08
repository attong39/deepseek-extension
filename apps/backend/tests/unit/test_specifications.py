import os
import active_agent
import admin_user
import all
import bad_agent
import created_at
import empty_agent
import good_agent
import hasattr
import heavy_user
import i
import inactive_agent
import inactive_session
import is_active
import limit_user
import limited_user
import long_agent
import normal_user
import old_session
import permissions
import range
import read_user
import recent_session
import request_count
import reserved_agent
import self
import short_agent
import valid_agent

"""
Unit tests for domain specifications.

Tests all domain specifications to ensure proper business rule validation.
"""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from core.domain.entities.agent import Agent
from core.domain.entities.memory import Memory, MemoryType
from core.domain.specifications.agent_specifications import (
    AgentCapabilitySpecification,
    AgentNameSpecification,
    AgentStatusSpecification,
    AgentTypeSpecification,
)
from core.domain.specifications.memory_specifications import (
    MemoryContentSpecification,
    MemoryExpirationSpecification,
    MemoryRelevanceSpecification,
    MemoryTypeSpecification,
)
from core.domain.specifications.security_specifications import (
    PasswordStrengthSpecification,
    PermissionSpecification,
    RateLimitSpecification,
    SessionValiditySpecification,
)


class TestAgentSpecifications:
    """Test cases for agent domain specifications."""

    def test_agent_name_specification_valid(self):
        """Test agent name specification with valid names."""
        spec = AgentNameSpecification()

        # Valid names
        Agent(name="ValidAgent", description="Test")
        assert spec.is_satisfied_by(valid_agent) is True

        # Valid with spaces and numbers
        valid_agent2 = Agent(name="Agent 123", description="Test")
        assert spec.is_satisfied_by(valid_agent2) is True

        # Direct string validation
        assert spec.is_satisfied_by("GoodAgentName") is True

    def test_agent_name_specification_invalid(self):
        """Test agent name specification with invalid names."""
        spec = AgentNameSpecification()

        # Too short
        Agent(name="A", description="Test")
        assert spec.is_satisfied_by(short_agent) is False

        # Too long (default max is 50)
        long_name = "A" * 60
        Agent(name=long_name, description="Test")
        assert spec.is_satisfied_by(long_agent) is False

        # Empty name
        Agent(name="", description="Test")
        assert spec.is_satisfied_by(empty_agent) is False

        # Reserved name
        Agent(name="admin", description="Test")
        assert spec.is_satisfied_by(reserved_agent) is False

    def test_agent_capability_specification(self):
        """Test agent capability specification."""
        spec = AgentCapabilitySpecification()

        # Test with capabilities list directly since Agent entity may not have capabilities field
        assert spec.is_satisfied_by(["conversation", "text_generation"]) is True

        # Invalid capabilities
        assert spec.is_satisfied_by(["invalid_capability"]) is False

    def test_agent_status_specification(self):
        """Test agent status specification."""
        spec = AgentStatusSpecification()

        # Active agent
        Agent(name="ActiveAgent", description="Test")
        active_agent.activate()
        assert spec.is_satisfied_by(active_agent) is True

        # Inactive agent
        Agent(name="InactiveAgent", description="Test")
        assert spec.is_satisfied_by(inactive_agent) is True  # inactive is valid status

        # Direct status validation
        assert spec.is_satisfied_by("active") is True
        assert spec.is_satisfied_by("invalid_status") is False

    def test_agent_type_specification(self):
        """Test agent type specification."""
        spec = AgentTypeSpecification(["conversational", "task_automation"])

        # Valid type
        assert spec.is_satisfied_by("conversational") is True
        assert spec.is_satisfied_by("task_automation") is True

        # Invalid type
        assert spec.is_satisfied_by("invalid_type") is False


class TestMemorySpecifications:
    """Test cases for memory domain specifications."""

    def test_memory_content_specification_valid(self):
        """Test memory content specification with valid content."""
        spec = MemoryContentSpecification(min_length=10, max_length=1000)

        # Valid content
        valid_memory = Memory(
            content="This is a valid memory content that meets the requirements",
            type=MemoryType.EPISODIC,
            user_id=uuid4(),
        )
        assert spec.is_satisfied_by(valid_memory) is True

        # Direct string validation
        assert spec.is_satisfied_by("Valid content here") is True

    def test_memory_content_specification_invalid(self):
        """Test memory content specification with invalid content."""
        spec = MemoryContentSpecification(min_length=10, max_length=50)

        # Too short
        short_memory = Memory(
            content="Short", type=MemoryType.EPISODIC, user_id=uuid4()
        )
        assert spec.is_satisfied_by(short_memory) is False

        # Too long
        long_content = "A" * 100
        long_memory = Memory(
            content=long_content, type=MemoryType.EPISODIC, user_id=uuid4()
        )
        assert spec.is_satisfied_by(long_memory) is False

        # Direct string validation
        assert spec.is_satisfied_by("Too short") is False
        assert spec.is_satisfied_by("") is False

    def test_memory_type_specification(self):
        """Test memory type specification."""
        episodic_types = ["episodic"]
        episodic_spec = MemoryTypeSpecification(episodic_types)

        # Correct type
        episodic_memory = Memory(
            content="User had a conversation about weather",
            type=MemoryType.EPISODIC,
            user_id=uuid4(),
        )

        # Check if memory has memory_type attribute, otherwise use type
        if hasattr(episodic_memory, "memory_type"):
            episodic_memory.memory_type = "episodic"
            assert episodic_spec.is_satisfied_by(episodic_memory) is True
        else:
            # Direct type validation
            assert episodic_spec.is_satisfied_by("episodic") is True
            assert episodic_spec.is_satisfied_by("semantic") is False

    def test_memory_relevance_specification(self):
        """Test memory relevance specification."""
        spec = MemoryRelevanceSpecification(min_score=0.0, max_score=1.0)

        # Valid relevance scores
        assert spec.is_satisfied_by(0.5) is True
        assert spec.is_satisfied_by(0.0) is True
        assert spec.is_satisfied_by(1.0) is True

        # Invalid relevance scores
        assert spec.is_satisfied_by(-0.1) is False
        assert spec.is_satisfied_by(1.1) is False
        assert spec.is_satisfied_by("not_a_number") is False

    def test_memory_expiration_specification(self):
        """Test memory expiration specification."""
        spec = MemoryExpirationSpecification(allow_permanent=True)

        # Fresh memory
        fresh_memory = Memory(
            content="Recent memory", type=MemoryType.EPISODIC, user_id=uuid4()
        )

        # Test assumes memory is valid by default
        assert spec.is_satisfied_by(fresh_memory) is True

        # Test with permanent memory allowed - specification handles the logic internally


class TestSecuritySpecifications:
    """Test cases for security domain specifications."""

    def test_password_strength_specification_valid(self):
        """Test password strength specification with strong passwords."""
        spec = PasswordStrengthSpecification()

        # Strong passwords
        assert spec.is_satisfied_by("StrongPass123!") is True
        assert spec.is_satisfied_by("MySecure@Password2024") is True
        assert spec.is_satisfied_by("Complex!Pass1") is True

    def test_password_strength_specification_invalid(self):
        """Test password strength specification with weak passwords."""
        spec = PasswordStrengthSpecification()

        # Weak passwords
        assert spec.is_satisfied_by("weak") is False
        assert spec.is_satisfied_by("password") is False
        assert spec.is_satisfied_by("12345678") is False
        assert spec.is_satisfied_by("NoNumbers!") is False
        assert spec.is_satisfied_by("nonumbers123") is False
        assert spec.is_satisfied_by("ONLYUPPERCASE123!") is False

    def test_permission_specification(self):
        """Test permission specification."""
        read_spec = PermissionSpecification(["read"])

        # Mock user with permissions
        class MockUser:
            def __init__(self, permissions):
                self.permissions = permissions

        # User with read permission
        MockUser(["read", "write"])
        assert read_spec.is_satisfied_by(read_user) is True

        # User without read permission
        MockUser(["write"])
        assert read_spec.is_satisfied_by(limited_user) is False

        # Admin user with all permissions
        MockUser(["read", "write", "admin", "delete"])
        assert read_spec.is_satisfied_by(admin_user) is True

    def test_rate_limit_specification(self):
        """Test rate limit specification."""
        spec = RateLimitSpecification(max_requests=100, time_window=timedelta(hours=1))

        # Mock user with request history
        class MockUser:
            def __init__(self, request_count):
                now = datetime.now(UTC)
                # Create request history within the time window
                self.request_history = [
                    now - timedelta(minutes=i * 5) for i in range(request_count)
                ]

        # User within limit
        MockUser(50)
        assert spec.is_satisfied_by(normal_user) is True

        # User at limit
        MockUser(100)
        assert spec.is_satisfied_by(limit_user) is True

        # User exceeding limit
        MockUser(150)
        assert spec.is_satisfied_by(heavy_user) is False

    def test_session_validity_specification(self):
        """Test session validity specification."""
        spec = SessionValiditySpecification(max_session_age=timedelta(hours=24))

        # Mock session class
        class MockSession:
            def __init__(self, created_at, is_active=True):
                self.created_at = created_at
                self.is_active = is_active

        # Fresh session
        MockSession(created_at=datetime.now(UTC), is_active=True)
        assert spec.is_satisfied_by(recent_session) is True

        # Old session
        MockSession(created_at=datetime.now(UTC) - timedelta(hours=25), is_active=True)
        assert spec.is_satisfied_by(old_session) is False

        # Inactive session
        MockSession(created_at=datetime.now(UTC), is_active=False)
        assert spec.is_satisfied_by(inactive_session) is False


class TestSpecificationComposition:
    """Test cases for specification composition and complex rules."""

    def test_agent_specification_and_combination(self):
        """Test combining agent specifications with AND logic."""
        name_spec = AgentNameSpecification()
        status_spec = AgentStatusSpecification()

        # Agent that satisfies all specifications
        Agent(name="GoodAgent", description="Test")
        good_agent.activate()

        assert name_spec.is_satisfied_by(good_agent) is True
        assert status_spec.is_satisfied_by(good_agent) is True

        # Agent that fails one specification
        Agent(name="A", description="Test")  # Bad name (too short)
        bad_agent.activate()

        assert name_spec.is_satisfied_by(bad_agent) is False
        assert status_spec.is_satisfied_by(bad_agent) is True

    def test_memory_specification_or_combination(self):
        """Test combining memory specifications with OR logic."""
        episodic_spec = MemoryTypeSpecification(["episodic"])
        semantic_spec = MemoryTypeSpecification(["semantic"])

        # Test direct type validation since memory type interface varies
        assert episodic_spec.is_satisfied_by("episodic") is True
        assert episodic_spec.is_satisfied_by("semantic") is False

        assert semantic_spec.is_satisfied_by("semantic") is True
        assert semantic_spec.is_satisfied_by("episodic") is False

    def test_security_specification_complex_rules(self):
        """Test complex security specification combinations."""
        password_spec = PasswordStrengthSpecification()
        permission_spec = PermissionSpecification(["admin"])
        rate_limit_spec = RateLimitSpecification(
            max_requests=1000, time_window=timedelta(hours=1)
        )

        # Strong authentication requirements
        strong_password = os.getenv("PASSWORD")

        class MockAdminUser:
            def __init__(self):
                self.permissions = ["read", "write", "admin"]
                # Light usage
                now = datetime.now(UTC)
                self.request_history = [
                    now - timedelta(minutes=i * 10) for i in range(50)
                ]

        MockAdminUser()

        assert password_spec.is_satisfied_by(strong_password) is True
        assert permission_spec.is_satisfied_by(admin_user) is True
        assert rate_limit_spec.is_satisfied_by(admin_user) is True

        # Failed authentication
        weak_password = os.getenv("PASSWORD")

        class MockLimitedUser:
            def __init__(self):
                self.permissions = ["read"]
                # Heavy usage
                now = datetime.now(UTC)
                self.request_history = [now - timedelta(minutes=i) for i in range(1500)]

        MockLimitedUser()

        assert password_spec.is_satisfied_by(weak_password) is False
        assert permission_spec.is_satisfied_by(limited_user) is False
        assert rate_limit_spec.is_satisfied_by(limited_user) is False


class TestSpecificationBusinessRules:
    """Test cases for business rule validation through specifications."""

    def test_agent_deployment_readiness(self):
        """Test business rule: Agent must meet criteria for deployment."""
        name_spec = AgentNameSpecification()
        status_spec = AgentStatusSpecification()

        # Ready for deployment
        deployment_ready = Agent(name="DeploymentAgent", description="Ready for prod")
        deployment_ready.activate()

        # Check all deployment criteria
        deployment_criteria = [
            name_spec.is_satisfied_by(deployment_ready),
            status_spec.is_satisfied_by(deployment_ready),
        ]

        assert all(deployment_criteria) is True

        # Not ready for deployment
        not_ready = Agent(name="N", description="Not ready")  # Bad name

        deployment_criteria_bad = [
            name_spec.is_satisfied_by(not_ready),
            status_spec.is_satisfied_by(not_ready),
        ]

        assert all(deployment_criteria_bad) is False

    def test_memory_archival_eligibility(self):
        """Test business rule: Memory archival based on type and content."""
        content_spec = MemoryContentSpecification(min_length=20, max_length=10000)
        type_spec = MemoryTypeSpecification(["semantic"])

        # Eligible for archival
        archival_content = "This is important semantic information that should be archived for long-term storage"

        assert content_spec.is_satisfied_by(archival_content) is True
        assert type_spec.is_satisfied_by("semantic") is True

        # Not eligible - wrong type
        episodic_content = (
            "User clicked on the save button at 3:45 PM during the meeting session"
        )

        assert content_spec.is_satisfied_by(episodic_content) is True
        assert type_spec.is_satisfied_by("episodic") is False

    def test_security_access_control(self):
        """Test business rule: Multi-layer security validation."""
        password_spec = PasswordStrengthSpecification()
        admin_permission = PermissionSpecification(["admin"])
        rate_limit_spec = RateLimitSpecification(
            max_requests=100, time_window=timedelta(hours=1)
        )

        # Valid admin access
        secure_password = os.getenv("PASSWORD")

        class MockSecureAdmin:
            def __init__(self):
                self.permissions = ["read", "write", "admin", "delete"]
                now = datetime.now(UTC)
                self.request_history = [
                    now - timedelta(minutes=i * 5) for i in range(25)
                ]

        secure_admin = MockSecureAdmin()

        # All security layers pass
        security_checks = [
            password_spec.is_satisfied_by(secure_password),
            admin_permission.is_satisfied_by(secure_admin),
            rate_limit_spec.is_satisfied_by(secure_admin),
        ]

        assert all(security_checks) is True

        # Blocked access - rate limited
        class MockRateLimitedAdmin:
            def __init__(self):
                self.permissions = ["read", "write", "admin"]
                now = datetime.now(UTC)
                self.request_history = [now - timedelta(minutes=i) for i in range(150)]

        rate_limited_admin = MockRateLimitedAdmin()

        security_checks_blocked = [
            password_spec.is_satisfied_by(secure_password),
            admin_permission.is_satisfied_by(rate_limited_admin),
            rate_limit_spec.is_satisfied_by(rate_limited_admin),  # This should fail
        ]

        assert all(security_checks_blocked) is False

        # Individual checks
        assert security_checks_blocked[0] is True  # Password OK
        assert security_checks_blocked[1] is True  # Permissions OK
        assert security_checks_blocked[2] is False  # Rate limit exceeded
