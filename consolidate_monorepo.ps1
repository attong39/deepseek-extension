# Script PowerShell để hợp nhất cấu trúc monorepo Zeta
# Chạy: .\consolidate_monorepo.ps1

param(
      [switch]$DryRun,
      [switch]$Force,
      [switch]$CopySwap,
      [string[]]$Exclude = @()
)

Write-Host "🚀 Bắt đầu hợp nhất cấu trúc monorepo Zeta" -ForegroundColor Green
Write-Host ("=" * 50) -ForegroundColor Yellow

# Hàm tạo thư mục
function New-DirectoryStructure {
      Write-Host "📁 Tạo cấu trúc thư mục mới..." -ForegroundColor Cyan

      $dirs = @(
            "apps",
            "packages\shared",
            "packages\ui-components",
            "packages\core-utils",
            "tools",
            "docs",
            "config",
            "scripts"
      )

      foreach ($dir in $dirs) {
            if (-not (Test-Path $dir)) {
                  if ($DryRun) {
                        Write-Host "  [DRY RUN] Sẽ tạo: $dir" -ForegroundColor Gray
                  }
                  else {
                        New-Item -ItemType Directory -Path $dir -Force | Out-Null
                        Write-Host "  ✓ Tạo: $dir" -ForegroundColor Green
                  }
            }
            else {
                  Write-Host "  ⚠️  Đã tồn tại: $dir" -ForegroundColor Yellow
            }
      }
}

# Hàm di chuyển thư mục
function Move-Apps {
      Write-Host "📦 Di chuyển các ứng dụng vào apps/..." -ForegroundColor Cyan

      $appNames = @('zeta-ai-agent', 'desktop', 'backend')
      foreach ($name in $appNames) {
            $src = $name
            $dst = Join-Path 'apps' $name

            if (-not (Test-Path $src)) {
                  Write-Host "  ⏭️  Bỏ qua (không tồn tại): $src" -ForegroundColor DarkYellow
                  continue
            }

            if (Test-Path $dst) {
                  if ($Force) {
                        Write-Host "  🗑️  Xóa thư mục đích: $dst" -ForegroundColor Red
                        if (-not $DryRun) { Remove-Item $dst -Recurse -Force }
                  }
                  else {
                        Write-Host "  ⚠️  Thư mục đích đã tồn tại: $dst" -ForegroundColor Yellow
                        $response = Read-Host "  Xóa và tiếp tục? (y/N)"
                        if ($response -eq 'y' -or $response -eq 'Y') {
                              if (-not $DryRun) { Remove-Item $dst -Recurse -Force }
                        }
                        else {
                              Write-Host "  ⏭️  Bỏ qua: $src" -ForegroundColor Gray
                              continue
                        }
                  }
            }

            if (-not $CopySwap) {
                  if ($DryRun) {
                        Write-Host "  [DRY RUN] Sẽ di chuyển: $src → $dst" -ForegroundColor Gray
                  }
                  else {
                        Write-Host "  📁 Di chuyển: $src → $dst" -ForegroundColor Green
                        New-Item -ItemType Directory -Path (Split-Path $dst) -Force | Out-Null
                        Move-Item $src $dst
                  }
            }
            else {
                  # Copy-Swap mode: copy filtered, verify, then remove source
                  $defaultExcludes = @('node_modules', 'dist', 'out', '.venv', '.git', '__pycache__', '.ruff_cache', '.mypy_cache', '.pytest_cache', '.vscode')
                  $allExcludes = $defaultExcludes + $Exclude
                  Write-Host "  🧩 Copy-Swap $src → $dst (bỏ qua: $($allExcludes -join ', '))" -ForegroundColor Cyan

                  if (-not $DryRun) {
                        New-Item -ItemType Directory -Path $dst -Force | Out-Null
                  }

                  function Get-Counts($base, $ex) {
                        $files = 0
                        $bytes = 0
                        if (-not (Test-Path $base)) { return @($files, $bytes) }
                        Get-ChildItem -Path $base -Recurse -Force -File -ErrorAction SilentlyContinue |
                        Where-Object { $rel = $_.FullName.Substring($base.Length) ; -not ($ex | ForEach-Object { $rel -match "\$_(\\\\|$)" }) } |
                        ForEach-Object { $files += 1; $bytes += $_.Length }
                        return @($files, $bytes)
                  }

                  $srcCounts = Get-Counts -base $src -ex $allExcludes
                  if ($DryRun) {
                        Write-Host "    [DRY RUN] Nguồn (lọc): $($srcCounts[0]) files, $($srcCounts[1]) bytes" -ForegroundColor Gray
                        Write-Host "    [DRY RUN] Sẽ SAO CHÉP (lọc) toàn bộ cây" -ForegroundColor Gray
                  }
                  else {
                        # copy filtered
                        Get-ChildItem -Path $src -Recurse -Force -File -ErrorAction SilentlyContinue |
                        Where-Object { $rel = $_.FullName.Substring($src.Length) ; -not ($allExcludes | ForEach-Object { $rel -match "\$_(\\\\|$)" }) } |
                        ForEach-Object {
                              $rel = $_.FullName.Substring($src.Length).TrimStart('\\', '/')
                              $destPath = Join-Path $dst $rel
                              New-Item -ItemType Directory -Path (Split-Path $destPath) -Force | Out-Null
                              Copy-Item -Path $_.FullName -Destination $destPath -Force -ErrorAction SilentlyContinue
                        }

                        $dstCounts = Get-Counts -base $dst -ex $allExcludes
                        if ($dstCounts[0] -ne $srcCounts[0] -or $dstCounts[1] -ne $srcCounts[1]) {
                              Write-Host "    ❌ Xác minh thất bại: src($($srcCounts[0]),$($srcCounts[1])) != dst($($dstCounts[0]),$($dstCounts[1]))" -ForegroundColor Red
                        }
                        else {
                              Write-Host "    ✓ Sao chép OK, xóa nguồn" -ForegroundColor Green
                              Remove-Item $src -Recurse -Force
                        }
                  }
            }
      }
}

