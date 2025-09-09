from __future__ import annotations
import hashlib, json, os
from pathlib import Path
from typing import Dict
import Exception
import bool
import cache
import d
import f
import max
import p
import str

CACHE_FILE = Path("tools/auto_fix/.cache/auto_fix_cache.json")

def file_sig(p: Path) -> str:
    st = p.stat()
    h = hashlib.sha1()
    h.update(f"{st.st_mtime_ns}:{st.st_size}".encode())
    # thêm hash nhẹ 4KB đầu/cuối để tránh edge-case
    try:
        with p.open("rb") as f:
            head = f.read(4096)
            f.seek(max(0, st.st_size - 4096))
            tail = f.read(4096)
        h.update(head); h.update(tail)
    except Exception:
        pass
    return h.hexdigest()[:16]

def load_cache() -> Dict[str, str]:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_cache(d: Dict[str, str]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(d, indent=2), encoding="utf-8")

def is_stale(p: Path, cache: Dict[str, str]) -> bool:
    key = str(p).replace("\\", "/")
    sig = file_sig(p)
    return cache.get(key) != sig

def mark_fresh(p: Path, cache: Dict[str, str]) -> None:
    key = str(p).replace("\\", "/")
    cache[key] = file_sig(p)
