from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any

from apps.backend.core.domain._base_model import DomainModel
from apps.backend.core.domain.mixins import Traceable, Versioned
from apps.backend.core.domain.shared_value_objects import now_utc
from pydantic import ConfigDict, Field, field_validator, model_validator
import ValueError
import classmethod
import dict
import self
import str
import v

_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$")


class ConfigScope(str, Enum):
    GLOBAL = "GLOBAL"
    USER = "USER"
    AGENT = "AGENT"


class ConfigItem(DomainModel, Versioned, Traceable):
    """
    Cấu hình theo scope (GLOBAL/USER/AGENT), immutable + versioned.
    - Key dot-notation: feature.flag_x, ai.temperature, security.rate_limit
    - Value: JSON-serializable dict
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(..., description="Config ID")
    scope: ConfigScope
    key: str = Field(..., min_length=1, max_length=200, description="dot.notation key")
    value: dict[str, Any] = Field(default_factory=dict)

    # scope ràng buộc
    user_id: str | None = Field(default=None)
    agent_id: str | None = Field(default=None)

    updated_by: str | None = Field(default=None)

    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    @field_validator("key")
    @classmethod
    def _valid_key(cls, v: str) -> str:
        if not _KEY_RE.match(v):
            raise ValueError("key phải là dot-notation: [a-z0-9_]+(.[a-z0-9_]+)*")
        return v

    @model_validator(mode="after")
    def _scope_requires_ids(self) -> ConfigItem:
        if self.scope == ConfigScope.USER and not self.user_id:
            raise ValueError("scope=USER yêu cầu user_id")
        if self.scope == ConfigScope.AGENT and not self.agent_id:
            raise ValueError("scope=AGENT yêu cầu agent_id")
        return self
