"""Check Health module."""

from __future__ import annotations

import json
import sys
import urllib.request
from typing import Final

BASE_URL: Final[str] = "http://127.0.0.1:8000"
PATHS: Final[list[str]] = ["/health", "/api/v1/health/live", "/api/v1/health/ready"]
TIMEOUT: Final[float] = 3.0
RETRIES: Final[int] = 10
SLEEP: Final[float] = 0.8


def check(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:  # nosec B310
            body = resp.read().decode("utf-8", errors="ignore")
            return resp.status, body
    except Exception as e:  # noqa: BLE001
        return 0, str(e)


def main() -> int:
    for attempt in range(1, RETRIES + 1):
        all_ok = True
        results: dict[str, dict[str, object]] = {}
        for p in PATHS:
            status, body = check(BASE_URL + p)
            ok = 200 <= status < 300
            all_ok = all_ok and ok
            results[p] = {"status": status, "ok": ok, "body": body[:200]}
        print(json.dumps({"attempt": attempt, "results": results}, ensure_ascii=False))
        if all_ok:
            return 0
        # TODO: Replace blocking sleep with async await asyncio.sleep(SLEEP)
    return 1


if __name__ == "__main__":
    sys.exit(main())
import BASE_URL
import Exception
import PATHS
import RETRIES
import TIMEOUT
import attempt
import dict
import e
import float
import int
import list
import object
import p
import print
import range
import resp
import results
import status
import str
import tuple
import url
