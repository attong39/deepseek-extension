"""
NumPy Compatibility Monitoring Dashboard Script.
Tạo monitoring reports và health checks.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import Exception
import cmd
import cwd
import e
import len
import print
import str


def run_command(cmd: List[str], cwd: Path | None = None) -> Dict[str, Any]:
    """Run command và return result với error handling."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": "Command timeout",
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }


def check_runtime_status() -> Dict[str, Any]:
    """Kiểm tra runtime status với assert_numpy_runtime.py."""
    script_path = Path("scripts/assert_numpy_runtime.py")
    
    if not script_path.exists():
        return {
            "status": "error",
            "message": "Runtime validation script không tồn tại"
        }
    
    # Test NP1
    np1_result = run_command([
        sys.executable, str(script_path)
    ])
    
    # Test NP2 expectation
    np2_result = run_command([
        sys.executable, str(script_path)
    ], cwd=None)
    
    return {
        "status": "ok" if np1_result["success"] else "warning",
        "np1_check": np1_result,
        "np2_check": np2_result,
        "timestamp": datetime.now().isoformat(),
    }


def check_dependencies() -> Dict[str, Any]:
    """Kiểm tra trạng thái dependencies."""
    backend_dir = Path("apps/backend")
    
    if not backend_dir.exists():
        return {"status": "error", "message": "Backend directory không tồn tại"}
    
    # Check uv environment
    uv_check = run_command(["uv", "pip", "list"], cwd=backend_dir)
    
    # Check critical imports
    import_check = run_command([
        "uv", "run", "python", "-c",
        "import numpy, torch, faiss, cv2, sentence_transformers; print('All imports OK')"
    ], cwd=backend_dir)
    
    return {
        "status": "ok" if import_check["success"] else "error",
        "uv_status": uv_check["success"],
        "imports_status": import_check["success"],
        "import_output": import_check["stdout"],
        "import_error": import_check["stderr"],
    }


def generate_compatibility_report() -> Dict[str, Any]:
    """Tạo báo cáo compatibility đầy đủ."""
    return {
        "report_date": datetime.now().isoformat(),
        "runtime_check": check_runtime_status(),
        "dependencies_check": check_dependencies(),
        "system_info": {
            "python_version": sys.version,
            "platform": sys.platform,
        }
    }


def create_monitoring_dashboard():
    """Tạo HTML dashboard cho monitoring."""
    report = generate_compatibility_report()
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>NumPy Compatibility Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .status-ok {{ color: green; }}
        .status-warning {{ color: orange; }}
        .status-error {{ color: red; }}
        .card {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
        pre {{ background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>NumPy Compatibility Dashboard</h1>
    <p class="timestamp">Generated: {report['report_date']}</p>
    
    <div class="card">
        <h2>Runtime Status</h2>
        <p class="status-{report['runtime_check']['status']}">
            Status: {report['runtime_check']['status'].upper()}
        </p>
        {f"<p>Message: {report['runtime_check'].get('message', '')}</p>" if 'message' in report['runtime_check'] else ""}
    </div>
    
    <div class="card">
        <h2>Dependencies</h2>
        <p class="status-{'ok' if report['dependencies_check']['status'] == 'ok' else 'error'}">
            Status: {report['dependencies_check']['status'].upper()}
        </p>
        {f"<pre>{report['dependencies_check'].get('import_output', '')}</pre>" if report['dependencies_check'].get('import_output') else ""}
        {f"<pre style='color: red;'>{report['dependencies_check'].get('import_error', '')}</pre>" if report['dependencies_check'].get('import_error') else ""}
    </div>
    
    <div class="card">
        <h2>System Information</h2>
        <p>Python: {report['system_info']['python_version']}</p>
        <p>Platform: {report['system_info']['platform']}</p>
    </div>
    
    <div class="card">
        <h2>Raw Report Data</h2>
        <pre>{json.dumps(report, indent=2)}</pre>
    </div>
    
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => window.location.reload(), 5 * 60 * 1000);
    </script>
</body>
</html>
"""
    
    # Save dashboard
    dashboard_path = Path("numpy_compatibility_dashboard.html")
    dashboard_path.write_text(html_content, encoding="utf-8")
    
    print(f"✅ Dashboard created: {dashboard_path}")
    return dashboard_path


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # Output JSON cho CI
        report = generate_compatibility_report()
        print(json.dumps(report, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "--dashboard":
        # Tạo HTML dashboard
        create_monitoring_dashboard()
    else:
        # Default: quick status check
        report = generate_compatibility_report()
        
        print("🔍 NumPy Compatibility Status")
        print(f"Runtime: {report['runtime_check']['status'].upper()}")
        print(f"Dependencies: {report['dependencies_check']['status'].upper()}")
        print(f"Timestamp: {report['report_date']}")
        
        if report['runtime_check']['status'] != 'ok':
            print("⚠️  Issues detected - run with --json for details")
            sys.exit(1)


if __name__ == "__main__":
    main()
