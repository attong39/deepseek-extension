# Advanced Duplicate Code Detector - PowerShell Version
# Phát hiện file có nội dung code trùng lặp thực sự

param(
    [string]$OutputFormat = "console",  # console, html, json
    [int]$MinFileSize = 100,            # Kích thước file tối thiểu (bytes)
    [string[]]$Extensions = @("*.py", "*.js", "*.ts", "*.tsx", "*.jsx", "*.cs", "*.java")
)

Write-Host "🔍 Advanced Duplicate Code Detector" -ForegroundColor Green
Write-Host "=" * 50

# Tạo hashtable để lưu hash của files
$fileHashes = @{}
$duplicateGroups = @()
$totalFiles = 0
$totalSize = 0

Write-Host "📁 Quét files theo extensions: $($Extensions -join ', ')" -ForegroundColor Yellow

foreach ($extension in $Extensions) {
    $files = Get-ChildItem -Recurse -Filter $extension | Where-Object { 
        $_.Length -gt $MinFileSize -and 
        $_.FullName -notlike "*node_modules*" -and 
        $_.FullName -notlike "*\.venv*" -and 
        $_.FullName -notlike "*\.git*" -and
        $_.FullName -notlike "*\bin\*" -and
        $_.FullName -notlike "*\obj\*"
    }
    
    foreach ($file in $files) {
        try {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
            
            # Normalize content (loại bỏ whitespace, comments để so sánh chính xác hơn)
            $normalizedContent = $content -replace '\s+', ' ' -replace '#.*$', '' -replace '//.*$', ''
            
            # Tính hash của nội dung đã normalize
            $hash = [System.Security.Cryptography.MD5]::Create().ComputeHash([System.Text.Encoding]::UTF8.GetBytes($normalizedContent))
            $hashString = [System.BitConverter]::ToString($hash) -replace '-', ''
            
            if ($fileHashes.ContainsKey($hashString)) {
                $fileHashes[$hashString] += $file
            } else {
                $fileHashes[$hashString] = @($file)
            }
            
            $totalFiles++
            $totalSize += $file.Length
            
            if ($totalFiles % 50 -eq 0) {
                Write-Host "   Đã quét: $totalFiles files..." -ForegroundColor Gray
            }
        }
        catch {
            Write-Host "⚠️ Lỗi đọc file: $($file.Name)" -ForegroundColor Red
        }
    }
}

# Tìm các nhóm duplicate
$duplicateGroups = $fileHashes.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 }

Write-Host "`n📊 Kết quả quét:" -ForegroundColor Cyan
Write-Host "   - Tổng files đã quét: $totalFiles" -ForegroundColor White
Write-Host "   - Tổng dung lượng: $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor White
Write-Host "   - Nhóm duplicate tìm thấy: $($duplicateGroups.Count)" -ForegroundColor White

if ($duplicateGroups.Count -eq 0) {
    Write-Host "`n✅ Không tìm thấy file duplicate code!" -ForegroundColor Green
    exit
}

# Phân tích chi tiết duplicates
$totalDuplicateFiles = 0
$totalWastedSpace = 0
$duplicateAnalysis = @()

Write-Host "`n🔴 Chi tiết file duplicate code:" -ForegroundColor Red

$groupIndex = 1
foreach ($group in $duplicateGroups) {
    $files = $group.Value
    $fileSize = $files[0].Length
    $wastedSpace = $fileSize * ($files.Count - 1)
    $totalDuplicateFiles += ($files.Count - 1)
    $totalWastedSpace += $wastedSpace
    
    $analysis = [PSCustomObject]@{
        GroupId = $groupIndex
        FileCount = $files.Count
        FileSize = $fileSize
        WastedSpace = $wastedSpace
        Files = $files | ForEach-Object { $_.FullName }
        Extension = $files[0].Extension
    }
    $duplicateAnalysis += $analysis
    
    if ($groupIndex -le 10) {  # Hiển thị top 10 nhóm
        Write-Host "`n   📦 Nhóm $groupIndex ($($files.Count) files - $([math]::Round($fileSize/1KB, 1))KB mỗi file):" -ForegroundColor Yellow
        foreach ($file in $files) {
            Write-Host "     - $($file.FullName.Replace((Get-Location), '.'))" -ForegroundColor White
        }
        Write-Host "     💾 Waste: $([math]::Round($wastedSpace/1KB, 1))KB" -ForegroundColor Red
    }
    
    $groupIndex++
}

if ($duplicateGroups.Count -gt 10) {
    Write-Host "`n   ... và $($duplicateGroups.Count - 10) nhóm khác" -ForegroundColor Gray
}

