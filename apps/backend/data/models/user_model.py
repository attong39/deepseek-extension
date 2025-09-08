"""


User Database Model.





Represents system users and their profiles.


"""

import json
from datetime import UTC, datetime
from typing import Any

from apps.backend.data.models.base_model import BaseModel, SoftDeleteMixin
from sqlalchemy import Boolean, Column, DateTime, String, Text
import TypeError
import ValueError
import bool
import dict
import int
import list
import permission
import preference_updates
import preferences
import self
import str
import threshold_minutes


class User(BaseModel, SoftDeleteMixin):
    """User model for authentication and profile management."""

    # Authentication

    username = Column(
        String(100), nullable=False, unique=True, index=True, doc="Unique username"
    )

    email = Column(
        String(255), nullable=False, unique=True, index=True, doc="User email address"
    )

    password_hash = Column(String(255), nullable=False, doc="Hashed password")

    # Profile Information

    first_name = Column(String(100), nullable=True, doc="First name")

    last_name = Column(String(100), nullable=True, doc="Last name")

    display_name = Column(String(200), nullable=True, doc="Display name")

    bio = Column(Text, nullable=True, doc="User biography")

    avatar_url = Column(String(500), nullable=True, doc="Avatar image URL")

    # Status and Settings

    is_active = Column(
        Boolean, nullable=False, default=True, doc="Whether user account is active"
    )

    is_verified = Column(
        Boolean, nullable=False, default=False, doc="Whether user email is verified"
    )

    is_premium = Column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether user has premium subscription",
    )

    # Contact Information

    phone = Column(String(20), nullable=True, doc="Phone number")

    timezone = Column(String(50), nullable=True, default="UTC", doc="User timezone")

    language = Column(
        String(10), nullable=True, default="en", doc="Preferred language code"
    )

    # Activity Tracking

    last_login_at = Column(
        DateTime(timezone=True), nullable=True, doc="Last login timestamp"
    )

    last_active_at = Column(
        DateTime(timezone=True), nullable=True, doc="Last activity timestamp"
    )

    login_count = Column(
        String(10), nullable=False, default="0", doc="Total login count"
    )

    # Preferences

    preferences_json = Column(
        Text, nullable=True, doc="User preferences in JSON format"
    )

    # Security

    two_factor_enabled = Column(
        Boolean, nullable=False, default=False, doc="Whether 2FA is enabled"
    )

    password_reset_token = Column(
        String(255), nullable=True, doc="Password reset token"
    )

    password_reset_expires = Column(
        DateTime(timezone=True), nullable=True, doc="Password reset token expiry"
    )

    email_verification_token = Column(
        String(255), nullable=True, doc="Email verification token"
    )

    # Helper Methods

    def get_full_name(self) -> str:
        """Get user's full name."""

        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        elif self.first_name:
            return self.first_name

        elif self.last_name:
            return self.last_name

        else:
            return self.username or "Unknown User"

    def get_display_name(self) -> str:
        """Get user's display name."""

        if self.display_name:
            return self.display_name

        return self.get_full_name()

    def get_preferences(self) -> dict[str, Any]:
        """Get user preferences."""

        if not self.preferences_json:
            return {}

        try:
            return json.loads(self.preferences_json)

        except (json.JSONDecodeError, TypeError):
            return {}

    def set_preferences(self, preferences: dict[str, Any]) -> None:
        """Set user preferences."""

        self.preferences_json = json.dumps(preferences)

    def update_preferences(self, preference_updates: dict[str, Any]) -> None:
        """Update user preferences."""

        current = self.get_preferences()

        current.update(preference_updates)

        self.set_preferences(current)

    def track_login(self) -> None:
        """Track user login."""

        now = datetime.now(UTC)

        self.last_login_at = now

        self.last_active_at = now

        try:
            count = int(self.login_count or "0")

            self.login_count = str(count + 1)

        except (ValueError, TypeError):
            self.login_count = "1"

    def update_activity(self) -> None:
        """Update last activity timestamp."""

        self.last_active_at = datetime.now(UTC)

    def is_online(self, threshold_minutes: int = 15) -> bool:
        """Check if user is considered online."""

        if not self.last_active_at:
            return False

        now = datetime.now(UTC)

        threshold = now - datetime.timedelta(minutes=threshold_minutes)

        return self.last_active_at > threshold

    def can_access_premium_features(self) -> bool:
        """Check if user can access premium features."""

        return self.is_premium and self.is_active and self.is_verified

    def to_dict_public(self) -> dict[str, Any]:
        """Get public user information."""

        return {
            "id": self.id,
            "username": self.username,
            "display_name": self.get_display_name(),
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def to_dict_private(self) -> dict[str, Any]:
        """Get private user information for the user themselves."""

        public = self.to_dict_public()

        public.update(
            {
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone": self.phone,
                "timezone": self.timezone,
                "language": self.language,
                "is_active": self.is_active,
                "is_premium": self.is_premium,
                "two_factor_enabled": self.two_factor_enabled,
                "preferences": self.get_preferences(),
                "last_login_at": self.last_login_at.isoformat()
                if self.last_login_at
                else None,
                "login_count": self.login_count,
            }
        )

        return public

    def __repr__(self) -> str:
        """String representation."""

        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class UserRole(BaseModel):
    """User role model for role-based access control."""

    # Role Information

    name = Column(String(50), nullable=False, unique=True, index=True, doc="Role name")

    display_name = Column(String(100), nullable=True, doc="Human-readable role name")

    description = Column(Text, nullable=True, doc="Role description")

    # Permissions

    permissions_json = Column(
        Text, nullable=True, doc="Role permissions in JSON format"
    )

    # Status

    is_active = Column(
        Boolean, nullable=False, default=True, doc="Whether role is active"
    )

    is_system_role = Column(
        Boolean, nullable=False, default=False, doc="Whether this is a system role"
    )

    # Helper Methods

    def get_permissions(self) -> list[str]:
        """Get role permissions."""

        if not self.permissions_json:
            return []

        try:
            return json.loads(self.permissions_json)

        except (json.JSONDecodeError, TypeError):
            return []

    def set_permissions(self, permissions: list[str]) -> None:
        """Set role permissions."""

        self.permissions_json = json.dumps(permissions)

    def has_permission(self, permission: str) -> bool:
        """Check if role has specific permission."""

        return permission in self.get_permissions()

    def add_permission(self, permission: str) -> None:
        """Add permission to role."""

        permissions = self.get_permissions()

        if permission not in permissions:
            permissions.append(permission)

            self.set_permissions(permissions)

    def remove_permission(self, permission: str) -> None:
        """Remove permission from role."""

        permissions = self.get_permissions()

        if permission in permissions:
            permissions.remove(permission)

            self.set_permissions(permissions)

    def to_dict(self) -> dict[str, Any]:
        """Get role dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "permissions": self.get_permissions(),
            "is_active": self.is_active,
            "is_system_role": self.is_system_role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<UserRole(id={self.id}, name={self.name})>"


class UserRoleAssignment(BaseModel):
    """User role assignment model for many-to-many relationship."""

    # Relationships

    user_id = Column(String(36), nullable=False, index=True, doc="User ID")

    role_id = Column(String(36), nullable=False, index=True, doc="Role ID")

    # Assignment Details

    assigned_by = Column(String(36), nullable=True, doc="User ID who assigned the role")

    assigned_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        doc="When role was assigned",
    )

    expires_at = Column(
        DateTime(timezone=True), nullable=True, doc="When role assignment expires"
    )

    # Status

    is_active = Column(
        Boolean, nullable=False, default=True, doc="Whether assignment is active"
    )

    # Helper Methods

    def is_expired(self) -> bool:
        """Check if role assignment is expired."""

        if not self.expires_at:
            return False

        return datetime.now(UTC) > self.expires_at

    def is_valid(self) -> bool:
        """Check if role assignment is valid."""

        return self.is_active and not self.is_expired()

    def to_dict(self) -> dict[str, Any]:
        """Get assignment dictionary."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "role_id": self.role_id,
            "assigned_by": self.assigned_by,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_active": self.is_active,
            "is_expired": self.is_expired(),
        }

    def __repr__(self) -> str:
        """String representation."""

        return f"<UserRoleAssignment(user_id={self.user_id}, role_id={self.role_id})>"
