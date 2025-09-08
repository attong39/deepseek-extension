#!/usr/bin/env python3
"""
Minimal HTTP benchmark driver using httpx and asyncio.

Usage (PowerShell):
    E:\\zeta\\.venv\\Scripts\\python.exe scripts/bench/bench_api.py --url http://127.0.0.1:8000/api/v1/health --concurrency 50 --duration 15

Outputs a small JSON with RPS and latency percentiles.
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
import int
import len
import list
import max
import min
import p
import print
import range
import self
import sorted
import str
import sum
import url


@dataclass
class Stats:
    latencies: list[float]
    errors: int
    completed: int

    def to_summary(self) -> dict[str, float | int]:
        if not self.latencies:
            return {
                "rps": 0.0,
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

        duration = sum(lat_sorted)
        rps = self.completed / duration if duration > 0 else 0.0
        return {
            "rps": rps,
            "p50_ms": pct(0.50),
            "p90_ms": pct(0.90),
            "p95_ms": pct(0.95),
            "p99_ms": pct(0.99),
            "errors": self.errors,
            "completed": self.completed,
        }


async def worker(client: httpx.AsyncClient, url: str, end_at: float, stats: Stats) -> None:
    while time.time() < end_at:
        t0 = time.perf_counter()
        try:
            r = await client.get(url, timeout=10.0)
            r.raise_for_status()
            stats.completed += 1
            stats.latencies.append(time.perf_counter() - t0)
        except Exception:
            stats.errors += 1


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--concurrency", type=int, default=50)
    ap.add_argument("--duration", type=int, default=15)
    args = ap.parse_args()

    end_at = time.time() + args.duration
    stats = Stats(latencies=[], errors=0, completed=0)

    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(worker(client, args.url, end_at, stats)) for _ in range(args.concurrency)]
        await asyncio.gather(*tasks)

    print(json.dumps(stats.to_summary(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
