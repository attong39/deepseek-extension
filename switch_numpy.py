#!/usr/bin/env python3
"""
NumPy switching utility for development và testing.
Usage: python switch_numpy.py [np1|np2]
"""

import sys
import subprocess
from pathlib import Path
import bool
import cmd
import cwd
import e
import len
import list
import print
import str

def run_cmd(cmd: list[str], cwd: Path | None = None) -> bool:
    """Run command và return success status."""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with code {e.returncode}")
        return False

def switch_numpy_version(version: str = "np1"):
    """Switch NumPy version."""
    backend_dir = Path("apps/backend")
    
    if not backend_dir.exists():
        print("❌ Run from monorepo root: apps/backend not found")
        return False
    
    print(f"🔄 Switching to NumPy {version}...")
    
    if version == "np2":
        # NumPy 2.x: upgrade packages that support it
        commands = [
            ["uv", "remove", "numpy"],  # Remove current numpy pin
            ["uv", "add", "numpy>=2.0,<3.0"],  # Add numpy 2.x
            ["uv", "add", "torch>=2.4.0"],  # Upgrade PyTorch
            ["uv", "add", "opencv-python-headless>=4.10.0"],  # Upgrade OpenCV
            ["uv", "sync", "--extra", "dev", "--extra", "ocr"],  # Sync
        ]
        
        print("📦 Installing NumPy 2.x compatible packages...")
        
    else:  # np1 (default)
        # NumPy 1.x: pin to stable versions
        commands = [
            ["uv", "remove", "numpy"],  # Remove current numpy
            ["uv", "add", "numpy>=1.26.4,<2.0"],  # Pin to numpy 1.x
            ["uv", "sync", "--extra", "dev", "--extra", "ocr"],  # Sync
        ]
        
        print("📦 Installing NumPy 1.x stable packages...")
    
    # Execute commands
    for cmd in commands:
        if not run_cmd(cmd, cwd=backend_dir):
            print(f"❌ Failed at: {' '.join(cmd)}")
            return False
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    verify_cmd = [
        "uv", "run", "python", "-c",
        "import numpy; print(f'NumPy: {numpy.__version__}'); "
        "import torch; print(f'PyTorch: {torch.__version__}'); "
        "import cv2; print(f'OpenCV: {cv2.__version__}');"
    ]
    
    if run_cmd(verify_cmd, cwd=backend_dir):
        print(f"✅ Successfully switched to NumPy {version}")
        return True
    else:
        print(f"❌ Verification failed for NumPy {version}")
        return False

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python switch_numpy.py [np1|np2]")
        print("  np1: NumPy 1.x (stable, production)")
        print("  np2: NumPy 2.x (bleeding edge, testing)")
        sys.exit(1)
    
    version = sys.argv[1].lower()
    if version not in ["np1", "np2"]:
        print("❌ Invalid version. Use: np1 or np2")
        sys.exit(1)
    
    success = switch_numpy_version(version)
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 NumPy {version} setup complete!")
    print("\n📖 Next steps:")
    if version == "np2":
        print("  - Test compatibility: python test_numpy_switch.py np2")
        print("  - Check for warnings in app startup")
        print("  - Verify all features work correctly")
    else:
        print("  - Production ready with stable NumPy 1.x")
        print("  - Test compatibility: python test_numpy_switch.py default")

if __name__ == "__main__":
    main()
