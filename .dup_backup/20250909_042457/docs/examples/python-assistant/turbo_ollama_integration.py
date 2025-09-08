#!/usr/bin/env python3
from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv
import Exception
import bool
import data
import dict
import exc
import print
import prompt
import self
import str
import use_turbo

load_dotenv()


class TurboOllamaHybrid:
    def __init__(self) -> None:
        self.turbo_api_key = os.getenv("TURBO_API_KEY")
        self.turbo_base = os.getenv("TURBO_API_ENDPOINT", "https://api.turbo.ai/v1")
        self.ollama_url = os.getenv("OLLAMA_ENDPOINT", "http://127.0.0.1:11434")

    def get_best_response(self, prompt: str, use_turbo: bool = True) -> str:
        if use_turbo and self.turbo_api_key:
            return self._call_turbo_api(prompt)
        return self._call_ollama(prompt)

    def _call_turbo_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.turbo_api_key}",
            "Content-Type": "application/json",
        }
        data: dict[str, Any] = {
            "model": "turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
        }
        try:
            r = requests.post(f"{self.turbo_base}/chat/completions", headers=headers, json=data, timeout=30)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"Turbo API Error: {r.status_code}"
        except Exception as exc:  # noqa: BLE001
            return f"Failed to call Turbo API: {exc}"

    def _call_ollama(self, prompt: str) -> str:
        try:
            r = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": os.getenv("OLLAMA_MODEL", "deepseek-coder"), "prompt": prompt, "stream": False},
                timeout=30,
            )
            if r.status_code == 200:
                return r.json().get("response", "")
            return f"Ollama Error: {r.status_code}"
        except Exception as exc:  # noqa: BLE001
            return f"Failed to call Ollama: {exc}"


if __name__ == "__main__":
    hybrid = TurboOllamaHybrid()
    print("Turbo:", hybrid.get_best_response("Giải thích về AI", use_turbo=True))
    print("Ollama:", hybrid.get_best_response("Giải thích về AI", use_turbo=False))
