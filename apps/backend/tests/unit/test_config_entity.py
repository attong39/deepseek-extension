"""
Tests for ConfigItem domain entity.

Tests cover DDD compliance, business rules, domain events, and edge cases.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from core.domain.entities.config import ConfigItem, ConfigNamespace
import ValueError
import abs
import isinstance
import len
import namespace
import str


class TestConfigItem:
    """Test cases for ConfigItem entity."""

    def test_create_basic_config(self) -> None:
        """Test basic config item creation."""
        config = ConfigItem(
            namespace=ConfigNamespace.SYSTEM,
            key="database_url",
            value="postgresql://localhost:5432/zeta",
            description="Main database connection URL",
        )

        assert isinstance(config.id, UUID)
        assert config.namespace == ConfigNamespace.SYSTEM
        assert config.key == "database_url"
        assert config.value == "postgresql://localhost:5432/zeta"
        assert config.description == "Main database connection URL"
        assert not config.is_secret
        assert config.is_editable
        assert config.version == 1
        assert config.created_at is not None
        assert config.updated_at is not None
        assert len(config._events) == 1
        assert config._events[0]["type"] == "config.created"

    def test_create_secret_config(self) -> None:
        """Test creating secret configuration."""
        config = ConfigItem(
            namespace=ConfigNamespace.SECURITY,
            key="jwt_secret",
            value="super-secret-key-123",
            is_secret=True,
            is_editable=False,
        )

        assert config.is_secret
        assert not config.is_editable
        assert config.get_safe_value() == "[SECRET]"

    def test_validation_errors(self) -> None:
        """Test validation errors during creation."""
        # Empty key
        with pytest.raises(ValueError, match="Key must be at least 2 characters"):
            ConfigItem(
                namespace=ConfigNamespace.SYSTEM,
                key="",
                value="test",
            )

        # Too short key
        with pytest.raises(ValueError, match="Key must be at least 2 characters"):
            ConfigItem(
                namespace=ConfigNamespace.SYSTEM,
                key="x",
                value="test",
            )

        # Too long key
        with pytest.raises(ValueError, match="Key must be less than 100 characters"):
            ConfigItem(
                namespace=ConfigNamespace.SYSTEM,
                key="x" * 101,
                value="test",
            )

    def test_update_value(self) -> None:
        """Test updating configuration value."""
        config = ConfigItem(
            namespace=ConfigNamespace.AGENT,
            key="max_tokens",
            value=1000,
        )

        initial_version = config.version
        initial_updated_at = config.updated_at

        # Update value
        config.update_value(2000, "Increased for better performance")

        assert config.value == 2000
        assert config.description == "Increased for better performance"
        assert config.version == initial_version + 1
        assert config.updated_at > initial_updated_at
        assert len(config._events) == 2
        assert config._events[1]["type"] == "config.updated"
        assert config._events[1]["data"]["old_value"] == 1000
        assert config._events[1]["data"]["new_value"] == 2000

    def test_update_non_editable_fails(self) -> None:
        """Test updating non-editable config raises error."""
        config = ConfigItem(
            namespace=ConfigNamespace.SYSTEM,
            key="readonly_setting",
            value="fixed_value",
            is_editable=False,
        )

        with pytest.raises(ValueError, match="Configuration is not editable"):
            config.update_value("new_value")

    def test_update_secret_value_no_leak(self) -> None:
        """Test updating secret value doesn't leak in events."""
        config = ConfigItem(
            namespace=ConfigNamespace.SECURITY,
            key="api_key",
            value="old-secret",
            is_secret=True,
        )

        config.update_value("new-secret")

        # Event should not contain actual values
        update_event = config._events[1]
        assert "old_value" not in update_event["data"]
        assert "new_value" not in update_event["data"]
        assert update_event["data"]["is_secret"] is True

    def test_mark_as_secret(self) -> None:
        """Test marking configuration as secret."""
        config = ConfigItem(
            namespace=ConfigNamespace.API,
            key="external_token",
            value="public-token-123",
        )

        assert not config.is_secret
        assert config.get_safe_value() == "public-token-123"

        config.mark_as_secret()

        assert config.is_secret
        assert config.get_safe_value() == "[SECRET]"
        assert len(config._events) == 2
        assert config._events[1]["type"] == "config.updated"
        assert config._events[1]["data"]["field"] == "is_secret"

    def test_make_read_only(self) -> None:
        """Test making configuration read-only."""
        config = ConfigItem(
            namespace=ConfigNamespace.PERFORMANCE,
            key="cache_ttl",
            value=3600,
        )

        assert config.is_editable

        config.make_read_only()

        assert not config.is_editable
        assert len(config._events) == 2
        assert config._events[1]["type"] == "config.updated"
        assert config._events[1]["data"]["field"] == "is_editable"

        # Should not be able to update anymore
        with pytest.raises(ValueError, match="Configuration is not editable"):
            config.update_value(7200)

    def test_to_dict_without_secrets(self) -> None:
        """Test dictionary representation without secrets."""
        config = ConfigItem(
            namespace=ConfigNamespace.CHAT,
            key="welcome_message",
            value="Hello! How can I help you?",
            description="Default welcome message",
        )

        config_dict = config.to_dict()

        assert config_dict["namespace"] == "chat"
        assert config_dict["key"] == "welcome_message"
        assert config_dict["value"] == "Hello! How can I help you?"
        assert config_dict["description"] == "Default welcome message"
        assert not config_dict["is_secret"]

    def test_to_dict_with_secrets(self) -> None:
        """Test dictionary representation with secret values."""
        config = ConfigItem(
            namespace=ConfigNamespace.SECURITY,
            key="encryption_key",
            value="very-secret-key",
            is_secret=True,
        )

        # Without including secrets
        config_dict = config.to_dict(include_secret=False)
        assert config_dict["value"] == "[SECRET]"

        # With including secrets
        config_dict = config.to_dict(include_secret=True)
        assert config_dict["value"] == "very-secret-key"

    def test_query_methods(self) -> None:
        """Test query methods for config categorization."""
        system_config = ConfigItem(
            namespace=ConfigNamespace.SYSTEM,
            key="log_level",
            value="INFO",
        )

        agent_config = ConfigItem(
            namespace=ConfigNamespace.AGENT,
            key="model_name",
            value="gpt-4",
        )

        api_config = ConfigItem(
            namespace=ConfigNamespace.API,
            key="rate_limit",
            value=100,
        )

        # System config
        assert system_config.is_system_config()
        assert not system_config.is_domain_config()

        # Domain config
        assert not agent_config.is_system_config()
        assert agent_config.is_domain_config()

        # API config (not domain)
        assert not api_config.is_system_config()
        assert not api_config.is_domain_config()

    def test_get_full_key(self) -> None:
        """Test full namespaced key generation."""
        config = ConfigItem(
            namespace=ConfigNamespace.MEMORY,
            key="max_entries",
            value=1000,
        )

        assert config.get_full_key() == "memory.max_entries"

    def test_different_namespaces(self) -> None:
        """Test all available configuration namespaces."""
        namespaces = [
            ConfigNamespace.SYSTEM,
            ConfigNamespace.AGENT,
            ConfigNamespace.USER,
            ConfigNamespace.CHAT,
            ConfigNamespace.MEMORY,
            ConfigNamespace.API,
            ConfigNamespace.SECURITY,
            ConfigNamespace.PERFORMANCE,
        ]

        for namespace in namespaces:
            config = ConfigItem(
                namespace=namespace,
                key="test_key",
                value="test_value",
            )
            assert config.namespace == namespace
            assert config.get_full_key() == f"{namespace.value}.test_key"

    def test_domain_events_structure(self) -> None:
        """Test domain events have correct structure."""
        config = ConfigItem(
            namespace=ConfigNamespace.AGENT,
            key="temperature",
            value=0.7,
        )

        # Creation event
        create_event = config._events[0]
        assert create_event["type"] == "config.created"
        assert create_event["entity_type"] == "config"
        assert create_event["entity_id"] == str(config.id)
        assert "timestamp" in create_event
        assert create_event["data"]["namespace"] == "agent"
        assert create_event["data"]["key"] == "temperature"
        assert create_event["data"]["version"] == 1

        # Update event
        config.update_value(0.8)
        update_event = config._events[1]
        assert update_event["type"] == "config.updated"
        assert update_event["entity_type"] == "config"
        assert update_event["entity_id"] == str(config.id)
        assert update_event["data"]["version"] == 2
        assert abs(update_event["data"]["old_value"] - 0.7) < 0.001
        assert abs(update_event["data"]["new_value"] - 0.8) < 0.001
