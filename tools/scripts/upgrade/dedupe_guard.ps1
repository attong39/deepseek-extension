#!/usr/bin/env pwsh
# Code Duplication Detection Script - PowerShell version
param(
    [int]$Threshold = 2,
    [switch]$OpenReport = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Color = "White")
    Write-Host "— Dedupe Guard — $Message" -ForegroundColor $Color
}

function Test-Command($CommandName) {
    return [bool](Get-Command $CommandName -ErrorAction SilentlyContinue)
}

Write-Log "Starting code duplication analysis..." "Green"

# Ensure artifacts directory exists
$ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$OUTPUT_DIR = Join-Path $ROOT ".artifacts/jscpd-report"

if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
    Write-Log "Created output directory: $OUTPUT_DIR" "Cyan"
}

# Check for npx/jscpd
if (-not (Test-Command "npx")) {
    Write-Log "❌ npx not found. Please install Node.js first." "Red"
    exit 1
}

# Create jscpd configuration if it doesn't exist
$jscpdConfig = Join-Path $ROOT ".jscpd.json"
if (-not (Test-Path $jscpdConfig)) {
    Write-Log "Creating jscpd configuration..." "Cyan"
    
    $config = @{
        threshold = $Threshold
        minTokens = 40
        reporters = @("html", "console")
        ignore = @(
            "node_modules/**",
            "dist/**", 
            "build/**",
            ".artifacts/**",
            ".venv/**",
            "**/__pycache__/**",
            "**/*.min.js",
            "**/*.d.ts",
            ".git/**",
            "coverage/**",
            "reports/**"
        )
        patterns = @(
            @{
                path = "**/*.{ts,tsx,js,py,md}"
            }
        )
        format = @("typescript", "python", "markdown", "javascript")
        gitignore = $true
    } | ConvertTo-Json -Depth 10
    
    Set-Content -Path $jscpdConfig -Value $config
    Write-Log "✅ Created .jscpd.json configuration" "Green"
}

# Run jscpd analysis
Write-Log "Running jscpd analysis (threshold: $Threshold%)..." "Cyan"

try {
    Push-Location $ROOT
    
    $jscpdCommand = @(
        "npx jscpd",
        "--reporters html,console",
        "--output `"$OUTPUT_DIR`"",
        "--threshold $Threshold",
        "--min-tokens 40",
        "--pattern `"**/*.{ts,tsx,js,py,md}`"",
        "--ignore `"node_modules/**,dist/**,build/**,.artifacts/**,.venv/**,**/__pycache__/**`""
    ) -join " "
    
    if ($Verbose) {
        Write-Host "Executing: $jscpdCommand" -ForegroundColor DarkGray
    }
    
    Invoke-Expression $jscpdCommand
    
    $reportFile = Join-Path $OUTPUT_DIR "jscpd-report.html"
    if (Test-Path $reportFile) {
        Write-Log "✅ Duplication report generated: $reportFile" "Green"
        
        # Read and parse the report for summary
        try {
            $reportContent = Get-Content $reportFile -Raw
            
            # Try to extract duplication percentage from HTML
            if ($reportContent -match "(\d+\.?\d*)%.*duplication") {
                $duplicationRate = $matches[1]
                Write-Log "📊 Code duplication rate: $duplicationRate%" "Yellow"
                
                if ([float]$duplicationRate -gt $Threshold) {
                    Write-Log "⚠️ Duplication rate ($duplicationRate%) exceeds threshold ($Threshold%)" "Red"
                }
                else {
                    Write-Log "✅ Duplication rate ($duplicationRate%) is within threshold ($Threshold%)" "Green"
                }
            }
        }
        catch {
            Write-Log "⚠️ Could not parse duplication rate from report" "Yellow"
        }
        
        if ($OpenReport) {
            Write-Log "🌐 Opening duplication report..." "Cyan"
            Start-Process $reportFile
        }
    }
    else {
        Write-Log "⚠️ Report file not found, but jscpd may have run successfully" "Yellow"
    }
    
    # Generate summary report
    $summaryFile = Join-Path $OUTPUT_DIR "duplication_summary.txt"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $summary = @"
# Code Duplication Analysis Summary
Generated: $timestamp
Tool: jscpd
Threshold: $Threshold%
Output: $OUTPUT_DIR

## Analysis Scope
- File patterns: **/*.{ts,tsx,js,py,md}
- Minimum tokens: 40
- Ignored: node_modules, dist, build, .artifacts, .venv, __pycache__

## Results
- Report: $(if (Test-Path $reportFile) { "jscpd-report.html (OK)" } else { "jscpd-report.html (missing)" })
- Summary: This file

## Recommendations
1. Review the HTML report for specific duplications
2. Refactor code with >$Threshold% duplication
3. Consider extracting common patterns into utilities
4. Update .jscpd.json to ignore false positives
5. Add duplication checks to CI/CD pipeline

## Next Steps
- Open: $reportFile
- Configure: $jscpdConfig
- Integrate: Add to pre-commit hooks
"@

    Set-Content -Path $summaryFile -Value $summary
    Write-Log "📄 Summary saved to $summaryFile" "Green"
    
}
catch {
    Write-Log "❌ jscpd analysis failed: $($_.Exception.Message)" "Red"
    
    # Create error report
    $errorFile = Join-Path $OUTPUT_DIR "error.txt"
    $errorContent = @"
jscpd analysis failed at $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Error: $($_.Exception.Message)

Possible solutions:
1. Install Node.js and npm
2. Run 'npm install -g jscpd'
3. Check file patterns and paths
4. Verify .jscpd.json configuration
"@
    Set-Content -Path $errorFile -Value $errorContent
    throw
}
finally {
    Pop-Location
}

Write-Log "Duplication analysis completed. Report: $OUTPUT_DIR" "Green"