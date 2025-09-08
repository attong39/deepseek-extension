# Script PowerShell khắc phục conflict settings VS Code
# Xử lý vấn đề global settings override workspace settings

param(
    [switch]$FixGlobal,
    [switch]$Backup
)

Write-Host "🔧 KHẮC PHỤC CONFLICT SETTINGS VS CODE" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

$GlobalSettingsPath = "$env:APPDATA\Code\User\settings.json"
$WorkspaceSettingsPath = ".vscode\settings.json"

Write-Host "📁 Global settings: $GlobalSettingsPath" -ForegroundColor White
Write-Host "📁 Workspace settings: $WorkspaceSettingsPath" -ForegroundColor White

# 1. Backup global settings nếu cần
if ($Backup) {
    $BackupPath = "$GlobalSettingsPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "`n💾 Tạo backup global settings..." -ForegroundColor Yellow
    Copy-Item $GlobalSettingsPath $BackupPath -Force
    Write-Host "✅ Backup created: $BackupPath" -ForegroundColor Green
}

# 2. Kiểm tra conflict
Write-Host "`n🔍 Kiểm tra conflict settings..." -ForegroundColor Cyan

# Đọc global settings
$GlobalPythonPath = Select-String -Path $GlobalSettingsPath -Pattern "python.*defaultInterpreterPath" -Context 0 | ForEach-Object { $_.Line }
if ($GlobalPythonPath) {
    Write-Host "❌ CONFLICT DETECTED!" -ForegroundColor Red
    Write-Host "Global setting: $GlobalPythonPath" -ForegroundColor Yellow
    
    # Đọc workspace settings
    $WorkspacePythonPath = Select-String -Path $WorkspaceSettingsPath -Pattern "python.*defaultInterpreterPath" -Context 2
    if ($WorkspacePythonPath) {
        Write-Host "Workspace setting:" -ForegroundColor White
        $WorkspacePythonPath | ForEach-Object { Write-Host "  $($_.Line)" -ForegroundColor White }
    }
}
else {
    Write-Host "✅ Không có global python.defaultInterpreterPath" -ForegroundColor Green
}

# 3. Giải pháp
Write-Host "`n💡 GIẢI PHÁP:" -ForegroundColor Cyan

if ($FixGlobal) {
    Write-Host "🔄 Đang xóa global python.defaultInterpreterPath..." -ForegroundColor Yellow
    
    try {
        # Đọc toàn bộ file
        $Content = Get-Content $GlobalSettingsPath -Raw
        
        # Xóa dòng python.defaultInterpreterPath
        $ModifiedContent = $Content -replace '(?m)^\s*"python\.defaultInterpreterPath":\s*"[^"]*",?\s*$', ''
        
        # Cleanup empty lines
        $ModifiedContent = $ModifiedContent -replace '(?m)^\s*\n', ''
        
        # Ghi lại file
        $ModifiedContent | Set-Content $GlobalSettingsPath -NoNewline
        
        Write-Host "✅ Đã xóa global python.defaultInterpreterPath" -ForegroundColor Green
        Write-Host "🎯 Workspace settings sẽ được ưu tiên" -ForegroundColor Green
        
    }
    catch {
        Write-Host "❌ Lỗi sửa global settings: $_" -ForegroundColor Red
        Write-Host "📋 Hãy sửa thủ công bằng cách:" -ForegroundColor Yellow
        Write-Host "   1. Mở: $GlobalSettingsPath" -ForegroundColor White
        Write-Host "   2. Xóa dòng: python.defaultInterpreterPath" -ForegroundColor White
        Write-Host "   3. Save file" -ForegroundColor White
    }
}
else {
    Write-Host "📋 Các bước khắc phục:" -ForegroundColor White
    Write-Host "1. 🔧 Chạy lại với flag -FixGlobal để tự động sửa" -ForegroundColor White
    Write-Host "   .\tools\fix_vscode_settings_conflict.ps1 -FixGlobal -Backup" -ForegroundColor Gray
    Write-Host "`n2. 🔨 Hoặc sửa thủ công:" -ForegroundColor White
    Write-Host "   - Mở: $GlobalSettingsPath" -ForegroundColor Gray
    Write-Host "   - Xóa dòng: python.defaultInterpreterPath" -ForegroundColor Gray
    Write-Host "   - Save file" -ForegroundColor Gray
    Write-Host "`n3. 🔄 Restart VS Code" -ForegroundColor White
    Write-Host "4. ✅ Workspace settings sẽ được ưu tiên" -ForegroundColor White
}

# 4. Verification
Write-Host "`n🧪 VERIFICATION:" -ForegroundColor Cyan
Write-Host "Sau khi sửa, chạy:" -ForegroundColor White
Write-Host "1. Restart VS Code" -ForegroundColor Gray
Write-Host "2. Ctrl+Shift+P → 'Python: Select Interpreter'" -ForegroundColor Gray
Write-Host "3. Chọn: E:\zeta\.venv\Scripts\python.exe" -ForegroundColor Gray
Write-Host "4. Mở terminal mới và kiểm tra: python --version" -ForegroundColor Gray

Write-Host "`n✅ Script hoàn thành!" -ForegroundColor Green
