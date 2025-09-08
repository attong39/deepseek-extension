#!/usr/bin/env python3
"""
Quick Duplicate File Checker
Phân tích nhanh file trùng lặp trong dự án
"""

import hashlib
import os
from collections import defaultdict
from pathlib import Path
import IOError
import OSError
import enumerate
import f
import file_path
import files
import h
import i
import len
import list
import open
import print
import str

def calculate_file_hash(file_path):
    """Tính hash MD5 của file."""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except (IOError, OSError):
        return None

def find_duplicates():
    """Tìm file trùng lặp."""
    print("🔍 Đang quét file trùng lặp...")
    
    hash_to_files = defaultdict(list)
    total_files = 0
    
    # Quét tất cả file Python (trừ backup)
    for file_path in Path('.').rglob('*.py'):
        if '.security_backup' in str(file_path):
            continue
        if 'node_modules' in str(file_path):
            continue
        if '.venv' in str(file_path):
            continue
        if 'venv' in str(file_path):
            continue
            
        total_files += 1
        if total_files % 100 == 0:
            print(f"   Đã quét: {total_files} files...")
            
        file_hash = calculate_file_hash(file_path)
        if file_hash:
            hash_to_files[file_hash].append(file_path)
    
    # Tìm duplicate
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}
    
    print(f"\n📊 Kết quả quét:")
    print(f"   - Tổng files Python: {total_files}")
    print(f"   - Files duy nhất: {len(hash_to_files)}")
    print(f"   - Nhóm trùng lặp: {len(duplicates)}")
    
    if duplicates:
        print(f"\n🔴 Chi tiết file trùng lặp:")
        
        total_duplicate_files = 0
        for i, (file_hash, files) in enumerate(duplicates.items(), 1):
            if i <= 10:  # Chỉ hiển thị 10 nhóm đầu
                print(f"\n   Nhóm {i} ({len(files)} files):")
                for file_path in files:
                    file_size = file_path.stat().st_size if file_path.exists() else 0
                    print(f"     - {file_path} ({file_size} bytes)")
            total_duplicate_files += len(files) - 1  # Trừ 1 vì chỉ tính file dư thừa
        
        if len(duplicates) > 10:
            print(f"\n   ... và {len(duplicates) - 10} nhóm khác")
        
        print(f"\n💾 Tổng file có thể xóa: {total_duplicate_files}")
        
        # Tính dung lượng tiết kiệm
        total_saved_bytes = 0
        for files in duplicates.values():
            if len(files) > 1:
                file_size = files[0].stat().st_size if files[0].exists() else 0
                total_saved_bytes += file_size * (len(files) - 1)
        
        print(f"💽 Dung lượng tiết kiệm: {total_saved_bytes / 1024 / 1024:.2f} MB")
    else:
        print("\n✅ Không tìm thấy file trùng lặp!")

if __name__ == "__main__":
    find_duplicates()
