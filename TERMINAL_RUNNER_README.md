# DeepSeek R1 Agent - Terminal Runner

🚀 **Chạy DeepSeek R1 AI Agent trực tiếp từ terminal mà không cần VS Code**

## ✨ Tính năng

- 🤖 **Chat với AI**: Trò chuyện tự nhiên với DeepSeek R1
- 🔍 **Code Review**: Phân tích và review code chất lượng
- ⚡ **Code Optimization**: Tối ưu performance và best practices
- 🧪 **Test Generation**: Tự động tạo unit tests
- 🌐 **Cross-platform**: Hoạt động trên Windows, Linux, macOS
- 📦 **Auto Setup**: Script setup tự động tất cả dependencies

## 🚀 Quick Start

### 1. Setup tự động (Khuyến nghị)

```bash
# Linux/macOS
chmod +x setup.sh
./setup.sh

# Windows (PowerShell)
.\setup.ps1
```

### 2. Setup thủ công

```bash
# Cài đặt Python dependencies
pip install ollama aiofiles

# Cài đặt Ollama (nếu chưa có)
# Windows: Download từ https://ollama.ai/download
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
# macOS: brew install ollama

# Khởi động Ollama và tải model
ollama serve &
ollama pull deepseek-r1:latest

# Cài đặt Node.js dependencies (cho TypeScript)
npm install --save-dev typescript @types/node eslint concurrently
```

## 📖 Usage

### Chat với AI

```bash
python run_deepseek_agent.py chat "Hello, how are you?"
python run_deepseek_agent.py chat --message "Explain Python async/await"
```

### Code Review

```bash
python run_deepseek_agent.py review src/extension.ts
python run_deepseek_agent.py review --file src/aiAgent.ts
```

### Code Optimization

```bash
python run_deepseek_agent.py optimize src/extension.ts
python run_deepseek_agent.py optimize --file src/aiAgent.ts
```

### Test Generation

```bash
python run_deepseek_agent.py test src/extension.ts
python run_deepseek_agent.py test --file src/aiAgent.ts
```

### Custom Model/URL

```bash
python run_deepseek_agent.py chat --model "llama2" --url "http://localhost:11435" "Hello"
```

## 🛠️ Development Workflow

### Với VS Code Extension

```bash
# Chạy development environment
python scripts/deepseek_start_assistant.py

# Hoặc dùng batch file (Windows only)
./start-dev.bat
```

### Quality Gates

```bash
# Lint và format
npm run lint
npm run compile

# Test extension
npm run test

# Package extension
npm run package
```

### Với Python Backend (zeta_vn)

```bash
# Chạy quality gates
uv run ruff check .
uv run mypy . --strict
uv run pytest --cov=core .
uv run bandit -r .
uv run pip-audit

# Chạy server
uv run uvicorn zeta_vn.app.main_production:app --host 0.0.0.0 --port 8000 --reload
```

## 📋 Commands Reference

| Command    | Description         | Example                 |
| ---------- | ------------------- | ----------------------- |
| `chat`     | Chat với AI agent   | `chat "Hello world"`    |
| `review`   | Review code file    | `review src/main.py`    |
| `optimize` | Optimize code       | `optimize src/utils.py` |
| `test`     | Generate unit tests | `test src/service.py`   |
| `setup`    | Kiểm tra setup      | `setup`                 |

## ⚙️ Configuration

Tạo file `.deepseek/config.json`:

```json
{
  "ollamaBaseUrl": "http://127.0.0.1:11434",
  "model": "deepseek-r1:latest",
  "maxTokens": 4096,
  "temperature": 0.7,
  "timeout": 300
}
```

## 🔧 Troubleshooting

### Ollama Issues

```bash
# Kiểm tra Ollama status
ollama list
ollama ps

# Restart Ollama server
pkill ollama
ollama serve

# Pull model lại
ollama pull deepseek-r1:latest --force
```

### Python Issues

```bash
# Upgrade pip và dependencies
pip install --upgrade pip
pip install --upgrade ollama aiofiles

# Check Python version
python --version
```

### Network Issues

```bash
# Test Ollama API
curl http://127.0.0.1:11434/api/tags

# Check port availability
netstat -an | grep 11434
```

## 📊 Performance Tips

- **Model Selection**: `deepseek-r1:latest` cho best quality
- **Context Window**: Giữ prompt dưới 4096 tokens
- **Batch Processing**: Xử lý nhiều files cùng lúc
- **Caching**: Ollama tự động cache responses

## 🔒 Security

- Agent chỉ đọc files, không modify trừ khi explicitly yêu cầu
- Không expose sensitive data trong prompts
- Sử dụng virtual environment cho Python
- Regular security audits với bandit

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Tạo Pull Request

## 📝 License

MIT License - Xem file `LICENSE` để biết thêm chi tiết.

## 🙏 Acknowledgments

- [DeepSeek](https://github.com/deepseek-ai) cho model R1
- [Ollama](https://ollama.ai) cho local AI inference
- [VS Code](https://code.visualstudio.com) cho extension framework

---

**Happy AI-assisted coding!** 🤖✨
