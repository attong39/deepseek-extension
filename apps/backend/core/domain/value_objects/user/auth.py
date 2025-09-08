"""
Auth Value Objects - ZETA AI
===========================
"""

from pydantic import BaseModel, EmailStr
import int
import str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str | None = None
    role: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user_id: str
    username: str
    email: EmailStr
