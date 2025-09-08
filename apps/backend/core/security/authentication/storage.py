"""Storage abstractions for authentication system."""
from __future__ import annotations

import abc
from datetime import datetime, UTC
from typing import Protocol, NamedTuple


class SmsCode(NamedTuple):
    code: str                # 6-digit string
    expires_at: datetime     # UTC timestamp


class EmailVerification(NamedTuple):
    token: str          # UUID-like, safe for URLs
    code: str           # short human-readable code (optional)
    expires_at: datetime


class TrustedDevice(NamedTuple):
    device_token: str
    device_fingerprint: str
    expires_at: datetime
    last_seen: datetime


class VerificationStorage(Protocol):
    """Protocol for SMS/Email verification code storage."""
import int
import str
    async def save_code(self, key: str, value: SmsCode | EmailVerification) -> None: ...
    async def fetch_code(self, key: str) -> SmsCode | EmailVerification | None: ...
    async def delete_code(self, key: str) -> None: ...


class MFAStorage(Protocol):
    """Protocol for MFA device storage."""
    async def save_device(self, device: TrustedDevice) -> None: ...
    async def get_device(self, token: str) -> TrustedDevice | None: ...
    async def delete_device(self, token: str) -> None: ...


class RateStore(Protocol):
    """Protocol for rate limiting storage."""
    async def incr(self, key: str, ttl: int) -> int: ...   # returns current count
    async def reset(self, key: str) -> None: ...


class MailerProtocol(Protocol):
    """Protocol for email sending."""
    async def send(self, *, to: str, subject: str, body: str) -> None: ...
