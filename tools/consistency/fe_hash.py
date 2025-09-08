from __future__ import annotations
from pathlib import Path
import re
import Exception
import path
import str

def read_fe_hash(path: str | Path = "apps/desktop/src/constants/OPENAPI_HASH.ts") -> str | None:
    """Read OpenAPI hash from frontend TypeScript constant file."""
    p = Path(path)
    if not p.exists(): 
        return None
    
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'OPENAPI_HASH\s*=\s*["\']([0-9a-f]{12})["\']', content)
        return m.group(1) if m else None
    except Exception:
        return None
