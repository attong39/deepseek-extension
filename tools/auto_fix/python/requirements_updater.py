from __future__ import annotations
from pathlib import Path
from typing import Iterable, Set, Dict
from importlib.metadata import packages_distributions
import Exception
import added
import dict
import dists
import line
import list
import m
import mod
import modules
import req_path
import set
import sorted
import str

def _module_to_dist_map() -> Dict[str, str]:
    m: Dict[str, str] = {}
    try:
        for mod, dists in packages_distributions().items():
            if dists:
                m[mod] = dists[0]
    except Exception:
        pass  # fallback to empty mapping
    return m

def ensure_requirements(modules: Iterable[str],
                        req_path: Path = Path("requirements.txt"),
                        mapping: dict[str, dict[str, str]] | None = None) -> list[str]:
    """Thêm distribution còn thiếu vào requirements.txt; trả về danh sách package đã thêm."""
    mapping = mapping or {}
    mod2dist = _module_to_dist_map()
    if not req_path.exists():
        req_path.touch()
    existing = {line.split("==")[0].strip()
                for line in req_path.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.strip().startswith("#")}
    added: list[str] = []
    lines = req_path.read_text(encoding="utf-8").splitlines()
    for mod in sorted(set(modules)):
        dist = mod2dist.get(mod) or (mapping.get(mod, {}).get("python")) or mod
        if dist not in existing:
            lines.append(f"{dist}  # AUTO-ADDED by auto_fix (from {mod})")
            existing.add(dist)
            added.append(dist)
    if added:
        req_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return added
