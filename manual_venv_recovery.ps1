# 🔧 Manual Virtual Environment Recovery
Write-Host "🔧 MANUAL VIRTUAL ENVIRONMENT RECOVERY" -ForegroundColor Cyan
Write-Host "=" * 45 -ForegroundColor Gray

# Create activation scripts manually
$venvPath = "E:\zeta-monorepo\.venv"
$scriptsPath = "$venvPath\Scripts"

Write-Host "`n1️⃣ Creating missing activation scripts..." -ForegroundColor Yellow

# Create PowerShell activation script
$activatePs1Content = @'
# Virtual Environment Activation Script for PowerShell

$VenvDir = Split-Path $PSCommandPath -Parent
$VenvDir = Split-Path $VenvDir -Parent

$Env:VIRTUAL_ENV = $VenvDir
$Env:VIRTUAL_ENV_PROMPT = "(venv) "

# Add venv Scripts to PATH
$Env:PATH = "$VenvDir\Scripts;" + $Env:PATH

# Set prompt
function global:prompt {
    Write-Host "(venv) " -NoNewline -ForegroundColor Green
    return "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) "
}

# Create deactivate function
function global:deactivate {
    # Remove venv from PATH
    $PathArray = $Env:PATH.Split(';')
    $NewPath = $PathArray | Where-Object { $_ -notlike "*$VenvDir\Scripts*" }
    $Env:PATH = $NewPath -join ';'
    
    # Clear environment variables
    Remove-Item Env:VIRTUAL_ENV -ErrorAction SilentlyContinue
    Remove-Item Env:VIRTUAL_ENV_PROMPT -ErrorAction SilentlyContinue
    
    # Reset prompt
    Remove-Item Function:prompt -ErrorAction SilentlyContinue
    Remove-Item Function:deactivate -ErrorAction SilentlyContinue
    
    Write-Host "Virtual environment deactivated" -ForegroundColor Yellow
}

Write-Host "Virtual environment activated: $Env:VIRTUAL_ENV" -ForegroundColor Green
'@

# Create batch activation script  
$activateBatContent = @'
@echo off
set "VIRTUAL_ENV=E:\zeta-monorepo\.venv"
set "VIRTUAL_ENV_PROMPT=(venv) "

REM Add venv Scripts to PATH
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"

REM Set prompt
set "PROMPT=(venv) %PROMPT%"

echo Virtual environment activated: %VIRTUAL_ENV%
'@

