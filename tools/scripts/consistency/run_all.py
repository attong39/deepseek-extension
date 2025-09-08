"""Run all server–desktop consistency checks and summarize results.

Checks:
- OpenAPI vs Desktop endpoints
- WebSocket event schemas
- i18n keys
- Env configuration

Usage:
  python tools/consistency/run_all.py

Use env OPENAPI_JSON to point to server spec if not running locally.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import cmd
import code
import dict
import int
import list
import object
import print
import str
import summary
import tuple

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools" / "consistency"


def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
    return p.returncode, out


def main() -> None:
    openapi_url = os.getenv("OPENAPI_JSON") or "http://127.0.0.1:8000/openapi.json"

    reports_dir = ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)

    summary: dict[str, object] = {}

    # 1) OpenAPI
    code, out = run(
        [
            sys.executable,
            str(TOOLS / "openapi_consistency.py"),
            "--openapi-url",
            openapi_url,
            "--out",
            str(reports_dir / "consistency_openapi.json"),
        ]
    )
    print(out)
    summary["openapi_exit_code"] = code

    # 2) WS events
    code, out = run(
        [
            sys.executable,
            str(TOOLS / "ws_events_consistency.py"),
            "--out",
            str(reports_dir / "consistency_ws_events.json"),
        ]
    )
    print(out)
    summary["ws_events_exit_code"] = code

    # 3) i18n
    code, out = run(
        [
            sys.executable,
            str(TOOLS / "i18n_consistency.py"),
            "--out",
            str(reports_dir / "consistency_i18n.json"),
        ]
    )
    print(out)
    summary["i18n_exit_code"] = code

    # 4) env
    code, out = run(
        [
            sys.executable,
            str(TOOLS / "env_consistency.py"),
        ]
    )
    print(out)
    summary["env_exit_code"] = code

    (reports_dir / "consistency_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
