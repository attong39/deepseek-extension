"""Notification interfaces.

This module defines abstract interfaces for notification operations
including email, SMS, push notifications, and in-app messaging.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
import bool
import dict
import float
import int
import list
import str


class EmailNotificationInterface(ABC):
    """Interface for email notification operations."""

    @abstractmethod
    async def send_email(
        self,
        to: list[str],
        subject: str,
        body: str,
        from_: str | None = None,
        cc: list[str] | None = None,
        bcc: list[str] | None = None,
        attachments: list[dict[str, Any]] | None = None,
        is_html: bool = False,
    ) -> str:
        """Send email notification.

        Args:
            to: List of recipient email addresses.
            subject: Email subject.
            body: Email body content.
            from_: Optional sender email address.
            cc: Optional CC recipients.
            bcc: Optional BCC recipients.
            attachments: Optional email attachments.
            is_html: Whether body is HTML formatted.

        Returns:
            Message ID of sent email.
        """

    @abstractmethod
    async def send_template_email(
        self,
        to: list[str],
        template_id: str,
        template_data: dict[str, Any],
        from_: str | None = None,
    ) -> str:
        """Send email using template.

        Args:
            to: List of recipient email addresses.
            template_id: Email template identifier.
            template_data: Data to populate template.
            from_: Optional sender email address.

        Returns:
            Message ID of sent email.
        """

    @abstractmethod
    async def validate_email(self, email: str) -> bool:
        """Validate email address format.

        Args:
            email: Email address to validate.

        Returns:
            True if email is valid.
        """

    @abstractmethod
    async def get_delivery_status(self, message_id: str) -> dict[str, Any]:
        """Get email delivery status.

        Args:
            message_id: Message ID to check.

        Returns:
            Delivery status information.
        """


class SMSNotificationInterface(ABC):
    """Interface for SMS notification operations."""

    @abstractmethod
    async def send_sms(
        self,
        to: str,
        message: str,
        from_: str | None = None,
    ) -> str:
        """Send SMS notification.

        Args:
            to: Recipient phone number.
            message: SMS message content.
            from_: Optional sender phone number.

        Returns:
            Message ID of sent SMS.
        """

    @abstractmethod
    async def send_bulk_sms(
        self,
        recipients: list[str],
        message: str,
        from_: str | None = None,
    ) -> list[str]:
        """Send SMS to multiple recipients.

        Args:
            recipients: List of recipient phone numbers.
            message: SMS message content.
            from_: Optional sender phone number.

        Returns:
            List of message IDs.
        """

    @abstractmethod
    async def validate_phone_number(self, phone: str) -> bool:
        """Validate phone number format.

        Args:
            phone: Phone number to validate.

        Returns:
            True if phone number is valid.
        """

    @abstractmethod
    async def get_sms_status(self, message_id: str) -> dict[str, Any]:
        """Get SMS delivery status.

        Args:
            message_id: Message ID to check.

        Returns:
            SMS delivery status.
        """


class PushNotificationInterface(ABC):
    """Interface for push notification operations."""

    @abstractmethod
    async def send_push(
        self,
        device_tokens: list[str],
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
        badge: int | None = None,
        sound: str | None = None,
    ) -> str:
        """Send push notification.

        Args:
            device_tokens: List of device tokens.
            title: Notification title.
            body: Notification body.
            data: Optional custom data.
            badge: Optional badge count.
            sound: Optional sound file.

        Returns:
            Notification ID.
        """

    @abstractmethod
    async def send_topic_push(
        self,
        topic: str,
        title: str,
        body: str,
        data: dict[str, Any] | None = None,
    ) -> str:
        """Send push notification to topic subscribers.

        Args:
            topic: Topic name.
            title: Notification title.
            body: Notification body.
            data: Optional custom data.

        Returns:
            Notification ID.
        """

    @abstractmethod
    async def register_device(
        self,
        user_id: str,
        device_token: str,
        platform: str,
    ) -> bool:
        """Register device for push notifications.

        Args:
            user_id: User identifier.
            device_token: Device push token.
            platform: Device platform (ios, android).

        Returns:
            True if registration successful.
        """

    @abstractmethod
    async def unregister_device(
        self,
        device_token: str,
    ) -> bool:
        """Unregister device from push notifications.

        Args:
            device_token: Device push token.

        Returns:
            True if unregistration successful.
        """

    @abstractmethod
    async def subscribe_to_topic(
        self,
        device_token: str,
        topic: str,
    ) -> bool:
        """Subscribe device to topic.

        Args:
            device_token: Device push token.
            topic: Topic name.

        Returns:
            True if subscription successful.
        """


class InAppNotificationInterface(ABC):
    """Interface for in-app notification operations."""

    @abstractmethod
    async def send_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        type_: str = "info",
        data: dict[str, Any] | None = None,
        expires_at: float | None = None,
    ) -> str:
        """Send in-app notification.

        Args:
            user_id: Recipient user ID.
            title: Notification title.
            message: Notification message.
            type_: Notification type (info, warning, error, success).
            data: Optional additional data.
            expires_at: Optional expiration timestamp.

        Returns:
            Notification ID.
        """

    @abstractmethod
    async def get_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Get user notifications.

        Args:
            user_id: User identifier.
            unread_only: Whether to return only unread notifications.
            limit: Maximum number of notifications.
            offset: Pagination offset.

        Returns:
            List of notifications.
        """

    @abstractmethod
    async def mark_as_read(
        self,
        user_id: str,
        notification_ids: list[str],
    ) -> bool:
        """Mark notifications as read.

        Args:
            user_id: User identifier.
            notification_ids: List of notification IDs.

        Returns:
            True if successful.
        """

    @abstractmethod
    async def delete_notification(
        self,
        user_id: str,
        notification_id: str,
    ) -> bool:
        """Delete notification.

        Args:
            user_id: User identifier.
            notification_id: Notification ID to delete.

        Returns:
            True if deletion successful.
        """

    @abstractmethod
    async def get_unread_count(self, user_id: str) -> int:
        """Get count of unread notifications.

        Args:
            user_id: User identifier.

        Returns:
            Number of unread notifications.
        """


