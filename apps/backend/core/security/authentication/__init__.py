"""Production-ready authentication system with MFA, device trust, and rate limiting.

This module provides:
- Cryptographically secure OTP/SMS codes
- Device trust with expiration and cleanup
- Pluggable storage abstraction (memory ↔ Redis ↔ DB)
- Rate limiting and brute-force protection
- Email verification with tokens and backup codes
- Structured logging and monitoring
"""

from .storage import (
    VerificationStorage,
    MFAStorage,
    RateStore,
    MailerProtocol,
    SmsCode,
    EmailVerification,
    TrustedDevice,
)
from .sms_manager import SMSManager
from .email_manager import EmailManager
from .device_trust_manager import DeviceTrustManager
from .rate_limiter import (
    SlidingWindowRateLimiter,
    InMemoryRateStore,
    RedisRateStore,
)
from .mfa_manager import MFAManager
from .mfa_config import MFAConfig, DEFAULT_MFA_CONFIG
from .memory_storage import MemoryMFAStorage, MemoryVerificationStorage
from .redis_storage import RedisMFAStorage, RedisVerificationStorage
from .factory import (
    make_mfa_storage,
    make_verification_storage,
    make_rate_store,
    create_mfa_system,
)

__all__ = [
    # Storage protocols
    "VerificationStorage",
    "MFAStorage", 
    "RateStore",
    "MailerProtocol",
    # Data types
    "SmsCode",
    "EmailVerification",
    "TrustedDevice",
    # Core managers
    "SMSManager",
    "EmailManager", 
    "DeviceTrustManager",
    "MFAManager",
    # Rate limiting
    "SlidingWindowRateLimiter",
    "InMemoryRateStore",
    "RedisRateStore",
    # Configuration
    "MFAConfig",
    "DEFAULT_MFA_CONFIG",
    # Storage implementations
    "MemoryMFAStorage",
    "MemoryVerificationStorage",
    "RedisMFAStorage",
    "RedisVerificationStorage",
    # Factory functions
    "make_mfa_storage",
    "make_verification_storage",
    "make_rate_store",
    "create_mfa_system",
]
