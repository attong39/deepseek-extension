#!/usr/bin/env pwsh
<#!
.SYNOPSIS
  Daily AI optimization script for Windows (PowerShell).
.DESCRIPTION
  Pulls latest changes, runs AI optimization with auto-commit, and pushes back.
#>

param(
      [string]$Branch = "main",
      [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

Write-Host "[AI] Switching to branch $Branch" -ForegroundColor Cyan
& git fetch origin $Branch
& git checkout $Branch
& git pull --ff-only origin $Branch

Write-Host "[AI] Running optimization with auto-commit" -ForegroundColor Cyan
& npm run ai:optimize:commit

if (-not $NoPush) {
      Write-Host "[AI] Pushing changes to origin/$Branch" -ForegroundColor Cyan
      & git push origin $Branch
}
else {
      Write-Host "[AI] Skipping push (NoPush specified)" -ForegroundColor Yellow
}
