"""
LLM Service - Orchestrator Cho Local Inference

Service để orchestrate LLM calls với local DeepSeek model.

Attributes:
    llm_port: Port cho LLM operations.
    model: Tên model mặc định.
"""

from __future__ import annotations

import logging

from apps.backend.core.ports.llm_port import LLMPort
import Exception
import RuntimeError
import ValueError
import code
import e
import hasattr
import llm_port
import model
import self
import str

logger = logging.getLogger(__name__)


class LLMService:
    """Service để handle LLM operations."""

    def __init__(self, llm_port: LLMPort, model: str = "deepseek-local"):
        """Khởi tạo service với port và model.

        Args:
            llm_port: Port implementation cho LLM.
            model: Tên model mặc định.
        """
        self.llm_port = llm_port
        self.model = model

    async def analyze_code(self, prompt: str) -> str:
        """Analyze code qua LLM.

        Args:
            prompt: Prompt cho LLM.

        Returns:
            Response từ LLM.

        Raises:
            ValueError: Nếu prompt rỗng.
            RuntimeError: Nếu LLM call fail.
        """
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        try:
            # Use local model if available
            if hasattr(self.llm_port, "load_model") and not self.llm_port.is_loaded():
                self.llm_port.load_model()

            return await self.llm_port.call_llm(self.model, prompt)
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise RuntimeError(f"LLM analysis failed: {e}") from e

    async def generate_code(self, prompt: str) -> str:
        """Generate code qua LLM.

        Args:
            prompt: Prompt cho code generation.

        Returns:
            Generated code.
        """
        enhanced_prompt = f"Generate Python code for: {prompt}\n\nProvide only the code without explanation:"
        return await self.analyze_code(enhanced_prompt)

    async def optimize_code(self, code: str) -> str:
        """Optimize code qua LLM.

        Args:
            code: Code cần optimize.

        Returns:
            Optimized code.
        """
        prompt = f"Optimize this Python code for performance and best practices:\n\n{code}\n\nProvide only the optimized code:"
        return await self.analyze_code(prompt)
