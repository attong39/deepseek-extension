#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import Exception
import SystemExit
import e
import print
import r
import str

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "zeta_vn"))

# Prefer running app directly if server isn't started; fallback to HTTP
try:
    from app.main import app  # type: ignore
    from fastapi.testclient import TestClient
except Exception:
    app = None  # type: ignore

out = ROOT / "contracts" / "openapi.json"

if app is not None:
    try:
        from fastapi.testclient import TestClient

        client = TestClient(app)
        resp = client.get("/openapi.json")
        resp.raise_for_status()
        out.write_text(json.dumps(resp.json(), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[export_openapi] wrote {out}")
        raise SystemExit(0)
    except Exception as e:
        print("[export_openapi] inline fetch failed, fallback to HTTP:", e)

# Fallback to HTTP
import urllib.request

base = os.environ.get("CONTRACT_API_BASE", "http://127.0.0.1:8000")
url = f"{base}/openapi.json"
with urllib.request.urlopen(url) as r:  # nosec
    data = r.read().decode("utf-8")
    out.write_text(data, encoding="utf-8")
print(f"[export_openapi] wrote {out}")
