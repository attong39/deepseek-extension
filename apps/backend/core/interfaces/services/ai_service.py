"""AI service interface"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.backend.core.domain.value_objects.ai_request import AIRequest
from apps.backend.core.domain.value_objects.ai_response import AIResponse


class AIServiceInterface(ABC):
    """Interface for AI service"""
import dict
import str

    @abstractmethod
    async def process_request(self, request: AIRequest) -> AIResponse:
        """Process AI request"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> dict[str, Any]:
        """Get service capabilities"""
        pass
