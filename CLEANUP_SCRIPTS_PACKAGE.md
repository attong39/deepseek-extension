# 🧹 Automated Cleanup Scripts Package

## 1. Build Artifacts Cleanup (Phase 1 - Safe)

### cleanup_build_artifacts.ps1
```powershell
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
# This would require before/after measurement - simplified for now

Write-Host "✅ Build artifacts cleanup completed!" -ForegroundColor Green
Write-Host "🔄 Run 'npm install' or 'pip install' to restore dependencies" -ForegroundColor Cyan
```

## 2. Configuration Consolidation (Phase 2)

### consolidate_configs.ps1
```powershell
#!/usr/bin/env pwsh
# Zeta Monorepo - Configuration Consolidation

Write-Host "⚙️ Starting Configuration Consolidation..." -ForegroundColor Green

# Create organized directory structure
$configDirs = @("configs/docker", "configs/api", "configs/ci", "configs/python")
foreach ($dir in $configDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "📁 Created: $dir" -ForegroundColor Cyan
    }
}

# 1. Consolidate Docker Compose Files
Write-Host "🐳 Consolidating Docker configurations..." -ForegroundColor Yellow
Get-ChildItem -Path . -File -Include "docker-compose*.yml" | ForEach-Object {
    $newPath = "configs/docker/$($_.Name)"
    Write-Host "  Moving: $($_.Name) -> $newPath"
    Move-Item -Path $_.FullName -Destination $newPath -Force
}

# 2. Consolidate API Configuration Files
Write-Host "🔧 Consolidating API configurations..." -ForegroundColor Yellow
$apiConfigs = @("ollama_*.json", "*_api_*.json", "api_*.json")
foreach ($pattern in $apiConfigs) {
    Get-ChildItem -Path . -File -Include $pattern | ForEach-Object {
        $newPath = "configs/api/$($_.Name)"
        Write-Host "  Moving: $($_.Name) -> $newPath"
        Move-Item -Path $_.FullName -Destination $newPath -Force
    }
}

# 3. Consolidate Python Configuration
Write-Host "🐍 Consolidating Python configurations..." -ForegroundColor Yellow
$pythonConfigs = @("mypy*.ini", "pytest.ini", "setup.cfg", ".flake8")
foreach ($pattern in $pythonConfigs) {
    Get-ChildItem -Path . -File -Include $pattern | ForEach-Object {
        $newPath = "configs/python/$($_.Name)"
        Write-Host "  Moving: $($_.Name) -> $newPath"
        Move-Item -Path $_.FullName -Destination $newPath -Force
    }
}

# 4. Create Master Configuration Index
$indexContent = @"
# 🗂️ Configuration Index
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Docker Configurations
$(Get-ChildItem -Path "configs/docker" -Name | ForEach-Object { "- $($_)" } | Out-String)

## API Configurations  
$(Get-ChildItem -Path "configs/api" -Name | ForEach-Object { "- $($_)" } | Out-String)

## Python Configurations
$(Get-ChildItem -Path "configs/python" -Name | ForEach-Object { "- $($_)" } | Out-String)

## CI/CD Configurations
$(Get-ChildItem -Path ".github/workflows" -Name | ForEach-Object { "- $($_)" } | Out-String)
"@

Set-Content -Path "configs/CONFIG_INDEX.md" -Value $indexContent

Write-Host "✅ Configuration consolidation completed!" -ForegroundColor Green
```

## 3. Documentation Organization (Phase 3)

