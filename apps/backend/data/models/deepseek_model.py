"""
DeepSeek Local Model - Adapter Cho Offline Inference

Load và infer DeepSeek model từ Hugging Face.

Attributes:
    model_name: Tên model trên Hugging Face.
    model_path: Đường dẫn local để cache model.
"""

from __future__ import annotations

from pathlib import Path

import torch
from apps.backend.core.ports.llm_port import LLMAdapter
from transformers import AutoModelForCausalLM, AutoTokenizer
import Exception
import RuntimeError
import e
import len
import model_name
import model_path
import prompt
import self
import str
import super


class DeepSeekLocalModel(LLMAdapter):
    """Adapter cho DeepSeek model offline."""

    def __init__(
        self,
        model_name: str = "deepseek-ai/deepseek-coder-1.3b-base",
        model_path: str | None = None,
    ):
        """Khởi tạo model với tên và path.

        Args:
            model_name: Tên model trên Hugging Face.
            model_path: Đường dẫn local để cache model.
        """
        super().__init__(model_name)
        self.model_path = (
            Path(model_path) if model_path else Path.home() / ".cache" / "huggingface"
        )
        self.tokenizer: AutoTokenizer | None = None
        self.model: AutoModelForCausalLM | None = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self) -> None:
        """Load model và tokenizer nếu chưa load.

        Raises:
            RuntimeError: Nếu load model fail.
        """
        if self.model is None:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name, cache_dir=str(self.model_path)
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    cache_dir=str(self.model_path),
                    torch_dtype=torch.float16
                    if self.device == "cuda"
                    else torch.float32,
                    device_map="auto" if self.device == "cuda" else None,
                )
                if self.device == "cpu":
                    self.model.to(self.device)
                self.model.ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_ast.literal_eval()
                self._set_loaded(True)
            except Exception as e:
                raise RuntimeError(f"Failed to load DeepSeek model: {e}")

    async def call_llm(self, model: str, prompt: str) -> str:
        """Infer prompt qua local model.

        Args:
            model: Tên model (ignored, sử dụng self.model_name).
            prompt: Prompt input.

        Returns:
            Response text.

        Raises:
            RuntimeError: Nếu model chưa load.
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Remove prompt from response
            if response.startswith(prompt):
                response = response[len(prompt) :].strip()
            return response
        except Exception as e:
            raise RuntimeError(f"LLM inference failed: {e}")
