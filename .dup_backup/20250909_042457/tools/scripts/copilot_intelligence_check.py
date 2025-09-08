#!/usr/bin/env python3
"""
Copilot Intelligence Verification Script
Kiểm tra xem Copilot có hiểu đúng cấu trúc dự án và các mối quan hệ không.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any
import Exception
import dict
import dir_name
import dir_path
import e
import f
import feature
import file_path
import info
import len
import list
import open
import print
import round
import str
import sum


def check_project_structure() -> dict[str, Any]:
    """Kiểm tra cấu trúc dự án ZETA_VN."""
    results = {
        "project_root": str(Path.cwd()),
        "key_directories": {},
        "config_files": {},
        "documentation": {},
    }

    # Kiểm tra các thư mục chính
    key_dirs = [
        "zeta_vn/core/domain",
        "zeta_vn/core/use_cases",
        "zeta_vn/core/services",
        "zeta_vn/core/interfaces",
        "zeta_vn/app/api",
        "zeta_vn/data/repositories",
        "tests",
        ".vscode",
    ]

    for dir_path in key_dirs:
        path = Path(dir_path)
        results["key_directories"][dir_path] = {
            "exists": path.exists(),
            "is_directory": path.is_dir() if path.exists() else False,
            "file_count": len(list(path.glob("**/*.py"))) if path.exists() and path.is_dir() else 0,
        }

    # Kiểm tra file cấu hình
    config_files = [
        "pyproject.toml",
        ".python-version",
        "uv.lock",
        ".vscode/settings.json",
        ".vscode/copilot-instructions.md",
        ".github/prompts/GUIDE.md",
        ".github/prompts/PROJECT_MAP.md",
    ]

    for file_path in config_files:
        path = Path(file_path)
        results["config_files"][file_path] = {
            "exists": path.exists(),
            "size_kb": round(path.stat().st_size / 1024, 2) if path.exists() else 0,
        }

    return results


def check_copilot_configuration() -> dict[str, Any]:
    """Kiểm tra cấu hình Copilot."""
    settings_path = Path(".vscode/settings.json")
    copilot_config = {
        "settings_file_exists": settings_path.exists(),
        "copilot_features": {},
        "intelligent_features": {},
    }

    if settings_path.exists():
        try:
            # Đọc settings (có thể có comments)
            content = settings_path.read_text(encoding="utf-8")

            # Kiểm tra các tính năng Copilot
            copilot_features = [
                "github.copilot.enable",
                "github.copilot.editor.enableAutoCompletions",
                "github.copilot.inlineSuggest.enable",
                "chat.extensionTools.enabled",
                "chat.promptFiles",
            ]

            for feature in copilot_features:
                copilot_config["copilot_features"][feature] = feature in content

            # Kiểm tra tính năng thông minh
            intelligent_features = [
                "explorer.fileNesting.enabled",
                "python.analysis.typeCheckingMode",
                "python.analysis.autoImportCompletions",
                "files.associations",
            ]

            for feature in intelligent_features:
                copilot_config["intelligent_features"][feature] = feature in content

        except Exception as e:
            copilot_config["error"] = str(e)

    return copilot_config


def check_development_tools() -> dict[str, Any]:
    """Kiểm tra các công cụ phát triển."""
    tools_status = {}

    # Kiểm tra Python environment
    venv_path = Path(".venv")
    tools_status["virtual_environment"] = {
        "exists": venv_path.exists(),
        "python_executable": (venv_path / "Scripts" / "python.exe").exists(),
    }

    # Kiểm tra các file quan trọng
    important_files = [
        "tools/quick_check.py",
        "SETUP_COMPLETE.md",
        ".vscode/copilot-instructions.md",
        ".vscode/settings_copilot_super_intelligent.jsonc",
    ]

    for file_path in important_files:
        path = Path(file_path)
        tools_status[file_path] = path.exists()

    return tools_status


def generate_copilot_context_summary() -> str:
    """Tạo tóm tắt ngữ cảnh cho Copilot."""
    summary = """
🤖 COPILOT CONTEXT SUMMARY - ZETA_VN PROJECT

📁 PROJECT STRUCTURE:
- Domain Layer: zeta_vn/core/domain/ (Entities, Value Objects)
- Use Cases: zeta_vn/core/use_cases/ (Business Logic)
- Services: zeta_vn/core/services/ (Domain Services)
- API Layer: zeta_vn/app/api/ (FastAPI Endpoints)
- Data Layer: zeta_vn/data/ (Repositories, Database)
- Tests: tests/ (Unit, Integration, E2E)

🎯 ARCHITECTURE PRINCIPLES:
- Clean Architecture with strict layer separation
- Domain-Driven Design patterns
- Dependency Inversion (core/ never imports app/ or data/)
- Type safety with mypy strict mode
- Async/await for I/O operations

🛠️ DEVELOPMENT STACK:
- Python 3.11+ with uv package manager
- FastAPI for REST API
- SQLAlchemy 2.x with AsyncPG
- pytest for testing
- ruff for formatting/linting
- mypy for type checking

📋 CODE STANDARDS:
- Google-style docstrings
- snake_case for functions/variables
- PascalCase for classes
- Type hints for all parameters and returns
- Coverage ≥ 80% for new code

🎪 COPILOT CAPABILITIES:
- Context-aware code generation
- Clean Architecture pattern recognition
- Intelligent file relationship understanding
- Project-wide refactoring suggestions
- Comprehensive test generation
"""
    return summary


def main():
    """Chạy kiểm tra và tạo báo cáo."""
    print("🔍 COPILOT INTELLIGENCE VERIFICATION")
    print("=" * 50)

    # Kiểm tra cấu trúc dự án
    print("\n📁 Project Structure Check...")
    structure = check_project_structure()

    missing_dirs = [dir_name for dir_name, info in structure["key_directories"].items() if not info["exists"]]

    if missing_dirs:
        print(f"⚠️  Missing directories: {', '.join(missing_dirs)}")
    else:
        print("✅ All key directories found")

    # Kiểm tra cấu hình Copilot
    print("\n🤖 Copilot Configuration Check...")
    copilot_config = check_copilot_configuration()

    if copilot_config["settings_file_exists"]:
        enabled_features = sum(copilot_config["copilot_features"].values())
        intelligent_features = sum(copilot_config["intelligent_features"].values())

        print(f"✅ Copilot features enabled: {enabled_features}/5")
        print(f"✅ Intelligent features enabled: {intelligent_features}/4")
    else:
        print("❌ VS Code settings file not found")

    # Kiểm tra công cụ phát triển
    print("\n🛠️  Development Tools Check...")
    tools = check_development_tools()

    if tools["virtual_environment"]["exists"]:
        print("✅ Virtual environment configured")
    else:
        print("❌ Virtual environment missing")

    # Tạo context summary
    context_summary = generate_copilot_context_summary()

    print("\n📋 Copilot Context Summary Generated")
    print("=" * 50)
    print(context_summary)

    # Tạo file báo cáo
    report = {
        "timestamp": "2025-08-28",
        "project_structure": structure,
        "copilot_configuration": copilot_config,
        "development_tools": tools,
        "context_summary": context_summary,
    }

    # Lưu báo cáo
    report_path = Path("copilot_intelligence_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed report saved to: {report_path}")
    print("\n🎉 Copilot Intelligence Verification Complete!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
