# DeepSeek Triển Khai Tự Động

## Tổng Quan
Hệ thống DeepSeek là AI-powered orchestrator cho code optimization, với auto-apply, brain, guardian, và extension tích hợp. Triển khai theo nguyên tắc domain-driven, tương thích ngược, và quality gates.

## Cài Đặt Nhanh

### 1. Chuẩn Bị Environment
```bash
# Cài uv nếu chưa có
pip install uv

# Sync dependencies
uv sync

# Set API keys
export ZETA_API_URL="http://127.0.0.1:8099"
# Thêm DEEPSEEK_API_KEY nếu cần
```

### 2. Chạy Triển Khai Tự Động
```bash
python deploy_deepseek.py
```

### 3. Chạy Core Scripts Thủ Công
```bash
# Auto-apply với LLM
python deepseek/auto/auto_apply.py --commit --push --llm --actions "upgrade, fix imports, quality + perf"

# AI Runner
python deepseek/auto/ai_runner.py --apply

# VN Copilot
python deepseek/auto/vn_copilot.py --help
```

### 4. Build VS Code Extension
```bash
cd deepseek-extension
npm install
npm run compile
npx vsce package
```

## Cấu Trúc Thư Mục
```
deepseek/
├── auto/           # Auto-apply & AI runner scripts
├── brain/          # AI reasoning modules
├── guardian/       # Security scanning
├── learning/       # Auto-learning system
└── integrations/   # External integrations

deepseek-extension/ # VS Code extension
├── src/           # TypeScript source
├── web/           # Webview UI
└── package.json   # Extension config
```

## Quality Gates
- **Python**: ruff check, mypy, pytest
- **TypeScript**: eslint, tsc
- **Performance**: uvicorn startup time
- **Security**: Guardian scan

## CI/CD Pipeline
Workflow tự động trong `.github/workflows/deploy.yml`:
- Test trên push/PR
- Auto-apply changes
- Build extension
- Deploy to production

## Best Practices
- Luôn chạy `tools/check_related_files.py` trước thay đổi
- Review changes trước commit
- Monitor logs trong `.artifacts/`
- Backup trước khi apply lớn

## Troubleshooting
- Logs: `.artifacts/auto_apply_*.log`
- Summary: `.artifacts/ai_runner_summary.json`
- Patch nếu fail: `.artifacts/auto_apply.patch`

## Liên Hệ
Nếu gặp vấn đề, chia sẻ logs cụ thể để debug.
