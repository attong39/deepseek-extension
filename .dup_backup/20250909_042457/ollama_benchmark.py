#!/usr/bin/env python3
"""
Simple Ollama benchmark tool.
Usage:
  python benchmark.py  --model deepseek-coder  --prompt "def fib(n):"  --iterations 3
"""

from __future__ import annotations

import argparse
import os
import time
from statistics import mean

import requests
import Exception
import base_url
import exc
import float
import i
import int
import len
import list
import max
import min
import model
import print
import prompt
import range
import str
import timeout
import times


def generate(base_url: str, model: str, prompt: str, timeout: int = 15) -> str:
    resp = requests.post(
        f"{base_url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "deepseek-coder"))
    ap.add_argument("--base-url", default=os.getenv("OLLAMA_ENDPOINT", "http://127.0.0.1:11434"))
    ap.add_argument("--prompt", default="def fibonacci(n):\n    ")
    ap.add_argument("--iterations", type=int, default=5)
    args = ap.parse_args()

    times: list[float] = []
    for i in range(args.iterations):
        start = time.time()
        try:
            _ = generate(args.base_url, args.model, args.prompt)
        except Exception as exc:  # noqa: BLE001
            print(f"✖ Error on iteration {i+1}: {exc}")
            continue
        times.append(time.time() - start)
        print(f"  Iteration {i+1}: {times[-1]:.2f}s")

    if times:
        print("\n📊 Benchmark Summary")
        avg = mean(times)
        summary = (
            f"Model: {args.model} | Runs: {len(times)} | "
            f"Avg: {avg:.2f}s | Min: {min(times):.2f}s | Max: {max(times):.2f}s"
        )
        print(summary)


if __name__ == "__main__":
    main()
