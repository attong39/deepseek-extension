# 🔧 Virtual Environment Integrity Check & Recovery
Write-Host "🔧 VIRTUAL ENVIRONMENT INTEGRITY CHECK" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

$venvPath = "E:\zeta-monorepo\.venv"
$scriptsPath = "$venvPath\Scripts"

# 1️⃣ Check current state
Write-Host "`n1️⃣ Checking current virtual environment..." -ForegroundColor Yellow

if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment directory exists" -ForegroundColor Green
    
    # Check Python executable
    $pythonExe = "$scriptsPath\python.exe"
    if (Test-Path $pythonExe) {
        Write-Host "✅ Python executable found" -ForegroundColor Green
        
        # Get Python version
        try {
            $pythonVersion = & $pythonExe --version 2>&1
            Write-Host "📋 Python version: $pythonVersion" -ForegroundColor White
        } catch {
            Write-Host "⚠️ Cannot get Python version" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Python executable missing" -ForegroundColor Red
    }
    
    # Check activation scripts
    $activatePs1 = "$scriptsPath\Activate.ps1"
    $activateBat = "$scriptsPath\activate.bat"
    
    Write-Host "`n📋 Activation scripts status:" -ForegroundColor Cyan
    Write-Host "   PowerShell (Activate.ps1): $(if (Test-Path $activatePs1) {'✅ Found'} else {'❌ Missing'})" -ForegroundColor White
    Write-Host "   Batch (activate.bat): $(if (Test-Path $activateBat) {'✅ Found'} else {'❌ Missing'})" -ForegroundColor White
    
    # List Scripts directory
    Write-Host "`n📂 Scripts directory contents:" -ForegroundColor Cyan
    Get-ChildItem $scriptsPath -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "   📄 $($_.Name)" -ForegroundColor Gray
    }
    
} else {
    Write-Host "❌ Virtual environment directory not found" -ForegroundColor Red
}

# 2️⃣ Fix/Recreate virtual environment
Write-Host "`n2️⃣ Fixing virtual environment..." -ForegroundColor Yellow

# Check if activation scripts are missing
$needsRecreate = $false
if (-not (Test-Path "$scriptsPath\Activate.ps1") -or -not (Test-Path "$scriptsPath\activate.bat")) {
    Write-Host "⚠️ Activation scripts missing - recreation needed" -ForegroundColor Yellow
    $needsRecreate = $true
}

if ($needsRecreate) {
    Write-Host "`n🔄 Recreating virtual environment..." -ForegroundColor Blue
    
    # Backup important files
    $backupDir = ".\venv_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    if (Test-Path $venvPath) {
        Write-Host "💾 Creating backup: $backupDir" -ForegroundColor Cyan
        
        # Copy important files only
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        if (Test-Path "$venvPath\pyvenv.cfg") {
            Copy-Item "$venvPath\pyvenv.cfg" "$backupDir\" -ErrorAction SilentlyContinue
        }
        if (Test-Path "$venvPath\Lib\site-packages") {
            $installedPackages = pip list --format=freeze 2>$null
            $installedPackages | Out-File "$backupDir\requirements_backup.txt" -Encoding UTF8
            Write-Host "📋 Saved package list to requirements_backup.txt" -ForegroundColor Green
        }
    }
    
    # Remove old venv safely
    Write-Host "🗑️ Removing corrupted virtual environment..." -ForegroundColor Yellow
    try {
        # Force unlock any locked files
        Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*zeta-monorepo*" } | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep 2
        
        Remove-Item $venvPath -Recurse -Force -ErrorAction Stop
        Write-Host "✅ Old virtual environment removed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Some files could not be removed: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "💡 You may need to restart VS Code and try again" -ForegroundColor Cyan
    }
    
    # Create new venv
    Write-Host "`n🚀 Creating new virtual environment..." -ForegroundColor Blue
    try {
        python -m venv .venv --upgrade-deps
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
        } else {
            throw "venv creation failed with exit code $LASTEXITCODE"
        }
    } catch {
        Write-Host "❌ Failed to create virtual environment: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Try running as Administrator or check Python installation" -ForegroundColor Cyan
        exit 1
    }
}