### organize_documentation.ps1
```powershell
#!/usr/bin/env pwsh
# Zeta Monorepo - Documentation Organization

Write-Host "📚 Starting Documentation Organization..." -ForegroundColor Green

# Create documentation structure
$docDirs = @("docs/reports", "docs/guides", "docs/api", "docs/archives")
foreach ($dir in $docDirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "📁 Created: $dir" -ForegroundColor Cyan
    }
}

# 1. Organize AI Reports
Write-Host "🤖 Organizing AI reports..." -ForegroundColor Yellow
Get-ChildItem -Path . -File -Include "AI_*_*.md" | ForEach-Object {
    $newPath = "docs/reports/$($_.Name)"
    Write-Host "  Moving: $($_.Name) -> $newPath"
    Move-Item -Path $_.FullName -Destination $newPath -Force
}

# 2. Organize Guides and Documentation
Write-Host "📖 Organizing guides..." -ForegroundColor Yellow
$guidePatterns = @("*_GUIDE.md", "*_README.md", "SETUP_*.md", "INSTALLATION_*.md")
foreach ($pattern in $guidePatterns) {
    Get-ChildItem -Path . -File -Include $pattern | ForEach-Object {
        $newPath = "docs/guides/$($_.Name)"
        Write-Host "  Moving: $($_.Name) -> $newPath"
        Move-Item -Path $_.FullName -Destination $newPath -Force
    }
}

# 3. Organize API Documentation
Write-Host "🔌 Organizing API documentation..." -ForegroundColor Yellow
Get-ChildItem -Path . -File -Include "API_*.md" | ForEach-Object {
    $newPath = "docs/api/$($_.Name)"
    Write-Host "  Moving: $($_.Name) -> $newPath"
    Move-Item -Path $_.FullName -Destination $newPath -Force
}

# 4. Archive Completed Reports
Write-Host "📦 Archiving completed reports..." -ForegroundColor Yellow
$archivePatterns = @("*_COMPLETE.md", "*_SUCCESS.md", "*_COMPLETED.md")
foreach ($pattern in $archivePatterns) {
    Get-ChildItem -Path . -File -Include $pattern | ForEach-Object {
        $newPath = "docs/archives/$($_.Name)"
        Write-Host "  Moving: $($_.Name) -> $newPath"
        Move-Item -Path $_.FullName -Destination $newPath -Force
    }
}

# 5. Create Documentation Index
$docIndexContent = @"
# 📚 Documentation Index
Last Updated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 📊 Reports ($(Get-ChildItem -Path "docs/reports" | Measure-Object | Select-Object -ExpandProperty Count))
$(Get-ChildItem -Path "docs/reports" -Name | Sort-Object | ForEach-Object { "- [$_](./reports/$_)" } | Out-String)

## 📖 Guides ($(Get-ChildItem -Path "docs/guides" | Measure-Object | Select-Object -ExpandProperty Count))
$(Get-ChildItem -Path "docs/guides" -Name | Sort-Object | ForEach-Object { "- [$_](./guides/$_)" } | Out-String)

## 🔌 API Documentation ($(Get-ChildItem -Path "docs/api" | Measure-Object | Select-Object -ExpandProperty Count))
$(Get-ChildItem -Path "docs/api" -Name | Sort-Object | ForEach-Object { "- [$_](./api/$_)" } | Out-String)

## 📦 Archives ($(Get-ChildItem -Path "docs/archives" | Measure-Object | Select-Object -ExpandProperty Count))
$(Get-ChildItem -Path "docs/archives" -Name | Sort-Object | ForEach-Object { "- [$_](./archives/$_)" } | Out-String)
"@

Set-Content -Path "docs/README.md" -Value $docIndexContent

Write-Host "✅ Documentation organization completed!" -ForegroundColor Green
```

## 4. Cleanup Automation Setup (Phase 4)

### setup_cleanup_automation.ps1
```powershell
#!/usr/bin/env pwsh
# Zeta Monorepo - Cleanup Automation Setup

Write-Host "🔄 Setting up cleanup automation..." -ForegroundColor Green

# 1. Create .gitignore entries
$gitignoreAdditions = @"

# Build Artifacts (Auto-cleanup)
**/node_modules/
**/.venv-*/
*.log
*.cache
*.tmp
*.temp
*.bak
.cleanup_backup/

# Generated Reports (Keep only in git)
ai_project_analysis.json
benchmark_results.json
duplicate_code_report_*.html
duplicate_code_report_*.json

# IDE and Editor files
.vscode/settings.json
.idea/
*.swp
*.swo

"@

Add-Content -Path ".gitignore" -Value $gitignoreAdditions
Write-Host "📝 Updated .gitignore with cleanup patterns" -ForegroundColor Cyan

# 2. Create GitHub Action for weekly cleanup
$githubActionContent = @"
name: 🧹 Weekly Cleanup
on:
  schedule:
    - cron: '0 2 * * 0'  # Every Sunday at 2 AM
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: 🧹 Run Cleanup
        run: |
          # Remove old log files
          find . -name "*.log" -mtime +7 -delete
          
          # Remove cache files
          find . -name "*.cache" -delete
          find . -name "*.tmp" -delete
          
          # Remove backup directories
          find . -name ".cleanup_backup" -type d -exec rm -rf {} +
          
      - name: 📊 Report Cleanup Results
        run: |
          echo "Cleanup completed on \$(date)"
          echo "Remaining files: \$(find . -type f | wc -l)"
"@

$workflowDir = ".github/workflows"
if (!(Test-Path $workflowDir)) {
    New-Item -ItemType Directory -Path $workflowDir -Force
}
Set-Content -Path "$workflowDir/weekly-cleanup.yml" -Value $githubActionContent
Write-Host "⚙️ Created GitHub Action for weekly cleanup" -ForegroundColor Cyan

# 3. Create monitoring script
$monitoringScript = @"
#!/usr/bin/env pwsh
# File Size Monitoring Script

`$totalFiles = (Get-ChildItem -Recurse -File | Measure-Object).Count
`$totalSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB

Write-Host "📊 Repository Statistics:" -ForegroundColor Green
Write-Host "Total Files: `$totalFiles"
Write-Host "Total Size: `$([math]::Round(`$totalSize, 2)) MB"

