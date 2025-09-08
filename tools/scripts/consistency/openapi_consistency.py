"""OpenAPI vs Desktop endpoints consistency checker.

This script verifies that API endpoints referenced by the Desktop app
(`desktop_ai_zeta/src/constants/index.ts`) exist in the server OpenAPI
specification exposed by `zeta_vn` (typically at `/openapi.json`).

Usage (PowerShell):
  # Using running server
  python tools/consistency/openapi_consistency.py --openapi-url http://127.0.0.1:8000/openapi.json

  # Using local file (e.g., exported to reports/openapi.json)
  python tools/consistency/openapi_consistency.py --openapi-file zeta_vn/reports/openapi.json

Outputs a summary to stdout and an optional JSON report via --out.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
import Exception
import FileNotFoundError
import RuntimeError
import dict
import e
import endpoints
import file
import int
import len
import list
import map
import openapi_url
import ordered
import p
import s
import seen
import set
import sorted
import str

try:
    import requests
except Exception:  # pragma: no cover - requests is expected in this repo
    requests = None  # type: ignore


logger = logging.getLogger("openapi_consistency")


@dataclass(frozen=True)
class CheckResult:
    total_desktop_endpoints: int
    matched: list[str]
    missing_in_openapi: list[str]
    extra_in_openapi: list[str]


def _read_openapi_paths(openapi_file: Path | None, openapi_url: str | None) -> set[str]:
    data: dict
    if openapi_file and openapi_file.exists():
        data = json.loads(openapi_file.read_text(encoding="utf-8"))
    else:
        if not openapi_url:
            raise RuntimeError("Provide --openapi-url or --openapi-file")
        if requests is None:
            raise RuntimeError("requests not available to fetch OpenAPI URL")
        resp = requests.get(openapi_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    paths = data.get("paths", {})
    return set(map(str, paths.keys()))


def _read_desktop_endpoints(file: Path) -> list[str]:
    """Extract endpoint paths declared in desktop `API` constants object.

    We collect string literal values like "/agents" and also attempt to parse
    template literals in arrow functions by extracting the static prefix
    between backticks (e.g., `/learning/jobs/${job_id}` -> `/learning/jobs/`).
    """
    content = file.read_text(encoding="utf-8")
    # Narrow to API object to reduce false positives
    m = re.search(r"export\s+const\s+API\s*=\s*\{([\s\S]*?)\}\s*as\s+const;", content)
    block = m.group(1) if m else content

    endpoints: set[str] = set()

    # 1) String literal values: key: "/path"
    for s in re.findall(r'"(/[^"`]+)"', block):
        # skip non-API strings (heuristic): must look like "/xxx"
        if s.startswith("/") and not s.startswith("/ws/"):
            endpoints.add(s)

    # 2) Template literal in arrow functions: `/foo/bar/${id}` -> `/foo/bar/`
    for s in re.findall(r"`(/[^`]+)`", block):
        if s.startswith("/") and not s.startswith("/ws/"):
            # remove ${...} segments conservatively -> prefix before first ${
            static_prefix = re.split(r"\$\{", s)[0]
            endpoints.add(static_prefix)

    # Normalize and deduplicate keeping order stable for reporting
    ordered: list[str] = []
    seen: set[str] = set()
    for e in endpoints:
        if e not in seen:
            ordered.append(e)
            seen.add(e)
    return ordered


def _prefix_with_api_v1(paths: Iterable[str]) -> list[str]:
    prefixed = []
    for p in paths:
        pp = "/api/v1" + (p if p.startswith("/") else f"/{p}")
        prefixed.append(pp)
    return prefixed


def check(openapi_paths: set[str], desktop_paths: list[str]) -> CheckResult:
    expected = set(_prefix_with_api_v1(desktop_paths))
    matched = sorted(expected & openapi_paths)
    missing = sorted(expected - openapi_paths)
    # Extra: paths in openapi that look like api/v1 but not referenced by desktop constants
    extra = sorted(p for p in openapi_paths if p.startswith("/api/v1/") and p not in expected)
    return CheckResult(
        total_desktop_endpoints=len(desktop_paths),
        matched=matched,
        missing_in_openapi=missing,
        extra_in_openapi=extra,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openapi-file", type=str, default=None)
    parser.add_argument("--openapi-url", type=str, default="http://127.0.0.1:8000/openapi.json")
    parser.add_argument(
        "--desktop-constants",
        type=str,
        default="desktop_ai_zeta/src/constants/index.ts",
    )
    parser.add_argument("--out", type=str, default=None, help="Write JSON report to this path")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    openapi_file = Path(args.openapi_file) if args.openapi_file else None
    constants_path = Path(args.desktop_constants)

    if not constants_path.exists():
        raise FileNotFoundError(constants_path)

    openapi_paths = _read_openapi_paths(openapi_file, args.openapi_url)
    desktop_paths = _read_desktop_endpoints(constants_path)
    result = check(openapi_paths, desktop_paths)

    logger.info("Desktop endpoints: %d", result.total_desktop_endpoints)
    logger.info("Matched in OpenAPI: %d", len(result.matched))
    if result.missing_in_openapi:
        logger.warning(
            "Missing in OpenAPI (%d):\n%s",
            len(result.missing_in_openapi),
            "\n".join(result.missing_in_openapi),
        )
    else:
        logger.info("No missing endpoints from OpenAPI")
    logger.info("Extra in OpenAPI not referenced by desktop: %d", len(result.extra_in_openapi))

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
        logger.info("Report written: %s", out_path)


if __name__ == "__main__":  # pragma: no cover
    main()
