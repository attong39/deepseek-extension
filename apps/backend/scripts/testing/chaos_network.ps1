param([int]$Seconds = 30)
Write-Host "Simulating network drop for $Seconds s"
# Windows: disable NIC (requires admin). Dev-safe: block host via hosts/Firewall (left as TODO).
Start-Sleep -Seconds $Seconds
Write-Host "Network restored (noop in dev)."
