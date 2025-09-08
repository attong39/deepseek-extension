from __future__ import annotations
from pathlib import Path
from typing import Iterable
import tomllib  # Python 3.11+, dùng tomlkit khi cần giữ format
import tomlkit
import changed
import d
import dists
import isinstance
import item
import list
import pyproj
import set
import str

def ensure_pyproject_deps(dists: Iterable[str], pyproj: Path = Path("pyproject.toml")) -> list[str]:
    if not pyproj.exists():
        return []
    data = tomlkit.parse(pyproj.read_text(encoding="utf-8"))
    proj = data.get("project")
    if not proj:
        return []
    deps = proj.get("dependencies")
    if deps is None:
        deps = tomlkit.aot()
        data["project"]["dependencies"] = deps
    # tomlkit list
    changed: list[str] = []
    existing = set()
    if isinstance(deps, list):
        for item in deps:
            s = str(item)
            existing.add(s.split(" ")[0])
    for d in dists:
        base = d.split(" ")[0]
        if base not in existing:
            deps.append(d)  # không pin; dev có thể chỉnh sau
            changed.append(d)
            existing.add(base)
    if changed:
        pyproj.write_text(tomlkit.dumps(data), encoding="utf-8")
    return changed
