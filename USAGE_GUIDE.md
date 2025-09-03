# 🚀 AI Agent Extension - Hướng dẫn chạy thực tế

## ✅ Trạng thái hiện tại:
- ✅ Ollama server đang chạy
- ✅ DeepSeek R1 model available  
- ✅ Extension compiled thành công
- ✅ All commands registered

## 🎯 Cách chạy thực tế:

### Bước 1: Launch Extension Development Host
```bash
# Trong VS Code (folder deepseek-extension):
1. Mở VS Code
2. Nhấn F5 (hoặc Ctrl+F5)
3. VS Code sẽ mở Extension Development Host window mới
```

### Bước 2: Test AI Agent Commands  
```
Trong Extension Development Host:
1. Ctrl+Shift+P để mở Command Palette
2. Gõ "AI Agent" để xem available commands:
   • AI Agent: Interactive Mode
   • AI Agent: Review Code  
   • AI Agent: Debug Code
   • AI Agent: Optimize Code
   • AI Agent: Check Status
```

### Bước 3: Test với file mẫu
```
1. Mở file: src/test-sample.ts (có sẵn nhiều issues)
2. Chọn "AI Agent: Optimize Code"  
3. Check Output channel "DeepSeek Agent" để xem kết quả
```

### Bước 4: Test Interactive Mode
```
1. Chọn "AI Agent: Interactive Mode"
2. Nhập prompt: "optimize imports and fix code issues"
3. AI sẽ phân tích và thực hiện changes
```

## 🧪 Test Cases:

### Test 1: Check Status
- Command: `AI Agent: Check Status`
- Expected: "✅ AI Agent ready! Ollama connected."

### Test 2: Optimize Code
- File: `src/test-sample.ts`
- Command: `AI Agent: Optimize Code`
- Expected: Fix `==` → `===`, remove unused vars, optimize loops

### Test 3: Interactive Mode  
- Prompt: "review code and suggest improvements"
- Expected: Detailed analysis và suggestions

## 📊 Monitoring:
- Output Channel: "DeepSeek Agent" - xem AI responses
- Developer Console: F12 để debug extension
- Terminal: Check Ollama logs

## 🔧 Troubleshooting:
- Nếu timeout: DeepSeek R1 model lớn, cần thời gian
- Nếu connection error: Check `ollama serve` đang chạy
- Nếu no response: Check Output channel cho error details

## 🎉 Expected Results:
AI Agent sẽ:
1. Analyze code qua DeepSeek R1
2. Generate JSON plan với specific actions
3. Apply changes safely với backup
4. Show results trong Output channel

**Ready to test! Nhấn F5 trong VS Code để bắt đầu! 🚀**
