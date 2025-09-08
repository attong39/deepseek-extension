"""Normalize Rendered Files module."""

from pathlib import Path

# Move files created under duplicated zeta_vn\zeta_vn to single zeta_vn root
ROOT = Path(r"e:\zeta")
BAD_PREFIX = ROOT / "zeta_vn" / "zeta_vn"
GOOD_PREFIX = ROOT / "zeta_vn"

moved = []
for p in BAD_PREFIX.rglob("*"):
    if p.is_file():
        rel = p.relative_to(BAD_PREFIX)
        dst = GOOD_PREFIX / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        p.replace(dst)
        moved.append((str(p), str(dst)))

print("Moved files:")
for src, dst in moved:
    print(src, "->", dst)
import p
import print
import src
import str
