"""Security configuration for ZETA AI system.

This module provides security settings including authentication,
authorization, encryption, and security policies.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import bool
import float
import int
import list
import str


class SecuritySettings(BaseSettings):
    """Security configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # ignore unrelated env keys (avoid validation errors)
    )

    # JWT Settings
    jwt_secret_key: str = Field(default="your-secret-key-change-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    jwt_refresh_token_expire_days: int = Field(default=30)

    # Password Settings
    password_min_length: int = Field(default=8)
    password_require_uppercase: bool = Field(default=True)
    password_require_lowercase: bool = Field(default=True)
    password_require_numbers: bool = Field(default=True)
    password_require_symbols: bool = Field(default=True)

    # Rate Limiting
    rate_limit_requests_per_minute: int = Field(default=60)
    rate_limit_burst_size: int = Field(default=10)
    max_login_attempts: int = Field(default=5)
    account_lockout_duration: int = Field(default=900)  # 15 minutes

    # Session Management
    session_timeout_minutes: int = Field(default=60)
    session_refresh_threshold_minutes: int = Field(default=15)

    # CORS Settings
    cors_origins: list[str] = Field(default=["http://localhost:3000"])
    cors_methods: list[str] = Field(default=["GET", "POST", "PUT", "DELETE"])
    cors_headers: list[str] = Field(default=["*"])

    # Security Headers
    enable_csrf_protection: bool = Field(default=True)
    enable_xss_protection: bool = Field(default=True)
    enable_content_type_sniffing: bool = Field(default=False)
    max_request_size: int = Field(default=10485760)  # 10MB

    # API Security
    api_key_header_name: str = Field(default="X-API-Key")
    api_key_length: int = Field(default=32)
    api_key_expire_days: int = Field(default=365)

    # Encryption
    encryption_key_length: int = Field(default=32)
    encryption_algorithm: str = Field(default="aes-256-gcm")

    # Request signature (Zero-Trust)
    request_signature_header: str = Field(
        default="X-Request-Signature",
        description="Header name containing the HMAC signature",
    )
    request_signature_secret: str | None = Field(
        default=None, description="Shared secret for HMAC request signatures"
    )
    require_request_signature: bool = Field(
        default=False, description="Reject requests missing signature if True"
    )

    # Zero-Trust: internal lightweight rate limit toggle
    zero_trust_rate_limit_enabled: bool = Field(
        default=False,
        description=(
            "Enable small in-memory per-identity limiter inside ZeroTrustMiddleware. "
            "Disable to centralize throttling in the dedicated rate_limiting middleware."
        ),
    )

    # Zero-Trust + Security-AI integration (optional)
    ai_risk_enabled: bool = Field(
        default=False,
        description=(
            "Enable Security-AI risk scoring in ZeroTrustMiddleware (requires security-ai extras)."
        ),
    )
    ai_block_threshold: float = Field(
        default=0.95,
        description=(
            "If AI anomaly score >= this threshold, request is blocked with 403."
        ),
    )

    # Privacy defaults
    privacy_whitelist_fields: list[str] = Field(
        default=[],
        description=(
            "If non-empty, PrivacyEngine only considers these fields for encryption by default."
        ),
    )
    privacy_blacklist_fields: list[str] = Field(
        default=[],
        description=("Fields to always encrypt regardless of auto-detection."),
    )

    # Audit & Monitoring
    enable_audit_logging: bool = Field(default=True)
    enable_security_monitoring: bool = Field(default=True)
    suspicious_activity_threshold: int = Field(default=10)

    # OAuth Settings (optional)
    oauth_google_client_id: str | None = Field(default=None)
    oauth_google_client_secret: str | None = Field(default=None)
    oauth_github_client_id: str | None = Field(default=None)
    oauth_github_client_secret: str | None = Field(default=None)

    # Two-Factor Authentication
    enable_2fa: bool = Field(default=False)
    totp_issuer_name: str = Field(default="ZETA AI")
    totp_digits: int = Field(default=6)
    totp_period: int = Field(default=30)

    # IP Whitelist/Blacklist
    ip_whitelist: list[str] = Field(default=[])
    ip_blacklist: list[str] = Field(default=[])
    enable_ip_filtering: bool = Field(default=False)

    # Content Security Policy
    _CSP_SELF = "'self'"
    csp_default_src: str = Field(default=_CSP_SELF)
    csp_script_src: str = Field(default=f"{_CSP_SELF} 'unsafe-inline'")
    csp_style_src: str = Field(default=f"{_CSP_SELF} 'unsafe-inline'")
    csp_img_src: str = Field(default=f"{_CSP_SELF} data: https:")
    csp_font_src: str = Field(default=_CSP_SELF)
    csp_connect_src: str = Field(default=_CSP_SELF)


def get_security_settings() -> SecuritySettings:
    """Get security settings instance."""
    return SecuritySettings()


# Security constants
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
}

# Sensitive data patterns for detection
SENSITIVE_PATTERNS = [
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
    r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # Credit card
    r"\b[A-Za-z0-9]{32,}\b",  # Potential tokens/keys
]

# Common password patterns to reject
WEAK_PASSWORD_PATTERNS = [
    r"^123+",
    r"^password",
    r"^admin",
    r"^qwerty",
    r"^abc+",
    r"(.)\1{3,}",  # Repeated characters
]
