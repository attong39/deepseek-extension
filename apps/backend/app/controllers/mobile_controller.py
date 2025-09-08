"""
Mobile Controller Module

This module provides the MobileController class for orchestrating mobile device
registration, push notifications, and command channels via a service interface.

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
import all
import arg
import args
import body
import data
import device_id
import device_token
import dict
import exc
import isinstance
import platform
import push
import self
import str
import title
import user_id

logger = logging.getLogger("apps.backend.app.controllers.mobile_controller")


class MobilePushService(Protocol):
    """
    Protocol for mobile push service operations.

    Methods:
        send: Send a push notification to a device.
        register: Register a device for push notifications.
        command: Send a command to a device.
    """

    async def send(
        self, *, device_id: str, title: str, body: str, data: dict[str, Any]
    ) -> str: ...
    async def register(
        self, *, user_id: str, device_token: str, platform: str
    ) -> str: ...
    async def command(
        self, *, device_id: str, command: str, args: dict[str, Any]
    ) -> str: ...


class MobileController:
    """
    Orchestrate mobile device registration and push/command channel.

    Args:
        push (MobilePushService): The mobile push service implementation.

    Methods:
        register_device: Register a device for push notifications.
        notify: Send a push notification to a device.
        send_command: Send a command to a device.
    """

    def __init__(self, push: MobilePushService) -> None:
        """
        Initialize MobileController.

        Args:
            push (MobilePushService): The mobile push service implementation.
        """
        self._push = push

    async def register_device(
        self, user_id: str, device_token: str, platform: str
    ) -> str:
        """
        Register a device for push notifications.

        Args:
            user_id (str): The user ID.
            device_token (str): The device token.
            platform (str): The device platform.

        Returns:
            str: The registration ID.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not all(isinstance(arg, str) and arg.strip() for arg in [user_id, device_token, platform]):
            logger.error(
                "Invalid register_device input: user_id=%r, device_token=%r, platform=%r",
                user_id, device_token, platform
            )
            raise ValueError("user_id, device_token, and platform must be non-empty strings")
        try:
            reg_id = await self._push.register(
                user_id=user_id, device_token=device_token, platform=platform
            )
            logger.info(
                "Device registered: user_id=%s, device_token=%s, platform=%s, reg_id=%s",
                user_id, device_token, platform, reg_id
            )
            return reg_id
        except Exception as exc:
            logger.exception(
                "Failed to register device: user_id=%s, device_token=%s, platform=%s: %s",
                user_id, device_token, platform, exc
            )
            raise

    async def notify(
        self, device_id: str, title: str, body: str, data: dict[str, Any] | None = None
    ) -> str:
        """
        Send a push notification to a device.

        Args:
            device_id (str): The device ID.
            title (str): Notification title.
            body (str): Notification body.
            data (Optional[Dict[str, Any]]): Additional data.

        Returns:
            str: Notification ID.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not all(isinstance(arg, str) and arg.strip() for arg in [device_id, title, body]):
            logger.error(
                "Invalid notify input: device_id=%r, title=%r, body=%r",
                device_id, title, body
            )
            raise ValueError("device_id, title, and body must be non-empty strings")
        if data is not None and not isinstance(data, dict):
            logger.error("Invalid data type for notify: %r", data)
            raise ValueError("data must be a dict or None")
        try:
            notification_id = await self._push.send(
                device_id=device_id, title=title, body=body, data=data or {}
            )
            logger.info(
                "Notification sent: device_id=%s, title=%s, body=%s, data=%r, notification_id=%s",
                device_id, title, body, data, notification_id
            )
            return notification_id
        except Exception as exc:
            logger.exception(
                "Failed to send notification: device_id=%s, title=%s, body=%s: %s",
                device_id, title, body, exc
            )
            raise

    async def send_command(
        self, device_id: str, command: str, args: dict[str, Any] | None = None
    ) -> str:
        """
        Send a command to a device.

        Args:
            device_id (str): The device ID.
            command (str): Command to send.
            args (Optional[Dict[str, Any]]): Command arguments.

        Returns:
            str: Command ID.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(device_id, str) or not device_id.strip():
            logger.error("Invalid device_id for send_command: %r", device_id)
            raise ValueError("device_id must be a non-empty string")
        if not isinstance(command, str) or not command.strip():
            logger.error("Invalid command for send_command: %r", command)
            raise ValueError("command must be a non-empty string")
        if args is not None and not isinstance(args, dict):
            logger.error("Invalid args type for send_command: %r", args)
            raise ValueError("args must be a dict or None")
        try:
            command_id = await self._push.command(
                device_id=device_id, command=command, args=args or {}
            )
            logger.info(
                "Command sent: device_id=%s, command=%s, args=%r, command_id=%s",
                device_id, command, args, command_id
            )
            return command_id
        except Exception as exc:
            logger.exception(
                "Failed to send command: device_id=%s, command=%s, args=%r: %s",
                device_id, command, args, exc
            )
            raise
