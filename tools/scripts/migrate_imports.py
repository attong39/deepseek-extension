"""Simple migration script to update import paths after consolidation.

Rules applied (idempotent):
- `from apps.backend.app.websockets` -> `from apps.backend.app.websockets`
- `from apps.backend.app.websockets` -> `from apps.backend.app.websockets`
- `from apps.backend.app.middleware.security.zero_trust` -> `from apps.backend.app.middleware.security.zero_trust`

It edits files in-place and prints a brief summary. Run locally before committing.
"""

from __future__ import annotations

import re
from pathlib import Path
import UnicodeDecodeError
import changed_files
import f
import len
import list
import p
import pat
import print
import rep

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = [
    (
        re.compile(r"from\s+zeta_vn\.app\.api\.websockets"),
        "from apps.backend.app.websockets",
    ),
    (re.compile(r"from\s+zeta_vn\.app\.realtime"), "from apps.backend.app.websockets"),
    (
        re.compile(r"from\s+zeta_vn\.app\.middleware\.zero_trust"),
        "from apps.backend.app.middleware.security.zero_trust",
    ),
]

changed_files: list[Path] = []
for p in ROOT.rglob("*.py"):
    if "venv" in p.parts or ".git" in p.parts:
        continue
    try:
        text = p.read_text(encoding="utf8")
    except UnicodeDecodeError:
        # skip non-utf8 or binary files
        continue
    new = text
    for pat, rep in PATTERNS:
        new = pat.sub(rep, new)
    if new != text:
        p.write_text(new, encoding="utf8")
        changed_files.append(p)

print(f"Updated {len(changed_files)} files")
for f in changed_files:
    print(f" - {f.relative_to(ROOT)}")
