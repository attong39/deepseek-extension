# 🎯 NEXT STEPS ADVISOR - Gợi ý hành động tiếp theo
Write-Host "🎯 NEXT STEPS ADVISOR" -ForegroundColor Cyan
Write-Host "Dựa trên tình trạng hiện tại của hệ thống" -ForegroundColor Gray
Write-Host "=" * 50 -ForegroundColor Gray

# Quick status check
Write-Host "`n🔍 Quick Status Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/health" -TimeoutSec 3
    Write-Host "✅ Ollama API: $($health.status)" -ForegroundColor Green
    $systemReady = $true
} catch {
    Write-Host "❌ Ollama API: Not responding" -ForegroundColor Red
    $systemReady = $false
}

if ($systemReady) {
    Write-Host "`n🎉 HỆ THỐNG SẴN SÀNG!" -ForegroundColor Green
    Write-Host "=" * 30 -ForegroundColor Green
    
    # Test Drive Options
    Write-Host "`n🚀 TỪ ĐÂY BẠN CÓ THỂ:" -ForegroundColor Cyan
    Write-Host "`n1️⃣ TEST DRIVE NGAY (5 phút)" -ForegroundColor Yellow
    Write-Host "   📝 Restart VS Code" -ForegroundColor White
    Write-Host "   📝 Mở file .py bất kỳ" -ForegroundColor White
    Write-Host "   📝 Ctrl+L → chọn DeepSeek 6.7B" -ForegroundColor White
    Write-Host "   📝 Prompt: 'Write a web scraper in Python'" -ForegroundColor White
    Write-Host "   🎯 Result: AI sẽ generate code hoàn chỉnh" -ForegroundColor Magenta
    
    Write-Host "`n2️⃣ NÂNG CAO WORKFLOW (15 phút)" -ForegroundColor Yellow
    Write-Host "   🔧 Thử Ctrl+I (inline editing)" -ForegroundColor White
    Write-Host "   🔧 Test autocomplete (gõ 'def ' và chờ)" -ForegroundColor White
    Write-Host "   🔧 Slash commands: /edit, /comment, /commit" -ForegroundColor White
    Write-Host "   🔧 Switch models theo task (1.3B→fast, 16B→quality)" -ForegroundColor White
    
    Write-Host "`n3️⃣ CHUYỂN SANG ONLINE MODE (10 phút)" -ForegroundColor Yellow
    Write-Host "   🌐 Get API key từ provider (OpenAI, Anthropic, etc.)" -ForegroundColor White
    Write-Host "   🌐 .\login.ps1 login → nhập API key" -ForegroundColor White
    Write-Host "   🌐 .\login.ps1 switch -Mode online" -ForegroundColor White
    Write-Host "   🌐 Access latest cloud models" -ForegroundColor White
    
    Write-Host "`n4️⃣ TEAM ADOPTION (15 phút)" -ForegroundColor Yellow
    Write-Host "   👥 Export .vscode/settings.json to repo" -ForegroundColor White
    Write-Host "   👥 Share Continue config với team" -ForegroundColor White
    Write-Host "   👥 Setup CI/CD với AI checks" -ForegroundColor White
    Write-Host "   👥 Document best practices" -ForegroundColor White
    
    Write-Host "`n5️⃣ CUSTOM OPTIMIZATION (10 phút)" -ForegroundColor Yellow
    Write-Host "   ⚙️ Tạo custom model configs" -ForegroundColor White
    Write-Host "   ⚙️ Set temperature, max_tokens per task" -ForegroundColor White
    Write-Host "   ⚙️ Project-specific prompts" -ForegroundColor White
    Write-Host "   ⚙️ Performance monitoring setup" -ForegroundColor White
    
    # Immediate Actions
    Write-Host "`n💡 GỢI Ý HÀNH ĐỘNG NGAY:" -ForegroundColor Cyan
    Write-Host "=" * 30 -ForegroundColor Gray
    
    Write-Host "`n🎯 RECOMMENDED PRIORITY:" -ForegroundColor Yellow
    Write-Host "   1st: Test Drive → Verify everything works" -ForegroundColor Green
    Write-Host "   2nd: Workflow → Learn features deeply" -ForegroundColor Blue
    Write-Host "   3rd: Online Mode → Scale up capabilities" -ForegroundColor Magenta
    Write-Host "   4th: Team Setup → Share với đồng nghiệp" -ForegroundColor Cyan
    
    # Model Selection Guide
    Write-Host "`n📊 MODEL SELECTION GUIDE:" -ForegroundColor Cyan
    Write-Host "=" * 30 -ForegroundColor Gray
    
    Write-Host "`n🧠 DeepSeek Coder v2 16B (8.9GB)" -ForegroundColor Blue
    Write-Host "   ✅ Best: Complex algorithms, architecture design" -ForegroundColor White
    Write-Host "   ✅ Best: Code reviews, optimization" -ForegroundColor White
    Write-Host "   ❌ Slow: ~15-20s response time" -ForegroundColor Gray
    
    Write-Host "`n⚡ DeepSeek Coder 6.7B (3.8GB)" -ForegroundColor Green
    Write-Host "   ✅ Best: General coding, debugging" -ForegroundColor White
    Write-Host "   ✅ Best: Balanced speed/quality" -ForegroundColor White
    Write-Host "   ✅ Recommended: Daily development" -ForegroundColor Yellow
    
    Write-Host "`n🚀 DeepSeek Coder 1.3B (776MB)" -ForegroundColor Magenta
    Write-Host "   ✅ Best: Autocomplete, quick fixes" -ForegroundColor White
    Write-Host "   ✅ Best: Learning, experimentation" -ForegroundColor White
    Write-Host "   ✅ Fast: ~3-5s response time" -ForegroundColor Green
    
    Write-Host "`n🦙 Llama 3.1 8B (4.9GB)" -ForegroundColor Yellow
    Write-Host "   ✅ Best: Explanations, documentation" -ForegroundColor White
    Write-Host "   ✅ Best: Non-code tasks" -ForegroundColor White
    Write-Host "   ✅ Good: General purpose" -ForegroundColor Blue
    
    # Quick Start Commands
    Write-Host "`n⚡ QUICK START COMMANDS:" -ForegroundColor Cyan
    Write-Host "=" * 30 -ForegroundColor Gray
    
    Write-Host "`n📋 Copy & Paste Ready:" -ForegroundColor Yellow
    Write-Host @"
# Test AI trong VS Code
1. Restart VS Code: code --new-window
2. Mở file: echo 'def hello(): pass' > test.py; code test.py
3. Chat AI: Ctrl+L → 'Improve this function'
4. Inline edit: Select code → Ctrl+I → 'Add docstring'
"@ -ForegroundColor White
    
    Write-Host "`n🔧 Management Commands:" -ForegroundColor Yellow
    Write-Host ".\login.ps1 status              # Check current status" -ForegroundColor White
    Write-Host ".\login.ps1 switch -Mode local  # Switch to local models" -ForegroundColor White
    Write-Host ".\login.ps1 switch -Mode online # Switch to cloud models" -ForegroundColor White
    Write-Host "ollama list                     # See available models" -ForegroundColor White
    Write-Host "ollama pull <model>             # Download new model" -ForegroundColor White
    
} else {
    Write-Host "`n🔧 CẦN FIX TRƯỚC:" -ForegroundColor Red
    Write-Host "1. Start Ollama: ollama serve" -ForegroundColor White
    Write-Host "2. Wait 10 seconds" -ForegroundColor White
    Write-Host "3. Run this script again" -ForegroundColor White
}

