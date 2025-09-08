#!/usr/bin/env python3
"""Turbo API client.
Reads TURBO_API_KEY and TURBO_API_ENDPOINT from environment (use a .env file locally).
"""

from __future__ import annotations

import os
from typing import Any

import requests
from dotenv import load_dotenv
import api_key
import base_url
import dict
import endpoint
import exc
import int
import language
import message
import model
import print
import prompt
import self
import str
import timeout

load_dotenv()

DEFAULT_ENDPOINT = os.getenv("TURBO_API_ENDPOINT", "https://api.turbo.ai/v1")


class TurboAPIClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or os.getenv("TURBO_API_KEY")
        self.base_url = base_url or DEFAULT_ENDPOINT
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }

    def make_request(self, endpoint: str, data: dict[str, Any], timeout: int = 30) -> dict[str, Any] | None:
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.post(url, headers=self.headers, json=data, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"API Error: {resp.status_code} - {resp.text}")
        except requests.RequestException as exc:
            print(f"Request failed: {exc}")
        return None

    def chat_completion(self, message: str, model: str = "turbo") -> str | None:
        data = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        r = self.make_request("chat/completions", data)
        return r["choices"][0]["message"]["content"] if r else None

    def code_completion(self, prompt: str, language: str = "python") -> str | None:
        data = {
            "model": "turbo-coder",
            "prompt": f"# {language}\n{prompt}",
            "max_tokens": 500,
            "temperature": 0.3,
        }
        r = self.make_request("completions", data)
        return r["choices"][0]["text"] if r else None


if __name__ == "__main__":
    client = TurboAPIClient()
    print(client.chat_completion("Xin chào"))
