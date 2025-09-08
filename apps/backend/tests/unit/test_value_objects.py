"""
Unit tests for domain value objects.

Tests core value objects to ensure immutability, validation, and business logic.
"""

import pytest

from core.domain.value_objects.agent_config import AgentConfig
from core.domain.value_objects.conversation_context import ConversationContext
from core.domain.value_objects.file_metadata import FileMetadata
from core.domain.value_objects.memory_context import MemoryContext
from core.domain.value_objects.performance_metrics import PerformanceMetrics
from core.domain.value_objects.security_context import SecurityContext
from core.domain.value_objects.user_preferences import (
import ValueError
import abs
import bool
import isinstance
    Language,
    Theme,
    Timezone,
    UserPreferences,
)


class TestAgentConfig:
    """Test cases for AgentConfig value object."""

    def test_create_agent_config(self):
        """Test creating an agent configuration."""
        config = AgentConfig(model="gpt-4", temperature=0.7, max_tokens=1000, top_p=0.9)

        assert config.model == "gpt-4"
        assert abs(config.temperature - 0.7) < 0.001
        assert config.max_tokens == 1000
        assert abs(config.top_p - 0.9) < 0.001

    def test_agent_config_defaults(self):
        """Test agent config default values."""
        config = AgentConfig()

        assert config.model == "gpt-4o-mini"
        assert abs(config.temperature - 0.7) < 0.001
        assert config.max_tokens == 1024
        assert abs(config.top_p - 1.0) < 0.001

    def test_agent_config_validation(self):
        """Test agent config validation."""
        # Invalid temperature
        with pytest.raises(ValueError, match="temperature must be in"):
            AgentConfig(temperature=3.0)

        # Invalid top_p
        with pytest.raises(ValueError, match="top_p must be in"):
            AgentConfig(top_p=1.5)

        # Invalid max_tokens
        with pytest.raises(ValueError, match="max_tokens must be > 0"):
            AgentConfig(max_tokens=0)

        # Empty model
        with pytest.raises(ValueError, match="model must be non-empty"):
            AgentConfig(model="")


class TestConversationContext:
    """Test cases for ConversationContext value object."""

    def test_create_conversation_context(self):
        """Test creating a conversation context."""
        metadata = {"priority": "high", "department": "engineering"}
        context = ConversationContext(
            topic="Project planning discussion", metadata=metadata
        )

        assert context.topic == "Project planning discussion"
        assert context.metadata == metadata

    def test_has_topic(self):
        """Test checking if context has a topic."""
        context_with_topic = ConversationContext(topic="Planning")
        context_without_topic = ConversationContext(topic=None)
        context_empty_topic = ConversationContext(topic="")

        assert context_with_topic.has_topic() is True
        assert context_without_topic.has_topic() is False
        assert context_empty_topic.has_topic() is False

    def test_get_metadata(self):
        """Test getting metadata values."""
        metadata = {"priority": "high", "department": "engineering"}
        context = ConversationContext(metadata=metadata)

        assert context.get("priority") == "high"
        assert context.get("department") == "engineering"
        assert context.get("nonexistent") is None
        assert context.get("nonexistent", "default") == "default"


class TestFileMetadata:
    """Test cases for FileMetadata value object."""

    def test_create_file_metadata(self):
        """Test creating file metadata."""
        metadata = FileMetadata(
            name="document.pdf",
            size_bytes=1024000,
            mime_type="application/pdf",
            checksum="abc123def456789012345678901234567890abcd",
        )

        assert metadata.name == "document.pdf"
        assert metadata.size_bytes == 1024000
        assert metadata.mime_type == "application/pdf"
        assert metadata.checksum == "abc123def456789012345678901234567890abcd"

    def test_is_binary(self):
        """Test binary file detection."""
        text_file = FileMetadata(
            name="readme.txt", size_bytes=1000, mime_type="text/plain"
        )

        binary_file = FileMetadata(
            name="image.jpg", size_bytes=500000, mime_type="image/jpeg"
        )

        assert text_file.is_binary() is False
        assert binary_file.is_binary() is True

    def test_extension_property(self):
        """Test file extension property."""
        python_file = FileMetadata(
            name="script.PY", size_bytes=1000, mime_type="text/x-python"
        )

        no_extension = FileMetadata(
            name="README", size_bytes=500, mime_type="text/plain"
        )

        assert python_file.extension == "py"
        assert no_extension.extension == ""

    def test_file_metadata_validation(self):
        """Test file metadata validation."""
        # Empty name
        with pytest.raises(ValueError, match="name must be non-empty"):
            FileMetadata(name="", size_bytes=100, mime_type="text/plain")

        # Invalid mime type
        with pytest.raises(ValueError, match="mime_type must be a valid"):
            FileMetadata(name="test.txt", size_bytes=100, mime_type="invalid")

        # Negative size
        with pytest.raises(ValueError, match="size_bytes must be >= 0"):
            FileMetadata(name="test.txt", size_bytes=-1, mime_type="text/plain")


