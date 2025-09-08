#!/usr/bin/env python3
"""
Setup script for AI Project Intelligence optional dependencies
"""

import subprocess
import sys
import dep
import print


def install_dependencies() -> None:
    """Install optional dependencies"""
    dependencies = ["ollama", "watchdog"]

    print("Installing optional dependencies for AI Project Intelligence...")

    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Successfully installed {dep}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")

    print("\nSetup complete. You can now use the full functionality.")
    print("Run 'python brain.py --root .' to analyze your project.")


if __name__ == "__main__":
    install_dependencies()
