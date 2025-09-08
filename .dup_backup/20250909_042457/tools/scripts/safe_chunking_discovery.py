#!/usr/bin/env python3
"""
Safe discovery script - Phase 1 của chunking consolidation.

Chỉ PHÂN TÍCH và tạo BACKUP, không thay đổi gì.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import Exception
import all
import bool
import cmd
import d
import deps
import dict
import dir_path
import e
import f
import file_path
import len
import line
import list
import open
import passed
import print
import rec
import stdout
import str
import test_name
import tuple


def run_command_safe(cmd: str) -> tuple[bool, str, str]:
    """Chạy command an toàn và return (success, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def analyze_dependencies() -> dict[str, list[str]]:
    """Phân tích tất cả dependencies của chunking modules."""
    print("🔍 Analyzing chunking dependencies...")

    analysis = {
        "rag_chunker_imports": [],
        "chunking_imports": [],
        "chunk_class_usages": [],
        "retrieval_service_imports": [],
        "context_planner_dependencies": [],
    }

    # Tìm files import rag_chunker
    success, stdout, _ = run_command_safe('grep -r "from.*rag_chunker" zeta_vn/ --include="*.py" || echo "No matches"')
    if success and "No matches" not in stdout:
        analysis["rag_chunker_imports"] = stdout.strip().split("\n")

    # Tìm files import chunking
    success, stdout, _ = run_command_safe('grep -r "from.*chunking" zeta_vn/ --include="*.py" || echo "No matches"')
    if success and "No matches" not in stdout:
        analysis["chunking_imports"] = stdout.strip().split("\n")

    # Tìm class usages
    success, stdout, _ = run_command_safe(
        'grep -r "RagChunker\\|TokenChunker\\|ChunkingService" zeta_vn/ --include="*.py" || echo "No matches"'
    )
    if success and "No matches" not in stdout:
        analysis["chunk_class_usages"] = stdout.strip().split("\n")

    # Tìm retrieval_service imports
    success, stdout, _ = run_command_safe(
        'grep -r "from.*retrieval_service" zeta_vn/ --include="*.py" || echo "No matches"'
    )
    if success and "No matches" not in stdout:
        analysis["retrieval_service_imports"] = stdout.strip().split("\n")

    # Phân tích context_planner dependencies
    context_planner_path = Path("zeta_vn/core/services/context_planner.py")
    if context_planner_path.exists():
        with open(context_planner_path, encoding="utf-8") as f:
            content = f.read()
            analysis["context_planner_dependencies"] = [
                line.strip()
                for line in content.split("\n")
                if "import" in line and ("Chunk" in line or "retrieval" in line)
            ]

    return analysis


def test_current_state() -> dict[str, bool]:
    """Test trạng thái hiện tại để establish baseline."""
    print("🧪 Testing current state baseline...")

    tests = {
        "rag_chunker_tests": False,
        "rag_services_tests": False,
        "chunk_related_tests": False,
        "ruff_check": False,
        "mypy_check": False,
    }

    # Test rag_chunker
    success, _, _ = run_command_safe("uv run pytest tests/unit/test_rag_chunker_sentences.py -v")
    tests["rag_chunker_tests"] = success

    # Test rag_services
    success, _, _ = run_command_safe("uv run pytest tests/unit/test_rag_services.py -v")
    tests["rag_services_tests"] = success

    # Test chunk-related
    success, _, _ = run_command_safe('uv run pytest tests/unit/ -k "chunk" -v')
    tests["chunk_related_tests"] = success

    # Ruff check
    success, _, _ = run_command_safe("uv run ruff check zeta_vn/core/services/")
    tests["ruff_check"] = success

    # Mypy check
    success, _, _ = run_command_safe("uv run mypy zeta_vn/core/services/")
    tests["mypy_check"] = success

    return tests


def create_comprehensive_backup() -> bool:
    """Tạo backup comprehensive của tất cả files liên quan."""
    print("📦 Creating comprehensive backup...")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_base = Path(f"_backup_chunking_safe_{timestamp}")
    backup_base.mkdir(exist_ok=True)

    # Directories to backup
    dirs_to_backup = [
        "zeta_vn/core/services",
        "zeta_vn/core/adapters/vector",
        "zeta_vn/tests/unit",
        "zeta_vn/core/domain/entities",
        "zeta_vn/core/domain/ports",
    ]

    for dir_path in dirs_to_backup:
        src = Path(dir_path)
        if src.exists():
            dest = backup_base / src.name
            shutil.copytree(src, dest, dirs_exist_ok=True)
            print(f"   ✅ Backed up {src} → {dest}")

    # Backup specific important files
    important_files = [
        "zeta_vn/core/services/context_planner.py",
        "tests/conftest.py",
        "pyproject.toml",
    ]

    for file_path in important_files:
        src = Path(file_path)
        if src.exists():
            dest = backup_base / "important_files" / src.name
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(src, dest)
            print(f"   ✅ Backed up {src} → {dest}")

    print(f"📦 Comprehensive backup created: {backup_base}")
    return True


def analyze_chunking_files() -> dict[str, dict]:
    """Phân tích chi tiết các file chunking hiện tại."""
    print("📊 Analyzing chunking files structure...")

    chunking_files = [
        "zeta_vn/core/services/rag_chunker.py",
        "zeta_vn/core/services/chunking.py",
        "zeta_vn/core/services/retrieval_service.py",
        "zeta_vn/core/adapters/vector/chunking_service.py",
        "zeta_vn/core/adapters/vector/semantic_chunking.py",
    ]

    analysis = {}

    for file_path in chunking_files:
        path = Path(file_path)
        if not path.exists():
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        file_analysis = {
            "size_bytes": len(content.encode("utf-8")),
            "line_count": len(content.split("\n")),
            "has_chunk_class": "class Chunk" in content
            or "class TextChunk" in content
            or "class DocumentChunk" in content,
            "has_chunking_logic": "def chunk" in content or "def split" in content,
            "imports": [
                line.strip()
                for line in content.split("\n")
                if line.strip().startswith("import") or line.strip().startswith("from")
            ],
            "classes": [
                line.strip()
                for line in content.split("\n")
                if line.strip().startswith("class ") and ("Chunk" in line or "Chun" in line)
            ],
            "functions": [
                line.strip()
                for line in content.split("\n")
                if line.strip().startswith("def ") and ("chunk" in line.lower() or "split" in line.lower())
            ],
        }

        analysis[file_path] = file_analysis

    return analysis


def generate_safety_report(dependencies: dict, tests: dict, file_analysis: dict) -> None:
    """Tạo báo cáo chi tiết về safety analysis."""
    print("📋 Generating safety analysis report...")

    report = {
        "timestamp": datetime.now().isoformat(),
        "safety_analysis": {
            "dependencies": dependencies,
            "current_test_status": tests,
            "file_analysis": file_analysis,
        },
        "risk_assessment": {
            "high_risk_files": [],
            "medium_risk_files": [],
            "low_risk_files": [],
        },
        "recommendations": [],
    }

    # Risk assessment
    for file_path, analysis in file_analysis.items():
        risk_factors = 0

        # Check if file has many dependencies
        deps_count = len([d for deps in dependencies.values() for d in deps if file_path in d])
        if deps_count > 3:
            risk_factors += 2
        elif deps_count > 1:
            risk_factors += 1

        # Check if file has chunking logic
        if analysis["has_chunking_logic"]:
            risk_factors += 1

        # Check if file has Chunk class
        if analysis["has_chunk_class"]:
            risk_factors += 1

        if risk_factors >= 3:
            report["risk_assessment"]["high_risk_files"].append(file_path)
        elif risk_factors >= 2:
            report["risk_assessment"]["medium_risk_files"].append(file_path)
        else:
            report["risk_assessment"]["low_risk_files"].append(file_path)

    # Recommendations
    if not all(tests.values()):
        report["recommendations"].append("⚠️ Some tests are currently failing - fix before consolidation")

    if len(report["risk_assessment"]["high_risk_files"]) > 0:
        report["recommendations"].append("🚨 High risk files detected - use gradual migration approach")

    if "context_planner.py" in str(dependencies):
        report["recommendations"].append("⚠️ context_planner.py depends on retrieval_service - handle carefully")

    # Save report
    report_path = Path("chunking_safety_analysis.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"📋 Safety analysis saved: {report_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("🛡️ SAFETY ANALYSIS SUMMARY")
    print("=" * 60)

    print("📊 Test Status:")
    for test_name, passed in tests.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")

    print("\n🎯 Risk Assessment:")
    print(f"   High Risk: {len(report['risk_assessment']['high_risk_files'])} files")
    print(f"   Medium Risk: {len(report['risk_assessment']['medium_risk_files'])} files")
    print(f"   Low Risk: {len(report['risk_assessment']['low_risk_files'])} files")

    print("\n📝 Recommendations:")
    for rec in report["recommendations"]:
        print(f"   {rec}")

    return report


def main() -> bool:
    """Main discovery và safety analysis."""
    print("🚀 Starting SAFE chunking discovery & analysis...")
    print("   (NO changes will be made - read-only analysis)")

    try:
        # Step 1: Analyze dependencies
        dependencies = analyze_dependencies()

        # Step 2: Test current state
        tests = test_current_state()

        # Step 3: Create backup
        if not create_comprehensive_backup():
            print("❌ Failed to create backup")
            return False

        # Step 4: Analyze files
        file_analysis = analyze_chunking_files()

        # Step 5: Generate safety report
        generate_safety_report(dependencies, tests, file_analysis)

        print("\n🎉 Safe discovery completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Review chunking_safety_analysis.json")
        print("   2. Fix any failing tests before proceeding")
        print("   3. Plan gradual migration for high-risk files")
        print("   4. Consider context_planner.py dependencies")

        return True

    except Exception as e:
        print(f"❌ Discovery failed: {e}")
        return False


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
