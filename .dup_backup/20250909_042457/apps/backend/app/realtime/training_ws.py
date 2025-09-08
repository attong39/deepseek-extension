# Shim: re-export canonical training WebSocket from app.websockets.
# Keeps backward compatibility for imports `zeta_vn.app.realtime.training_ws`.
from __future__ import annotations

from apps.backend.app.websockets.training_ws import (  # noqa: F401
    broadcast_training_progress,
    router,
)
