import os
import action
import assigned_by
import assignment
import bool
import conditions
import d
import description
import dict
import display_name
import end_time
import enumerate
import expires_at
import include_expired
import kwargs
import len
import list
import name
import organization_id
import p
import parent_role_id
import permission_id
import permission_manager
import project_id
import resource_id
import resource_owner_id
import resource_type
import role_id
import scope
import self
import set
import start_time
import str
import user_id
"""Advanced Role-Based Access Control (RBAC) system for ZETA AI.





This module provides comprehensive RBAC capabilities including:


- Hierarchical role management


- Fine-grained permission system


- Dynamic role assignment


- Resource-based access control


- Audit logging for access decisions


- Policy-based authorization


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ActionType(str, Enum):
    """Supported action types for permissions."""

    CREATE = "create"

    READ = "read"

    UPDATE = "update"

    DELETE = "delete"

    EXECUTE = "execute"

    APPROVE = "approve"

    ADMIN = "admin"

    MANAGE = "manage"


class ResourceType(str, Enum):
    """Supported resource types."""

    USER = "user"

    ROLE = "role"

    PERMISSION = "permission"

    api_key = os.getenv("API_KEY")

    CONVERSATION = "conversation"

    DOCUMENT = "document"

    AI_MODEL = "ai_model"

    ANALYTICS = "analytics"

    SYSTEM = "system"

    AUDIT_LOG = "audit_log"

    ORGANIZATION = "organization"

    PROJECT = "project"


class PermissionScope(str, Enum):
    """Permission scope levels."""

    GLOBAL = "global"  # System-wide permission

    ORGANIZATION = "organization"  # Organization-level

    PROJECT = "project"  # Project-level

    RESOURCE = "resource"  # Specific resource

    OWNER = "owner"  # Only resource owner


class Permission(BaseModel):
    """Permission definition."""

    permission_id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    resource_type: ResourceType

    action: ActionType

    scope: PermissionScope

    description: str | None = None

    conditions: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Role(BaseModel):
    """Role definition with hierarchical support."""

    role_id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    display_name: str

    description: str | None = None

    parent_role_id: str | None = None  # For role hierarchy

    permissions: set[str] = Field(default_factory=set)  # Permission IDs

    is_system_role: bool = Field(default=False)

    is_active: bool = Field(default=True)

    organization_id: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserRole(BaseModel):
    """User role assignment."""

    assignment_id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str

    role_id: str

    organization_id: str | None = None

    project_id: str | None = None

    assigned_by: str

    assigned_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    expires_at: datetime | None = None

    is_active: bool = Field(default=True)

    conditions: dict[str, Any] = Field(default_factory=dict)


class AccessContext(BaseModel):
    """Context for access control decisions."""

    user_id: str

    ip_address: str | None = None

    user_agent: str | None = None

    organization_id: str | None = None

    project_id: str | None = None

    resource_id: str | None = None

    resource_owner_id: str | None = None

    time_constraints: dict[str, Any] | None = None

    additional_context: dict[str, Any] = Field(default_factory=dict)


class AccessDecision(BaseModel):
    """Access control decision result."""

    decision_id: str = Field(default_factory=lambda: str(uuid4()))

    user_id: str

    resource_type: ResourceType

    action: ActionType

    resource_id: str | None = None

    allowed: bool

    reason: str

    applied_roles: list[str] = Field(default_factory=list)

    applied_permissions: list[str] = Field(default_factory=list)

    context: AccessContext | None = None

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PermissionManager:
    """Permission management system."""

    def __init__(self):
        """Initialize permission manager."""

        self._permissions: dict[str, Permission] = {}

        self._initialize_default_permissions()

    def _initialize_default_permissions(self) -> None:
        """Initialize default system permissions."""

        default_permissions = [
            # User management
            Permission(
                name="user.create",
                resource_type=ResourceType.USER,
                action=ActionType.CREATE,
                scope=PermissionScope.ORGANIZATION,
                description="Create new users",
            ),
            Permission(
                name="user.read",
                resource_type=ResourceType.USER,
                action=ActionType.READ,
                scope=PermissionScope.ORGANIZATION,
                description="View user information",
            ),
            Permission(
                name="user.read.own",
                resource_type=ResourceType.USER,
                action=ActionType.READ,
                scope=PermissionScope.OWNER,
                description="View own user information",
            ),
            Permission(
                name="user.update",
                resource_type=ResourceType.USER,
                action=ActionType.UPDATE,
                scope=PermissionScope.ORGANIZATION,
                description="Update user information",
            ),
            Permission(
                name="user.update.own",
                resource_type=ResourceType.USER,
                action=ActionType.UPDATE,
                scope=PermissionScope.OWNER,
                description="Update own user information",
            ),
            Permission(
                name="user.delete",
                resource_type=ResourceType.USER,
                action=ActionType.DELETE,
                scope=PermissionScope.ORGANIZATION,
                description="Delete users",
            ),
            # Role management
            Permission(
                name="role.create",
                resource_type=ResourceType.ROLE,
                action=ActionType.CREATE,
                scope=PermissionScope.ORGANIZATION,
                description="Create new roles",
            ),
            Permission(
                name="role.read",
                resource_type=ResourceType.ROLE,
                action=ActionType.READ,
                scope=PermissionScope.ORGANIZATION,
                description="View roles",
            ),
            Permission(
                name="role.update",
                resource_type=ResourceType.ROLE,
                action=ActionType.UPDATE,
                scope=PermissionScope.ORGANIZATION,
                description="Update roles",
            ),
            Permission(
                name="role.delete",
                resource_type=ResourceType.ROLE,
                action=ActionType.DELETE,
                scope=PermissionScope.ORGANIZATION,
                description="Delete roles",
            ),
            Permission(
                name="role.assign",
                resource_type=ResourceType.ROLE,
                action=ActionType.MANAGE,
                scope=PermissionScope.ORGANIZATION,
                description="Assign roles to users",
            ),
            # Conversation management
            Permission(
                name="conversation.create",
                resource_type=ResourceType.CONVERSATION,
                action=ActionType.CREATE,
                scope=PermissionScope.PROJECT,
                description="Create conversations",
            ),
            Permission(
                name="conversation.read",
                resource_type=ResourceType.CONVERSATION,
                action=ActionType.READ,
                scope=PermissionScope.PROJECT,
                description="View conversations",
            ),
            Permission(
                name="conversation.read.own",
                resource_type=ResourceType.CONVERSATION,
                action=ActionType.READ,
                scope=PermissionScope.OWNER,
                description="View own conversations",
            ),
            Permission(
                name="conversation.update.own",
                resource_type=ResourceType.CONVERSATION,
                action=ActionType.UPDATE,
                scope=PermissionScope.OWNER,
                description="Update own conversations",
            ),
            Permission(
                name="conversation.delete.own",
                resource_type=ResourceType.CONVERSATION,
                action=ActionType.DELETE,
                scope=PermissionScope.OWNER,
                description="Delete own conversations",
            ),
            # AI Model management
            Permission(
                name="ai_model.use",
                resource_type=ResourceType.AI_MODEL,
                action=ActionType.EXECUTE,
                scope=PermissionScope.PROJECT,
                description="Use AI models",
            ),
            Permission(
                name="ai_model.manage",
                resource_type=ResourceType.AI_MODEL,
                action=ActionType.MANAGE,
                scope=PermissionScope.ORGANIZATION,
                description="Manage AI models",
            ),
            # Analytics
            Permission(
                name="analytics.read",
                resource_type=ResourceType.ANALYTICS,
                action=ActionType.READ,
                scope=PermissionScope.PROJECT,
                description="View analytics",
            ),
            Permission(
                name="analytics.read.organization",
                resource_type=ResourceType.ANALYTICS,
                action=ActionType.READ,
                scope=PermissionScope.ORGANIZATION,
                description="View organization analytics",
            ),
            # System administration
            Permission(
                name="system.admin",
                resource_type=ResourceType.SYSTEM,
                action=ActionType.ADMIN,
                scope=PermissionScope.GLOBAL,
                description="System administration",
            ),
            Permission(
                name="audit_log.read",
                resource_type=ResourceType.AUDIT_LOG,
                action=ActionType.READ,
                scope=PermissionScope.ORGANIZATION,
                description="View audit logs",
            ),
        ]

        for permission in default_permissions:
            self._permissions[permission.permission_id] = permission

    def create_permission(
        self,
        name: str,
        resource_type: ResourceType,
        action: ActionType,
        scope: PermissionScope,
        description: str | None = None,
        conditions: dict[str, Any] | None = None,
    ) -> Permission:
        """Create a new permission.





        Args:


            name: Permission name


            resource_type: Resource type


            action: Action type


            scope: Permission scope


            description: Optional description


            conditions: Optional conditions





        Returns:


            Created permission


        """

        permission = Permission(
            name=name,
            resource_type=resource_type,
            action=action,
            scope=scope,
            description=description,
            conditions=conditions or {},
        )

        self._permissions[permission.permission_id] = permission

        logger.info(f"Created permission: {name}")

        return permission

    def get_permission(self, permission_id: str) -> Permission | None:
        """Get permission by ID.





        Args:


            permission_id: Permission ID





        Returns:


            Permission or None


        """

        return self._permissions.get(permission_id)

    def get_permission_by_name(self, name: str) -> Permission | None:
        """Get permission by name.





        Args:


            name: Permission name





        Returns:


            Permission or None


        """

        for permission in self._permissions.values():
            if permission.name == name:
                return permission

        return None

    def list_permissions(
        self,
        resource_type: ResourceType | None = None,
        action: ActionType | None = None,
        scope: PermissionScope | None = None,
    ) -> list[Permission]:
        """List permissions with optional filtering.





        Args:


            resource_type: Filter by resource type


            action: Filter by action


            scope: Filter by scope





        Returns:


            List of permissions


        """

        permissions = list(self._permissions.values())

        if resource_type:
            permissions = [p for p in permissions if p.resource_type == resource_type]

        if action:
            permissions = [p for p in permissions if p.action == action]

        if scope:
            permissions = [p for p in permissions if p.scope == scope]

        return permissions


class RoleManager:
    """Role management system with hierarchy support."""

    def __init__(self, permission_manager: PermissionManager):
        """Initialize role manager.





        Args:


            permission_manager: Permission manager instance


        """

        self.permission_manager = permission_manager

        self._roles: dict[str, Role] = {}

        self._user_roles: dict[str, list[UserRole]] = {}  # user_id -> [UserRole]

        self._initialize_default_roles()

    def _initialize_default_roles(self) -> None:
        """Initialize default system roles."""

        # Super Admin role

        super_admin_permissions = [
            p.permission_id for p in self.permission_manager.list_permissions()
        ]

        super_admin = Role(
            name="super_admin",
            display_name="Super Administrator",
            description="Full system access",
            permissions=set(super_admin_permissions),
            is_system_role=True,
        )

        self._roles[super_admin.role_id] = super_admin

        # Organization Admin role

        org_admin_permissions = [
            p.permission_id
            for p in self.permission_manager.list_permissions()
            if p.scope
            in [
                PermissionScope.ORGANIZATION,
                PermissionScope.PROJECT,
                PermissionScope.RESOURCE,
                PermissionScope.OWNER,
            ]
        ]

        org_admin = Role(
            name="org_admin",
            display_name="Organization Administrator",
            description="Organization-level administration",
            permissions=set(org_admin_permissions),
            is_system_role=True,
        )

        self._roles[org_admin.role_id] = org_admin

        # Project Manager role

        project_permissions = [
            p.permission_id
            for p in self.permission_manager.list_permissions()
            if p.scope
            in [
                PermissionScope.PROJECT,
                PermissionScope.RESOURCE,
                PermissionScope.OWNER,
            ]
            and p.resource_type
            in [
                ResourceType.CONVERSATION,
                ResourceType.DOCUMENT,
                ResourceType.AI_MODEL,
                ResourceType.ANALYTICS,
            ]
        ]

        project_manager = Role(
            name="project_manager",
            display_name="Project Manager",
            description="Project-level management",
            permissions=set(project_permissions),
            is_system_role=True,
        )

        self._roles[project_manager.role_id] = project_manager

        # User role

        user_permissions = [
            p.permission_id
            for p in self.permission_manager.list_permissions()
            if p.scope == PermissionScope.OWNER
            or (
                p.resource_type == ResourceType.AI_MODEL
                and p.action == ActionType.EXECUTE
            )
            or (
                p.resource_type == ResourceType.CONVERSATION
                and p.action == ActionType.CREATE
            )
        ]

        user_role = Role(
            name="user",
            display_name="User",
            description="Standard user access",
            permissions=set(user_permissions),
            is_system_role=True,
        )

        self._roles[user_role.role_id] = user_role

        # Viewer role

        viewer_permissions = [
            p.permission_id
            for p in self.permission_manager.list_permissions()
            if p.action == ActionType.READ and p.scope == PermissionScope.OWNER
        ]

        viewer_role = Role(
            name="viewer",
            display_name="Viewer",
            description="Read-only access",
            permissions=set(viewer_permissions),
            is_system_role=True,
        )

        self._roles[viewer_role.role_id] = viewer_role

    def create_role(
        self,
        name: str,
        display_name: str,
        description: str | None = None,
        parent_role_id: str | None = None,
        permissions: set[str] | None = None,
        organization_id: str | None = None,
    ) -> Role:
        """Create a new role.





        Args:


            name: Role name


            display_name: Display name


            description: Optional description


            parent_role_id: Parent role for hierarchy


            permissions: Set of permission IDs


            organization_id: Organization ID





        Returns:


            Created role


        """

        role = Role(
            name=name,
            display_name=display_name,
            description=description,
            parent_role_id=parent_role_id,
            permissions=permissions or set(),
            organization_id=organization_id,
        )

        self._roles[role.role_id] = role

        logger.info(f"Created role: {name}")

        return role

    def get_role(self, role_id: str) -> Role | None:
        """Get role by ID.





        Args:


            role_id: Role ID





        Returns:


            Role or None


        """

        return self._roles.get(role_id)

    def get_role_by_name(
        self, name: str, organization_id: str | None = None
    ) -> Role | None:
        """Get role by name.





        Args:


            name: Role name


            organization_id: Organization ID





        Returns:


            Role or None


        """

        for role in self._roles.values():
            if role.name == name:
                if organization_id is None or role.organization_id == organization_id:
                    return role

        return None

    def get_effective_permissions(self, role_id: str) -> set[str]:
        """Get effective permissions including inherited permissions.





        Args:


            role_id: Role ID





        Returns:


            Set of effective permission IDs


        """

        role = self.get_role(role_id)

        if not role:
            return set()

        permissions = role.permissions.copy()

        # Add parent role permissions (recursive)

        if role.parent_role_id:
            parent_permissions = self.get_effective_permissions(role.parent_role_id)

            permissions.update(parent_permissions)

        return permissions

    def assign_role(
        self,
        user_id: str,
        role_id: str,
        assigned_by: str,
        organization_id: str | None = None,
        project_id: str | None = None,
        expires_at: datetime | None = None,
        conditions: dict[str, Any] | None = None,
    ) -> UserRole:
        """Assign role to user.





        Args:


            user_id: User ID


            role_id: Role ID


            assigned_by: ID of user making assignment


            organization_id: Organization ID


            project_id: Project ID


            expires_at: Optional expiration time


            conditions: Optional conditions





        Returns:


            User role assignment


        """

        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            organization_id=organization_id,
            project_id=project_id,
            assigned_by=assigned_by,
            expires_at=expires_at,
            conditions=conditions or {},
        )

        if user_id not in self._user_roles:
            self._user_roles[user_id] = []

        self._user_roles[user_id].append(user_role)

        logger.info(f"Assigned role {role_id} to user {user_id}")

        return user_role

    def revoke_role(
        self,
        user_id: str,
        role_id: str,
        organization_id: str | None = None,
        project_id: str | None = None,
    ) -> bool:
        """Revoke role from user.





        Args:


            user_id: User ID


            role_id: Role ID


            organization_id: Organization ID


            project_id: Project ID





        Returns:


            True if role was revoked


        """

        if user_id not in self._user_roles:
            return False

        user_role_assignments = self._user_roles[user_id]

        for i, assignment in enumerate(user_role_assignments):
            if (
                assignment.role_id == role_id
                and assignment.organization_id == organization_id
                and assignment.project_id == project_id
            ):
                assignment.is_active = False

                logger.info(f"Revoked role {role_id} from user {user_id}")

                return True

        return False

    def get_user_roles(
        self,
        user_id: str,
        organization_id: str | None = None,
        project_id: str | None = None,
        include_expired: bool = False,
    ) -> list[UserRole]:
        """Get user's role assignments.





        Args:


            user_id: User ID


            organization_id: Filter by organization


            project_id: Filter by project


            include_expired: Include expired assignments





        Returns:


            List of user role assignments


        """

        if user_id not in self._user_roles:
            return []

        assignments = self._user_roles[user_id]

        current_time = datetime.now(UTC)

        filtered_assignments = []

        for assignment in assignments:
            if not assignment.is_active:
                continue

            if (
                not include_expired
                and assignment.expires_at
                and assignment.expires_at < current_time
            ):
                continue

            if organization_id and assignment.organization_id != organization_id:
                continue

            if project_id and assignment.project_id != project_id:
                continue

            filtered_assignments.append(assignment)

        return filtered_assignments

    def get_user_effective_permissions(
        self, user_id: str, context: AccessContext | None = None
    ) -> set[str]:
        """Get user's effective permissions from all roles.





        Args:


            user_id: User ID


            context: Access context for filtering





        Returns:


            Set of effective permission IDs


        """

        assignments = self.get_user_roles(
            user_id,
            organization_id=context.organization_id if context else None,
            project_id=context.project_id if context else None,
        )

        all_permissions = set()

        for assignment in assignments:
            role_permissions = self.get_effective_permissions(assignment.role_id)

            all_permissions.update(role_permissions)

        return all_permissions


class AccessControlManager:
    """Central access control manager."""

    def __init__(self):
        """Initialize access control manager."""

        self.permission_manager = PermissionManager()

        self.role_manager = RoleManager(self.permission_manager)

        self._access_log: list[AccessDecision] = []

    def check_permission(
        self,
        user_id: str,
        resource_type: ResourceType,
        action: ActionType,
        context: AccessContext | None = None,
    ) -> AccessDecision:
        """Check if user has permission to perform action.





        Args:


            user_id: User ID


            resource_type: Resource type


            action: Action to perform


            context: Access context





        Returns:


            Access decision


        """

        if context is None:
            context = AccessContext(user_id=user_id)

        # Get user's effective permissions

        user_permissions = self.role_manager.get_user_effective_permissions(
            user_id, context
        )

        # Find matching permissions

        matching_permissions = []

        applied_roles = []

        for permission_id in user_permissions:
            permission = self.permission_manager.get_permission(permission_id)

            if not permission:
                continue

            if (
                permission.resource_type == resource_type
                and permission.action == action
            ):
                # Check scope

                if self._check_permission_scope(permission, context):
                    matching_permissions.append(permission_id)

        # Get applied roles

        user_role_assignments = self.role_manager.get_user_roles(
            user_id, context.organization_id, context.project_id
        )

        applied_roles = [assignment.role_id for assignment in user_role_assignments]

        # Make decision

        allowed = len(matching_permissions) > 0

        reason = (
            f"Permission granted via {len(matching_permissions)} matching permissions"
            if allowed
            else "No matching permissions found"
        )

        decision = AccessDecision(
            user_id=user_id,
            resource_type=resource_type,
            action=action,
            resource_id=context.resource_id,
            allowed=allowed,
            reason=reason,
            applied_roles=applied_roles,
            applied_permissions=matching_permissions,
            context=context,
        )

        self._access_log.append(decision)

        return decision

    def _check_permission_scope(
        self, permission: Permission, context: AccessContext
    ) -> bool:
        """Check if permission scope matches context.





        Args:


            permission: Permission to check


            context: Access context





        Returns:


            True if scope matches


        """

        if permission.scope == PermissionScope.GLOBAL:
            return True

        if permission.scope == PermissionScope.ORGANIZATION:
            return context.organization_id is not None

        if permission.scope == PermissionScope.PROJECT:
            return context.project_id is not None

        if permission.scope == PermissionScope.RESOURCE:
            return context.resource_id is not None

        if permission.scope == PermissionScope.OWNER:
            return (
                context.resource_owner_id is not None
                and context.resource_owner_id == context.user_id
            )

        return False

    def has_permission(
        self,
        user_id: str,
        resource_type: ResourceType,
        action: ActionType,
        context: AccessContext | None = None,
    ) -> bool:
        """Check if user has permission (convenience method).





        Args:


            user_id: User ID


            resource_type: Resource type


            action: Action to perform


            context: Access context





        Returns:


            True if user has permission


        """

        decision = self.check_permission(user_id, resource_type, action, context)

        return decision.allowed

    def get_access_log(
        self,
        user_id: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[AccessDecision]:
        """Get access control log.





        Args:


            user_id: Filter by user ID


            start_time: Filter by start time


            end_time: Filter by end time





        Returns:


            List of access decisions


        """

        filtered_log = self._access_log

        if user_id:
            filtered_log = [d for d in filtered_log if d.user_id == user_id]

        if start_time:
            filtered_log = [d for d in filtered_log if d.timestamp >= start_time]

        if end_time:
            filtered_log = [d for d in filtered_log if d.timestamp <= end_time]

        return filtered_log


# Factory functions


def create_access_control_manager() -> AccessControlManager:
    """Create access control manager instance.





    Returns:


        AccessControlManager instance


    """

    return AccessControlManager()


def create_access_context(
    user_id: str,
    organization_id: str | None = None,
    project_id: str | None = None,
    resource_id: str | None = None,
    resource_owner_id: str | None = None,
    **kwargs,
) -> AccessContext:
    """Create access context.





    Args:


        user_id: User ID


        organization_id: Organization ID


        project_id: Project ID


        resource_id: Resource ID


        resource_owner_id: Resource owner ID


        **kwargs: Additional context data





    Returns:


        Access context


    """

    return AccessContext(
        user_id=user_id,
        organization_id=organization_id,
        project_id=project_id,
        resource_id=resource_id,
        resource_owner_id=resource_owner_id,
        additional_context=kwargs,
    )
