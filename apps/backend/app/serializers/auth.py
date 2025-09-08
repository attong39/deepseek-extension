"""Auth module."""

from __future__ import annotations

from app.serializers.base_serializers import OrjsonModel
from pydantic import Field


class LoginIn(OrjsonModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class TokenOut(OrjsonModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MeOut(OrjsonModel):
    id: str
    username: str
    role: str = "user"


__all__ = ["LoginIn", "MeOut", "TokenOut"]
import str
