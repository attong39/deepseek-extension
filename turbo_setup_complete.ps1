# ✅ Turbo Setup Complete!
Write-Host "✅ TURBO SETUP HOÀN TẤT!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

Write-Host "`n🎯 BƯỚC TIẾP THEO:" -ForegroundColor Yellow
Write-Host "1. Restart VS Code: Ctrl+Shift+P → 'Developer: Reload Window'" -ForegroundColor White
Write-Host "2. Mở Continue: Ctrl+L" -ForegroundColor White
Write-Host "3. Chọn model: '🚀 Turbo gpt-oss:120b (Cloud)'" -ForegroundColor White
Write-Host "4. Test: Gõ 'Write a hello function'" -ForegroundColor White

Write-Host "`n🚀 TẠI SAO SẼ NHANH HƠN:" -ForegroundColor Cyan
Write-Host "• Trước: DeepSeek local model (~10-15 giây)" -ForegroundColor Red
Write-Host "• Bây giờ: Turbo cloud API (~2-3 giây)" -ForegroundColor Green
Write-Host "• Autocomplete: Turbo instant suggestions" -ForegroundColor Green

Write-Host "`n📊 HIỆU SUẤT HIỆN TẠI:" -ForegroundColor Magenta
$start = Get-Date
try {
    $headers = @{ "Authorization" = "Bearer $env:OLLAMA_TURBO_API_KEY"; "Content-Type" = "application/json" }
    $body = '{"model": "gpt-oss:120b", "prompt": "OK", "stream": false}'
    $response = Invoke-RestMethod -Uri "https://ollama.com/api/generate" -Method POST -Headers $headers -Body $body
    $end = Get-Date
    $duration = ($end - $start).TotalSeconds
    Write-Host "✅ Turbo API: $duration giây" -ForegroundColor Green
    Write-Host "⚡ Tốc độ: $(if ($duration -lt 3) { 'RẤT NHANH' } elseif ($duration -lt 5) { 'NHANH' } else { 'BÌ̀NH THƯỜNG' })" -ForegroundColor Yellow
} catch {
    Write-Host "❌ Lỗi API: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 HOÀN TẤT! Enjoy coding với Turbo speed!" -ForegroundColor Green