from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import Exception
import bool
import c
import dict
import dry_run
import e
import file_path
import fix_func
import int
import len
import list
import match
import max
import original_name
import print
import should_fix
import str
import target_path

"""
🔧 Auto Fix Tool - Dọn dẹp import issues & di chuyển file theo PROJECT_MAP.md
Tính năng:
- Đọc PROJECT_MAP.md để lấy mapping patterns
- Auto-fix ruff/mypy issues
- Di chuyển file đến đúng vị trí Clean Architecture
- Tạo stub cho missing files
- Backup an toàn trước khi thay đổi
Usage:
  uv run python tools/maintenance/autofix_imports.py --dry-run
  uv run python tools/maintenance/autofix_imports.py --apply --limit 5
  uv run python tools/maintenance/autofix_imports.py --full
"""
ROOT = Path(__file__).resolve().parents[2]


@dataclass
class FileReport:
    """Báo cáo về file cần fix"""

    path: Path
    score: int  # 0-100
    issues: list[str]
    suggested_move: Path | None = None
    can_autofix: bool = False


def parse_mapping_patterns(project_map: Path) -> dict[str, str]:
    """Parse PROJECT_MAP.md để lấy mapping patterns"""
    if not project_map.exists():
        return {}
    content = project_map.read_text(encoding="utf-8", errors="ignore")
    mapping = {}
    pattern = re.compile(r"^\s*-\s*(.+?)\s*->\s*(.+?)\s*$", re.MULTILINE)
    for match in pattern.finditer(content):
        src = match.group(1).strip()
        dst = match.group(2).strip()
        mapping[src] = dst
    return mapping


def scan_file_issues(file_path: Path) -> FileReport:
    """Scan file để tìm issues và đánh giá khả năng fix"""
    issues = []
    score = 100
    can_autofix = True
    if not file_path.exists() or file_path.suffix != ".py":
        return FileReport(file_path, 0, ["not_python"], can_autofix=False)
    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "check", str(file_path)], capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode != 0:
            issues.append("ruff")
            score -= 20
        result = subprocess.run(["uv", "run", "mypy", str(file_path)], capture_output=True, text=True, cwd=ROOT)
        if result.returncode != 0:
            issues.append("mypy")
            score -= 40
            if "import" in result.stdout.lower():
                can_autofix = True
            else:
                can_autofix = False
    except Exception as e:
        issues.append(f"scan_error: {e}")
        score = 0
        can_autofix = False
    return FileReport(file_path, max(0, score), issues, can_autofix=can_autofix)


def auto_fix_file(file_path: Path) -> bool:
    """Tự động fix file issues"""
    success = True
    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "check", str(file_path), "--fix"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if result.returncode != 0:
            print(f"⚠️  Ruff fix partial: {file_path.name}")
        content = file_path.read_text(encoding="utf-8")
        fixes = [
            (
                lambda c: "from __future__ import annotations" not in c and "import " in c,
                lambda c: "from __future__ import annotations\n\n" + c,
            ),
            (lambda c: "except:" in c, lambda c: c.replace("except:", "except Exception:")),
            (
                lambda c: "import os\nimport sys" in c,
                lambda c: c.replace("import os\nimport sys", "import os\nimport sys"),
            ),
        ]
        for should_fix, fix_func in fixes:
            if should_fix(content):
                content = fix_func(content)
        file_path.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"❌ Auto-fix failed for {file_path}: {e}")
        success = False
    return success


def move_file_safely(src: Path, dst: Path, dry_run: bool = True) -> bool:
    """An toàn di chuyển file đến vị trí mới"""
    try:
        if not src.exists():
            return False
        if dry_run:
            print(f"📁 Would move: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
            return True
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            backup = dst.with_suffix(f"{dst.suffix}.backup")
            shutil.move(str(dst), str(backup))
            print(f"📦 Backed up: {dst} -> {backup}")
        shutil.move(str(src), str(dst))
        print(f"✅ Moved: {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
        return True
    except Exception as e:
        print(f"❌ Failed to move {src} -> {dst}: {e}")
        return False


def create_stub_file(target_path: Path, original_name: str) -> bool:
    """Tạo stub file cho missing file"""
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        stub_content = f'''"""
Stub for {original_name}
This file was auto-generated during refactoring.
TODO: Implement proper functionality.
"""
def placeholder() -> None:
    """Placeholder function - remove when implementing."""
    pass
'''
        target_path.write_text(stub_content, encoding="utf-8")
        print(f"📄 Created stub: {target_path.relative_to(ROOT)}")
        return True
    except Exception as e:
        print(f"❌ Failed to create stub {target_path}: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-fix imports and move files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--apply", action="store_true", help="Actually apply changes")
    parser.add_argument("--limit", type=int, default=10, help="Limit files to process")
    parser.add_argument("--full", action="store_true", help="Process all files")
    args = parser.parse_args()
    if not args.apply and not args.dry_run:
        args.dry_run = True
    print("🔧 Auto Fix Tool - Import Issues & Clean Architecture Migration")
    print("=" * 60)
    project_map = ROOT / ".github" / "prompts" / "PROJECT_MAP.md"
    mapping = parse_mapping_patterns(project_map)
    print(f"📋 Loaded {len(mapping)} mapping patterns from PROJECT_MAP.md")
    problem_files = []
    for pattern in ["*.py", "demo_*.py", "fix_*.py", "test_*.py"]:
        for file_path in ROOT.glob(pattern):
            if file_path.name != "conftest.py":  # Skip some files
                report = scan_file_issues(file_path)
                if report.issues:
                    problem_files.append(report)
    if not args.full:
        problem_files = problem_files[: args.limit]
    print(f"🔍 Found {len(problem_files)} files with issues")
    results = {"fixed": 0, "moved": 0, "stubbed": 0, "failed": 0}
    for report in problem_files:
        print(f"\n📁 Processing: {report.path.name}")
        print(f"   Score: {report.score}/100, Issues: {', '.join(report.issues)}")
        if report.can_autofix and not args.dry_run:
            if auto_fix_file(report.path):
                results["fixed"] += 1
                report = scan_file_issues(report.path)
        rel_path = str(report.path.relative_to(ROOT)).replace("\\", "/")
        if rel_path in mapping:
            target = ROOT / mapping[rel_path]
            if report.score >= 70:  # Good enough to move
                if move_file_safely(report.path, target, dry_run=args.dry_run):
                    results["moved"] += 1
            else:  # Create stub instead
                if not args.dry_run:
                    if create_stub_file(target, report.path.name):
                        results["stubbed"] += 1
                else:
                    print(f"📄 Would create stub: {target.relative_to(ROOT)}")
                    results["stubbed"] += 1
        else:
            print(f"   ⚠️  No mapping found for {rel_path}")
            results["failed"] += 1
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    print(f"   ✅ Fixed: {results['fixed']} files")
    print(f"   📁 Moved: {results['moved']} files")
    print(f"   📄 Stubbed: {results['stubbed']} files")
    print(f"   ❌ Failed: {results['failed']} files")
    if args.dry_run:
        print("\n💡 Run with --apply to actually make changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
