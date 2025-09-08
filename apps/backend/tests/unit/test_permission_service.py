from __future__ import annotations

from uuid import uuid4

import pytest
from apps.backend.core.domain.entities.permission import PermissionAction, ResourceType
from apps.backend.core.services.permission_service import PermissionService

"""Tests for Permission Service."""


class TestPermissionService:
    """Test permission service."""

    @pytest.fixture
    def service(self):
        """Create permission service."""
        return PermissionService()

    def test_create_permission(self, service):
        """Test creating permission."""
        permission = service.create_permission(
            name="read_documents",
            description="Read document permission",
            resource_type=ResourceType.DOCUMENT,
            actions={PermissionAction.READ},
        )
        assert permission.name == "read_documents"
        assert permission.resource_type == ResourceType.DOCUMENT
        assert PermissionAction.READ in permission.actions

    def test_create_role(self, service):
        """Test creating role."""
        permission = service.create_permission(
            name="read_docs",
            description="Read docs",
            resource_type=ResourceType.DOCUMENT,
            actions={PermissionAction.READ},
        )
        role = service.create_role(
            name="viewer",
            description="Document viewer role",
            permission_ids={permission.id},
        )
        assert role.name == "viewer"
        assert permission.id in role.permissions

    def test_assign_role_to_user(self, service):
        """Test assigning role to user."""
        role = service.create_role("test_role", "Test role")
        user_id = uuid4()
        success = service.assign_role_to_user(user_id, role.id)
        assert success
        user_perms = service._user_permissions[user_id]
        assert role.id in user_perms.roles

    def test_check_permission_with_role(self, service):
        """Test checking permission through role."""
        permission = service.create_permission(
            name="read_documents",
            description="Read documents",
            resource_type=ResourceType.DOCUMENT,
            actions={PermissionAction.READ},
        )
        role = service.create_role(
            name="reader", description="Reader role", permission_ids={permission.id}
        )
        user_id = uuid4()
        service.assign_role_to_user(user_id, role.id)
        has_permission = service.check_permission(
            user_id=user_id,
            resource_type=ResourceType.DOCUMENT,
            action=PermissionAction.READ,
        )
        assert has_permission

    def test_check_permission_denied(self, service):
        """Test permission denied."""
        user_id = uuid4()
        has_permission = service.check_permission(
            user_id=user_id,
            resource_type=ResourceType.DOCUMENT,
            action=PermissionAction.WRITE,
        )
        assert not has_permission

    def test_admin_permission_allows_all_actions(self, service):
        """Test admin permission allows all actions."""
        permission = service.create_permission(
            name="admin_documents",
            description="Admin documents",
            resource_type=ResourceType.DOCUMENT,
            actions={PermissionAction.ADMIN},
        )
        role = service.create_role("admin", "Admin role", {permission.id})
        user_id = uuid4()
        service.assign_role_to_user(user_id, role.id)
        for action in [
            PermissionAction.READ,
            PermissionAction.WRITE,
            PermissionAction.DELETE,
        ]:
            has_permission = service.check_permission(
                user_id=user_id, resource_type=ResourceType.DOCUMENT, action=action
            )
            assert has_permission


__all__ = [
    "TestPermissionService",
    "action",
]


@pytest.fixture
def action():
    """Fixture for action"""
    return None  # TODO: Define appropriate fixture
