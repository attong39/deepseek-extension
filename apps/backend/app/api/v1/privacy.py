"""API v1 - Privacy utilities endpoints.

Provides a sanitize endpoint that applies PrivacyEngine to request payloads,
performing PII detection and field-level encryption.
"""

from __future__ import annotations

import logging
from typing import Any

from apps.backend.core.security.privacy import PIIDetector, PrivacyEngine
from fastapi import APIRouter
from pydantic import BaseModel, Field
import dict
import list
import req
import str

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/privacy", tags=["Privacy", "v1"])


class SanitizeRequest(BaseModel):
    """Incoming payload to sanitize by encrypting detected PII fields."""

    payload: dict[str, Any] = Field(default_factory=dict)


class SanitizeResponse(BaseModel):
    """Sanitized payload and detected PII field names."""

    sanitized: dict[str, Any]
    pii_fields: list[str]


@router.post(
    "/sanitize",
    response_model=SanitizeResponse,
    summary="Sanitize payload (encrypt PII)",
)
async def sanitize_payload(req: SanitizeRequest) -> SanitizeResponse:
    """Detect and encrypt PII fields in payload.

    Returns the sanitized payload and the list of fields that matched PII patterns.
    """
    engine = PrivacyEngine()
    detector = PIIDetector()

    pii_fields = detector.scan(req.payload)
    sanitized = await engine.process_sensitive_data(req.payload)

    return SanitizeResponse(sanitized=sanitized, pii_fields=pii_fields)
