import os
import f
import file_path
import len
import open
import print

"""
Fix all syntax errors by adding pass statements to empty try blocks
"""


def fix_empty_try_blocks():
    """Fix empty try blocks with only comments"""
    files_to_fix = ["zeta_vn/app/api/v1/__init__.py", "zeta_vn/app/api/v2/__init__.py"]
    for file_path in files_to_fix:
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        fixed_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            fixed_lines.append(line)
            if line.strip() == "try:":
                j = i + 1
                has_code = False
                comment_found = False
                while j < len(lines) and not lines[j].strip().startswith("except"):
                    next_line = lines[j].strip()
                    if next_line and not next_line.startswith("#"):
                        has_code = True
                        break
                    elif next_line.startswith("#"):
                        comment_found = True
                    j += 1
                if not has_code and comment_found:
                    fixed_lines.append("    pass  # Added to fix syntax error\n")
            i += 1
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(fixed_lines)
        print(f"✅ Fixed empty try blocks in {file_path}")


if __name__ == "__main__":
    print("🔧 Fixing empty try blocks...")
    fix_empty_try_blocks()
    print("✅ Empty try block fixes completed!")
