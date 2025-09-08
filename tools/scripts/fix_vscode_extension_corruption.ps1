# Script PowerShell khắc phục VS Code extension corruption
# Xử lý lỗi "Extension activation failed" và SonarLint issues

param(
    [switch]$Force,
    [switch]$Backup
)

Write-Host "🔧 KHẮC PHỤC VS CODE EXTENSION CORRUPTION" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

$ExtensionsPath = "$env:USERPROFILE\.vscode\extensions"
$LogPath = "$env:APPDATA\Code\logs"

Write-Host "📁 Extensions path: $ExtensionsPath" -ForegroundColor White
Write-Host "📁 Logs path: $LogPath" -ForegroundColor White

# 1. Phân tích lỗi từ logs
Write-Host "`n🔍 PHÂN TÍCH LỖI TỪ LOGS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

$LatestLogDir = Get-ChildItem $LogPath | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($LatestLogDir) {
    $CliLog = Join-Path $LatestLogDir.FullName "cli.log"
    if (Test-Path $CliLog) {
        Write-Host "📋 Analyzing latest CLI log..." -ForegroundColor Yellow
        $ErrorLines = Get-Content $CliLog | Select-String "error|Error|ERROR" | Select-Object -Last 5
        
        if ($ErrorLines) {
            Write-Host "❌ Recent errors found:" -ForegroundColor Red
            foreach ($line in $ErrorLines) {
                if ($line -match "sonarlint") {
                    Write-Host "  🎯 SonarLint issue: $($line.Line.Substring(0, [Math]::Min(100, $line.Line.Length)))..." -ForegroundColor Yellow
                }
                else {
                    Write-Host "  ⚠️  $($line.Line.Substring(0, [Math]::Min(80, $line.Line.Length)))..." -ForegroundColor Gray
                }
            }
        }
        else {
            Write-Host "✅ No recent errors in CLI log" -ForegroundColor Green
        }
    }
}

# 2. Kiểm tra SonarLint corruption
Write-Host "`n🔍 KIỂM TRA SONARLINT CORRUPTION" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

