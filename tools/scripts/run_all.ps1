#!/usr/bin/env powershell
param(
    [string]$ApiUrl = "http://127.0.0.1:8099",
    [switch]$LLM = $false,
    [string]$Actions = "link copilot, guard, upgrade, fix imports, tạo __init__.__all__, ts, openapi, quality + perf, dedupe, dead code"
)

Write-Host "🚀 ZETA Auto-Dev: Running All Components..." -ForegroundColor Cyan
Write-Host "📋 Actions: $Actions" -ForegroundColor Gray
Write-Host "🌐 API URL: $ApiUrl" -ForegroundColor Gray
Write-Host "🧠 LLM Mode: $(if ($LLM) { 'ON' } else { 'OFF' })" -ForegroundColor Gray

$cmdArgs = @("uv", "run", "python", "ai_runner.py", "--once", $Actions, "--apply", "--api-url", $ApiUrl)
if ($LLM) { 
    $cmdArgs += "--llm" 
    Write-Host "🔮 LLM synthesis enabled" -ForegroundColor Magenta
}

$startTime = Get-Date
try {
    Write-Host "Running command: $($cmdArgs -join ' ')" -ForegroundColor Yellow
    $process = Start-Process -FilePath $cmdArgs[0] -ArgumentList $cmdArgs[1..($cmdArgs.Length - 1)] -NoNewWindow -Wait -PassThru
    $duration = (Get-Date) - $startTime
    
    if ($process.ExitCode -eq 0) {
        Write-Host "✅ Auto-Dev completed successfully in $($duration.TotalSeconds.ToString('F1'))s" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Auto-Dev failed (exit code: $($process.ExitCode))" -ForegroundColor Red
        exit $process.ExitCode
    }
}
catch {
    Write-Host "❌ Error running Auto-Dev: $_" -ForegroundColor Red
    exit 1
}
