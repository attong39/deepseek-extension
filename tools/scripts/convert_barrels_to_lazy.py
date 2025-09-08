"""
Convert package __init__.py barrel files that use `from . import X` into
lazy-import barrels using PEP 562 (__getattr__).

Safe rules:
- Only modify __init__.py files under the workspace that contain `from . import`.
- Preserve module docstring and non-barrel lines (try/except blocks, existing __all__).
- Create __all__ auto from imported names when missing.
- Add __getattr__ and __dir__ to lazy-load submodules on attribute access.
- Make a backup copy with .bak extension before writing.

Run: python tools/convert_barrels_to_lazy.py
"""

from __future__ import annotations

import re
from pathlib import Path
import Exception
import bool
import e
import i
import len
import line
import list
import ln
import n
import p
import part
import path
import print
import range
import str

ROOT = Path(__file__).resolve().parents[1]

BARREL_PATTERN = re.compile(r"^from \. import\s+(.+)$")
IMPORT_AS_PATTERN = re.compile(r"^\s*([A-Za-z0-9_]+)(?:\s+as\s+([A-Za-z0-9_]+))?\s*$")

SKIP_DIRS = {".venv", "node_modules", "build", "backup", "archive"}


def parse_barrel_lines(text: str) -> list[str]:
    names: list[str] = []
    for line in text.splitlines():
        m = BARREL_PATTERN.match(line.strip())
        if m:
            rhs = m.group(1)
            # handle comma-separated list
            parts = [p.strip() for p in rhs.split(",")]
            for part in parts:
                mm = IMPORT_AS_PATTERN.match(part)
                if mm:
                    orig = mm.group(1)
                    alias = mm.group(2) or orig
                    names.append(alias)
    return names


LATE_TEMPLATE = """
{header}

# NOTE: This file was converted to lazy imports by tools/convert_barrels_to_lazy.py
# to avoid eager imports in package barrels. Keep manual additions below.

{preserve}

__all__ = [{all_list}]

def __getattr__(name: str):
    if name in __all__:
        mod = __import__(f"{pkg_name}." + name, fromlist=[name])
        # if submodule exposes an attribute with same name, prefer it, else return module
        val = getattr(mod, name, mod)
        globals()[name] = val
        return val
    raise AttributeError(name)


def __dir__():
    return sorted(list(__all__) + list(globals().keys()))
"""


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def process_init(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "from . import" not in text:
        return False

    names = parse_barrel_lines(text)
    if not names:
        return False

    # preserve docstring and other code except the matching barrel import lines
    lines = text.splitlines()
    # Preserve everything except direct `from . import ...` barrel lines.
    preserve_lines = [ln for ln in lines if not ln.strip().startswith("from . import")]
    # Keep original module docstring if present (first triple-quoted block)
    header = ""
    if preserve_lines and preserve_lines[0].strip().startswith(('"""', "'''")):
        # find closing docstring line
        delim = preserve_lines[0].strip()[:3]
        end_idx = None
        for i in range(1, len(preserve_lines)):
            if preserve_lines[i].strip().endswith(delim):
                end_idx = i
                break
        if end_idx is not None:
            header = "\n".join(preserve_lines[: end_idx + 1]).strip()

    preserve = "\n".join(preserve_lines).strip()

    pkg_name = ".".join(path.parent.relative_to(ROOT).parts)
    all_list = ", ".join([f'"{n}"' for n in names])

    new_text = LATE_TEMPLATE.format(
        header=header,
        preserve=preserve,
        all_list=all_list,
        pkg_name=pkg_name,
    ).lstrip()

    # backup
    bak = path.with_suffix(path.suffix + ".bak")
    path.replace(bak)
    path.write_text(new_text, encoding="utf-8")
    print(f"Converted: {path} -> backup: {bak}")
    return True


def main():
    changed = []
    for p in ROOT.rglob("__init__.py"):
        if should_skip(p):
            # skip virtualenv, node_modules, build etc.
            continue
        try:
            text = p.read_text(encoding="utf-8")
            if "from . import" not in text:
                print(f"Skipping (no barrel): {p}")
                continue
            print(f"Candidate: {p}")
            if process_init(p):
                changed.append(p)
            else:
                print(f"No barrel names parsed, skipping: {p}")
        except Exception as e:
            print(f"Failed to process {p}: {e}")
    print(f"Total converted: {len(changed)}")


if __name__ == "__main__":
    main()
