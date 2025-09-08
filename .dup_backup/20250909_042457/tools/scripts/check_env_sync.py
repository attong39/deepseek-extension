#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import SystemExit
import e
import errors
import lines
import list
import ln
import out
import print
import set
import sorted
import str

ROOT = Path(__file__).resolve().parent.parent
shared = (ROOT / "contracts" / "env" / "shared.env.example").read_text(encoding="utf-8").splitlines()
server = (ROOT / "zeta_vn" / ".env.example").read_text(encoding="utf-8").splitlines()
desktop = (ROOT / "desktop_ai_zeta" / ".env.example").read_text(encoding="utf-8").splitlines()


def keys(lines: list[str]) -> set[str]:
    out: set[str] = set()
    for ln in lines:
        line = ln.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k = line.split("=", 1)[0].strip()
            out.add(k)
    return out


ks = keys(shared)
kv = keys(server)
kd = keys(desktop)

errors: list[str] = []

# Shared phải là tập con của cả server và desktop
missing_in_server = ks - kv
missing_in_desktop = ks - kd
if missing_in_server:
    errors.append("Server .env.example missing keys from shared: " + ", ".join(sorted(missing_in_server)))
if missing_in_desktop:
    errors.append("Desktop .env.example missing keys from shared: " + ", ".join(sorted(missing_in_desktop)))

# Cảnh báo: phần dư so với shared (không fail)
extra_server = kv - ks
extra_desktop = kd - ks
if extra_server:
    print(
        "[check_env_sync] Server has extra keys (ok but review):",
        ", ".join(sorted(extra_server)),
    )
if extra_desktop:
    print(
        "[check_env_sync] Desktop has extra keys (ok but review):",
        ", ".join(sorted(extra_desktop)),
    )

if errors:
    for e in errors:
        print("[check_env_sync]", e)
    raise SystemExit(1)

print("[check_env_sync] ENV keys are in sync across shared/server/desktop")