# Thống kê theo extension
Write-Host "`n📈 Thống kê theo loại file:" -ForegroundColor Cyan
$extensionStats = $duplicateAnalysis | Group-Object Extension | Sort-Object Count -Descending
foreach ($stat in $extensionStats) {
    $totalFiles = ($stat.Group | Measure-Object FileCount -Sum).Sum
    $totalWaste = ($stat.Group | Measure-Object WastedSpace -Sum).Sum
    Write-Host "   $($stat.Name): $($stat.Count) nhóm, $totalFiles files, $([math]::Round($totalWaste/1KB, 1))KB waste" -ForegroundColor White
}

# Tổng kết
Write-Host "`n🎯 Tổng kết:" -ForegroundColor Green
Write-Host "   - Files duplicate: $totalDuplicateFiles" -ForegroundColor White
Write-Host "   - Dung lượng lãng phí: $([math]::Round($totalWastedSpace / 1MB, 2)) MB" -ForegroundColor White
Write-Host "   - Tiết kiệm được: $([math]::Round(($totalWastedSpace / $totalSize) * 100, 1))% tổng dung lượng" -ForegroundColor White

# Lưu báo cáo chi tiết
$reportFile = "duplicate_code_report_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Tạo HTML report
if ($OutputFormat -eq "html" -or $OutputFormat -eq "all") {
    $htmlFile = "$reportFile.html"
    $html = @"
<!DOCTYPE html>
<html>
<head>
    <title>Duplicate Code Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 10px; border-radius: 5px; }
        .group { margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        .group-header { background: #e7f3ff; padding: 10px; font-weight: bold; }
        .file-list { padding: 10px; }
        .file { margin: 2px 0; color: #666; }
        .stats { background: #fff8dc; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Duplicate Code Analysis Report</h1>
        <p>Generated: $(Get-Date)</p>
        <div class="stats">
            <h3>📊 Tổng quan:</h3>
            <ul>
                <li>Files đã quét: $totalFiles</li>
                <li>Nhóm duplicate: $($duplicateGroups.Count)</li>
                <li>Files duplicate: $totalDuplicateFiles</li>
                <li>Dung lượng lãng phí: $([math]::Round($totalWastedSpace / 1MB, 2)) MB</li>
            </ul>
        </div>
    </div>
"@

    $groupIndex = 1
    foreach ($analysis in $duplicateAnalysis) {
        $html += @"
    <div class="group">
        <div class="group-header">
            📦 Nhóm $groupIndex - $($analysis.FileCount) files ($($analysis.Extension)) - Waste: $([math]::Round($analysis.WastedSpace/1KB, 1))KB
        </div>
        <div class="file-list">
"@
        foreach ($file in $analysis.Files) {
            $html += "            <div class='file'>📄 $($file.Replace((Get-Location), '.'))</div>`n"
        }
        $html += @"
        </div>
    </div>
"@
        $groupIndex++
    }

    $html += @"
</body>
</html>
"@

    $html | Out-File -FilePath $htmlFile -Encoding UTF8
    Write-Host "`n📄 HTML Report: $htmlFile" -ForegroundColor Green
}

# Tạo JSON report
if ($OutputFormat -eq "json" -or $OutputFormat -eq "all") {
    $jsonFile = "$reportFile.json"
    $jsonData = [PSCustomObject]@{
        GeneratedAt = Get-Date
        Summary = [PSCustomObject]@{
            TotalFilesScanned = $totalFiles
            TotalSizeMB = [math]::Round($totalSize / 1MB, 2)
            DuplicateGroups = $duplicateGroups.Count
            DuplicateFiles = $totalDuplicateFiles
            WastedSpaceMB = [math]::Round($totalWastedSpace / 1MB, 2)
            WastePercentage = [math]::Round(($totalWastedSpace / $totalSize) * 100, 1)
        }
        DuplicateGroups = $duplicateAnalysis
        ExtensionStats = $extensionStats | ForEach-Object {
            [PSCustomObject]@{
                Extension = $_.Name
                Groups = $_.Count
                TotalFiles = ($_.Group | Measure-Object FileCount -Sum).Sum
                WastedSpaceKB = [math]::Round(($_.Group | Measure-Object WastedSpace -Sum).Sum / 1KB, 1)
            }
        }
    }
    
    $jsonData | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonFile -Encoding UTF8
    Write-Host "📄 JSON Report: $jsonFile" -ForegroundColor Green
}

# Đề xuất hành động
Write-Host "`n💡 Đề xuất hành động:" -ForegroundColor Cyan
Write-Host "   1. 🔧 Review các file trong top 5 nhóm duplicate lớn nhất" -ForegroundColor White
Write-Host "   2. 📦 Tạo shared modules cho code chung" -ForegroundColor White
Write-Host "   3. 🗂️ Refactor duplicate utilities thành reusable functions" -ForegroundColor White
Write-Host "   4. 🧹 Xóa các file duplicate không cần thiết" -ForegroundColor White
Write-Host "   5. 📋 Setup linting rules để prevent future duplicates" -ForegroundColor White

Write-Host "`n🎉 Analysis hoàn tất!" -ForegroundColor Green
