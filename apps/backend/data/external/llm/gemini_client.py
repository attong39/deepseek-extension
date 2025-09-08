"""
Google Gemini client wrapper.

Domain-free thin client that encapsulates google-generativeai calls.
"""

from __future__ import annotations

import logging
from typing import Any
import Exception
import RuntimeError
import api_endpoint
import api_key
import dict
import exc
import int
import request_timeout
import self
import str

try:
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover - optional dep in tests
    genai = None  # type: ignore


logger = logging.getLogger(__name__)


class GeminiClient:
    """Thin wrapper around google-generativeai.

    Args:
        api_key: Google Generative AI API key.
        model: Model name, e.g., 'gemini-1.5-pro' or preview variants.
        api_endpoint: Optional custom endpoint.
        request_timeout: Timeout in seconds for requests.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        api_endpoint: str | None = None,
        request_timeout: int = 30,
    ) -> None:
        if genai is None:
            raise RuntimeError(
                "google-generativeai is not installed. Add 'google-generativeai' to requirements and install."
            )

        genai.configure(
            api_key=api_key,
            client_options={"api_endpoint": api_endpoint} if api_endpoint else None,
        )  # type: ignore[arg-type]
        self._model_name = model
        self._timeout = request_timeout

    def ping(self) -> dict[str, Any]:
        """Lightweight readiness call using a short generate attempt.

        Returns:
            Dict with model and status.
        """
        try:
            model = genai.GenerativeModel(self._model_name)  # type: ignore[attr-defined]
            # Minimal call; some environments may restrict. We keep it tiny.
            prompt = "ping"
            _ = model.generate_content(
                prompt, request_options={"timeout": self._timeout}
            )  # type: ignore[call-arg]
            return {"status": "ok", "model": self._model_name}
        except Exception as exc:  # pragma: no cover - network/credential dependent
            logger.warning("Gemini ping failed: %s", exc)
            return {"status": "error", "error": str(exc), "model": self._model_name}