try {
    # Ensure Scripts directory exists
    if (-not (Test-Path $scriptsPath)) {
        New-Item -ItemType Directory -Path $scriptsPath -Force | Out-Null
    }
    
    # Write PowerShell activation script
    $activatePs1Path = "$scriptsPath\Activate.ps1"
    $activatePs1Content | Out-File -FilePath $activatePs1Path -Encoding UTF8 -Force
    Write-Host "✅ Created Activate.ps1" -ForegroundColor Green
    
    # Write batch activation script
    $activateBatPath = "$scriptsPath\activate.bat"
    $activateBatContent | Out-File -FilePath $activateBatPath -Encoding UTF8 -Force  
    Write-Host "✅ Created activate.bat" -ForegroundColor Green
    
    # Create deactivate.bat
    $deactivateBatContent = @'
@echo off
set "PATH=%PATH:;E:\zeta-monorepo\.venv\Scripts=%"
set "VIRTUAL_ENV="
set "VIRTUAL_ENV_PROMPT="
set "PROMPT=%PROMPT:(venv) =%"
echo Virtual environment deactivated
'@
    
    $deactivateBatContent | Out-File -FilePath "$scriptsPath\deactivate.bat" -Encoding UTF8 -Force
    Write-Host "✅ Created deactivate.bat" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to create activation scripts: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2️⃣ Test activation
Write-Host "`n2️⃣ Testing manual activation..." -ForegroundColor Yellow

try {
    # Test PowerShell activation
    Write-Host "🧪 Testing PowerShell activation..." -ForegroundColor Blue
    
    # Create and run test script
    $testActivation = @"
. "$activatePs1Path"
if (`$env:VIRTUAL_ENV) {
    Write-Host "✅ Manual activation successful!" -ForegroundColor Green
    Write-Host "📍 VIRTUAL_ENV: `$env:VIRTUAL_ENV" -ForegroundColor White
    Write-Host "🐍 Python path: `$(Get-Command python -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source)" -ForegroundColor White
    
    # Test Python
    python --version 2>&1 | ForEach-Object { Write-Host "🐍 $_" -ForegroundColor Cyan }
    
    # Test pip if available
    if (Get-Command pip -ErrorAction SilentlyContinue) {
        pip --version 2>&1 | ForEach-Object { Write-Host "📦 $_" -ForegroundColor Cyan }
    }
} else {
    Write-Host "❌ Manual activation failed" -ForegroundColor Red
}
"@
    
    $testActivation | Out-File ".\test_manual_activation.ps1" -Encoding UTF8
    powershell -ExecutionPolicy Bypass -File ".\test_manual_activation.ps1"
    Remove-Item ".\test_manual_activation.ps1" -ErrorAction SilentlyContinue
    
} catch {
    Write-Host "❌ Test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# 3️⃣ Install essential packages using existing Python
Write-Host "`n3️⃣ Installing essential packages..." -ForegroundColor Yellow

try {
    # Use the Python in venv directly
    $pythonExe = "$scriptsPath\python.exe"
    if (Test-Path $pythonExe) {
        Write-Host "📦 Installing packages using venv Python..." -ForegroundColor Blue
        
        # Upgrade pip first
        & $pythonExe -m pip install --upgrade pip
        
        # Install essential packages
        $packages = @(
            "setuptools",
            "wheel", 
            "ruff",
            "black",
            "isort",
            "requests",
            "fastapi",
            "uvicorn"
        )
        
        foreach ($package in $packages) {
            Write-Host "📥 Installing $package..." -ForegroundColor Gray
            & $pythonExe -m pip install $package --quiet
        }
        
        Write-Host "✅ Essential packages installed" -ForegroundColor Green
        
        # Show installed packages
        Write-Host "`n📋 Installed packages:" -ForegroundColor Cyan
        & $pythonExe -m pip list | Select-Object -First 10 | ForEach-Object {
            Write-Host "   $_" -ForegroundColor Gray
        }
        
    } else {
        Write-Host "❌ Python executable not found in venv" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️ Package installation had issues: $($_.Exception.Message)" -ForegroundColor Yellow
}

# 4️⃣ Create helper functions
Write-Host "`n4️⃣ Creating helper functions..." -ForegroundColor Yellow

$helperModule = @"
# Zeta Virtual Environment Helper Module

function Activate-ZetaVenv {
    `$activateScript = "E:\zeta-monorepo\.venv\Scripts\Activate.ps1"
    if (Test-Path `$activateScript) {
        . `$activateScript
        Write-Host "🚀 Zeta virtual environment activated!" -ForegroundColor Green
    } else {
        Write-Host "❌ Activation script not found: `$activateScript" -ForegroundColor Red
    }
}

function Deactivate-ZetaVenv {
    if (`$env:VIRTUAL_ENV) {
        deactivate
        Write-Host "✅ Virtual environment deactivated" -ForegroundColor Green
    } else {
        Write-Host "⚠️ No virtual environment active" -ForegroundColor Yellow
    }
}

function Check-ZetaVenv {
    Write-Host "🔍 Virtual Environment Status:" -ForegroundColor Cyan
    if (`$env:VIRTUAL_ENV) {
        Write-Host "✅ Active: `$env:VIRTUAL_ENV" -ForegroundColor Green
        Write-Host "🐍 Python: `$(python --version 2>&1)" -ForegroundColor White
        Write-Host "📦 Pip: `$(pip --version 2>&1)" -ForegroundColor White
    } else {
        Write-Host "❌ No virtual environment active" -ForegroundColor Red
        Write-Host "💡 Run: Activate-ZetaVenv" -ForegroundColor Cyan
    }
}

# Aliases for convenience
Set-Alias -Name "venv" -Value "Activate-ZetaVenv"
Set-Alias -Name "devenv" -Value "Check-ZetaVenv"

Export-ModuleMember -Function Activate-ZetaVenv, Deactivate-ZetaVenv, Check-ZetaVenv -Alias venv, devenv
"@

$helperModule | Out-File ".\ZetaVenvHelper.psm1" -Encoding UTF8
Write-Host "✅ Created ZetaVenvHelper.psm1" -ForegroundColor Green

# 5️⃣ Final verification
Write-Host "`n5️⃣ Final verification..." -ForegroundColor Yellow

$checks = @(
    @{ Path = "$scriptsPath\python.exe"; Name = "Python executable" },
    @{ Path = "$scriptsPath\Activate.ps1"; Name = "PowerShell activation" },
    @{ Path = "$scriptsPath\activate.bat"; Name = "Batch activation" },
    @{ Path = "$venvPath\pyvenv.cfg"; Name = "Virtual env config" }
)

$allPassed = $true
foreach ($check in $checks) {
    if (Test-Path $check.Path) {
        Write-Host "✅ $($check.Name): OK" -ForegroundColor Green
    } else {
        Write-Host "❌ $($check.Name): Missing" -ForegroundColor Red
        $allPassed = $false
    }
}

# Summary
Write-Host "`n" + "=" * 45 -ForegroundColor Gray
if ($allPassed) {
    Write-Host "🎉 VIRTUAL ENVIRONMENT RECOVERY SUCCESSFUL!" -ForegroundColor Green
    Write-Host "=" * 45 -ForegroundColor Green
    
    Write-Host "`n🚀 USAGE INSTRUCTIONS:" -ForegroundColor Cyan
    Write-Host "=" * 20 -ForegroundColor Gray
    
    Write-Host "`n1️⃣ Load helper module:" -ForegroundColor Yellow
    Write-Host "   Import-Module .\ZetaVenvHelper.psm1" -ForegroundColor White
    
    Write-Host "`n2️⃣ Activate environment:" -ForegroundColor Yellow  
    Write-Host "   Activate-ZetaVenv" -ForegroundColor White
    Write-Host "   # or simply: venv" -ForegroundColor Gray
    
    Write-Host "`n3️⃣ Check status:" -ForegroundColor Yellow
    Write-Host "   Check-ZetaVenv" -ForegroundColor White
    Write-Host "   # or simply: devenv" -ForegroundColor Gray
    
    Write-Host "`n4️⃣ Deactivate:" -ForegroundColor Yellow
    Write-Host "   Deactivate-ZetaVenv" -ForegroundColor White
    Write-Host "   # or simply: deactivate" -ForegroundColor Gray
    
    Write-Host "`n💡 Quick test:" -ForegroundColor Cyan
    Write-Host "   Activate-ZetaVenv; python --version; pip list" -ForegroundColor White
    
} else {
    Write-Host "❌ SOME ISSUES REMAIN" -ForegroundColor Red
    Write-Host "💡 Check file permissions and try running as Administrator" -ForegroundColor Cyan
}

Write-Host "`n✨ Virtual Environment Ready! ✨" -ForegroundColor Magenta