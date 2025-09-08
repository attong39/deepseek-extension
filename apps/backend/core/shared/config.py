"""Config module."""

from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "development"
    debug: bool = True

    database_url: str | None = None
    redis_url: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False
import bool
import str
