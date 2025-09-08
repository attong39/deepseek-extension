"""Notification service for managing system notifications.





This service handles creating, sending, and managing notifications across


different channels following Clean Architecture principles.


"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID

from apps.backend.core.domain.entities.notification import (
import Exception
import RuntimeError
import action_text
import action_url
import bool
import channel
import channels
import dict
import e
import image_url
import list
import memory_repository
import message
import metadata
import notification_type
import priority
import recipient_id
import recipient_type
import self
import str
import summary
import title
    Notification,
    NotificationChannel,
    NotificationContent,
    NotificationPriority,
    NotificationStatus,
    NotificationType,
)

if TYPE_CHECKING:
    from apps.backend.core.interfaces.repositories.memory import (
        MemoryRepository,  # Use existing interface for now
    )


logger = logging.getLogger(__name__)


class NotificationService:
    """Service for managing notifications across the system."""

    def __init__(self, memory_repository: MemoryRepository) -> None:
        """Initialize notification service.





        Args:


            memory_repository: Repository for notification persistence (placeholder).


        """

        self.memory_repository = memory_repository

    def _get_current_time(self) -> datetime:
        """Get current UTC time."""

        return datetime.now(UTC)

    def create_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType,
        channels: list[NotificationChannel],
        recipient_id: UUID,
        recipient_type: str = "user",
        priority: NotificationPriority = NotificationPriority.NORMAL,
        metadata: dict[str, Any] | None = None,
        summary: str | None = None,
        action_url: str | None = None,
        action_text: str | None = None,
        image_url: str | None = None,
    ) -> Notification:
        """Create a new notification.





        Args:


            title: Notification title.


            message: Notification message content.


            notification_type: Type of notification.


            channels: Delivery channels for the notification.


            recipient_id: ID of the notification recipient.


            recipient_type: Type of recipient.


            priority: Priority level.


            metadata: Additional notification metadata.


            summary: Optional short summary.


            action_url: Optional action URL.


            action_text: Optional action button text.


            image_url: Optional image URL.





        Returns:


            Created notification entity.





        Raises:


            RuntimeError: If notification creation fails.


        """

        try:
            logger.info(f"Creating notification: {title} for recipient {recipient_id}")

            # Create notification content

            content = NotificationContent(
                title=title,
                message=message,
                summary=summary,
                action_url=action_url,
                action_text=action_text,
                image_url=image_url,
                metadata=metadata or {},
            )

            # Create notification entity

            notification = Notification(
                content=content,
                type=notification_type,
                priority=priority,
                recipient_id=recipient_id,
                recipient_type=recipient_type,
                channels=channels,
                scheduled_at=self._get_current_time(),
                expires_at=None,
                source="notification_service",
                source_id=str(recipient_id),
                correlation_id=None,
            )

            logger.info(f"Created notification: {notification.id}")

            return notification

        except Exception as e:
            logger.error(f"Failed to create notification: {e}")

            raise RuntimeError(f"Failed to create notification: {e!s}") from e

    def send_notification(self, notification: Notification) -> bool:
        """Send a notification using the configured channels.





        Args:


            notification: Notification to send.





        Returns:


            True if notification was sent successfully.





        Raises:


            RuntimeError: If sending fails.


        """

        try:
            logger.info(f"Sending notification: {notification.id}")

            # Check if already sent

            if notification.status == NotificationStatus.SENT:
                logger.warning(f"Notification already sent: {notification.id}")

                return True

            # Attempt to send via all channels

            success = True

            for channel in notification.channels:
                channel_success = self._send_via_channel(notification, channel)

                if not channel_success:
                    success = False

            if success:
                # Update status to sent

                notification.mark_sent()

                logger.info(f"Successfully sent notification: {notification.id}")

                return True

            else:
                # Update status to failed

                notification.mark_failed("Failed to send via one or more channels")

                logger.error(f"Failed to send notification: {notification.id}")

                return False

        except Exception as e:
            logger.error(f"Error sending notification {notification.id}: {e}")

            raise RuntimeError(f"Failed to send notification: {e!s}") from e

    def _send_via_channel(
        self, notification: Notification, channel: NotificationChannel
    ) -> bool:
        """Send notification via a specific channel.





        Args:


            notification: Notification to send.


            channel: Channel to send via.





        Returns:


            True if sent successfully.


        """

        try:
            # For now, just log the sending attempt

            # In a real implementation, this would integrate with actual notification services

            logger.info(
                f"Sending notification {notification.id} via {channel.value}: "
                f"{notification.content.title}"
            )

            # Simulate successful sending

            return True

        except Exception as e:
            logger.error(f"Failed to send via channel {channel}: {e}")

            return False

    def send_immediate(
        self,
        title: str,
        message: str,
        notification_type: NotificationType,
        channels: list[NotificationChannel],
        recipient_id: UUID,
        recipient_type: str = "user",
        priority: NotificationPriority = NotificationPriority.NORMAL,
        metadata: dict[str, Any] | None = None,
    ) -> bool:
        """Create and immediately send a notification.





        Args:


            title: Notification title.


            message: Notification message content.


            notification_type: Type of notification.


            channels: Delivery channels for the notification.


            recipient_id: ID of the notification recipient.


            recipient_type: Type of recipient.


            priority: Priority level.


            metadata: Additional notification metadata.





        Returns:


            True if notification was sent successfully.


        """

        try:
            # Create notification

            notification = self.create_notification(
                title=title,
                message=message,
                notification_type=notification_type,
                channels=channels,
                recipient_id=recipient_id,
                recipient_type=recipient_type,
                priority=priority,
                metadata=metadata,
            )

            # Send immediately

            return self.send_notification(notification)

        except Exception as e:
            logger.error(f"Failed to send immediate notification: {e}")

            return False

    def create_alert(
        self,
        title: str,
        message: str,
        recipient_id: UUID,
        channels: list[NotificationChannel] | None = None,
    ) -> bool:
        """Create and send an urgent alert notification.





        Args:


            title: Alert title.


            message: Alert message.


            recipient_id: ID of the alert recipient.


            channels: Optional channels to send via.





        Returns:


            True if alert was sent successfully.


        """

        default_channels = [NotificationChannel.EMAIL, NotificationChannel.IN_APP]

        return self.send_immediate(
            title=title,
            message=message,
            notification_type=NotificationType.ALERT,
            channels=channels or default_channels,
            recipient_id=recipient_id,
            priority=NotificationPriority.URGENT,
        )

    def create_info_notification(
        self,
        title: str,
        message: str,
        recipient_id: UUID,
        channels: list[NotificationChannel] | None = None,
    ) -> bool:
        """Create and send an info notification.





        Args:


            title: Notification title.


            message: Notification message.


            recipient_id: ID of the notification recipient.


            channels: Optional channels to send via.





        Returns:


            True if notification was sent successfully.


        """

        default_channels = [NotificationChannel.IN_APP]

        return self.send_immediate(
            title=title,
            message=message,
            notification_type=NotificationType.INFO,
            channels=channels or default_channels,
            recipient_id=recipient_id,
            priority=NotificationPriority.NORMAL,
        )
