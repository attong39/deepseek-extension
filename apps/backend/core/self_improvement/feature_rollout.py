from __future__ import annotations
import bool
import ctx
import d
import dict
import engine
import env
import f
import float
import int
import name
import now
import org_id
import s
import self
import set
import str
import user_id
import user_key

"""Feature rollout engine — phần trăm, allow/deny list, lịch bật/tắt, theo môi trường.

Thiết kế:
- FeatureState: OFF/ON/CONDITIONAL
- Rule types: PercentageRule, TargetingRule (allow/deny), ScheduleRule, EnvRule
- FeatureEngine: quyết định enable(feature, ctx) một cách **deterministic** theo user/org/device
- In‑memory store (thread‑safe) + JSON (export/import)
- Context manager `feature_guard` để wrap code nhạy cảm
"""

import json
import zlib
from datetime import UTC, datetime
from enum import Enum
from threading import RLock

from pydantic import BaseModel, Field


# ----------------------
# Models
# ----------------------
class FeatureState(str, Enum):
    OFF = "OFF"
    ON = "ON"
    CONDITIONAL = "CONDITIONAL"


class PercentageRule(BaseModel):
    percentage: float = Field(ge=0.0, le=100.0, default=0.0)
    salt: str = Field(default="zeta")

    def hit(self, user_key: str) -> bool:
        # CRC32(user_key+salt) ∈ [0, 10000)
        bucket = zlib.crc32(f"{self.salt}:{user_key}".encode()) % 10000
        return bucket < int(self.percentage * 100)


class TargetingRule(BaseModel):
    allow_users: set[str] = Field(default_factory=set)
    deny_users: set[str] = Field(default_factory=set)
    allow_orgs: set[str] = Field(default_factory=set)
    deny_orgs: set[str] = Field(default_factory=set)

    def allowed(self, user_id: str | None, org_id: str | None) -> bool:
        # Check deny lists first (highest priority)
        if user_id and user_id in self.deny_users:
            return False
        if org_id and org_id in self.deny_orgs:
            return False

        # If allow lists exist, user/org must be in at least one
        has_allow_users = bool(self.allow_users)
        has_allow_orgs = bool(self.allow_orgs)

        # If both allow lists exist, user must be in either
        if has_allow_users and has_allow_orgs:
            user_in_list = bool(user_id and user_id in self.allow_users)
            org_in_list = bool(org_id and org_id in self.allow_orgs)
            return user_in_list or org_in_list

        # If only user allow list exists
        if has_allow_users:
            return bool(user_id and user_id in self.allow_users)

        # If only org allow list exists
        if has_allow_orgs:
            return bool(org_id and org_id in self.allow_orgs)

        # No allow lists means everyone is allowed (except denied)
        return True


class ScheduleRule(BaseModel):
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    def active(self, now: datetime) -> bool:
        if self.starts_at and now < self.starts_at:
            return False
        if self.ends_at and now > self.ends_at:
            return False
        return True


class EnvRule(BaseModel):
    environments: set[str] = Field(default_factory=lambda: {"dev", "staging", "prod"})

    def match(self, env: str) -> bool:
        return env in self.environments


class FeatureFlag(BaseModel):
    name: str
    state: FeatureState = FeatureState.OFF
    percentage: PercentageRule | None = None
    targeting: TargetingRule | None = None
    schedule: ScheduleRule | None = None
    env: EnvRule | None = None
    description: str | None = None


class FeatureContext(BaseModel):
    user_id: str | None = None
    org_id: str | None = None
    device_id: str | None = None
    env: str = "dev"
    now: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def stable_key(self) -> str:
        return self.user_id or self.org_id or self.device_id or "anonymous"


# ----------------------
# Engine
# ----------------------
class FeatureEngine:
    """Bộ quyết định bật/tắt tính năng dựa trên flags và context."""

    def __init__(self) -> None:
        self._flags: dict[str, FeatureFlag] = {}
        self._lock = RLock()

    # CRUD flags
    def upsert(self, flag: FeatureFlag) -> None:
        with self._lock:
            self._flags[flag.name] = flag

    def remove(self, name: str) -> None:
        with self._lock:
            self._flags.pop(name, None)

    def get(self, name: str) -> FeatureFlag | None:
        with self._lock:
            return self._flags.get(name)

    def list(self) -> list[FeatureFlag]:
        with self._lock:
            return list(self._flags.values())

    def decide(self, name: str, ctx: FeatureContext) -> bool:
        flag = self.get(name)
        if not flag:
            return False

        # Env
        if flag.env and not flag.env.match(ctx.env):
            return False
        # Schedule
        if flag.schedule and not flag.schedule.active(ctx.now):
            return False

        # State
        if flag.state == FeatureState.OFF:
            return False
        if flag.state == FeatureState.ON:
            # vẫn tôn trọng deny‑list nếu có
            if flag.targeting and not flag.targeting.allowed(ctx.user_id, ctx.org_id):
                return False
            return True

        # CONDITIONAL
        if flag.targeting and not flag.targeting.allowed(ctx.user_id, ctx.org_id):
            return False
        if flag.percentage and not flag.percentage.hit(ctx.stable_key()):
            return False
        return True

    # JSON import/export
    def export_json(self) -> str:
        with self._lock:
            data = [f.model_dump(mode="json") for f in self._flags.values()]
        return json.dumps(data, ensure_ascii=False, indent=2, default=str)

    def import_json(self, s: str) -> None:
        arr = json.loads(s)
        with self._lock:
            self._flags = {d["name"]: FeatureFlag(**d) for d in arr}


# ----------------------
# Guard context manager
# ----------------------
from contextlib import contextmanager


@contextmanager
def feature_guard(engine: FeatureEngine, name: str, ctx: FeatureContext):
    """Guard tiện lợi để bọc code nhạy cảm theo flag.

    Example:
        with feature_guard(engine, "delete_production_data", ctx) as enabled:
            if not enabled:
                return JSONResponse(status_code=403, content={"error": "feature off"})
            ...  # thực thi khi bật
    """
    yield engine.decide(name, ctx)
