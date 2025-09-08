# Zeta AI Agent - User Guide 📖

> Comprehensive user manual for Vietnamese-speaking AI coding assistant

## 📚 Table of Contents

1. [Getting Started](#-getting-started)
2. [Extension Features](#-extension-features)
3. [Model Selection](#-model-selection)
4. [Vietnamese Language Support](#-vietnamese-language-support)
5. [Chat Interface](#-chat-interface)
6. [Code Analysis](#-code-analysis)
7. [Performance Optimization](#-performance-optimization)
8. [Troubleshooting](#-troubleshooting)
9. [Best Practices](#-best-practices)

## 🚀 Getting Started

### Initial Setup

1. **Install Prerequisites**
   ```bash
   # Install Ollama
   winget install Ollama.Ollama  # Windows
   brew install ollama           # macOS
   
   # Start Ollama service
   ollama serve
   ```

2. **Deploy AI Models**
   ```bash
   # Vietnamese-optimized models (Required)
   ollama pull attong39/zeta      # Best Vietnamese quality
   ollama pull zeta-py-teacher    # Python specialist
   
   # Supporting models (Recommended)
   ollama pull starcoder          # Fast responses
   ollama pull codellama:13b      # Complex reasoning
   ollama pull deepseek-coder     # Code optimization
   ```

3. **Install Extension**
   - Download `zeta-ai-agent-1.0.0.vsix`
   - VS Code → Extensions → Install from VSIX
   - Restart VS Code

4. **First Configuration**
   ```
   Ctrl+Shift+P → "Zeta AI: Configure"
   
   ✅ Select primary model: attong39/zeta
   ✅ Enable Vietnamese mode: Yes
   ✅ Set response timeout: 30 seconds
   ✅ Enable monitoring: Yes
   ```

### Quick Verification

```typescript
// Create test file: test.ts
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Right-click → "Zeta AI: Review Code"
// Expected: Vietnamese commentary about function quality
```

## 🎯 Extension Features

### Command Palette Actions

| Command | Shortcut | Description |
|---------|----------|-------------|
| `Zeta AI: Start Chat` | `Ctrl+Shift+C` | Open chat interface |
| `Zeta AI: Review Code` | `Ctrl+Alt+R` | Analyze selected code |
| `Zeta AI: Debug Code` | `Ctrl+Alt+D` | Debug assistance |
| `Zeta AI: Optimize Code` | `Ctrl+Alt+O` | Performance suggestions |
| `Zeta AI: Add Comments` | `Ctrl+Alt+M` | Vietnamese comments |
| `Zeta AI: Explain Code` | `Ctrl+Alt+E` | Code explanation |

### Context Menu Options

```
Right-click on code:
├── Zeta AI: Review Code ⭐
├── Zeta AI: Debug Issue 🐛
├── Zeta AI: Optimize Performance ⚡
├── Zeta AI: Add Vietnamese Comments 🇻🇳
├── Zeta AI: Explain Logic 💡
└── Zeta AI: Suggest Improvements 🚀
```

### Status Bar Integration

```
Bottom status bar shows:
[🤖 Zeta AI] [Model: attong39/zeta] [Status: Ready] [Latency: 3.8s]
```

## 🧠 Model Selection

### Automatic Model Routing

The extension intelligently selects models based on request complexity:

```typescript
// Simple query → starcoder (fast)
"How to declare a variable?"

// Medium complexity → zeta-py-teacher (balanced)
"Explain this function's logic"

// Complex reasoning → codellama:13b (thorough)
"Refactor this class for better architecture"

// Vietnamese content → attong39/zeta (best quality)
"Giải thích đoạn code này bằng tiếng Việt"
```

### Manual Model Selection

```json
// VS Code Settings
{
  "zeta.defaultModel": "attong39/zeta",
  "zeta.speedModel": "starcoder", 
  "zeta.complexModel": "codellama:13b-instruct",
  "zeta.vietnameseModel": "attong39/zeta"
}
```

### Model Performance Comparison

| Use Case | Recommended Model | Avg Speed | Quality |
|----------|------------------|-----------|---------|
| Quick questions | `starcoder` | 4.9s | 9/10 |
| Code review | `zeta-py-teacher` | 3.8s | 9/10 |
| Complex debugging | `codellama:13b` | 6.2s | 8/10 |
| Vietnamese content | `attong39/zeta` | 8.4s | 10/10 |
| Performance optimization | `deepseek-coder` | 6.8s | 8/10 |

## 🇻🇳 Vietnamese Language Support

### Native Vietnamese Interaction

```python
# Example interaction
User: "Làm thế nào để tối ưu hóa đoạn code này?"

AI: """
Tôi sẽ phân tích đoạn code và đưa ra các gợi ý tối ưu:

1. **Hiệu suất**: Sử dụng list comprehension thay vì loop
2. **Bộ nhớ**: Tránh tạo ra các bản copy không cần thiết  
3. **Đọc hiểu**: Thêm docstring và type hints

Đây là phiên bản được tối ưu:
```python
def process_items(items: List[str]) -> List[str]:
    \"\"\"Xử lý danh sách items và trả về kết quả đã được format\"\"\"
    return [item.strip().upper() for item in items if item.strip()]
```
"""
```

### Vietnamese Code Comments

```python
# Before
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# After using "Zeta AI: Add Vietnamese Comments"
def calculate_total(items):
    """
    Tính tổng giá trị của danh sách sản phẩm
    
    Args:
        items: Danh sách các sản phẩm với thuộc tính price
        
    Returns:
        float: Tổng giá trị của tất cả sản phẩm
    """
    total = 0  # Khởi tạo biến tổng
    for item in items:  # Duyệt qua từng sản phẩm
        total += item.price  # Cộng giá vào tổng
    return total  # Trả về kết quả
```

### Vietnamese Quality Scoring

```
Quality Metrics for Vietnamese responses:
✅ Grammar accuracy: 95%+
✅ Technical terminology: 90%+  
✅ Context understanding: 85%+
✅ Cultural appropriateness: 100%
✅ Code explanation clarity: 90%+
```

## 💬 Chat Interface

### Opening Chat Panel

```
Method 1: Ctrl+Shift+C
Method 2: Command Palette → "Zeta AI: Start Chat"
Method 3: Click status bar → "Open Chat"
```

### Chat Features

```
Chat Interface Components:
├── Message History 📜
├── Model Selector 🔄
├── Language Toggle 🇻🇳/🇺🇸
├── Code Insertion Button 📝
├── Feedback Buttons 👍👎
├── Clear History 🗑️
└── Export Conversation 💾
```

### Advanced Chat Commands

```
Special commands in chat:
/model attong39/zeta     # Switch model
/vietnamese              # Enable Vietnamese mode
/english                 # Switch to English
/analyze <file>          # Analyze specific file
/debug                   # Debug mode
/optimize               # Optimization suggestions
/clear                  # Clear chat history
```

### Chat Best Practices

1. **Be Specific**: Include relevant code context
2. **Use Vietnamese**: For best results with Vietnamese queries
3. **Provide Context**: Mention programming language and framework
4. **Break Down Complex**: Split large questions into smaller parts

## 🔍 Code Analysis

### Code Review Features

```typescript
// Select this code block
function processUserData(userData: any[]): any[] {
  const results = [];
  for (let i = 0; i < userData.length; i++) {
    if (userData[i] && userData[i].active) {
      results.push({
        id: userData[i].id,
        name: userData[i].name.toUpperCase(),
        processed: true
      });
    }
  }
  return results;
}

// Right-click → "Zeta AI: Review Code"
```

**AI Analysis Output:**
```
🔍 Code Review - processUserData

Đánh giá chất lượng: 6/10

⚠️ Vấn đề được phát hiện:
1. **Type Safety**: Sử dụng 'any' type thay vì interface cụ thể
2. **Performance**: Loop truyền thống thay vì functional methods
3. **Error Handling**: Thiếu xử lý lỗi khi userData[i].name null
4. **Readability**: Logic có thể đơn giản hóa

✅ Gợi ý cải thiện:
```typescript
interface UserData {
  id: string;
  name: string;
  active: boolean;
}

interface ProcessedUser {
  id: string;
  name: string;
  processed: boolean;
}

function processUserData(userData: UserData[]): ProcessedUser[] {
  return userData
    .filter(user => user?.active && user?.name)
    .map(user => ({
      id: user.id,
      name: user.name.toUpperCase(),
      processed: true
    }));
}
```

📊 Cải thiện:
- Type safety: +3 points
- Performance: +1 point  
- Maintainability: +2 points
```

### Performance Analysis

```python
# Analyze this slow function
def find_duplicates(data):
    duplicates = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] == data[j] and data[i] not in duplicates:
                duplicates.append(data[i])
    return duplicates

# Use "Zeta AI: Optimize Code"
```

**Performance Report:**
```
⚡ Performance Analysis - find_duplicates

🐌 Current Complexity: O(n³)
🚀 Target Complexity: O(n)

Performance Issues:
1. Nested loops: O(n²) time complexity
2. Linear search in duplicates: +O(n) per iteration
3. Multiple list scans: Inefficient memory access

Optimized Solution:
```python
def find_duplicates(data):
    """Tìm các phần tử trùng lặp với độ phức tạp O(n)"""
    seen = set()
    duplicates = set()
    
    for item in data:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return list(duplicates)
```

📈 Performance Improvement:
- Time complexity: O(n³) → O(n) (300x faster for large datasets)
- Memory usage: Optimal with sets
- Readability: Improved with clear variable names
```

## ⚡ Performance Optimization

### Response Time Optimization

```json
// Optimize for speed
{
  "zeta.performance": {
    "preferredModel": "starcoder",      // Fastest model
    "maxResponseTime": 5000,            // 5s timeout
    "enableCaching": true,              // Cache responses
    "batchRequests": true,              // Group similar requests
    "streamingEnabled": false           // Disable for speed
  }
}
```

### Memory Usage Optimization

```json
// Optimize for memory
{
  "zeta.memory": {
    "maxChatHistory": 50,               // Limit chat messages
    "clearCacheInterval": 3600000,      // Clear cache hourly
    "maxConcurrentRequests": 2,         // Limit parallel requests
    "compressionEnabled": true          // Compress large responses
  }
}
```

### Network Optimization

```json
// Optimize for bandwidth
{
  "zeta.network": {
    "connectionTimeout": 10000,         // 10s connection timeout
    "retryAttempts": 3,                 // Retry failed requests
    "compressionLevel": 6,              // Response compression
    "keepAliveEnabled": true            // Reuse connections
  }
}
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Extension Not Starting

**Symptoms**: No Zeta AI commands in Command Palette

**Solutions**:
```bash
# Check extension status
Ctrl+Shift+P → "Extensions: Show Installed Extensions"
# Look for "Zeta AI Agent" - should show "Enabled"

# Reload VS Code
Ctrl+Shift+P → "Developer: Reload Window"

# Check output logs
View → Output → Select "Zeta AI Agent"
```

#### 2. Ollama Connection Failed

**Symptoms**: "Failed to connect to Ollama" error

**Solutions**:
```bash
# Verify Ollama is running
ollama serve

# Check Ollama status
curl http://localhost:11434/api/tags

# Restart Ollama service
# Windows: Stop Ollama → Start Ollama
# macOS/Linux: killall ollama && ollama serve
```

#### 3. Models Not Found

**Symptoms**: "Model 'attong39/zeta' not found"

**Solutions**:
```bash
# List installed models
ollama list

# Pull missing models
ollama pull attong39/zeta
ollama pull starcoder
ollama pull codellama:13b-instruct

# Verify model installation
ollama show attong39/zeta
```

#### 4. High Response Latency

**Symptoms**: >10s response times

**Solutions**:
```json
// Switch to faster model
{
  "zeta.defaultModel": "starcoder"  // 4.9s avg vs 8.4s
}
```

```bash
# Check system resources
# Windows: Task Manager → Performance
# macOS: Activity Monitor
# Linux: htop or top

# Optimize Ollama performance
export OLLAMA_NUM_PARALLEL=2        # Limit parallel requests
export OLLAMA_MAX_LOADED_MODELS=1   # Reduce memory usage
```

#### 5. Vietnamese Text Issues

**Symptoms**: Broken Vietnamese characters

**Solutions**:
```json
// VS Code settings
{
  "files.encoding": "utf8",
  "terminal.integrated.fontFamily": "Consolas, 'Times New Roman'",
  "editor.fontFamily": "Fira Code, Consolas"
}
```

### Debug Mode

```
Enable detailed logging:
Ctrl+Shift+P → "Zeta AI: Enable Debug Mode"

Debug output location:
- Windows: %APPDATA%/Code/logs/apps/zeta-ai-agent/
- macOS: ~/Library/Logs/Code/apps/zeta-ai-agent/
- Linux: ~/.config/Code/logs/apps/zeta-ai-agent/
```

## 💡 Best Practices

### 1. Effective Prompting

**Good Prompts:**
```
❌ Bad: "Fix this code"
✅ Good: "Phân tích function Python này và gợi ý cải thiện performance"

❌ Bad: "Help"  
✅ Good: "Giải thích tại sao TypeScript function này báo lỗi type"

❌ Bad: "Optimize"
✅ Good: "Tối ưu hóa React component này để giảm re-renders"
```

### 2. Model Selection Strategy

```
Quick questions → starcoder (4.9s avg)
Code review → zeta-py-teacher (3.8s avg)  
Complex debugging → codellama:13b (6.2s avg)
Vietnamese content → attong39/zeta (10/10 quality)
Performance tuning → deepseek-coder (8/10 optimization)
```

### 3. Context Management

```typescript
// Provide sufficient context
// ❌ Bad
function process(data) { ... }

// ✅ Good  
// File: userService.ts
// Framework: Express.js + TypeScript
// Purpose: Process user registration data
interface UserData {
  email: string;
  password: string;
  profile: UserProfile;
}

function processUserRegistration(userData: UserData): Promise<User> {
  // Function implementation
}
```

### 4. Performance Monitoring

```
Monitor these metrics:
📊 Response Time: Target <5s for interactive use
📊 Success Rate: Should be >90% for production  
📊 Vietnamese Quality: Maintain >8/10 for Vietnamese content
📊 Memory Usage: Keep <500MB for optimal performance
📊 Model Accuracy: Track feedback scores for improvement
```

### 5. Feedback Loop

```
Provide feedback for continuous improvement:
👍 Thumbs up: Accurate, helpful responses
👎 Thumbs down: Incorrect or unhelpful responses

Rate Vietnamese quality:
⭐⭐⭐⭐⭐ Perfect Vietnamese grammar and context
⭐⭐⭐⭐ Good with minor issues
⭐⭐⭐ Acceptable with some errors
⭐⭐ Poor quality, needs improvement
⭐ Unacceptable, major issues
```

## 📞 Support

### Getting Help

1. **Documentation**: This guide + README.md
2. **GitHub Issues**: Report bugs and feature requests
3. **Community**: Join discussions on GitHub Discussions
4. **Email**: support@zeta-ai.dev for enterprise support

### Diagnostic Information

When reporting issues, include:
```
System Info:
- OS: Windows 11 / macOS 14 / Ubuntu 22.04
- VS Code: 1.85.0
- Node.js: 18.17.0  
- Ollama: 0.11.8
- Extension: 1.0.0

Models Installed:
- attong39/zeta: ✅ (3.2B parameters)
- starcoder: ✅  
- codellama:13b: ✅

Error Details:
- Error message: [exact error text]
- Steps to reproduce: [detailed steps]
- Expected behavior: [what should happen]
- Actual behavior: [what actually happens]
```

---

**Happy coding with Zeta AI! 🚀🇻🇳**

*For more advanced usage, see [DEVOPS_PLAYBOOK.md](DEVOPS_PLAYBOOK.md)*
