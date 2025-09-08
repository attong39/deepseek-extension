#!/usr/bin/env pwsh
# Repository Size Monitoring Script

$totalFiles = (Get-ChildItem -Recurse -File | Measure-Object).Count
$totalSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "📊 Repository Statistics:" -ForegroundColor Green
Write-Host "Total Files: $totalFiles"
Write-Host "Total Size: $([math]::Round($totalSize, 2)) MB"

# Check for large directories
Write-Host "`n📁 Largest Directories:" -ForegroundColor Yellow
Get-ChildItem -Directory | ForEach-Object {
    $size = (Get-ChildItem -Path $_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    [PSCustomObject]@{
        Directory = $_.Name
        "Size (MB)" = [math]::Round($size, 2)
    }
} | Sort-Object "Size (MB)" -Descending | Select-Object -First 10 | Format-Table

# Alert if size exceeds threshold
if ($totalSize -gt 1000) {
    Write-Host "⚠️ Repository size exceeds 1GB - consider cleanup" -ForegroundColor Red
}
