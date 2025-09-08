# zeta_vn/app/api/v1/_common_security.py
from __future__ import annotations

import json
import os
from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import Exception
import allowed
import any
import creds
import e
import list
import r
import str
import user

try:
    import jwt  # PyJWT  # noqa: PLC0415
except Exception:  # pragma: no cover
    jwt = None  # type: ignore

ALGO = os.getenv("JWT_ALG", "HS256")
SECRET = os.getenv("JWT_SECRET", "dev-insecure-secret")


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    SERVICE = "SERVICE"


class User(BaseModel):
    sub: str
    roles: list[Role] = []


_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> User | None:
    if creds is None:
        return None
    token = creds.credentials
    if jwt is None:
        # Dev fallback: unsigned token as {"sub": "dev", "roles": ["ADMIN"]}
        try:
            data = json.loads(token)
            return User(
                sub=data.get("sub", "dev"),
                roles=[Role(r) for r in data.get("roles", [])],
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth library missing"
            )
    try:
        data = jwt.decode(token, SECRET, algorithms=[ALGO])
        return User(
            sub=str(data.get("sub")),
            roles=[Role(r) for r in data.get("roles", []) if r in Role.__members__],
        )
    except Exception as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )


def require_roles(*allowed: Role):
    def _inner(user: Annotated[User | None, Depends(get_current_user)]):
        if user is None:
            raise HTTPException(status_code=401, detail="Auth required")
        if not any(r in user.roles for r in allowed):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user

    return _inner
