# 🎯 Quality Gates Configuration - Updated Paths

## ✅ Configuration Applied Successfully!

VS Code đã được cấu hình với **quality gates tự động** và **đường dẫn cập nhật** cho cấu trúc dự án mới.

## 🏗️ Cấu Trúc Dự Án Mới

```
zeta/
├── zeta_vn_restructured/    # Backend Python (cũ: zeta_vn)
├── desktop_ai_zeta/         # Desktop Electron app  
├── tests/                   # Test files
├── tools/                   # Development tools
└── scripts/quality/         # Quality gate scripts
```

## 🚀 Tính Năng Tự Động

### ⚡ Khi Mở VS Code:
- ✅ **Auto-run quality checks** (ruff + mypy + pytest)
- ✅ **Problems panel** hiển thị lỗi ngay lập tức
- ✅ **Type checking strict** cho code quality cao
- ✅ **Auto-fix on save** sửa lỗi tự động

### 📁 Đường Dẫn Đã Cập Nhật:
- ✅ `zeta_vn_restructured/**` cho Python apps/backend
- ✅ `desktop_ai_zeta/**` cho Electron apps/desktop app  
- ✅ MyPy checks: `zeta_vn_restructured/`
- ✅ Bandit security: `zeta_vn_restructured/`
- ✅ File associations cho cả Python và TypeScript

## ⌨️ Phím Tắt Mới

| Phím | Action |
|------|--------|
| `Ctrl+Shift+9` | Run quality gates nhanh |
| `Ctrl+Shift+0` | Run quality gates đầy đủ |
| `Ctrl+Shift+8` | Switch to quality gates config |

## 🔧 Scripts Chạy Thủ Công

### Backend (Python):
```powershell
# Chạy quality gates toàn bộ
./scripts/quality/quality_gates_updated.ps1

# Hoặc từng bước:
uv run ruff check .
uv run mypy zeta_vn_restructured
uv run pytest -q -k "not slow"
uv run bandit -q -r zeta_vn_restructured
```

### Desktop (TypeScript):
```powershell
cd desktop_ai_zeta
npm run lint
npm run type-check
npm run test
```

## 🔄 Chuyển Đổi Cấu Hình

```powershell
# Quality Gates (current) - Auto checks, strict typing
Copy-Item '.vscode/settings_quality_gates.json' '.vscode/settings.json' -Force

# Ultra Light - Maximum speed
Copy-Item '.vscode/settings_ultra_light.json' '.vscode/settings.json' -Force

# Minimal - Balanced
Copy-Item '.vscode/settings_minimal.json' '.vscode/settings.json' -Force
```

## 📊 Tasks Tự Động

| Task | Trigger | Description |
|------|---------|-------------|
| `Run: Gates Quick` | **folderOpen** | Auto-run khi mở workspace |
| `Gates: Ruff` | Manual/Auto | Lint + format check |
| `Gates: Mypy` | Manual/Auto | Type checking strict |
| `Gates: Pytest (quick)` | Manual/Auto | Fast tests only |
| `dev:apps/desktop` | Manual | Start apps/desktop dev server |

## 🛡️ Pre-commit Hooks

```bash
# Cài đặt pre-commit cho cả apps/backend và apps/desktop
cp .pre-commit-config-updated.yaml .pre-commit-config.yaml
uv pip install pre-commit
pre-commit install
```

## 🎯 Kết Quả Mong Đợi

1. **Mở VS Code** → Auto quality checks chạy ngay
2. **Viết code** → Lỗi hiện ngay trong Problems panel
3. **Save file** → Auto-fix formatting và imports
4. **Commit** → Pre-commit hooks ngăn lỗi vào repo
5. **Fast feedback** → Phát hiện lỗi sớm, fix nhanh

## 🔄 Reload VS Code

**Quan trọng**: Reload VS Code ngay để kích hoạt cấu hình mới:
- Press `Ctrl+Shift+P`
- Type "Developer: Reload Window"  
- Press Enter

Quality gates sẽ tự động chạy khi reload xong! 🚀