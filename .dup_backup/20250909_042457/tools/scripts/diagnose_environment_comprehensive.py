#!/usr/bin/env python3
"""
Script chẩn đoán toàn diện môi trường VS Code và các extensions
Phân tích chi tiết từ screenshot và đưa ra giải pháp cụ thể
"""

import os
import subprocess
import sys
from pathlib import Path
import Exception
import ImportError
import any
import cmd
import dict
import dir_path
import e
import enumerate
import ext
import f
import fix
import i
import issue
import len
import list
import open
import p
import path
import pkg
import print
import tool


def check_environment_status():
    """Kiểm tra trạng thái môi trường hiện tại."""
    print("🔍 CHẨN ĐOÁN TOÀN DIỆN MÔI TRƯỜNG VS CODE")
    print("=" * 60)

    # 1. Python Environment
    print("🐍 PYTHON ENVIRONMENT:")
    print(f"  Python version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    print(f"  Virtual env: {os.environ.get('VIRTUAL_ENV', 'Not set')}")
    print(f"  Virtual env active: {sys.prefix != sys.base_prefix}")

    # 2. Key packages
    print("\n📦 KEY PACKAGES:")
    key_packages = ["fastapi", "uvicorn", "pydantic", "pytest", "ruff", "mypy"]
    for pkg in key_packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} - MISSING")

    # 3. PYTHONPATH
    print(f"\n🛤️  PYTHONPATH ({len(sys.path)} entries):")
    zeta_paths = [p for p in sys.path if "zeta" in p.lower()]
    for path in zeta_paths:
        print(f"  ✅ {path}")


def analyze_screenshot_issues():
    """Phân tích các vấn đề từ screenshot."""
    print("\n📸 PHÂN TÍCH CÁC VẤN ĐỀ TỪ SCREENSHOT:")
    print("=" * 60)

    issues = [
        {
            "type": "Extension Error",
            "description": "Extension activation failed - Developer: Toggle D...",
            "severity": "HIGH",
            "impact": "Development tools không hoạt động",
        },
        {
            "type": "Notification Spam",
            "description": "Bookmarks extension notification",
            "severity": "LOW",
            "impact": "UI clutter",
        },
        {
            "type": "Workspace Warning",
            "description": "zeta_vn.code-workspace file prompt",
            "severity": "MEDIUM",
            "impact": "Workspace configuration",
        },
        {
            "type": "Python Extension",
            "description": "Python extension loading...",
            "severity": "MEDIUM",
            "impact": "Python development tools delayed",
        },
    ]

    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. 🔴 {issue['type']} ({issue['severity']})")
        print(f"   📝 {issue['description']}")
        print(f"   💥 Impact: {issue['impact']}")

    return issues


