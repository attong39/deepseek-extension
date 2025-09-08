"""Deprecated Agent WebSocket module (canonical location).

Kept for backward compatibility. Prefer importing from
`zeta_vn.app.websockets.agent_websocket` or use the new chat/training modules.
"""

from __future__ import annotations

from typing import Any
import Exception
import RuntimeError
import str

try:  # Optional: allow type-check without FastAPI installed
    from fastapi import WebSocket
except Exception:  # pragma: no cover - fallback typing stub

    class WebSocket:  # type: ignore[override]
        """Minimal stub for type hints when FastAPI isn't available."""


class _DeprecatedAgentWSManager:
    """Placeholder manager for deprecated module.

    Any attribute access raises a clear runtime error guiding callers to the
    new modules.
    """

    def __getattr__(self, name: str) -> Any:  # noqa: D401 - simple redirect
        raise RuntimeError(
            "Agent WebSocket is deprecated. Use chat_websocket or training_ws."
        )


agent_ws_manager = _DeprecatedAgentWSManager()


async def agent_websocket_endpoint(websocket: WebSocket, user_id: str) -> None:
    """Deprecated endpoint placeholder."""

    raise RuntimeError(
        "Deprecated endpoint. Use chat_websocket or training_ws instead."
    )


__all__ = ["agent_ws_manager", "agent_websocket_endpoint"]
