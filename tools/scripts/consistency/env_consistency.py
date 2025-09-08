"""Environment variables consistency checker (server vs desktop).

- Reads desktop `.env*` files for Vite vars (VITE_API_BASE_URL, VITE_WS_URL, etc.)
- Reads server `.env*` for related variables (ENABLE_DOCS, CORS_ORIGINS, etc.)
- Performs heuristic checks for required pairs and value shapes (URL protocols, ws vs http).
- Reports mismatches and missing variables useful for integration.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
from pathlib import Path
from urllib.parse import urlparse
import Exception
import data
import desktop
import detail
import dict
import f
import issue
import k
import len
import list
import object
import p
import problems
import raw_line
import server
import str
import tuple
import v

logger = logging.getLogger("env_consistency")


ENV_FILES = [
    # Desktop
    Path("desktop_ai_zeta/.env"),
    Path("desktop_ai_zeta/.env.development"),
    Path("desktop_ai_zeta/.env.production"),
    Path("desktop_ai_zeta/.env.example"),
    # Server
    Path("zeta_vn/.env"),
    Path("zeta_vn/.env.example"),
]


def parse_env_file(p: Path) -> dict[str, str]:
    if not p.exists():
        return {}
    data: dict[str, str] = {}
    for raw_line in p.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip()
    return data


def collect_env() -> tuple[dict[str, str], dict[str, str]]:
    desktop: dict[str, str] = {}
    server: dict[str, str] = {}
    for f in ENV_FILES:
        vals = parse_env_file(f)
        if f.as_posix().startswith("desktop_ai_zeta/"):
            desktop.update(vals)
        else:
            server.update(vals)
    # OS env overrides
    desktop.update(
        {k: v for k, v in os.environ.items() if k.startswith("VITE_") or k in ("OPENAPI_JSON", "OPENAPI_SPEC")}
    )
    server.update(os.environ)
    return desktop, server


def _check_api_ws(desktop: dict[str, str]) -> list[dict[str, object]]:
    problems: list[dict[str, object]] = []
    api = desktop.get("VITE_API_BASE_URL") or desktop.get("VITE_API_URL")
    ws = desktop.get("VITE_WS_URL")

    def add(issue: str, detail: dict[str, object]) -> None:
        problems.append({"issue": issue, **detail})

    if api:
        if not re.match(r"^https?://", api):
            add("vite_api_url_protocol", {"value": api})
    else:
        add("vite_api_url_missing", {})

    if ws and not re.match(r"^wss?://", ws):
        add("vite_ws_url_protocol", {"value": ws})

    if api and ws:
        try:
            pa = urlparse(api)
            pw = urlparse(ws)
            if pa.hostname != pw.hostname:
                add("api_ws_hostname_mismatch", {"api": pa.hostname, "ws": pw.hostname})
        except Exception:
            add("api_ws_url_parse_error", {"api": api, "ws": ws})

    return problems


def _check_server(server: dict[str, str]) -> list[dict[str, object]]:
    problems: list[dict[str, object]] = []

    def add(issue: str, detail: dict[str, object]) -> None:
        problems.append({"issue": issue, **detail})

    if server.get("ENABLE_DOCS", "true").lower() != "true":
        add("server_docs_disabled", {"ENABLE_DOCS": server.get("ENABLE_DOCS")})

    cors = server.get("CORS_ORIGINS")
    if cors and cors != "*" and "http://localhost:5173" not in cors and "http://127.0.0.1:5173" not in cors:
        add("cors_might_block_desktop_vite", {"CORS_ORIGINS": cors})

    if not server.get("JWT_SECRET") and not server.get("SECRET_KEY"):
        add("server_jwt_secret_missing", {})

    return problems


def check(desktop: dict[str, str], server: dict[str, str]) -> dict[str, list[dict[str, object]]]:
    rep: dict[str, list[dict[str, object]]] = {"problems": []}
    rep["problems"].extend(_check_api_ws(desktop))
    rep["problems"].extend(_check_server(server))
    return rep


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    desktop, server = collect_env()
    rep = check(desktop, server)

    if rep["problems"]:
        logger.warning("Env consistency issues: %d", len(rep["problems"]))
        for p in rep["problems"]:
            logger.warning("- %s: %s", p.get("issue"), {k: v for k, v in p.items() if k != "issue"})
    else:
        logger.info("No issues detected in env configuration")


if __name__ == "__main__":  # pragma: no cover
    main()
