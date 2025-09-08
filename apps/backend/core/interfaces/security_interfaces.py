"""Security interfaces.

This module defines abstract interfaces for security operations
including authentication, authorization, encryption, and audit.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import bool
import bytes
import dict
import float
import int
import list
import str
import tuple


class AuthenticationInterface(ABC):
    """Interface for authentication operations."""

    @abstractmethod
    async def authenticate_user(
        self,
        credentials: dict[str, str],
    ) -> dict[str, Any] | None:
        """Authenticate user with credentials.

        Args:
            credentials: User credentials (username, password, etc.).

        Returns:
            User information if authentication successful, None otherwise.
        """

    @abstractmethod
    async def validate_token(self, token: str) -> dict[str, Any] | None:
        """Validate authentication token.

        Args:
            token: Authentication token to validate.

        Returns:
            Token payload if valid, None otherwise.
        """

    @abstractmethod
    async def generate_token(
        self,
        user_info: dict[str, Any],
        expires_in: int | None = None,
    ) -> str:
        """Generate authentication token.

        Args:
            user_info: User information to encode in token.
            expires_in: Token expiration time in seconds.

        Returns:
            Generated authentication token.
        """

    @abstractmethod
    async def revoke_token(self, token: str) -> bool:
        """Revoke authentication token.

        Args:
            token: Token to revoke.

        Returns:
            True if revocation successful.
        """

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> str | None:
        """Refresh authentication token.

        Args:
            refresh_token: Refresh token.

        Returns:
            New access token if refresh successful.
        """


class AuthorizationInterface(ABC):
    """Interface for authorization operations."""

    @abstractmethod
    async def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
    ) -> bool:
        """Check if user has permission for action on resource.

        Args:
            user_id: User identifier.
            resource: Resource identifier.
            action: Action to perform.

        Returns:
            True if user has permission.
        """

    @abstractmethod
    async def grant_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        granted_by: str,
    ) -> bool:
        """Grant permission to user.

        Args:
            user_id: User identifier.
            resource: Resource identifier.
            action: Action to grant.
            granted_by: User granting the permission.

        Returns:
            True if permission granted successfully.
        """

    @abstractmethod
    async def revoke_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        revoked_by: str,
    ) -> bool:
        """Revoke permission from user.

        Args:
            user_id: User identifier.
            resource: Resource identifier.
            action: Action to revoke.
            revoked_by: User revoking the permission.

        Returns:
            True if permission revoked successfully.
        """

    @abstractmethod
    async def get_user_permissions(
        self,
        user_id: str,
    ) -> list[dict[str, str]]:
        """Get all permissions for user.

        Args:
            user_id: User identifier.

        Returns:
            List of user permissions.
        """

    @abstractmethod
    async def check_role(self, user_id: str, role: str) -> bool:
        """Check if user has specific role.

        Args:
            user_id: User identifier.
            role: Role to check.

        Returns:
            True if user has role.
        """


class EncryptionInterface(ABC):
    """Interface for encryption and decryption operations."""

    @abstractmethod
    async def encrypt_data(
        self,
        data: str | bytes,
        key_id: str | None = None,
    ) -> dict[str, Any]:
        """Encrypt data.

        Args:
            data: Data to encrypt.
            key_id: Optional encryption key identifier.

        Returns:
            Encryption result with encrypted data and metadata.
        """

    @abstractmethod
    async def decrypt_data(
        self,
        encrypted_data: dict[str, Any],
    ) -> str | bytes:
        """Decrypt data.

        Args:
            encrypted_data: Encrypted data with metadata.

        Returns:
            Decrypted data.
        """

    @abstractmethod
    async def generate_key(
        self,
        algorithm: str = "AES-256",
        key_id: str | None = None,
    ) -> str:
        """Generate encryption key.

        Args:
            algorithm: Encryption algorithm.
            key_id: Optional key identifier.

        Returns:
            Generated key identifier.
        """

    @abstractmethod
    async def rotate_key(self, key_id: str) -> str:
        """Rotate encryption key.

        Args:
            key_id: Key identifier to rotate.

        Returns:
            New key identifier.
        """

    @abstractmethod
    async def hash_data(
        self,
        data: str | bytes,
        algorithm: str = "SHA-256",
        salt: str | None = None,
    ) -> str:
        """Hash data.

        Args:
            data: Data to hash.
            algorithm: Hash algorithm.
            salt: Optional salt value.

        Returns:
            Hash digest.
        """


class DigitalSignatureInterface(ABC):
    """Interface for digital signature operations."""

    @abstractmethod
    async def sign_data(
        self,
        data: str | bytes,
        private_key_id: str,
    ) -> str:
        """Create digital signature for data.

        Args:
            data: Data to sign.
            private_key_id: Private key identifier.

        Returns:
            Digital signature.
        """

    @abstractmethod
    async def verify_signature(
        self,
        data: str | bytes,
        signature: str,
        public_key_id: str,
    ) -> bool:
        """Verify digital signature.

        Args:
            data: Original data.
            signature: Digital signature to verify.
            public_key_id: Public key identifier.

        Returns:
            True if signature is valid.
        """

    @abstractmethod
    async def generate_key_pair(
        self,
        algorithm: str = "RSA-2048",
    ) -> tuple[str, str]:
        """Generate public-private key pair.

        Args:
            algorithm: Key generation algorithm.

        Returns:
            Tuple of (public_key_id, private_key_id).
        """


class AuditInterface(ABC):
    """Interface for security audit operations."""

    @abstractmethod
    async def log_security_event(
        self,
        event_type: str,
        user_id: str | None,
        resource: str | None,
        action: str | None,
        result: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Log security event.

        Args:
            event_type: Type of security event.
            user_id: User involved in event.
            resource: Resource accessed.
            action: Action performed.
            result: Event result (success, failure, etc.).
            metadata: Additional event metadata.

        Returns:
            Audit log entry ID.
        """

    @abstractmethod
    async def get_audit_logs(
        self,
        user_id: str | None = None,
        resource: str | None = None,
        event_type: str | None = None,
        start_time: float | None = None,
        end_time: float | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Retrieve audit logs.

        Args:
            user_id: Filter by user ID.
            resource: Filter by resource.
            event_type: Filter by event type.
            start_time: Start time filter.
            end_time: End time filter.
            limit: Maximum number of logs.

        Returns:
            List of audit log entries.
        """

    @abstractmethod
    async def export_audit_logs(
        self,
        filters: dict[str, Any] | None = None,
        format_: str = "json",
    ) -> str:
        """Export audit logs.

        Args:
            filters: Optional filters to apply.
            format_: Export format (json, csv, etc.).

        Returns:
            Export file path or URL.
        """


class SessionManagementInterface(ABC):
    """Interface for session management operations."""

    @abstractmethod
    async def create_session(
        self,
        user_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Create user session.

        Args:
            user_id: User identifier.
            metadata: Optional session metadata.

        Returns:
            Session identifier.
        """

    @abstractmethod
    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get session information.

        Args:
            session_id: Session identifier.

        Returns:
            Session information or None if not found.
        """

    @abstractmethod
    async def update_session(
        self,
        session_id: str,
        updates: dict[str, Any],
    ) -> bool:
        """Update session information.

        Args:
            session_id: Session identifier.
            updates: Updates to apply.

        Returns:
            True if update successful.
        """

    @abstractmethod
    async def terminate_session(self, session_id: str) -> bool:
        """Terminate user session.

        Args:
            session_id: Session identifier.

        Returns:
            True if termination successful.
        """

    @abstractmethod
    async def get_active_sessions(
        self,
        user_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get active sessions.

        Args:
            user_id: Optional user filter.

        Returns:
            List of active sessions.
        """

    @abstractmethod
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions.

        Returns:
            Number of sessions cleaned up.
        """


class RateLimitingInterface(ABC):
    """Interface for rate limiting operations."""

    @abstractmethod
    async def check_rate_limit(
        self,
        identifier: str,
        limit_type: str,
        window_seconds: int,
        max_requests: int,
    ) -> dict[str, Any]:
        """Check if rate limit is exceeded.

        Args:
            identifier: Unique identifier (user, IP, etc.).
            limit_type: Type of rate limit.
            window_seconds: Time window in seconds.
            max_requests: Maximum requests in window.

        Returns:
            Rate limit status and remaining quota.
        """

    @abstractmethod
    async def record_request(
        self,
        identifier: str,
        limit_type: str,
    ) -> bool:
        """Record a request for rate limiting.

        Args:
            identifier: Unique identifier.
            limit_type: Type of rate limit.

        Returns:
            True if request recorded successfully.
        """

    @abstractmethod
    async def reset_rate_limit(
        self,
        identifier: str,
        limit_type: str,
    ) -> bool:
        """Reset rate limit for identifier.

        Args:
            identifier: Unique identifier.
            limit_type: Type of rate limit.

        Returns:
            True if reset successful.
        """


class SecurityScanningInterface(ABC):
    """Interface for security scanning operations."""

    @abstractmethod
    async def scan_vulnerabilities(
        self,
        target: str,
        scan_type: str,
    ) -> dict[str, Any]:
        """Scan for security vulnerabilities.

        Args:
            target: Target to scan (URL, file, etc.).
            scan_type: Type of security scan.

        Returns:
            Scan results with vulnerabilities found.
        """

    @abstractmethod
    async def validate_input(
        self,
        input_data: str,
        validation_rules: list[str],
    ) -> dict[str, Any]:
        """Validate input for security issues.

        Args:
            input_data: Input data to validate.
            validation_rules: List of validation rules.

        Returns:
            Validation results.
        """

    @abstractmethod
    async def check_malware(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        """Check file for malware.

        Args:
            file_path: Path to file to check.

        Returns:
            Malware scan results.
        """
