from __future__ import annotations
import re
import os
from pathlib import Path
from typing import Set, Optional
import from_file
import m
import nm
import out
import path
import root
import set
import start_file
import str
import sym
import target
import tok
import tuple

# Bắt default + named import
IMPORT_NAMES_RE = re.compile(r'import\s+([^;]+)\s+from\s+[\'\"]+[^\'\"]+[\'\"]+', re.MULTILINE)
DEFAULT_RE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)')
NAMED_RE = re.compile(r'\{\s*([^}]+)\s*\}')
PASCAL_IDENT_RE = re.compile(r'\b([A-Z][A-Za-z0-9_]*)\b')
JSX_TAG_RE = re.compile(r'<([A-Z][A-Za-z0-9_]*)')

IGNORE = {"JSON","Date","Promise","Array","Object","String","Number","Boolean","React","console"}

def extract_imported_identifiers(text: str) -> Set[str]:
    out: Set[str] = set()
    for m in IMPORT_NAMES_RE.finditer(text):
        seg = m.group(1)
        d = DEFAULT_RE.search(seg)
        if d: 
            out.add(d.group(1))
        n = NAMED_RE.search(seg)
        if n:
            for tok in n.group(1).split(","):
                name = tok.strip().split(" as ")[-1].strip()
                if name: 
                    out.add(name)
    return out

def scan_ts_file(path: Path) -> tuple[Set[str], Set[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    imported = extract_imported_identifiers(text)
    used = set(PASCAL_IDENT_RE.findall(text))
    jsx = set(JSX_TAG_RE.findall(text))
    # các JSX tag nhiều khi là component tự định nghĩa -> vẫn cần import
    # nhưng component có thể đã import qua default/named -> loại trừ
    candidates = (used | jsx) - imported - IGNORE
    return imported, candidates

def find_component_source(sym: str, start_file: Path) -> Optional[Path]:
    """Tìm file export default/const Sym gần nhất: ./Sym.tsx, ./Sym/index.tsx, src/components/**/Sym.tsx"""
    roots = [start_file.parent, Path("apps/desktop/src"), Path("src")]
    names = [f"{sym}.tsx", f"{sym}.ts", f"{sym}.jsx", f"{sym}.js", f"{sym}/index.tsx", f"{sym}/index.ts"]
    for root in roots:
        if not root.exists():
            continue
        for nm in names:
            p = root / nm
            if p.exists():
                return p
        # tìm rộng hơn
        for p in root.rglob(f"{sym}.tsx"):
            return p
    return None

def to_import_path(from_file: Path, target: Path) -> str:
    rel = os.path.relpath(target.with_suffix(""), from_file.parent)
    rel = rel.replace("\\", "/")
    if not rel.startswith("."):
        rel = "./" + rel
    return rel
