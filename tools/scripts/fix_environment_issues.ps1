# Script PowerShell chẩn đoán và sửa lỗi môi trường VS Code
# Phân tích từ screenshot và đưa ra giải pháp cụ thể

param(
    [switch]$AutoFix,
    [switch]$DetailedAnalysis
)

Write-Host "🔍 CHẨN ĐOÁN LỖI MÔI TRƯỜNG VS CODE" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# 1. Kiểm tra Python Environment
Write-Host "`n🐍 PYTHON ENVIRONMENT CHECK:" -ForegroundColor Yellow
$VenvPython = "E:\zeta\.venv\Scripts\python.exe"
$CurrentPython = (Get-Command python -ErrorAction SilentlyContinue).Source

Write-Host "Current Python: $CurrentPython" -ForegroundColor White
Write-Host "Virtual Env Python: $VenvPython" -ForegroundColor White
Write-Host "VIRTUAL_ENV: $env:VIRTUAL_ENV" -ForegroundColor White

if ($env:VIRTUAL_ENV -and ($CurrentPython -eq $VenvPython)) {
    Write-Host "✅ Python environment: OK" -ForegroundColor Green
}
else {
    Write-Host "❌ Python environment: ISSUE" -ForegroundColor Red
}

# 2. Phân tích các lỗi từ Screenshot
Write-Host "`n📸 SCREENSHOT ISSUES ANALYSIS:" -ForegroundColor Yellow

$IssuesFromScreenshot = @(
    @{
        Issue    = "Extension activation failed - Developer: Toggle D..."
        Severity = "HIGH"
        Impact   = "Development tools không hoạt động"
        Solution = "Restart VS Code + Reload extensions"
    },
    @{
        Issue    = "Bookmarks extension notification"  
        Severity = "LOW"
        Impact   = "UI notification spam"
        Solution = "Install extension hoặc dismiss"
    },
    @{
        Issue    = "Workspace file prompt (zeta_vn.code-workspace)"
        Severity = "MEDIUM"
        Impact   = "Workspace configuration warning"
        Solution = "Open workspace file hoặc dismiss"
    },
    @{
        Issue    = "Python extension loading..."
        Severity = "MEDIUM"
        Impact   = "Python tools delayed loading"
        Solution = "Wait hoặc restart VS Code"
    }
)

foreach ($Issue in $IssuesFromScreenshot) {
    Write-Host "`n🔴 $($Issue.Issue) ($($Issue.Severity))" -ForegroundColor Red
    Write-Host "   💥 Impact: $($Issue.Impact)" -ForegroundColor White
    Write-Host "   💡 Solution: $($Issue.Solution)" -ForegroundColor Green
}

# 3. Kiểm tra VS Code Extensions
Write-Host "`n🔌 VS CODE EXTENSIONS CHECK:" -ForegroundColor Yellow

try {
    $Extensions = code --list-extensions
    $TotalExtensions = ($Extensions | Measure-Object).Count
    $PythonExtensions = $Extensions | Where-Object { $_ -like "*python*" }
    $ProblematicExtensions = @()
    
    Write-Host "Total extensions: $TotalExtensions" -ForegroundColor White
    Write-Host "Python extensions: $(($PythonExtensions | Measure-Object).Count)" -ForegroundColor White
    
    # Kiểm tra SonarLint
    $SonarLint = $Extensions | Where-Object { $_ -like "*sonarlint*" }
    if ($SonarLint) {
        Write-Host "SonarLint found: $SonarLint" -ForegroundColor White
        $SonarLintPath = "$env:USERPROFILE\.vscode\extensions\sonarsource.sonarlint-vscode*"
        $SonarLintDirs = Get-ChildItem $SonarLintPath -Directory -ErrorAction SilentlyContinue
        
        foreach ($Dir in $SonarLintDirs) {
            $PackageJson = Join-Path $Dir.FullName "package.json"
            if (-not (Test-Path $PackageJson)) {
                Write-Host "❌ Corrupted: $($Dir.Name)" -ForegroundColor Red
                $ProblematicExtensions += $Dir.Name
            }
            else {
                Write-Host "✅ OK: $($Dir.Name)" -ForegroundColor Green
            }
        }
    }
    
}
catch {
    Write-Host "❌ Error checking extensions: $_" -ForegroundColor Red
}

