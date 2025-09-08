"""Check Runtime Imports module."""

from __future__ import annotations

import importlib
import json

MODULES = [
    # app entry & DI
    "zeta_vn.app.main",
    "zeta_vn.app.di_container",
    "zeta_vn.app.dependencies",
    # routers
    "zeta_vn.app.api.v1.router",
    # auth/jwt
    "zeta_vn.app.auth.jwt_handler",
    "zeta_vn.app.security.jwt",
    # core (services/interfaces)
    "zeta_vn.core.services.agent.service",
    "zeta_vn.core.interfaces.repositories",
    # data (models/repositories) — chỉ kiểm tra tồn tại module
    "zeta_vn.data.models.base",
    "zeta_vn.data.repositories.sqlalchemy_user_repository",
    "zeta_vn.data.repositories.sqlalchemy_agent_repository",
    "zeta_vn.data.repositories.sqlalchemy_memory_repository",
]


def main() -> int:
    results: dict[str, str] = {}
    for mod in MODULES:
        try:
            importlib.import_module(mod)
            results[mod] = "ok"
        except Exception as e:  # noqa: BLE001 - report any runtime import error
            results[mod] = f"ERR:{type(e).__name__}:{e}"

    print(json.dumps(results, ensure_ascii=False, indent=2))
    # exit code: 0 if all ok, else 1
    if any(v.startswith("ERR:") for v in results.values()):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
import Exception
import SystemExit
import any
import dict
import e
import int
import mod
import print
import results
import str
import type
import v
