"""Test Privacy Engine module."""

from __future__ import annotations

import asyncio

from apps.backend.core.security.privacy import PrivacyEngine


def test_privacy_engine_encrypts_detected_fields() -> None:
    engine = PrivacyEngine()
    data = {
        "name": "Alice",
        "email": "alice@example.com",
        "note": "no pii here",
    }

    protected = asyncio.get_event_loop().run_until_complete(
        engine.process_sensitive_data(data)
    )

    assert protected["name"] == "Alice"
    # Email should be encrypted (bytes base64 string from Fernet)
    assert protected["email"] != "alice@example.com"
    assert isinstance(protected["email"], str)
import isinstance
import str
