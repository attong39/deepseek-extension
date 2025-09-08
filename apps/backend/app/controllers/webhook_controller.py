"""
Webhook Controller Module

This module provides the WebhookController class for orchestrating third-party
callback handling (e.g., Stripe, GitHub) via a service interface.

Author: duy_bg_vn
Layer: Controllers (Application Orchestration)
Responsibility:
    - Orchestrate use-cases across services/adapters
    - Keep controllers framework-agnostic (usable by API, CLI, WS)
    - No DB/HTTP here; call services in core/services via DI
"""

from __future__ import annotations

import logging
from typing import Any, Protocol
import Exception
import ValueError
import bool
import bytes
import data
import dict
import event
import exc
import headers
import isinstance
import payload
import provider
import self
import str
import webhook

logger = logging.getLogger("apps.backend.app.controllers.webhook_controller")


class WebhookService(Protocol):
    """
    Protocol for webhook service operations.

    Methods:
        verify: Verify webhook signature.
        handle: Handle webhook event.
    """

    async def verify(
        self, *, provider: str, headers: dict[str, Any], payload: bytes
    ) -> bool: ...
    async def handle(
        self, *, provider: str, event: str, data: dict[str, Any]
    ) -> dict[str, Any]: ...


class WebhookController:
    """
    Entry for third-party callbacks (Stripe/GitHub/etc.).

    Args:
        webhook (WebhookService): The webhook service implementation.

    Methods:
        process: Process incoming webhook request.
        dispatch: Dispatch webhook event to handler.
    """

    def __init__(self, webhook: WebhookService) -> None:
        """
        Initialize WebhookController.

        Args:
            webhook (WebhookService): The webhook service implementation.
        """
        self._wh = webhook

    async def process(
        self, provider: str, headers: dict[str, Any], payload: bytes
    ) -> dict[str, Any]:
        """
        Process incoming webhook request.

        Args:
            provider (str): Webhook provider name.
            headers (Dict[str, Any]): Request headers.
            payload (bytes): Raw request payload.

        Returns:
            Dict[str, Any]: Processing result.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(provider, str) or not provider.strip():
            logger.error("Invalid provider for process: %r", provider)
            raise ValueError("provider must be a non-empty string")
        if not isinstance(headers, dict):
            logger.error("Invalid headers for process: %r", headers)
            raise ValueError("headers must be a dict")
        if not isinstance(payload, bytes) or not payload:
            logger.error("Invalid payload for process: %r", payload)
            raise ValueError("payload must be non-empty bytes")
        try:
            verified = await self._wh.verify(
                provider=provider, headers=headers, payload=payload
            )
            if not verified:
                logger.warning("Invalid signature provider=%s", provider)
                return {"status": "error", "reason": "invalid_signature"}
            # TODO: Parse event+data from payload per provider spec
            logger.info("Webhook verified for provider=%s", provider)
            return {"status": "ok"}
        except Exception as exc:
            logger.exception("Failed to process webhook: provider=%s: %s", provider, exc)
            raise

    async def dispatch(
        self, provider: str, event: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Dispatch webhook event to handler.

        Args:
            provider (str): Webhook provider name.
            event (str): Event name.
            data (Dict[str, Any]): Event data.

        Returns:
            Dict[str, Any]: Handler result.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(provider, str) or not provider.strip():
            logger.error("Invalid provider for dispatch: %r", provider)
            raise ValueError("provider must be a non-empty string")
        if not isinstance(event, str) or not event.strip():
            logger.error("Invalid event for dispatch: %r", event)
            raise ValueError("event must be a non-empty string")
        if not isinstance(data, dict):
            logger.error("Invalid data for dispatch: %r", data)
            raise ValueError("data must be a dict")
        try:
            result = await self._wh.handle(provider=provider, event=event, data=data)
            logger.info("Webhook dispatched: provider=%s, event=%s", provider, event)
            return result
        except Exception as exc:
            logger.exception("Failed to dispatch webhook: provider=%s, event=%s: %s", provider, event, exc)
            raise
