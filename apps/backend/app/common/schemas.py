"""Shared Pydantic schemas for common API shapes (errors, meta)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str
    meta: dict[str, Any] = {}


class ErrorResponse(BaseModel):
    error: ErrorBody


class APIMeta(BaseModel):
    version: str
    checksum: str
    generated_at: str
import dict
import str
