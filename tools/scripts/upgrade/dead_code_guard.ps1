#!/usr/bin/env pwsh
# Dead Code Detection Script - PowerShell version
param(
    [int]$MinConfidence = 80,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Color = "White")
    Write-Host "— Dead Code Guard — $Message" -ForegroundColor $Color
}

function Test-Command($CommandName) {
    return [bool](Get-Command $CommandName -ErrorAction SilentlyContinue)
}

Write-Log "Starting dead code analysis..." "Green"

# Ensure artifacts directory exists
$ROOT = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$OUTPUT_DIR = Join-Path $ROOT ".artifacts/deadcode"

if (-not (Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR -Force | Out-Null
    Write-Log "Created output directory: $OUTPUT_DIR" "Cyan"
}

Push-Location $ROOT

try {
    # 1. Python dead code analysis with vulture
    Write-Log "Analyzing Python dead code with vulture..." "Cyan"
    
    $vultureOutput = Join-Path $OUTPUT_DIR "vulture.txt"
    $pythonDirs = @("zeta_vn", "zeta_vn_restructured", "scripts")
    $pythonTargets = @()
    
    # Find Python directories that exist
    foreach ($dir in $pythonDirs) {
        if (Test-Path $dir) {
            $pythonTargets += $dir
        }
    }
    
    if ($pythonTargets.Count -gt 0) {
        $targetString = $pythonTargets -join " "
        
        try {
            if (Test-Command "uv") {
                $vultureCommand = "uvx vulture $targetString --min-confidence $MinConfidence"
            }
            else {
                $vultureCommand = "python -m vulture $targetString --min-confidence $MinConfidence"
            }
            
            if ($Verbose) {
                Write-Host "Executing: $vultureCommand" -ForegroundColor DarkGray
            }
            
            $vultureResult = Invoke-Expression $vultureCommand 2>&1 | Out-String
            Set-Content -Path $vultureOutput -Value $vultureResult
            
            # Count potential dead code items
            $lines = ($vultureResult -split "`n" | Where-Object { $_.Trim() -ne "" }).Count
            Write-Log "✅ Python analysis complete. Found $lines potential dead code items" "Green"
            
        }
        catch {
            $errorMsg = "Vulture analysis failed: $($_.Exception.Message)"
            Set-Content -Path $vultureOutput -Value $errorMsg
            Write-Log "⚠️ $errorMsg" "Yellow"
        }
    }
    else {
        $noTargetsMsg = "No Python directories found for analysis"
        Set-Content -Path $vultureOutput -Value $noTargetsMsg
        Write-Log "⚠️ $noTargetsMsg" "Yellow"
    }

    # 2. TypeScript unused exports analysis
    Write-Log "Analyzing TypeScript unused exports..." "Cyan"
    
    $tsPruneOutput = Join-Path $OUTPUT_DIR "ts-prune.txt"
    $frontendDirs = @("desktop_ai_zeta", "apps/desktop", "frontend")
    
    $tsPruneCompleted = $false
    foreach ($dir in $frontendDirs) {
        if (Test-Path $dir) {
            Write-Log "Found TypeScript directory: $dir" "Cyan"
            
            Push-Location $dir
            try {
                if (Test-Path "package.json") {
                    # Ensure dependencies are installed
                    if (Test-Command "npm") {
                        try {
                            & npm ci --silent 2>&1 | Out-Null
                        }
                        catch {
                            & npm install --silent 2>&1 | Out-Null
                        }
                    }
                    
                    # Run ts-prune
                    try {
                        $tsPruneCommand = "npx ts-prune"
                        if ($Verbose) {
                            Write-Host "Executing: $tsPruneCommand" -ForegroundColor DarkGray
                        }
                        
                        $tsPruneResult = Invoke-Expression $tsPruneCommand 2>&1 | Out-String
                        Set-Content -Path $tsPruneOutput -Value $tsPruneResult
                        
                        # Count unused exports
                        $unusedExports = ($tsPruneResult -split "`n" | Where-Object { $_ -match "used" }).Count
                        Write-Log "✅ TypeScript analysis complete. Found $unusedExports potentially unused exports" "Green"
                        $tsPruneCompleted = $true
                        
                    }
                    catch {
                        $errorMsg = "ts-prune analysis failed: $($_.Exception.Message)"
                        Set-Content -Path $tsPruneOutput -Value $errorMsg
                        Write-Log "⚠️ $errorMsg" "Yellow"
                    }
                }
                else {
                    Write-Log "⚠️ No package.json found in $dir" "Yellow"
                }
            }
            finally {
                Pop-Location
            }
            break  # Use first found directory
        }
    }
    
    if (-not $tsPruneCompleted) {
        $noFrontendMsg = "No TypeScript frontend directories found or ts-prune failed"
        Set-Content -Path $tsPruneOutput -Value $noFrontendMsg
        Write-Log "⚠️ $noFrontendMsg" "Yellow"
    }

    # 3. Generate comprehensive dead code report
    Write-Log "Generating dead code analysis report..." "Cyan"
    
    $reportFile = Join-Path $OUTPUT_DIR "dead_code_report.txt"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    # Read analysis results
    $vultureContent = if (Test-Path $vultureOutput) { Get-Content $vultureOutput -Raw } else { "Not available" }
    $tsPruneContent = if (Test-Path $tsPruneOutput) { Get-Content $tsPruneOutput -Raw } else { "Not available" }
    
    $report = @"
# Dead Code Analysis Report
Generated: $timestamp
Tools: vulture (Python), ts-prune (TypeScript)

## Configuration
- Python confidence threshold: $MinConfidence%
- Python targets: $($pythonTargets -join ", ")
- TypeScript targets: $($frontendDirs -join ", ")

## Python Dead Code (vulture)
$vultureContent

## TypeScript Unused Exports (ts-prune)
$tsPruneContent

## Summary
- Python report: $(if (Test-Path $vultureOutput) { "vulture.txt (OK)" } else { "vulture.txt (missing)" })
- TypeScript report: $(if (Test-Path $tsPruneOutput) { "ts-prune.txt (OK)" } else { "ts-prune.txt (missing)" })

## Recommendations
1. Review reported dead code carefully - tools may have false positives
2. Consider dynamic imports and reflection which tools can't detect
3. Remove confirmed dead code gradually in separate commits
4. Update configuration to ignore known false positives
5. Add dead code checks to CI/CD pipeline

## Configuration Files
- Python: Consider .vulture-whitelist for false positives
- TypeScript: Check tsconfig.json and consider ts-unused-exports

## Next Steps
1. Manual review of reported items
2. Test thoroughly before removing code
3. Update documentation if needed
4. Consider refactoring instead of deletion
"@

    Set-Content -Path $reportFile -Value $report
    Write-Log "📄 Comprehensive report saved to $reportFile" "Green"

    # 4. Summary output
    Write-Log "" 
    Write-Log "=== DEAD CODE ANALYSIS SUMMARY ===" "Cyan"
    Write-Log "📁 Reports directory: $OUTPUT_DIR" "White"
    Write-Log "🐍 Python analysis: $(if (Test-Path $vultureOutput) { "vulture.txt" } else { "failed" })" "White"
    Write-Log "📘 TypeScript analysis: $(if (Test-Path $tsPruneOutput) { "ts-prune.txt" } else { "failed" })" "White"
    Write-Log "📄 Summary report: dead_code_report.txt" "White"
    Write-Log "" 

}
finally {
    Pop-Location
}

Write-Log "Dead code analysis completed. Reports: $OUTPUT_DIR" "Green"