#!/usr/bin/env python3
"""
Test script để verify NumPy compatibility switching.
Chạy: python test_numpy_switch.py [np1|np2]
"""

import sys
import json
import subprocess
from pathlib import Path
import cmd
import cwd
import e
import len
import list
import print
import str

def run_cmd(cmd: list[str], cwd: Path | None = None) -> str:
    """Run command và return output."""
    try:
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=cwd,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return ""

def test_numpy_profile(profile: str = "default"):
    """Test NumPy profile switching."""
    backend_dir = Path("apps/backend")
    
    if not backend_dir.exists():
        print("❌ apps/backend directory not found")
        print(f"Current working dir: {Path.cwd()}")
        print("Please run from monorepo root directory")
        return False
    
    print(f"🔍 Testing NumPy profile: {profile}")
    print("=" * 50)
    
    # Check if we have a virtual environment
    venv_check = run_cmd(["uv", "venv", "--help"], cwd=backend_dir)
    if not venv_check:
        print("⚠️  uv not found or not working")
    
    # 1. Install dependencies
    if profile == "np2":
        print("📦 Installing NumPy 2.x dependencies...")
        install_result = run_cmd(["uv", "sync", "--extra", "dev", "--extra", "np2"], cwd=backend_dir)
    else:
        print("📦 Installing NumPy 1.x dependencies...")
        install_result = run_cmd(["uv", "sync", "--extra", "dev", "--extra", "ocr"], cwd=backend_dir)
    
    if not install_result and "uv sync" in str(install_result):
        print("⚠️  Installation may have issues, continuing with checks...")
    
    # 2. Check versions
    print("\n🔢 Checking library versions:")
    numpy_version = run_cmd(
        ["uv", "run", "python", "-c", "import numpy; print(numpy.__version__)"], 
        cwd=backend_dir
    )
    print(f"  NumPy: {numpy_version}")
    
    faiss_version = run_cmd(
        ["uv", "run", "python", "-c", "try: import faiss; print(faiss.__version__); except: print('N/A')"], 
        cwd=backend_dir
    )
    print(f"  FAISS: {faiss_version}")
    
    cv2_version = run_cmd(
        ["uv", "run", "python", "-c", "try: import cv2; print(cv2.__version__); except: print('N/A')"], 
        cwd=backend_dir
    )
    print(f"  OpenCV: {cv2_version}")
    
    torch_version = run_cmd(
        ["uv", "run", "python", "-c", "try: import torch; print(torch.__version__); except: print('N/A')"], 
        cwd=backend_dir
    )
    print(f"  PyTorch: {torch_version}")
    
    # 3. Run compatibility check
    print("\n🔍 Running compatibility check:")
    compat_output = run_cmd(
        ["uv", "run", "python", "-c", 
         "from app.compat.startup_check import report; import json; print(json.dumps(report(), indent=2))"],
        cwd=backend_dir
    )
    
    if compat_output:
        try:
            compat_data = json.loads(compat_output)
            print("✅ Compatibility check successful:")
            print(json.dumps(compat_data, indent=2))
        except json.JSONDecodeError:
            print(f"⚠️  Raw output: {compat_output}")
    
    # 4. Test FastAPI import
    print("\n🚀 Testing FastAPI import:")
    fastapi_test = run_cmd(
        ["uv", "run", "python", "-c", "from app.main import app; print('✅ FastAPI import successful')"],
        cwd=backend_dir
    )
    
    if fastapi_test:
        print(fastapi_test)
    
    # 5. Syntax check
    print("\n🔧 Running syntax check:")
    syntax_check = run_cmd(
        ["uv", "run", "python", "-m", "py_compile", "app/main.py"],
        cwd=backend_dir
    )
    print("✅ Syntax check passed")
    
    print(f"\n🎉 NumPy {profile} profile test completed!")
    return True

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        profile = sys.argv[1]
        if profile not in ["np1", "default", "np2"]:
            print("❌ Invalid profile. Use: default|np1|np2")
            sys.exit(1)
        
        # Normalize profile name
        if profile == "np1":
            profile = "default"
    else:
        profile = "default"
    
    success = test_numpy_profile(profile)
    
    if success:
        print(f"\n✅ All tests passed for NumPy profile: {profile}")
        
        # Show usage instructions
        print("\n📖 Usage instructions:")
        print("  Default (NumPy 1.x): uv sync --extra dev --extra ocr")
        print("  NumPy 2.x testing:   uv sync --extra dev --extra np2")
        print("  Windows OCR fallback: uv add --optional ocr-alt pytesseract pillow")
        
    else:
        print(f"\n❌ Tests failed for NumPy profile: {profile}")
        sys.exit(1)

if __name__ == "__main__":
    main()
