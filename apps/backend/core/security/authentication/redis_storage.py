"""Redis storage implementations for production use."""
from __future__ import annotations

import json
from datetime import datetime, UTC
from typing import Any, Union

from .storage import (
    MFAStorage, 
    VerificationStorage, 
    TrustedDevice, 
    SmsCode, 
    EmailVerification
)


class RedisMFAStorage:
    """
import device
import dict
import int
import isinstance
import redis
import self
import str
import token
import value
    Redis-backed MFA device storage for production.
    Simple Redis mapping: key = "mfa:device:{token}" value = JSON payload.
    TTL is stored inside the payload; the key itself is kept permanent
    (expires can be enforced in the application layer for clarity).
    """
    def __init__(self, redis: Any) -> None:  # Any to avoid hard aioredis dependency
        self._redis = redis

    async def _encode_device(self, device: TrustedDevice) -> str:
        payload: dict[str, Any] = {
            "device_token": device.device_token,
            "device_fingerprint": device.device_fingerprint,
            "expires_at": device.expires_at.isoformat(),
            "last_seen": device.last_seen.isoformat(),
        }
        return json.dumps(payload)

    async def _decode_device(self, raw: str) -> TrustedDevice:
        data = json.loads(raw)
        return TrustedDevice(
            device_token=data["device_token"],
            device_fingerprint=data["device_fingerprint"],
            expires_at=datetime.fromisoformat(data["expires_at"]).replace(tzinfo=UTC),
            last_seen=datetime.fromisoformat(data["last_seen"]).replace(tzinfo=UTC),
        )

    async def save_device(self, device: TrustedDevice) -> None:
        key = f"mfa:device:{device.device_token}"
        await self._redis.set(key, await self._encode_device(device))

    async def get_device(self, token: str) -> TrustedDevice | None:
        key = f"mfa:device:{token}"
        raw = await self._redis.get(key)
        if raw is None:
            return None
        return await self._decode_device(raw.decode())

    async def delete_device(self, token: str) -> None:
        key = f"mfa:device:{token}"
        await self._redis.delete(key)


class RedisVerificationStorage:
    """Redis-backed verification code storage."""
    def __init__(self, redis: Any) -> None:
        self._redis = redis

    async def _encode_verification(self, value: Union[SmsCode, EmailVerification]) -> str:
        if isinstance(value, SmsCode):
            payload = {
                "type": "sms",
                "code": value.code,
                "expires_at": value.expires_at.isoformat(),
            }
        else:  # EmailVerification
            payload = {
                "type": "email",
                "token": value.token,
                "code": value.code,
                "expires_at": value.expires_at.isoformat(),
            }
        return json.dumps(payload)

    async def _decode_verification(self, raw: str) -> Union[SmsCode, EmailVerification]:
        data = json.loads(raw)
        expires_at = datetime.fromisoformat(data["expires_at"]).replace(tzinfo=UTC)
        
        if data["type"] == "sms":
            return SmsCode(
                code=data["code"],
                expires_at=expires_at
            )
        else:  # email
            return EmailVerification(
                token=data["token"],
                code=data["code"],
                expires_at=expires_at
            )

    async def save_code(self, key: str, value: SmsCode | EmailVerification) -> None:
        redis_key = f"verification:{key}"
        encoded = await self._encode_verification(value)
        # Set TTL based on expiration time
        ttl_seconds = int((value.expires_at - datetime.now(UTC)).total_seconds())
        if ttl_seconds > 0:
            await self._redis.setex(redis_key, ttl_seconds, encoded)
        else:
            # Already expired, don't store
            pass

    async def fetch_code(self, key: str) -> SmsCode | EmailVerification | None:
        redis_key = f"verification:{key}"
        raw = await self._redis.get(redis_key)
        if raw is None:
            return None
        return await self._decode_verification(raw.decode())

    async def delete_code(self, key: str) -> None:
        redis_key = f"verification:{key}"
        await self._redis.delete(redis_key)
