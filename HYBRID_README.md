# DeepSeek Hybrid AI Agent

## 🎯 Tổng quan

Hybrid AI Agent kết hợp sức mạnh của Python CLI DeepSeek và VS Code Extension để tạo ra workflow AI tự động hoàn chỉnh.

## 🏗️ Kiến trúc Hybrid

```
┌─────────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   VS Code Extension │◄──►│  Python CLI Bridge   │◄──►│   DeepSeek Python   │
│  (TypeScript Frontend)  │    │   (Communication)    │    │    CLI Backend      │
├─────────────────────┤    ├──────────────────────┤    ├─────────────────────┤
│ • Rich UI/UX        │    │ • Command Translation│    │ • AI Agent Use Case │
│ • File Operations   │    │ • Process Management │    │ • Service Logic     │
│ • Context Collection│    │ • Error Handling     │    │ • Ollama Integration│
│ • Action Application│    │ • Output Parsing     │    │ • File Safety       │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
            │                         │                         │
            ▼                         ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DeepSeek R1 via Ollama                           │
│                      http://127.0.0.1:11434/api/chat                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Tính năng chính

### TypeScript Frontend (VS Code Extension)
- **Interactive AI Agent**: Prompt tự nhiên cho mọi task
- **Quick Actions**: Review/Debug/Optimize/Test/Document file hiện tại
- **Workspace Operations**: Xử lý toàn bộ workspace
- **Continuous Mode**: Chạy liên tục cho đến khi không còn thay đổi
- **Smart File Selection**: Tự động chọn files liên quan theo task type
- **Rich UI**: Command palette, context menu, keyboard shortcuts

### Python Backend (AI Agent CLI)
- **Powerful AI Logic**: Service layer thuần với business logic
- **File Safety**: Backup/rollback mechanisms 
- **Clean Architecture**: Use cases/Services separation
- **Comprehensive Testing**: Unit/Integration tests
- **Error Handling**: Robust error recovery

### Hybrid Intelligence
- **Task Delegation**: TypeScript ưu tiên Python cho Python files
- **Action Types**: 
  - File operations (upsert, append, replace, insert)
  - Import optimization 
  - Python CLI tasks (delegate to backend)
- **Context Aware**: Thu thập context thông minh theo task type

## 🛠️ Cài đặt & Sử dụng

### Prerequisites
```bash
# 1. Cài đặt Ollama và DeepSeek R1
ollama pull deepseek-r1:latest

# 2. Kiểm tra Python DeepSeek CLI
cd /path/to/deepseek
python main_cli.py  # Phải hiển thị option "11" cho AI Agent

# 3. Build VS Code Extension
cd /path/to/deepseek-extension
npm install
npm run compile
```

### Extension Commands

| Command                                    | Shortcut                    | Description              |
| ------------------------------------------ | --------------------------- | ------------------------ |
| `DeepSeek: Interactive AI Agent`           | `Ctrl+Shift+D Ctrl+Shift+I` | Nhập prompt tự nhiên     |
| `DeepSeek: Review Active File`             | `Ctrl+Shift+D Ctrl+Shift+R` | Review file hiện tại     |
| `DeepSeek: Optimize Active File`           | `Ctrl+Shift+D Ctrl+Shift+O` | Optimize file hiện tại   |
| `DeepSeek: Debug Active File`              | -                           | Debug file hiện tại      |
| `DeepSeek: Generate Tests for Active File` | -                           | Sinh tests               |
| `DeepSeek: Document Active File`           | -                           | Sinh documentation       |
| `DeepSeek: Continuous Code Review`         | -                           | Review liên tục          |
| `DeepSeek: Review Workspace`               | -                           | Review toàn bộ workspace |
| `DeepSeek: Show AI Agent Status`           | -                           | Hiển thị trạng thái      |
| `DeepSeek: Configure AI Agent`             | -                           | Cấu hình và kiểm tra     |

## 📝 Workflow Examples

### 1. Interactive Mode
```
1. Ctrl+Shift+P → "DeepSeek: Interactive AI Agent"
2. Nhập: "review Python files và fix import issues"
3. AI Agent sẽ:
   - Phân tích task type: 'review'
   - Thu thập context từ Python files
   - Delegate Python files cho Python CLI backend
   - Apply changes qua TypeScript frontend
