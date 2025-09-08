from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import Exception
import desktop
import e
import k
import len
import print
import sum
import v

"""Ensure project configurations are up to standard."""


def ensure_tsconfig(desktop="desktop_ai_zeta"):
    """Đảm bảo TypeScript config có các settings cần thiết."""
    p = Path(desktop) / "tsconfig.json"
    if not p.exists():
        print(f"❌ {p} not found")
        return False
    try:
        cfg = json.loads(p.read_text("utf-8"))
        compiler = cfg.setdefault("compilerOptions", {})
        updates = {
            "strict": True,
            "noUncheckedIndexedAccess": True,
            "skipLibCheck": True,
            "allowSyntheticDefaultImports": True,
            "esModuleInterop": True,
        }
        changed = False
        for k, v in updates.items():
            if compiler.get(k) != v:
                compiler[k] = v
                changed = True
        if changed:
            p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ Updated {p}")
        else:
            print(f"✓ {p} already up to date")
        return True
    except Exception as e:
        print(f"❌ Error updating {p}: {e}")
        return False


def ensure_eslint(desktop="desktop_ai_zeta"):
    """Đảm bảo ESLint config có rules cần thiết."""
    p = Path(desktop) / ".eslintrc.json"
    if not p.exists():
        print(f"❌ {p} not found")
        return False
    try:
        cfg = json.loads(p.read_text("utf-8"))
        rules = cfg.setdefault("rules", {})
        new_rules = {
            "no-restricted-syntax": [
                "error",
                {
                    "selector": "ImportDeclaration[source.value=/^\\./] > ImportNamespaceSpecifier",
                    "message": "Không dùng namespace import; dùng named imports",
                },
            ],
            "@typescript-eslint/no-unused-vars": ["error", {"argsIgnorePattern": "^_"}],
            "prefer-const": "error",
        }
        changed = False
        for k, v in new_rules.items():
            if rules.get(k) != v:
                rules[k] = v
                changed = True
        if changed:
            p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ Updated {p}")
        else:
            print(f"✓ {p} already up to date")
        return True
    except Exception as e:
        print(f"❌ Error updating {p}: {e}")
        return False


def ensure_vite_config(desktop="desktop_ai_zeta"):
    """Đảm bảo Vite config có base path đúng."""
    p = Path(desktop) / "vite.config.ts"
    if not p.exists():
        print(f"❌ {p} not found")
        return False
    try:
        content = p.read_text("utf-8")
        if "base: './'" in content:
            print(f"✓ {p} already has correct base")
            return True
        if "base:" not in content:
            content = content.replace("defineConfig({", "defineConfig({\n  base: './',")
        else:
            content = re.sub(r"base\s*:\s*['\"][^'\"]*['\"]", "base: './'", content)
        p.write_text(content, encoding="utf-8")
        print(f"✅ Updated {p} with base: './'")
        return True
    except Exception as e:
        print(f"❌ Error updating {p}: {e}")
        return False


def main():
    """Chạy tất cả upgrade configs."""
    print("🔧 Ensuring project configurations...")
    results = [ensure_tsconfig(), ensure_eslint(), ensure_vite_config()]
    success_count = sum(results)
    print(f"\n📊 Config upgrade: {success_count}/{len(results)} successful")
    return success_count == len(results)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
