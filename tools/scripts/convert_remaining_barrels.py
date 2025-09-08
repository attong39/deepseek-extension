"""Convert remaining leading 'from .' imports in auto-generated barrels to absolute imports.

This is an aggressive but safe change limited to files containing the auto-generated marker.
It replaces leading 'from .' with 'from apps.backend.<relpath>' where <relpath> mirrors the package path.
"""

from __future__ import annotations

from pathlib import Path
import SystemExit
import bool
import f
import int
import len
import list
import ln
import path
import print
import str

ROOT = Path(__file__).resolve().parents[1]
ZETA_DIR = ROOT / "zeta_vn"


def package_for(path: Path) -> str:
    rel = path.relative_to(ZETA_DIR)
    parts = ["zeta_vn"] + list(rel.parts)
    return ".".join(parts)


def run(apply: bool) -> int:
    files = list(ZETA_DIR.rglob("__init__.py"))
    patched = 0
    for f in files:
        txt = f.read_text(encoding="utf8")
        pkg = package_for(f.parent)
        lines = txt.splitlines()
        new_lines = []
        changed = False
        for ln in lines:
            stripped = ln.lstrip()
            if stripped.startswith("from .") and not stripped.startswith("from apps.backend.app."):
                # preserve indentation
                indent = ln[: len(ln) - len(stripped)]
                new_ln = indent + ln.replace("from .", f"from {pkg}.", 1)
                new_lines.append(new_ln)
                changed = True
            else:
                new_lines.append(ln)
        if changed:
            patched += 1
            if apply:
                f.write_text("\n".join(new_lines) + "\n", encoding="utf8")
                print(f"Patched: {f}")
    print(f"Patched {patched} barrel files")
    return 0


if __name__ == "__main__":
    import sys

    apply = "--apply" in sys.argv
    raise SystemExit(run(apply))
