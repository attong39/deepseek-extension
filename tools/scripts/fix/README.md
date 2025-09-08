# Auto-Fix Deps & Virtual Environment

Bộ công cụ "một lệnh sửa hết" để khắc phục lỗi virtual environment và dependencies.

## 🎯 Mục tiêu

- ✅ Sửa lỗi `_virtualenv.pth` conflict (backup an toàn)
- ✅ Đảm bảo `typer`, `rich`, `requests` dependencies 
- ✅ Tạo/refresh virtual environment bằng `uv`
- ✅ Kiểm tra nhanh import và stack readiness
- ✅ VS Code tasks để chạy ngay

## 🚀 Cách sử dụng

### PowerShell (Windows) - Khuyến nghị
```powershell
# Chạy auto-fix toàn bộ
pwsh -File scripts/fix/auto_fix_env.ps1

# Hoặc qua VS Code tasks
# Ctrl+Shift+P → Tasks: Run Task → "Fix: Deps & Venv (Auto)"
```

### Bash (Linux/Mac)
```bash
# Cấp quyền
chmod +x scripts/fix/auto_fix_env.sh

# Chạy auto-fix
bash scripts/fix/auto_fix_env.sh
```

### Python trực tiếp
```bash
# Chỉ sửa environment
uv run python scripts/fix/repair_env.py --apply

# Kiểm tra stack
uv run python scripts/fix/verify_stack.py

# Demo đầy đủ
uv run python scripts/fix/demo_fix_env.py
```

## 🔧 VS Code Tasks

Đã được cấu hình sẵn trong `.vscode/tasks.json`:

1. **"Fix: Deps & Venv (Auto)"** - Auto-fix toàn bộ environment
2. **"Fix: Repair Environment Only"** - Chỉ sửa `_virtualenv.pth` conflict

### Cách chạy:
1. `Ctrl+Shift+P`
2. Gõ: `Tasks: Run Task`
3. Chọn task mong muốn

## 📁 Cấu trúc Files

```
scripts/fix/
├── auto_fix_env.ps1      # PowerShell orchestrator
├── auto_fix_env.sh       # Bash orchestrator  
├── repair_env.py         # Core environment repair
├── verify_stack.py       # Stack verification
├── demo_fix_env.py       # Demo & testing
└── test_fix_env.py       # Automated tests
```

## 🛠️ Chi tiết hoạt động

### 1. repair_env.py
- Tìm và backup `_virtualenv.pth` files → `.pth.bak`
- Tạo/refresh virtual environment qua `uv venv` và `uv sync`
- Cài đặt `typer`, `rich`, `requests` nếu thiếu
- Kiểm tra import để đảm bảo dependencies sẵn sàng

### 2. auto_fix_env.ps1/sh  
- Orchestrator chạy toàn bộ pipeline
- Sync apps/backend dependencies (`zeta_vn_restructured` hoặc `zeta_vn`)
- Cài apps/desktop dependencies nếu có (`npm ci` hoặc `npm i`)
- Kiểm tra cuối cùng bằng `verify_stack.py`

### 3. verify_stack.py
- Report Python packages status
- Check Node.js/npm availability
- Export JSON report → `.artifacts/verify_stack.json`

## ✅ Test & Validation

```bash
# Test tự động
uv run python scripts/fix/test_fix_env.py

# Demo manual
uv run python scripts/fix/demo_fix_env.py

# Kiểm tra typer import
uv run python -c "import typer; print(f'typer OK: {typer.__version__}')"
```

## 🔍 Troubleshooting

### Lỗi thường gặp:

1. **`_virtualenv.pth` conflict**
   ```
   IndentationError: unexpected indent in _virtualenv.py
   ```
   **Giải pháp**: Chạy `repair_env.py --apply` để backup file

2. **`ModuleNotFoundError: No module named 'typer'`**
   ```
   ImportError during Deepseek execution
   ```
   **Giải pháp**: Chạy `uv add typer rich requests --dev`

3. **Virtual environment không tìm thấy**
   ```
   No virtual environment detected
   ```
   **Giải pháp**: Chạy `uv venv` để tạo environment mới

### Debug commands:
```bash
# Check virtual environment
echo $VIRTUAL_ENV

# List installed packages  
uv pip list

# Check site-packages
python -c "import site; print(site.getsitepackages())"
```

## 🎯 Next Steps

1. **Sau khi auto-fix thành công:**
   ```bash
   uv run python -m deepseek agent --apply
   ```

2. **Hoặc chạy start_all.py:**
   ```bash
   uv run python start_all.py --apply
   ```

3. **Kiểm tra reports:**
   ```bash
   cat .artifacts/verify_stack.json
   ls .artifacts/
   ```

## 🔒 Safety Features

- ✅ **Backup tự động**: `_virtualenv.pth` → `_virtualenv.pth.bak`
- ✅ **Dry-run mặc định**: Cần `--apply` để thay đổi files
- ✅ **Error handling**: Graceful degradation nếu commands fail
- ✅ **Idempotent**: An toàn chạy nhiều lần
- ✅ **Cross-platform**: PowerShell + Bash support

## 🚨 Important Notes

- Script không động đến secrets/credentials
- Chỉ backup/rename files, không xóa hoàn toàn
- Dependencies sử dụng `uv` package manager
- Compatible với existing `pyproject.toml` setup
- Không ảnh hưởng đến production environment
