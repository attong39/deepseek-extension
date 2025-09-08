"""
Security System Tests - Test security components and authentication.

Tests cho hệ thống bảo mật:
- Authentication testing
- Authorization testing
- Permission system testing
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from apps.backend.core.domain.entities.user import User
from apps.backend.core.domain.value_objects.security import (
import ImportError
import ValueError
import all
import event
import len
import user
    Permission,
    Role,
    SecurityContext,
)


class TestSecurityContext:
    """Test SecurityContext functionality."""

    def test_create_security_context(self) -> None:
        """Test creating security context."""
        user_id = uuid4()
        tenant_id = uuid4()

        context = SecurityContext(
            user_id=user_id,
            tenant_id=tenant_id,
        )

        assert context.user_id == user_id
        assert context.tenant_id == tenant_id
        assert context.is_authenticated() is True

    def test_anonymous_security_context(self) -> None:
        """Test anonymous security context."""
        context = SecurityContext()

        assert context.user_id is None
        assert context.tenant_id is None
        assert context.is_authenticated() is False

    def test_security_context_with_roles(self) -> None:
        """Test security context with roles."""
        user_id = uuid4()
        roles = ["admin", "user"]

        context = SecurityContext(
            user_id=user_id,
            roles=roles,
        )

        assert context.has_role("admin") is True
        assert context.has_role("user") is True
        assert context.has_role("guest") is False

    def test_security_context_permissions(self) -> None:
        """Test security context permissions."""
        user_id = uuid4()
        permissions = ["read:users", "write:users", "delete:files"]

        context = SecurityContext(
            user_id=user_id,
            permissions=permissions,
        )

        assert context.has_permission("read:users") is True
        assert context.has_permission("write:users") is True
        assert context.has_permission("admin:system") is False


class TestPermissionSystem:
    """Test permission system."""

    def test_create_permission(self) -> None:
        """Test creating permission."""
        permission = Permission(
            name="read:files",
            description="Read files permission",
            resource="files",
            action="read",
        )

        assert permission.name == "read:files"
        assert permission.resource == "files"
        assert permission.action == "read"

    def test_permission_matching(self) -> None:
        """Test permission matching logic."""
        permission = Permission(
            name="write:documents",
            resource="documents",
            action="write",
        )

        # Test exact match
        assert permission.matches("write:documents") is True
        assert permission.matches("read:documents") is False

        # Test wildcard matching
        wildcard_permission = Permission(
            name="*:documents",
            resource="documents",
            action="*",
        )
        assert wildcard_permission.matches("read:documents") is True
        assert wildcard_permission.matches("write:documents") is True
        assert wildcard_permission.matches("delete:files") is False

    def test_permission_hierarchy(self) -> None:
        """Test permission hierarchy."""
        admin_permission = Permission(
            name="admin:*",
            resource="*",
            action="admin",
        )

        # Admin should have access to everything
        assert admin_permission.implies("read:users") is True
        assert admin_permission.implies("write:files") is True
        assert admin_permission.implies("delete:anything") is True

    def test_permission_validation(self) -> None:
        """Test permission validation."""
        with pytest.raises(ValueError, match="Permission name cannot be empty"):
            Permission(
                name="",
                resource="files",
                action="read",
            )

        with pytest.raises(ValueError, match="Resource cannot be empty"):
            Permission(
                name="read:files",
                resource="",
                action="read",
            )


class TestRoleSystem:
    """Test role system."""

    def test_create_role(self) -> None:
        """Test creating role."""
        permissions = [
            Permission(name="read:files", resource="files", action="read"),
            Permission(name="write:files", resource="files", action="write"),
        ]

        role = Role(
            name="file_manager",
            description="File management role",
            permissions=permissions,
        )

        assert role.name == "file_manager"
        assert len(role.permissions) == 2
        assert role.has_permission("read:files") is True
        assert role.has_permission("delete:files") is False

    def test_role_hierarchy(self) -> None:
        """Test role hierarchy."""
        user_role = Role(
            name="user",
            permissions=[
                Permission(name="read:own_files", resource="files", action="read"),
            ],
        )

        admin_role = Role(
            name="admin",
            permissions=[
                Permission(name="admin:*", resource="*", action="admin"),
            ],
            inherits_from=[user_role],
        )

        # Admin should inherit user permissions
        assert admin_role.has_permission("read:own_files") is True
        assert admin_role.has_permission("admin:system") is True

    def test_role_validation(self) -> None:
        """Test role validation."""
        with pytest.raises(ValueError, match="Role name cannot be empty"):
            Role(
                name="",
                permissions=[],
            )


class TestUserAuthentication:
    """Test user authentication."""

    def test_user_creation(self) -> None:
        """Test user creation."""
        user_id = uuid4()
        _ = User(
            id=user_id,
            username="testuser",
            email="test@example.com",
        )

        assert user.id == user_id
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True

    def test_user_password_hashing(self) -> None:
        """Test user password hashing."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        user.set_password("plaintext_password")

        # Password should be hashed
        assert user.password_hash != "plaintext_password"
        assert user.verify_password("plaintext_password") is True
        assert user.verify_password("wrong_password") is False

    def test_user_activation(self) -> None:
        """Test user activation/deactivation."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        assert user.is_active is True

        user.deactivate()
        assert user.is_active is False

        user.activate()
        assert user.is_active is True

    def test_user_roles(self) -> None:
        """Test user roles."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        role = Role(
            name="admin",
            permissions=[
                Permission(name="admin:*", resource="*", action="admin"),
            ],
        )

        user.add_role(role)

        assert user.has_role("admin") is True
        assert user.has_permission("admin:system") is True


