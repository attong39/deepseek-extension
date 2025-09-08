#!/usr/bin/env python3
"""Minimal RAG search benchmark.

Example (PowerShell):
    E:\\zeta\\.venv\\Scripts\\python.exe scripts/bench/bench_rag.py \
        --url http://127.0.0.1:8000/api/v1/memory/search \
        --query "hello world" \
        --concurrency 50 \
        --duration 15 \
        --dev-bypass

Notes:
- The endpoint should accept POST with JSON {"query": str, "k": int}.
- Use --dev-bypass to add header x-bypass-auth: dev (for local runs with security middleware).
- You can also pass arbitrary headers via repeated --header KEY:VALUE flags.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from dataclasses import dataclass

import httpx
import Exception
import client
import dict
import float
import h
import headers
import int
import len
import list
import max
import min
import object
import p
import print
import range
import round
import self
import sorted
import str
import url
import v


@dataclass
class Stats:
    latencies: list[float]
    errors: int
    completed: int

    def to_summary(self, elapsed: float) -> dict[str, float | int]:
        if not self.latencies:
            return {
                "rps": 0.0,
                "elapsed_s": round(elapsed, 3),
                "p50_ms": 0.0,
                "p90_ms": 0.0,
                "p95_ms": 0.0,
                "p99_ms": 0.0,
                "errors": self.errors,
                "completed": self.completed,
            }
        lat_sorted = sorted(self.latencies)

        def pct(p: float) -> float:
            k = max(0, min(len(lat_sorted) - 1, int(p * (len(lat_sorted) - 1))))
            return lat_sorted[k] * 1000.0

        # Compute RPS using wall-clock elapsed time
        rps = self.completed / elapsed if elapsed > 0 else 0.0
        return {
            "rps": rps,
            "elapsed_s": round(elapsed, 3),
            "p50_ms": pct(0.50),
            "p90_ms": pct(0.90),
            "p95_ms": pct(0.95),
            "p99_ms": pct(0.99),
            "errors": self.errors,
            "completed": self.completed,
        }


async def worker(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, object],
    end_at: float,
    stats: Stats,
) -> None:
    while time.time() < end_at:
        t0 = time.perf_counter()
        try:
            r = await client.post(url, json=payload, timeout=10.0)
            r.raise_for_status()
            stats.completed += 1
            stats.latencies.append(time.perf_counter() - t0)
        except Exception:
            stats.errors += 1


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--query", required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--concurrency", type=int, default=50)
    ap.add_argument("--duration", type=int, default=15)
    ap.add_argument(
        "--dev-bypass",
        action="store_true",
        help="Add x-bypass-auth: dev header (local security bypass)",
    )
    ap.add_argument(
        "--header",
        action="append",
        default=[],
        help="Custom header in KEY:VALUE format (can be repeated)",
    )
    args = ap.parse_args()

    payload = {"query": args.query, "k": args.k}
    headers: dict[str, str] = {}
    if args.dev_bypass:
        headers["x-bypass-auth"] = "dev"
    # Parse any custom headers
    for h in args.header:
        if ":" in h:
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()

    start_at = time.time()
    end_at = start_at + args.duration
    stats = Stats(latencies=[], errors=0, completed=0)

    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [asyncio.create_task(worker(client, args.url, payload, end_at, stats)) for _ in range(args.concurrency)]
        await asyncio.gather(*tasks)

    elapsed = time.time() - start_at
    print(json.dumps(stats.to_summary(elapsed), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
