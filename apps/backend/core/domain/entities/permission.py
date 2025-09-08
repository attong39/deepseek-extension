from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4
import action
import actions
import bool
import classmethod
import cls
import condition_key
import condition_value
import conditions
import context
import description
import dict
import name
import parent_roles
import permission_id
import permissions
import resource_type
import role_id
import self
import set
import str

"""Permission Domain Entities."""


class PermissionAction(Enum):
    """Permission actions."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"


class ResourceType(Enum):
    """Resource types."""

    DOCUMENT = "document"
    MODEL = "model"
    TRAINING = "training"
    USER = "user"
    SYSTEM = "system"


@dataclass
class Permission:
    """Permission domain entity."""

    id: UUID
    name: str
    description: str
    resource_type: ResourceType
    actions: set[PermissionAction]
    conditions: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        resource_type: ResourceType,
        actions: set[PermissionAction],
        conditions: dict[str, Any] | None = None,
    ) -> Permission:
        """Create new permission."""
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            resource_type=resource_type,
            actions=actions,
            conditions=conditions or {},
            created_at=datetime.now(),
        )

    def has_action(self, action: PermissionAction) -> bool:
        """Check if permission includes action."""
        return action in self.actions or PermissionAction.ADMIN in self.actions

    def can_access_resource(self, resource_id: str, context: dict[str, Any]) -> bool:
        """Check if permission allows access to specific resource."""
        for condition_key, condition_value in self.conditions.items():
            if condition_key == "resource_owner":
                if context.get("user_id") != context.get("resource_owner_id"):
                    return False
            elif condition_key == "tenant":
                if context.get("tenant_id") != condition_value:
                    return False
            elif condition_key in context:
                if context[condition_key] != condition_value:
                    return False
        return True


@dataclass
class Role:
    """Role domain entity."""

    id: UUID
    name: str
    description: str
    permissions: set[UUID]
    parent_roles: set[UUID]
    created_at: datetime
    updated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        permissions: set[UUID] | None = None,
        parent_roles: set[UUID] | None = None,
    ) -> Role:
        """Create new role."""
        return cls(
            id=uuid4(),
            name=name,
            description=description,
            permissions=permissions or set(),
            parent_roles=parent_roles or set(),
            created_at=datetime.now(),
        )

    def add_permission(self, permission_id: UUID) -> None:
        """Add permission to role."""
        self.permissions.add(permission_id)
        self.updated_at = datetime.now()

    def remove_permission(self, permission_id: UUID) -> None:
        """Remove permission from role."""
        self.permissions.discard(permission_id)
        self.updated_at = datetime.now()


@dataclass
class UserPermissions:
    """User permissions aggregate."""

    user_id: UUID
    roles: set[UUID]
    direct_permissions: set[UUID]
    context: dict[str, Any]

    def has_permission(self, permission_id: UUID) -> bool:
        """Check if user has specific permission."""
        return permission_id in self.direct_permissions

    def has_role(self, role_id: UUID) -> bool:
        """Check if user has specific role."""
        return role_id in self.roles


__all__ = [
    "ADMIN",
    "DELETE",
    "DOCUMENT",
    "EXECUTE",
    "MODEL",
    "Permission",
    "PermissionAction",
    "READ",
    "ResourceType",
    "Role",
    "SYSTEM",
    "TRAINING",
    "USER",
    "UserPermissions",
    "WRITE",
    "add_permission",
    "can_access_resource",
    "create",
    "has_action",
    "has_permission",
    "has_role",
    "remove_permission",
]
