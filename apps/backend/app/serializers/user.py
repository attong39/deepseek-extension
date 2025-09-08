"""User module."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.serializers.base_serializers import OrjsonModel
from pydantic import EmailStr, Field


class UserCreateIn(OrjsonModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field("user", pattern=r"^(user|premium|admin)$")
    profile: dict[str, Any] = Field(default_factory=dict)


class UserUpdateIn(OrjsonModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6)
    role: str | None = Field(default=None, pattern=r"^(user|premium|admin)$")
    profile: dict[str, Any] | None = None


class UserOut(OrjsonModel):
    id: str
    username: str
    email: EmailStr
    role: str
    profile: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


__all__ = ["UserCreateIn", "UserOut", "UserUpdateIn"]
import dict
import str
