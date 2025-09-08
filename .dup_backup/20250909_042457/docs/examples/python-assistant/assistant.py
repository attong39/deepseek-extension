#!/usr/bin/env python3
"""
Python Assistant – Chat with gpt-oss:20b via Ollama.
- Checks that the model is available (local or remote)
- Simple interactive loop
- Optional OLLAMA_API_KEY support for remote/proxied servers
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from enum import Enum
from pathlib import Path
from typing import Any

import requests
from pydantic import BaseModel, Field, ValidationError
import Exception
import KeyboardInterrupt
import ValueError
import any
import body
import bool
import cfg
import chat_history
import dict
import exc
import getattr
import input
import int
import language
import len
import list
import m
import max_tokens
import mode
import payload
import print
import self
import staticmethod
import str

# Shared constants
JSON_CT = "application/json"


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role: user/assistant")
    content: str = Field(..., description="Message content")


class AssistantConfig(BaseModel):
    model: str = Field(default="gpt-oss:20b", description="Ollama model name")
    base_url: str = Field(default="http://127.0.0.1:11434", description="Ollama API base URL")
    timeout: int = Field(default=120, description="Timeout (sec)")
    max_tokens: int | None = Field(default=None, description="Optional max tokens")
    api_key: str | None = Field(default=None, description="Bearer token for remote Ollama")

    @staticmethod
    def from_env() -> AssistantConfig:
        # Lazy import to avoid optional dependency at import time
        try:  # pragma: no cover - optional convenience
            from dotenv import load_dotenv

            load_dotenv()
        except Exception:
            pass
        return AssistantConfig(
            model=os.getenv("OLLAMA_MODEL", "gpt-oss:20b"),
            # Support both OLLAMA_ENDPOINT and OLLAMA_API_URL
            base_url=os.getenv("OLLAMA_ENDPOINT", os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")),
            timeout=int(os.getenv("OLLAMA_TIMEOUT", "120")),
            max_tokens=int(os.getenv("OLLAMA_MAX_TOKENS", "0")) or None,
            api_key=os.getenv("OLLAMA_API_KEY"),
        )


class CopilotAssistant:
    """Lightweight completion helper using Ollama /api/generate."""

    def __init__(self, cfg: AssistantConfig) -> None:
        self.cfg = cfg

    def get_code_suggestion(self, context: str, language: str = "python") -> str:
        prompt = (
            f"You are an AI coding assistant. Provide code completion and suggestions for the "
            f"following {language} code. Provide only the code completion without explanations.\n\n"
            f"{context}\n"
        )
        headers: dict[str, str] = {"Content-Type": JSON_CT}
        if self.cfg.api_key:
            headers["Authorization"] = f"Bearer {self.cfg.api_key}"

        try:
            r = requests.post(
                f"{self.cfg.base_url}/api/generate",
                json={
                    "model": self.cfg.model,
                    "prompt": prompt,
                    "stream": False,
                },
                headers=headers,
                timeout=self.cfg.timeout,
            )
            r.raise_for_status()
            data = r.json()
            return str(data.get("response", ""))
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"


class TurboMode(str, Enum):
    STANDARD = "standard"
    TURBO = "turbo"
    EXTREME = "extreme"


class TurboAssistant:
    """Turbo completion helper with adjustable timeouts and models."""

    def __init__(self, cfg: AssistantConfig, mode: TurboMode = TurboMode.STANDARD) -> None:
        self.cfg = cfg
        self.mode = mode
        # Model preferences per mode; fall back to cfg.model
        self.turbo_models: dict[TurboMode, str] = {
            TurboMode.STANDARD: os.getenv("OLLAMA_MODEL_STANDARD", cfg.model),
            TurboMode.TURBO: os.getenv("OLLAMA_MODEL_TURBO", "deepseek-coder:6.7b"),
            TurboMode.EXTREME: os.getenv("OLLAMA_MODEL_EXTREME", "codellama:7b"),
        }

    def set_turbo_mode(self, mode: TurboMode) -> None:
        self.mode = mode

    def turbo_completion(self, prompt: str, language: str = "python", max_tokens: int | None = None) -> str:
        model = self.turbo_models.get(self.mode, self.cfg.model)
        # Shorter timeouts for faster feedback
        if self.mode == TurboMode.TURBO:
            timeout = 10
        elif self.mode == TurboMode.EXTREME:
            timeout = 8
        else:
            timeout = self.cfg.timeout

        body: dict[str, Any] = {
            "model": model,
            "prompt": (
                f"You are an AI coding assistant. Provide only the {language} code completion without explanations.\n\n"
                f"{prompt}\n"
            ),
            "stream": False,
        }
        if max_tokens or self.cfg.max_tokens:
            body.setdefault("options", {})["num_predict"] = max_tokens or self.cfg.max_tokens

        headers: dict[str, str] = {"Content-Type": JSON_CT}
        if self.cfg.api_key:
            headers["Authorization"] = f"Bearer {self.cfg.api_key}"

        start = time.time()
        try:
            r = requests.post(
                f"{self.cfg.base_url}/api/generate",
                json=body,
                headers=headers,
                timeout=timeout,
            )
            r.raise_for_status()
            data = r.json()
            return str(data.get("response", ""))
        except Exception as exc:  # noqa: BLE001
            return f"Error: {exc}"
        finally:
            elapsed = time.time() - start
            # Print timing info to stderr to avoid polluting completions
            print(f"⏱️  {self.mode.value} response: {elapsed:.2f}s", file=sys.stderr)


def call_ollama_api(config: AssistantConfig, messages: list[ChatMessage]) -> str:
    """Call Ollama chat API. Returns assistant text."""
    headers = {"Content-Type": JSON_CT}
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"

    payload: dict[str, Any] = {
        "model": config.model,
        "messages": [m.model_dump() for m in messages],
        "stream": False,
    }
    if config.max_tokens:
        payload["options"] = {"num_predict": config.max_tokens}

    r = requests.post(
        f"{config.base_url}/api/chat",
        json=payload,
        headers=headers,
        timeout=config.timeout,
    )
    r.raise_for_status()
    data = r.json()
    if "message" not in data or "content" not in data["message"]:
        raise ValueError("Invalid response from Ollama")
    return data["message"]["content"]


def check_model_exists(config: AssistantConfig) -> bool:
    try:
        r = requests.get(f"{config.base_url}/api/tags", timeout=10)
        r.raise_for_status()
        return any(m.get("name") == config.model for m in r.json().get("models", []))
    except requests.RequestException as exc:  # noqa: PERF203
        raise requests.RequestException(f"Unable to check model: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python Assistant / Copilot Mode")
    parser.add_argument("context", nargs="*", help="Optional context text for completion mode")
    parser.add_argument("--generate", action="store_true", help="Run Copilot completion mode (/api/generate)")
    parser.add_argument("--language", default="python", help="Language hint for completion prompts")
    parser.add_argument("--review", action="store_true", help="Review code (simple prompt via chat API)")
    parser.add_argument(
        "--mode",
        choices=[m.value for m in TurboMode],
        default=TurboMode.STANDARD.value,
        help="Turbo mode speed preset",
    )
    parser.add_argument("--max-tokens", type=int, default=None, help="Optional max tokens for completion")
    return parser


def read_context_from_input(args: argparse.Namespace) -> str:
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raw = " ".join(getattr(args, "context", [])).strip()
    if raw and len(getattr(args, "context", [])) == 1:
        try:
            p = Path(raw)
            return p.read_text(encoding="utf-8") if p.exists() and p.is_file() else raw
        except Exception:
            return raw
    return raw


def run_generate(config: AssistantConfig, args: argparse.Namespace, context: str) -> None:
    turbo = TurboAssistant(config, TurboMode(args.mode))
    print(turbo.turbo_completion(context, args.language, args.max_tokens))


def run_review(config: AssistantConfig, args: argparse.Namespace, context: str) -> None:
    messages = [
        ChatMessage(
            role="user",
            content=(
                f"Review this {args.language} code for issues and improvements. "
                f"Return a concise bullet list.\n\n{context}"
            ),
        )
    ]
    print(call_ollama_api(config, messages))


def run_interactive_chat(config: AssistantConfig) -> None:
    print("🚀 Python Assistant (GPT‑OSS:20B)")
    print("Type a prompt or 'exit' to quit.\n")

    try:
        if not check_model_exists(config):
            print(f"✖ Model {config.model} not found.")
            print(f"👉 Run: ollama pull {config.model}")
            sys.exit(1)
    except requests.RequestException as exc:
        print(f"✖ Cannot reach Ollama API at {config.base_url}: {exc}")
        sys.exit(1)

    chat_history: list[ChatMessage] = []
    try:
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("👋 Bye!")
                break

            chat_history.append(ChatMessage(role="user", content=user_input))
            try:
                reply = call_ollama_api(config, chat_history)
            except (requests.Timeout, requests.RequestException, ValueError) as exc:
                print(f"✖ Error: {exc}")
                continue

            print(f"Assistant: {reply}\n")
            chat_history.append(ChatMessage(role="assistant", content=reply))

    except KeyboardInterrupt:
        print("\n👋 Stopped.")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        config = AssistantConfig.from_env()
    except ValidationError as exc:  # pydantic validation
        print(f"✖ Config validation error: {exc}")
        sys.exit(1)

    if args.generate or args.review:
        context = read_context_from_input(args)
        if not context:
            print("No context provided.")
            sys.exit(2)
        if args.generate:
            run_generate(config, args, context)
            return
        run_review(config, args, context)
        return

    run_interactive_chat(config)


if __name__ == "__main__":
    main()
