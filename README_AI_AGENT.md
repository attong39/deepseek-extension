# DeepSeek Extension with AI Agent

VS Code extension tích hợp AI Agent thông minh với DeepSeek R1 model qua Ollama và Python CLI bridge.

## 🚀 Tính năng chính

### AI Agent Hybrid Architecture
- **Frontend TypeScript**: VS Code extension với UI/UX tương tác
- **Backend Python CLI**: Logic AI phức tạp qua `deepseek/main_cli.py`
- **Ollama Integration**: DeepSeek R1 model chạy local
- **Intelligent Task Inference**: Tự động nhận dạng loại task từ prompt

### File Operations
- `upsert_file`: Tạo/cập nhật file an toàn
- `append`: Thêm nội dung vào cuối file
- `replace`: Thay thế theo regex pattern
- `insert`: Chèn nội dung tại vị trí cụ thể
- `optimize_imports`: Tự động sắp xếp import statements

### Task Types
- **Review**: Phân tích code, phát hiện issues
- **Debug**: Chuẩn đoán và sửa lỗi
- **Optimize**: Tối ưu imports, loại bỏ duplicate
- **Test**: Sinh unit tests cho functions/classes  
- **Document**: Tạo documentation/docstrings

## 📋 Prerequisites

1. **Ollama** với DeepSeek R1 model:
   ```bash
   # Cài đặt Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull DeepSeek R1 model
   ollama pull deepseek-r1:latest
   
   # Start Ollama server
   ollama serve
   ```

2. **Python CLI** tại `deepseek/main_cli.py` với `--ai-agent` support

3. **VS Code** 1.96.0+

## 🛠️ Installation

1. Clone repository:
   ```bash
   git clone <repo-url>
   cd deepseek-extension
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Compile TypeScript:
   ```bash
   npm run compile
   ```

4. Install extension:
   - Mở VS Code
   - `Ctrl+Shift+P` → "Extensions: Install from VSIX"
   - Chọn file `.vsix` đã build

## 🎯 Cách sử dụng

### Command Palette
`Ctrl+Shift+P` và tìm:
- `AI Agent: Interactive Mode` - Nhập prompt tự do
- `AI Agent: Review Code` - Review file hiện tại
- `AI Agent: Debug Code` - Debug file hiện tại  
- `AI Agent: Optimize Code` - Tối ưu file hiện tại
- `AI Agent: Generate Tests` - Sinh tests cho file hiện tại
- `AI Agent: Generate Documentation` - Sinh docs cho file hiện tại

### Interactive Mode Examples
```
"review all TypeScript files"
"optimize imports in current file"  
"debug this Python function"
"generate unit tests for class UserService"
"add documentation for all public methods"
```

### Python CLI Delegation
Với Python files, AI Agent tự động delegate qua Python CLI:
```bash
python deepseek/main_cli.py --ai-agent --request "optimize imports" --files "src/utils.py,src/models.py"
```

## 🏗️ Architecture

```
VS Code Extension (TypeScript)
├── AIAgent class
│   ├── OllamaService - Giao tiếp với DeepSeek R1
│   ├── PythonCLIBridge - Delegate Python tasks  
│   ├── Task Inference - Nhận dạng task type
│   └── File Operations - An toàn file manipulation
└── Extension.ts - Command registration & activation

Python CLI Backend
├── main_cli.py --ai-agent mode
├── AIAgentUseCase integration
└── Enhanced argument parsing
```

## 🔧 Configuration

### Ollama Settings
```json
{
  "deepseek.ollama.baseUrl": "http://127.0.0.1:11434",
  "deepseek.ollama.model": "deepseek-r1:latest"
}
```

### Python CLI Path
Extension tự động tìm `deepseek/main_cli.py` trong:
- `{workspace}/deepseek/main_cli.py`
- `{workspace}/../deepseek/main_cli.py`  
- `{workspace}/../../deepseek/main_cli.py`

## 🛡️ Safety Features

- **Path Validation**: Chặn `..` và path traversal
- **Workspace Restriction**: Chỉ thao tác trong workspace
- **Backup Mechanism**: Tự động backup trước khi sửa
- **Error Recovery**: Graceful handling of failures
- **Content Size Limits**: Giới hạn context để tránh overflow

## 🧪 Development

### Build Extension
```bash
npm run compile
npm run package  # Tạo .vsix file
```

### Debug Mode
1. Mở VS Code
2. `F5` để start debug session
3. Test commands trong Extension Development Host

### Testing
```bash
npm test
```

## 📊 Output Channels

- **DeepSeek Agent**: Main AI Agent logs
- **Python CLI Bridge**: Python delegation logs
- **Ollama Communication**: Model interaction logs

## 🐛 Troubleshooting

### Ollama Connection Failed
```bash
# Kiểm tra Ollama server
curl http://127.0.0.1:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

### Python CLI Not Found
```bash
# Verify Python CLI path
python deepseek/main_cli.py --help

# Check --ai-agent support
python deepseek/main_cli.py --ai-agent --help
```

### TypeScript Compilation Errors
```bash
# Clean và rebuild
rm -rf out/
npm run compile
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM runtime
- [DeepSeek](https://deepseek.com/) - R1 reasoning model
- [VS Code API](https://code.visualstudio.com/api) - Extension framework
