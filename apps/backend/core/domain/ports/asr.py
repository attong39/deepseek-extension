from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
import bytes
import float
import list
import str


class ASRPort(ABC):
    """
    Port interface cho Automatic Speech Recognition (ASR) service.

    Abstraction cho các implementation khác nhau:
    - OpenAI Whisper
    - Google Speech-to-Text
    - Azure Speech Services
    - Local ASR models
    """

    @abstractmethod
    async def transcribe_audio(
        self, audio_data: bytes, language: str | None = None, format: str = "wav"
    ) -> str:
        """
        Chuyển đổi audio thành text.

        Args:
            audio_data: Raw audio bytes
            language: Language code (auto-detect nếu None)
            format: Audio format (wav, mp3, m4a, etc.)

        Returns:
            Transcribed text

        Raises:
            ASRError: Khi transcription thất bại
        """

    @abstractmethod
    async def transcribe_streaming(
        self, audio_stream: AsyncIterator[bytes], language: str | None = None
    ) -> AsyncIterator[str]:
        """
        Real-time streaming transcription.

        Args:
            audio_stream: Stream of audio chunks
            language: Language code (auto-detect nếu None)

        Yields:
            Partial transcription results
        """

    @abstractmethod
    async def get_supported_languages(self) -> list[str]:
        """
        Trả về danh sách ngôn ngữ hỗ trợ.

        Returns:
            List of language codes (vd: ['en', 'vi', 'ja'])
        """

    @abstractmethod
    async def detect_language(self, audio_data: bytes) -> str:
        """
        Tự động phát hiện ngôn ngữ từ audio.

        Args:
            audio_data: Raw audio bytes

        Returns:
            Detected language code
        """

    @abstractmethod
    async def reduce_noise(self, audio_data: bytes) -> bytes:
        """
        Noise reduction preprocessing cho audio quality.

        Args:
            audio_data: Raw audio with potential noise

        Returns:
            Cleaned audio bytes
        """

    @abstractmethod
    async def get_confidence_score(self, transcription_id: str) -> float:
        """
        Lấy confidence score của transcription.

        Args:
            transcription_id: ID của transcription request

        Returns:
            Confidence score (0.0 - 1.0)
        """
