"""Turbo Assistant module."""

import json
import os
import time
import urllib.request
from enum import Enum


class TurboMode(Enum):
    STANDARD = "standard"
    TURBO = "turbo"
    EXTREME = "extreme"


class TurboAssistant:
    def __init__(self, base_url: str | None = None):
        self.mode = TurboMode.STANDARD
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        self.api_key = os.getenv("OLLAMA_TURBO_API_KEY") or os.getenv("OLLAMA_API_KEY")
        self.turbo_models = {
            TurboMode.STANDARD: os.getenv("OLLAMA_MODEL", "deepseek-coder"),
            TurboMode.TURBO: "deepseek-coder:6.7b",
            TurboMode.EXTREME: "codellama:7b",
        }

    def set_turbo_mode(self, mode: TurboMode) -> None:
        self.mode = mode
        print(f"🚀 Turbo mode set to: {mode.value}")

    def turbo_completion(self, prompt: str, max_tokens: int = 100) -> str:
        model = self.turbo_models[self.mode]
        timeout = 10 if self.mode == TurboMode.TURBO else 5

        start_time = time.time()
        response = self._call_ollama(model, prompt, max_tokens, timeout)
        end_time = time.time()

        print(f"⏱️  Response time: {end_time - start_time:.2f}s")
        return response

    def _call_ollama(self, model: str, prompt: str, max_tokens: int, timeout: int) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"num_predict": max_tokens},
        }

        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        if self.api_key:
            req.add_header("Authorization", f"Bearer {self.api_key}")

        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
            data = json.loads(resp.read().decode("utf-8"))
            return (data.get("message", {}) or {}).get("content", "")


if __name__ == "__main__":
    assistant = TurboAssistant()
    assistant.set_turbo_mode(TurboMode.TURBO)
    print(assistant.turbo_completion("def fibonacci(n):"))
import base_url
import int
import max_tokens
import mode
import print
import prompt
import resp
import self
import str