# Performance Tips
Write-Host "`n🚀 PERFORMANCE TIPS:" -ForegroundColor Cyan
Write-Host "=" * 20 -ForegroundColor Gray
Write-Host "💻 RAM: 16GB+ recommended cho 16B model" -ForegroundColor White
Write-Host "⚡ SSD: Models load faster từ SSD" -ForegroundColor White
Write-Host "🔧 GPU: NVIDIA GPU sẽ tăng tốc inference" -ForegroundColor White
Write-Host "🌐 Network: Stable internet cho online mode" -ForegroundColor White

# Troubleshooting Reference
Write-Host "`n🛠️ TROUBLESHOOTING REFERENCE:" -ForegroundColor Yellow
Write-Host "=" * 30 -ForegroundColor Gray
Write-Host "Slow response → Switch to 1.3B model" -ForegroundColor White
Write-Host "No response → Restart Ollama: ollama serve" -ForegroundColor White
Write-Host "Wrong model → Check Continue config" -ForegroundColor White
Write-Host "VS Code issues → Restart VS Code completely" -ForegroundColor White
Write-Host "Extension missing → Install: code --install-extension continue.continue" -ForegroundColor White

Write-Host "`n" + "=" * 50 -ForegroundColor Gray
Write-Host "🎯 CHOOSE YOUR ADVENTURE!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Gray

$choice = Read-Host "`nBạn muốn làm gì tiếp theo? (1-5, hoặc 'help')"

