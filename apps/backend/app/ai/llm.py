# apps/backend/app/ai/llm.py
from __future__ import annotations
import os
import httpx
from typing import Sequence
import Exception
import base_url
import c
import client
import contexts
import ctxs
import enumerate
import i
import model
import q
import question
import self
import str

class LLMClient:
    """
    Ollama HTTP client (optional). If OLLAMA_URL not set,
    fallback returns a deterministic template answer.
    """
    def __init__(self, base_url: str | None = None, model: str | None = None) -> None:
        self.base_url = base_url or os.getenv("OLLAMA_URL")  # e.g. http://localhost:11434
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    async def generate(self, question: str, contexts: Sequence[str]) -> str:
        if self.base_url:
            try:
                async with httpx.AsyncClient(timeout=60) as client:
                    prompt = self._build_prompt(question, contexts)
                    r = await client.post(
                        f"{self.base_url}/api/generate",
                        json={"model": self.model, "prompt": prompt, "stream": False},
                    )
                    r.raise_for_status()
                    data = r.json()
                    return data.get("response", "").strip() or "No response."
            except Exception:
                # fall‑through to deterministic fallback
                pass

        # Deterministic fallback – guarantees the endpoint works offline
        top = "\n\n".join(contexts[:3])
        return (
            f"Câu hỏi: {question}\n\n"
            f"Tóm tắt ngữ cảnh (tối đa 3 đoạn):\n{top}\n\n"
            f"Trả lời (ước lượng): {question}"
        )

    def _build_prompt(self, q: str, ctxs: Sequence[str]) -> str:
        blocks = "\n\n".join(
            f"### Context #{i + 1}\n{c}" for i, c in enumerate(ctxs[:5])
        )
        return f"{blocks}\n\n### Question\n{q}\n\n### Answer (Vietnamese, concise):"
