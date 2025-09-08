#!/usr/bin/env python3
"""
Quick TypeScript Compilation Error Fixer
Automates bulk replacement of common errors in autonomousAI.ts
"""

import re
import f
import open
import print


def main():
    file_path = "E:/zeta/zeta-monorepo/zeta-ai-agent/src/core/integration/autonomousAI.ts"

    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Fix 1: Replace observability.log('error', ...) with Logger
    content = re.sub(
        r"this\.observability\.log\('error',\s*([^,]+),\s*([^)]+)\)",
        r"new Logger('AutonomousAI').error(\1, \2 as Error)",
        content,
    )

    # Fix 2: Replace observability.log('info', ...) with Logger
    content = re.sub(
        r"this\.observability\.log\('info',\s*([^,]+),\s*([^)]+)\)", r"new Logger('AutonomousAI').info(\1)", content
    )

    # Fix 3: Replace observability.log('warn', ...) with Logger
    content = re.sub(
        r"this\.observability\.log\('warn',\s*([^,]+),\s*([^)]+)\)", r"new Logger('AutonomousAI').warn(\1)", content
    )

    # Fix 4: Replace observability.log('debug', ...) with Logger
    content = re.sub(
        r"this\.observability\.log\('debug',\s*([^,]+)\)", r"new Logger('AutonomousAI').debug(\1)", content
    )

    # Fix 5: Replace observability.log('info', single_arg) with Logger
    content = re.sub(r"this\.observability\.log\('info',\s*([^)]+)\)", r"new Logger('AutonomousAI').info(\1)", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Bulk Logger fixes applied!")


if __name__ == "__main__":
    main()
