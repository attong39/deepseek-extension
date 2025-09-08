# VN Copilot - Thầy Huấn luyện DeepSeek 

## 🎯 TỔNG QUAN

**VN Copilot** đã được nâng cấp thành **"Thầy Huấn luyện DeepSeek"** - một AI coding assistant hoàn chỉnh với khả năng:

✅ **Nhận lệnh tiếng Việt tự nhiên** - giao tiếp bằng tiếng Việt trong terminal  
✅ **DeepSeek AI Coach** - phân tích, giảng dạy, đề xuất patch, thực thi an toàn  
✅ **Patch JSON chuẩn** - hệ thống vá code an toàn với backup + dry-run  
✅ **Học từ mã nguồn** - thu thập context để ngày càng thông minh  
✅ **Tất cả trong 1 file** - `deepseek/auto/vn_copilot.py` chạy độc lập  

---

## 🔧 CẤU HÌNH

### Biến môi trường bắt buộc:
```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY = "sk-your-api-key-here"
$env:DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"  # optional
$env:DEEPSEEK_MODEL = "deepseek-chat"                   # optional

# Linux/macOS
export DEEPSEEK_API_KEY="sk-your-api-key-here"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
export DEEPSEEK_MODEL="deepseek-chat"
```

### Kiểm tra cấu hình:
```bash
python demo_deepseek_coach.py
```

---

## 🚀 CÁCH SỬ DỤNG

### 1. REPL Mode (Chat tiếng Việt)
```bash
python deepseek/auto/vn_copilot.py

🇻🇳 VN Copilot + Thầy Huấn Luyện – `help` để xem. `thoát` để rời.
🇻🇳> help
🇻🇳> giảng dạy clean architecture trên deepseek/auto/
🇻🇳> phân tích dự án zeta_vn
🇻🇳> đề xuất vá cải thiện typing cho deepseek/auto/
🇻🇳> thực thi vá !force
🇻🇳> thoát
```

### 2. One-shot Mode
```bash
# Giảng dạy
python deepseek/auto/vn_copilot.py -c "giảng dạy unit testing trên deepseek/auto/"

# Phân tích dự án
python deepseek/auto/vn_copilot.py -c "phân tích dự án zeta_vn"

# Đề xuất vá (dry-run)
python deepseek/auto/vn_copilot.py -c "đề xuất vá cải thiện imports"

# Thực thi vá (ghi thật)
python deepseek/auto/vn_copilot.py -c "thực thi vá !force"

# Học từ mã nguồn
python deepseek/auto/vn_copilot.py -c "học từ deepseek/"

# File operations
python deepseek/auto/vn_copilot.py -c "quét dự án"
python deepseek/auto/vn_copilot.py -c "chạy ruff"
python deepseek/auto/vn_copilot.py -c "xem file deepseek/auto/vn_copilot.py"
```

---

## 🎓 CHỨC NĂNG COACH (MỚI)

### 1. Giảng dạy (Teaching)
```bash
🇻🇳> giảng dạy clean architecture
🇻🇳> giảng dạy unit testing trên deepseek/auto/
🇻🇳> giảng dạy async programming trên zeta_vn/app/
```
**→ Giải thích khái niệm, đưa ra checklist thực dụng**

### 2. Phân tích (Analysis)
```bash
🇻🇳> phân tích dự án zeta_vn
🇻🇳> phân tích file deepseek/auto/vn_copilot.py
🇻🇳> phân tích thư mục deepseek/brain/
```
**→ Đánh giá chất lượng, phát hiện rủi ro, đưa ra khuyến nghị**

### 3. Đề xuất vá (Patch Proposal)
```bash
🇻🇳> đề xuất vá cải thiện typing
🇻🇳> đề xuất vá fix imports trên deepseek/auto/
🇻🇳> đề xuất vá nâng coverage unit test
```
**→ Tạo JSON patches an toàn, lưu vào `.artifacts/patches/`**

### 4. Thực thi vá (Patch Application)
```bash
🇻🇳> thực thi vá          # dry-run
🇻🇳> thực thi vá !force   # ghi thật
```
**→ Áp dụng LAST patches với backup tự động**

---

## 📋 PATCH JSON SCHEMA

VN Copilot sử dụng format JSON đơn giản nhưng mạnh mẽ:

```json
{
  "patches": [
    {
      "op": "write_file",
      "path": "path/to/file.py",
      "content": "# New file content\n..."
    },
    {
      "op": "replace_regex", 
      "path": "path/to/file.py",
      "pattern": "old_pattern",
      "repl": "new_replacement"
    },
    {
      "op": "append",
      "path": "path/to/file.py", 
      "content": "\n# Additional content"
    },
    {
      "op": "delete",
      "path": "path/to/old_file.py"
    }
  ],
  "notes": [
    "Giải thích patch 1",
    "Khuyến nghị cho patch 2",
    "Lưu ý bảo mật"
  ]
}
```

**Supported Operations:**
- `write_file` - Tạo/ghi đè file
- `replace_regex` - Thay thế theo regex
- `append` - Thêm nội dung cuối file  
- `delete` - Xóa file

---

## 🗂️ CẤU TRÚC THƯ MỤC

