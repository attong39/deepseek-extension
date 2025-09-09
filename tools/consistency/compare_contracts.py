"""
Contract Comparison - Analyze differences and determine severity
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Diff:
    """Contract difference representation."""
    missing_in_frontend: list[str]
    extra_in_frontend: list[str]


def _load_flags_map() -> dict[str, str]:
    """Load explicit backend -> frontend flag mapping from JSON file."""
    p = Path("tools/consistency/flags_map.json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def compare(frontend_scan: dict[str, set], backend_scan) -> dict[str, Any]:
    """
    Compare frontend and backend contracts to detect mismatches.
    
    Args:
        frontend_scan: Frontend scan results
        backend_scan: Backend scan results
        
    Returns:
        Comparison result with severity and detailed differences
    """
    print("🔄 Comparing frontend ↔ backend contracts...")
    
    # API routes comparison
    api_missing_fe = sorted(backend_scan.routes - frontend_scan["apis"])
    api_extra_fe = sorted(frontend_scan["apis"] - backend_scan.routes)
    
    # WebSocket routes comparison  
    ws_missing_fe = sorted(backend_scan.ws_routes - frontend_scan["wss"])
    ws_extra_fe = sorted(frontend_scan["wss"] - backend_scan.ws_routes)
    
    # WebSocket events comparison
    events_missing_fe = sorted(backend_scan.ws_events_spec - frontend_scan["events"])
    events_extra_fe = sorted(frontend_scan["events"] - backend_scan.ws_events_spec)
    
    # Feature flags comparison with explicit mapping
    flags_map = _load_flags_map()
    backend_flags = set(backend_scan.flags)
    
    # Map backend flag → expected VITE name (fallback VITE_<NAME>)
    backend_as_frontend = {flags_map.get(f, f"VITE_{f}") for f in backend_flags}
    frontend_flags = frontend_scan["flags"]
    
    flags_missing_fe = sorted(backend_as_frontend - frontend_flags)
    flags_missing_be = sorted(frontend_flags - backend_as_frontend)
    
    # Determine severity level
    severity = "ok"
    reasons = []
    
    # Critical issues (fail CI)
    critical_issues = []
    if api_missing_fe:
        critical_issues.append(f"{len(api_missing_fe)} API routes missing in frontend")
    if ws_missing_fe:
        critical_issues.append(f"{len(ws_missing_fe)} WebSocket routes missing in frontend") 
    if events_missing_fe:
        critical_issues.append(f"{len(events_missing_fe)} WebSocket events missing in frontend")
    
    if critical_issues:
        severity = "fail"
        reasons.append("Critical contract mismatches detected")
        
    # Warning issues (don't fail CI but should be reviewed)
    warning_issues = []
    if api_extra_fe:
        warning_issues.append(f"{len(api_extra_fe)} extra API routes in frontend")
    if ws_extra_fe:
        warning_issues.append(f"{len(ws_extra_fe)} extra WebSocket routes in frontend")
    if events_extra_fe:
        warning_issues.append(f"{len(events_extra_fe)} extra WebSocket events in frontend")
    if flags_missing_fe:
        warning_issues.append(f"{len(flags_missing_fe)} backend flags not used in frontend")
    if flags_missing_be:
        warning_issues.append(f"{len(flags_missing_be)} frontend flags not defined in backend")
        
    if warning_issues and severity == "ok":
        severity = "warn"
        reasons.append("Non-blocking contract drift detected")
    
    # Log results
    if severity == "fail":
        print("❌ Critical mismatches found:")
        for issue in critical_issues:
            print(f"   - {issue}")
    elif severity == "warn":
        print("⚠️  Warning issues found:")
        for issue in warning_issues:
            print(f"   - {issue}")
    else:
        print("✅ All contracts are in sync")
    
    return {
        "severity": severity,
        "reasons": reasons,
        "critical_issues": critical_issues,
        "warning_issues": warning_issues,
        
        "api": {
            "missing_in_frontend": api_missing_fe,
            "extra_in_frontend": api_extra_fe
        },
        
        "ws_routes": {
            "missing_in_frontend": ws_missing_fe, 
            "extra_in_frontend": ws_extra_fe
        },
        
        "ws_events": {
            "missing_in_frontend": events_missing_fe,
            "extra_in_frontend": events_extra_fe
        },
        
        "feature_flags": {
            "missing_in_frontend": flags_missing_fe,
            "missing_in_backend": flags_missing_be
        },
        
        "openapi_hash": backend_scan.openapi_hash,
        "stats": {
            "backend_api_routes": len(backend_scan.routes),
            "backend_ws_routes": len(backend_scan.ws_routes),
            "backend_ws_events": len(backend_scan.ws_events_spec),
            "backend_flags": len(backend_scan.flags),
            "frontend_api_calls": len(frontend_scan["apis"]),
            "frontend_ws_calls": len(frontend_scan["wss"]),
            "frontend_events": len(frontend_scan["events"]),
            "frontend_flags": len(frontend_scan["flags"])
        }
    }
