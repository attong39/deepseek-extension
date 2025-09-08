#!/usr/bin/env python3
"""Examples: TurboAPIClient code help and batch chat.
- Requires TURBO_API_KEY in environment (use .env locally)
- Optional TURBO_API_ENDPOINT (defaults from client)
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

# Local import from the same folder
from turbo_api_client import TurboAPIClient
import bool
import list
import print
import q
import queries
import str

load_dotenv()


def ensure_api_key() -> bool:
    key = os.getenv("TURBO_API_KEY", "")
    if not key:
        print("Missing TURBO_API_KEY. Create .env or set the variable and retry.")
        return False
    return True


def demo_code_help() -> None:
    client = TurboAPIClient()
    prompt = "def calculate_fibonacci(n):"
    print("[Turbo] Code help for:", prompt)
    code = client.code_completion(prompt, language="python")
    print(code or "<no response>")


def demo_batch_chat() -> None:
    queries: list[str] = [
        "Giải thích về machine learning",
        "Cách viết REST API trong Python",
        "Sự khác biệt giữa SQL và NoSQL",
    ]
    client = TurboAPIClient()
    for q in queries:
        a = client.chat_completion(q)
        print(f"Q: {q}\nA: {a}\n")


if __name__ == "__main__":
    if not ensure_api_key():
        sys.exit(1)

    # Run both demos
    demo_code_help()
    print("\n---\n")
    demo_batch_chat()
