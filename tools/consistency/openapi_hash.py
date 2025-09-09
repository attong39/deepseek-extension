#!/usr/bin/env python
"""openapi_hash.py — Tạo/kiểm tra OpenAPI hash và (tuỳ chọn) ghi vào TS constant.

- Nguồn OpenAPI: ưu tiên OPENAPI_URL; fallback file apps/backend/openapi.json; cuối cùng import app.
- Hash: sha256(json.dumps(sort_keys=True, separators=(",",":")))[0:12]
- Chế độ:
  --check  : chỉ kiểm tra, exit 1 nếu khác.
  --write  : cập nhật file TS (tạo nếu thiếu).
  --out    : đường dẫn file TS (mặc định apps/desktop/src/constants/OPENAPI_HASH.ts)

Usage:
  uv run python tools/consistency/openapi_hash.py --write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.consistency.openapi_loader import load_openapi

TS_TEMPLATE = """// AUTO-GENERATED. Do not edit by hand.
// Source: OpenAPI contract normalized SHA-256 (12 hex)
export const OPENAPI_HASH = "{hash}";
"""

def calc_hash(doc: dict) -> str:
    norm = json.dumps(doc, sort_keys=True, separators=(",",":")).encode("utf-8")
    return hashlib.sha256(norm).hexdigest()[:12]

def read_ts_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    txt = path.read_text(encoding="utf-8", errors="ignore")
    import re
    m = re.search(r'OPENAPI_HASH\s*=\s*["\']([0-9a-f]{12})["\']', txt)
    return m.group(1) if m else None

def write_ts_hash(path: Path, h: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TS_TEMPLATE.format(hash=h), encoding="utf-8")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out", default="apps/desktop/src/constants/OPENAPI_HASH.ts")
    args = ap.parse_args()

    openapi = load_openapi()
    h = calc_hash(openapi)
    out = Path(args.out)
    current = read_ts_hash(out)

    if args.check and current != h:
        print(f"[openapi-hash] mismatch: current={current or '<none>'} expected={h}")
        return 1

    if args.write and current != h:
        write_ts_hash(out, h)
        print(f"[openapi-hash] updated {out} → {h}")
    else:
        print(f"[openapi-hash] OK {current or h}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