```
deepseek/
├── guardian/
│   └── .artifacts/
│       ├── backup/          # Auto-backup files
│       │   └── 20250901_221234/
│       └── patches/         # Patch history
│           ├── patch_20250901_221234.json
│           └── last_patches.json
├── knowledge/
│   └── import_map_ext.json  # Knowledge base
└── auto/
    └── vn_copilot.py       # Main coach file
```

---

## 🛡️ AN TOÀN & KIỂM SOÁT

### Tự động backup
- **Mọi thay đổi** đều được backup vào `.artifacts/backup/`
- **Timestamp**: `20250901_221234` format
- **Khôi phục**: Copy từ backup folder

### Dry-run mặc định  
- **Mặc định**: Chỉ hiển thị diff, không ghi file
- **Force mode**: Thêm `!force` để ghi thật
- **Review**: Luôn xem diff trước khi force

### Khoanh vùng repository
- **Chỉ hoạt động** trong git repository  
- **Không sửa** file ngoài repo root
- **PII masking** trong logs

### Quality gates
- **Tự động chạy** `ruff`, `mypy`, `pytest` sau khi patch
- **Exit codes** được kiểm tra
- **Rollback** nếu test fail (tuỳ chọn)

---

## 📚 HỌC VÀ NHẬN THỨC

### Thu thập knowledge
```bash
🇻🇳> học từ deepseek/
🇻🇳> học từ zeta_vn/app/
🇻🇳> học từ .
```

### Context awareness
- **Tự động scan** `.py`, `.md`, `.json`, `.yml` files
- **Preview content** (3KB per file)  
- **Hash fingerprinting** để tránh duplicate
- **Knowledge base** trong `deepseek/knowledge/import_map_ext.json`

### Continuous learning
- **Mỗi lần patch** → update knowledge
- **Project structure** → context cho AI
- **Coding patterns** → improve suggestions

---

## 🔍 EXAMPLES THỰC TẾ

### Workflow hoàn chỉnh:
```bash
# 1. Học về dự án
python deepseek/auto/vn_copilot.py -c "học từ deepseek/"

# 2. Phân tích tổng thể  
python deepseek/auto/vn_copilot.py -c "phân tích dự án zeta_vn"

# 3. Giảng dạy theo yêu cầu
python deepseek/auto/vn_copilot.py -c "giảng dạy clean architecture trên deepseek/auto/"

# 4. Đề xuất cải thiện
python deepseek/auto/vn_copilot.py -c "đề xuất vá cải thiện typing cho deepseek/auto/"

# 5. Review patches (dry-run)
python deepseek/auto/vn_copilot.py -c "thực thi vá"

# 6. Apply (nếu OK)
python deepseek/auto/vn_copilot.py -c "thực thi vá !force"

# 7. Quality check
python deepseek/auto/vn_copilot.py -c "chạy ruff"
python deepseek/auto/vn_copilot.py -c "chạy mypy"
```

### File operations:
```bash
# Tạo file
python deepseek/auto/vn_copilot.py -c "tạo file demo.py"

# Xem file  
python deepseek/auto/vn_copilot.py -c "xem file deepseek/auto/vn_copilot.py"

# Backup files
python deepseek/auto/vn_copilot.py -c "backup deepseek/auto/vn_copilot.py,demo.py"

# Scan project
python deepseek/auto/vn_copilot.py -c "quét dự án"
```

---

## 🐛 XỬ LÝ LỖI

### API connection issues:
```bash
# Check config
python demo_deepseek_coach.py

# Verify key
echo $DEEPSEEK_API_KEY  # Linux/macOS
echo $env:DEEPSEEK_API_KEY  # Windows
```

### Patch failures:
```bash
# Check last patches
cat deepseek/guardian/.artifacts/patches/last_patches.json

# Restore from backup
cp deepseek/guardian/.artifacts/backup/20250901_221234/path/file.py path/file.py
```

### Permission issues:
```bash
# Ensure write permissions
chmod +w deepseek/guardian/.artifacts/
```

---

## 🔗 TÍCH HỢP VỚI WORKFLOWS

### VS Code tasks.json:
```json
{
  "label": "VN Copilot: Analyze Project",
  "type": "shell", 
  "command": "python deepseek/auto/vn_copilot.py -c 'phân tích dự án zeta_vn'"
}
```

### Git hooks:
```bash
# pre-commit
python deepseek/auto/vn_copilot.py -c "chạy ruff"
```

### CI/CD:
```bash
# Quality gate
python deepseek/auto/vn_copilot.py -c "đề xuất vá quality check"
```

---

## 🚧 ROADMAP TIẾP THEO

1. **RAG cải tiến** - Vector embeddings với FAISS
2. **Streaming responses** - WebSocket cho UI tương tác  
3. **Multi-model support** - Claude, GPT-4, Gemini
4. **Custom rules engine** - Domain-specific patches
5. **Team collaboration** - Shared knowledge base
6. **IDE integration** - VS Code extension

---

## 📞 HỖ TRỢ

- **File config**: `deepseek/auto/vn_copilot.py` (1 file duy nhất)
- **Demo**: `python demo_deepseek_coach.py`  
- **Test**: `python test_deepseek_coach.py`
- **Logs**: `deepseek/guardian/.artifacts/`

**🎯 VN Copilot - Thầy Huấn luyện DeepSeek sẵn sàng phục vụ!**