```

### 2. Quick File Review
```
1. Mở file Python/TypeScript
2. Ctrl+Shift+D Ctrl+Shift+R (hoặc right-click → DeepSeek Review)
3. AI Agent review và suggest improvements
```

### 3. Continuous Optimization
```
1. Ctrl+Shift+P → "DeepSeek: Continuous Optimization"
2. AI Agent chạy multiple iterations cho đến khi stable
3. Hiển thị summary của mọi thay đổi
```

## 🔧 Configuration

### Ollama Setup
```bash
# Kiểm tra Ollama
curl http://127.0.0.1:11434/api/tags

# Response phải có deepseek-r1:latest
```

### Python CLI Bridge
Extension tự động tìm DeepSeek CLI tại:
- `${workspaceRoot}/deepseek/main_cli.py`
- `${workspaceRoot}/../deepseek/main_cli.py`
- `${workspaceRoot}/../../deepseek/main_cli.py`

### VS Code Settings
```json
{
  "deepseek.aiAgent.autoActivate": true,
  "deepseek.aiAgent.maxContextSize": 40000,
  "deepseek.aiAgent.ollama.baseUrl": "http://127.0.0.1:11434",
  "deepseek.aiAgent.ollama.model": "deepseek-r1:latest"
}
```

## 🎯 Action Types

### File Actions (TypeScript Frontend)
```typescript
type FileAction = 
  | { type: 'upsert_file', path: string, content: string }
  | { type: 'append', path: string, content: string }
  | { type: 'replace', path: string, pattern: string, replacement: string }
  | { type: 'insert', path: string, anchor: string, position: 'above'|'below', content: string }
  | { type: 'optimize_imports', path: string, language: 'ts'|'py' }
```

### Python Tasks (Backend Delegation)
```typescript
type PythonTaskAction = {
  type: 'python_cli_task',
  request: string,     // Natural language request
  files: string[]      // Target files
}
```

## 📊 Performance & Safety

### Safety Mechanisms
- **Path Validation**: Reject `..` traversal
- **File Backups**: Python CLI có backup/rollback
- **Error Recovery**: Comprehensive error handling
- **Context Limits**: Max 40KB context để tránh overflow

### Performance Optimizations
- **Smart File Selection**: Chỉ load files liên quan
- **Batch Operations**: Combine multiple actions
- **Async Processing**: Non-blocking operations
- **Connection Pooling**: Reuse Ollama connections

## 🧪 Testing

### Extension Testing
```bash
cd deepseek-extension
npm test
```

### Python CLI Testing
```bash
cd deepseek
python -m pytest tests/test_ai_agent.py -v
```

### Integration Testing
```bash
# Test Python CLI từ extension
code deepseek-extension
# Open Command Palette → "DeepSeek: Configure AI Agent" → "Verify Python CLI"
```

## 🚨 Troubleshooting

### Common Issues

1. **"AI Agent not initialized"**
   - Kiểm tra Ollama đang chạy: `ollama list`
   - Verify DeepSeek CLI path trong Output channel

2. **"Python CLI failed"**
   - Chạy trực tiếp: `python deepseek/main_cli.py`
   - Kiểm tra option "11" có sẵn không

3. **"Ollama connection failed"**
   - Khởi động Ollama: `ollama serve`
   - Pull model: `ollama pull deepseek-r1:latest`

4. **Extension not activating**
   - Check VS Code Developer Console (Ctrl+Shift+I)
   - Look for activation errors

### Debug Mode
```bash
# Enable verbose logging
export DEEPSEEK_DEBUG=1

# VS Code Extension Development Host
code --extensionDevelopmentPath=/path/to/deepseek-extension
```

## 🎉 Success Indicators

✅ **Extension activated successfully**
✅ **Python CLI Bridge: Ready**  
✅ **Ollama Service: Connected**
✅ **File Operations: Ready**
✅ **AI Agent commands appear in Command Palette**
✅ **Context menu items available**
✅ **Keyboard shortcuts working**

## 🔮 Roadmap

- [ ] **WebSocket connection** cho real-time communication
- [ ] **Multi-model support** (CodeLlama, Claude, etc.)
- [ ] **Project-aware context** (package.json, requirements.txt)
- [ ] **Diff preview** trước khi apply changes
- [ ] **Undo/Redo** cho AI operations
- [ ] **Batch file processing** với progress bars
- [ ] **Custom prompts** và templates
- [ ] **Team sharing** của AI configurations

---

**💡 Tips**: Bắt đầu với `DeepSeek: Interactive AI Agent` để làm quen với workflow, sau đó sử dụng quick commands cho productivity cao hơn.
