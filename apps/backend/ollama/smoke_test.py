"""
Minimal smoke test for Ollama client.

Usage (Windows PowerShell):
    # Create venv and install deps
    python -m venv .venv-ollama
    .venv-ollama/Scripts/python.exe -m pip install -U pip
    .venv-ollama/Scripts/python.exe -m pip install httpx prometheus-client

    # Run test
    .venv-ollama/Scripts/python.exe apps/backend/ollama/smoke_test.py
"""

import asyncio

from client import OllamaConfig, create_client
import Exception
import dict
import e
import int
import isinstance
import print
import str


async def main() -> None:
    cfg = OllamaConfig()
    print(f"Connecting to Ollama at {cfg.host} ...")
    try:
        client = await create_client(cfg)
    except Exception as e:  # noqa: BLE001
        print(f"Failed to connect: {e}")
        return

    try:
        resp = await client.health_check()
        if resp.success:
            raw = resp.data if isinstance(resp.data, dict) else None
            version: str | None = None
            count: int | None = None
            if raw is not None:
                v = raw.get("version")
                version = str(v) if v is not None else None
                mc = raw.get("model_count")
                try:
                    count = int(mc) if mc is not None else None
                except Exception:  # noqa: BLE001
                    count = None
            print(f"OK: version={version}, model_count={count}")
            print(f"OK: version={version}, model_count={count}")
        else:
            print(f"Health check failed: {resp.error}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
