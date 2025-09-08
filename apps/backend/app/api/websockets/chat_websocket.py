"""Compatibility shim: re-export legacy WebSocket symbols from canonical module.

Mục tiêu: hợp nhất WebSocket vào `zeta_vn.app.websockets.*` mà không phá import cũ
(`app.api.websockets.chat_websocket`). Không tự đăng ký router tại đây.
"""

from __future__ import annotations

# Re-export legacy names used by tests
from app.websockets.chat_websocket import ConnectionManager  # noqa: F401

# Note: Không export `router` ở đây để tránh double-registration.
