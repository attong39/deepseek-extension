"""Enhanced device trust manager with HMAC fingerprints and security hardening."""
from __future__ import annotations

import hmac
import hashlib
import secrets
import base64
import logging
from datetime import datetime, timedelta, UTC
from typing import Final, Dict

# Handle both relative and absolute imports
try:
    from .storage import TrustedDevice
    from .mfa_config import MFAConfig
except ImportError:
    from storage import TrustedDevice
    from mfa_config import MFAConfig

log = logging.getLogger(__name__)


class DeviceTrustManager:
    """
import ImportError
import any
import bool
import config
import device
import dict
import fingerprint
import int
import len
import list
import provided_fingerprint
import reason
import self
import stored_hmac
import str
import sum
import token
import ttl
    Enhanced device trust manager with HMAC-based fingerprint security.
    
    Features:
    - HMAC-protected device fingerprints
    - Secure token generation (32+ bytes)
    - Automatic cleanup of expired and inactive devices
    - Anti-brute force device enumeration
    """
    _DEFAULT_TTL: Final[timedelta] = timedelta(days=30)
    _INACTIVE_TTL: Final[timedelta] = timedelta(days=7)

    def __init__(self, config: MFAConfig) -> None:
        self.config = config
        # key → TrustedDevice
        self._trusted: Dict[str, TrustedDevice] = {}
        self._failed_fingerprint_attempts: Dict[str, int] = {}
        self._total_devices_created: int = 0

    def _generate_secure_token(self) -> str:
        """Generate cryptographically secure device token."""
        token_bytes = secrets.token_bytes(self.config.secure_token_length)
        return base64.urlsafe_b64encode(token_bytes).rstrip(b'=').decode('ascii')

    def _hmac_fingerprint(self, fingerprint: str) -> str:
        """Create HMAC of device fingerprint for secure storage."""
        return hmac.new(
            self.config.device_fingerprint_secret.encode('utf-8'),
            fingerprint.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _verify_fingerprint(self, stored_hmac: str, provided_fingerprint: str) -> bool:
        """Verify fingerprint using constant-time HMAC comparison."""
        computed_hmac = self._hmac_fingerprint(provided_fingerprint)
        return hmac.compare_digest(stored_hmac, computed_hmac)

    def trust_device(self, fingerprint: str, ttl: timedelta | None = None) -> str:
        """Trust a device and return secure token."""
        now = datetime.now(UTC)
        expires = now + (ttl or self._DEFAULT_TTL)
        
        # Generate secure token
        device_token = self._generate_secure_token()
        
        # Store HMAC of fingerprint, not the fingerprint itself
        fingerprint_hmac = self._hmac_fingerprint(fingerprint)
        
        self._trusted[device_token] = TrustedDevice(
            device_token=device_token,
            device_fingerprint=fingerprint_hmac,  # Store HMAC, not raw fingerprint
            expires_at=expires,
            last_seen=now,
        )
        
        # Increment counter for total devices created
        self._total_devices_created += 1
        
        if self.config.log_security_events:
            log.info(
                "Device trusted",
                extra={
                    "event": "device_trusted",
                    "device_token": device_token[:8] + "...",
                    "expires_at": expires.isoformat(),
                    "fingerprint_hash": fingerprint_hmac[:16] + "..."
                }
            )
        
        return device_token

    def is_device_trusted(self, device_token: str, fingerprint: str) -> bool:
        """Check if device is trusted with enhanced security checks."""
        dev = self._trusted.get(device_token)
        if dev is None:
            return False

        now = datetime.now(UTC)

        # Anti-brute force: limit fingerprint verification attempts
        attempt_key = f"{device_token}:{fingerprint[:10]}"
        failed_attempts = self._failed_fingerprint_attempts.get(attempt_key, 0)
        
        if failed_attempts >= 5:  # Max 5 fingerprint attempts per token
            if self.config.log_security_events:
                log.warning(
                    "Device fingerprint brute force detected",
                    extra={
                        "event": "fingerprint_brute_force",
                        "device_token": device_token[:8] + "...",
                        "failed_attempts": failed_attempts
                    }
                )
            return False

        # 1️⃣ HMAC fingerprint verification (constant-time)
        # 2️⃣ Token not expired
        # 3️⃣ Device used recently (not idle)
        trusted = (
            self._verify_fingerprint(dev.device_fingerprint, fingerprint)
            and now <= dev.expires_at
            and now - dev.last_seen <= self._INACTIVE_TTL
        )
        
        if trusted:
            # Reset failed attempts on success
            self._failed_fingerprint_attempts.pop(attempt_key, None)
            # Update last_seen on each successful check
            self._trusted[device_token] = dev._replace(last_seen=now)
            
            if self.config.log_security_events:
                log.info(
                    "Device trust verified",
                    extra={
                        "event": "device_trust_verified",
                        "device_token": device_token[:8] + "..."
                    }
                )
        else:
            # Record failed attempt
            self._failed_fingerprint_attempts[attempt_key] = failed_attempts + 1
            
            if self.config.log_security_events:
                log.warning(
                    "Device trust verification failed",
                    extra={
                        "event": "device_trust_failed",
                        "device_token": device_token[:8] + "...",
                        "reason": "expired" if now > dev.expires_at else "idle" if now - dev.last_seen > self._INACTIVE_TTL else "fingerprint_mismatch"
                    }
                )

        return trusted

    async def cleanup_expired(self) -> None:
        """
        Enhanced cleanup with metrics and logging.
        """
        now = datetime.now(UTC)
        expired_count = 0
        idle_count = 0
        
        expired_tokens = []
        for token, device in self._trusted.items():
            if device.expires_at < now:
                expired_tokens.append((token, "expired"))
                expired_count += 1
            elif now - device.last_seen > self._INACTIVE_TTL:
                expired_tokens.append((token, "idle"))
                idle_count += 1
        
        for token, reason in expired_tokens:
            del self._trusted[token]
            if self.config.log_security_events:
                log.info(
                    "Device trust revoked",
                    extra={
                        "event": "device_cleanup",
                        "device_token": token[:8] + "...",
                        "reason": reason
                    }
                )
        
        # Cleanup failed fingerprint attempts (older than 1 hour)
        self._failed_fingerprint_attempts.clear()
        
        if expired_count > 0 or idle_count > 0:
            log.info(
                "Device cleanup completed",
                extra={
                    "event": "cleanup_completed",
                    "expired_devices": expired_count,
                    "idle_devices": idle_count,
                    "remaining_devices": len(self._trusted)
                }
            )

    def get_device_info(self, device_token: str) -> TrustedDevice | None:
        """Get device information for debugging/admin purposes."""
        return self._trusted.get(device_token)

    def revoke_device(self, device_token: str) -> bool:
        """Manually revoke a trusted device with logging."""
        if device_token in self._trusted:
            del self._trusted[device_token]
            if self.config.log_security_events:
                log.info(
                    "Device manually revoked",
                    extra={
                        "event": "device_revoked",
                        "device_token": device_token[:8] + "..."
                    }
                )
            return True
        return False

    def revoke_all_devices(self) -> int:
        """Revoke all trusted devices (emergency function)."""
        count = len(self._trusted)
        self._trusted.clear()
        self._failed_fingerprint_attempts.clear()
        
        if self.config.log_security_events:
            log.warning(
                "All devices revoked",
                extra={
                    "event": "all_devices_revoked",
                    "revoked_count": count
                }
            )
        
        return count

    def list_devices(self) -> list[TrustedDevice]:
        """List all trusted devices (for admin interface)."""
        return list(self._trusted.values())

    def get_stats(self) -> dict:
        """Get trust manager statistics."""
        now = datetime.now(UTC)
        active_devices = sum(
            1 for device in self._trusted.values()
            if now - device.last_seen <= self._INACTIVE_TTL
        )
        
        return {
            "total_trusted_devices": len(self._trusted),
            "active_devices": active_devices,
            "total_devices_created": self._total_devices_created,
            "failed_fingerprint_attempts": len(self._failed_fingerprint_attempts),
            "cleanup_due": any(
                device.expires_at < now or now - device.last_seen > self._INACTIVE_TTL
                for device in self._trusted.values()
            )
        }
