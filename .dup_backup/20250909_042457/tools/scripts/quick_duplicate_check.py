#!/usr/bin/env python3
"""
Quick Duplicate Code Analysis Script
===================================

Script chạy nhanh để phân tích duplicate code trong dự án Zeta.
"""

import sys
from pathlib import Path
import blocks
import len
import print
import str
import sum

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.duplicate_code_analyzer import DuplicateCodeAnalyzer, ReportGenerator


def quick_analysis():
    """Run quick duplicate code analysis on Zeta project."""
    print("🚀 ZETA AI SERVER - DUPLICATE CODE ANALYSIS")
    print("=" * 50)

    # Analyze zeta_vn directory
    zeta_path = project_root / "zeta_vn"
    if not zeta_path.exists():
        print("❌ zeta_vn directory not found!")
        return

    print(f"📁 Analyzing project: {zeta_path}")

    # Run analysis
    analyzer = DuplicateCodeAnalyzer(str(zeta_path))
    report = analyzer.analyze()

    # Generate reports
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)

    generator = ReportGenerator(report, str(reports_dir))

    # Console report
    generator.generate_console_report()

    # HTML report
    html_file = generator.generate_html_report()
    print(f"\n📄 Detailed HTML report: {html_file}")

    # JSON report for tools
    json_file = generator.generate_json_report()
    print(f"📊 JSON report: {json_file}")

    # Quick stats
    total_functions = sum(len(blocks) for _, blocks in report.duplicate_functions)
    total_similar = len(report.similar_blocks)
    total_redundant = len(report.redundant_imports)

    print("\n📊 QUICK STATS:")
    print(f"  • Total files analyzed: {len(analyzer.python_files)}")
    print(f"  • Code blocks extracted: {len(analyzer.code_blocks)}")
    print(f"  • Duplicate functions: {total_functions}")
    print(f"  • Similar code blocks: {total_similar}")
    print(f"  • Redundant imports: {total_redundant}")

    # Recommendations
    print("\n💡 QUICK RECOMMENDATIONS:")
    if total_functions > 10:
        print("  🔥 HIGH function duplication - Priority refactoring needed!")
    elif total_functions > 5:
        print("  ⚠️ Moderate function duplication - Consider refactoring")
    else:
        print("  ✅ Low function duplication")

    if total_redundant > 20:
        print("  📦 Many redundant imports - Create utility modules")
    elif total_redundant > 10:
        print("  📦 Some redundant imports - Consolidate common imports")
    else:
        print("  ✅ Import structure looks good")

    print("\n🎯 Next steps:")
    print("  1. Review HTML report for detailed analysis")
    print("  2. Focus on high-similarity code blocks")
    print("  3. Extract common functions to utilities")
    print("  4. Create shared modules for repeated imports")


if __name__ == "__main__":
    quick_analysis()
