# 🎯 Quick Start Guide - DeepSeek R1 với VS Code

## ⚡ Setup nhanh (5 phút)

### 1. Cài đặt dependencies
```powershell
# Chạy script setup tự động
.\scripts\setup-complete.ps1
```

### 2. Kiểm tra Ollama
```powershell
# Test API
.\scripts\test-ollama-api.ps1

# Hoặc manual
curl http://127.0.0.1:11434/api/tags
```

### 3. Chạy VS Code Extension
```powershell
# Development mode
.\scripts\run_deepseek_r1.ps1 -DevHost -QuickReview

# Production mode  
.\scripts\run_deepseek_r1.ps1 -Model "gpt-oss:20b"
```

---

## 🎮 Commands có sẵn

| Command                         | Mô tả                             | Shortcut       |
| ------------------------------- | --------------------------------- | -------------- |
| `DeepSeek: Review Current File` | Review file đang mở               | `Ctrl+Shift+P` |
| `DeepSeek: Run Task`            | Chọn task (review/debug/optimize) | -              |
| `DeepSeek: Continuous Mode`     | Chạy liên tục nhiều vòng          | -              |
| `DeepSeek: Choose Model`        | Đổi model Ollama                  | -              |
| `DeepSeek: Health Check`        | Kiểm tra Ollama service           | -              |

---

## 🔧 CLI Usage

```powershell
# Review Python file
.\cli\deepseek-agent.ps1 review "src\app.py" -Verbose

# Debug JavaScript với model khác
.\cli\deepseek-agent.ps1 debug "src\bug.js" -Model "deepseek-r1:latest"

# Optimize với streaming
.\cli\deepseek-agent.ps1 optimize "src\slow.py" -Stream
```

---

## 📊 Models khuyến nghị

| Model                | Size  | Use Case                          | VRAM  |
| -------------------- | ----- | --------------------------------- | ----- |
| `gpt-oss:20b`        | ~20GB | **Default**, balanced performance | 16GB+ |
| `deepseek-r1:latest` | ~14GB | Code-specific tasks               | 12GB+ |
| `deepseek-r1:8b`     | ~8GB  | Low-resource machines             | 8GB+  |

---

## ⚙️ Cấu hình VS Code Settings

```json
{
  "deepseek.agent.model": "gpt-oss:20b",
  "deepseek.agent.baseUrl": "http://127.0.0.1:11434", 
  "deepseek.agent.timeout": 120000
}
```

---

## 🐛 Troubleshooting nhanh

| Lỗi                             | Fix                             |
| ------------------------------- | ------------------------------- |
| `Ollama service không khả dụng` | `ollama serve`                  |
| `Model not found`               | `ollama pull gpt-oss:20b`       |
| `Out of VRAM`                   | `OLLAMA_NUM_GPU=0 ollama serve` |
| `Extension commands không hiện` | Reload VS Code                  |

---

## 🚀 Test nhanh

1. **Health check**: `DeepSeek: Health Check` → ✅
2. **Review file**: Mở file Python → `DeepSeek: Review Current File`  
3. **CLI test**: `.\cli\deepseek-agent.ps1 review run_deepseek_agent.py`

🎉 **Hoàn thành!** Extension đã sẵn sàng với model **gpt-oss:20b** mặc định!
