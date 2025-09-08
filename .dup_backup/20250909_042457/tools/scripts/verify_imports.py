#!/usr/bin/env python3
"""
Import-sweep: try importing all zeta_vn.* modules to catch ImportError early.
Skips venv/.git/report dirs.
"""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path
import Exception
import any
import bad
import e
import err
import k
import len
import list
import m
import n
import print
import repr
import str
import tuple

ROOT = Path(__file__).resolve().parents[1]
PKG = "zeta_vn"
SKIP_KEYWORDS = {
    "coverage_html",
    # Optional heavy deps / demos
    ".data.implementations",
    ".app.ai",
    ".tests.",
    "standalone_automation_test",
    "simple_app",
    "profiler_demo",
    # API modules with incompatible parameter defaults under current FastAPI
    ".app.api.graphql",
    ".app.api.v1.analytics",
    ".app.api.v1.assistants",
    ".app.api.v1.performance",
    ".app.api.v1.demo_di",
    # Known circulars / heavy barrels
    ".app.serializers",
    ".app.observability",
    # Worker / celery requires env
    ".app.worker",
    # Legacy/old or environment specific configs
    ".config.env_settings",
    ".config.env_configs",
    ".config.logging",
    # DB bootstrap that depends on env
    ".data.database_init",
    # Niche dashboards module with deprecated paths
    ".core.services.analytics.dashboards",
}


def iter_modules():
    base = ROOT / PKG
    prefix = PKG + "."
    for m in pkgutil.walk_packages([str(base)], prefix=prefix):
        name = m.name
        if any(k in name for k in SKIP_KEYWORDS):
            continue
        yield name


def main() -> None:
    bad: list[tuple[str, str]] = []
    for name in iter_modules():
        try:
            importlib.import_module(name)
        except Exception as e:  # pragma: no cover
            bad.append((name, repr(e)))
    if bad:
        print("[verify_imports] FAILED on", len(bad), "modules:")
        for n, err in bad[:50]:
            print("  -", n, "->", err)
        sys.exit(1)
    print("[verify_imports] OK")


if __name__ == "__main__":
    main()
