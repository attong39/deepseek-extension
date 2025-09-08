#!/usr/bin/env powershell
# Quick test script for updated quality gates

Write-Host "🧪 Testing Updated Quality Gates for zeta_vn_restructured" -ForegroundColor Cyan

# Test VS Code settings update
Write-Host "`n1. Testing VS Code settings..." -ForegroundColor Yellow
if (Test-Path ".vscode/settings.json") {
    $settings = Get-Content ".vscode/settings.json" | ConvertFrom-Json
    if ($settings."python.analysis.extraPaths" -contains "zeta_vn_restructured") {
        Write-Host "✅ VS Code settings include zeta_vn_restructured paths" -ForegroundColor Green
    } else {
        Write-Host "❌ VS Code settings missing restructured paths" -ForegroundColor Red
    }
}

# Test tasks.json update
Write-Host "`n2. Testing tasks.json..." -ForegroundColor Yellow
if (Test-Path ".vscode/tasks.json") {
    $tasks = Get-Content ".vscode/tasks.json" -Raw
    if ($tasks -match "zeta_vn_restructured") {
        Write-Host "✅ Tasks include zeta_vn_restructured" -ForegroundColor Green
    } else {
        Write-Host "❌ Tasks missing restructured paths" -ForegroundColor Red
    }
}

# Test quality gates script
Write-Host "`n3. Testing quality gates script..." -ForegroundColor Yellow
if (Test-Path "scripts/quality/quality_gates.ps1") {
    $script = Get-Content "scripts/quality/quality_gates.ps1" -Raw
    if ($script -match "zeta_vn_restructured") {
        Write-Host "✅ Quality gates script includes restructured paths" -ForegroundColor Green
    } else {
        Write-Host "❌ Quality gates script missing restructured paths" -ForegroundColor Red
    }
}

# Test pre-commit config
Write-Host "`n4. Testing pre-commit config..." -ForegroundColor Yellow
if (Test-Path ".pre-commit-config.yaml") {
    $precommit = Get-Content ".pre-commit-config.yaml" -Raw
    if ($precommit -match "zeta_vn_restructured") {
        Write-Host "✅ Pre-commit config includes restructured paths" -ForegroundColor Green
    } else {
        Write-Host "❌ Pre-commit config missing restructured paths" -ForegroundColor Red
    }
}

# Test if uv can find both packages
Write-Host "`n5. Testing package discovery..." -ForegroundColor Yellow
try {
    $ruffCheck = uv run ruff check . --dry-run 2>&1
    Write-Host "✅ Ruff can scan both projects" -ForegroundColor Green
} catch {
    Write-Host "❌ Ruff check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test key shortcuts
Write-Host "`n6. Available shortcuts:" -ForegroundColor Yellow
Write-Host "   Ctrl+Shift+9: Quick quality gates" -ForegroundColor Gray
Write-Host "   Ctrl+Shift+0: Full quality gates" -ForegroundColor Gray

Write-Host "`n🎯 Test completed! Check results above." -ForegroundColor Cyan
Write-Host "💡 To run quality gates manually:" -ForegroundColor Yellow
Write-Host "   pwsh scripts/quality/quality_gates.ps1 -Mode quick" -ForegroundColor Gray
Write-Host "   pwsh scripts/quality/quality_gates.ps1 -Mode full" -ForegroundColor Gray