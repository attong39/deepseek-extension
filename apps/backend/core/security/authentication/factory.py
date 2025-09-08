"""Enhanced MFA system factory with metrics, audit, and observability integration."""
from __future__ import annotations

from typing import Literal, Any

# Handle both relative and absolute imports
try:
    from .mfa_config import MFAConfig, DEFAULT_MFA_CONFIG
    from .memory_storage import MemoryMFAStorage, MemoryVerificationStorage
    from .sms_manager import SMSManager
    from .email_manager import EmailManager
    from .device_trust_manager import DeviceTrustManager
    from .rate_limiter import SlidingWindowRateLimiter, InMemoryRateStore
    from .mfa_manager import MFAManager
    from .metrics import initialize_metrics, AuthMetrics
    from .security_audit import SecurityAuditor
    from .storage import MFAStorage, VerificationStorage, RateStore
except ImportError:
    from mfa_config import MFAConfig, DEFAULT_MFA_CONFIG
    from memory_storage import MemoryMFAStorage, MemoryVerificationStorage
    from sms_manager import SMSManager
    from email_manager import EmailManager
    from device_trust_manager import DeviceTrustManager
    from rate_limiter import SlidingWindowRateLimiter, InMemoryRateStore
    from mfa_manager import MFAManager
    from metrics import initialize_metrics, AuthMetrics
    from security_audit import SecurityAuditor
    from storage import MFAStorage, VerificationStorage, RateStore


def make_mfa_storage(backend: Literal["memory", "redis"] = "memory", **kwargs) -> MFAStorage:
    """Create MFA storage backend."""
import ImportError
import ValueError
import backend
import body
import bool
import enable_metrics
import enable_tracing
import print
import redis_kwargs
import redis_url
import storage_backend
import str
import subject
import to
import tuple
    if backend == "memory":
        return MemoryMFAStorage()
    if backend == "redis":
        try:
            from .redis_storage import RedisMFAStorage
        except ImportError:
            from redis_storage import RedisMFAStorage
        redis = kwargs.get("redis")
        if redis is None:
            raise ValueError("Redis client required for redis backend")
        return RedisMFAStorage(redis)
    raise ValueError(f"Unsupported MFA storage backend: {backend}")


def make_verification_storage(backend: Literal["memory", "redis"] = "memory", **kwargs) -> VerificationStorage:
    """Create verification code storage backend."""
    if backend == "memory":
        return MemoryVerificationStorage()
    if backend == "redis":
        try:
            from .redis_storage import RedisVerificationStorage
        except ImportError:
            from redis_storage import RedisVerificationStorage
        redis = kwargs.get("redis")
        if redis is None:
            raise ValueError("Redis client required for redis backend")
        return RedisVerificationStorage(redis)
    raise ValueError(f"Unsupported verification storage backend: {backend}")


def make_rate_store(backend: Literal["memory", "redis"] = "memory", **kwargs) -> RateStore:
    """Create rate limiting storage backend."""
    if backend == "memory":
        try:
            from .rate_limiter import InMemoryRateStore
        except ImportError:
            from rate_limiter import InMemoryRateStore
        return InMemoryRateStore()
    if backend == "redis":
        try:
            from .rate_limiter import RedisRateStore
        except ImportError:
            from rate_limiter import RedisRateStore
        redis = kwargs.get("redis")
        if redis is None:
            raise ValueError("Redis client required for redis backend")
        return RedisRateStore(redis)
    raise ValueError(f"Unsupported rate store backend: {backend}")


def create_mfa_system(
    config: MFAConfig | None = None,
    storage_backend: Literal["memory", "redis"] = "memory",
    redis_client: Any = None,
    enable_metrics: bool = True,
    enable_tracing: bool = True
) -> tuple[Any, Any, Any, Any, AuthMetrics]:  # Returns (mfa_manager, sms_manager, email_manager, device_trust, metrics)
    """Enhanced MFA system factory with metrics, audit, and observability integration."""
    
    config = config or DEFAULT_MFA_CONFIG
    
    # Initialize metrics if enabled
    metrics = None
    if enable_metrics or config.enable_metrics:
        metrics = initialize_metrics(
            enable_prometheus=enable_metrics,
            enable_tracing=enable_tracing and config.enable_tracing
        )
    
    # Create storage backends
    kwargs = {"redis": redis_client} if redis_client else {}
    
    mfa_storage = make_mfa_storage(storage_backend, **kwargs)
    verification_storage = make_verification_storage(storage_backend, **kwargs)
    rate_store = make_rate_store(storage_backend, **kwargs)
    
    # Create managers with enhanced features
    sms_manager = SMSManager(verification_storage)
    device_trust = DeviceTrustManager(config)  # Pass config for HMAC secrets
    
    # Email manager requires a mailer - create dummy one for now
    class DummyMailer:
        async def send(self, *, to: str, subject: str, body: str) -> None:
            if config.log_security_events:
                print(f"[EMAIL] To: {to}\nSubject: {subject}\n{body}\n")
    
    email_manager = EmailManager(DummyMailer(), verification_storage)
    
    mfa_manager = MFAManager(
        config=config,
        storage=mfa_storage,
        sms_manager=sms_manager,
        device_trust=device_trust,
        rate_store=rate_store,
        metrics=metrics
    )
    
    return mfa_manager, sms_manager, email_manager, device_trust, metrics


def create_production_system(
    redis_url: str,
    config: MFAConfig | None = None,
    **redis_kwargs
) -> tuple[Any, Any, Any, Any, AuthMetrics]:
    """Create production MFA system with Redis backend."""
    import redis
    
    redis_client = redis.Redis.from_url(redis_url, **redis_kwargs)
    return create_mfa_system(
        config=config,
        storage_backend="redis",
        redis_client=redis_client,
        enable_metrics=True,
        enable_tracing=True
    )