class TestAuthorizationRules:
    """Test authorization rules and policies."""

    def test_resource_access_control(self) -> None:
        """Test resource-based access control."""
        user_id = uuid4()
        resource_owner_id = uuid4()

        # User should be able to access their own resources
        context = SecurityContext(user_id=user_id)
        assert context.can_access_resource(resource_owner_id=user_id) is True
        assert context.can_access_resource(resource_owner_id=resource_owner_id) is False

    def test_tenant_isolation(self) -> None:
        """Test tenant isolation."""
        tenant_a = uuid4()
        tenant_b = uuid4()

        context_a = SecurityContext(user_id=uuid4(), tenant_id=tenant_a)
        context_b = SecurityContext(user_id=uuid4(), tenant_id=tenant_b)

        # Users should only access resources in their tenant
        assert context_a.can_access_tenant(tenant_a) is True
        assert context_a.can_access_tenant(tenant_b) is False
        assert context_b.can_access_tenant(tenant_b) is True
        assert context_b.can_access_tenant(tenant_a) is False

    def test_admin_override(self) -> None:
        """Test admin permissions override restrictions."""
        admin_context = SecurityContext(
            user_id=uuid4(),
            roles=["admin"],
            permissions=["admin:*"],
        )

        # Admin should access everything
        assert admin_context.has_permission("read:any_resource") is True
        assert admin_context.has_permission("delete:any_resource") is True
        assert admin_context.can_access_tenant(uuid4()) is True


class TestSecurityValidation:
    """Test security validation and constraints."""

    def test_password_complexity(self) -> None:
        """Test password complexity requirements."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        # Test weak passwords
        with pytest.raises(ValueError, match="Password too weak"):
            user.set_password("123")

        with pytest.raises(ValueError, match="Password too weak"):
            user.set_password("password")

        # Test strong password
        user.set_password("StrongP@ssw0rd123!")
        assert user.verify_password("StrongP@ssw0rd123!") is True

    def test_username_validation(self) -> None:
        """Test username validation."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            User(
                id=uuid4(),
                username="",
                email="test@example.com",
            )

        with pytest.raises(ValueError, match="Invalid username format"):
            User(
                id=uuid4(),
                username="user@name",  # Invalid characters
                email="test@example.com",
            )

    def test_email_validation(self) -> None:
        """Test email validation."""
        with pytest.raises(ValueError, match="Invalid email format"):
            User(
                id=uuid4(),
                username="testuser",
                email="invalid-email",
            )

        # Valid email should work
        _ = User(
            id=uuid4(),
            username="testuser",
            email="valid@example.com",
        )
        assert user.email == "valid@example.com"


class TestSecurityIntegration:
    """Integration tests for security system."""

    def test_authentication_service_integration(self) -> None:
        """Test authentication service integration."""
        try:
            from apps.backend.core.services.auth_service import AuthService

            assert AuthService is not None
        except ImportError:
            pytest.skip("AuthService not available")

    def test_permission_service_integration(self) -> None:
        """Test permission service integration."""
        try:
            from apps.backend.core.services.permission_service import PermissionService

            assert PermissionService is not None
        except ImportError:
            pytest.skip("PermissionService not available")

    def test_security_middleware_integration(self) -> None:
        """Test security middleware integration."""
        try:
            from app.middleware.security import SecurityMiddleware

            assert SecurityMiddleware is not None
        except ImportError:
            pytest.skip("SecurityMiddleware not available")

    def test_jwt_token_integration(self) -> None:
        """Test JWT token integration."""
        try:
            from apps.backend.core.security.jwt import JWTManager

            assert JWTManager is not None
        except ImportError:
            pytest.skip("JWTManager not available")


class TestSecurityEvents:
    """Test security-related events."""

    def test_login_event(self) -> None:
        """Test login event generation."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        # Simulate login
        login_event = user.create_login_event()

        assert login_event.event_type == "user.login"
        assert login_event.user_id == user.id
        assert login_event.timestamp is not None

    def test_permission_denied_event(self) -> None:
        """Test permission denied event."""
        context = SecurityContext(user_id=uuid4())

        # Simulate permission check failure
        denied_event = context.create_permission_denied_event("admin:delete")

        assert denied_event.event_type == "security.permission_denied"
        assert denied_event.permission == "admin:delete"
        assert denied_event.user_id == context.user_id

    def test_security_audit_trail(self) -> None:
        """Test security audit trail."""
        _ = User(
            id=uuid4(),
            username="testuser",
            email="test@example.com",
        )

        # Generate multiple events
        events = [
            user.create_login_event(),
            user.create_logout_event(),
            user.create_password_change_event(),
        ]

        assert len(events) == 3
        assert all(event.user_id == user.id for event in events)
        assert all(event.timestamp is not None for event in events)
