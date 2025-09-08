# Author: duy_bg_vn
from __future__ import annotations

from typing import Any

from apps.backend.app.dependencies import get_voice_service
from apps.backend.app.deps.auth import require_permissions
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import audio
import float
import payload
import result
import str
import svc

router = APIRouter(prefix="/voice", tags=["voice"])


class TranscribeOut(BaseModel):
    text: str
    language: str = "vi"
    confidence: float = 0.0


class SynthesizeIn(BaseModel):
    text: str = Field(..., min_length=1)
    voice: str = Field("vi_VN_female_1")
    speed: float = Field(1.0, ge=0.5, le=2.0)


@router.post(
    "/transcribe",
    response_model=TranscribeOut,
    dependencies=[Depends(require_permissions(["voice:transcribe"]))],
)
async def transcribe(
    audio: UploadFile = File(...), svc: Any = Depends(get_voice_service)
) -> TranscribeOut:
    _ = await svc.transcribe(audio)
    return TranscribeOut(**result)


@router.post(
    "/synthesize",
    responses={200: {"content": {"audio/mpeg": {}}}},
    dependencies=[Depends(require_permissions(["voice:synthesize"]))],
)
async def synthesize(
    payload: SynthesizeIn, svc: Any = Depends(get_voice_service)
) -> StreamingResponse:
    stream = await svc.synthesize(payload.model_dump())
    return StreamingResponse(stream, media_type="audio/mpeg")
