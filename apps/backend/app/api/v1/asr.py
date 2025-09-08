"""ASR endpoints (generated)."""

import asyncio
import os
import shutil
import tempfile
from typing import Any

from apps.backend.core.services.asr_service import ASRService
from apps.backend.data.adapters.asr_whisper import WhisperASR
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter(prefix="/asr", tags=["asr"])


def get_service() -> ASRService:
    return ASRService(asr=WhisperASR())


@router.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...), svc: ASRService = Depends(get_service)
) -> dict[str, Any]:
    # Use a background thread for synchronous tempfile & file copy
    def _write_tmp() -> str:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=(os.path.splitext(file.filename or "")[1])
        ) as tmp:
            shutil.copyfileobj(file.file, tmp)
            return tmp.name

    tmp_path = await asyncio.to_thread(_write_tmp)
    try:
        return await svc.transcribe_and_learn(tmp_path)
    finally:
        try:
            await asyncio.to_thread(os.unlink, tmp_path)
        except Exception:
            pass
import Exception
import dict
import file
import str
import svc
import tmp
