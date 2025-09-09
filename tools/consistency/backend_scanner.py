"""
Backend Scanner - Extract contracts from backend code and specifications
"""
import json
import hashlib
import os
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class BackendScan(BaseModel):
    """Backend scan results."""
    routes: set[str]
    ws_routes: set[str] 
    flags: set[str]
    ws_events_spec: set[str]
    openapi_hash: str


def _hash_openapi(doc: dict) -> str:
    """
    Generate short SHA-256 hash of OpenAPI document for versioning.
    
    Args:
        doc: OpenAPI document dictionary
        
    Returns:
        First 12 characters of SHA-256 hash
    """
    normalized = json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(normalized).hexdigest()[:12]


def scan_backend(openapi_doc: dict[str, Any], repo_root: str | Path = ".") -> BackendScan:
    """
    Scan backend for API routes, WebSocket contracts, and feature flags.
    
    Args:
        openapi_doc: OpenAPI specification document
        repo_root: Repository root directory
        
    Returns:
        BackendScan with extracted contract information
    """
    repo_root = Path(repo_root)
    
    print("🔍 Scanning backend contracts...")
    
    # 1. Extract API routes from OpenAPI paths
    routes = set()
    for path in openapi_doc.get("paths", {}):
        if path.startswith("/api/"):
            routes.add(path)
    
    print(f"   - Found {len(routes)} API routes in OpenAPI")
    
    # 2. Load WebSocket events specification
    ws_events_spec = set()
    ws_contract_path = repo_root / "apps/backend/app/contracts/ws_events.json"
    
    if ws_contract_path.exists():
        try:
            spec = json.loads(ws_contract_path.read_text(encoding="utf-8"))
            ws_events_spec = set(spec.get("events", []))
            print(f"   - Found {len(ws_events_spec)} WebSocket events in contract")
        except Exception as e:
            print(f"⚠️  Failed to load WebSocket contract: {e}")
    else:
        print("⚠️  WebSocket contract file not found")
    
    # 3. Scan for WebSocket route definitions in Python files
    ws_routes = set()
    ws_route_pattern = re.compile(r'@router\.websocket\(["\'](/api/v1/[^"\']+)["\']\)')
    
    python_files = list(repo_root.rglob("*.py"))
    for py_file in python_files:
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            matches = ws_route_pattern.findall(content)
            ws_routes.update(matches)
        except Exception:
            continue
    
    print(f"   - Found {len(ws_routes)} WebSocket routes in code")
    
    # 4. Extract feature flags from environment variable usage
    flags = set()
    
    # Patterns for environment variable detection
    env_patterns = [
        re.compile(r'os\.getenv\(\s*["\']([A-Z0-9_]+)["\']'),  # os.getenv("FLAG")
        re.compile(r'env\s*=\s*["\']([A-Z0-9_]+)["\']'),       # Field(..., env="FLAG")
        re.compile(r'getenv\(\s*["\']([A-Z0-9_]+)["\']'),      # getenv("FLAG")
        re.compile(r'environ\.get\(\s*["\']([A-Z0-9_]+)["\']'), # environ.get("FLAG")
        re.compile(r'settings\.([A-Z0-9_]+)'),                 # settings.FLAG_NAME
    ]
    
    for py_file in python_files:
        try:
            content = py_file.read_text(encoding="utf-8", errors="ignore")
            
            for pattern in env_patterns:
                matches = pattern.findall(content)
                flags.update(matches)
                
        except Exception:
            continue
    
    # Filter out common non-feature flags
    excluded_flags = {
        "PATH", "HOME", "USER", "PYTHONPATH", "DATABASE_URL", "REDIS_URL",
        "SECRET_KEY", "JWT_SECRET", "API_KEY", "TOKEN", "PASSWORD"
    }
    flags = {f for f in flags if f not in excluded_flags}
    
    print(f"   - Found {len(flags)} feature flags")
    
    # 5. Generate OpenAPI hash for versioning
    openapi_hash = _hash_openapi(openapi_doc)
    print(f"   - OpenAPI hash: {openapi_hash}")
    
    return BackendScan(
        routes=routes,
        ws_routes=ws_routes,
        flags=flags, 
        ws_events_spec=ws_events_spec,
        openapi_hash=openapi_hash
    )
