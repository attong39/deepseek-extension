"""Tests for User domain entity.

Tests the User entity's DDD compliance, invariants, and business logic.
"""

import pytest

from core.domain.entities.user import User, UserStatus
from core.domain.value_objects.permissions import (
import ValueError
import e
import isinstance
import len
import list
    UserQuota,
    ZetaAIPermission,
    ZetaAIRole,
)
from core.domain.value_objects.user_preferences import UserPreferences


class TestUserEntity:
    """Test cases for User entity."""

    def test_user_creation_with_defaults(self) -> None:
        """Test user creation with default values."""
        user = User()

        assert user.id is not None
        assert user.email == ""
        assert user.username == ""
        assert user.display_name == ""
        assert user.roles == {ZetaAIRole.USER}
        assert user.status == UserStatus.PENDING_VERIFICATION
        assert user.login_count == 0
        assert user.session_count == 0
        assert isinstance(user.quota, UserQuota)
        assert isinstance(user.preferences, UserPreferences)

    def test_user_create_factory_method(self) -> None:
        """Test User.create factory method."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            display_name="Test User",
            full_name="Test Full Name",
            test_meta="test_value",
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert user.display_name == "Test User"
        assert user.full_name == "Test Full Name"
        assert user.metadata["test_meta"] == "test_value"

        # Check events
        events = user.get_events()
        assert len(events) == 1
        assert events[0].event_type == "user.created"
        assert events[0].event_data["username"] == "testuser"
        assert events[0].event_data["email"] == "test@example.com"

    def test_user_validation(self) -> None:
        """Test user validation logic."""
        # Valid cases should not raise
        User.validate("validuser", "test@example.com", "password_hash")

        # Invalid username
        with pytest.raises(ValueError, match="Username must be at least 3 characters"):
            User.validate("ab", "test@example.com", "password_hash")

        with pytest.raises(
            ValueError, match="Username must be less than 50 characters"
        ):
            User.validate("a" * 51, "test@example.com", "password_hash")

        # Invalid email
        with pytest.raises(ValueError, match="Valid email is required"):
            User.validate("validuser", "invalid_email", "password_hash")

        with pytest.raises(ValueError, match="Valid email is required"):
            User.validate("validuser", "", "password_hash")

        # Invalid password hash
        with pytest.raises(ValueError, match="Password hash is required"):
            User.validate("validuser", "test@example.com", "")

    def test_user_post_init_validation(self) -> None:
        """Test post-initialization validation."""
        # Should validate if username and email are provided
        with pytest.raises(ValueError):
            User(username="ab", email="test@example.com", password_hash="hash")

    def test_user_role_management(self) -> None:
        """Test user role granting and revoking."""
        user = User.create("testuser", "test@example.com", "hash")

        # Initially has USER role
        assert user.has_role(ZetaAIRole.USER)
        assert user.can(ZetaAIPermission.CHAT_CREATE)

        # Grant PREMIUM role
        user.grant_role(ZetaAIRole.PREMIUM)
        assert user.has_role(ZetaAIRole.PREMIUM)
        assert user.can(ZetaAIPermission.AGENT_CREATE)

        # Check events
        events = user.get_events()
        creation_events = [e for e in events if e.event_type == "user.role_granted"]
        assert len(creation_events) == 1
        assert creation_events[0].event_data["role"] == ZetaAIRole.PREMIUM

        # Revoke USER role (should fail - can't revoke last USER role)
        user.revoke_role(ZetaAIRole.PREMIUM)  # First remove premium
        with pytest.raises(ValueError, match="Cannot revoke the last USER role"):
            user.revoke_role(ZetaAIRole.USER)

    def test_user_permission_system(self) -> None:
        """Test user permission checking."""
        user = User.create("testuser", "test@example.com", "hash")

        # USER role permissions
        assert user.can(ZetaAIPermission.CHAT_CREATE)
        assert user.can(ZetaAIPermission.CHAT_READ)
        assert not user.can(ZetaAIPermission.AGENT_CREATE)

        # Check multiple permissions
        assert user.can_access(ZetaAIPermission.CHAT_CREATE, ZetaAIPermission.CHAT_READ)
        assert not user.can_access(
            ZetaAIPermission.AGENT_CREATE, ZetaAIPermission.CHAT_CREATE
        )
        assert user.can_access_any(
            ZetaAIPermission.AGENT_CREATE, ZetaAIPermission.CHAT_CREATE
        )

    def test_user_highest_role(self) -> None:
        """Test highest role determination."""
        user = User.create("testuser", "test@example.com", "hash")
        assert user.get_highest_role() == ZetaAIRole.USER

        user.grant_role(ZetaAIRole.PREMIUM)
        assert user.get_highest_role() == ZetaAIRole.PREMIUM

        user.grant_role(ZetaAIRole.ADMIN)
        assert user.get_highest_role() == ZetaAIRole.ADMIN

    def test_user_status_management(self) -> None:
        """Test user status changes."""
        user = User.create("testuser", "test@example.com", "hash")
        assert user.status == UserStatus.PENDING_VERIFICATION

        # Activate
        user.activate()
        assert user.status == UserStatus.ACTIVE
        assert user.is_active()

        # Deactivate
        user.deactivate()
        assert user.status == UserStatus.INACTIVE
        assert not user.is_active()

        # Suspend
        user.suspend(reason="policy violation")
        assert user.status == UserStatus.SUSPENDED

        # Check events
        events = user.get_events()
        status_events = [e for e in events if "user.suspended" in e.event_type]
        assert len(status_events) == 1
        assert status_events[0].event_data["reason"] == "policy violation"

    def test_user_email_verification(self) -> None:
        """Test email verification process."""
        user = User.create("testuser", "test@example.com", "hash")
        assert not user.is_verified()
        assert user.verified_at is None

        user.verify_email()

        assert user.is_verified()
        assert user.verified_at is not None
        assert user.status == UserStatus.ACTIVE

        events = user.get_events()
        verify_events = [e for e in events if e.event_type == "user.verified"]
        assert len(verify_events) == 1

    def test_user_deletion(self) -> None:
        """Test user deletion (soft and hard)."""
        user = User.create("testuser", "test@example.com", "hash")

        # Soft delete
        user.delete(hard_delete=False)
        assert user.status == UserStatus.DELETED
        assert user.deleted_at is not None
        assert user.is_deleted()

        # Clear events to test hard delete
        user.get_events()

        # Hard delete
        user.delete(hard_delete=True)
        events = user.get_events()
        hard_delete_events = [e for e in events if e.event_type == "user.hard_deleted"]
        assert len(hard_delete_events) == 1

    def test_user_login_tracking(self) -> None:
        """Test login tracking."""
        user = User.create("testuser", "test@example.com", "hash")
        assert user.login_count == 0
        assert user.last_login is None

        user.record_login()

        assert user.login_count == 1
        assert user.last_login is not None

        events = user.get_events()
        login_events = [e for e in events if e.event_type == "user.logged_in"]
        assert len(login_events) == 1
        assert login_events[0].event_data["login_count"] == 1

    def test_user_session_tracking(self) -> None:
        """Test session tracking."""
        user = User.create("testuser", "test@example.com", "hash")
        assert user.session_count == 0

        user.record_session_start()

        assert user.session_count == 1

    def test_user_password_update(self) -> None:
        """Test password updates."""
        user = User.create("testuser", "test@example.com", "old_hash")

        user.update_password_hash("new_hash")

        assert user.password_hash == "new_hash"

        events = user.get_events()
        password_events = [e for e in events if e.event_type == "user.password_changed"]
        assert len(password_events) == 1

        # Test validation
        with pytest.raises(ValueError, match="Password hash cannot be empty"):
            user.update_password_hash("")

    def test_user_profile_update(self) -> None:
        """Test profile updates."""
        user = User.create("testuser", "test@example.com", "hash")
        user.update_profile(
            display_name="New Display Name",
            full_name="New Full Name",
            bio="New bio",
            avatar_url="https://example.com/avatar.jpg",
            custom_field="custom_value",
        )

        assert user.display_name == "New Display Name"
        assert user.full_name == "New Full Name"
        assert user.bio == "New bio"
        assert user.avatar_url == "https://example.com/avatar.jpg"
        assert user.metadata["custom_field"] == "custom_value"

        events = user.get_events()
        profile_events = [e for e in events if e.event_type == "user.profile_updated"]
        assert len(profile_events) == 1

    def test_user_preferences_update(self) -> None:
        """Test preferences updates."""
        user = User.create("testuser", "test@example.com", "hash")
        new_preferences = UserPreferences()

        user.update_preferences(new_preferences)

        assert user.preferences == new_preferences

        events = user.get_events()
        pref_events = [e for e in events if e.event_type == "user.preferences_updated"]
        assert len(pref_events) == 1

    def test_user_quota_update(self) -> None:
        """Test quota updates."""
        user = User.create("testuser", "test@example.com", "hash")
        new_quota = UserQuota(max_chats_per_day=100)

        user.update_quota(new_quota)

        assert user.quota == new_quota

        events = user.get_events()
        quota_events = [e for e in events if e.event_type == "user.quota_updated"]
        assert len(quota_events) == 1

    def test_user_admin_checks(self) -> None:
        """Test admin role checks."""
        user = User.create("testuser", "test@example.com", "hash")
        assert not user.is_admin()

        user.grant_role(ZetaAIRole.ADMIN)
        assert user.is_admin()

        user.revoke_role(ZetaAIRole.ADMIN)
        user.grant_role(ZetaAIRole.SUPER_ADMIN)
        assert user.is_admin()

    def test_user_quota_checks(self) -> None:
        """Test quota-based permission checks."""
        user = User.create("testuser", "test@example.com", "hash")

        # Test chat creation quota
        assert user.can_create_chat(current_chats_today=10)
        assert not user.can_create_chat(current_chats_today=100)

        # Test message sending quota
        assert user.can_send_message(current_messages=50, message_length=1000)
        assert not user.can_send_message(current_messages=200, message_length=1000)
        assert not user.can_send_message(current_messages=50, message_length=5000)

        # Test agent creation quota
        assert user.can_create_agent(current_agents=1)
        assert not user.can_create_agent(current_agents=5)

        # Test file upload quota
        assert user.can_upload_file(
            current_files_today=5, file_size_mb=5.0, current_storage_mb=100.0
        )
        assert not user.can_upload_file(
            current_files_today=15, file_size_mb=5.0, current_storage_mb=100.0
        )

    def test_user_to_dict(self) -> None:
        """Test user dictionary representation."""
        user = User.create(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            display_name="Test User",
        )

        user_dict = user.to_dict()

        assert user_dict["username"] == "testuser"
        assert user_dict["email"] == "test@example.com"
        assert user_dict["display_name"] == "Test User"
        assert "password_hash" not in user_dict  # Should not be exposed
        assert user_dict["is_active"] is False  # Pending verification
        assert user_dict["is_verified"] is False
        assert user_dict["highest_role"] == ZetaAIRole.USER
        assert isinstance(user_dict["roles"], list)
        assert isinstance(user_dict["permissions"], list)

    def test_user_events_management(self) -> None:
        """Test domain events management."""
        user = User.create("testuser", "test@example.com", "hash")

        # Should have creation event
        events = user.get_events()
        assert len(events) == 1
        assert events[0].event_type == "user.created"

        # Events should be cleared after getting them
        events_again = user.get_events()
        assert len(events_again) == 0

        # New operations should create new events
        user.activate()
        user.record_login()

        events = user.get_events()
        assert len(events) == 2
        assert events[0].event_type == "user.activated"
        assert events[1].event_type == "user.logged_in"

    def test_user_permission_sync_with_roles(self) -> None:
        """Test that permissions are synced when roles change."""
        user = User.create("testuser", "test@example.com", "hash")
        initial_perms = len(user.permissions)

        # Grant premium role - should add more permissions
        user.grant_role(ZetaAIRole.PREMIUM)
        premium_perms = len(user.permissions)
        assert premium_perms > initial_perms

        # Grant admin role - should add even more permissions
        user.grant_role(ZetaAIRole.ADMIN)
        admin_perms = len(user.permissions)
        assert admin_perms > premium_perms

    def test_user_quota_sync_with_highest_role(self) -> None:
        """Test that quota is synced when roles change."""
        user = User.create("testuser", "test@example.com", "hash")
        initial_quota = user.quota.max_chats_per_day

        # Grant premium role - should update quota
        user.grant_role(ZetaAIRole.PREMIUM)
        premium_quota = user.quota.max_chats_per_day
        assert premium_quota > initial_quota

    def test_user_display_name_defaults(self) -> None:
        """Test display name defaulting logic."""
        user = User(username="testuser", email="test@example.com", password_hash="hash")

        # Post-init should set display_name to username if not provided
        assert user.display_name == "testuser"

        # Creating with explicit display_name should preserve it
        user2 = User.create(
            username="testuser2",
            email="test2@example.com",
            password_hash="hash",
            display_name="Custom Name",
        )
        assert user2.display_name == "Custom Name"
