#!/usr/bin/env python3
"""
Xác thực runtime environment khớp với profile NumPy kỳ vọng.
Exit codes: 0 = OK, 1 = Warning (có thể chạy), 2 = Error (không thể chạy).
"""
from __future__ import annotations

import os
import importlib
import sys
from pathlib import Path
import ImportError
import IndexError
import ValueError
import bool
import faiss_ver
import getattr
import int
import module_name
import name
import print
import str
import torch_ver
import version


def get_version(module_name: str) -> str | None:
    """Lấy version của module nếu có thể import."""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, "__version__", "unknown")
    except ImportError:
        return None


def check_numpy_faiss_compatibility(numpy_ver: str, faiss_ver: str | None) -> bool:
    """Kiểm tra tương thích giữa NumPy và FAISS."""
    if not faiss_ver:
        return True  # FAISS không bắt buộc
    
    numpy_major = int(numpy_ver.split(".")[0])
    
    # FAISS có thể có vấn đề với NumPy 2.x
    if numpy_major >= 2:
        print(f"⚠️  NumPy {numpy_ver} với FAISS {faiss_ver} - cần test compatibility")
        return False
    
    return True


def check_torch_compatibility(numpy_ver: str, torch_ver: str | None) -> bool:
    """Kiểm tra tương thích giữa NumPy và PyTorch."""
    if not torch_ver:
        return True
    
    numpy_major = int(numpy_ver.split(".")[0])
    
    # PyTorch cũ có thể không tương thích với NumPy 2.x
    if numpy_major >= 2:
        try:
            torch_major = int(torch_ver.split(".")[0])
            torch_minor = int(torch_ver.split(".")[1])
            
            # PyTorch >= 2.4 mới hỗ trợ NumPy 2.x tốt
            if torch_major < 2 or (torch_major == 2 and torch_minor < 4):
                print(f"⚠️  PyTorch {torch_ver} có thể không tương thích với NumPy {numpy_ver}")
                return False
        except (ValueError, IndexError):
            print(f"⚠️  Không thể parse PyTorch version: {torch_ver}")
            return False
    
    return True


def main() -> int:
    """Main entry point."""
    # Đọc profile kỳ vọng từ env, mặc định auto-detect
    expected_profile = os.environ.get("ZETA_NUMPY_PROFILE", "").lower()
    
    # Kiểm tra NumPy
    numpy_ver = get_version("numpy")
    if not numpy_ver:
        print("❌ ERROR: NumPy không được cài đặt", file=sys.stderr)
        return 2
    
    # Xác định profile hiện tại
    major_version = int(numpy_ver.split(".")[0])
    current_profile = "np2" if major_version >= 2 else "np1"
    
    # Kiểm tra các thư viện quan trọng
    critical_deps = {
        "faiss": get_version("faiss"),
        "opencv": get_version("cv2"),
        "torch": get_version("torch"),
        "sentence_transformers": get_version("sentence_transformers"),
        "paddleocr": get_version("paddleocr"),
    }
    
    # Log thông tin cơ bản
    print(f"🔍 NumPy Runtime Check")
    print(f"NumPy: {numpy_ver} → Profile: {current_profile}")
    print(f"Expected: {expected_profile or 'auto'}")
    print(f"Python: {sys.version.split()[0]}")
    print("Dependencies:")
    for name, version in critical_deps.items():
        status = "✅" if version else "❌"
        print(f"  {status} {name}: {version or 'NOT_INSTALLED'}")
    
    exit_code = 0
    
    # Kiểm tra profile mismatch
    if expected_profile and expected_profile != current_profile:
        print(f"⚠️  WARNING: Profile mismatch (expected {expected_profile}, got {current_profile})", 
              file=sys.stderr)
        exit_code = 1
    
    # Kiểm tra compatibility giữa các thư viện
    if not check_numpy_faiss_compatibility(numpy_ver, critical_deps["faiss"]):
        exit_code = 1
    
    if not check_torch_compatibility(numpy_ver, critical_deps["torch"]):
        exit_code = 1
    
    # Kiểm tra thư viện quan trọng cho RAG
    if not critical_deps["sentence_transformers"]:
        print("⚠️  WARNING: Thiếu sentence_transformers - RAG sẽ không hoạt động", 
              file=sys.stderr)
        exit_code = 1
    
    # Kiểm tra OCR
    if not critical_deps["paddleocr"] and not get_version("pytesseract"):
        print("⚠️  WARNING: Thiếu OCR engine (paddleocr hoặc pytesseract)", 
              file=sys.stderr)
        exit_code = 1
    
    # Summary
    if exit_code == 0:
        print("✅ Runtime environment OK")
    elif exit_code == 1:
        print("⚠️  Runtime có warnings - có thể chạy nhưng cần review")
    else:
        print("❌ Runtime environment có lỗi nghiêm trọng")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
