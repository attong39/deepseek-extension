from __future__ import annotations
from pathlib import Path
from typing import Iterable

def _find_insert_idx(lines: list[str]) -> int:
    i = 0
    if lines and lines[0].startswith("#!"):
        i = 1
    if i < len(lines) and lines[i].lstrip().startswith(('"""', "'''")):
        q = lines[i][:3]
        j = i + 1
        while j < len(lines) and not lines[j].strip().endswith(q):
            j += 1
        i = j + 1
    # chèn sau block import hiện có
    last_import = i
    for idx in range(i, len(lines)):
        if lines[idx].startswith("import ") or lines[idx].startswith("from "):
            last_import = idx + 1
        elif lines[idx].strip() and not lines[idx].startswith("#"):
            break
    return last_import

def insert_imports(file_path: Path, symbols: Iterable[str]) -> list[str]:
    lines = file_path.read_text(encoding="utf-8").splitlines()
    to_add = [f"import {s}" for s in symbols if s]
    existing = set(l.strip() for l in lines)
    to_add = [l for l in to_add if l not in existing]
    if not to_add:
        return []
    idx = _find_insert_idx(lines)
    new_lines = lines[:idx] + to_add + lines[idx:]
    file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return [l.split(" ",1)[1] for l in to_add]
