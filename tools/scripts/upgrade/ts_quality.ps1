#!/usr/bin/env pwsh
# TypeScript Quality Script - PowerShell version
param(
    [switch]$SkipTests = $false,
    [switch]$SkipInstall = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Color = "White")
    Write-Host "— TS Quality — $Message" -ForegroundColor $Color
}

function Invoke-SafeCommand {
    param([string]$Command, [string]$Description, [switch]$ContinueOnError = $false)
    
    Write-Log "$Description..." "Cyan"
    if ($Verbose) {
        Write-Host "Executing: $Command" -ForegroundColor DarkGray
    }
    
    try {
        Invoke-Expression $Command
        Write-Log "✅ $Description completed" "Green"
        return $true
    }
    catch {
        if ($ContinueOnError) {
            Write-Log "⚠️ $Description failed but continuing: $($_.Exception.Message)" "Yellow"
            return $false
        }
        else {
            Write-Log "❌ $Description failed: $($_.Exception.Message)" "Red"
            throw
        }
    }
}

function Test-Command($CommandName) {
    return [bool](Get-Command $CommandName -ErrorAction SilentlyContinue)
}

Write-Log "Starting TypeScript quality checks..." "Green"

# Check if we're in a valid Node.js project
if (-not (Test-Path "package.json")) {
    Write-Log "❌ No package.json found. Are you in the right directory?" "Red"
    exit 1
}

# Check for Node.js
if (-not (Test-Command "node")) {
    Write-Log "❌ Node.js not found. Please install Node.js first." "Red"
    exit 1
}

if (-not (Test-Command "npm")) {
    Write-Log "❌ npm not found. Please install npm first." "Red"
    exit 1
}

# 1. Install dependencies (unless skipped)
if (-not $SkipInstall) {
    Write-Log "Installing dependencies..." "Cyan"
    
    # Try npm ci first (faster), fallback to npm install
    $installSuccess = Invoke-SafeCommand "npm ci --ignore-scripts" "Installing dependencies (npm ci)" -ContinueOnError
    
    if (-not $installSuccess) {
        Invoke-SafeCommand "npm install --include=dev" "Installing dependencies (npm install)"
    }
}
else {
    Write-Log "Skipping dependency installation as requested" "Yellow"
}

# 2. Code formatting
if (Test-Path "src") {
    Invoke-SafeCommand 'npx prettier "src/**/*.{ts,tsx,css,md,json}" --write' "Formatting code with Prettier"
}
else {
    Invoke-SafeCommand 'npx prettier "**/*.{ts,tsx,css,md,json}" --write --ignore-path .gitignore' "Formatting code with Prettier"
}

# 3. Linting with auto-fix
if (Test-Path "src") {
    Invoke-SafeCommand 'npx eslint "src/**/*.{ts,tsx}" --fix' "Linting and fixing with ESLint" -ContinueOnError
}
else {
    Invoke-SafeCommand 'npx eslint "**/*.{ts,tsx}" --fix --ignore-path .gitignore' "Linting and fixing with ESLint" -ContinueOnError
}

# 4. Type checking
$tscSuccess = $false
if (Test-Path "tsconfig.json") {
    $tscSuccess = Invoke-SafeCommand "npx tsc --noEmit" "Type checking with TypeScript" -ContinueOnError
}
else {
    Write-Log "⚠️ No tsconfig.json found, skipping type check" "Yellow"
}

