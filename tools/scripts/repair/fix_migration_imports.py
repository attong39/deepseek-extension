from pathlib import Path
import any
import i
import line
import migration_init
import pattern
import print
import range

"""
Sửa lỗi import migration files bắt đầu bằng số
"""
ROOT = Path(__file__).resolve().parents[2]


def fix_migration_imports():
    """Fix migration import errors"""
    migration_files = [
        ROOT / "zeta_vn/data/migrations/__init__.py",
        ROOT / "zeta_vn/data/migrations/versions/__init__.py",
    ]
    fixed_count = 0
    for migration_init in migration_files:
        if not migration_init.exists():
            print(f"Migration file not found: {migration_init}")
            continue
        content = migration_init.read_text(encoding="utf-8", errors="ignore")
        original_content = content
        problematic_patterns = [
            "from .001_",
            "from .002_",
            "from .003_",
            "from .004_",
            "from .005_",
            "from .006_",
            "from .007_",
            "from .008_",
            "from .009_",
            "from .010_",
            "from .011_",
            "from .012_",
        ]
        for pattern in problematic_patterns:
            if pattern in content:
                content = content.replace(pattern, f"# {pattern}")
                print(f"🔧 Commented out import: {pattern} in {migration_init.name}")
        lines = content.split("\n")
        new_lines = []
        in_try_block = False
        for line in lines:
            if line.strip().startswith("try:") and any(f"from .{i:03d}_" in content for i in range(1, 20)):
                next_lines = content[content.find(line) : content.find(line) + 200]
                if any(f"from .{i:03d}_" in next_lines for i in range(1, 20)):
                    new_lines.append(f"# {line}")
                    in_try_block = True
                else:
                    new_lines.append(line)
            elif in_try_block and (line.strip().startswith("except") or line.strip().startswith("pass")):
                new_lines.append(f"# {line}")
                if line.strip().startswith("pass"):
                    in_try_block = False
            elif in_try_block:
                new_lines.append(f"# {line}")
            else:
                new_lines.append(line)
        content = "\n".join(new_lines)
        if content != original_content:
            migration_init.write_text(content, encoding="utf-8")
            print(f"✅ Fixed migration imports in {migration_init}")
            fixed_count += 1
        else:
            print(f"No fixes needed in {migration_init}")
    return fixed_count > 0


def main():
    print("🔧 Fixing migration import syntax errors...")
    fixed = fix_migration_imports()
    if fixed:
        print("\n✅ Migration imports fixed!")
        print("💡 Next: Run mypy again to check for other errors")
    else:
        print("\n⚠️  No fixes applied")


if __name__ == "__main__":
    main()
