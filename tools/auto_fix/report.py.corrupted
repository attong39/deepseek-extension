from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime
import data
import dict
import len
import out_dir

def write_report(data: dict, out_dir: Path = Path("reports/auto_fix")) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Add timestamp and guard version
    data["timestamp"] = datetime.now().isoformat()
    data["guard_version"] = "1.0.0"
    
    # Write JSON report
    (out_dir / "report.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), 
        encoding="utf-8"
    )
    
    # Generate markdown report
    md = [
        "# Auto-Fix Report",
        f"Generated: {data['timestamp']}",
        "",
        "## Summary",
        f"- **Python**: imports_added={len(data['python']['imports_added'])}, reqs_added={len(data['python']['requirements_added'])}",
        f"- **TypeScript**: imports_added={len(data['ts']['imports_added'])}, deps_added={len(data['ts']['deps_added'])}",
        f"- **Unresolved**: {len(data.get('unresolved', []))}",
        "",
    ]
    
    if data['python']['imports_added']:
        md.extend([
            "## Python Imports Added",
            "```",
            *data['python']['imports_added'],
            "```",
            ""
        ])
    
    if data['python']['requirements_added']:
        md.extend([
            "## Python Requirements Added",
            "```",
            *data['python']['requirements_added'],
            "```",
            ""
        ])
    
    if data['ts']['imports_added']:
        md.extend([
            "## TypeScript Imports Added",
            "```",
            *data['ts']['imports_added'],
            "```",
            ""
        ])
    
    if data['ts']['deps_added']:
        md.extend([
            "## TypeScript Dependencies Added",
            "```",
            *data['ts']['deps_added'],
            "```",
            ""
        ])
    
    if data.get('unresolved'):
        md.extend([
            "## Unresolved Symbols",
            "```",
            *data['unresolved'],
            "```",
            ""
        ])
    
    (out_dir / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
