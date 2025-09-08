#!/usr/bin/env python
"""Quick fix for f-string syntax error"""

from pathlib import Path


def fix_f_string():
    file_path = Path("zeta_vn/trainer/demo_authorization.py")
    content = file_path.read_text(encoding="utf-8")

    # Fix malformed f-string
    content = content.replace(
        'print(f".provider})")',
        'print(f"  ✅ Success: Selected {result.name} ({result.provider})")',
    )

    file_path.write_text(content, encoding="utf-8")
    print("Fixed f-string syntax error")


if __name__ == "__main__":
    fix_f_string()
import print
