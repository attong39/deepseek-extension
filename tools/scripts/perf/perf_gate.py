from __future__ import annotations

import urllib.request  # stdlib
from contextlib import suppress
import json
import os
import subprocess
import sys
import time

import psutil  # type: ignore
import argparse

"""
Perf gate cho FastAPI: đo time-to-ready & RSS RAM.
Khởi chạy uvicorn app:app (hoặc main:app) ở cổng tạm, ping /healthz nếu có.
Fail nếu startup > budget hoặc RAM > budget_mb.
"""
def ping(url: str, timeout: float = 3.0) -> bool:
    """Ping URL để check health endpoint"""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.getcode() < 500
    except Exception:
        return False
def rss_mb(pid: int) -> float:
    """Lấy RSS memory usage in MB"""
    try:
    except Exception:
        return -1.0
    try:
        p = psutil.Process(pid)
        return p.memory_info().rss / (1024 * 1024)
    except Exception:
        return -1.0
def main():
    ap = argparse.ArgumentParser(description="Performance gate cho FastAPI server")
    ap.add_argument("--host", default="127.0.0.1", help="Host to bind server")
    ap.add_argument("--port", type=int, default=8099, help="Port to bind server")
    ap.add_argument("--app", default="zeta_vn.app.main:app", help="App module path")
    ap.add_argument("--startup-budget", type=float, default=3.0, help="Max startup time in seconds")
    ap.add_argument("--ram-budget-mb", type=float, default=300.0, help="Max RAM usage in MB")
    args = ap.parse_args()
    cmd = [
        "uv",
        "run",
        "python",
        "-m",
        "uvicorn",
        args.app,
        f"--host={args.host}",
        f"--port={args.port}",
        "--log-level=warning",
    ]
    print(f"Starting server: {' '.join(cmd)}")
    t0 = time.perf_counter()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        ready = False
        probes = [
            f"http://{args.host}:{args.port}/health",
            f"http://{args.host}:{args.port}/healthz",
            f"http://{args.host}:{args.port}/status",
            f"http://{args.host}:{args.port}/docs",
        ]
        print("Waiting for server to be ready...")
        while time.perf_counter() - t0 <= args.startup_budget:
            # TODO: Replace blocking sleep with async await asyncio.sleep(0.1)
            for probe_url in probes:
                if ping(probe_url, timeout=0.5):
                    ready = True
                    break
            if ready:
                break
        t_ready = time.perf_counter() - t0
        ram = rss_mb(proc.pid)
        with suppress(Exception):
            proc.terminate()
        with suppress(Exception):
            proc.wait(timeout=2.0)
        result = {
            "ready": ready,
            "startup_sec": round(t_ready, 3),
            "rss_mb": None if ram < 0 else round(ram, 1),
            "startup_budget": args.startup_budget,
            "ram_budget_mb": args.ram_budget_mb,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        failed_reasons = []
        if not ready:
            failed_reasons.append(f"Server not ready after {args.startup_budget}s")
        if t_ready > args.startup_budget:
            failed_reasons.append(f"Startup time {t_ready:.3f}s > {args.startup_budget}s budget")
        if ram > 0 and ram > args.ram_budget_mb:
            failed_reasons.append(f"RAM usage {ram:.1f}MB > {args.ram_budget_mb}MB budget")
        if failed_reasons:
            print("❌ PERF GATE FAILED:", file=sys.stderr)
            for reason in failed_reasons:
                print(f"  - {reason}", file=sys.stderr)
            sys.exit(2)
        else:
            print("✅ PERF GATE PASSED")
    finally:
        with suppress(Exception):
            proc.kill()
if __name__ == "__main__":
    main()