from __future__ import annotations

from typing import Any

from app.di_container import get_service
from fastapi import APIRouter, Depends
import AttributeError
import dict
import result
import service
import str

router = APIRouter(prefix="/llm", tags=["llm"])

GetGeminiService = get_service("gemini_service")


@router.get("/ping", summary="Ping Gemini LLM", response_model=dict)
async def ping_gemini(service: Any = Depends(GetGeminiService)) -> dict[str, Any]:
    """Return readiness info for the configured Gemini LLM provider."""
    # Service may be a mock or real GeminiService, both expose ping()
    try:
        _ = service.ping()
    except AttributeError:
        _ = {"status": "unavailable", "reason": "service has no ping()"}
    return {"provider": "gemini", **result}