def check_vscode_extensions():
    """Kiểm tra trạng thái VS Code extensions."""
    print("\n🔌 VS CODE EXTENSIONS ANALYSIS:")
    print("=" * 60)

    try:
        # Get extensions list
        result = subprocess.run(["code", "--list-extensions"], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            extensions = result.stdout.strip().split("\n")

            # Categorize extensions
            python_exts = [ext for ext in extensions if "python" in ext.lower()]
            dev_tools = [
                ext
                for ext in extensions
                if any(tool in ext.lower() for tool in ["sonarlint", "copilot", "git", "developer"])
            ]

            print(f"📊 Total extensions: {len(extensions)}")
            print(f"🐍 Python-related: {len(python_exts)}")
            print(f"🛠️  Dev tools: {len(dev_tools)}")

            # Check problematic extensions
            problematic = []

            # SonarLint check
            if "sonarsource.sonarlint-vscode" in extensions:
                print("\n🔍 SonarLint Status:")
                extensions_path = Path.home() / ".vscode" / "extensions"
                sonarlint_dirs = list(extensions_path.glob("sonarsource.sonarlint-vscode*"))

                for dir_path in sonarlint_dirs:
                    package_json = dir_path / "package.json"
                    if package_json.exists():
                        print(f"  ✅ {dir_path.name}")
                    else:
                        print(f"  ❌ {dir_path.name} - Missing package.json")
                        problematic.append(dir_path.name)

            return {"total": len(extensions), "problematic": problematic}

    except Exception as e:
        print(f"❌ Error checking extensions: {e}")
        return {"total": 0, "problematic": []}


def generate_fix_recommendations(issues: list[dict], ext_status: dict):
    """Tạo khuyến nghị sửa lỗi cụ thể."""
    print("\n🔧 KHUYẾN NGHỊ SỬA LỖI CỤ THỂ:")
    print("=" * 60)

    fixes = []

    # 1. Extension activation failed
    fixes.append(
        {
            "priority": "HIGH",
            "issue": "Extension activation failed",
            "solution": "Restart VS Code + Disable/Re-enable problematic extensions",
            "commands": [
                "1. Ctrl+Shift+P → 'Developer: Reload Window'",
                "2. Nếu vẫn lỗi: Disable extension → Restart → Enable lại",
            ],
        }
    )

    # 2. Python extension loading
    fixes.append(
        {
            "priority": "HIGH",
            "issue": "Python extension loading slow",
            "solution": "Check Python interpreter + Clear extension cache",
            "commands": [
                "1. Ctrl+Shift+P → 'Python: Select Interpreter'",
                "2. Chọn: E:\\zeta\\.venv\\Scripts\\python.exe",
                "3. Restart VS Code",
            ],
        }
    )

    # 3. Workspace configuration
    fixes.append(
        {
            "priority": "MEDIUM",
            "issue": "Workspace file prompt",
            "solution": "Open workspace hoặc dismiss notification",
            "commands": [
                "1. Click 'Open Workspace' để sử dụng workspace file",
                "2. Hoặc click X để dismiss và tiếp tục",
            ],
        }
    )

    # 4. Notification spam
    fixes.append(
        {
            "priority": "LOW",
            "issue": "Bookmarks extension notification",
            "solution": "Install extension hoặc disable notifications",
            "commands": [
                "1. Click 'Install' để cài extension",
                "2. Hoặc Settings → Extensions → Disable recommendations",
            ],
        }
    )

    # 5. Problematic extensions
    if ext_status.get("problematic"):
        fixes.append(
            {
                "priority": "HIGH",
                "issue": f"Corrupted extensions: {ext_status['problematic']}",
                "solution": "Reinstall corrupted extensions",
                "commands": [
                    "1. Uninstall extension: code --uninstall-extension <extension-id>",
                    "2. Restart VS Code",
                    "3. Reinstall: code --install-extension <extension-id>",
                ],
            }
        )

    # Display fixes
    for i, fix in enumerate(fixes, 1):
        print(f"\n{i}. 🎯 {fix['issue']} ({fix['priority']})")
        print(f"   💡 Solution: {fix['solution']}")
        for cmd in fix["commands"]:
            print(f"   📋 {cmd}")

    return fixes


def create_automated_fix_script():
    """Tạo script tự động sửa lỗi."""
    print("\n🤖 TẠO SCRIPT TỰ ĐỘNG SỬA LỖI:")
    print("=" * 60)

    script_content = """# Script PowerShell tự động sửa lỗi VS Code Environment
# Generated by diagnose_environment_comprehensive.py

Write-Host "🔧 VS CODE ENVIRONMENT AUTO-FIX" -ForegroundColor Cyan

# 1. Check Python interpreter
Write-Host "`n🐍 Checking Python interpreter..." -ForegroundColor Yellow
$VenvPython = "E:\\zeta\\.venv\\Scripts\\python.exe"
if (Test-Path $VenvPython) {
    Write-Host "✅ Python venv found: $VenvPython" -ForegroundColor Green
} else {
    Write-Host "❌ Python venv not found!" -ForegroundColor Red
    exit 1
}

# 2. Reload VS Code window
Write-Host "`n🔄 Reloading VS Code window..." -ForegroundColor Yellow
code --command "workbench.action.reloadWindow"

# 3. Clear extension cache
Write-Host "`n🧹 Clearing extension cache..." -ForegroundColor Yellow
$ExtensionCache = "$env:USERPROFILE\\.vscode\\extensions"
Get-ChildItem $ExtensionCache -Filter "*.cache" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue

# 4. Restart extension host
Write-Host "`n🔌 Restarting extension host..." -ForegroundColor Yellow
code --command "workbench.action.restartExtensionHost"

Write-Host "`n✅ Auto-fix completed! Check VS Code status." -ForegroundColor Green
"""

    script_path = Path("tools/autofix_vscode_environment.ps1")
    script_path.parent.mkdir(exist_ok=True)

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)

    print(f"✅ Created: {script_path}")
    print(f"📋 Run: .\\{script_path}")

    return script_path


def main():
    """Chạy chẩn đoán toàn diện."""
    check_environment_status()
    issues = analyze_screenshot_issues()
    ext_status = check_vscode_extensions()
    fixes = generate_fix_recommendations(issues, ext_status)
    script_path = create_automated_fix_script()

    print("\n" + "=" * 60)
    print("🎯 TÓM TẮT VÀ HÀNH ĐỘNG")
    print("=" * 60)

    print("\n📊 SUMMARY:")
    print(f"  🔴 Issues found: {len(issues)}")
    print(f"  🔧 Fixes available: {len(fixes)}")
    print(f"  🔌 Extensions: {ext_status.get('total', 0)} total")
    print(f"  ❌ Problematic: {len(ext_status.get('problematic', []))}")

    print("\n⚡ IMMEDIATE ACTIONS:")
    print(f"  1. 🔄 Run auto-fix: .\\{script_path}")
    print("  2. 🐍 Select Python interpreter: Ctrl+Shift+P → Python: Select Interpreter")
    print("  3. 🔌 Check extensions: Ctrl+Shift+X")
    print("  4. 🔄 Restart VS Code if needed")

    print("\n✅ Environment diagnosis completed!")


if __name__ == "__main__":
    main()
