"""
Report Generator - Create JSON and Markdown reports
"""
import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
import ImportError
import event
import issue
import len
import print
import reason
import result
import route
import str

try:
    from .utils import mask
except ImportError:
    from utils import mask


def write_reports(result: Dict[str, Any], out_dir: str | Path = "reports/consistency") -> None:
    """
    Write consistency check results to JSON and Markdown files.
    
    Args:
        result: Comparison result dictionary
        out_dir: Output directory for reports
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Add timestamp to result
    result["timestamp"] = datetime.now().isoformat()
    result["guard_version"] = "1.0.0"
    
    # Write JSON report (machine readable)
    json_file = out_dir / "result.json"
    json_file.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    # Write Markdown report (human readable)
    md_content = _generate_markdown_report(result)
    md_file = out_dir / "result.md"
    md_file.write_text(md_content, encoding="utf-8")
    
    print(f"📋 Reports written to:")
    print(f"   - JSON: {json_file}")
    print(f"   - Markdown: {md_file}")


def _generate_markdown_report(result: Dict[str, Any]) -> str:
    """Generate human-readable Markdown report."""
    
    severity = result["severity"]
    reasons = result.get("reasons", [])
    
    # Status emoji
    status_emoji = {
        "ok": "✅",
        "warn": "⚠️", 
        "fail": "❌"
    }
    
    emoji = status_emoji.get(severity, "❓")
    
    md_lines = [
        "# 🛡️ Consistency Guard Report",
        "",
        f"**Status**: {emoji} {severity.upper()}",
        f"**Timestamp**: {result.get('timestamp', 'unknown')}",
        f"**OpenAPI Hash**: `{result['openapi_hash']}`",
        ""
    ]
    
    # Summary section
    if reasons:
        md_lines.extend([
            "## 📊 Summary",
            ""
        ])
        for reason in reasons:
            md_lines.append(f"- {reason}")
        md_lines.append("")
    
    # Critical issues (if any)
    critical_issues = result.get("critical_issues", [])
    if critical_issues:
        md_lines.extend([
            "## ❌ Critical Issues (Will Fail CI)",
            ""
        ])
        for issue in critical_issues:
            md_lines.append(f"- {issue}")
        md_lines.append("")
    
    # Warning issues (if any)
    warning_issues = result.get("warning_issues", [])
    if warning_issues:
        md_lines.extend([
            "## ⚠️ Warning Issues (Non-blocking)",
            ""
        ])
        for issue in warning_issues:
            md_lines.append(f"- {issue}")
        md_lines.append("")
    
    # Statistics
    stats = result.get("stats", {})
    if stats:
        md_lines.extend([
            "## 📈 Statistics",
            "",
            "| Component | Backend | Frontend |",
            "|-----------|---------|----------|",
            f"| API Routes | {stats.get('backend_api_routes', 0)} | {stats.get('frontend_api_calls', 0)} |",
            f"| WebSocket Routes | {stats.get('backend_ws_routes', 0)} | {stats.get('frontend_ws_calls', 0)} |",
            f"| WebSocket Events | {stats.get('backend_ws_events', 0)} | {stats.get('frontend_events', 0)} |",
            f"| Feature Flags | {stats.get('backend_flags', 0)} | {stats.get('frontend_flags', 0)} |",
            ""
        ])
    
    # Detailed differences
    md_lines.extend([
        "## 🔍 Detailed Analysis",
        ""
    ])
    
    # API Routes
    api_diff = result.get("api", {})
    md_lines.extend([
        "### API Routes",
        f"- **Missing in Frontend**: {len(api_diff.get('missing_in_frontend', []))} routes",
        f"- **Extra in Frontend**: {len(api_diff.get('extra_in_frontend', []))} routes",
        ""
    ])
    
    if api_diff.get("missing_in_frontend"):
        md_lines.extend([
            "**Missing API routes:**",
            "```"
        ])
        for route in api_diff["missing_in_frontend"]:
            md_lines.append(route)
        md_lines.extend(["```", ""])
    
    if api_diff.get("extra_in_frontend"):
        md_lines.extend([
            "**Extra API routes:**",
            "```"
        ])
        for route in api_diff["extra_in_frontend"]:
            md_lines.append(route)
        md_lines.extend(["```", ""])
    
    # WebSocket Routes
    ws_diff = result.get("ws_routes", {})
    md_lines.extend([
        "### WebSocket Routes", 
        f"- **Missing in Frontend**: {len(ws_diff.get('missing_in_frontend', []))} routes",
        f"- **Extra in Frontend**: {len(ws_diff.get('extra_in_frontend', []))} routes",
        ""
    ])
    
    # WebSocket Events
    events_diff = result.get("ws_events", {})
    md_lines.extend([
        "### WebSocket Events",
        f"- **Missing in Frontend**: {len(events_diff.get('missing_in_frontend', []))} events", 
        f"- **Extra in Frontend**: {len(events_diff.get('extra_in_frontend', []))} events",
        ""
    ])
    
    if events_diff.get("missing_in_frontend"):
        md_lines.extend([
            "**Missing WebSocket events:**",
            "```"
        ])
        for event in events_diff["missing_in_frontend"]:
            md_lines.append(event)
        md_lines.extend(["```", ""])
    
    # Feature Flags
    flags_diff = result.get("feature_flags", {})
    md_lines.extend([
        "### Feature Flags",
        f"- **Backend flags not used in Frontend**: {len(flags_diff.get('missing_in_frontend', []))}",
        f"- **Frontend flags not defined in Backend**: {len(flags_diff.get('missing_in_backend', []))}",
        ""
    ])
    
    # Footer
    md_lines.extend([
        "---",
        "",
        f"Generated by Consistency Guard v{result.get('guard_version', '1.0.0')}",
        f"Report timestamp: {result.get('timestamp', 'unknown')}",
        ""
    ])
    
    return "\n".join(md_lines)
