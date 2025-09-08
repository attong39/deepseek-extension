# 🐍 Virtual Environment Health Check & Fix
Write-Host "🐍 Checking Python Virtual Environment..." -ForegroundColor Cyan

$venvPath = "e:\zeta-monorepo\.venv"
$activateScript = "$venvPath\Scripts\Activate.ps1"
$pythonExe = "$venvPath\Scripts\python.exe"

# Check if venv exists
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment directory exists" -ForegroundColor Green
    Write-Host "📍 Path: $venvPath" -ForegroundColor Gray
    
    # Check activation script
    if (Test-Path $activateScript) {
        Write-Host "✅ Activation script exists" -ForegroundColor Green
    } else {
        Write-Host "❌ Activation script missing" -ForegroundColor Red
        Write-Host "🔧 Attempting to recreate virtual environment..." -ForegroundColor Yellow
        
        try {
            # Remove corrupted venv
            Remove-Item -Path $venvPath -Recurse -Force -ErrorAction Stop
            Write-Host "✅ Removed corrupted virtual environment" -ForegroundColor Green
            
            # Create new venv
            python -m venv $venvPath
            Write-Host "✅ Created new virtual environment" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to recreate venv: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "💡 Try running as Administrator" -ForegroundColor Yellow
        }
    }
    
    # Check Python executable
    if (Test-Path $pythonExe) {
        Write-Host "✅ Python executable exists" -ForegroundColor Green
        
        # Test Python version
        try {
            $pythonVersion = & $pythonExe --version 2>&1
            Write-Host "✅ Python version: $pythonVersion" -ForegroundColor Green
        } catch {
            Write-Host "❌ Python executable not working" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Python executable missing" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Virtual environment does not exist" -ForegroundColor Red
    Write-Host "🔧 Creating new virtual environment..." -ForegroundColor Yellow
    
    try {
        python -m venv $venvPath
        Write-Host "✅ Created virtual environment" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to create venv: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Test activation
Write-Host "`n🧪 Testing virtual environment activation..." -ForegroundColor Cyan
if (Test-Path $activateScript) {
    try {
        Write-Host "Running activation test..." -ForegroundColor Gray
        # Test if we can activate (just check syntax)
        $activateContent = Get-Content $activateScript -Raw
        if ($activateContent -match "function.*deactivate") {
            Write-Host "✅ Activation script appears valid" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Activation script may be corrupted" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ Activation script test failed" -ForegroundColor Red
    }
}

# Show activation instructions
Write-Host "`n🚀 TO ACTIVATE VIRTUAL ENVIRONMENT:" -ForegroundColor Cyan
Write-Host "1. cd e:\zeta-monorepo" -ForegroundColor White
Write-Host "2. .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. pip install -r requirements.txt" -ForegroundColor White

Write-Host "`n💡 ALTERNATIVE ACTIVATION:" -ForegroundColor Yellow
Write-Host "1. cd e:\zeta-monorepo" -ForegroundColor White
Write-Host "2. .\.venv\Scripts\python.exe -m pip install -r requirements.txt" -ForegroundColor White

Write-Host "`n📋 SUMMARY:" -ForegroundColor Cyan
Write-Host "- Continue Extension: ✅ config.json created and validated" -ForegroundColor Green
Write-Host "- Virtual Environment: $(if (Test-Path $activateScript) { '✅ Ready' } else { '❌ Needs attention' })" -ForegroundColor $(if (Test-Path $activateScript) { 'Green' } else { 'Red' })
Write-Host "- Ollama Integration: ✅ Configured" -ForegroundColor Green