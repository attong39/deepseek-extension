"""Enhanced MFA manager with metrics and advanced security features."""
from __future__ import annotations

import logging
from datetime import datetime, UTC
from typing import Dict, List

# Handle both relative and absolute imports
try:
    from .mfa_config import MFAConfig
    from .storage import MFAStorage, RateStore
    from .sms_manager import SMSManager
    from .device_trust_manager import DeviceTrustManager
    from .rate_limiter import SlidingWindowRateLimiter, InMemoryRateStore
    from .metrics import get_metrics, AuthMetrics
except ImportError:
    from mfa_config import MFAConfig
    from storage import MFAStorage, RateStore
    from sms_manager import SMSManager
    from device_trust_manager import DeviceTrustManager
    from rate_limiter import SlidingWindowRateLimiter, InMemoryRateStore
    from metrics import get_metrics, AuthMetrics

log = logging.getLogger(__name__)


class MFAManager:
    """Enhanced MFA manager with comprehensive security and observability."""
import Exception
import ImportError
import attempt
import bool
import config
import device_fingerprint
import device_trust
import dict
import e
import int
import len
import list
import phone
import rate_store
import self
import span
import str
import sum
import user_id
    
    def __init__(self,
                 config: MFAConfig,
                 storage: MFAStorage,
                 sms_manager: SMSManager,
                 device_trust: DeviceTrustManager,
                 *,
                 rate_store: RateStore | None = None,
                 metrics: AuthMetrics | None = None) -> None:
        self.config = config
        self.storage = storage
        self.sms = sms_manager
        self.trust = device_trust
        self._failed_attempts: Dict[str, List[datetime]] = {}
        self.metrics = metrics or get_metrics()

        # Enhanced rate limiting
        self._rate_limiter = SlidingWindowRateLimiter(
            store=rate_store or InMemoryRateStore(),
            max_requests=self.config.max_failed_attempts,
            window_seconds=self.config.rate_limit_window_seconds,
        )
        
        # SMS-specific rate limiter
        self._sms_rate_limiter = SlidingWindowRateLimiter(
            store=rate_store or InMemoryRateStore(),
            max_requests=self.config.max_sms_per_hour,
            window_seconds=3600  # 1 hour
        )
        
        # Daily SMS rate limiter (anti-SMS bombing)
        self._daily_sms_limiter = SlidingWindowRateLimiter(
            store=rate_store or InMemoryRateStore(),
            max_requests=self.config.max_sms_per_phone_per_day,
            window_seconds=86400  # 24 hours
        )

    async def verify_mfa(self, user_id: str, phone: str, code: str, 
                        device_token: str | None = None, 
                        device_fingerprint: str | None = None) -> bool:
        """Enhanced MFA verification with metrics and comprehensive security."""
        
        async with self.metrics.time_operation("mfa_verify") as span:
            # 1️⃣ Rate limit check
            if await self._rate_limiter.is_limited(user_id):
                self.metrics.increment_rate_limit_hit("user_attempts")
                self.metrics.increment_security_event("rate_limit_triggered", "medium")
                
                if self.config.log_security_events:
                    log.warning(
                        "MFA verification blocked by rate limiter",
                        extra={
                            "user_id": user_id, 
                            "event": "mfa_rate_limited",
                            "severity": "medium"
                        }
                    )
                return False

            # 2️⃣ Check if device is already trusted (skip MFA if so)
            if device_token and device_fingerprint:
                if self.trust.is_device_trusted(device_token, device_fingerprint):
                    self.metrics.increment_device_trust_event("bypass_mfa")
                    
                    if self.config.log_security_events:
                        log.info(
                            "MFA bypassed for trusted device",
                            extra={
                                "user_id": user_id, 
                                "device_token": device_token[:8] + "...", 
                                "event": "mfa_trusted_device"
                            }
                        )
                    return True

            # 3️⃣ Verify SMS code
            success = await self.sms.verify_code(phone, code)
            
            if success:
                self.metrics.increment_sms_verified("success")
            else:
                self.metrics.increment_sms_verified("failed")

            if not success:
                # Record failure for monitoring
                now = datetime.now(UTC)
                self._failed_attempts.setdefault(user_id, []).append(now)
                
                self.metrics.increment_security_event("mfa_verification_failed", "low")
                
                if self.config.log_security_events:
                    log.warning(
                        "MFA verification failed",
                        extra={
                            "user_id": user_id, 
                            "phone": phone[:3] + "***" + phone[-2:] if len(phone) > 5 else "***",
                            "event": "mfa_failed",
                            "attempts": len(self._failed_attempts.get(user_id, []))
                        }
                    )
            else:
                # Success! Reset counters and optionally trust device
                await self._rate_limiter.reset(user_id)
                self._failed_attempts.pop(user_id, None)
                
                # Trust device if token and fingerprint provided
                if device_token and device_fingerprint:
                    # Use existing token or generate new one
                    if not self.trust.get_device_info(device_token):
                        device_token = self.trust.trust_device(device_fingerprint)
                    self.metrics.increment_device_trust_event("device_trusted")
                
                self.metrics.increment_security_event("mfa_verification_success", "low")
                
                if self.config.log_security_events:
                    log.info(
                        "MFA verification successful",
                        extra={
                            "user_id": user_id,
                            "device_trusted": bool(device_token and device_fingerprint),
                            "event": "mfa_success"
                        }
                    )
            
            if span:
                span.set_attribute("mfa.success", success)
                span.set_attribute("mfa.user_id", user_id)
                span.set_attribute("mfa.device_trusted", bool(device_token and device_fingerprint))

            return success

    async def send_sms_code(self, user_id: str, phone: str) -> bool:
        """Enhanced SMS sending with anti-bombing protection."""
        
        async with self.metrics.time_operation("sms_send") as span:
            # Rate limit SMS sending (hourly)
            if await self._sms_rate_limiter.is_limited(f"sms:{phone}"):
                self.metrics.increment_rate_limit_hit("sms_hourly")
                self.metrics.increment_security_event("sms_rate_limited", "medium")
                
                if self.config.log_security_events:
                    log.warning(
                        "SMS sending rate limited (hourly)",
                        extra={"user_id": user_id, "phone": phone[:3] + "***", "event": "sms_rate_limited"}
                    )
                return False
            
            # Rate limit SMS sending (daily - anti-bombing)
            if await self._daily_sms_limiter.is_limited(f"daily_sms:{phone}"):
                self.metrics.increment_rate_limit_hit("sms_daily")
                self.metrics.increment_security_event("sms_bombing_detected", "high")
                
                if self.config.log_security_events:
                    log.error(
                        "SMS bombing detected - daily limit exceeded",
                        extra={"user_id": user_id, "phone": phone[:3] + "***", "event": "sms_bombing"}
                    )
                return False
            
            try:
                code = await self.sms.generate_code(phone)
                self.metrics.increment_sms_generated("success")
                
                if self.config.log_security_events:
                    log.info(
                        "SMS code generated", 
                        extra={
                            "user_id": user_id, 
                            "phone": phone[:3] + "***", 
                            "code_length": len(code),
                            "event": "sms_sent"
                        }
                    )
                
                if span:
                    span.set_attribute("sms.success", True)
                    span.set_attribute("sms.phone_masked", phone[:3] + "***")
                
                return True
                
            except Exception as e:
                self.metrics.increment_sms_generated("failed")
                self.metrics.increment_security_event("sms_send_failed", "medium")
                
                if self.config.log_security_events:
                    log.error(
                        "Failed to send SMS code",
                        extra={"user_id": user_id, "error": str(e), "event": "sms_failed"}
                    )
                
                if span:
                    span.set_attribute("sms.success", False)
                    span.set_attribute("sms.error", str(e))
                
                return False

    async def get_failed_attempts(self, user_id: str) -> int:
        """Get number of recent failed attempts for user."""
        attempts = self._failed_attempts.get(user_id, [])
        # Clean up old attempts (older than rate limit window)
        now = datetime.now(UTC)
        recent = [
            attempt for attempt in attempts 
            if (now - attempt).total_seconds() < self.config.rate_limit_window_seconds
        ]
        self._failed_attempts[user_id] = recent
        return len(recent)

    def revoke_device_trust(self, device_token: str) -> bool:
        """Revoke trust for a specific device with metrics."""
        success = self.trust.revoke_device(device_token)
        if success:
            self.metrics.increment_device_trust_event("device_revoked")
        return success
    
    def revoke_all_devices(self) -> int:
        """Revoke all trusted devices (emergency function)."""
        count = self.trust.revoke_all_devices()
        if count > 0:
            self.metrics.increment_device_trust_event("all_devices_revoked")
            self.metrics.increment_security_event("emergency_device_revocation", "high")
        return count

    async def cleanup_expired_data(self) -> None:
        """Enhanced cleanup with metrics tracking."""
        async with self.metrics.time_operation("cleanup_expired"):
            # Clean up expired trusted devices
            await self.trust.cleanup_expired()
            
            # Clean up old failed attempts
            now = datetime.now(UTC)
            cleaned_users = 0
            for user_id in list(self._failed_attempts.keys()):
                attempts = self._failed_attempts[user_id]
                recent = [
                    attempt for attempt in attempts 
                    if (now - attempt).total_seconds() < self.config.rate_limit_window_seconds
                ]
                if recent:
                    self._failed_attempts[user_id] = recent
                else:
                    del self._failed_attempts[user_id]
                    cleaned_users += 1
            
            # Update metrics
            self.metrics.set_active_devices(len(self.trust.list_devices()))
            self.metrics.set_failed_attempts_current(len(self._failed_attempts))
            
            if self.config.log_security_events:
                log.info(
                    "Cleanup completed",
                    extra={
                        "event": "cleanup_completed",
                        "cleaned_failed_attempts": cleaned_users,
                        "active_devices": len(self.trust.list_devices())
                    }
                )
    
    def get_security_stats(self) -> dict:
        """Get comprehensive security statistics."""
        device_stats = self.trust.get_stats()
        
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "failed_attempts_users": len(self._failed_attempts),
            "total_failed_attempts": sum(len(attempts) for attempts in self._failed_attempts.values()),
            "device_trust": device_stats,
            "rate_limiting": {
                "enabled": True,
                "max_failed_attempts": self.config.max_failed_attempts,
                "window_seconds": self.config.rate_limit_window_seconds,
                "sms_rate_limits": {
                    "hourly": self.config.max_sms_per_hour,
                    "daily": self.config.max_sms_per_phone_per_day
                }
            },
            "security_features": {
                "hmac_fingerprints": True,
                "constant_time_comparison": True,
                "secure_token_generation": True,
                "adaptive_rate_limiting": self.config.adaptive_rate_limiting,
                "dynamic_blocklist": self.config.enable_dynamic_blocklist
            }
        }
