"""Mock notification provider for development and tests.

Implements email/sms/webhook/push/in-app interfaces with deterministic
behaviour and no external network calls.
"""

from __future__ import annotations

import asyncio
import uuid
from importlib import import_module
from typing import Any

from apps.backend.core.interfaces import notification_interfaces as ni
import Exception
import bool
import delivery_id
import dict
import email
import f
import getattr
import int
import list
import message_id
import phone
import recipients
import str
import url
import webhook_id


class MockNotificationProvider(
    ni.EmailNotificationInterface,
    ni.SMSNotificationInterface,
    ni.WebhookNotificationInterface,
    ni.PushNotificationInterface,
    ni.InAppNotificationInterface,
):
    """Simple mock provider returning deterministic IDs and logs operations."""

    async def send_email(
        self,
        to,
        subject,
        body,
        from_=None,
        cc=None,
        bcc=None,
        attachments=None,
        is_html=False,
    ) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-email-" + uuid.uuid4().hex

    async def send_template_email(
        self, to, template_id, template_data, from_=None
    ) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-template-email-" + uuid.uuid4().hex

    async def validate_email(self, email: str) -> bool:  # type: ignore[override]
        return "@" in email

    async def get_delivery_status(self, message_id: str) -> dict[str, Any]:  # type: ignore[override]
        await asyncio.sleep(0)
        return {"message_id": message_id, "status": "delivered", "channel": "email"}

    async def send_sms(self, to, message, from_=None) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-sms-" + uuid.uuid4().hex

    async def send_bulk_sms(self, recipients, message, from_=None) -> list[str]:  # type: ignore[override]
        await asyncio.sleep(0)
        return ["mock-sms-" + uuid.uuid4().hex for _ in recipients]

    async def validate_phone_number(self, phone: str) -> bool:  # type: ignore[override]
        return phone.isdigit()

    async def get_sms_status(self, message_id: str) -> dict[str, Any]:  # type: ignore[override]
        await asyncio.sleep(0)
        return {"message_id": message_id, "status": "delivered", "channel": "sms"}

    async def send_push(
        self, device_tokens, title, body, data=None, badge=None, sound=None
    ) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-push-" + uuid.uuid4().hex

    async def send_topic_push(self, topic, title, body, data=None) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-topic-push-" + uuid.uuid4().hex

    async def register_device(
        self, user_id: str, device_token: str, platform: str
    ) -> bool:  # type: ignore[override]
        await asyncio.sleep(0)
        return True

    async def unregister_device(self, device_token: str) -> bool:  # type: ignore[override]
        await asyncio.sleep(0)
        return True

    async def subscribe_to_topic(self, device_token: str, topic: str) -> bool:  # type: ignore[override]
        await asyncio.sleep(0)
        return True

    async def send_notification(
        self, user_id, title, message, type_="info", data=None, expires_at=None
    ) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-inapp-" + uuid.uuid4().hex

    async def get_notifications(
        self, user_id, unread_only=False, limit=50, offset=0
    ) -> list[dict[str, Any]]:  # type: ignore[override]
        await asyncio.sleep(0)
        return []

    async def mark_as_read(self, user_id, notification_ids) -> bool:  # type: ignore[override]
        await asyncio.sleep(0)
        return True

    async def delete_notification(self, user_id, notification_id) -> bool:  # type: ignore[override]
        await asyncio.sleep(0)
        return True

    async def get_unread_count(self, user_id) -> int:  # type: ignore[override]
        await asyncio.sleep(0)
        return 0

    async def send_webhook(
        self, url, payload, headers=None, method="POST", timeout=30
    ) -> dict[str, Any]:  # type: ignore[override]
        # Import helpers at runtime to avoid circular package imports during test/import time
        try:
            nh = import_module("zeta_vn.core.utils.notification_helpers")
            retry_decorator = getattr(nh, "async_retry", None)
        except Exception:
            retry_decorator = None

        def _noop_retry(**kwargs):
            def _wrap(f):
                return f

            return _wrap

        decorator = retry_decorator or _noop_retry

        @decorator(retries=2)  # type: ignore[call-arg]
        async def _do_send():
            await asyncio.sleep(0)
            return {"url": url, "status": 200, "body": {"ok": True}}

        return await _do_send()

    async def register_webhook(
        self, name, url, events, secret=None, is_active=True
    ) -> str:  # type: ignore[override]
        await asyncio.sleep(0)
        return "mock-webhook-" + uuid.uuid4().hex

    async def validate_webhook_signature(
        self, payload: str, signature: str, secret: str
    ) -> bool:  # type: ignore[override]
        # We don't import helpers here to avoid circular; simple equality for mock
        return True

    async def retry_webhook(self, webhook_id: str, delivery_id: str) -> dict[str, Any]:  # type: ignore[override]
        await asyncio.sleep(0)
        return {
            "webhook_id": webhook_id,
            "delivery_id": delivery_id,
            "status": "retried",
        }