class TestMemoryContext:
    """Test cases for MemoryContext value object."""

    def test_create_memory_context(self):
        """Test creating a memory context."""
        metadata = {"source": "chat", "importance": "high"}
        context = MemoryContext(source="user_interaction", metadata=metadata)

        assert context.source == "user_interaction"
        assert context.metadata == metadata

    def test_has_metadata_key(self):
        """Test checking if metadata key exists."""
        metadata = {"source": "chat", "importance": "high"}
        context = MemoryContext(metadata=metadata)

        assert context.has("source") is True
        assert context.has("importance") is True
        assert context.has("nonexistent") is False

    def test_get_metadata_value(self):
        """Test getting metadata values."""
        metadata = {"source": "chat", "importance": "high"}
        context = MemoryContext(metadata=metadata)

        assert context.get("source") == "chat"
        assert context.get("importance") == "high"
        assert context.get("nonexistent") is None
        assert context.get("nonexistent", "default") == "default"


class TestPerformanceMetrics:
    """Test cases for PerformanceMetrics value object."""

    def test_create_performance_metrics(self):
        """Test creating performance metrics."""
        metrics = PerformanceMetrics(
            latency_ms=150.5, throughput_rps=256.7, error_rate=0.02
        )

        assert abs(metrics.latency_ms - 150.5) < 0.001
        assert abs(metrics.throughput_rps - 256.7) < 0.001
        assert abs(metrics.error_rate - 0.02) < 0.001

    def test_performance_metrics_defaults(self):
        """Test default performance metrics."""
        metrics = PerformanceMetrics()

        assert abs(metrics.latency_ms - 0.0) < 0.001
        assert abs(metrics.throughput_rps - 0.0) < 0.001
        assert abs(metrics.error_rate - 0.0) < 0.001

    def test_performance_metrics_validation(self):
        """Test performance metrics validation."""
        # Negative latency
        with pytest.raises(ValueError, match="latency_ms must be >= 0"):
            PerformanceMetrics(latency_ms=-1.0)

        # Negative throughput
        with pytest.raises(ValueError, match="throughput_rps must be >= 0"):
            PerformanceMetrics(throughput_rps=-1.0)

        # Invalid error rate
        with pytest.raises(ValueError, match="error_rate must be in"):
            PerformanceMetrics(error_rate=1.5)

    def test_with_new_latency(self):
        """Test creating metrics with new latency."""
        original = PerformanceMetrics(
            latency_ms=100.0, throughput_rps=50.0, error_rate=0.01
        )
        updated = original.with_new_latency(200.0)

        assert abs(updated.latency_ms - 200.0) < 0.001
        assert abs(updated.throughput_rps - 50.0) < 0.001
        assert abs(updated.error_rate - 0.01) < 0.001

        # Original should be unchanged
        assert abs(original.latency_ms - 100.0) < 0.001

    def test_to_dict(self):
        """Test serialization to dict."""
        metrics = PerformanceMetrics(
            latency_ms=100.0, throughput_rps=50.0, error_rate=0.01
        )
        result = metrics.to_dict()

        expected = {"latency_ms": 100.0, "throughput_rps": 50.0, "error_rate": 0.01}

        assert result == expected


class TestSecurityContext:
    """Test cases for SecurityContext value object."""

    def test_create_security_context(self):
        """Test creating a security context."""
        scopes = ("read", "write", "admin")
        attributes = {"ip": "192.168.1.1", "user_agent": "browser"}

        context = SecurityContext(
            user_id="user123", scopes=scopes, attributes=attributes
        )

        assert context.user_id == "user123"
        assert context.scopes == scopes
        assert context.attributes == attributes

    def test_has_scope(self):
        """Test checking if context has specific scope."""
        context = SecurityContext(user_id="user123", scopes=("read", "write"))

        assert context.has_scope("read") is True
        assert context.has_scope("write") is True
        assert context.has_scope("admin") is False

    def test_get_attribute(self):
        """Test getting security attributes."""
        attributes = {"ip": "192.168.1.1", "user_agent": "browser"}
        context = SecurityContext(attributes=attributes)

        assert context.get("ip") == "192.168.1.1"
        assert context.get("user_agent") == "browser"
        assert context.get("nonexistent") is None
        assert context.get("nonexistent", "default") == "default"

    def test_empty_scopes_validation(self):
        """Test validation of empty scopes."""
        with pytest.raises(ValueError, match="scopes must not contain empty strings"):
            SecurityContext(scopes=("read", "", "write"))