# 3️⃣ Verify integrity
Write-Host "`n3️⃣ Verifying virtual environment integrity..." -ForegroundColor Yellow

$allGood = $true
$checks = @(
    @{ Path = "$scriptsPath\python.exe"; Name = "Python executable" },
    @{ Path = "$scriptsPath\Activate.ps1"; Name = "PowerShell activation script" },
    @{ Path = "$scriptsPath\activate.bat"; Name = "Batch activation script" },
    @{ Path = "$scriptsPath\pip.exe"; Name = "Pip executable" },
    @{ Path = "$venvPath\pyvenv.cfg"; Name = "Virtual env config" }
)

foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "✅ $($check.Name): Found" -ForegroundColor Green
    } else {
        Write-Host "❌ $($check.Name): Missing" -ForegroundColor Red
        $allGood = $false
    }
}

# 4️⃣ Test activation
Write-Host "`n4️⃣ Testing virtual environment activation..." -ForegroundColor Yellow

if (Test-Path "$scriptsPath\Activate.ps1") {
    try {
        # Test PowerShell activation
        Write-Host "🔧 Testing PowerShell activation..." -ForegroundColor Blue
        
        # Create test script for activation
        $testScript = @"
& "$scriptsPath\Activate.ps1"
if (`$env:VIRTUAL_ENV) {
    Write-Host "✅ PowerShell activation: SUCCESS" -ForegroundColor Green
    Write-Host "📍 Virtual env path: `$env:VIRTUAL_ENV" -ForegroundColor White
    python --version
    pip --version
} else {
    Write-Host "❌ PowerShell activation: FAILED" -ForegroundColor Red
}
"@
        
        $testScript | Out-File ".\test_activation.ps1" -Encoding UTF8
        powershell -ExecutionPolicy Bypass -File ".\test_activation.ps1"
        Remove-Item ".\test_activation.ps1" -ErrorAction SilentlyContinue
        
    } catch {
        Write-Host "❌ Activation test failed: $($_.Exception.Message)" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "❌ Cannot test - Activate.ps1 missing" -ForegroundColor Red
    $allGood = $false
}

# 5️⃣ Install essential packages
Write-Host "`n5️⃣ Installing essential packages..." -ForegroundColor Yellow

if ($allGood) {
    # Activate and install packages
    $activateCmd = "& `"$scriptsPath\Activate.ps1`""
    $installCmd = @"
$activateCmd
pip install --upgrade pip setuptools wheel
pip install ruff black isort mypy
pip install requests fastapi uvicorn
pip list
"@
    
    try {
        $installCmd | Out-File ".\install_packages.ps1" -Encoding UTF8
        Write-Host "📦 Installing packages..." -ForegroundColor Blue
        powershell -ExecutionPolicy Bypass -File ".\install_packages.ps1"
        Remove-Item ".\install_packages.ps1" -ErrorAction SilentlyContinue
        Write-Host "✅ Essential packages installed" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Package installation had issues" -ForegroundColor Yellow
    }
}

# 6️⃣ Create activation helpers
Write-Host "`n6️⃣ Creating activation helpers..." -ForegroundColor Yellow

# PowerShell helper function
$psHelper = @"
# Virtual Environment Activation Helper for PowerShell
function Activate-VirtualEnv {
    param([string]`$Path = "$venvPath")
    
    `$activateScript = "`$Path\Scripts\Activate.ps1"
    if (Test-Path `$activateScript) {
        & `$activateScript
        if (`$env:VIRTUAL_ENV) {
            Write-Host "✅ Virtual environment activated: `$env:VIRTUAL_ENV" -ForegroundColor Green
            Write-Host "🐍 Python: `$(python --version)" -ForegroundColor Cyan
            Write-Host "📦 Pip: `$(pip --version)" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Activation script not found: `$activateScript" -ForegroundColor Red
        Write-Host "💡 Run: python -m venv .venv" -ForegroundColor Cyan
    }
}

# Deactivation helper
function Deactivate-VirtualEnv {
    if (`$env:VIRTUAL_ENV) {
        deactivate
        Write-Host "✅ Virtual environment deactivated" -ForegroundColor Green
    } else {
        Write-Host "⚠️ No virtual environment is currently active" -ForegroundColor Yellow
    }
}

# Quick activation for this project
function Activate-Zeta {
    Activate-VirtualEnv -Path "$venvPath"
}

Export-ModuleMember -Function Activate-VirtualEnv, Deactivate-VirtualEnv, Activate-Zeta
"@

$psHelper | Out-File ".\VirtualEnvHelper.psm1" -Encoding UTF8
Write-Host "✅ Created VirtualEnvHelper.psm1" -ForegroundColor Green

# Batch helper
$batchHelper = @"
@echo off
echo 🚀 Activating Zeta Virtual Environment...
call "$venvPath\Scripts\activate.bat"
if defined VIRTUAL_ENV (
    echo ✅ Virtual environment activated: %VIRTUAL_ENV%
    python --version
    pip --version
) else (
    echo ❌ Failed to activate virtual environment
)
"@

$batchHelper | Out-File ".\activate_zeta.bat" -Encoding UTF8
Write-Host "✅ Created activate_zeta.bat" -ForegroundColor Green

# 7️⃣ Final summary
Write-Host "`n" + "=" * 50 -ForegroundColor Gray
Write-Host "📊 VIRTUAL ENVIRONMENT STATUS" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

if ($allGood) {
    Write-Host "`n🎉 VIRTUAL ENVIRONMENT IS HEALTHY!" -ForegroundColor Green
    Write-Host "=" * 35 -ForegroundColor Green
    
    Write-Host "`n📋 Environment Details:" -ForegroundColor Cyan
    Write-Host "   📍 Path: $venvPath" -ForegroundColor White
    Write-Host "   🐍 Python: Available" -ForegroundColor White
    Write-Host "   📦 Pip: Available" -ForegroundColor White
    Write-Host "   ⚡ Activation: Ready" -ForegroundColor White
    
    Write-Host "`n🚀 ACTIVATION METHODS:" -ForegroundColor Cyan
    Write-Host "=" * 20 -ForegroundColor Gray
    
    Write-Host "`n1️⃣ PowerShell (Recommended):" -ForegroundColor Yellow
    Write-Host "   Import-Module .\VirtualEnvHelper.psm1" -ForegroundColor White
    Write-Host "   Activate-Zeta" -ForegroundColor White
    
    Write-Host "`n2️⃣ Direct PowerShell:" -ForegroundColor Yellow
    Write-Host "   . `"$scriptsPath\Activate.ps1`"" -ForegroundColor White
    
    Write-Host "`n3️⃣ Batch/CMD:" -ForegroundColor Yellow
    Write-Host "   .\activate_zeta.bat" -ForegroundColor White
    
    Write-Host "`n4️⃣ Direct Batch:" -ForegroundColor Yellow
    Write-Host "   $scriptsPath\activate.bat" -ForegroundColor White
    
    Write-Host "`n🔧 PACKAGE MANAGEMENT:" -ForegroundColor Cyan
    Write-Host "   pip install <package>    # Install package" -ForegroundColor White
    Write-Host "   pip list                 # List packages" -ForegroundColor White
    Write-Host "   pip freeze > requirements.txt  # Save deps" -ForegroundColor White
    
} else {
    Write-Host "`n❌ VIRTUAL ENVIRONMENT HAS ISSUES" -ForegroundColor Red
    Write-Host "=" * 35 -ForegroundColor Red
    
    Write-Host "`n🛠️ TROUBLESHOOTING STEPS:" -ForegroundColor Yellow
    Write-Host "1. Close all VS Code instances" -ForegroundColor White
    Write-Host "2. Run as Administrator" -ForegroundColor White
    Write-Host "3. python -m venv .venv --clear" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
}

Write-Host "`n💡 QUICK COMMANDS:" -ForegroundColor Cyan
Write-Host "Activate-Zeta              # Activate environment" -ForegroundColor Gray
Write-Host "python --version           # Check Python version" -ForegroundColor Gray
Write-Host "pip list                   # List installed packages" -ForegroundColor Gray
Write-Host "deactivate                 # Deactivate environment" -ForegroundColor Gray

Write-Host "`n✨ Virtual Environment Ready for Development! ✨" -ForegroundColor Magenta