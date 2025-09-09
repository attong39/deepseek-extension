from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Any


CACHE_FILE = Path("tools/auto_fix/.cache/auto_fix_cache.json")


def file_sig(file_path: Path) -> str:
    """Generate a signature for a file based on mtime, size, and content hash."""
    try:
        stat = file_path.stat()
        hasher = hashlib.sha1()
        hasher.update(f"{stat.st_mtime_ns}:{stat.st_size}".encode())
        
        # Add light hash of first/last 4KB to catch edge cases
        content = file_path.read_bytes()
        if len(content) > 8192:
            hasher.update(content[:4096])
            hasher.update(content[-4096:])
        else:
            hasher.update(content)
        
        return hasher.hexdigest()
    except (OSError, IOError):
        return ""


def load_cache() -> Dict[str, Any]:
    """Load the auto-fix cache."""
    if not CACHE_FILE.exists():
        return {}
    
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache: Dict[str, Any]) -> None:
    """Save the auto-fix cache."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        CACHE_FILE.write_text(
            json.dumps(cache, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except OSError:
        pass  # Ignore cache write failures


def is_stale(file_path: Path, cache: Dict[str, Any]) -> bool:
    """Check if a file is stale (needs processing) based on cache."""
    if not file_path.exists():
        return False
    
    current_sig = file_sig(file_path)
    cached_sig = cache.get(str(file_path), {}).get("signature")
    
    return current_sig != cached_sig


def mark_fresh(file_path: Path, cache: Dict[str, Any]) -> None:
    """Mark a file as fresh (processed) in the cache."""
    cache[str(file_path)] = {
        "signature": file_sig(file_path),
        "processed": True
    }