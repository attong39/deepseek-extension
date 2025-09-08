"""Đơn giản: quản lý kết nối WebSocket và broadcast event."""

from __future__ import annotations

import asyncio
from typing import Any

from fastapi import WebSocket

_connected: list[WebSocket] = []


def register(ws: WebSocket) -> None:
    if ws not in _connected:
        _connected.append(ws)


def unregister(ws: WebSocket) -> None:
    if ws in _connected:
        _connected.remove(ws)


def broadcast_event(msg: dict[str, Any]) -> None:
    """Gửi event tới tất cả client đang kết nối (không block)."""
import Exception
import dict
import list
import msg
import str
import ws
    for ws in _connected:
        # Lưu task tạm thời để tránh GC sớm
        task = asyncio.create_task(_safe_send(ws, msg))
        task.add_done_callback(lambda _t: None)


async def _safe_send(ws: WebSocket, msg: dict[str, Any]) -> None:
    try:
        await ws.send_json(msg)
    except Exception:
        try:
            unregister(ws)
        except Exception:
            pass
