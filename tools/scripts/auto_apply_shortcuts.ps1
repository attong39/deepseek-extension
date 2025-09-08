# PowerShell shortcuts for auto-apply mode
function AI-Apply { uv run python ai_runner.py --once "$args" --apply }
function AI-Dedupe { uv run python ai_runner.py --once "xóa duplicate code" --apply }
function AI-Fix { uv run python ai_runner.py --once "fix imports, tạo __init__.__all__" --apply }
function AI-Clean { uv run python ai_runner.py --once "cleanup xóa unused" --apply }
function AI-Smart { uv run python ai_runner.py --once "smart remove" --apply }
function AI-Cleanup-File { param($file) uv run python ai_runner.py --once "cleanup $file" --apply }
function Guardian-Apply { uv run python -m deepseek.guardian.runner --scan --apply }
function Brain-Apply { uv run python -m deepseek.brain.orchestrator --apply }
function All-Apply { uv run python ai_runner.py --once "all" --apply }
function Enable-Apply { uv run python enable_apply_mode.py }

Set-Alias -Name "aia" -Value AI-Apply
Set-Alias -Name "aid" -Value AI-Dedupe
Set-Alias -Name "aif" -Value AI-Fix
Set-Alias -Name "aic" -Value AI-Clean
Set-Alias -Name "ais" -Value AI-Smart
Set-Alias -Name "aicf" -Value AI-Cleanup-File
Set-Alias -Name "ga" -Value Guardian-Apply
Set-Alias -Name "ba" -Value Brain-Apply
Set-Alias -Name "aa" -Value All-Apply
Set-Alias -Name "enable" -Value Enable-Apply

Write-Host "✅ Enhanced Auto-apply shortcuts loaded!"
Write-Host "Available commands:"
Write-Host "  aia <command>      - AI Runner with apply"
Write-Host "  aid                - Auto dedupe duplicate code"
Write-Host "  aif                - Auto fix imports + __init__.__all__"
Write-Host "  aic                - Auto cleanup dead code (all apps/backend)"
Write-Host "  ais                - Auto smart remove duplicates"
Write-Host "  aicf <file>        - Auto cleanup specific file"
Write-Host "  ga                 - Guardian apply"
Write-Host "  ba                 - Brain apply" 
Write-Host "  aa                 - All systems apply"
Write-Host "  enable             - Enable apply mode permanently"
Write-Host ""
Write-Host "Examples:"
Write-Host "  aic                                    # Clean all Python files"
Write-Host "  aicf zeta_vn/app/common/__init__.py   # Clean specific file"
Write-Host "  aid                                    # Remove duplicate code"
Write-Host "  aia 'cleanup, quality, dedupe'        # Combined cleanup"
