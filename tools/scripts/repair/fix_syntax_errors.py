import os
import re
import f
import file_path
import line
import match
import open
import print

"""
Fix syntax errors in import blocks
"""


def fix_syntax_errors():
    """Fix syntax errors in commented import blocks"""
    files_to_fix = ["zeta_vn/app/api/v1/__init__.py", "zeta_vn/app/api/v2/__init__.py"]
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        pattern = r"try:\s*\n(\s*#[^\n]*\n)+\s*except ImportError:"

        def replace_try_block(match):
            lines = match.group(0).split("\n")
            try_line = lines[0]
            comment_lines = [line for line in lines[1:-1] if line.strip().startswith("#")]
            except_line = lines[-1]
            return f"{try_line}\n    pass  # {comment_lines[0].strip()[1:].strip() if comment_lines else 'Commented imports'}\n{except_line}"

        content = re.sub(pattern, replace_try_block, content, flags=re.MULTILINE)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Fixed syntax errors in {file_path}")


if __name__ == "__main__":
    print("🔧 Fixing syntax errors in import blocks...")
    fix_syntax_errors()
    print("✅ Syntax error fixes completed!")