# Hàm cập nhật package.json
function Update-PackageJson {
      Write-Host "📝 Cập nhật package.json..." -ForegroundColor Cyan

      $packageJsonPath = "package.json"

      if (-not (Test-Path $packageJsonPath)) {
            Write-Host "  ⚠️  Không tìm thấy package.json" -ForegroundColor Yellow
            return
      }

      try {
            $packageData = Get-Content $packageJsonPath -Raw | ConvertFrom-Json

            if (-not $packageData.PSObject.Properties.Match('workspaces')) {
                  $packageData | Add-Member -MemberType NoteProperty -Name 'workspaces' -Value @('apps/*', 'packages/*')

                  if (-not $DryRun) {
                        $packageData | ConvertTo-Json -Depth 10 | Set-Content $packageJsonPath -Encoding UTF8
                  }
                  Write-Host "  ✓ Thêm workspaces vào package.json" -ForegroundColor Green
            }
            else {
                  Write-Host "  ⚠️  Workspaces đã tồn tại trong package.json" -ForegroundColor Yellow
            }
      }
      catch {
            Write-Host "  ❌ Lỗi đọc package.json: $($_.Exception.Message)" -ForegroundColor Red
      }
}

# Hàm tạo package shared
function New-SharedPackage {
      Write-Host "📦 Tạo package shared..." -ForegroundColor Cyan

      $sharedDir = "packages\shared"

      if (-not (Test-Path $sharedDir)) {
            if (-not $DryRun) {
                  New-Item -ItemType Directory -Path $sharedDir -Force | Out-Null
            }
      }

      # Tạo package.json
      $packageJson = @{
            name        = "@zeta/shared"
            version     = "1.0.0"
            description = "Shared utilities for Zeta monorepo"
            main        = "index.js"
            types       = "index.d.ts"
            scripts     = @{
                  build = "tsc"
                  test  = "jest"
            }
      }

      $packageJsonPath = Join-Path $sharedDir "package.json"
      if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ tạo: $packageJsonPath" -ForegroundColor Gray
      }
      else {
            $packageJson | ConvertTo-Json | Set-Content $packageJsonPath -Encoding UTF8
            Write-Host "  ✓ Tạo: $packageJsonPath" -ForegroundColor Green
      }

      # Tạo tsconfig.json
      $tsconfig = @{
            compilerOptions = @{
                  target          = "ES2020"
                  module          = "commonjs"
                  declaration     = $true
                  outDir          = "./dist"
                  rootDir         = "./src"
                  strict          = $true
                  esModuleInterop = $true
            }
            include         = @("src/**/*")
            exclude         = @("node_modules", "dist")
      }

      $tsconfigPath = Join-Path $sharedDir "tsconfig.json"
      if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ tạo: $tsconfigPath" -ForegroundColor Gray
      }
      else {
            $tsconfig | ConvertTo-Json | Set-Content $tsconfigPath -Encoding UTF8
            Write-Host "  ✓ Tạo: $tsconfigPath" -ForegroundColor Green
      }

      # Tạo thư mục src
      $srcDir = Join-Path $sharedDir "src"
      if (-not (Test-Path $srcDir)) {
            if (-not $DryRun) {
                  New-Item -ItemType Directory -Path $srcDir -Force | Out-Null
            }
            Write-Host "  ✓ Tạo thư mục: $srcDir" -ForegroundColor Green
      }

      # Tạo file index.ts
      $indexPath = Join-Path $srcDir "index.ts"
      $indexContent = @"
// Shared utilities for Zeta monorepo

export const VERSION = '1.0.0';

export function logInfo(message: string) {
    console.log(`[INFO] ${message}`);
}

export function logError(message: string) {
    console.error(`[ERROR] ${message}`);
}
"@

      if ($DryRun) {
            Write-Host "  [DRY RUN] Sẽ tạo: $indexPath" -ForegroundColor Gray
      }
      else {
            $indexContent | Set-Content $indexPath -Encoding UTF8
            Write-Host "  ✓ Tạo: $indexPath" -ForegroundColor Green
      }
}

# Main execution
try {
      New-DirectoryStructure
      Write-Host ""

      Move-Apps
      Write-Host ""

      Update-PackageJson
      Write-Host ""

      New-SharedPackage
      Write-Host ""

      if ($DryRun) {
            Write-Host "✅ Dry run hoàn thành! Chạy lại không có -DryRun để thực hiện." -ForegroundColor Green
      }
      else {
            Write-Host "✅ Hoàn thành hợp nhất cấu trúc!" -ForegroundColor Green
      }

      Write-Host ""
      Write-Host "📋 Các bước tiếp theo:" -ForegroundColor Cyan
      Write-Host "1. Kiểm tra các apps hoạt động: npm run build trong apps/*" -ForegroundColor White
      Write-Host "2. Cập nhật import paths nếu cần" -ForegroundColor White
      Write-Host "3. Test integration giữa các apps" -ForegroundColor White
      Write-Host "4. Cập nhật documentation" -ForegroundColor White

}
catch {
      Write-Host "❌ Lỗi: $($_.Exception.Message)" -ForegroundColor Red
      exit 1
}