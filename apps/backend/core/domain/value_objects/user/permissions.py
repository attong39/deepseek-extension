"""Permission and role value objects for ZETA AI.

This module defines the permission system and role mappings used throughout the domain.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import ROLE_PERMISSIONS
import ROLE_QUOTAS
import all
import any
import bool
import current_agents
import current_chats_today
import current_files_today
import current_messages
import current_storage_mb
import dict
import file_size_mb
import float
import int
import message_length
import p
import permission
import permissions
import role
import self
import set
import str


class ZetaAIPermission(str, Enum):
    """ZETA AI permission enumeration.

    Defines all available permissions in the system.
    """

    # Agent permissions
    AGENT_CREATE = "agent:create"
    AGENT_READ = "agent:read"
    AGENT_UPDATE = "agent:update"
    AGENT_DELETE = "agent:delete"
    AGENT_EXECUTE = "agent:execute"

    # Chat permissions
    CHAT_CREATE = "chat:create"
    CHAT_READ = "chat:read"
    CHAT_UPDATE = "chat:update"
    CHAT_DELETE = "chat:delete"
    CHAT_HISTORY = "chat:history"

    # Memory permissions
    MEMORY_CREATE = "memory:create"
    MEMORY_READ = "memory:read"
    MEMORY_UPDATE = "memory:update"
    MEMORY_DELETE = "memory:delete"

    # Plan permissions
    PLAN_CREATE = "plan:create"
    PLAN_READ = "plan:read"
    PLAN_UPDATE = "plan:update"
    PLAN_DELETE = "plan:delete"
    PLAN_EXECUTE = "plan:execute"

    # Session permissions
    SESSION_CREATE = "session:create"
    SESSION_READ = "session:read"
    SESSION_UPDATE = "session:update"
    SESSION_DELETE = "session:delete"

    # File permissions
    FILE_UPLOAD = "file:upload"
    FILE_READ = "file:read"
    FILE_UPDATE = "file:update"
    FILE_DELETE = "file:delete"

    # Admin permissions
    ADMIN_FULL = "admin:full"
    ADMIN_USERS = "admin:users"
    ADMIN_SYSTEM = "admin:system"
    ADMIN_ANALYTICS = "admin:analytics"

    # System permissions
    SYSTEM_READ = "system:read"
    SYSTEM_WRITE = "system:write"
    SYSTEM_ADMIN = "system:admin"


class ZetaAIRole(str, Enum):
    """ZETA AI role enumeration.

    Defines all available roles in the system.
    """

    GUEST = "guest"
    USER = "user"
    PREMIUM = "premium"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


@dataclass(frozen=True, slots=True)
class RolePermissions:
    """Immutable mapping of role to permissions."""

    role: ZetaAIRole
    permissions: set[ZetaAIPermission]

    def has_permission(self, permission: ZetaAIPermission) -> bool:
        """Check if this role has the given permission.

        Args:
            permission: Permission to check

        Returns:
            True if role has permission
        """
        return permission in self.permissions

    def can_access(self, *permissions: ZetaAIPermission) -> bool:
        """Check if role has all the given permissions.

        Args:
            *permissions: Permissions to check

        Returns:
            True if role has all permissions
        """
        return all(p in self.permissions for p in permissions)

    def can_access_any(self, *permissions: ZetaAIPermission) -> bool:
        """Check if role has any of the given permissions.

        Args:
            *permissions: Permissions to check

        Returns:
            True if role has at least one permission
        """
        return any(p in self.permissions for p in permissions)


# Role permission mappings
ROLE_PERMISSIONS: dict[ZetaAIRole, RolePermissions] = {
    ZetaAIRole.GUEST: RolePermissions(
        role=ZetaAIRole.GUEST,
        permissions={
            ZetaAIPermission.AGENT_READ,
            ZetaAIPermission.CHAT_READ,
        },
    ),
    ZetaAIRole.USER: RolePermissions(
        role=ZetaAIRole.USER,
        permissions={
            ZetaAIPermission.AGENT_READ,
            ZetaAIPermission.CHAT_CREATE,
            ZetaAIPermission.CHAT_READ,
            ZetaAIPermission.CHAT_UPDATE,
            ZetaAIPermission.MEMORY_READ,
            ZetaAIPermission.PLAN_READ,
            ZetaAIPermission.SESSION_CREATE,
            ZetaAIPermission.SESSION_READ,
            ZetaAIPermission.SESSION_UPDATE,
            ZetaAIPermission.FILE_UPLOAD,
            ZetaAIPermission.FILE_READ,
        },
    ),
    ZetaAIRole.PREMIUM: RolePermissions(
        role=ZetaAIRole.PREMIUM,
        permissions={
            ZetaAIPermission.AGENT_CREATE,
            ZetaAIPermission.AGENT_READ,
            ZetaAIPermission.AGENT_UPDATE,
            ZetaAIPermission.CHAT_CREATE,
            ZetaAIPermission.CHAT_READ,
            ZetaAIPermission.CHAT_UPDATE,
            ZetaAIPermission.CHAT_HISTORY,
            ZetaAIPermission.MEMORY_CREATE,
            ZetaAIPermission.MEMORY_READ,
            ZetaAIPermission.MEMORY_UPDATE,
            ZetaAIPermission.PLAN_CREATE,
            ZetaAIPermission.PLAN_READ,
            ZetaAIPermission.PLAN_UPDATE,
            ZetaAIPermission.PLAN_EXECUTE,
            ZetaAIPermission.SESSION_CREATE,
            ZetaAIPermission.SESSION_READ,
            ZetaAIPermission.SESSION_UPDATE,
            ZetaAIPermission.FILE_UPLOAD,
            ZetaAIPermission.FILE_READ,
            ZetaAIPermission.FILE_UPDATE,
        },
    ),
    ZetaAIRole.MODERATOR: RolePermissions(
        role=ZetaAIRole.MODERATOR,
        permissions={
            ZetaAIPermission.AGENT_CREATE,
            ZetaAIPermission.AGENT_READ,
            ZetaAIPermission.AGENT_UPDATE,
            ZetaAIPermission.AGENT_DELETE,
            ZetaAIPermission.CHAT_CREATE,
            ZetaAIPermission.CHAT_READ,
            ZetaAIPermission.CHAT_UPDATE,
            ZetaAIPermission.CHAT_DELETE,
            ZetaAIPermission.CHAT_HISTORY,
            ZetaAIPermission.MEMORY_CREATE,
            ZetaAIPermission.MEMORY_READ,
            ZetaAIPermission.MEMORY_UPDATE,
            ZetaAIPermission.MEMORY_DELETE,
            ZetaAIPermission.PLAN_CREATE,
            ZetaAIPermission.PLAN_READ,
            ZetaAIPermission.PLAN_UPDATE,
            ZetaAIPermission.PLAN_DELETE,
            ZetaAIPermission.PLAN_EXECUTE,
            ZetaAIPermission.SESSION_CREATE,
            ZetaAIPermission.SESSION_READ,
            ZetaAIPermission.SESSION_UPDATE,
            ZetaAIPermission.SESSION_DELETE,
            ZetaAIPermission.FILE_UPLOAD,
            ZetaAIPermission.FILE_READ,
            ZetaAIPermission.FILE_UPDATE,
            ZetaAIPermission.FILE_DELETE,
            ZetaAIPermission.ADMIN_USERS,
        },
    ),
    ZetaAIRole.ADMIN: RolePermissions(
        role=ZetaAIRole.ADMIN,
        permissions={
            ZetaAIPermission.ADMIN_FULL,
            ZetaAIPermission.ADMIN_USERS,
            ZetaAIPermission.ADMIN_SYSTEM,
            ZetaAIPermission.ADMIN_ANALYTICS,
            ZetaAIPermission.SYSTEM_READ,
            ZetaAIPermission.SYSTEM_WRITE,
        },
    ),
    ZetaAIRole.SUPER_ADMIN: RolePermissions(
        role=ZetaAIRole.SUPER_ADMIN,
        permissions=set(ZetaAIPermission),  # All permissions
    ),
}


def get_permissions_for_role(role: ZetaAIRole) -> set[ZetaAIPermission]:
    """Get permissions for a given role.

    Args:
        role: Role to get permissions for

    Returns:
        Set of permissions for the role
    """
    return ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS[ZetaAIRole.GUEST]).permissions


def can_role_access(role: ZetaAIRole, permission: ZetaAIPermission) -> bool:
    """Check if a role has a specific permission.

    Args:
        role: Role to check
        permission: Permission to check

    Returns:
        True if role has permission
    """
    return ROLE_PERMISSIONS.get(
        role, ROLE_PERMISSIONS[ZetaAIRole.GUEST]
    ).has_permission(permission)


@dataclass(frozen=True, slots=True)
class UserQuota:
    """User resource quota value object."""

    # Chat limits
    max_chats_per_day: int = 50
    max_messages_per_chat: int = 100
    max_message_length: int = 4000

    # Agent limits
    max_agents: int = 3
    max_agent_memory_mb: int = 100

    # File limits
    max_files_per_day: int = 10
    max_file_size_mb: int = 10
    max_total_storage_mb: int = 500

    # API limits
    max_api_calls_per_hour: int = 1000
    max_concurrent_sessions: int = 5

    def can_create_chat(self, current_chats_today: int) -> bool:
        """Check if user can create more chats today.

        Args:
            current_chats_today: Number of chats created today

        Returns:
            True if user can create more chats
        """
        return current_chats_today < self.max_chats_per_day

    def can_send_message(self, current_messages: int, message_length: int) -> bool:
        """Check if user can send a message.

        Args:
            current_messages: Current messages in chat
            message_length: Length of new message

        Returns:
            True if user can send message
        """
        return (
            current_messages < self.max_messages_per_chat
            and message_length <= self.max_message_length
        )

    def can_create_agent(self, current_agents: int) -> bool:
        """Check if user can create more agents.

        Args:
            current_agents: Current number of agents

        Returns:
            True if user can create more agents
        """
        return current_agents < self.max_agents

    def can_upload_file(
        self, current_files_today: int, file_size_mb: float, current_storage_mb: float
    ) -> bool:
        """Check if user can upload a file.

        Args:
            current_files_today: Files uploaded today
            file_size_mb: Size of new file in MB
            current_storage_mb: Current storage usage in MB

        Returns:
            True if user can upload file
        """
        return (
            current_files_today < self.max_files_per_day
            and file_size_mb <= self.max_file_size_mb
            and (current_storage_mb + file_size_mb) <= self.max_total_storage_mb
        )


# Quota presets for different roles
ROLE_QUOTAS: dict[ZetaAIRole, UserQuota] = {
    ZetaAIRole.GUEST: UserQuota(
        max_chats_per_day=5,
        max_messages_per_chat=20,
        max_message_length=1000,
        max_agents=0,
        max_agent_memory_mb=0,
        max_files_per_day=0,
        max_file_size_mb=0,
        max_total_storage_mb=0,
        max_api_calls_per_hour=100,
        max_concurrent_sessions=1,
    ),
    ZetaAIRole.USER: UserQuota(
        max_chats_per_day=50,
        max_messages_per_chat=100,
        max_message_length=4000,
        max_agents=3,
        max_agent_memory_mb=100,
        max_files_per_day=10,
        max_file_size_mb=10,
        max_total_storage_mb=500,
        max_api_calls_per_hour=1000,
        max_concurrent_sessions=5,
    ),
    ZetaAIRole.PREMIUM: UserQuota(
        max_chats_per_day=200,
        max_messages_per_chat=500,
        max_message_length=8000,
        max_agents=10,
        max_agent_memory_mb=500,
        max_files_per_day=50,
        max_file_size_mb=50,
        max_total_storage_mb=5000,
        max_api_calls_per_hour=5000,
        max_concurrent_sessions=20,
    ),
    ZetaAIRole.MODERATOR: UserQuota(
        max_chats_per_day=500,
        max_messages_per_chat=1000,
        max_message_length=16000,
        max_agents=25,
        max_agent_memory_mb=1000,
        max_files_per_day=100,
        max_file_size_mb=100,
        max_total_storage_mb=10000,
        max_api_calls_per_hour=10000,
        max_concurrent_sessions=50,
    ),
    ZetaAIRole.ADMIN: UserQuota(
        max_chats_per_day=-1,  # Unlimited
        max_messages_per_chat=-1,
        max_message_length=-1,
        max_agents=-1,
        max_agent_memory_mb=-1,
        max_files_per_day=-1,
        max_file_size_mb=-1,
        max_total_storage_mb=-1,
        max_api_calls_per_hour=-1,
        max_concurrent_sessions=-1,
    ),
    ZetaAIRole.SUPER_ADMIN: UserQuota(
        max_chats_per_day=-1,  # Unlimited
        max_messages_per_chat=-1,
        max_message_length=-1,
        max_agents=-1,
        max_agent_memory_mb=-1,
        max_files_per_day=-1,
        max_file_size_mb=-1,
        max_total_storage_mb=-1,
        max_api_calls_per_hour=-1,
        max_concurrent_sessions=-1,
    ),
}


def get_quota_for_role(role: ZetaAIRole) -> UserQuota:
    """Get quota for a given role.

    Args:
        role: Role to get quota for

    Returns:
        UserQuota for the role
    """
    return ROLE_QUOTAS.get(role, ROLE_QUOTAS[ZetaAIRole.GUEST])
