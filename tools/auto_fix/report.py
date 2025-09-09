from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any


def write_report(data: Dict[str, Any], out_dir: Path = Path("reports/auto_fix")) -> None:
    """Write auto-fix report in JSON and Markdown formats."""
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Add timestamp and guard version
    data["timestamp"] = datetime.now().isoformat()
    data["guard_version"] = "1.0.0"
    
    # Write JSON report
    (out_dir / "report.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), 
        encoding="utf-8"
    )
    
    # Write Markdown report
    md_content = _generate_markdown_report(data)
    (out_dir / "report.md").write_text(md_content, encoding="utf-8")


def _generate_markdown_report(data: Dict[str, Any]) -> str:
    """Generate Markdown report from data."""
    lines = [
        "# Auto-Fix Report",
        "",
        f"**Generated:** {data.get('timestamp', 'N/A')}",
        f"**Mode:** {data.get('mode', 'N/A')}",
        f"**Dry Run:** {data.get('dry_run', False)}",
        "",
    ]
    
    # Python section
    if "python" in data:
        py_data = data["python"]
        lines.extend([
            "## Python",
            f"- **Files scanned:** {py_data.get('files_scanned', 0)}",
            f"- **Imports added:** {len(py_data.get('imports_added', []))}",
            f"- **Dependencies added:** {len(py_data.get('deps_added', []))}",
            "",
        ])
        
        if py_data.get("imports_added"):
            lines.extend(["### Imports Added", ""])
            for imp in py_data["imports_added"]:
                lines.append(f"- `{imp}`")
            lines.append("")
        
        if py_data.get("deps_added"):
            lines.extend(["### Dependencies Added", ""])
            for dep in py_data["deps_added"]:
                lines.append(f"- `{dep}`")
            lines.append("")
    
    # TypeScript section
    if "typescript" in data:
        ts_data = data["typescript"]
        lines.extend([
            "## TypeScript",
            f"- **Files scanned:** {ts_data.get('files_scanned', 0)}",
            f"- **Imports added:** {len(ts_data.get('imports_added', []))}",
            f"- **Dependencies added:** {len(ts_data.get('deps_added', []))}",
            "",
        ])
        
        if ts_data.get("imports_added"):
            lines.extend(["### Imports Added", ""])
            for imp in ts_data["imports_added"]:
                lines.append(f"- `{imp}`")
            lines.append("")
        
        if ts_data.get("deps_added"):
            lines.extend(["### Dependencies Added", ""])
            for dep in ts_data["deps_added"]:
                lines.append(f"- `{dep}`")
            lines.append("")
    
    # Errors section
    if data.get("errors"):
        lines.extend(["## Errors", ""])
        for error in data["errors"]:
            lines.append(f"- {error}")
        lines.append("")
    
    return "\n".join(lines)