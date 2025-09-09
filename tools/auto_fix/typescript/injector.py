from __future__ import annotations
from pathlib import Path
from typing import Iterable, Tuple


def insert_imports_ts(file_path: Path, imports: list[tuple[str, str]]) -> list[str]:
    """
    Insert imports into TypeScript file.
    
    Args:
        file_path: Path to TypeScript file
        imports: List of (symbol, module_path) tuples
            - module_path: "./relative/path" or "package-name"
    
    Returns:
        List of added import statements
    """
    lines = file_path.read_text(encoding="utf-8").splitlines()
    added: list[str] = []
    
    # Find insertion point (after existing imports)
    insert_idx = _find_insert_point(lines)
    
    for sym, mod in imports:
        if _import_exists(lines, sym, mod):
            continue
            
        import_stmt = f'import {{ {sym} }} from "{mod}";'
        lines.insert(insert_idx, import_stmt)
        added.append(import_stmt)
        insert_idx += 1
    
    # Write back to file
    file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return added


def _find_insert_point(lines: list[str]) -> int:
    """Find the best place to insert new imports."""
    last_import_idx = -1
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('import ') and ' from ' in stripped:
            last_import_idx = i
    
    # Insert after last import, or at beginning if no imports
    return last_import_idx + 1 if last_import_idx >= 0 else 0


def _import_exists(lines: list[str], symbol: str, module: str) -> bool:
    """Check if import already exists."""
    for line in lines:
        stripped = line.strip()
        if (f'import {{ {symbol} }}' in stripped or 
            f'import {symbol}' in stripped) and f'from "{module}"' in stripped:
            return True
    return False