from __future__ import annotations
from importlib.metadata import packages_distributions
from pathlib import Path
from typing import Iterable

def _module_to_dist(mod: str, mapping: dict[str, dict[str,str]]) -> str:
    """Map module name to distribution name."""
    m2d = packages_distributions()
    dist = (m2d.get(mod) or [None])[0]
    return dist or (mapping.get(mod, {}).get("python") or mod)

def ensure_requirements(modules: Iterable[str],
                        mapping: dict[str, dict[str,str]] | None = None,
                        req: Path = Path("requirements.txt")) -> list[str]:
    """Add missing distributions to requirements.txt; return list of packages added."""
    mapping = mapping or {}
    if not req.exists():
        req.touch()
        
    raw = req.read_text(encoding="utf-8").splitlines()
    existing = {ln.split("==")[0].strip() for ln in raw if ln.strip() and not ln.strip().startswith("#")}
    added: list[str] = []
    
    for mod in sorted(set(modules)):
        dist = _module_to_dist(mod, mapping)
        if dist not in existing:
            raw.append(f"{dist}  # AUTO-ADDED by auto_fix (from {mod})")
            existing.add(dist)
            added.append(dist)
    
    if added:
        req.write_text("\n".join(raw) + "\n", encoding="utf-8")
    
    return added