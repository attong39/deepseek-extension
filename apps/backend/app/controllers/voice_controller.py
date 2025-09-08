"""
Voice Controller Module

This module provides the VoiceController class for orchestrating ASR (transcribe)
and TTS (synthesize) operations via a service interface.

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
import bytes
import dict
import exc
import float
import isinstance
import language
import self
import speed
import str
import text
import voice

logger = logging.getLogger("apps.backend.app.controllers.voice_controller")


class VoiceService(Protocol):
    """
    Protocol for voice service operations.

    Methods:
        transcribe: Transcribe audio bytes to text.
        synthesize: Synthesize text to audio bytes.
    """

    async def transcribe(
        self, audio_bytes: bytes, *, language: str = "vi"
    ) -> dict[str, Any]: ...
    async def synthesize(self, *, text: str, voice: str, speed: float) -> bytes: ...


class VoiceController:
    """
    Bridge for ASR (transcribe) and TTS (synthesize).

    Args:
        voice (VoiceService): The voice service implementation.

    Methods:
        transcribe: Transcribe audio bytes to text.
        synthesize: Synthesize text to audio bytes.
    """

    def __init__(self, voice: VoiceService) -> None:
        """
        Initialize VoiceController.

        Args:
            voice (VoiceService): The voice service implementation.
        """
        self._voice = voice

    async def transcribe(
        self, audio_bytes: bytes, language: str = "vi"
    ) -> dict[str, Any]:
        """
        Transcribe audio bytes to text.

        Args:
            audio_bytes (bytes): Audio data bytes.
            language (str, optional): Language code. Defaults to "vi".

        Returns:
            Dict[str, Any]: Transcription result.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(audio_bytes, bytes) or not audio_bytes:
            logger.error("Invalid audio_bytes for transcribe: %r", audio_bytes)
            raise ValueError("audio_bytes must be non-empty bytes")
        if not isinstance(language, str) or not language.strip():
            logger.error("Invalid language for transcribe: %r", language)
            raise ValueError("language must be a non-empty string")
        try:
            logger.debug("ASR request language=%s", language)
            result = await self._voice.transcribe(audio_bytes, language=language)
            logger.info("Transcription completed for language=%s", language)
            return result
        except Exception as exc:
            logger.exception("Failed to transcribe audio: %s", exc)
            raise

    async def synthesize(
        self, text: str, voice: str = "vi_VN_female_1", speed: float = 1.0
    ) -> bytes:
        """
        Synthesize text to audio bytes.

        Args:
            text (str): Text to synthesize.
            voice (str, optional): Voice model. Defaults to "vi_VN_female_1".
            speed (float, optional): Speech speed. Defaults to 1.0.

        Returns:
            bytes: Synthesized audio bytes.

        Raises:
            ValueError: If input is invalid.
            Exception: If service fails.
        """
        if not isinstance(text, str) or not text.strip():
            logger.error("Invalid text for synthesize: %r", text)
            raise ValueError("text must be a non-empty string")
        if not isinstance(voice, str) or not voice.strip():
            logger.error("Invalid voice for synthesize: %r", voice)
            raise ValueError("voice must be a non-empty string")
        if not isinstance(speed, float) or not (0.5 <= speed <= 2.0):
            logger.error("Invalid speed for synthesize: %r", speed)
            raise ValueError("speed must be a float between 0.5 and 2.0")
        try:
            logger.debug("TTS request voice=%s speed=%s", voice, speed)
            audio_bytes = await self._voice.synthesize(text=text, voice=voice, speed=speed)
            logger.info("Synthesis completed: voice=%s speed=%s", voice, speed)
            return audio_bytes
        except Exception as exc:
            logger.exception("Failed to synthesize text: %s", exc)
            raise
