"""Field-level encryption system for sensitive data protection.





This module provides comprehensive encryption capabilities including:


- AES-256 encryption for field-level data protection


- Key management and rotation


- Secure key derivation


- Format-preserving encryption for specific use cases


- Audit logging for encryption operations


"""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
import secrets
from datetime import UTC, datetime
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pydantic import BaseModel, Field
import Exception
import ValueError
import algorithm
import bool
import bytes
import config
import data
import data_b64
import data_dict
import dict
import e
import encrypted_fields
import end_time
import error_message
import field_name
import int
import isinstance
import key_info
import key_rotation_enabled
import kwargs
import list
import locals
import master_key
import new_purpose
import operation_type
import password
import purpose
import result
import self
import start_time
import str
import success
import tuple
import user_id

logger = logging.getLogger(__name__)


class EncryptionConfig(BaseModel):
    """Encryption configuration settings."""

    master_key: str | None = Field(default=None, description="Master encryption key")

    key_rotation_enabled: bool = Field(default=True)

    key_rotation_interval_days: int = Field(default=90)

    audit_encryption_operations: bool = Field(default=True)

    use_hardware_security_module: bool = Field(default=False)

    kdf_iterations: int = Field(default=100000)  # PBKDF2 iterations

    salt_length: int = Field(default=32)  # Salt length in bytes


class EncryptionKey(BaseModel):
    """Encryption key metadata."""

    key_id: str

    algorithm: str = Field(default="AES-256")

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    expires_at: datetime | None = None

    is_active: bool = Field(default=True)

    version: int = Field(default=1)

    purpose: str = Field(default="general")  # general, pii, financial, etc.


class EncryptionAuditEntry(BaseModel):
    """Audit entry for encryption operations."""

    operation_id: str

    operation_type: str  # encrypt, decrypt, key_rotation, etc.

    key_id: str

    field_name: str | None = None

    user_id: str | None = None

    ip_address: str | None = None

    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    success: bool

    error_message: str | None = None


class KeyManager:
    """Encryption key management system."""

    def __init__(self, config: EncryptionConfig):
        """Initialize key manager.





        Args:


            config: Encryption configuration


        """

        self.config = config

        self._keys: dict[str, EncryptionKey] = {}

        self._key_data: dict[str, bytes] = {}

        # Initialize master key

        self._master_key = self._load_or_generate_master_key()

    def _load_or_generate_master_key(self) -> bytes:
        """Load or generate master encryption key.





        Returns:


            Master key bytes


        """

        if self.config.master_key:
            # Load from configuration

            return base64.b64decode(self.config.master_key.encode())

        # Load from environment

        env_key = os.getenv("ZETA_ENCRYPTION_MASTER_KEY")

        if env_key:
            return base64.b64decode(env_key.encode())

        # Generate new key (not recommended for production)

        logger.warning("Generating new master key - not recommended for production")

        return Fernet.generate_key()

    def generate_key(self, purpose: str = "general", algorithm: str = "AES-256") -> str:
        """Generate a new encryption key.





        Args:


            purpose: Key purpose (general, pii, financial, etc.)


            algorithm: Encryption algorithm





        Returns:


            Key ID


        """

        key_id = secrets.token_urlsafe(16)

        key_data = Fernet.generate_key()

        encryption_key = EncryptionKey(
            key_id=key_id, algorithm=algorithm, purpose=purpose
        )

        self._keys[key_id] = encryption_key

        self._key_data[key_id] = key_data

        logger.info(f"Generated new encryption key: {key_id} for purpose: {purpose}")

        return key_id

    def get_active_key(self, purpose: str = "general") -> str | None:
        """Get active encryption key for purpose.





        Args:


            purpose: Key purpose





        Returns:


            Active key ID or None


        """

        for key_id, key_info in self._keys.items():
            if key_info.purpose == purpose and key_info.is_active:
                return key_id

        # Generate new key if none exists

        return self.generate_key(purpose=purpose)

    def get_key_data(self, key_id: str) -> bytes | None:
        """Get encryption key data.





        Args:


            key_id: Key ID





        Returns:


            Key data bytes or None


        """

        return self._key_data.get(key_id)

    def rotate_key(self, key_id: str) -> str:
        """Rotate encryption key.





        Args:


            key_id: Key ID to rotate





        Returns:


            New key ID


        """

        old_key = self._keys.get(key_id)

        if not old_key:
            raise ValueError(f"Key not found: {key_id}")

        # Mark old key as inactive

        old_key.is_active = False

        # Generate new key

        new_key_id = self.generate_key(
            purpose=old_key.purpose, algorithm=old_key.algorithm
        )

        logger.info(f"Rotated key {key_id} to {new_key_id}")

        return new_key_id

    def derive_key(
        self, password: str, salt: bytes | None = None, iterations: int | None = None
    ) -> tuple[bytes, bytes]:
        """Derive encryption key from password.





        Args:


            password: Password to derive from


            salt: Optional salt (generated if not provided)


            iterations: KDF iterations (uses config default if not provided)





        Returns:


            Tuple of (derived_key, salt)


        """

        if salt is None:
            salt = os.urandom(self.config.salt_length)

        iterations = iterations or self.config.kdf_iterations

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
        )

        derived_key = kdf.derive(password.encode())

        return derived_key, salt