$SonarExtensions = Get-ChildItem $ExtensionsPath -Filter "*sonar*" -Directory
if ($SonarExtensions) {
    Write-Host "📦 Found SonarLint extensions: $($SonarExtensions.Count)" -ForegroundColor White
    
    foreach ($ext in $SonarExtensions) {
        Write-Host "`n📁 Checking: $($ext.Name)" -ForegroundColor White
        $PackageJson = Join-Path $ext.FullName "package.json"
        
        if (Test-Path $PackageJson) {
            Write-Host "  ✅ package.json exists" -ForegroundColor Green
            try {
                $Content = Get-Content $PackageJson -Raw | ConvertFrom-Json
                Write-Host "  ✅ Valid JSON structure" -ForegroundColor Green
                Write-Host "  📋 Version: $($Content.version)" -ForegroundColor Gray
            }
            catch {
                Write-Host "  ❌ Corrupted package.json: $_" -ForegroundColor Red
                Write-Host "  🔧 Marking for removal..." -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "  ❌ Missing package.json - CORRUPTED!" -ForegroundColor Red
            Write-Host "  🔧 Marking for removal..." -ForegroundColor Yellow
            
            if ($Force) {
                Write-Host "  🗑️  Removing corrupted extension..." -ForegroundColor Red
                Remove-Item $ext.FullName -Recurse -Force -ErrorAction SilentlyContinue
                if (-not (Test-Path $ext.FullName)) {
                    Write-Host "  ✅ Successfully removed" -ForegroundColor Green
                }
                else {
                    Write-Host "  ❌ Failed to remove - manual intervention needed" -ForegroundColor Red
                }
            }
        }
    }
}
else {
    Write-Host "ℹ️  No SonarLint extensions found" -ForegroundColor Gray
}

# 3. Kiểm tra extensions khác có vấn đề
Write-Host "`n🔍 KIỂM TRA CÁC EXTENSION KHÁC" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

$AllExtensions = Get-ChildItem $ExtensionsPath -Directory
$CorruptedExtensions = @()

Write-Host "📦 Total extensions: $($AllExtensions.Count)" -ForegroundColor White
Write-Host "🔍 Scanning for corruption..." -ForegroundColor Yellow

foreach ($ext in $AllExtensions) {
    $PackageJson = Join-Path $ext.FullName "package.json"
    if (-not (Test-Path $PackageJson)) {
        $CorruptedExtensions += $ext
    }
}

if ($CorruptedExtensions) {
    Write-Host "❌ Found $($CorruptedExtensions.Count) corrupted extensions:" -ForegroundColor Red
    foreach ($ext in $CorruptedExtensions) {
        Write-Host "  📁 $($ext.Name)" -ForegroundColor Yellow
    }
    
    if ($Force) {
        Write-Host "`n🔧 Removing all corrupted extensions..." -ForegroundColor Yellow
        foreach ($ext in $CorruptedExtensions) {
            Write-Host "  🗑️  Removing: $($ext.Name)" -ForegroundColor Red
            Remove-Item $ext.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
        Write-Host "✅ Cleanup completed" -ForegroundColor Green
    }
}
else {
    Write-Host "✅ No corrupted extensions found" -ForegroundColor Green
}

# 4. Kiểm tra Python extensions
Write-Host "`n🐍 KIỂM TRA PYTHON EXTENSIONS" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

$PythonExtensions = $AllExtensions | Where-Object { $_.Name -like "*python*" }
Write-Host "📦 Python extensions found: $($PythonExtensions.Count)" -ForegroundColor White

foreach ($ext in $PythonExtensions) {
    Write-Host "  📁 $($ext.Name)" -ForegroundColor Gray
    $PackageJson = Join-Path $ext.FullName "package.json"
    if (Test-Path $PackageJson) {
        try {
            $Content = Get-Content $PackageJson -Raw | ConvertFrom-Json
            Write-Host "    ✅ Version: $($Content.version)" -ForegroundColor Green
        }
        catch {
            Write-Host "    ❌ Corrupted JSON" -ForegroundColor Red
        }
    }
    else {
        Write-Host "    ❌ Missing package.json" -ForegroundColor Red
    }
}

# 5. Solutions và next steps
Write-Host "`n💡 GIẢI PHÁP VÀ KHUYẾN NGHỊ" -ForegroundColor Cyan
Write-Host "-" * 40 -ForegroundColor Gray

if (-not $Force) {
    Write-Host "📋 Để khắc phục tự động, chạy lại với -Force:" -ForegroundColor White
    Write-Host "   .\tools\fix_vscode_extension_corruption.ps1 -Force" -ForegroundColor Gray
}

Write-Host "`n🔄 Manual steps nếu cần:" -ForegroundColor White
Write-Host "1. Restart VS Code hoàn toàn" -ForegroundColor Gray
Write-Host "2. Ctrl+Shift+P → 'Developer: Restart Extension Host'" -ForegroundColor Gray
Write-Host "3. Reinstall SonarLint nếu cần:" -ForegroundColor Gray
Write-Host "   - Ctrl+Shift+X → Search 'SonarLint'" -ForegroundColor Gray
Write-Host "   - Uninstall → Install" -ForegroundColor Gray

Write-Host "`n🧪 Verification:" -ForegroundColor White
Write-Host "1. Check status bar không còn 'Extension activation failed'" -ForegroundColor Gray
Write-Host "2. Python extension hoạt động bình thường" -ForegroundColor Gray
Write-Host "3. Linting và formatting hoạt động" -ForegroundColor Gray

Write-Host "`n✅ Script completed!" -ForegroundColor Green
Write-Host "🎯 VS Code extension health should be improved." -ForegroundColor Cyan
