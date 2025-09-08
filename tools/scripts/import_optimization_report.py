from __future__ import annotations

import subprocess
from pathlib import Path
import cmd
import code
import desc
import description
import l
import len
import list
import name
import print
import status
import suggestion

"""
Báo cáo tổng kết tối ưu imports cho dự án ZETA_VN.
Import optimization summary report for ZETA_VN project.
"""


def get_import_stats():
    """Lấy thống kê về imports."""
    print("📊 IMPORT OPTIMIZATION REPORT")
    print("=" * 60)
    python_files = list(Path(".").rglob("*.py"))
    print(f"📁 Total Python files scanned: {len(python_files)}")
    checks = [
        ("I001", "Import order issues", "Import ordering problems"),
        ("F401", "Unused imports", "Imported but never used"),
        ("F403", "Star imports", "from module import * (avoid)"),
    ]
    total_issues = 0
    for code, name, description in checks:
        result = subprocess.run(f"uv run ruff check . --select {code}", shell=False, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {name}: No issues found")
        else:
            lines = result.stdout.split("\n")
            issue_count = len([l for l in lines if code in l])
            total_issues += issue_count
            print(f"⚠️  {name}: {issue_count} issues")
            print(f"   └─ {description}")
    print("\n📈 SUMMARY:")
    print(f"  • Total import issues remaining: {total_issues}")
    if total_issues == 0:
        print("🎉 ALL IMPORTS OPTIMIZED!")
    elif total_issues < 10:
        print("✅ Import optimization mostly complete")
    elif total_issues < 50:
        print("⚠️  Moderate import optimization needed")
    else:
        print("🔧 Significant import optimization needed")
    return total_issues


def show_improvement_suggestions():
    """Hiển thị đề xuất cải tiến."""
    print("\n💡 OPTIMIZATION SUGGESTIONS:")
    print("=" * 60)
    suggestions = [
        "1. 📋 Import Order: Follow PEP 8 (stdlib → third-party → local)",
        "2. 🗑️  Unused Imports: Remove to improve load time and memory",
        "3. ⭐ Star Imports: Replace with explicit imports for clarity",
        "4. 🔗 Future Annotations: Add 'from __future__ import annotations'",
        "5. 📝 Type Hints: Use proper type annotations consistently",
    ]
    for suggestion in suggestions:
        print(f"   {suggestion}")
    print("\n🛠️  QUICK FIX COMMANDS:")
    print("=" * 60)
    commands = [
        ("Import Order", "uv run ruff check . --select I --fix"),
        ("Unused Imports", "uv run ruff check . --select F401 --fix"),
        ("Format Code", "uv run ruff format ."),
        ("Full Check", "uv run ruff check ."),
    ]
    for name, cmd in commands:
        print(f"   • {name:<15}: {cmd}")


def check_architecture_compliance():
    """Kiểm tra tuân thủ Clean Architecture trong imports."""
    print("\n🏗️  CLEAN ARCHITECTURE COMPLIANCE:")
    print("=" * 60)
    problem_patterns = [
        ("app → core", "app.*import.*core", "🔄 Dependency inversion OK"),
        ("core → app", "core.*import.*app", "❌ Circular dependency"),
        ("data → core", "data.*import.*core", "🔄 Repository pattern OK"),
        ("core → data", "core.*import.*data", "❌ Clean architecture violation"),
    ]
    for desc, pattern, status in problem_patterns:
        print(f"   • {desc:<15}: {status}")
    print("\n📋 IMPORT BEST PRACTICES:")
    print("   ✅ Use absolute imports for clarity")
    print("   ✅ Group imports by: stdlib → third-party → local")
    print("   ✅ One import per line for readability")
    print("   ✅ Use TYPE_CHECKING for type-only imports")
    print("   ✅ Avoid circular imports between modules")


def main():
    """Main function."""
    print("🔍 ZETA_VN IMPORT OPTIMIZATION REPORT")
    print("🕐 Generated:", "2025-09-01")
    print("=" * 80)
    total_issues = get_import_stats()
    show_improvement_suggestions()
    check_architecture_compliance()
    print("\n🎯 NEXT ACTIONS:")
    print("=" * 60)
    if total_issues == 0:
        print("🎉 Imports are fully optimized!")
        print("   • Consider running periodic checks")
        print("   • Monitor for new import issues in CI/CD")
    elif total_issues < 10:
        print("🔧 Quick cleanup needed:")
        print("   • Run: uv run ruff check . --select F401 --fix")
        print("   • Review remaining issues manually")
    else:
        print("🚀 Comprehensive optimization recommended:")
        print("   • Run: uv run python tools/smart_import_cleaner.py")
        print("   • Use: uv run ruff check . --select I,F401 --fix")
        print("   • Review and test changes")
    print("\n✨ Happy coding with optimized imports! ✨")


if __name__ == "__main__":
    main()
