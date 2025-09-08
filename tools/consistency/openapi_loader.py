"""
OpenAPI Loader - Multiple fallback strategies
1. HTTP endpoint (if OPENAPI_URL env var set)
2. Local file (openapi.json)
3. Direct import of FastAPI app
"""
import os
import json
import importlib
from pathlib import Path
from typing import Any, Dict
import Exception
import ImportError
import SystemExit
import e
import filepath
import getattr
import hasattr
import module_path
import print
import str


def load_openapi() -> Dict[str, Any]:
    """
    Load OpenAPI specification using multiple fallback strategies.
    
    Returns:
        OpenAPI specification as dictionary
        
    Raises:
        SystemExit: If all loading strategies fail
    """
    # Strategy 1: HTTP endpoint (for running servers)
    url = os.getenv("OPENAPI_URL")
    if url:
        try:
            import httpx
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
            print(f"✅ Loaded OpenAPI from HTTP: {url}")
            return response.json()
        except Exception as e:
            print(f"⚠️  HTTP load failed ({url}): {e}")

    # Strategy 2: Local file
    for filepath in (
        Path("apps/backend/openapi.json"), 
        Path("openapi.json"),
        Path("docs/openapi.json")
    ):
        if filepath.exists():
            try:
                content = json.loads(filepath.read_text(encoding="utf-8"))
                print(f"✅ Loaded OpenAPI from file: {filepath}")
                return content
            except Exception as e:
                print(f"⚠️  File load failed ({filepath}): {e}")

    # Strategy 3: Direct FastAPI app import
    try:
        # Try different possible module paths
        module_paths = [
            "apps.backend.app.main",
            "app.main", 
            "main"
        ]
        
        for module_path in module_paths:
            try:
                mod = importlib.import_module(module_path)
                app = getattr(mod, "app", None)
                if app and hasattr(app, "openapi"):
                    spec = app.openapi()
                    print(f"✅ Loaded OpenAPI from app import: {module_path}")
                    return spec
            except ImportError:
                continue
                
    except Exception as e:
        print(f"⚠️  App import failed: {e}")

    # All strategies failed
    raise SystemExit(
        "❌ [openapi_loader] Cannot load OpenAPI specification. "
        "Try setting OPENAPI_URL env var or ensure FastAPI app is importable."
    )
