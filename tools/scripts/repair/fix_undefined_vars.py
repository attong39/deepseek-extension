import re
from pathlib import Path
import file_path
import line
import list
import pattern
import print
import replacement

"""
Sửa các lỗi undefined variable phổ biến
"""
ROOT = Path(__file__).resolve().parents[2]


def fix_undefined_vars_in_tests():
    """Fix common undefined variable patterns in test files"""
    fixes_applied = 0
    perf_files = [
        "zeta_vn/tests/performance/test_load.py",
        "zeta_vn/tests/performance/test_performance.py",
        "zeta_vn/tests/performance/test_stress.py",
    ]
    for file_path in perf_files:
        full_path = ROOT / file_path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8", errors="ignore")
        original_content = content
        if "result[" in content and "result =" not in content:
            print(f"🔧 Fixing missing result assignment in {file_path}")
            content = re.sub(r"(\s+)_ = await make_request\(", r"\1result = await make_request(", content)
            content = re.sub(
                r"(\s+)await suite\.run_load_test\(config\)",
                r"\1load_result = await suite.run_load_test(config)",
                content,
            )
            fixes_applied += 1
        patterns = [
            (
                r"(\s+)await register_use_case\(request\)",
                r"\1user = await register_use_case(request)",
            ),
            (
                r"(\s+)await activate_agent_use_case\.execute\(",
                r"\1activated_agent = await activate_agent_use_case.execute(",
            ),
            (
                r"(\s+)await deactivate_agent_use_case\.execute\(",
                r"\1deactivated_agent = await deactivate_agent_use_case.execute(",
            ),
            (
                r"(\s+)await add_capability_use_case\.execute\(",
                r"\1updated_agent = await add_capability_use_case.execute(",
            ),
            (
                r"(\s+)await remove_capability_use_case\.execute\(",
                r"\1updated_agent = await remove_capability_use_case.execute(",
            ),
            (
                r"(\s+)await create_agent_use_case\.execute\(",
                r"\1agent = await create_agent_use_case.execute(",
            ),
            (r"(\s+)Session\(", r"\1session = Session("),
            (r'(\s+)Agent\(name="A"', r'\1short_agent = Agent(name="A"'),
            (
                r'(\s+)Agent\(name="A".*# Bad name',
                r'\1bad_agent = Agent(name="A", description="Test")  # Bad name',
            ),
        ]
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                fixes_applied += 1
        if content != original_content:
            full_path.write_text(content, encoding="utf-8")
            print(f"✅ Fixed undefined vars in {file_path}")
    return fixes_applied


def fix_import_orders():
    """Fix import order issues"""
    fixes_applied = 0
    test_files = list((ROOT / "zeta_vn/tests").rglob("*.py"))
    for file_path in test_files:
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        original_content = content
        if "from __future__ import" in content:
            lines = content.split("\n")
            future_imports = []
            other_lines = []
            docstring_started = False
            docstring_ended = False
            for line in lines:
                if line.strip().startswith('"""'):
                    if not docstring_started:
                        docstring_started = True
                        other_lines.append(line)
                    elif not docstring_ended:
                        docstring_ended = True
                        other_lines.append(line)
                    else:
                        other_lines.append(line)
                elif line.strip().startswith("from __future__ import"):
                    if docstring_ended or not docstring_started:
                        future_imports.append(line)
                    else:
                        other_lines.append(line)
                else:
                    other_lines.append(line)
            if future_imports and docstring_ended:
                new_lines = []
                in_docstring = False
                docstring_count = 0
                for line in other_lines:
                    if '"""' in line:
                        docstring_count += 1
                        new_lines.append(line)
                        if docstring_count == 2:  # End of docstring
                            new_lines.append("")
                            new_lines.extend(future_imports)
                            new_lines.append("")
                    else:
                        new_lines.append(line)
                content = "\n".join(new_lines)
                fixes_applied += 1
        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            print(f"✅ Fixed imports in {file_path.relative_to(ROOT)}")
    return fixes_applied


def main():
    print("🔧 Starting undefined variable fixes...")
    var_fixes = fix_undefined_vars_in_tests()
    import_fixes = fix_import_orders()
    total_fixes = var_fixes + import_fixes
    print(f"\n✅ Applied {total_fixes} fixes")
    print(f"   - Variable fixes: {var_fixes}")
    print(f"   - Import fixes: {import_fixes}")
    print("\n💡 Next steps:")
    print("   1. Run: uv run ruff check . --fix")
    print("   2. Run: uv run mypy zeta_vn")
    print("   3. Run: uv run pytest -q")


if __name__ == "__main__":
    main()
