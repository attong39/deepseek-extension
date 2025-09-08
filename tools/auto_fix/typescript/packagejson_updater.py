from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable, List
import FileNotFoundError
import added
import list
import packages
import pkg
import pkg_path
import set
import sorted
import str

def ensure_dependencies(packages: Iterable[str], pkg_path: Path = Path("package.json")) -> list[str]:
    if not pkg_path.exists():
        return []
    try:
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
    deps = data.setdefault("dependencies", {})
    added: list[str] = []
    for pkg in sorted(set(packages)):
        if pkg not in deps:
            deps[pkg] = "latest"  # cố ý: dev có thể pin version sau
            added.append(pkg)
    if added:
        pkg_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return added
