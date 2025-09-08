from __future__ import annotations

from datetime import datetime
from enum import Enum

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, EmailStr, Field
import any
import bool
import list
import role
import self
import str
import x


class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    PENDING = "PENDING"


class UserRole(str, Enum):
    USER = "USER"
    PREMIUM = "PREMIUM"
    ADMIN = "ADMIN"


class User(DomainModel, Versioned, Traceable):
    """
    Người dùng hệ thống (immutable).
    - Không chứa secret; auth layer quản lý hash/token.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="User ID")
    email: EmailStr
    display_name: str = Field(..., min_length=1, max_length=100)

    status: UserStatus = UserStatus.ACTIVE
    roles: list[UserRole] = Field(default_factory=lambda: [UserRole.USER])

    avatar_url: str | None = None
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    def has_role(self, role: UserRole) -> bool:
        r = role.value
        return any(r == x.value for x in self.roles)
