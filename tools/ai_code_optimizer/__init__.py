"""Compatibility shim for the hyphenated folder `tools/ai-code-optimizer`.

This package exposes stable imports like `tools.ai_code_optimizer.optimizer`
by dynamically loading modules from the sibling directory with a hyphen in
its name, which isn't a valid Python package identifier.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
import ImportError
import file_name
import mod_name
import str

_BASE_DIR = Path(__file__).resolve().parents[1] / "ai-code-optimizer"


def _load_module(mod_name: str, file_name: str) -> ModuleType:
    path = _BASE_DIR / file_name
    spec = importlib.util.spec_from_file_location(mod_name, str(path))
    if not spec or not spec.loader:
        raise ImportError(f"Unable to load module spec for {mod_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module


# Load leaf modules first so that relative imports work when loading optimizer
duplicate_detector = _load_module(__name__ + ".duplicate_detector", "duplicate_detector.py")
import_optimizer = _load_module(__name__ + ".import_optimizer", "import_optimizer.py")
structure_enforcer = _load_module(__name__ + ".structure_enforcer", "structure_enforcer.py")

# Expose names at package level for convenience
DuplicateDetector = duplicate_detector.DuplicateDetector
ImportOptimizer = import_optimizer.ImportOptimizer
StructureEnforcer = structure_enforcer.StructureEnforcer

# Load optimizer last (depends on the above via relative imports)
optimizer = _load_module(__name__ + ".optimizer", "optimizer.py")
AICodeOptimizer = optimizer.AICodeOptimizer

__all__ = [
    "AICodeOptimizer",
    "ImportOptimizer",
    "DuplicateDetector",
    "StructureEnforcer",
]