class TestUserPreferences:
    """Test cases for UserPreferences value object."""

    def test_create_user_preferences(self):
        """Test creating user preferences."""
        prefs = UserPreferences(
            language=Language.ENGLISH,
            timezone=Timezone.UTC,
            date_format="MM/DD/YYYY",
            time_format="12h",
        )

        assert prefs.language == Language.ENGLISH
        assert prefs.timezone == Timezone.UTC
        assert prefs.date_format == "MM/DD/YYYY"
        assert prefs.time_format == "12h"

    def test_default_preferences(self):
        """Test default user preferences."""
        prefs = UserPreferences()

        assert prefs.language == Language.VIETNAMESE
        assert prefs.timezone == Timezone.ASIA_HO_CHI_MINH
        assert prefs.date_format == "DD/MM/YYYY"
        assert prefs.time_format == "24h"

    def test_custom_settings(self):
        """Test custom settings management."""
        prefs = UserPreferences()

        # Set custom setting
        prefs.set_custom_setting("theme_color", "blue")
        assert prefs.get_custom_setting("theme_color") == "blue"

        # Get non-existent setting with default
        assert prefs.get_custom_setting("nonexistent", "default") == "default"

        # Remove custom setting
        prefs.remove_custom_setting("theme_color")
        assert prefs.get_custom_setting("theme_color") is None

    def test_effective_theme(self):
        """Test effective theme calculation."""
        prefs = UserPreferences()

        # Manual theme
        prefs.ui.theme = Theme.DARK
        assert prefs.get_effective_theme() == Theme.DARK

        # Auto theme (defaults to light)
        prefs.ui.theme = Theme.AUTO
        assert prefs.get_effective_theme() == "light"

    def test_locale_string(self):
        """Test locale string generation."""
        prefs = UserPreferences(language=Language.ENGLISH, timezone=Timezone.US_PACIFIC)

        locale = prefs.get_locale_string()
        assert locale == "en_Pacific"


class TestValueObjectEnums:
    """Test cases for value object enumerations."""

    def test_theme_enum(self):
        """Test Theme enumeration."""
        assert Theme.LIGHT.value == "light"
        assert Theme.DARK.value == "dark"
        assert Theme.AUTO.value == "auto"

    def test_language_enum(self):
        """Test Language enumeration."""
        assert Language.VIETNAMESE.value == "vi"
        assert Language.ENGLISH.value == "en"
        assert Language.CHINESE.value == "zh"
        assert Language.JAPANESE.value == "ja"
        assert Language.KOREAN.value == "ko"

    def test_timezone_enum(self):
        """Test Timezone enumeration."""
        assert Timezone.ASIA_HO_CHI_MINH.value == "Asia/Ho_Chi_Minh"
        assert Timezone.UTC.value == "UTC"
        assert Timezone.US_PACIFIC.value == "US/Pacific"


class TestValueObjectBusinessLogic:
    """Test cases for value object business logic and validation."""

    def test_security_context_validation(self):
        """Test security context validation logic."""
        # Valid context
        context = SecurityContext(
            user_id="user123",
            scopes=("read", "write", "admin"),
            attributes={"role": "admin"},
        )

        assert context.has_scope("admin") is True
        assert context.get("role") == "admin"

    def test_file_metadata_validation(self):
        """Test file metadata validation and helpers."""
        # Text file
        text_metadata = FileMetadata(
            name="script.py", size_bytes=5000, mime_type="text/x-python"
        )

        assert text_metadata.is_binary() is False

        # Binary file
        binary_metadata = FileMetadata(
            name="archive.zip", size_bytes=1000000, mime_type="application/zip"
        )

        assert binary_metadata.is_binary() is True

    def test_conversation_context_topic_validation(self):
        """Test conversation context topic validation."""
        # Valid topic
        valid_context = ConversationContext(topic="Project planning")
        assert valid_context.has_topic() is True

        # Empty topic
        empty_context = ConversationContext(topic="   ")
        assert empty_context.has_topic() is False

        # None topic
        none_context = ConversationContext(topic=None)
        assert none_context.has_topic() is False

    def test_memory_context_metadata_access(self):
        """Test memory context metadata access patterns."""
        metadata = {"importance": "high", "category": "task", "tags": "planning,work"}

        context = MemoryContext(source="user_input", metadata=metadata)

        # Check metadata access
        assert context.has("importance") is True
        assert context.has("nonexistent") is False
        assert context.get("category") == "task"
        assert context.get("tags") == "planning,work"
        assert context.get("missing", "default") == "default"

    def test_performance_metrics_realistic_values(self):
        """Test performance metrics with realistic values."""
        metrics = PerformanceMetrics(
            latency_ms=125.7, throughput_rps=512.3, error_rate=0.238
        )

        # Verify realistic ranges
        assert 0 < metrics.latency_ms < 10000  # Reasonable response time
        assert 0 < metrics.throughput_rps < 16384  # Reasonable throughput
        assert 0 <= metrics.error_rate <= 1.0  # Valid error rate

    def test_user_preferences_notification_check(self):
        """Test user preferences notification checking."""
        prefs = UserPreferences()

        # Test notification checking (without modifying internal structure)
        result = prefs.is_notification_enabled("system_alerts")
        assert isinstance(result, bool)  # Should return a boolean

        # Test non-existent notification type
        result = prefs.is_notification_enabled("nonexistent")
        assert result is False