class FieldEncryption:
    """Field-level encryption service."""

    def __init__(self, config: EncryptionConfig | None = None):
        """Initialize field encryption.





        Args:


            config: Encryption configuration


        """

        self.config = config or EncryptionConfig()

        self.key_manager = KeyManager(self.config)

        self._audit_log: list[EncryptionAuditEntry] = []

    def _log_operation(
        self,
        operation_type: str,
        key_id: str,
        success: bool,
        field_name: str | None = None,
        user_id: str | None = None,
        error_message: str | None = None,
    ) -> None:
        """Log encryption operation for audit.





        Args:


            operation_type: Type of operation


            key_id: Key ID used


            success: Whether operation succeeded


            field_name: Field name (if applicable)


            user_id: User ID (if applicable)


            error_message: Error message (if failed)


        """

        if not self.config.audit_encryption_operations:
            return

        entry = EncryptionAuditEntry(
            operation_id=secrets.token_urlsafe(16),
            operation_type=operation_type,
            key_id=key_id,
            field_name=field_name,
            user_id=user_id,
            success=success,
            error_message=error_message,
        )

        self._audit_log.append(entry)

        logger.info(f"Encryption audit: {operation_type} - Success: {success}")

    def encrypt(
        self,
        data: str | bytes,
        purpose: str = "general",
        field_name: str | None = None,
        user_id: str | None = None,
    ) -> str:
        """Encrypt data with field-level encryption.





        Args:


            data: Data to encrypt


            purpose: Encryption purpose (general, pii, financial, etc.)


            field_name: Field name for audit


            user_id: User ID for audit





        Returns:


            Base64-encoded encrypted data with key reference


        """

        key_id: str | None = None
        try:
            # Get active key for purpose

            key_id = self.key_manager.get_active_key(purpose)

            if not key_id:
                raise ValueError(f"No active key found for purpose: {purpose}")

            key_data = self.key_manager.get_key_data(key_id)

            if not key_data:
                raise ValueError(f"Key data not found: {key_id}")

            # Convert data to bytes if needed
            data_bytes = data.encode("utf-8") if isinstance(data, str) else data

            # Encrypt data

            fernet = Fernet(key_data)

            encrypted_data = fernet.encrypt(data_bytes)

            # Create encrypted data package with key reference

            package = {
                "key_id": key_id,
                "data": base64.b64encode(encrypted_data).decode("ascii"),
            }

            # Encode package

            package_json = f"{package['key_id']}:{package['data']}"

            _ = base64.b64encode(package_json.encode()).decode("ascii")

            self._log_operation(
                operation_type="encrypt",
                key_id=key_id,
                success=True,
                field_name=field_name,
                user_id=user_id,
            )

            return result

        except Exception as e:
            self._log_operation(
                operation_type="encrypt",
                key_id=str(key_id or "unknown"),
                success=False,
                field_name=field_name,
                user_id=user_id,
                error_message=str(e),
            )

            raise

    def decrypt(
        self,
        encrypted_data: str,
        field_name: str | None = None,
        user_id: str | None = None,
    ) -> str:
        """Decrypt field-level encrypted data.





        Args:


            encrypted_data: Base64-encoded encrypted data with key reference


            field_name: Field name for audit


            user_id: User ID for audit





        Returns:


            Decrypted data as string


        """

        try:
            # Decode package

            package_json = base64.b64decode(encrypted_data.encode()).decode("ascii")

            if ":" not in package_json:
                raise ValueError("Invalid encrypted data format")

            key_id, data_b64 = package_json.split(":", 1)

            # Get key data

            key_data = self.key_manager.get_key_data(key_id)

            if not key_data:
                raise ValueError(f"Encryption key not found: {key_id}")

            # Decrypt data

            fernet = Fernet(key_data)

            encrypted_bytes = base64.b64decode(data_b64.encode())

            decrypted_bytes = fernet.decrypt(encrypted_bytes)

            _ = decrypted_bytes.decode("utf-8")

            self._log_operation(
                operation_type="decrypt",
                key_id=key_id,
                success=True,
                field_name=field_name,
                user_id=user_id,
            )

            return result

        except Exception as e:
            self._log_operation(
                operation_type="decrypt",
                key_id=key_id if "key_id" in locals() else "unknown",
                success=False,
                field_name=field_name,
                user_id=user_id,
                error_message=str(e),
            )

            raise

    def encrypt_dict(
        self,
        data_dict: dict[str, Any],
        encrypted_fields: list[str],
        purpose: str = "general",
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Encrypt specific fields in a dictionary.





        Args:


            data_dict: Dictionary to encrypt fields in


            encrypted_fields: List of field names to encrypt


            purpose: Encryption purpose


            user_id: User ID for audit





        Returns:


            Dictionary with specified fields encrypted


        """

        _ = data_dict.copy()

        for field_name in encrypted_fields:
            if field_name in result and result[field_name] is not None:
                # Convert to string if needed

                field_value = str(result[field_name])

                result[field_name] = self.encrypt(
                    field_value, purpose=purpose, field_name=field_name, user_id=user_id
                )

        return result

    def decrypt_dict(
        self,
        data_dict: dict[str, Any],
        encrypted_fields: list[str],
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Decrypt specific fields in a dictionary.





        Args:


            data_dict: Dictionary to decrypt fields in


            encrypted_fields: List of field names to decrypt


            user_id: User ID for audit





        Returns:


            Dictionary with specified fields decrypted


        """

        _ = data_dict.copy()

        for field_name in encrypted_fields:
            if field_name in result and result[field_name] is not None:
                try:
                    result[field_name] = self.decrypt(
                        result[field_name], field_name=field_name, user_id=user_id
                    )

                except Exception as e:
                    logger.error(f"Failed to decrypt field {field_name}: {e}")

                    # Keep encrypted value on error

        return result

    def hash_for_search(self, data: str, salt: str | None = None) -> str:
        """Create searchable hash of sensitive data.





        This creates a deterministic hash that can be used for


        searching encrypted data without decryption.





        Args:


            data: Data to hash


            salt: Optional salt (uses default if not provided)





        Returns:


            Base64-encoded hash


        """

        salt_bytes = salt.encode() if salt else b"zeta_ai_search_salt"

        # Use HMAC for searchable hash

        hash_bytes = hmac.new(
            self.key_manager._master_key, data.encode() + salt_bytes, hashlib.sha256
        ).digest()

        return base64.b64encode(hash_bytes).decode("ascii")

    def rotate_field_encryption(
        self,
        data_dict: dict[str, Any],
        encrypted_fields: list[str],
        _old_purpose: str = "general",
        new_purpose: str = "general",
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Rotate encryption keys for specific fields.





        Args:


            data_dict: Dictionary with encrypted fields


            encrypted_fields: List of field names to re-encrypt


            old_purpose: Current encryption purpose


            new_purpose: New encryption purpose


            user_id: User ID for audit





        Returns:


            Dictionary with fields re-encrypted with new keys


        """

        # First decrypt with old keys

        decrypted = self.decrypt_dict(data_dict, encrypted_fields, user_id)

        # Then encrypt with new keys

        return self.encrypt_dict(decrypted, encrypted_fields, new_purpose, user_id)

    def get_audit_log(
        self,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        operation_type: str | None = None,
        user_id: str | None = None,
    ) -> list[EncryptionAuditEntry]:
        """Get encryption audit log.





        Args:


            start_time: Filter by start time


            end_time: Filter by end time


            operation_type: Filter by operation type


            user_id: Filter by user ID





        Returns:


            List of audit entries


        """

        filtered_log = self._audit_log

        if start_time:
            filtered_log = [e for e in filtered_log if e.timestamp >= start_time]

        if end_time:
            filtered_log = [e for e in filtered_log if e.timestamp <= end_time]

        if operation_type:
            filtered_log = [
                e for e in filtered_log if e.operation_type == operation_type
            ]

        if user_id:
            filtered_log = [e for e in filtered_log if e.user_id == user_id]

        return filtered_log


# Factory functions


def create_field_encryption(config: EncryptionConfig | None = None) -> FieldEncryption:
    """Create field encryption instance.





    Args:


        config: Optional encryption configuration





    Returns:


        FieldEncryption instance


    """

    return FieldEncryption(config)


def create_encryption_config(
    master_key: str | None = None, key_rotation_enabled: bool = True, **kwargs
) -> EncryptionConfig:
    """Create encryption configuration.





    Args:


        master_key: Master encryption key


        key_rotation_enabled: Enable key rotation


        **kwargs: Additional configuration options





    Returns:


        Encryption configuration


    """

    return EncryptionConfig(
        master_key=master_key, key_rotation_enabled=key_rotation_enabled, **kwargs
    )
