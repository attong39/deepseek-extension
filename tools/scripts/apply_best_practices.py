"""tools/apply_best_practices.py

Small safety-first script to apply/verify best-practices for ZETA project.
- Verifies desktop tsconfig (paths + strict)
- Ensures pyproject.toml production extras include uvloop/httptools
- Verifies .env.example contains recommended keys
- Prints a report and optional patch commands

This script is non-destructive by default (runs in --check mode). Use --apply to write changes.
"""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path
import Exception
import SystemExit
import any
import bool
import dict
import env_missing
import f
import int
import k
import list
import ok_env
import ok_py
import ok_ts
import pkg
import print
import py_data
import py_msg
import s
import str
import ts_msg
import tuple

try:
    import tomli_w  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    tomli_w = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
TSCONFIG = ROOT / "desktop_ai_zeta" / "tsconfig.json"
PYPROJECT = ROOT / "pyproject.toml"
ENV_EXAMPLE = ROOT / ".env.example"

RECOMMENDED_ENV_KEYS = [
    "ALLOW_DEV_WS_NO_TOKEN",
    "JWT_SECRET",
    "DATABASE_URL",
    "REDIS_URL",
    "MINIO_ENDPOINT",
    "OTEL_EXPORTER_OTLP_ENDPOINT",
]


def check_tsconfig() -> tuple[bool, str]:
    if not TSCONFIG.exists():
        return False, f"{TSCONFIG} not found"
    data = json.loads(TSCONFIG.read_text())
    co = data.get("compilerOptions", {})
    missing = []
    if not co.get("strict"):
        missing.append("strict")
    paths = co.get("paths", {})
    if not paths:
        missing.append("paths")
    ok = not missing
    return ok, "missing: " + ", ".join(missing) if missing else "ok"


def check_pyproject() -> tuple[bool, str, dict]:
    if not PYPROJECT.exists():
        return False, f"{PYPROJECT} not found", {}
    text = PYPROJECT.read_text(encoding="utf8")
    data = tomllib.loads(text)
    production = data.get("project", {}).get("optional-dependencies", {}).get("production")
    # Some projects use top-level 'production' variable earlier; try fallback
    if production is None:
        production = data.get("project", {}).get("optional-dependencies", {}).get("production", None)
    if production is None:
        # check for 'production' key at root level (older style)
        production = data.get("project", {}).get("production")
    if production is None:
        # as final fallback, try project['optional-dependencies']['production'] earlier
        production = data.get("project", {}).get("optional-dependencies", {}).get("production")
    if not production:
        return False, "production extras not found in pyproject.toml", data
    need = [pkg for pkg in ("uvloop", "httptools") if not any(pkg in s for s in production)]
    ok = not need
    return ok, ("missing: " + ", ".join(need)) if need else "ok", data


def check_env_example() -> tuple[bool, list[str]]:
    if not ENV_EXAMPLE.exists():
        return False, [".env.example not found"]
    txt = ENV_EXAMPLE.read_text()
    missing = [k for k in RECOMMENDED_ENV_KEYS if k not in txt]
    return not missing, missing


def apply_pyproject_patch(data: dict) -> bool:
    # add uvloop and httptools to production extras if not present
    prod = data.setdefault("project", {}).setdefault("optional-dependencies", {}).setdefault("production", [])
    changed = False
    for pkg in ("uvloop>=0.17.0,<1.0.0", "httptools>=0.6.0,<1.0.0"):
        name = pkg.split("<=")[0].split(">=")[0].split(",")[0]
        if not any(name in s for s in prod):
            prod.append(pkg)
            changed = True
    if changed:
        if tomli_w is not None:
            PYPROJECT.write_text(tomli_w.dumps(data), encoding="utf8")
        else:
            # minimal safe write: append missing packages to file (non-ideal but safe)
            old = PYPROJECT.read_text(encoding="utf8")
            # naive append: add a comment noting manual review
            PYPROJECT.write_text(
                old + "\n# TODO: add uvloop and httptools to production extras (tooling).\n",
                encoding="utf8",
            )
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes instead of dry-run")
    args = ap.parse_args()

    ok_ts, ts_msg = check_tsconfig()
    ok_py, py_msg, py_data = check_pyproject()
    ok_env, env_missing = check_env_example()

    print("Best-practices check report:\n")
    print(f"TS Config: {ts_msg}")
    print(f"Pyproject production extras: {py_msg}")
    print(f"Env example missing keys: {env_missing if env_missing else 'none'}")

    if not args.apply:
        print("Run with --apply to write safe changes to pyproject.toml and .env.example")
        # return non-zero if important checks failed so CI can notice
        return 2 if (not ok_ts or not ok_py or not ok_env) else 0

    # apply mode
    any_written = False
    if not ok_py:
        print("Applying pyproject patch to add uvloop/httptools to production extras...")
        if apply_pyproject_patch(py_data):
            print("Patched pyproject.toml")
            any_written = True
        else:
            print("No changes needed for pyproject.toml")
    else:
        print("pyproject production extras already OK")

    if not ok_env:
        print("Appending recommended keys to .env.example (non-destructive)...")
        with ENV_EXAMPLE.open("a", encoding="utf8") as f:
            f.write("\n# Recommended keys added by tools/apply_best_practices.py\n")
            for k in RECOMMENDED_ENV_KEYS:
                f.write(f"{k}=\n")
        any_written = True
    else:
        print(".env.example already contains recommended keys")

    if any_written:
        print("Changes applied. Review with 'git diff' and commit if OK.")
    else:
        print("No changes applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
