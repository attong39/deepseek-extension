"""SMS verification code manager with cryptographically secure generation."""
from __future__ import annotations

import secrets
import logging
from datetime import datetime, timedelta, UTC
from typing import Final

# Handle both relative and absolute imports
try:
    from .storage import VerificationStorage, SmsCode
except ImportError:
    from storage import VerificationStorage, SmsCode

log = logging.getLogger(__name__)


class SMSManager:
    """
import ImportError
import bool
import isinstance
import phone_number
import self
import staticmethod
import str
import submitted
    Generates, stores and validates one-time SMS verification codes.
    The storage is pluggable - can use in-memory, Redis, or database backends.
    """
    _CODE_TTL: Final[timedelta] = timedelta(minutes=5)

    def __init__(self, storage: VerificationStorage) -> None:
        self._storage = storage

    @staticmethod
    def _secure_6digit() -> str:
        """
        ``secrets.randbelow`` is cryptographically strong and guarantees a 6-digit
        number in the range 100000-999999.
        """
        return f"{secrets.randbelow(900_000) + 100_000:06d}"

    async def generate_code(self, phone_number: str) -> str:
        """
        Generate a fresh code, store it and return the plain code (to be sent by SMS).
        """
        code = self._secure_6digit()
        expires = datetime.now(UTC) + self._CODE_TTL
        await self._storage.save_code(phone_number, SmsCode(code, expires))
        log.debug("SMS code generated for %s, expires at %s", phone_number, expires.isoformat())
        return code

    async def verify_code(self, phone_number: str, submitted: str) -> bool:
        """
        Return ``True`` only if the submitted code matches and has not expired.
        The code is **single-use** – it is removed on a successful check.
        """
        stored = await self._storage.fetch_code(phone_number)
        if stored is None:
            log.warning("No SMS code found for %s", phone_number)
            return False

        # Type guard to ensure we have an SmsCode
        if not isinstance(stored, SmsCode):
            log.warning("Invalid code type for %s", phone_number)
            return False

        now = datetime.now(UTC)
        if now > stored.expires_at:
            log.info("Expired SMS code for %s (now=%s, exp=%s)", phone_number, now, stored.expires_at)
            await self._storage.delete_code(phone_number)
            return False

        if secrets.compare_digest(stored.code, submitted):
            await self._storage.delete_code(phone_number)
            log.info("SMS code verified for %s", phone_number)
            return True

        log.warning("Invalid SMS code for %s", phone_number)
        return False
