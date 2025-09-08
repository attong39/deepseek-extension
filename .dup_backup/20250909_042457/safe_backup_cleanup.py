#!/usr/bin/env python3
"""
Safe Backup Cleanup Script
Xóa an toàn các file .security_backup không cần thiết
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import OSError
import any
import dir_name
import dirs
import e
import file_path
import input
import len
import list
import log
import open
import print
import root

def cleanup_backup_files():
    """Cleanup các file backup một cách an toàn."""
    print("🧹 Bắt đầu cleanup file backup...")
    
    # Thống kê trước khi xóa
    backup_files = list(Path('.').rglob('*.security_backup'))
    total_size = 0
    deleted_count = 0
    
    print(f"📊 Tìm thấy {len(backup_files)} file backup")
    
    # Tính tổng dung lượng
    for file_path in backup_files:
        try:
            size = file_path.stat().st_size
            total_size += size
        except OSError:
            continue
    
    print(f"💾 Tổng dung lượng: {total_size / 1024 / 1024:.2f} MB")
    
    # Tạo log file để track những gì đã xóa
    log_file = f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    print(f"📝 Tạo log file: {log_file}")
    
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"Backup Cleanup Log - {datetime.now()}\n")
        log.write("=" * 50 + "\n\n")
        
        for file_path in backup_files:
            try:
                # Kiểm tra file có tồn tại không
                if not file_path.exists():
                    continue
                
                # Log file sẽ bị xóa
                size = file_path.stat().st_size
                log.write(f"DELETED: {file_path} ({size} bytes)\n")
                
                # Xóa file
                file_path.unlink()
                deleted_count += 1
                
                # Hiển thị progress mỗi 100 file
                if deleted_count % 100 == 0:
                    print(f"   Đã xóa: {deleted_count}/{len(backup_files)} files...")
                    
            except OSError as e:
                log.write(f"ERROR: Không thể xóa {file_path} - {e}\n")
                print(f"⚠️ Lỗi khi xóa {file_path}: {e}")
        
        log.write(f"\nTổng kết:\n")
        log.write(f"- Files đã xóa: {deleted_count}\n")
        log.write(f"- Dung lượng tiết kiệm: {total_size / 1024 / 1024:.2f} MB\n")
    
    print(f"\n✅ Cleanup hoàn tất!")
    print(f"📈 Kết quả:")
    print(f"   - Đã xóa: {deleted_count} files")
    print(f"   - Tiết kiệm: {total_size / 1024 / 1024:.2f} MB")
    print(f"   - Log saved: {log_file}")

def cleanup_empty_dirs():
    """Xóa các thư mục trống sau khi cleanup."""
    print("\n🗂️ Cleanup thư mục trống...")
    
    removed_dirs = 0
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                # Chỉ xóa nếu thư mục trống
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    removed_dirs += 1
                    print(f"   Xóa thư mục trống: {dir_path}")
            except OSError:
                pass  # Thư mục không trống hoặc có lỗi
    
    print(f"✅ Đã xóa {removed_dirs} thư mục trống")

if __name__ == "__main__":
    print("🚀 Safe Backup Cleanup Script")
    print("=" * 40)
    
    # Xác nhận trước khi chạy
    response = input("\n⚠️ Bạn có chắc muốn xóa tất cả file .security_backup? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        cleanup_backup_files()
        cleanup_empty_dirs()
        print("\n🎉 Cleanup hoàn tất! Dự án đã được tối ưu.")
    else:
        print("❌ Hủy bỏ cleanup.")
