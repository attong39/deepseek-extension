from __future__ import annotations

from pathlib import Path
import Exception
import e
import f
import filename
import open
import print

"""
Fix Syntax Errors in Tools
==========================
Fix basic syntax errors in tool files.
"""


def fix_syntax_errors():
    """Fix basic syntax errors in tool files."""
    tools_dir = Path(__file__).parent
    problematic_files = ["cleanup_tools.py", "fix_imports_gradual.py", "update_roadmap.py"]
    for filename in problematic_files:
        file_path = tools_dir / filename
        if file_path.exists():
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
                lines = content.split("\n")
                fixed_lines = []
                for line in lines:
                    if line.startswith("    ") and not fixed_lines:
                        stripped = line.lstrip()
                        if stripped and not stripped.startswith("#"):
                            line = stripped
                    fixed_lines.append(line)
                fixed_content = "\n".join(fixed_lines)
                if fixed_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(fixed_content)
                    print(f"✅ Fixed syntax in {filename}")
            except Exception as e:
                print(f"❌ Error fixing {filename}: {e}")


if __name__ == "__main__":
    fix_syntax_errors()