switch ($choice) {
    "1" {
        Write-Host "`n🚀 STARTING TEST DRIVE..." -ForegroundColor Green
        Write-Host "1. Opening VS Code..." -ForegroundColor White
        Start-Process "code" -ArgumentList "--new-window"
        Write-Host "2. Creating test file..." -ForegroundColor White
        "def fibonacci(n):`n    # TODO: Implement fibonacci`n    pass" | Out-File -FilePath ".\ai_test.py" -Encoding UTF8
        Start-Sleep 2
        Start-Process "code" -ArgumentList ".\ai_test.py"
        Write-Host "3. ✅ VS Code opened with test file" -ForegroundColor Green
        Write-Host "`n🎯 NEXT: Press Ctrl+L in VS Code và select DeepSeek 6.7B" -ForegroundColor Cyan
        Write-Host "💬 PROMPT: 'Complete the fibonacci function with recursion'" -ForegroundColor Yellow
    }
    "2" {
        Write-Host "`n⚡ WORKFLOW ENHANCEMENT GUIDE..." -ForegroundColor Blue
        Write-Host "🔧 Key shortcuts to learn:" -ForegroundColor White
        Write-Host "   Ctrl+L: Chat with AI" -ForegroundColor Gray
        Write-Host "   Ctrl+I: Inline edit" -ForegroundColor Gray
        Write-Host "   Tab: Accept autocomplete" -ForegroundColor Gray
        Write-Host "   /edit: Edit selected code" -ForegroundColor Gray
        Write-Host "   /comment: Add comments" -ForegroundColor Gray
        Write-Host "   /commit: Generate commit message" -ForegroundColor Gray
    }
    "3" {
        Write-Host "`n🌐 ONLINE MODE SETUP..." -ForegroundColor Magenta
        Write-Host "📋 Available providers:" -ForegroundColor White
        Write-Host "   • OpenAI (GPT-4, GPT-3.5)" -ForegroundColor Gray
        Write-Host "   • Anthropic (Claude)" -ForegroundColor Gray
        Write-Host "   • Together.ai (Various models)" -ForegroundColor Gray
        Write-Host "   • Fireworks.ai (Fast inference)" -ForegroundColor Gray
        Write-Host "`n🔧 To setup: .\login.ps1 login" -ForegroundColor Yellow
    }
    "4" {
        Write-Host "`n👥 TEAM ADOPTION GUIDE..." -ForegroundColor Cyan
        Write-Host "📂 Files to share:" -ForegroundColor White
        Write-Host "   • .vscode/settings.json" -ForegroundColor Gray
        Write-Host "   • .continue/config.json" -ForegroundColor Gray
        Write-Host "   • setup scripts (.ps1 files)" -ForegroundColor Gray
        Write-Host "`n📚 Documentation to create:" -ForegroundColor White
        Write-Host "   • AI usage guidelines" -ForegroundColor Gray
        Write-Host "   • Model selection guide" -ForegroundColor Gray
        Write-Host "   • Best practices" -ForegroundColor Gray
    }
    "5" {
        Write-Host "`n⚙️ CUSTOM OPTIMIZATION..." -ForegroundColor Yellow
        Write-Host "🔧 Advanced configurations:" -ForegroundColor White
        Write-Host "   • Custom model parameters" -ForegroundColor Gray
        Write-Host "   • Project-specific prompts" -ForegroundColor Gray
        Write-Host "   • Performance monitoring" -ForegroundColor Gray
        Write-Host "   • Resource optimization" -ForegroundColor Gray
    }
    "help" {
        Write-Host "`n📚 HELP RESOURCES:" -ForegroundColor Blue
        Write-Host "🔗 Documentation:" -ForegroundColor White
        Write-Host "   • Ollama: https://ollama.ai/docs" -ForegroundColor Gray
        Write-Host "   • Continue: https://continue.dev/docs" -ForegroundColor Gray
        Write-Host "   • DeepSeek: https://deepseek.com" -ForegroundColor Gray
        Write-Host "`n🛠️ Support commands:" -ForegroundColor White
        Write-Host "   • .\quick_health_check.ps1" -ForegroundColor Gray
        Write-Host "   • .\login.ps1 status" -ForegroundColor Gray
        Write-Host "   • ollama --help" -ForegroundColor Gray
    }
    default {
        Write-Host "`n✨ NO CHOICE? NO PROBLEM!" -ForegroundColor Green
        Write-Host "🎯 Recommended: Start with option 1 (Test Drive)" -ForegroundColor White
        Write-Host "💡 Just restart VS Code and press Ctrl+L to begin!" -ForegroundColor Cyan
    }
}

Write-Host "`n🎉 Happy coding với AI assistant! 🚀" -ForegroundColor Green