"""Webhook client for sending and receiving webhook notifications."""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import logging
from datetime import UTC, datetime
from functools import lru_cache
from typing import Any

import aiohttp
from apps.backend.config.settings import Settings
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WebhookPayload(BaseModel):
    """Webhook payload model."""
import Exception
import TimeoutError
import base_url
import bool
import config
import dict
import e
import event_id
import event_type
import events
import int
import isinstance
import list
import max_retries
import metadata
import name
import result
import retry_count
import self
import session
import str
import webhook
import webhook_config

    event_type: str = Field(..., description="Type of event")

    event_id: str = Field(..., description="Unique event identifier")

    timestamp: str = Field(..., description="Event timestamp")

    data: dict[str, Any] = Field(default_factory=dict, description="Event data")

    metadata: dict[str, Any] | None = Field(
        default=None, description="Additional metadata"
    )


class WebhookResponse(BaseModel):
    """Webhook response model."""

    success: bool = Field(..., description="Whether webhook was successful")

    status_code: int = Field(..., description="HTTP status code")

    response_data: dict[str, Any] | None = Field(
        default=None, description="Response data"
    )

    error_message: str | None = Field(
        default=None, description="Error message if failed"
    )

    response_time_ms: int = Field(..., description="Response time in milliseconds")


class WebhookClient:
    """Client for sending webhook notifications."""

    def __init__(
        self, base_url: str | None = None, timeout: int = 30, max_retries: int = 3
    ):
        """Initialize webhook client."""

        self.settings = Settings()

        self.base_url = base_url

        self.timeout = timeout

        self.max_retries = max_retries

        # Create HTTP session

        self.session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""

        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            # Await a trivial asyncio operation to satisfy async contract
            await asyncio.sleep(0)
            self._ = aiohttp.ClientSession(timeout=timeout)

        return self.session

    async def close(self) -> None:
        """Close the HTTP session."""

        if self.session and not self.session.closed:
            await self.session.close()

    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook payload."""

        signature = hmac.new(
            secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return f"sha256={signature}"

    def _verify_signature(self, payload: str, signature: str, secret: str) -> bool:
        """Verify webhook signature."""

        expected_signature = self._generate_signature(payload, secret)

        return hmac.compare_digest(signature, expected_signature)

    async def send_webhook(
        self,
        url: str,
        payload: WebhookPayload,
        secret: str | None = None,
        headers: dict[str, str] | None = None,
        retry_count: int = 0,
    ) -> WebhookResponse:
        """Send a webhook notification."""

        _ = await self._get_session()

        # Prepare payload

        payload_str = payload.model_dump_json()

        # Prepare headers

        request_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Zeta-AI-Webhook/1.0",
        }

        if headers:
            request_headers.update(headers)

        # Add signature if secret provided

        if secret:
            signature = self._generate_signature(payload_str, secret)

            request_headers["X-Webhook-Signature"] = signature

        start_time = asyncio.get_event_loop().time()

        try:
            async with session.post(
                url, data=payload_str, headers=request_headers
            ) as response:
                end_time = asyncio.get_event_loop().time()

                response_time_ms = int((end_time - start_time) * 1000)

                # Parse response

                try:
                    response_data = await response.json()

                except Exception:
                    response_data = {"text": await response.text()}

                success = 200 <= response.status < 300

                return WebhookResponse(
                    success=success,
                    status_code=response.status,
                    response_data=response_data,
                    response_time_ms=response_time_ms,
                )

        except TimeoutError:
            end_time = asyncio.get_event_loop().time()

            response_time_ms = int((end_time - start_time) * 1000)

            # Retry if configured

            if retry_count < self.max_retries:
                logger.warning(
                    f"Webhook timeout, retrying {retry_count + 1}/{self.max_retries}"
                )

                await asyncio.sleep(2**retry_count)  # Exponential backoff

                return await self.send_webhook(
                    url, payload, secret, headers, retry_count + 1
                )

            return WebhookResponse(
                success=False,
                status_code=408,
                error_message="Request timeout",
                response_time_ms=response_time_ms,
            )

        except Exception as e:
            end_time = asyncio.get_event_loop().time()

            response_time_ms = int((end_time - start_time) * 1000)

            # Retry if configured

            if retry_count < self.max_retries:
                logger.warning(
                    f"Webhook error, retrying {retry_count + 1}/{self.max_retries}: {e}"
                )

                await asyncio.sleep(2**retry_count)  # Exponential backoff

                return await self.send_webhook(
                    url, payload, secret, headers, retry_count + 1
                )

            return WebhookResponse(
                success=False,
                status_code=500,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

    async def send_multiple_webhooks(
        self, webhooks: list[dict[str, Any]]
    ) -> list[WebhookResponse]:
        """Send multiple webhooks concurrently."""

        tasks = []

        for webhook_config in webhooks:
            url = webhook_config["url"]

            payload = WebhookPayload(**webhook_config["payload"])

            secret = webhook_config.get("secret")

            headers = webhook_config.get("headers")

            task = self.send_webhook(url, payload, secret, headers)

            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error responses

        responses = []

        for result in results:
            if isinstance(result, Exception):
                responses.append(
                    WebhookResponse(
                        success=False,
                        status_code=500,
                        error_message=str(result),
                        response_time_ms=0,
                    )
                )

            else:
                responses.append(result)

        return responses

    async def test_webhook(
        self, url: str, secret: str | None = None
    ) -> WebhookResponse:
        """Send a test webhook to verify connectivity."""

        test_payload = WebhookPayload(
            event_type="test",
            event_id="test-webhook",
            timestamp="2024-01-01T00:00:00Z",
            data={"message": "This is a test webhook from Zeta AI"},
        )

        return await self.send_webhook(url, test_payload, secret)

    def validate_incoming_webhook(
        self, payload: str, signature: str, secret: str
    ) -> bool:
        """Validate an incoming webhook signature."""

        return self._verify_signature(payload, signature, secret)

    async def parse_incoming_webhook(self, payload: str) -> WebhookPayload | None:
        """Parse an incoming webhook payload."""

        try:
            data = json.loads(payload)

            # No async work required, but keep signature for symmetry and future hooks
            await asyncio.sleep(0)
            return WebhookPayload(**data)

        except Exception as e:
            logger.error(f"Failed to parse webhook payload: {e}")

            return None


class WebhookRegistry:
    """Registry for managing webhook endpoints."""

    def __init__(self):
        """Initialize webhook registry."""

        self.webhooks: dict[str, dict[str, Any]] = {}

        self.client = WebhookClient()

    def register_webhook(
        self,
        name: str,
        url: str,
        events: list[str],
        secret: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Register a webhook endpoint."""

        self.webhooks[name] = {
            "url": url,
            "events": events,
            "secret": secret,
            "headers": headers or {},
            "active": True,
        }

        logger.info(f"Registered webhook: {name} -> {url}")

    def unregister_webhook(self, name: str) -> None:
        """Unregister a webhook endpoint."""

        if name in self.webhooks:
            del self.webhooks[name]

            logger.info(f"Unregistered webhook: {name}")

    def get_webhooks_for_event(self, event_type: str) -> list[dict[str, Any]]:
        """Get all webhooks that should receive a specific event."""

        matching_webhooks = []

        for name, config in self.webhooks.items():
            if config["active"] and event_type in config["events"]:
                matching_webhooks.append(
                    {
                        "name": name,
                        "url": config["url"],
                        "secret": config["secret"],
                        "headers": config["headers"],
                    }
                )

        return matching_webhooks

    async def send_event(
        self,
        event_type: str,
        event_id: str,
        data: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, WebhookResponse]:
        """Send an event to all registered webhooks."""

        webhooks = self.get_webhooks_for_event(event_type)

        if not webhooks:
            logger.debug(f"No webhooks registered for event: {event_type}")

            return {}

        payload = WebhookPayload(
            event_type=event_type,
            event_id=event_id,
            timestamp=datetime.now(UTC).isoformat(),
            data=data,
            metadata=metadata,
        )

        results = {}

        for webhook in webhooks:
            response = await self.client.send_webhook(
                webhook["url"], payload, webhook["secret"], webhook["headers"]
            )

            results[webhook["name"]] = response

        return results

    async def close(self) -> None:
        """Close the webhook client."""

        await self.client.close()


@lru_cache(maxsize=1)
def get_webhook_registry() -> WebhookRegistry:
    """Get a process-wide webhook registry singleton.

    Uses an LRU cache to avoid global mutation (PLW0603) while providing a
    simple, testable singleton. The cache can be cleared in tests via
    ``get_webhook_registry.cache_clear()``.
    """

    return WebhookRegistry()