# 4. Đề xuất sửa lỗi cụ thể
Write-Host "`n🔧 ĐỀ XUẤT SỬA LỖI CỤ THỂ:" -ForegroundColor Cyan

$FixRecommendations = @(
    @{
        Priority = "HIGH"
        Action   = "Restart VS Code Development Environment"
        Commands = @(
            "1. Ctrl+Shift+P → 'Developer: Reload Window'",
            "2. Nếu vẫn lỗi: Close all VS Code → Reopen"
        )
    },
    @{
        Priority = "HIGH"
        Action   = "Fix Python Interpreter"
        Commands = @(
            "1. Ctrl+Shift+P → 'Python: Select Interpreter'",
            "2. Chọn: $VenvPython",
            "3. Wait for extension to load"
        )
    },
    @{
        Priority = "MEDIUM"
        Action   = "Handle Workspace Warning"
        Commands = @(
            "1. Click 'Open Workspace' để dùng workspace file",
            "2. Hoặc click X để dismiss và tiếp tục"
        )
    },
    @{
        Priority = "LOW"
        Action   = "Dismiss Bookmarks Notification"
        Commands = @(
            "1. Click 'Install' nếu muốn dùng extension",
            "2. Hoặc click X để dismiss"
        )
    }
)

if ($ProblematicExtensions.Count -gt 0) {
    $FixRecommendations += @{
        Priority = "HIGH"
        Action   = "Fix Corrupted Extensions"
        Commands = @(
            "1. Uninstall: code --uninstall-extension sonarsource.sonarlint-vscode",
            "2. Restart VS Code",
            "3. Reinstall: code --install-extension sonarsource.sonarlint-vscode"
        )
    }
}

foreach ($Fix in $FixRecommendations) {
    Write-Host "`n🎯 $($Fix.Action) ($($Fix.Priority))" -ForegroundColor Green
    foreach ($Command in $Fix.Commands) {
        Write-Host "   📋 $Command" -ForegroundColor White
    }
}

# 5. Auto-fix nếu được yêu cầu
if ($AutoFix) {
    Write-Host "`n🤖 EXECUTING AUTO-FIX..." -ForegroundColor Cyan
    
    # Reload VS Code window
    Write-Host "🔄 Reloading VS Code window..." -ForegroundColor Yellow
    try {
        code --command "workbench.action.reloadWindow"
        Start-Sleep 3
    }
    catch {
        Write-Host "❌ Could not reload window: $_" -ForegroundColor Red
    }
    
    # Clear extension cache
    Write-Host "🧹 Clearing extension cache..." -ForegroundColor Yellow
    $CacheFiles = Get-ChildItem "$env:USERPROFILE\.vscode\extensions" -Filter "*.cache" -Recurse -ErrorAction SilentlyContinue
    foreach ($Cache in $CacheFiles) {
        Remove-Item $Cache.FullName -Force -ErrorAction SilentlyContinue
    }
    
    Write-Host "✅ Auto-fix completed!" -ForegroundColor Green
}

# 6. Summary và next steps
Write-Host "`n" + "=" * 50 -ForegroundColor Gray
Write-Host "📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "Issues identified: $($IssuesFromScreenshot.Count)" -ForegroundColor White
Write-Host "Fixes available: $($FixRecommendations.Count)" -ForegroundColor White
Write-Host "Extensions total: $TotalExtensions" -ForegroundColor White
Write-Host "Problematic extensions: $($ProblematicExtensions.Count)" -ForegroundColor White

Write-Host "`n⚡ IMMEDIATE NEXT STEPS:" -ForegroundColor Cyan
Write-Host "1. 🔄 Restart VS Code completely (close all windows)" -ForegroundColor White
Write-Host "2. 🐍 Select Python interpreter: Ctrl+Shift+P → Python: Select Interpreter" -ForegroundColor White
Write-Host "3. 📋 Choose: $VenvPython" -ForegroundColor White
Write-Host "4. ⏳ Wait for all extensions to load" -ForegroundColor White
Write-Host "5. ✅ Verify: python --version should show Python 3.11.13" -ForegroundColor White

if (-not $AutoFix) {
    Write-Host "`n🤖 To run auto-fix:" -ForegroundColor Yellow
    Write-Host "   .\tools\fix_environment_issues.ps1 -AutoFix" -ForegroundColor Gray
}

Write-Host "`n✅ Environment diagnosis completed!" -ForegroundColor Green
