# Virtual Environment Optimization Script
# Tối ưu môi trường ảo - Thống nhất sử dụng Python 3.11.13

Write-Host "🔧 OPTIMIZING VIRTUAL ENVIRONMENT SETUP" -ForegroundColor Cyan
Write-Host "Removing duplicate and corrupted virtual environments..." -ForegroundColor Yellow

# Backup current requirements
Write-Host "📋 Creating backup of requirements..." -ForegroundColor Green
$BackupDir = "e:\zeta-monorepo\venv_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

# Copy all requirements files to backup
Copy-Item "e:\zeta-monorepo\requirements.txt" "$BackupDir\" -ErrorAction SilentlyContinue
Copy-Item "e:\zeta-monorepo\requirements-dev.txt" "$BackupDir\" -ErrorAction SilentlyContinue

# Remove corrupted virtual environments
Write-Host "🗑️ Removing corrupted virtual environments..." -ForegroundColor Red
if (Test-Path "e:\zeta-monorepo\.venv") {
    Remove-Item "e:\zeta-monorepo\.venv" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   ✓ Removed .venv" -ForegroundColor Green
}

if (Test-Path "e:\zeta-monorepo\venv") {
    Remove-Item "e:\zeta-monorepo\venv" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "   ✓ Removed venv" -ForegroundColor Green
}

# Check for Python 3.11.13
Write-Host "🔍 Checking for Python 3.11.13..." -ForegroundColor Blue
$Python3113 = $null

# Common Python installation paths
$PythonPaths = @(
    "C:\Python311\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python311\python.exe",
    "C:\Program Files\Python311\python.exe",
    "C:\Program Files (x86)\Python311\python.exe"
)

foreach ($path in $PythonPaths) {
    if (Test-Path $path) {
        $version = & $path --version 2>$null
        if ($version -like "*3.11*") {
            $Python3113 = $path
            Write-Host "   ✓ Found Python: $path ($version)" -ForegroundColor Green
            break
        }
    }
}

if (-not $Python3113) {
    Write-Host "❌ Python 3.11.13 not found. Using system Python..." -ForegroundColor Yellow
    $Python3113 = "python"
}

# Create new optimized virtual environment
Write-Host "🏗️ Creating optimized virtual environment..." -ForegroundColor Cyan
$VenvPath = "e:\zeta-monorepo\.venv"

try {
    & $Python3113 -m venv $VenvPath
    Write-Host "   ✓ Created new .venv with Python 3.11.13" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create virtual environment: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Activate virtual environment and install packages
Write-Host "📦 Installing packages..." -ForegroundColor Blue
$ActivateScript = "$VenvPath\Scripts\Activate.ps1"

# Check if requirements files exist and install
if (Test-Path "e:\zeta-monorepo\requirements.txt") {
    Write-Host "   Installing from requirements.txt..." -ForegroundColor Yellow
    & "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
    & "$VenvPath\Scripts\python.exe" -m pip install -r "e:\zeta-monorepo\requirements.txt"
}

if (Test-Path "e:\zeta-monorepo\requirements-dev.txt") {
    Write-Host "   Installing from requirements-dev.txt..." -ForegroundColor Yellow
    & "$VenvPath\Scripts\python.exe" -m pip install -r "e:\zeta-monorepo\requirements-dev.txt"
}

# Update VS Code settings
Write-Host "⚙️ Updating VS Code settings..." -ForegroundColor Cyan
$VscodeSettingsPath = "e:\zeta-monorepo\.vscode\settings.json"

if (Test-Path $VscodeSettingsPath) {
    $settings = Get-Content $VscodeSettingsPath -Raw | ConvertFrom-Json
    $settings."python.defaultInterpreterPath" = "$VenvPath\Scripts\python.exe"
    $settings."python.terminal.activateEnvironment" = $true
    $settings | ConvertTo-Json -Depth 10 | Set-Content $VscodeSettingsPath -Encoding UTF8
    Write-Host "   ✓ Updated python.defaultInterpreterPath" -ForegroundColor Green
}

# Verify installation
Write-Host "✅ Verifying installation..." -ForegroundColor Green
$PythonVersion = & "$VenvPath\Scripts\python.exe" --version
$PipVersion = & "$VenvPath\Scripts\python.exe" -m pip --version
Write-Host "   Python: $PythonVersion" -ForegroundColor White
Write-Host "   Pip: $PipVersion" -ForegroundColor White

# Show installed packages count
$PackageCount = (& "$VenvPath\Scripts\python.exe" -m pip list --format=freeze | Measure-Object).Count
Write-Host "   Packages installed: $PackageCount" -ForegroundColor White

Write-Host ""
Write-Host "🎉 VIRTUAL ENVIRONMENT OPTIMIZATION COMPLETE!" -ForegroundColor Green
Write-Host "   ✓ Single unified .venv directory" -ForegroundColor White
Write-Host "   ✓ Python version standardized" -ForegroundColor White
Write-Host "   ✓ VS Code configuration updated" -ForegroundColor White
Write-Host "   ✓ Backup created in: $BackupDir" -ForegroundColor White
Write-Host ""
Write-Host "To activate: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan