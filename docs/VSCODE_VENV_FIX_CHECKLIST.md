# 🔧 Checklist Khắc Phục Lỗi Môi Trường Ảo VS Code

## ❗ Vấn đề Phổ Biến Đã Phát Hiện

1. **Python Interpreter sai**: VS Code/Terminal đang dùng Python global thay vì môi trường ảo `.venv`
2. **Môi trường ảo chưa được kích hoạt** trong terminal VS Code
3. **Path conflicts** giữa Python global và virtual environment

## ✅ Các Bước Khắc Phục (Theo Thứ Tự)

### 1. Kích Hoạt Môi Trường Ảo Ngay Lập Tức
```powershell
# PowerShell (Windows)
.\.venv\Scripts\Activate.ps1

# Hoặc dùng script tự động
.\tools\fix_vscode_venv.ps1
```

### 2. Cấu Hình Python Interpreter Trong VS Code
- `Ctrl+Shift+P` → "Python: Select Interpreter"
- Chọn: `E:\zeta\.venv\Scripts\python.exe`
- **Quan trọng**: Không chọn Python global!

### 3. Restart VS Code Hoàn Toàn
- Đóng tất cả VS Code windows
- Mở lại workspace: `code .`

### 4. Kiểm Tra Terminal Mới
- Mở terminal mới: `Ctrl+Shift+` `
- Kiểm tra: `python --version` và `which python` (Linux/macOS) hoặc `Get-Command python` (Windows)
- Phải hiển thị đường dẫn `.venv`

### 5. Test Imports
```python
python -c "import fastapi, uvicorn, pydantic; print('✅ OK')"
```

## 🛠️ Scripts Tự Động

### PowerShell (Windows) - Khuyến nghị
```powershell
.\tools\fix_vscode_venv.ps1
```

### Python (Cross-platform)
```bash
uv run python tools/fix_vscode_venv.py
```

## 🔍 Kiểm Tra Cuối Cùng

### ✅ Dấu hiệu môi trường ảo hoạt động đúng:
- Terminal có prefix `(.venv)` 
- `python --version` trả về `Python 3.11.13` (từ `.venv`)
- `python -c "import sys; print(sys.executable)"` trả về đường dẫn `.venv\Scripts\python.exe`
- VS Code status bar hiển thị Python interpreter từ `.venv`

### ❌ Dấu hiệu vẫn có vấn đề:
- Không có prefix `(.venv)` trong terminal
- `python --version` trả về đường dẫn global (`AppData\Local\Programs\Python`)
- Import packages thất bại
- VS Code status bar hiển thị Python global

## 🚨 Xử Lý Sự Cố Nâng Cao

### Nếu vẫn không hoạt động:

1. **Xóa và tạo lại môi trường ảo**:
```powershell
Remove-Item -Recurse -Force .venv
uv venv
uv sync
```

2. **Reset VS Code workspace settings**:
```powershell
# Backup settings
Copy-Item .vscode\settings.json .vscode\settings.json.backup

# Reset Python settings (giữ nguyên phần khác)
# Sửa python.defaultInterpreterPath trong settings.json
```

3. **Kiểm tra PATH environment**:
```powershell
$env:PATH -split ';' | Select-String 'python'
```

4. **Force reload VS Code extensions**:
- `Ctrl+Shift+P` → "Developer: Reload Window"

## 📋 Task VS Code

Đã tạo task tự động trong `.vscode/tasks.json`:
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Fix Python Virtual Environment"

## 🎯 Kết Quả Mong Đợi

Sau khi hoàn thành tất cả bước:
- ✅ Terminal VS Code tự động kích hoạt `.venv`
- ✅ Python imports hoạt động bình thường  
- ✅ Development server chạy được: `uv run uvicorn zeta_vn.app.main_production:app --reload`
- ✅ Tests chạy được: `uv run pytest`
- ✅ Linting hoạt động: `uv run ruff check .`

## 📞 Hỗ Trợ

Nếu vẫn gặp vấn đề, chạy script diagnostic:
```powershell
.\tools\fix_vscode_venv.ps1 -Verbose
```

Và báo cáo kết quả đầy đủ.
