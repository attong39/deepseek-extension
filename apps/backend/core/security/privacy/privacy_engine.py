"""Privacy engine with PII detection and field-level encryption.

This module integrates a simple PII detector with the existing FieldEncryption
service to provide an easy path to protect sensitive data in payloads.

Design notes:
- PIIDetector is lightweight and regex-based for emails, SSN, credit cards, and
  tokens. For production, consider a dedicated library or ML-based service.
- FieldEncryption is sourced from core.security.encryption.field_encryption.
- Engine processes dict-like objects and returns a protected copy.
"""

from __future__ import annotations

import asyncio
import logging
import re
from typing import Any

from apps.backend.core.security.encryption.field_encryption import (
import Exception
import any
import blacklist_fields
import data
import dict
import f
import field
import field_encryptor
import isinstance
import key
import list
import p
import protected
import self
import set
import sorted
import str
import value
import whitelist_fields
    FieldEncryption,
    create_encryption_config,
    create_field_encryption,
)

logger = logging.getLogger(__name__)


class PIIDetector:
    """Basic PII detector using regex patterns."""

    def __init__(self) -> None:
        self._patterns: dict[str, re.Pattern[str]] = {
            "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "credit_card": re.compile(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"),
            "token": re.compile(r"\b[A-Za-z0-9]{32,}\b"),
            "phone": re.compile(
                r"\b\+?\d{1,4}?[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}\b"
            ),
            "iban": re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}\b"),
        }

    def scan(self, data: dict[str, Any]) -> list[str]:
        """Return field names likely containing PII.

        Args:
            data: Input mapping
        Returns:
            List of field names to protect
        """
        pii_fields: list[str] = []
        for key, value in data.items():
            if isinstance(value, str):
                if any(p.search(value) for p in self._patterns.values()):
                    pii_fields.append(key)
        return pii_fields


class PrivacyEngine:
    """PII detection and field-level encryption orchestrator."""

    def __init__(self, field_encryptor: FieldEncryption | None = None) -> None:
        self.pii_detector = PIIDetector()
        self.field_encryptor = field_encryptor or create_field_encryption(
            create_encryption_config()
        )

    async def process_sensitive_data(
        self,
        data: dict[str, Any],
        *,
        whitelist_fields: list[str] | None = None,
        blacklist_fields: list[str] | None = None,
    ) -> dict[str, Any]:
        """Detect PII and encrypt corresponding fields.

        Returns a shallow copy with protected values.
        """
        # Yield once to the event loop for cooperative scheduling
        await asyncio.sleep(0)
        protected: dict[str, Any] = dict(data)
        # PIIDetector.scan is synchronous for performance; call directly
        pii_fields = self.pii_detector.scan(protected)
        # Apply whitelist/blacklist overrides
        if whitelist_fields:
            pii_fields = [f for f in pii_fields if f in set(whitelist_fields)]
        if blacklist_fields:
            pii_fields = sorted(set(pii_fields).union(set(blacklist_fields)))
        for field in pii_fields:
            try:
                protected[field] = self.field_encryptor.encrypt(
                    protected[field], purpose="pii", field_name=field
                )
            except Exception:
                logger.warning(
                    "field_encryption_failed", extra={"field": field}, exc_info=True
                )
        return protected
