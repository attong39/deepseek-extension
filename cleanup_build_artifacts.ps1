#!/usr/bin/env pwsh
# Zeta Monorepo - Safe Build Artifacts Cleanup
# Removes node_modules, .venv, and temporary files

Write-Host "🧹 Starting Build Artifacts Cleanup..." -ForegroundColor Green

# 1. Remove Node.js Dependencies
Write-Host "📦 Removing node_modules directories..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Name "node_modules" | ForEach-Object {
    $path = $_.FullName
    Write-Host "  Removing: $path"
    Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
}

# 2. Remove Python Virtual Environments (keep root .venv)
Write-Host "🐍 Removing temporary Python environments..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory | Where-Object { 
    $_.Name -match "\.venv-.*" -or $_.Name -eq ".venv-ollama" 
} | ForEach-Object {
    Write-Host "  Removing: $($_.FullName)"
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

# 3. Remove Log Files (older than 7 days)
Write-Host "📄 Cleaning old log files..." -ForegroundColor Yellow
$cutoffDate = (Get-Date).AddDays(-7)
Get-ChildItem -Path . -Recurse -File -Include "*.log" | Where-Object {
    $_.LastWriteTime -lt $cutoffDate
} | ForEach-Object {
    Write-Host "  Removing: $($_.FullName)"
    Remove-Item -Path $_.FullName -Force
}

# 4. Remove Cache and Temp Files
Write-Host "🗂️ Removing cache and temp files..." -ForegroundColor Yellow
$tempExtensions = @("*.cache", "*.tmp", "*.temp", "*.bak")
foreach ($ext in $tempExtensions) {
    Get-ChildItem -Path . -Recurse -File -Include $ext | ForEach-Object {
        Write-Host "  Removing: $($_.FullName)"
        Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue
    }
}

# 5. Remove Backup Directories
Write-Host "💾 Removing backup directories..." -ForegroundColor Yellow
Get-ChildItem -Path . -Recurse -Directory -Include ".cleanup_backup", "*_backup" | ForEach-Object {
    Write-Host "  Removing: $($_.FullName)"
    Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

# 6. Calculate Space Saved
Write-Host "📊 Calculating space savings..." -ForegroundColor Yellow
$totalFiles = (Get-ChildItem -Recurse -File | Measure-Object).Count
$totalSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "Current repository stats:" -ForegroundColor Cyan
Write-Host "  Total Files: $totalFiles"
Write-Host "  Total Size: $([math]::Round($totalSize, 2)) MB"

Write-Host "✅ Build artifacts cleanup completed!" -ForegroundColor Green
Write-Host "🔄 Run 'npm install' or 'pip install' to restore dependencies" -ForegroundColor Cyan
