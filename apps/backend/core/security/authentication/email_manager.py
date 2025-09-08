"""Email verification manager."""
from __future__ import annotations

import secrets
import logging
from datetime import datetime, timedelta, UTC
from typing import Final

# Handle both relative and absolute imports
try:
    from .storage import VerificationStorage, EmailVerification, MailerProtocol
except ImportError:
    from storage import VerificationStorage, EmailVerification, MailerProtocol

log = logging.getLogger(__name__)


class EmailManager:
    """Handles email verification with tokens and backup codes."""
import ImportError
import base_url
import bool
import email
import is_token
import isinstance
import mailer
import self
import str
import value
    _TTL: Final[timedelta] = timedelta(hours=2)

    def __init__(self, mailer: MailerProtocol, storage: VerificationStorage) -> None:
        """
        ``mailer`` is any object that implements ``send(to, subject, body)``.
        ``storage`` can be the same ``VerificationStorage`` used for SMS.
        """
        self._mailer = mailer
        self._storage = storage

    async def send_verification(self, email: str, base_url: str = "https://example.com") -> str:
        """Send verification email with token and backup code."""
        token = secrets.token_urlsafe(32)
        code = f"{secrets.randbelow(9000) + 1000:04d}"   # optional 4-digit backup code
        expires = datetime.now(UTC) + self._TTL
        
        verification = EmailVerification(token, code, expires)
        await self._storage.save_code(f"email:{email}", verification)

        # Email body with both token link and backup code
        body = (
            f"Your email verification code is: **{code}**\n\n"
            f"Or click this link to verify automatically:\n"
            f"{base_url}/verify-email?token={token}\n\n"
            f"This verification expires at {expires.isoformat()}\n\n"
            f"If you didn't request this verification, please ignore this email."
        )
        
        await self._mailer.send(
            to=email, 
            subject="Verify your email address", 
            body=body
        )
        
        log.info("Verification email sent to %s (expires %s)", email, expires.isoformat())
        return token

    async def verify_token(self, email: str, token: str) -> bool:
        """Verify email using the URL token."""
        return await self._verify_email(email, token, is_token=True)

    async def verify_code(self, email: str, code: str) -> bool:
        """Verify email using the 4-digit backup code."""
        return await self._verify_email(email, code, is_token=False)

    async def _verify_email(self, email: str, value: str, is_token: bool) -> bool:
        """Internal verification method for both tokens and codes."""
        stored = await self._storage.fetch_code(f"email:{email}")
        if not stored:
            log.warning("No email verification found for %s", email)
            return False

        # Type guard to ensure we have an EmailVerification
        if not isinstance(stored, EmailVerification):
            log.warning("Invalid verification type for %s", email)
            return False

        now = datetime.now(UTC)
        if now > stored.expires_at:
            log.info("Expired email verification for %s (now=%s, exp=%s)", 
                    email, now, stored.expires_at)
            await self._storage.delete_code(f"email:{email}")
            return False

        # Check either token or code based on verification type
        target_value = stored.token if is_token else stored.code
        if secrets.compare_digest(target_value, value):
            await self._storage.delete_code(f"email:{email}")
            log.info("Email %s verified via %s", email, "token" if is_token else "code")
            return True

        log.warning("Invalid email %s for %s", "token" if is_token else "code", email)
        return False

    async def resend_verification(self, email: str, base_url: str = "https://example.com") -> str:
        """Resend verification email (invalidates previous one)."""
        # Delete any existing verification
        await self._storage.delete_code(f"email:{email}")
        # Send new one
        return await self.send_verification(email, base_url)
