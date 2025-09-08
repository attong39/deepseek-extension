# zeta_vn/app/api/websockets/router.py
from __future__ import annotations

from apps.backend.app.api.websockets import agent_websocket, chat_websocket
from fastapi import APIRouter


def build_ws_router() -> APIRouter:
    ws = APIRouter(prefix="/ws")
    ws.include_router(agent_websocket.router)
    ws.include_router(chat_websocket.router)
    return ws
