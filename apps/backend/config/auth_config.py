import os
import bool
import int
import str

"""Authentication configuration for ZETA AI system.

This module provides authentication-specific settings including
JWT configuration, OAuth providers, and authentication policies.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    """Authentication configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # JWT Configuration
    jwt_secret_key: str = Field(default="change-this-secret-key-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=30)
    jwt_refresh_token_expire_minutes: int = Field(default=43200)  # 30 days
    jwt_issuer: str = Field(default="zeta-ai")
    jwt_audience: str = Field(default="zeta-ai-users")

    # Authentication Providers
    enable_local_auth: bool = Field(default=True)
    enable_oauth: bool = Field(default=False)
    enable_api_key_auth: bool = Field(default=True)

    # OAuth Providers
    oauth_google_enabled: bool = Field(default=False)
    oauth_google_client_id: str | None = Field(default=None)
    oauth_google_client_secret: str | None = Field(default=None)
    oauth_google_redirect_uri: str = Field(
        default="http://localhost:8000/auth/google/callback"
    )

    oauth_github_enabled: bool = Field(default=False)
    oauth_github_client_id: str | None = Field(default=None)
    oauth_github_client_secret: str | None = Field(default=None)
    oauth_github_redirect_uri: str = Field(
        default="http://localhost:8000/auth/github/callback"
    )

    oauth_microsoft_enabled: bool = Field(default=False)
    oauth_microsoft_client_id: str | None = Field(default=None)
    oauth_microsoft_client_secret: str | None = Field(default=None)
    oauth_microsoft_redirect_uri: str = Field(
        default="http://localhost:8000/auth/microsoft/callback"
    )

    # Multi-Factor Authentication
    enable_mfa: bool = Field(default=False)
    mfa_required_for_admin: bool = Field(default=True)
    totp_issuer: str = Field(default="ZETA AI")
    totp_period: int = Field(default=30)
    totp_digits: int = Field(default=6)
    totp_backup_codes_count: int = Field(default=10)

    # Password Policies
    password_min_length: int = Field(default=8)
    password_max_length: int = Field(default=128)
    password_require_uppercase: bool = Field(default=True)
    password_require_lowercase: bool = Field(default=True)
    password_require_numbers: bool = Field(default=True)
    password_require_special_chars: bool = Field(default=True)
    password_special_chars: str = Field(default="!@#$%^&*()_+-=[]{}|;:,.<>?")
    password_history_count: int = Field(default=5)  # Remember last N passwords
    password_expiry_days: int = Field(default=90)  # Password expires after N days

    # Account Security
    max_login_attempts: int = Field(default=5)
    account_lockout_duration_minutes: int = Field(default=15)
    failed_login_reset_time_minutes: int = Field(default=60)

    # Session Management
    session_timeout_minutes: int = Field(default=60)
    session_absolute_timeout_hours: int = Field(default=24)
    session_remember_me_days: int = Field(default=30)
    allow_concurrent_sessions: bool = Field(default=True)
    max_concurrent_sessions: int = Field(default=5)

    # API Key Authentication
    api_key_length: int = Field(default=32)
    api_key_prefix: str = Field(default="zeta_")
    api_key_expire_days: int = Field(default=365)
    api_key_rate_limit_requests_per_minute: int = Field(default=1000)

    # Email Verification
    require_email_verification: bool = Field(default=True)
    email_verification_expire_hours: int = Field(default=24)
    resend_verification_cooldown_minutes: int = Field(default=5)

    # Password Reset
    password_reset_expire_hours: int = Field(default=2)
    password_reset_cooldown_minutes: int = Field(default=5)
    password_reset_max_attempts: int = Field(default=3)

    # Registration Settings
    allow_registration: bool = Field(default=True)
    require_invitation: bool = Field(default=False)
    auto_activate_accounts: bool = Field(default=False)
    default_user_role: str = Field(default="user")

    # Token Blacklist
    enable_token_blacklist: bool = Field(default=True)
    token_blacklist_cleanup_interval_hours: int = Field(default=24)

    # Audit and Logging
    log_authentication_events: bool = Field(default=True)
    log_failed_attempts: bool = Field(default=True)
    log_password_changes: bool = Field(default=True)
    log_privilege_escalations: bool = Field(default=True)

    # Rate Limiting
    auth_rate_limit_requests_per_minute: int = Field(default=20)
    auth_rate_limit_burst: int = Field(default=5)
    registration_rate_limit_per_ip_per_hour: int = Field(default=3)

    # Device Management
    enable_device_tracking: bool = Field(default=True)
    max_devices_per_user: int = Field(default=10)
    device_token_expire_days: int = Field(default=30)
    require_device_verification: bool = Field(default=False)


def get_auth_settings() -> AuthSettings:
    """Get authentication settings instance."""
    return AuthSettings()


# JWT Token Types
class TokenType:
    """JWT token type constants."""

    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"
    api_key = os.getenv("API_KEY")


# Authentication Methods
class AuthMethod:
    """Authentication method constants."""

    password = os.getenv("PASSWORD")
    OAUTH_GOOGLE = "oauth_google"
    OAUTH_GITHUB = "oauth_github"
    OAUTH_MICROSOFT = "oauth_microsoft"
    api_key = os.getenv("API_KEY")
    MFA_TOTP = "mfa_totp"
    MFA_BACKUP_CODE = "mfa_backup_code"


# OAuth Scopes
OAUTH_SCOPES = {
    "google": [
        "openid",
        "email",
        "profile",
    ],
    "github": [
        "user:email",
        "read:user",
    ],
    "microsoft": [
        "openid",
        "email",
        "profile",
    ],
}

# Default permissions for new users
DEFAULT_PERMISSIONS = [
    "user:read_profile",
    "user:update_profile",
    "chat:create",
    "chat:read_own",
    "memory:create_own",
    "memory:read_own",
]
