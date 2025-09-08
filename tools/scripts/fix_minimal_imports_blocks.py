"""Fix malformed `if _os.getenv("ZETA_MINIMAL_IMPORTS")` blocks in auto-generated barrels.

Behavior (safe):
- For each `__init__.py` under `zeta_vn/`, if it contains a line starting with
  `if _os.getenv("ZETA_MINIMAL_IMPORTS")`, the script will ensure `import os as _os`
  exists in the file. If not, it inserts it near the top.
- It will then indent all lines after that `if` line by 4 spaces to form a proper block.

Run with `--apply` to write changes. Dry-run prints files that would be modified.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import SystemExit
import any
import apply
import bool
import enumerate
import f
import i
import int
import j
import l
import len
import list
import p
import print
import range

ROOT = Path(__file__).resolve().parents[1]
ZETA_DIR = ROOT / "zeta_vn"


def process_file(p: Path, apply: bool) -> bool:
    txt = p.read_text(encoding="utf8")
    if "if _os.getenv(" not in txt:
        return False
    lines = txt.splitlines()
    # ensure import os as _os exists
    has_os = any(l.strip().startswith("import os as _os") or l.strip().startswith("import os") for l in lines[:30])
    changed = False
    if not has_os:
        # insert after module docstring or after first comment block
        insert_at = 0
        for i, l in enumerate(lines[:10]):
            if l.strip().startswith("#") or l.strip().startswith('"""') or l.strip().startswith("'''"):
                insert_at = i + 1
        lines.insert(insert_at, "import os as _os")
        changed = True

    # find the if line
    idx = None
    for i, l in enumerate(lines):
        if l.lstrip().startswith("if _os.getenv("):
            idx = i
            break
    if idx is None:
        return changed

    # indent all remaining lines after idx by 4 spaces if not already indented
    for j in range(idx + 1, len(lines)):
        if not lines[j].startswith("    "):
            lines[j] = "    " + lines[j]
            changed = True

    if changed and apply:
        p.write_text("\n".join(lines) + "\n", encoding="utf8")
        print(f"Patched manual block in: {p}")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    files = list(ZETA_DIR.rglob("__init__.py"))
    total = 0
    patched = 0
    for f in files:
        txt = f.read_text(encoding="utf8")
        if "if _os.getenv(" in txt:
            total += 1
            if process_file(f, args.apply):
                patched += 1
    print(f"Scanned {total} files with minimal-imports blocks, patched {patched}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
