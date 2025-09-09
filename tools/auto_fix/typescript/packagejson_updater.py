from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable


def ensure_dependencies(packages: Iterable[str], pkg_path: Path = Path("package.json")) -> list[str]:
    """
    Add packages to package.json dependencies if not already present.
    
    Args:
        packages: Packages to add
        pkg_path: Path to package.json
        
    Returns:
        List of packages that were added
    """
    if not pkg_path.exists():
        return []
        
    try:
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
    dependencies = data.get("dependencies", {})
    dev_dependencies = data.get("devDependencies", {})
    existing = set(dependencies.keys()) | set(dev_dependencies.keys())
    
    added: list[str] = []
    for pkg in sorted(set(packages)):
        if pkg not in existing:
            dependencies[pkg] = "latest"  # Or use specific version
            added.append(pkg)
    
    if added:
        data["dependencies"] = dependencies
        pkg_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    
    return added