class WebhookNotificationInterface(ABC):
    """Interface for webhook notification operations."""

    @abstractmethod
    async def send_webhook(
        self,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
        method: str = "POST",
        timeout: int = 30,
    ) -> dict[str, Any]:
        """Send webhook notification.

        Args:
            url: Webhook URL.
            payload: Webhook payload.
            headers: Optional HTTP headers.
            method: HTTP method.
            timeout: Request timeout in seconds.

        Returns:
            Webhook response information.
        """

    @abstractmethod
    async def register_webhook(
        self,
        name: str,
        url: str,
        events: list[str],
        secret: str | None = None,
        is_active: bool = True,
    ) -> str:
        """Register webhook endpoint.

        Args:
            name: Webhook name.
            url: Webhook URL.
            events: List of events to subscribe to.
            secret: Optional webhook secret for signature verification.
            is_active: Whether webhook is active.

        Returns:
            Webhook ID.
        """

    @abstractmethod
    async def validate_webhook_signature(
        self,
        payload: str,
        signature: str,
        secret: str,
    ) -> bool:
        """Validate webhook signature.

        Args:
            payload: Webhook payload.
            signature: Received signature.
            secret: Webhook secret.

        Returns:
            True if signature is valid.
        """

    @abstractmethod
    async def retry_webhook(
        self,
        webhook_id: str,
        delivery_id: str,
    ) -> dict[str, Any]:
        """Retry failed webhook delivery.

        Args:
            webhook_id: Webhook identifier.
            delivery_id: Delivery attempt identifier.

        Returns:
            Retry result.
        """


class NotificationTemplateInterface(ABC):
    """Interface for notification template operations."""

    @abstractmethod
    async def create_template(
        self,
        name: str,
        type_: str,
        content: dict[str, Any],
        variables: list[str] | None = None,
    ) -> str:
        """Create notification template.

        Args:
            name: Template name.
            type_: Template type (email, sms, push, etc.).
            content: Template content.
            variables: Optional list of template variables.

        Returns:
            Template ID.
        """

    @abstractmethod
    async def get_template(self, template_id: str) -> dict[str, Any] | None:
        """Get notification template.

        Args:
            template_id: Template identifier.

        Returns:
            Template data or None if not found.
        """

    @abstractmethod
    async def update_template(
        self,
        template_id: str,
        updates: dict[str, Any],
    ) -> bool:
        """Update notification template.

        Args:
            template_id: Template identifier.
            updates: Template updates.

        Returns:
            True if update successful.
        """

    @abstractmethod
    async def delete_template(self, template_id: str) -> bool:
        """Delete notification template.

        Args:
            template_id: Template identifier.

        Returns:
            True if deletion successful.
        """

    @abstractmethod
    async def render_template(
        self,
        template_id: str,
        variables: dict[str, Any],
    ) -> dict[str, Any]:
        """Render template with variables.

        Args:
            template_id: Template identifier.
            variables: Template variable values.

        Returns:
            Rendered template content.
        """


class NotificationPreferencesInterface(ABC):
    """Interface for user notification preferences."""

    @abstractmethod
    async def get_preferences(self, user_id: str) -> dict[str, Any]:
        """Get user notification preferences.

        Args:
            user_id: User identifier.

        Returns:
            User notification preferences.
        """

    @abstractmethod
    async def update_preferences(
        self,
        user_id: str,
        preferences: dict[str, Any],
    ) -> bool:
        """Update user notification preferences.

        Args:
            user_id: User identifier.
            preferences: New preference settings.

        Returns:
            True if update successful.
        """

    @abstractmethod
    async def check_preference(
        self,
        user_id: str,
        notification_type: str,
        channel: str,
    ) -> bool:
        """Check if user wants notifications of specific type via channel.

        Args:
            user_id: User identifier.
            notification_type: Type of notification.
            channel: Notification channel (email, sms, push, etc.).

        Returns:
            True if user wants this type of notification.
        """

    @abstractmethod
    async def set_do_not_disturb(
        self,
        user_id: str,
        enabled: bool,
        until: float | None = None,
    ) -> bool:
        """Set do not disturb mode for user.

        Args:
            user_id: User identifier.
            enabled: Whether to enable do not disturb.
            until: Optional end time for do not disturb.

        Returns:
            True if setting successful.
        """
