# Safe Backup Cleanup Script - PowerShell Version
# Xóa an toàn các file .security_backup không cần thiết

Write-Host "🧹 Safe Backup Cleanup Script" -ForegroundColor Green
Write-Host "=" * 40

# Tìm tất cả file backup
Write-Host "🔍 Đang quét file backup..." -ForegroundColor Yellow
$backupFiles = Get-ChildItem -Recurse -Filter "*.security_backup"
$totalCount = $backupFiles.Count

if ($totalCount -eq 0) {
    Write-Host "✅ Không tìm thấy file backup nào!" -ForegroundColor Green
    exit
}

# Tính tổng dung lượng
Write-Host "📊 Tìm thấy $totalCount file backup" -ForegroundColor Cyan
$totalSize = ($backupFiles | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)
Write-Host "💾 Tổng dung lượng: $totalSizeMB MB" -ForegroundColor Cyan

# Xác nhận trước khi xóa
$confirmation = Read-Host "`n⚠️ Bạn có chắc muốn xóa tất cả $totalCount file backup? (y/N)"

if ($confirmation -eq 'y' -or $confirmation -eq 'Y' -or $confirmation -eq 'yes') {
    
    # Tạo log file
    $logFile = "cleanup_log_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    Write-Host "`n📝 Tạo log file: $logFile" -ForegroundColor Yellow
    
    "Backup Cleanup Log - $(Get-Date)" | Out-File -FilePath $logFile -Encoding UTF8
    "=" * 50 | Out-File -FilePath $logFile -Append -Encoding UTF8
    "" | Out-File -FilePath $logFile -Append -Encoding UTF8
    
    # Xóa từng file và log
    $deletedCount = 0
    $errorCount = 0
    
    Write-Host "🗑️ Bắt đầu xóa file..." -ForegroundColor Yellow
    
    foreach ($file in $backupFiles) {
        try {
            $fileSize = $file.Length
            "DELETED: $($file.FullName) ($fileSize bytes)" | Out-File -FilePath $logFile -Append -Encoding UTF8
            
            Remove-Item -Path $file.FullName -Force
            $deletedCount++
            
            # Hiển thị progress mỗi 100 file
            if ($deletedCount % 100 -eq 0) {
                Write-Host "   Đã xóa: $deletedCount/$totalCount files..." -ForegroundColor Gray
            }
        }
        catch {
            "ERROR: Không thể xóa $($file.FullName) - $($_.Exception.Message)" | Out-File -FilePath $logFile -Append -Encoding UTF8
            Write-Host "⚠️ Lỗi khi xóa $($file.Name): $($_.Exception.Message)" -ForegroundColor Red
            $errorCount++
        }
    }
    
    # Ghi tổng kết vào log
    "`nTổng kết:" | Out-File -FilePath $logFile -Append -Encoding UTF8
    "- Files đã xóa: $deletedCount" | Out-File -FilePath $logFile -Append -Encoding UTF8
    "- Files lỗi: $errorCount" | Out-File -FilePath $logFile -Append -Encoding UTF8
    "- Dung lượng tiết kiệm: $totalSizeMB MB" | Out-File -FilePath $logFile -Append -Encoding UTF8
    
    # Cleanup thư mục trống
    Write-Host "`n🗂️ Cleanup thư mục trống..." -ForegroundColor Yellow
    $emptyDirs = Get-ChildItem -Recurse -Directory | Where-Object { (Get-ChildItem $_.FullName).Count -eq 0 }
    $removedDirs = 0
    
    foreach ($dir in $emptyDirs) {
        try {
            Remove-Item -Path $dir.FullName -Force
            Write-Host "   Xóa thư mục trống: $($dir.FullName)" -ForegroundColor Gray
            $removedDirs++
        }
        catch {
            # Ignore errors for non-empty directories
        }
    }
    
    # Kết quả cuối cùng
    Write-Host "`n✅ Cleanup hoàn tất!" -ForegroundColor Green
    Write-Host "📈 Kết quả:" -ForegroundColor Cyan
    Write-Host "   - Đã xóa: $deletedCount files" -ForegroundColor White
    Write-Host "   - Lỗi: $errorCount files" -ForegroundColor White  
    Write-Host "   - Tiết kiệm: $totalSizeMB MB" -ForegroundColor White
    Write-Host "   - Thư mục trống đã xóa: $removedDirs" -ForegroundColor White
    Write-Host "   - Log saved: $logFile" -ForegroundColor White
    Write-Host "`n🎉 Dự án đã được tối ưu!" -ForegroundColor Green
    
} else {
    Write-Host "❌ Hủy bỏ cleanup." -ForegroundColor Red
}
