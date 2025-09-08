import subprocess
import sys
from pathlib import Path
import FileNotFoundError
import int
import len
import list
import print
import script_path
import str

"""
Windows batch wrapper cho upgrade scripts
"""


def run_bash_script(script_path: str, *args) -> int:
    """Run bash script trên Windows thông qua Git Bash hoặc WSL"""
    script_full_path = Path(__file__).parent / script_path
    try:
        cmd = ["bash", str(script_full_path)] + list(args)
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        pass
    try:
        cmd = ["wsl", "bash", str(script_full_path)] + list(args)
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        pass
    print("❌ Không tìm thấy bash. Cài Git Bash hoặc WSL để chạy scripts.")
    return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python upgrade_wrapper.py <script_name> [args...]")
        print("Available scripts:")
        print("  upgrade_all.sh - Full upgrade")
        print("  py_quality.sh - Python quality only")
        print("  ts_quality.sh - TypeScript quality only")
        sys.exit(1)
    script_name = sys.argv[1]
    args = sys.argv[2:]
    if script_name == "upgrade_all":
        return run_bash_script("upgrade_all.sh", *args)
    elif script_name == "py_quality":
        return run_bash_script("py_quality.sh", *args)
    elif script_name == "ts_quality":
        return run_bash_script("ts_quality.sh", *args)
    else:
        print(f"❌ Unknown script: {script_name}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
