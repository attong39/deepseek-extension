"""
LLM Port - Interface Cho LLM Operations

Port interface để abstract LLM operations, cho phép dễ dàng switch giữa
local models và API-based models.

Attributes:
    model_name: Tên model đang sử dụng.
    is_loaded: Trạng thái model đã load hay chưa.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol
import bool
import loaded
import model_name
import self
import str


class LLMPort(Protocol):
    """Protocol cho LLM operations."""

    @abstractmethod
    async def call_llm(self, model: str, prompt: str) -> str:
        """Call LLM với prompt.

        Args:
            model: Tên model.
            prompt: Prompt cho LLM.

        Returns:
            Response từ LLM.
        """
        ...

    @abstractmethod
    def is_loaded(self) -> bool:
        """Check xem model đã load hay chưa.

        Returns:
            True nếu model đã load.
        """
        ...

    @abstractmethod
    def load_model(self) -> None:
        """Load model vào memory.

        Raises:
            RuntimeError: Nếu load model thất bại.
        """
        ...


class LLMAdapter(ABC):
    """Abstract base class cho LLM adapters."""

    def __init__(self, model_name: str):
        """Khởi tạo adapter với model name.

        Args:
            model_name: Tên model.
        """
        self.model_name = model_name
        self._loaded = False

    def is_loaded(self) -> bool:
        """Check trạng thái loaded."""
        return self._loaded

    def _set_loaded(self, loaded: bool) -> None:
        """Set trạng thái loaded."""
        self._loaded = loaded

    @abstractmethod
    async def call_llm(self, model: str, prompt: str) -> str:
        """Abstract method cho LLM call."""
        ...

    @abstractmethod
    def load_model(self) -> None:
        """Abstract method cho model loading."""
        ...
