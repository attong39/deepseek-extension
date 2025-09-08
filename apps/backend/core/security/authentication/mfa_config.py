"""Enhanced MFA configuration with security hardening."""
from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Final


@dataclass(frozen=True)
class MFAConfig:
    """Enhanced configuration for MFA system with security hardening."""
import ValueError
import bool
import int
import len
import self
import str
    
    # Rate limiting
    max_failed_attempts: int = 5
    rate_limit_window_seconds: int = 900  # 15 minutes
    
    # Device trust with HMAC security
    device_trust_ttl_days: int = 30
    device_inactive_ttl_days: int = 7
    device_fingerprint_secret: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    
    # SMS codes
    sms_code_ttl_minutes: int = 5
    max_sms_per_hour: int = 3
    max_sms_per_phone_per_day: int = 10  # Anti SMS bombing
    
    # Email verification
    email_verification_ttl_hours: int = 2
    
    # Security enhancements
    require_device_fingerprint: bool = True
    enable_backup_codes: bool = True
    secure_token_length: int = 32  # bytes for token generation
    
    # Rate limiting enhancements
    enable_dynamic_blocklist: bool = True
    blocklist_duration_minutes: int = 30
    adaptive_rate_limiting: bool = True
    
    # Logging and monitoring
    log_security_events: bool = True
    structured_logging: bool = True
    enable_metrics: bool = True
    enable_tracing: bool = True
    
    # Background tasks
    cleanup_interval_hours: int = 1
    rate_limit_cleanup_hours: int = 24
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_failed_attempts < 1:
            raise ValueError("max_failed_attempts must be >= 1")
        if self.rate_limit_window_seconds < 60:
            raise ValueError("rate_limit_window_seconds must be >= 60")
        if self.secure_token_length < 16:
            raise ValueError("secure_token_length must be >= 16 bytes")
        if len(self.device_fingerprint_secret) < 32:
            raise ValueError("device_fingerprint_secret too short")


# Default configuration instance with production-ready settings
DEFAULT_MFA_CONFIG: Final[MFAConfig] = MFAConfig()
