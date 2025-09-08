# Advanced Duplicate Code Analysis Script for Zeta AI Server
# ========================================================

param(
    [string]$Target = "zeta_vn",
    [string]$Format = "all",
    [double]$Similarity = 0.8,
    [switch]$AutoFix,
    [switch]$Interactive
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 ZETA AI SERVER - ADVANCED DUPLICATE ANALYSIS" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Set project root
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Activate virtual environment
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
}

# Create reports directory
$ReportsDir = Join-Path $ProjectRoot "reports"
if (!(Test-Path $ReportsDir)) {
    New-Item -ItemType Directory -Path $ReportsDir | Out-Null
}

Write-Host "📊 Running duplicate code analysis..." -ForegroundColor Green
Write-Host "  Target: $Target" -ForegroundColor Gray
Write-Host "  Format: $Format" -ForegroundColor Gray
Write-Host "  Similarity threshold: $Similarity" -ForegroundColor Gray

# Run main analysis
try {
    $analysisArgs = @(
        "scripts\duplicate_code_analyzer.py",
        $Target,
        "--output", $ReportsDir,
        "--format", $Format,
        "--similarity", $Similarity
    )

    & python @analysisArgs

    if ($LASTEXITCODE -ne 0) {
        throw "Analysis failed with exit code $LASTEXITCODE"
    }

    Write-Host "✅ Analysis completed successfully!" -ForegroundColor Green

}
catch {
    Write-Host "❌ Analysis failed: $_" -ForegroundColor Red
    exit 1
}

# Interactive mode
if ($Interactive) {
    Write-Host "`n🔧 INTERACTIVE MODE" -ForegroundColor Cyan
    Write-Host "=================" -ForegroundColor Cyan

    do {
        Write-Host "`nAvailable actions:" -ForegroundColor Yellow
        Write-Host "1. Open HTML report" -ForegroundColor Gray
        Write-Host "2. View JSON report" -ForegroundColor Gray
        Write-Host "3. Run specific file analysis" -ForegroundColor Gray
        Write-Host "4. Search for specific duplicates" -ForegroundColor Gray
        Write-Host "5. Generate refactoring script" -ForegroundColor Gray
        Write-Host "0. Exit" -ForegroundColor Gray

        $choice = Read-Host "`nSelect action (0-5)"

        switch ($choice) {
            "1" {
                $htmlReport = Join-Path $ReportsDir "duplicate_analysis_report.html"
                if (Test-Path $htmlReport) {
                    Start-Process $htmlReport
                }
                else {
                    Write-Host "❌ HTML report not found" -ForegroundColor Red
                }
            }
            "2" {
                $jsonReport = Join-Path $ReportsDir "duplicate_analysis_report.json"
                if (Test-Path $jsonReport) {
                    Get-Content $jsonReport | ConvertFrom-Json | ConvertTo-Json -Depth 10 | Out-Host
                }
                else {
                    Write-Host "❌ JSON report not found" -ForegroundColor Red
                }
            }
            "3" {
                $filePath = Read-Host "Enter file path to analyze"
                if (Test-Path $filePath) {
                    # Run analysis on specific file
                    Write-Host "📝 Analyzing $filePath..." -ForegroundColor Yellow
                    # TODO: Implement single file analysis
                }
                else {
                    Write-Host "❌ File not found: $filePath" -ForegroundColor Red
                }
            }
            "4" {
                $searchTerm = Read-Host "Enter function/class name to search for duplicates"
                Write-Host "🔍 Searching for duplicates of '$searchTerm'..." -ForegroundColor Yellow
                # TODO: Implement specific search
            }
            "5" {
                Write-Host "🔧 Generating refactoring script..." -ForegroundColor Yellow
                # TODO: Generate refactoring suggestions script
            }
            "0" {
                Write-Host "👋 Exiting..." -ForegroundColor Green
                break
            }
            default {
                Write-Host "❌ Invalid choice" -ForegroundColor Red
            }
        }
    } while ($choice -ne "0")
}

# Auto-fix mode
if ($AutoFix) {
    Write-Host "`n🔧 AUTO-FIX MODE" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan

    $jsonReport = Join-Path $ReportsDir "duplicate_analysis_report.json"
    if (Test-Path $jsonReport) {
        $reportData = Get-Content $jsonReport | ConvertFrom-Json

        Write-Host "🔍 Found potential fixes:" -ForegroundColor Yellow

        # Auto-fix unused imports
        if ($reportData.unused_imports) {
            $confirm = Read-Host "Remove unused imports? (y/N)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                Write-Host "🧹 Removing unused imports..." -ForegroundColor Yellow
                # TODO: Implement auto-removal of unused imports
                foreach ($file in $reportData.unused_imports.PSObject.Properties.Name) {
                    Write-Host "  Processing: $file" -ForegroundColor Gray
                }
            }
        }

        # Auto-fix duplicate functions (extract to utility)
        if ($reportData.duplicate_functions) {
            $confirm = Read-Host "Extract duplicate functions to utilities? (y/N)"
            if ($confirm -eq "y" -or $confirm -eq "Y") {
                Write-Host "🔧 Extracting duplicate functions..." -ForegroundColor Yellow
                # TODO: Implement function extraction
            }
        }
    }
}

# Generate summary
Write-Host "`n📊 ANALYSIS SUMMARY" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

$files = Get-ChildItem -Path $ReportsDir -Filter "*.html", "*.json"
foreach ($file in $files) {
    Write-Host "📄 $($file.Name)" -ForegroundColor Green
    Write-Host "   Size: $([math]::Round($file.Length / 1KB, 2)) KB" -ForegroundColor Gray
    Write-Host "   Path: $($file.FullName)" -ForegroundColor Gray
}

# Performance metrics
$pythonFiles = Get-ChildItem -Path $Target -Recurse -Filter "*.py" | Where-Object {
    $_.FullName -notmatch "__pycache__" -and
    $_.FullName -notmatch ".venv" -and
    $_.FullName -notmatch "migrations"
}

Write-Host "`n📈 PROJECT METRICS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "Python files: $($pythonFiles.Count)" -ForegroundColor Gray
Write-Host "Total lines: $((Get-Content $pythonFiles.FullName | Measure-Object -Line).Lines)" -ForegroundColor Gray
Write-Host "Average file size: $([math]::Round(($pythonFiles | Measure-Object -Property Length -Average).Average / 1KB, 2)) KB" -ForegroundColor Gray

Write-Host "`n🎯 RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host "1. Review the HTML report for visual analysis" -ForegroundColor Yellow
Write-Host "2. Focus on functions with >80% similarity" -ForegroundColor Yellow
Write-Host "3. Create utility modules for common patterns" -ForegroundColor Yellow
Write-Host "4. Use inheritance for similar classes" -ForegroundColor Yellow
Write-Host "5. Implement factory patterns for object creation" -ForegroundColor Yellow

Write-Host "`n✅ Analysis complete! Reports saved to: $ReportsDir" -ForegroundColor Green
