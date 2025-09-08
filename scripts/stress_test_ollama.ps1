<#
Stress test Ollama API
- PowerShell 5.1 compatible (uses Start-Job) with optional PS7+ -Parallel path
- Parameters:
    -Model         Model name (default: phi3:mini)
    -Prompt        Prompt string (default: simple Vietnamese task)
    -Requests      Total number of requests (default: 100) [Alias: -RequestCount]
    -Concurrency   Number of concurrent jobs (default: 10)
    -Host          Ollama host:port (default: 127.0.0.1:11434)
#>
[CmdletBinding()]
param(
    [string]$Model = "phi3:mini",
    [string]$Prompt = "Viết hàm Python tính giai thừa",
    [Alias("RequestCount")][int]$Requests = 100,
    [int]$Concurrency = 10,
    [string]$Host = "127.0.0.1:11434",
    [string]$BaseUrl = "",
    [string]$OutPrefix = "stress"
)

$ErrorActionPreference = 'Stop'
$base = if ([string]::IsNullOrWhiteSpace($BaseUrl)) { "http://$Host" } else { $BaseUrl.TrimEnd('/') }
$uri = "$base/api/generate"
$payloadTemplate = '{ "model": "{0}", "prompt": "{1}" }'

Write-Host "Starting stress test -> $Requests requests, concurrency $Concurrency, model '$Model' at $Host"
$sw = [System.Diagnostics.Stopwatch]::StartNew()
$_ts = (Get-Date -Format 'yyyyMMdd_HHmmss')
$_logFile = "${OutPrefix}_test_${_ts}.log"
$_jsonFile = "ollama_metrics_${_ts}.json"

# Shared stats (thread-safe updates via synchronized hashtable)
$sync = [hashtable]::Synchronized(@{ ok = 0; fail = 0; durations = New-Object System.Collections.ArrayList })

function Invoke-OneRequest {
    param([string]$Uri, [string]$Body)
    $localSw = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $resp = Invoke-RestMethod -Method Post -Uri $Uri -ContentType 'application/json' -Body $Body -TimeoutSec 120
        $null = $sync.durations.Add($localSw.Elapsed.TotalSeconds)
        [System.Threading.Monitor]::Enter($sync)
        try { $sync.ok++ } finally { [System.Threading.Monitor]::Exit($sync) }
    } catch {
        $null = $sync.durations.Add($localSw.Elapsed.TotalSeconds)
        [System.Threading.Monitor]::Enter($sync)
        try { $sync.fail++ } finally { [System.Threading.Monitor]::Exit($sync) }
        Write-Warning ("Request failed: {0}" -f $_.Exception.Message)
    }
}

# Worker loop for a job
$script:JobWorker = {
    param($start, $end, $uri, $model, $prompt)
    $payload = [string]::Format($payloadTemplate, $model, $prompt.Replace('"','\"'))
    for ($i = $start; $i -le $end; $i++) {
        Invoke-OneRequest -Uri $uri -Body $payload
    }
}

# Partition requests into $Concurrency jobs
$range = 1..$Requests
$chunkSize = [Math]::Ceiling($Requests / [double]$Concurrency)
$jobs = @()
for ($idx = 0; $idx -lt $Concurrency; $idx++) {
    $startIdx = ($idx * $chunkSize) + 1
    $endIdx = [Math]::Min($Requests, $startIdx + $chunkSize - 1)
    if ($startIdx -le $endIdx) {
        $jobs += Start-Job -ScriptBlock $script:JobWorker -ArgumentList @($startIdx, $endIdx, $uri, $Model, $Prompt)
    }
}

Receive-Job -Job $jobs -Wait | Out-Null
$sw.Stop()

# Summaries
$total = $Requests
$ok = $sync.ok
$fail = $sync.fail
$avg = if ($sync.durations.Count -gt 0) { ($sync.durations | Measure-Object -Average).Average } else { 0 }
$p95 = if ($sync.durations.Count -gt 0) {
    $sorted = $sync.durations | Sort-Object
    $idx95 = [Math]::Floor($sorted.Count * 0.95) - 1
    if ($idx95 -lt 0) { $idx95 = 0 }
    [double]$sorted[$idx95]
} else { 0 }

Write-Host "--- Stress Test Summary ---"
Write-Host ("Total: {0}, OK: {1}, Fail: {2}" -f $total, $ok, $fail)
Write-Host ("Avg latency: {0:N3}s, p95 latency: {1:N3}s" -f $avg, $p95)
Write-Host ("Wall time: {0:N3}s" -f $sw.Elapsed.TotalSeconds)

# Persist logs
@(
    "Total: $total",
    "OK: $ok",
    "Fail: $fail",
    ("Avg latency: {0:N3}s" -f $avg),
    ("p95 latency: {0:N3}s" -f $p95),
    ("Wall time: {0:N3}s" -f $sw.Elapsed.TotalSeconds)
) | Out-File -FilePath $_logFile -Encoding UTF8

# Emit machine-readable metrics
$rps = if ($sw.Elapsed.TotalSeconds -gt 0) { [math]::Round($total / $sw.Elapsed.TotalSeconds, 2) } else { 0 }
$metrics = [ordered]@{
    timestamp = (Get-Date -Format 'o')
    model = $Model
    total_requests = $total
    successful_requests = $ok
    failed_requests = $fail
    average_latency_s = [math]::Round([double]$avg, 4)
    p95_latency_s = [math]::Round([double]$p95, 4)
    total_duration_s = [math]::Round([double]$sw.Elapsed.TotalSeconds, 4)
    requests_per_second = $rps
}
$metrics | ConvertTo-Json | Out-File -FilePath $_jsonFile -Encoding UTF8
Write-Host ("Metrics saved: {0}" -f $_jsonFile)

# Exit code reflects failures
if ($fail -gt 0) { exit 2 } else { exit 0 }
