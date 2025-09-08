"""Application service for Google Gemini LLM.

This service bridges FastAPI/DI and the data external Gemini client.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any
import Exception
import bool
import client_provider
import dict
import exc
import self
import settings
import str

logger = logging.getLogger(__name__)


class GeminiService:
    """Facade service wrapping the data-layer Gemini client."""

    def __init__(
        self,
        settings: Any,
        client_provider: Callable[[], Any] | None = None,
    ) -> None:
        self._settings = settings
        self._client = None

        if self._settings.GEMINI_ENABLED and self._settings.GEMINI_API_KEY:
            try:
                self._client = client_provider() if client_provider else None
            except Exception as exc:  # pragma: no cover - optional dependency
                logger.warning("Gemini client not initialized: %s", exc)
                self._client = None

    def is_configured(self) -> bool:
        return bool(self._client)

    def ping(self) -> dict[str, Any]:
        if not self._client:
            return {
                "status": "disabled",
                "reason": "GEMINI_ENABLED is False or GEMINI_API_KEY missing",
            }
        return self._client.ping()
