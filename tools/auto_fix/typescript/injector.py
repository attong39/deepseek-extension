from __future__ import annotations
from pathlib import Path
from typing import Iterable, Tuple
import added
import enumerate
import file_path
import i
import imports
import line
import list
import mod
import str
import sym
import tuple

def insert_imports_ts(file_path: Path, imports: list[tuple[str, str]]) -> list[str]:
    """
    imports: list of (symbol, module_path)
      - module_path: "./relative/path" hoặc "pkg"
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    last_import = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            last_import = i
    new_lines = lines[:]
    added: list[str] = []
    for sym, mod in imports:
        stmt = f'import {sym} from "{mod}";'
        if stmt in lines:
            continue
        insert_at = last_import + 1 if last_import >= 0 else 0
        new_lines = new_lines[:insert_at] + [stmt] + new_lines[insert_at:]
        last_import = insert_at  # giữ thứ tự nhóm
        added.append(stmt)
    if added:
        file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return added
