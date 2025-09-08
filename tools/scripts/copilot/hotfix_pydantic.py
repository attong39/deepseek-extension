from __future__ import annotations

import re
import sys
from pathlib import Path
import Exception
import e
import fix
import print

"""
Hotfix for Pydantic v2 Settings Configuration Issues
Fixes the "extra_forbidden" validation errors in DatabaseSettings and other BaseSettings
"""


def fix_pydantic_settings():
    """Fix Pydantic v2 settings configuration issues"""
    print("🔧 Fixing Pydantic v2 Settings Configuration...")
    settings_file = Path("zeta_vn/config/advanced_settings.py")
    if not settings_file.exists():
        print("❌ Settings file not found")
        return False
    content = settings_file.read_text(encoding="utf-8")
    fixes = [
        {
            "pattern": r"class Config:\s*\n(\s*)env_file = \"\.env\"\s*\n(\s*)env_prefix = \"([^\"]+)\"",
            "replacement": r"model_config = {\"env_file\": \".env\", \"env_prefix\": \"\3\", \"extra\": \"ignore\"}",
        },
        {
            "pattern": r"class Config:\s*\n(\s*)env_file = \"\.env\"\s*\n(\s*)case_sensitive = False",
            "replacement": r"model_config = {\"env_file\": \".env\", \"case_sensitive\": False, \"extra\": \"ignore\"}",
        },
        {
            "pattern": r"class Config:\s*\n(\s*)env_file = \"\.env\"",
            "replacement": r"model_config = {\"env_file\": \".env\", \"extra\": \"ignore\"}",
        },
        {"pattern": r"@validator\((.*?)\)", "replacement": r"@field_validator(\1)"},
    ]
    modified = False
    for fix in fixes:
        new_content = re.sub(fix["pattern"], fix["replacement"], content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True
    if "from pydantic import" in content and "field_validator" not in content:
        content = content.replace(
            "from pydantic import Field, validator",
            "from pydantic import Field, field_validator, ConfigDict",
        )
        modified = True
    if modified:
        settings_file.write_text(content, encoding="utf-8")
        print("✅ Settings file updated with Pydantic v2 compatibility")
        return True
    else:
        print("✅ Settings file already compatible")
        return True


def fix_pyproject_toml():
    """Fix deprecated ruff configuration in test_architecture/pyproject.toml"""
    print("🔧 Fixing deprecated ruff configuration...")
    pyproject_file = Path("test_architecture/pyproject.toml")
    if not pyproject_file.exists():
        print("✅ test_architecture/pyproject.toml not found - skipping")
        return True
    content = pyproject_file.read_text(encoding="utf-8")
    if "[tool.ruff]" in content and "ignore =" in content:
        content = re.sub(
            r"\[tool\.ruff\]\s*\n(.*?)\n(select = .*?)\n(ignore = .*?)\n(.*?isort.*?)\n",
            r"[tool.ruff]\n\1\n\n[tool.ruff.lint]\n\2\n\3\n\4\n",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )
        pyproject_file.write_text(content, encoding="utf-8")
        print("✅ pyproject.toml updated with new ruff configuration")
        return True
    else:
        print("✅ pyproject.toml already up to date")
        return True


def main():
    """Run all hotfixes"""
    print("🚑 PYDANTIC V2 HOTFIX - STARTING")
    print("=" * 50)
    success = True
    try:
        success &= fix_pydantic_settings()
        success &= fix_pyproject_toml()
        if success:
            print("\n🎉 ALL HOTFIXES APPLIED SUCCESSFULLY!")
            print("💡 You can now run: uv run python scripts/copilot/simple_runner.py")
        else:
            print("\n⚠️ Some hotfixes failed. Check output above.")
    except Exception as e:
        print(f"\n💥 HOTFIX FAILED: {e}")
        success = False
    return success


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
