"""Advanced Multi-Factor Authentication (MFA) system for ZETA AI.





This module provides comprehensive MFA capabilities including:


- TOTP (Time-based One-Time Password) support


- SMS verification


- Email verification


- Backup codes


- Device trust management


- Progressive MFA enforcement


"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import random
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import bcrypt
import pyotp
import qrcode
from apps.backend.core.security.encryption.field_encryption import FieldEncryption
from pydantic import BaseModel, Field
from qrcode import constants as qrcode_constants
from qrcode.image.styledpil import StyledPilImage
import Exception
import additional_data
import bool
import bytes
import config
import d
import device_fingerprint
import device_name
import dict
import e
import int
import ip_address
import key
import kwargs
import len
import list
import method
import phone_number
import provided_code
import range
import require_mfa_for_admin
import self
import sorted
import stored_code
import stored_hash
import str
import token
import totp_issuer
import tuple
import user_agent
import user_email
import user_id
import user_roles
import value

logger = logging.getLogger(__name__)


class MFAConfig(BaseModel):
    """MFA configuration settings."""

    totp_issuer: str = Field(default="ZETA AI")

    totp_period: int = Field(default=30)  # 30 seconds

    totp_digits: int = Field(default=6)

    backup_codes_count: int = Field(default=10)

    device_trust_duration_days: int = Field(default=30)

    max_failed_attempts: int = Field(default=3)

    lockout_duration_minutes: int = Field(default=15)

    require_mfa_for_admin: bool = Field(default=True)

    progressive_mfa_enabled: bool = Field(default=True)


class MFADevice(BaseModel):
    """MFA device representation."""

    device_id: str

    user_id: str

    device_type: str  # "totp", "sms", "email"

    device_name: str

    secret_key: str | None = None  # Encrypted

    phone_number: str | None = None  # For SMS

    email: str | None = None  # For email

    is_verified: bool = Field(default=False)

    is_primary: bool = Field(default=False)

    last_used: datetime | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    metadata: dict[str, Any] = Field(default_factory=dict)


class TrustedDevice(BaseModel):
    """Trusted device for MFA bypass."""

    device_token: str

    user_id: str

    device_fingerprint: str

    device_name: str

    ip_address: str

    user_agent: str

    last_seen: datetime = Field(default_factory=lambda: datetime.now(UTC))

    expires_at: datetime

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class BackupCode(BaseModel):
    """MFA backup recovery code."""

    code_id: str

    user_id: str

    code_hash: str  # Hashed backup code

    is_used: bool = Field(default=False)

    used_at: datetime | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class MFAAttempt(BaseModel):
    """MFA verification attempt tracking."""

    attempt_id: str

    user_id: str

    device_id: str | None = None

    method: str  # "totp", "sms", "email", "backup"

    success: bool

    ip_address: str

    user_agent: str

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    error_message: str | None = None


class TOTPManager:
    """TOTP (Time-based One-Time Password) manager."""

    def __init__(self, config: MFAConfig):
        """Initialize TOTP manager.





        Args:


            config: MFA configuration


        """

        self.config = config

        self.field_encryption = FieldEncryption()

    def generate_secret(self) -> str:
        """Generate a new TOTP secret key.





        Returns:


            Base32-encoded secret key


        """

        return pyotp.random_base32()

    def generate_qr_code(
        self, secret: str, user_email: str, account_name: str | None = None
    ) -> bytes:
        """Generate QR code for TOTP setup.





        Args:


            secret: TOTP secret key


            user_email: User's email address


            account_name: Optional account name





        Returns:


            QR code image as bytes


        """

        account_name = account_name or user_email

        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=account_name, issuer_name=self.config.totp_issuer
        )
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode_constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(totp_uri)

        qr.make(fit=True)

        # Create QR code image

        img = qr.make_image(
            fill_color="black", back_color="white", image_factory=StyledPilImage
        )

        # Convert to bytes

        import io

        img_buffer = io.BytesIO()

        img.save(img_buffer, format="PNG")

        return img_buffer.getvalue()

    def verify_totp(self, secret: str, token: str) -> bool:
        """Verify TOTP token.





        Args:


            secret: TOTP secret key


            token: User-provided token





        Returns:


            True if token is valid


        """

        try:
            totp = pyotp.TOTP(secret, digits=self.config.totp_digits)

            return totp.verify(token, valid_window=1)  # Allow 1 time step tolerance

        except Exception as e:
            logger.error(f"TOTP verification error: {e}")

            return False


class SMSManager:
    """SMS-based MFA manager."""

    def __init__(self, config: MFAConfig):
        """Initialize SMS manager.





        Args:


            config: MFA configuration


        """

        self.config = config

        self._verification_codes: dict[str, tuple[str, datetime]] = {}

    def generate_code(self) -> str:
        """Generate a random verification code.





        Returns:


            6-digit verification code


        """

        return f"{random.randint(100000, 999999):06d}"

    async def send_verification_code(self, phone_number: str, user_id: str) -> str:
        """Send SMS verification code.





        Args:


            phone_number: Target phone number


            user_id: User ID for tracking





        Returns:


            Code ID for verification


        """

        code = self.generate_code()

        code_id = str(uuid4())

        expires_at = datetime.now(UTC) + timedelta(minutes=5)

        # Store code temporarily

        self._verification_codes[code_id] = (code, expires_at)

        # TODO: Integrate with SMS service (Twilio, AWS SNS, etc.)

        logger.info(f"SMS code {code} sent to {phone_number[-4:]} for user {user_id}")

        # In development, log the code

        if os.getenv("ZETA_AI_ENV") != "production":
            logger.info(f"SMS verification code: {code}")

        return code_id

    def verify_code(self, code_id: str, provided_code: str) -> bool:
        """Verify SMS code.





        Args:


            code_id: Code ID from send_verification_code


            provided_code: User-provided code





        Returns:


            True if code is valid


        """

        if code_id not in self._verification_codes:
            return False

        stored_code, expires_at = self._verification_codes[code_id]

        # Check expiration

        if datetime.now(UTC) > expires_at:
            del self._verification_codes[code_id]

            return False

        # Verify code

        is_valid = hmac.compare_digest(stored_code, provided_code)

        # Remove code after verification attempt

        del self._verification_codes[code_id]

        return is_valid


class BackupCodeManager:
    """Backup code manager for MFA recovery."""

    def __init__(self, config: MFAConfig):
        """Initialize backup code manager.





        Args:


            config: MFA configuration


        """

        self.config = config

    def generate_backup_codes(self, count: int | None = None) -> list[str]:
        """Generate backup recovery codes.





        Args:


            count: Number of codes to generate





        Returns:


            List of backup codes


        """

        count = count or self.config.backup_codes_count

        codes = []

        for _ in range(count):
            # Generate 8-character alphanumeric code

            code = secrets.token_hex(4).upper()

            codes.append(code)

        return codes

    def hash_backup_code(self, code: str) -> str:
        """Hash a backup code for storage.





        Args:


            code: Plain backup code





        Returns:


            Hashed backup code


        """

        return bcrypt.hashpw(code.encode(), bcrypt.gensalt()).decode()

    def verify_backup_code(self, provided_code: str, stored_hash: str) -> bool:
        """Verify backup code against stored hash.





        Args:


            provided_code: User-provided backup code


            stored_hash: Stored hash





        Returns:


            True if code is valid


        """

        try:
            return bcrypt.checkpw(provided_code.encode(), stored_hash.encode())

        except Exception as e:
            logger.error(f"Backup code verification error: {e}")

            return False


class DeviceTrustManager:
    """Device trust management for MFA bypass."""

    def __init__(self, config: MFAConfig):
        """Initialize device trust manager.





        Args:


            config: MFA configuration


        """

        self.config = config

    def generate_device_fingerprint(
        self,
        user_agent: str,
        ip_address: str,
        additional_data: dict[str, Any] | None = None,
    ) -> str:
        """Generate device fingerprint.





        Args:


            user_agent: Browser user agent


            ip_address: Client IP address


            additional_data: Additional fingerprint data





        Returns:


            Device fingerprint hash


        """

        fingerprint_data = f"{user_agent}:{ip_address}"

        if additional_data:
            for key, value in sorted(additional_data.items()):
                fingerprint_data += f":{key}={value}"

        return hashlib.sha256(fingerprint_data.encode()).hexdigest()

    def create_trusted_device(
        self,
        user_id: str,
        device_fingerprint: str,
        device_name: str,
        ip_address: str,
        user_agent: str,
    ) -> TrustedDevice:
        """Create a trusted device.





        Args:


            user_id: User ID


            device_fingerprint: Device fingerprint


            device_name: Human-readable device name


            ip_address: Device IP address


            user_agent: Device user agent





        Returns:


            TrustedDevice instance


        """

        device_token = secrets.token_urlsafe(32)

        expires_at = datetime.now(UTC) + timedelta(
            days=self.config.device_trust_duration_days
        )

        return TrustedDevice(
            device_token=device_token,
            user_id=user_id,
            device_fingerprint=device_fingerprint,
            device_name=device_name,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
        )

    def is_device_trusted(self, device_token: str, device_fingerprint: str) -> bool:
        """Check if device is trusted.





        Args:


            device_token: Device trust token


            device_fingerprint: Current device fingerprint





        Returns:


            True if device is trusted


        """

        # TODO: Implement database lookup

        # This is a placeholder implementation

        return False


class MFAManager:
    """Central MFA management system."""

    def __init__(self, config: MFAConfig | None = None):
        """Initialize MFA manager.





        Args:


            config: MFA configuration


        """

        self.config = config or MFAConfig()

        self.totp = TOTPManager(self.config)

        self.sms = SMSManager(self.config)

        self.backup_codes = BackupCodeManager(self.config)

        self.device_trust = DeviceTrustManager(self.config)

        self.field_encryption = FieldEncryption()

        # In-memory storage for demo (replace with database)

        self._devices: dict[str, MFADevice] = {}

        self._trusted_devices: dict[str, TrustedDevice] = {}

        self._backup_codes: dict[str, list[BackupCode]] = {}

        self._attempts: list[MFAAttempt] = []

    async def setup_totp(
        self, user_id: str, user_email: str, device_name: str = "Authenticator App"
    ) -> tuple[str, bytes]:
        """Set up TOTP for a user.





        Args:


            user_id: User ID


            user_email: User email


            device_name: Device name





        Returns:


            Tuple of (device_id, qr_code_image)


        """

        secret = self.totp.generate_secret()

        device_id = str(uuid4())

        # Encrypt the secret

        encrypted_secret = self.field_encryption.encrypt(secret)

        device = MFADevice(
            device_id=device_id,
            user_id=user_id,
            device_type="totp",
            device_name=device_name,
            secret_key=encrypted_secret,
            is_verified=False,
        )

        self._devices[device_id] = device

        # Generate QR code

        qr_code = self.totp.generate_qr_code(secret, user_email)

        return device_id, qr_code

    async def verify_totp_setup(self, device_id: str, token: str) -> bool:
        """Verify TOTP setup with initial token.





        Args:


            device_id: Device ID


            token: TOTP token





        Returns:


            True if setup is verified


        """

        device = self._devices.get(device_id)

        if not device or device.device_type != "totp":
            return False

        # Decrypt secret

        secret = self.field_encryption.decrypt(device.secret_key)

        # Verify token

        if self.totp.verify_totp(secret, token):
            device.is_verified = True

            device.last_used = datetime.now(UTC)

            return True

        return False

    async def setup_sms(
        self, user_id: str, phone_number: str, device_name: str = "SMS Device"
    ) -> str:
        """Set up SMS MFA for a user.





        Args:


            user_id: User ID


            phone_number: Phone number


            device_name: Device name





        Returns:


            Device ID


        """

        device_id = str(uuid4())

        device = MFADevice(
            device_id=device_id,
            user_id=user_id,
            device_type="sms",
            device_name=device_name,
            phone_number=phone_number,
            is_verified=False,
        )

        self._devices[device_id] = device

        return device_id

    async def verify_sms_setup(self, device_id: str, code_id: str, code: str) -> bool:
        """Verify SMS setup.





        Args:


            device_id: Device ID


            code_id: SMS code ID


            code: Verification code





        Returns:


            True if setup is verified


        """

        device = self._devices.get(device_id)

        if not device or device.device_type != "sms":
            return False

        if self.sms.verify_code(code_id, code):
            device.is_verified = True

            device.last_used = datetime.now(UTC)

            return True

        return False

    async def generate_backup_codes(self, user_id: str) -> list[str]:
        """Generate backup codes for a user.





        Args:


            user_id: User ID





        Returns:


            List of backup codes


        """

        codes = self.backup_codes.generate_backup_codes()

        backup_code_objects = []

        for code in codes:
            backup_code = BackupCode(
                code_id=str(uuid4()),
                user_id=user_id,
                code_hash=self.backup_codes.hash_backup_code(code),
            )

            backup_code_objects.append(backup_code)

        self._backup_codes[user_id] = backup_code_objects

        return codes

    async def verify_mfa(
        self,
        user_id: str,
        method: str,
        token: str,
        device_id: str | None = None,
        ip_address: str = "unknown",
        user_agent: str = "unknown",
    ) -> bool:
        """Verify MFA token.





        Args:


            user_id: User ID


            method: MFA method ("totp", "sms", "backup")


            token: Token/code to verify


            device_id: Device ID (for TOTP/SMS)


            ip_address: Client IP address


            user_agent: Client user agent





        Returns:


            True if verification successful


        """

        attempt_id = str(uuid4())

        success = False

        error_message = None

        try:
            if method == "totp" and device_id:
                device = self._devices.get(device_id)

                if device and device.device_type == "totp" and device.is_verified:
                    secret = self.field_encryption.decrypt(device.secret_key)

                    success = self.totp.verify_totp(secret, token)

                    if success:
                        device.last_used = datetime.now(UTC)

            elif method == "backup":
                user_backup_codes = self._backup_codes.get(user_id, [])

                for backup_code in user_backup_codes:
                    if not backup_code.is_used:
                        if self.backup_codes.verify_backup_code(
                            token, backup_code.code_hash
                        ):
                            backup_code.is_used = True

                            backup_code.used_at = datetime.now(UTC)

                            success = True

                            break

            else:
                error_message = f"Unsupported MFA method: {method}"

        except Exception as e:
            logger.error(f"MFA verification error: {e}")

            error_message = str(e)

        # Log attempt

        attempt = MFAAttempt(
            attempt_id=attempt_id,
            user_id=user_id,
            device_id=device_id,
            method=method,
            success=success,
            ip_address=ip_address,
            user_agent=user_agent,
            error_message=error_message,
        )

        self._attempts.append(attempt)

        return success

    def get_user_devices(self, user_id: str) -> list[MFADevice]:
        """Get all MFA devices for a user.





        Args:


            user_id: User ID





        Returns:


            List of user's MFA devices


        """

        return [
            device for device in self._devices.values() if device.user_id == user_id
        ]

    def is_mfa_required(self, user_id: str, user_roles: list[str]) -> bool:
        """Check if MFA is required for a user.





        Args:


            user_id: User ID


            user_roles: User's roles





        Returns:


            True if MFA is required


        """

        if self.config.require_mfa_for_admin and "admin" in user_roles:
            return True

        # Add other MFA requirement logic here

        return False

    def get_mfa_status(self, user_id: str) -> dict[str, Any]:
        """Get MFA status for a user.





        Args:


            user_id: User ID





        Returns:


            MFA status information


        """

        devices = self.get_user_devices(user_id)

        verified_devices = [d for d in devices if d.is_verified]

        has_backup_codes = user_id in self._backup_codes

        return {
            "has_mfa": len(verified_devices) > 0,
            "total_devices": len(devices),
            "verified_devices": len(verified_devices),
            "has_backup_codes": has_backup_codes,
            "devices": [
                {
                    "device_id": d.device_id,
                    "device_type": d.device_type,
                    "device_name": d.device_name,
                    "is_verified": d.is_verified,
                    "is_primary": d.is_primary,
                    "last_used": d.last_used,
                }
                for d in devices
            ],
        }


# Factory functions


def create_mfa_manager(config: MFAConfig | None = None) -> MFAManager:
    """Create MFA manager instance.





    Args:


        config: Optional MFA configuration





    Returns:


        MFAManager instance


    """

    return MFAManager(config)


def create_mfa_config(
    totp_issuer: str = "ZETA AI", require_mfa_for_admin: bool = True, **kwargs
) -> MFAConfig:
    """Create MFA configuration.





    Args:


        totp_issuer: TOTP issuer name


        require_mfa_for_admin: Require MFA for admin users


        **kwargs: Additional configuration options





    Returns:


        MFA configuration


    """

    return MFAConfig(
        totp_issuer=totp_issuer, require_mfa_for_admin=require_mfa_for_admin, **kwargs
    )