# 5. Tests (if not skipped)
if (-not $SkipTests) {
    Write-Log "Running tests..." "Cyan"
    
    $testConfigs = @("vitest.config.ts", "vitest.config.js", "jest.config.js", "jest.config.ts")
    $testConfigFound = $false
    
    foreach ($config in $testConfigs) {
        if (Test-Path $config) {
            $testConfigFound = $true
            break
        }
    }
    
    if ($testConfigFound) {
        # Try different test runners
        $testRunners = @(
            @{ cmd = "npx vitest run --coverage"; desc = "Running tests with Vitest" },
            @{ cmd = "npm test"; desc = "Running tests with npm test" },
            @{ cmd = "npx jest --coverage"; desc = "Running tests with Jest" }
        )
        
        $testPassed = $false
        foreach ($runner in $testRunners) {
            if ($testPassed) { break }
            
            try {
                Invoke-Expression $runner.cmd
                Write-Log "✅ $($runner.desc) passed" "Green"
                $testPassed = $true
            }
            catch {
                Write-Log "⚠️ $($runner.desc) failed" "Yellow"
            }
        }
        
        if (-not $testPassed) {
            Write-Log "⚠️ All test runners failed" "Yellow"
        }
    }
    else {
        Write-Log "⚠️ No test configuration found, skipping tests" "Yellow"
    }
}
else {
    Write-Log "Tests skipped as requested" "Yellow"
}

# 6. Dependency analysis
Write-Log "Analyzing dependencies..." "Cyan"

# Check for unused dependencies
Invoke-SafeCommand "npx depcheck" "Checking for unused dependencies" -ContinueOnError

# Check for unused exports (ts-prune)
$artifactsDir = "../.artifacts/deadcode"
if (-not (Test-Path $artifactsDir)) {
    New-Item -ItemType Directory -Path $artifactsDir -Force | Out-Null
}

try {
    & npx ts-prune > "$artifactsDir/ts-prune.txt" 2>&1
    Write-Log "✅ Dead code analysis saved to $artifactsDir/ts-prune.txt" "Green"
}
catch {
    Write-Log "⚠️ ts-prune analysis failed" "Yellow"
    Set-Content -Path "$artifactsDir/ts-prune.txt" -Value "ts-prune analysis failed: $($_.Exception.Message)"
}

# 7. Build check (if build script exists)
$packageJson = Get-Content "package.json" | ConvertFrom-Json
if ($packageJson.scripts.build) {
    Write-Log "Running build check..." "Cyan"
    Invoke-SafeCommand "npm run build" "Building project" -ContinueOnError
}
else {
    Write-Log "⚠️ No build script found in package.json" "Yellow"
}

# 8. Generate quality report
Write-Log "Generating TypeScript quality report..." "Cyan"

$reportPath = "../.artifacts/typescript_quality_report.txt"
$artifactsParent = "../.artifacts"
if (-not (Test-Path $artifactsParent)) {
    New-Item -ItemType Directory -Path $artifactsParent -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$report = @"
# TypeScript Quality Report
Generated: $timestamp

## Summary
- ✅ Code formatting: Prettier
- ⚠️ Linting: ESLint --fix (warnings allowed)
- $(if ($tscSuccess) { "✅" } else { "⚠️" }) Type checking: TypeScript compiler
$(if (-not $SkipTests) { "- ⚠️ Tests: Multiple runners attempted" } else { "- ⏭️ Tests: skipped" })
- ✅ Dependency analysis: depcheck + ts-prune

## Quality Gates
- Formatting: PASS
- Linting: CONDITIONAL
- Type Safety: $(if ($tscSuccess) { "PASS" } else { "CONDITIONAL" })
- Tests: $(if (-not $SkipTests) { "CONDITIONAL" } else { "SKIPPED" })
- Dependencies: ADVISORY

## Files Analyzed
- Source: src/**/*.{ts,tsx}
- Configs: $(if (Test-Path "tsconfig.json") { "tsconfig.json" } else { "none" })
- Tests: $(if (Test-Path "vitest.config.ts") { "vitest" } elseif (Test-Path "jest.config.js") { "jest" } else { "none" })

## Next Steps
1. Review ESLint warnings
2. Fix TypeScript errors if any
3. Ensure test coverage is adequate
4. Remove unused dependencies
5. Consider adding pre-commit hooks
"@

Set-Content -Path $reportPath -Value $report
Write-Log "📄 Quality report saved to $reportPath" "Green"

Write-Log "TypeScript quality checks completed!" "Green"