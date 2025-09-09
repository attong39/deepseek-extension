from __future__ import annotations
import re
import os
from pathlib import Path
from typing import Set, Optional

# Regex patterns for TypeScript analysis
IMPORT_NAMES_RE = re.compile(r'import\s+([^;]+)\s+from\s+[\'\"]+[^\'\"]+[\'\"]+', re.MULTILINE)
DEFAULT_RE = re.compile(r'^\s*([A-Za-z_][A-Za-z0-9_]*)')
NAMED_RE = re.compile(r'\{\s*([^}]+)\s*\}')
PASCAL_RE = re.compile(r'\b([A-Z][A-Za-z0-9_]*)\b')
JSX_TAG_RE = re.compile(r'<([A-Z][A-Za-z0-9_]*)')

# Common TypeScript/React symbols to ignore
IGNORE = {"JSON", "Date", "Promise", "Array", "Object", "String", "Number", "Boolean", "React", "console"}


def _imports_in(text: str) -> Set[str]:
    """Extract imported identifiers from TypeScript import statements."""
    out: Set[str] = set()
    for match in IMPORT_NAMES_RE.finditer(text):
        segment = match.group(1)
        
        # Check for default import
        default_match = DEFAULT_RE.search(segment)
        if default_match:
            out.add(default_match.group(1))
        
        # Check for named imports
        named_match = NAMED_RE.search(segment)
        if named_match:
            for token in named_match.group(1).split(","):
                name = token.strip().split(" as ")[-1].strip()
                if name:
                    out.add(name)
    
    return out


def scan_ts_file(path: Path) -> tuple[Set[str], Set[str]]:
    """Scan TypeScript file and return (imported_symbols, candidate_missing_symbols)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    imported = _imports_in(text)
    used = set(PASCAL_RE.findall(text)) | set(JSX_TAG_RE.findall(text))
    candidates = (used - imported) - IGNORE
    return imported, candidates


def find_component_source(symbol: str, start_file: Path) -> Optional[Path]:
    """Find source file for a TypeScript component."""
    search_roots = [start_file.parent, Path("apps/desktop/src"), Path("src")]
    extensions = [".tsx", ".ts", ".jsx", ".js"]
    
    for root in search_roots:
        if not root.exists():
            continue
            
        # Direct file match
        for ext in extensions:
            direct_path = root / f"{symbol}{ext}"
            if direct_path.exists():
                return direct_path
                
        # Index file match
        for ext in extensions:
            index_path = root / symbol / f"index{ext}"
            if index_path.exists():
                return index_path
        
        # Recursive search
        for ext in extensions:
            for found_path in root.rglob(f"{symbol}{ext}"):
                return found_path
    
    return None


def to_import_path(from_file: Path, target: Path) -> str:
    """Convert absolute paths to relative import path."""
    rel_path = os.path.relpath(target.with_suffix(""), from_file.parent)
    rel_path = rel_path.replace("\\", "/")
    
    if not rel_path.startswith("."):
        rel_path = "./" + rel_path
        
    return rel_path