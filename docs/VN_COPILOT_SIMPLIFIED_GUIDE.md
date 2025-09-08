# 🇻🇳 VN Copilot Simplified - Hướng dẫn sử dụng

## Tổng quan

VN Copilot Simplified là phiên bản đơn giản của "Thầy Huấn luyện DeepSeek" - một trợ lý AI lập trình hỗ trợ tiếng Việt tự nhiên.

## Tính năng chính

### ✅ Hoạt động ổn định
- ✅ Giao diện tiếng Việt tự nhiên
- ✅ Không cần cấu hình phức tạp  
- ✅ Single-file, chỉ dùng Python stdlib
- ✅ Backup tự động
- ✅ PII masking an toàn

### 📚 Chức năng hiện tại
- **Quét dự án**: Phân tích cấu trúc project
- **Thu thập knowledge**: Học từ mã nguồn
- **Quality checks**: Chạy ruff, mypy, pytest
- **Xem file**: Hiển thị nội dung với mask PII
- **Learning system**: Lưu knowledge về project

## Cách sử dụng

### 1. Chạy single command
```bash
python deepseek/auto/vn_copilot_simple.py -c "help"
python deepseek/auto/vn_copilot_simple.py -c "quét dự án"
python deepseek/auto/vn_copilot_simple.py -c "học từ deepseek/auto"
```

### 2. Chạy interactive mode
```bash
python deepseek/auto/vn_copilot_simple.py
```

### 3. Demo đầy đủ
```bash
python deepseek/auto/demo_vn_copilot_simple.py
```

## Lệnh được hỗ trợ

| Lệnh tiếng Việt   | Mô tả                  | Ví dụ                                         |
| ----------------- | ---------------------- | --------------------------------------------- |
| `help`            | Hiển thị trợ giúp      | `help`                                        |
| `quét dự án`      | Quét toàn bộ project   | `quét dự án`                                  |
| `chạy <tool>`     | Chạy quality tools     | `chạy ruff`                                   |
| `xem file <path>` | Hiển thị nội dung file | `xem file deepseek/auto/vn_copilot_simple.py` |
| `học từ <path>`   | Thu thập knowledge     | `học từ deepseek/auto`                        |
| `thoát`           | Thoát chương trình     | `thoát`                                       |

## Đường dẫn quan trọng

```
E:\zeta\
├── deepseek/auto/
│   ├── vn_copilot_simple.py     # Script chính
│   └── demo_vn_copilot_simple.py # Demo
├── deepseek/guardian/.artifacts/ # Kết quả scan, backup
└── deepseek/knowledge/           # Knowledge học được
```

## Quality Tools hỗ trợ

- **ruff**: Code linting & formatting
- **mypy**: Type checking
- **pytest**: Unit testing  
- **bandit**: Security scanning
- **pip-audit**: Dependency vulnerabilities

## An toàn & Bảo mật

- ✅ **PII Masking**: Tự động ẩn email, số dài
- ✅ **Backup tự động**: Lưu backup trước khi thay đổi
- ✅ **Repository scope**: Chỉ hoạt động trong project
- ✅ **Dry-run mặc định**: An toàn cho production

## Kết quả output

### Scan Report
```json
{
  "repo": "E:\\zeta",
  "total_files": 106514,
  "ext_stats": {
    ".py": 1234,
    ".md": 567,
    ".json": 234
  },
  "time": "20250901_221532"
}
```

### Knowledge Learning
```json
{
  "updated_at": "20250901_221532", 
  "items": [
    {
      "path": "deepseek/auto/vn_copilot_simple.py",
      "hash": "abc123def456",
      "size": 15678,
      "preview": "# -*- coding: utf-8 -*-..."
    }
  ]
}
```

## Khắc phục sự cố

### Lỗi Unicode
```bash
# Đã được xử lý tự động với _normalize()
```

### Lỗi Import
```bash
# Chỉ dùng Python stdlib - không cần install gì thêm
```

### Lỗi Path
```bash
# Kiểm tra đường dẫn tương đối từ repo root E:\zeta
```

## So sánh với phiên bản đầy đủ

| Tính năng       | Simplified | Full Version |
| --------------- | ---------- | ------------ |
| DeepSeek API    | ❌          | ✅            |
| JSON Patch      | ❌          | ✅            |
| Vietnamese AI   | ❌          | ✅            |
| Basic Commands  | ✅          | ✅            |
| Quality Tools   | ✅          | ✅            |
| Learning System | ✅          | ✅            |
| Stability       | ✅          | ⚠️            |

## Nâng cấp lên Full Version

Để sử dụng tính năng DeepSeek AI đầy đủ:

1. **Cấu hình API key**:
```bash
export DEEPSEEK_API_KEY="your-api-key"
```

2. **Sử dụng vn_copilot.py** (khi đã fix lỗi)

## Kết luận

VN Copilot Simplified cung cấp:
- ✅ **Ổn định**: Không lỗi runtime
- ✅ **Tiếng Việt**: Giao diện tự nhiên  
- ✅ **Hữu ích**: Quality tools + learning
- ✅ **An toàn**: PII masking + backup

Phù hợp cho việc sử dụng hàng ngày trong development workflow.