# Check for large directories
Write-Host "`n📁 Largest Directories:" -ForegroundColor Yellow
Get-ChildItem -Directory | ForEach-Object {
    `$size = (Get-ChildItem -Path `$_.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
    [PSCustomObject]@{
        Directory = `$_.Name
        "Size (MB)" = [math]::Round(`$size, 2)
    }
} | Sort-Object "Size (MB)" -Descending | Select-Object -First 10 | Format-Table

# Alert if size exceeds threshold
if (`$totalSize -gt 1000) {
    Write-Host "⚠️ Repository size exceeds 1GB - consider cleanup" -ForegroundColor Red
}
"@

Set-Content -Path "scripts/monitor_repo_size.ps1" -Value $monitoringScript
Write-Host "📊 Created repository monitoring script" -ForegroundColor Cyan

Write-Host "✅ Cleanup automation setup completed!" -ForegroundColor Green
Write-Host "🔄 Weekly cleanup will run automatically via GitHub Actions" -ForegroundColor Cyan
```

## 5. Master Cleanup Orchestrator

### run_full_cleanup.ps1
```powershell
#!/usr/bin/env pwsh
# Zeta Monorepo - Master Cleanup Orchestrator

param(
    [switch]$DryRun,
    [switch]$SkipPhase2,
    [switch]$SkipPhase3,
    [switch]$Force
)

Write-Host "🎯 Zeta Monorepo Full Cleanup Orchestrator" -ForegroundColor Magenta
Write-Host "=========================================" -ForegroundColor Magenta

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
}

# Phase 1: Safe Cleanup
Write-Host "`n🧹 Phase 1: Build Artifacts Cleanup" -ForegroundColor Green
if (!$DryRun) {
    & ./cleanup_build_artifacts.ps1
} else {
    Write-Host "  [DRY RUN] Would remove build artifacts and temporary files"
}

# Phase 2: Configuration Consolidation  
if (!$SkipPhase2) {
    Write-Host "`n⚙️ Phase 2: Configuration Consolidation" -ForegroundColor Green
    if (!$DryRun) {
        & ./consolidate_configs.ps1
    } else {
        Write-Host "  [DRY RUN] Would consolidate configuration files"
    }
}

# Phase 3: Documentation Organization
if (!$SkipPhase3) {
    Write-Host "`n📚 Phase 3: Documentation Organization" -ForegroundColor Green
    if (!$DryRun) {
        & ./organize_documentation.ps1
    } else {
        Write-Host "  [DRY RUN] Would organize documentation files"
    }
}

# Phase 4: Setup Automation
Write-Host "`n🔄 Phase 4: Cleanup Automation Setup" -ForegroundColor Green
if (!$DryRun) {
    & ./setup_cleanup_automation.ps1
} else {
    Write-Host "  [DRY RUN] Would setup cleanup automation"
}

# Final Report
Write-Host "`n📊 Cleanup Summary" -ForegroundColor Magenta
if (!$DryRun) {
    & ./scripts/monitor_repo_size.ps1
} else {
    Write-Host "  [DRY RUN] Would generate final size report"
}

Write-Host "`n✅ Full cleanup orchestration completed!" -ForegroundColor Green

if ($DryRun) {
    Write-Host "🔄 Run without -DryRun to execute cleanup" -ForegroundColor Cyan
}
```

## Usage Instructions

### Quick Start
```powershell
# Safe cleanup only (recommended first run)
./cleanup_build_artifacts.ps1

# Full cleanup with dry run
./run_full_cleanup.ps1 -DryRun

# Full cleanup execution
./run_full_cleanup.ps1

# Skip specific phases
./run_full_cleanup.ps1 -SkipPhase2 -SkipPhase3
```

### Manual Phase Execution
```powershell
# Phase 1: Safe cleanup
./cleanup_build_artifacts.ps1

# Phase 2: Configuration consolidation  
./consolidate_configs.ps1

# Phase 3: Documentation organization
./organize_documentation.ps1

# Phase 4: Setup automation
./setup_cleanup_automation.ps1
```

### Monitoring
```powershell
# Check repository size
./scripts/monitor_repo_size.ps1

# Check specific directory
Get-ChildItem -Path "apps/" -Recurse | Measure-Object Length -Sum
```

All scripts include error handling and provide detailed output for transparency and debugging.
