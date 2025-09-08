"""
Frontend Scanner - Extract contract usage from TypeScript/TSX files
Uses regex patterns for fast scanning without AST parsing
"""
import re
from pathlib import Path
from typing import Set, Dict, Iterable
import Exception
import e
import ext
import filepath
import len
import m
import print
import set
import str


# Regex patterns for contract extraction
API_RE = re.compile(
    r"""(?:fetch|axios\.(?:get|post|put|patch|delete))\s*\(\s*['"](/api/v1/[^'"]+)"""
)

WS_RE = re.compile(
    r"""new\s+WebSocket\s*\(\s*['"](?:(?:wss?|)://[^/]+)?(/api/v1/[^'"]+)"""
)

EVENT_RE = re.compile(
    r"""['"](?:event|type)['"]\s*:\s*['"]([a-zA-Z0-9\.\-_]+)['"]"""
)

VITE_RE = re.compile(
    r"""import\.meta\.env\.(VITE_[A-Z0-9_]+)"""
)

# Additional patterns for dynamic API construction
DYNAMIC_API_RE = re.compile(
    r"""['"](/api/v1/[^'"]*)\$\{[^}]+\}[^'"]*['"]"""
)

# Template literal patterns
TEMPLATE_API_RE = re.compile(
    r"""`(/api/v1/[^`]*)`"""
)


def _iter_typescript_files(root: Path) -> Iterable[Path]:
    """Iterate over all TypeScript files in directory tree."""
    for ext in ("*.ts", "*.tsx", "*.js", "*.jsx"):
        yield from root.rglob(ext)


def scan_frontend(root: str | Path) -> Dict[str, Set[str]]:
    """
    Scan frontend files for API usage, WebSocket endpoints, events, and flags.
    
    Args:
        root: Root directory to scan (e.g., apps/desktop/src)
        
    Returns:
        Dictionary with sets of found items:
        - apis: API endpoint paths
        - wss: WebSocket endpoint paths  
        - events: WebSocket event names
        - flags: Vite environment variables
    """
    root = Path(root)
    
    apis = set()
    wss = set() 
    events = set()
    flags = set()
    
    print(f"🔍 Scanning frontend files in: {root}")
    
    file_count = 0
    for filepath in _iter_typescript_files(root):
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            file_count += 1
            
            # Extract API calls
            apis.update(API_RE.findall(content))
            apis.update(DYNAMIC_API_RE.findall(content))
            apis.update(TEMPLATE_API_RE.findall(content))
            
            # Extract WebSocket endpoints
            wss.update(WS_RE.findall(content))
            
            # Extract event names (filter out empty matches)
            found_events = [m for m in EVENT_RE.findall(content) if m.strip()]
            events.update(found_events)
            
            # Extract Vite environment variables
            flags.update(VITE_RE.findall(content))
            
        except Exception as e:
            print(f"⚠️  Failed to read {filepath}: {e}")
            continue
    
    print(f"✅ Scanned {file_count} frontend files")
    print(f"   - Found {len(apis)} API endpoints")
    print(f"   - Found {len(wss)} WebSocket endpoints") 
    print(f"   - Found {len(events)} event types")
    print(f"   - Found {len(flags)} feature flags")
    
    return {
        "apis": apis,
        "wss": wss, 
        "events": events,
        "flags": flags
    }
