# 🚀 Quy trình chạy DeepSeek R1 (Ollama) & tích hợp vào VS Code extension

> **Tất cả công cụ offline** - không cần API key, chỉ cần Docker (hoặc Ollama binary) và Node.js

## 📋 Bảng công việc

| Bước | Mục tiêu                | Tham chiếu file / lệnh                           |
| ---- | ----------------------- | ------------------------------------------------ |
| 1️⃣    | Chuẩn bị môi trường     | `install-ollama.ps1`, `install-node.ps1`         |
| 2️⃣    | Cài Ollama & Pull model | `ollama serve`, `ollama pull deepseek-r1:latest` |
| 3️⃣    | Kiểm tra REST API       | `curl` / PowerShell `Invoke-WebRequest`          |
| 4️⃣    | Build extension         | `npm install && npm run compile`                 |
| 5️⃣    | Chạy VS Code extension  | `code . + F5` or cài `.vsix`                     |
| 6️⃣    | Gọi AI-Agent            | VS Code commands hoặc CLI                        |
| 7️⃣    | Theo dõi logs           | `vscode.OutputChannel`, `ollama logs`            |
| 8️⃣    | Tối ưu & bảo mật        | GPU settings, path-checking, diff-preview        |

---

## 1️⃣ Cài đặt & thiết lập

### 1.1 Install Ollama (Windows PowerShell)

```powershell
# Cách 1: Sử dụng Chocolatey (khuyến nghị)
choco install ollama

# Cách 2: Tải trực tiếp
Invoke-WebRequest -Uri "https://ollama.com/download/ollama-windows.zip" -OutFile "C:\tmp\ollama.zip"
Expand-Archive "C:\tmp\ollama.zip" -DestinationPath "C:\ProgramData\ollama"
$env:PATH += ";C:\ProgramData\ollama"

# Kiểm tra cài đặt
ollama --version
```

### 1.2 Install Node.js & TypeScript

```powershell
# Cài Node.js LTS
choco install nodejs-lts

# Kiểm tra phiên bản
node -v   # >= 18.0.0
npm -v    # >= 9.0.0

# Cài TypeScript globally (tùy chọn)
npm install -g typescript
```

### 1.3 Script tự động

```powershell
# scripts/run_deepseek_r1.ps1
# Requires -Version 5.1
param(
  [string]$Model = "deepseek-r1:latest",
  [string]$ExtDir = "E:\zeta\deepseek-extension", 
  [switch]$DevHost,      # Mở VS Code Dev Host thay vì cài .vsix
  [switch]$QuickReview   # Gọi review file đang mở ngay
)

function Test-Port11434 {
  try { 
    (Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 2).StatusCode -eq 200 
  } 
  catch { $false }
}

Write-Host "=== 1) Start Ollama service" -ForegroundColor Cyan
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 3

Write-Host "=== 2) Pull model ($Model)" -ForegroundColor Cyan
& ollama pull $Model

Write-Host "=== 3) Sanity-check REST (generate ping)" -ForegroundColor Cyan
$payload = @{ 
  model = $Model
  prompt = "ping"
  stream = $false 
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/generate" `
  -Method POST -ContentType "application/json" -Body $payload | Out-Null

Write-Host "=== 4) Build VS Code extension" -ForegroundColor Cyan
Push-Location $ExtDir

if (-not (Test-Path package.json)) { 
  Write-Error "Không thấy package.json trong $ExtDir"
  exit 1 
}

npm install
npm run compile

Write-Host "=== 5) Launch extension" -ForegroundColor Cyan
if ($DevHost) {
  code .
  Write-Host "=> Nhấn F5 để mở Extension Development Host" -ForegroundColor Yellow
} else {
  # Auto-install .vsix nếu có
  $vsix = Get-ChildItem -Path $ExtDir -Filter "*.vsix" -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($vsix) { 
    code --install-extension $vsix.FullName 
    Write-Host "=> Đã cài extension từ $($vsix.Name)" -ForegroundColor Green
  }
  code .
}

Write-Host "=== 6) Run AI Agent (optional)" -ForegroundColor Cyan
if ($QuickReview) {
  Start-Sleep -Seconds 2
  code --command "deepseek.agent.reviewActiveFile"
  Write-Host "=> Đã gọi: deepseek.agent.reviewActiveFile" -ForegroundColor Green
}

Pop-Location
Write-Host "✅ HOÀN THÀNH!" -ForegroundColor Green
```

**Cách chạy:**
```powershell
# Development mode với quick review
./scripts/run_deepseek_r1.ps1 -DevHost -QuickReview

# Production mode
./scripts/run_deepseek_r1.ps1 -Model "gpt-oss:20b"
```

---

## 2️⃣ Client gọi Ollama (TypeScript)

### File: `src/ai/ollamaClient.ts`

```typescript
// SPDX-License-Identifier: MIT
/* eslint-disable @typescript-eslint/no-explicit-any */

export interface OllamaMessage { 
  role: 'system' | 'user' | 'assistant'
  content: string 
}

export interface OllamaResponse {
  message: { content: string }
  done: boolean
}

export class OllamaClient {
  constructor(
    private readonly baseUrl = 'http://127.0.0.1:11434',
    private readonly model = 'deepseek-r1:latest',
    private readonly timeout = 120000  // 2 phút
  ) {}

  async chat(messages: OllamaMessage[], stream = false): Promise<string> {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), this.timeout)

    try {
      const res = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ 
          model: this.model, 
          messages, 
          stream,
          options: {
            temperature: 0.7,
            top_p: 0.9,
            num_predict: 2048
          }
        }),
        signal: controller.signal
      })

      if (!res.ok) {
        throw new Error(`Ollama HTTP ${res.status}: ${await res.text()}`)
      }

      const json: OllamaResponse = await res.json()
      return json?.message?.content ?? ''

    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error(`Timeout sau ${this.timeout}ms`)
      }
      throw error
    } finally {
      clearTimeout(timeoutId)
    }
  }

  async *chatStream(messages: OllamaMessage[]): AsyncGenerator<string, void, unknown> {
    const res = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ 
        model: this.model, 
        messages, 
        stream: true 
      })
    })

    if (!res.ok) {
      throw new Error(`Ollama HTTP ${res.status}`)
    }

    const reader = res.body?.getReader()
    const decoder = new TextDecoder()

    while (reader) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n').filter(line => line.trim())

      for (const line of lines) {
        try {
          const json: OllamaResponse = JSON.parse(line)
          if (json.message?.content) {
            yield json.message.content
          }
        } catch {
          // Skip invalid JSON lines
        }
      }
    }
  }

  async checkHealth(): Promise<boolean> {
    try {
      const res = await fetch(`${this.baseUrl}/api/tags`, { 
        method: 'GET',
        signal: AbortSignal.timeout(5000)
      })
      return res.ok
    } catch {
      return false
    }
  }

  async listModels(): Promise<string[]> {
    const res = await fetch(`${this.baseUrl}/api/tags`)
    if (!res.ok) throw new Error(`Cannot list models: ${res.status}`)
    
    const data: any = await res.json()
    return data.models?.map((m: any) => m.name) ?? []
  }
}
```

---

## 3️⃣ Enhanced AI Agent

### File cập nhật: `src/aiAgent.ts`

```typescript
import * as vscode from 'vscode'
import { OllamaClient, OllamaMessage } from './ai/ollamaClient'

export type AgentTask = 'review' | 'debug' | 'optimize' | 'test' | 'document'

export interface AgentResult {
  success: boolean
  message: string
  suggestions?: string[]
  errors?: string[]
}

export class AIAgent {
  private readonly client: OllamaClient
  private readonly output: vscode.OutputChannel

  constructor(private readonly context: vscode.ExtensionContext) {
    // Đọc model từ settings
    const config = vscode.workspace.getConfiguration('deepseek.agent')
    const model = config.get<string>('model') ?? 'gpt-oss:20b'
    
    this.client = new OllamaClient('http://127.0.0.1:11434', model)
    this.output = vscode.window.createOutputChannel('DeepSeek Agent')
  }

  async runTask(task: AgentTask, files?: vscode.Uri[]): Promise<AgentResult> {
    this.output.show(true)
    this.output.appendLine(`🚀 Bắt đầu task: ${task}`)

    try {
      // Kiểm tra Ollama service
      const isHealthy = await this.client.checkHealth()
      if (!isHealthy) {
        throw new Error('Ollama service không khả dụng. Chạy: ollama serve')
      }

      const targetFiles = files ?? this.getActiveFiles()
      if (targetFiles.length === 0) {
        throw new Error('Không có file nào để xử lý')
      }

      const results: AgentResult[] = []
      
      for (const fileUri of targetFiles) {
        this.output.appendLine(`📁 Xử lý: ${fileUri.fsPath}`)
        const result = await this.processFile(task, fileUri)
        results.push(result)
      }

      const overallSuccess = results.every(r => r.success)
      return {
        success: overallSuccess,
        message: `Hoàn thành ${task} cho ${results.length} file(s)`,
        suggestions: results.flatMap(r => r.suggestions ?? []),
        errors: results.flatMap(r => r.errors ?? [])
      }

    } catch (error) {
      const errorMsg = `❌ Lỗi ${task}: ${error}`
      this.output.appendLine(errorMsg)
      vscode.window.showErrorMessage(errorMsg)
      
      return {
        success: false,
        message: errorMsg,
        errors: [String(error)]
      }
    }
  }

  private async processFile(task: AgentTask, fileUri: vscode.Uri): Promise<AgentResult> {
    const document = await vscode.workspace.openTextDocument(fileUri)
    const code = document.getText()
    const language = document.languageId
    const fileName = vscode.workspace.asRelativePath(fileUri)

    const prompt = this.buildPrompt(task, code, language, fileName)
    const messages: OllamaMessage[] = [
      { role: 'user', content: prompt }
    ]

    try {
      const response = await this.client.chat(messages)
      this.output.appendLine(`✅ ${fileName}: ${response.substring(0, 200)}...`)

      return {
        success: true,
        message: `Thành công ${task} cho ${fileName}`,
        suggestions: this.extractSuggestions(response)
      }

    } catch (error) {
      return {
        success: false,
        message: `Lỗi ${task} cho ${fileName}`,
        errors: [String(error)]
      }
    }
  }

  private buildPrompt(task: AgentTask, code: string, language: string, fileName: string): string {
    const basePrompt = `
Bạn là AI assistant chuyên nghiệp. 
File: ${fileName}
Language: ${language}

Code:
\`\`\`${language}
${code}
\`\`\`
`

    switch (task) {
      case 'review':
        return basePrompt + `
Nhiệm vụ: CODE REVIEW chi tiết
Phân tích:
1. Code quality & best practices
2. Performance issues
3. Security vulnerabilities  
4. Error handling
5. Documentation quality

Trả về format JSON:
{
  "summary": "Tóm tắt đánh giá",
  "issues": ["Vấn đề 1", "Vấn đề 2"],
  "suggestions": ["Gợi ý 1", "Gợi ý 2"],
  "score": 8.5
}
`

      case 'debug':
        return basePrompt + `
Nhiệm vụ: PHÂN TÍCH LỖI & DEBUG
Tìm kiếm:
1. Logic errors
2. Runtime exceptions
3. Edge cases
4. Potential bugs
5. Memory leaks

Trả về các điểm cần kiểm tra và cách sửa.
`

      case 'optimize':
        return basePrompt + `
Nhiệm vụ: TỐI ƯU HÓA CODE
Cải thiện:
1. Algorithm complexity
2. Memory usage
3. I/O operations
4. Caching strategies
5. Code structure

Đề xuất code tối ưu hơn với giải thích.
`

      case 'test':
        return basePrompt + `
Nhiệm vụ: TẠO UNIT TESTS
Tạo test cases cho:
1. Normal scenarios
2. Edge cases
3. Error conditions
4. Boundary values

Trả về complete test code.
`

      case 'document':
        return basePrompt + `
Nhiệm vụ: TẠO DOCUMENTATION
Tạo:
1. Function/class docstrings
2. Usage examples
3. Parameter descriptions
4. Return value docs

Format theo chuẩn của ${language}.
`

      default:
        return basePrompt + `Phân tích code này và đưa ra nhận xét.`
    }
  }

  private extractSuggestions(response: string): string[] {
    // Thử parse JSON trước
    try {
      const json = JSON.parse(response)
      if (json.suggestions) return json.suggestions
      if (json.issues) return json.issues
    } catch {
      // Fallback: extract từ text
    }

    // Extract suggestions từ markdown/text
    const lines = response.split('\n')
    return lines
      .filter(line => line.trim().startsWith('-') || line.trim().startsWith('*'))
      .map(line => line.trim().substring(1).trim())
      .slice(0, 10) // Giới hạn 10 suggestions
  }

  private getActiveFiles(): vscode.Uri[] {
    const activeEditor = vscode.window.activeTextEditor
    return activeEditor ? [activeEditor.document.uri] : []
  }

  async continuous(task: AgentTask, iterations: number = 3): Promise<void> {
    this.output.appendLine(`🔄 Bắt đầu continuous ${task} với ${iterations} vòng lặp`)

    for (let i = 1; i <= iterations; i++) {
      this.output.appendLine(`\n--- Vòng lặp ${i}/${iterations} ---`)
      
      const result = await this.runTask(task)
      if (!result.success) {
        this.output.appendLine(`⏹️ Dừng ở vòng ${i} do lỗi: ${result.message}`)
        break
      }

      if (i < iterations) {
        this.output.appendLine(`⏳ Chờ 5 giây trước vòng tiếp theo...`)
        await new Promise(resolve => setTimeout(resolve, 5000))
      }
    }

    this.output.appendLine(`\n✅ Hoàn thành continuous ${task}`)
  }

  dispose(): void {
    this.output.dispose()
  }
}
```

---

## 4️⃣ Enhanced VS Code Extension Commands

### File cập nhật: `src/extension.ts` (phần commands)

```typescript
export function activate(context: vscode.ExtensionContext) {
  const output = vscode.window.createOutputChannel('DeepSeek Agent')

  // 1) Review Active File
  const reviewActiveCmd = vscode.commands.registerCommand(
    'deepseek.agent.reviewActiveFile', 
    async () => {
      const editor = vscode.window.activeTextEditor
      if (!editor) {
        return vscode.window.showWarningMessage('Không có file đang mở')
      }

      const agent = new AIAgent(context)
      await agent.runTask('review', [editor.document.uri])
      output.show(true)
    }
  )

  // 2) Run Task với QuickPick
  const runTaskCmd = vscode.commands.registerCommand(
    'deepseek.agent.runTask',
    async () => {
      const task = await vscode.window.showQuickPick(
        ['review', 'debug', 'optimize', 'test', 'document'],
        { 
          placeHolder: 'Chọn task để chạy',
          canPickMany: false
        }
      )

      if (!task) return

      const agent = new AIAgent(context)
      await agent.runTask(task as any)
      output.show(true)
    }
  )

  // 3) Continuous Mode
  const continuousCmd = vscode.commands.registerCommand(
    'deepseek.agent.continuous',
    async () => {
      const task = await vscode.window.showQuickPick(
        ['review', 'debug', 'optimize'],
        { placeHolder: 'Chọn task cho continuous mode' }
      )

      if (!task) return

      const iterations = await vscode.window.showInputBox({
        prompt: 'Số vòng lặp (1-10)',
        value: '3',
        validateInput: (value) => {
          const num = parseInt(value)
          if (isNaN(num) || num < 1 || num > 10) {
            return 'Nhập số từ 1 đến 10'
          }
          return null
        }
      })

      if (!iterations) return

      const agent = new AIAgent(context)
      await agent.continuous(task as any, parseInt(iterations))
      output.show(true)
    }
  )

  // 4) Choose Model
  const chooseModelCmd = vscode.commands.registerCommand(
    'deepseek.agent.chooseModel',
    async () => {
      try {
        const client = new OllamaClient()
        const models = await client.listModels()
        
        if (models.length === 0) {
          return vscode.window.showWarningMessage('Không tìm thấy model nào. Chạy: ollama pull <model>')
        }

        const selected = await vscode.window.showQuickPick(models, {
          placeHolder: 'Chọn model để sử dụng'
        })

        if (selected) {
          const config = vscode.workspace.getConfiguration('deepseek.agent')
          await config.update('model', selected, vscode.ConfigurationTarget.Workspace)
          vscode.window.showInformationMessage(`Đã chọn model: ${selected}`)
        }

      } catch (error) {
        vscode.window.showErrorMessage(`Lỗi khi lấy danh sách model: ${error}`)
      }
    }
  )

  // 5) Health Check  
  const healthCmd = vscode.commands.registerCommand(
    'deepseek.agent.health',
    async () => {
      try {
        const client = new OllamaClient()
        const isHealthy = await client.checkHealth()
        
        if (isHealthy) {
          const models = await client.listModels()
          vscode.window.showInformationMessage(
            `✅ Ollama khỏe mạnh. Models: ${models.length}`
          )
        } else {
          vscode.window.showWarningMessage(
            '❌ Ollama không khả dụng. Chạy: ollama serve'
          )
        }
      } catch (error) {
        vscode.window.showErrorMessage(`Health check failed: ${error}`)
      }
    }
  )

  // Đăng ký tất cả commands
  context.subscriptions.push(
    reviewActiveCmd,
    runTaskCmd, 
    continuousCmd,
    chooseModelCmd,
    healthCmd,
    output
  )

  // Auto health check khi activate
  vscode.commands.executeCommand('deepseek.agent.health')
}
```

---

## 5️⃣ Package.json với đầy đủ commands

### File cập nhật: `package.json` (phần contributes)

```json
{
  "contributes": {
    "configuration": {
      "title": "DeepSeek Agent",
      "properties": {
        "deepseek.agent.model": {
          "type": "string",
          "default": "gpt-oss:20b",
          "description": "Model Ollama để sử dụng (deepseek-r1:latest, gpt-oss:20b, ...)"
        },
        "deepseek.agent.baseUrl": {
          "type": "string", 
          "default": "http://127.0.0.1:11434",
          "description": "URL của Ollama service"
        },
        "deepseek.agent.timeout": {
          "type": "number",
          "default": 120000,
          "description": "Timeout cho API calls (ms)"
        }
      }
    },
    "commands": [
      {
        "command": "deepseek.agent.reviewActiveFile",
        "title": "DeepSeek: Review Current File",
        "icon": "$(search-view-icon)"
      },
      {
        "command": "deepseek.agent.runTask", 
        "title": "DeepSeek: Run Task (Review/Debug/Optimize)",
        "icon": "$(play)"
      },
      {
        "command": "deepseek.agent.continuous",
        "title": "DeepSeek: Continuous Mode",
        "icon": "$(refresh)"
      },
      {
        "command": "deepseek.agent.chooseModel",
        "title": "DeepSeek: Choose Model",
        "icon": "$(settings-gear)"
      },
      {
        "command": "deepseek.agent.health",
        "title": "DeepSeek: Health Check",
        "icon": "$(pulse)"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "when": "editorHasSelection",
          "command": "deepseek.agent.reviewActiveFile",
          "group": "deepseek@1"
        }
      ],
      "editor/title": [
        {
          "command": "deepseek.agent.reviewActiveFile",
          "when": "resourceExtname =~ /\\.(py|js|ts|java|cpp|c|go|rs)$/",
          "group": "navigation@1"
        }
      ]
    }
  }
}
```

---

## 6️⃣ Scripts PowerShell cho automation

### File: `scripts/install-ollama.ps1`

```powershell
# Requires -Version 5.1
# Install Ollama trên Windows

param(
  [string[]]$Models = @("deepseek-r1:latest", "gpt-oss:20b"),
  [switch]$StartService,
  [switch]$TestAPI
)

Write-Host "🚀 Cài đặt Ollama..." -ForegroundColor Cyan

# Kiểm tra Chocolatey
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
  Write-Host "❌ Cần cài Chocolatey trước. Chạy:" -ForegroundColor Red
  Write-Host "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
  exit 1
}

# Cài Ollama
Write-Host "📦 Cài đặt Ollama..." -ForegroundColor Yellow
choco install ollama -y

# Kiểm tra cài đặt
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  Write-Host "❌ Ollama không cài được" -ForegroundColor Red
  exit 1
}

Write-Host "✅ Ollama đã cài: $(ollama --version)" -ForegroundColor Green

# Start service
if ($StartService) {
  Write-Host "🔧 Khởi động Ollama service..." -ForegroundColor Yellow
  Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
  Start-Sleep -Seconds 5
}

# Pull models
foreach ($model in $Models) {
  Write-Host "📥 Pulling model: $model" -ForegroundColor Yellow
  & ollama pull $model
}

# Test API
if ($TestAPI) {
  Write-Host "🧪 Test Ollama API..." -ForegroundColor Yellow
  try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 10
    Write-Host "✅ API hoạt động: HTTP $($response.StatusCode)" -ForegroundColor Green
  } catch {
    Write-Host "❌ API không hoạt động: $($_.Exception.Message)" -ForegroundColor Red
  }
}

Write-Host "🎉 Hoàn thành cài đặt Ollama!" -ForegroundColor Green
```

### File: `scripts/install-node.ps1`

```powershell
# Install Node.js và dependencies

param(
  [string]$NodeVersion = "lts",
  [switch]$InstallYarn
)

Write-Host "🚀 Cài đặt Node.js..." -ForegroundColor Cyan

# Cài Node.js
if ($NodeVersion -eq "lts") {
  choco install nodejs-lts -y
} else {
  choco install nodejs --version $NodeVersion -y  
}

# Kiểm tra
$nodeVer = & node -v 2>$null
$npmVer = & npm -v 2>$null

if ($nodeVer -and $npmVer) {
  Write-Host "✅ Node.js: $nodeVer, npm: $npmVer" -ForegroundColor Green
} else {
  Write-Host "❌ Node.js không cài được" -ForegroundColor Red
  exit 1
}

# Cài Yarn (tùy chọn)
if ($InstallYarn) {
  npm install -g yarn
  $yarnVer = & yarn -v 2>$null
  Write-Host "✅ Yarn: $yarnVer" -ForegroundColor Green
}

# Cài TypeScript global
npm install -g typescript @types/node

Write-Host "🎉 Hoàn thành cài đặt Node.js!" -ForegroundColor Green
```

---

## 7️⃣ Kiểm thử & Testing

### File: `scripts/test-ollama-api.ps1`

```powershell
# Test Ollama API endpoints

param(
  [string]$BaseUrl = "http://127.0.0.1:11434",
  [string]$Model = "gpt-oss:20b"
)

Write-Host "🧪 Testing Ollama API..." -ForegroundColor Cyan

# Test 1: Health check
Write-Host "1️⃣ Health check..." -ForegroundColor Yellow
try {
  $health = Invoke-WebRequest -Uri "$BaseUrl/api/tags" -TimeoutSec 5
  Write-Host "✅ Health: HTTP $($health.StatusCode)" -ForegroundColor Green
} catch {
  Write-Host "❌ Health failed: $($_.Exception.Message)" -ForegroundColor Red
  exit 1
}

# Test 2: List models
Write-Host "2️⃣ List models..." -ForegroundColor Yellow
try {
  $models = Invoke-WebRequest -Uri "$BaseUrl/api/tags" | ConvertFrom-Json
  $modelNames = $models.models | ForEach-Object { $_.name }
  Write-Host "✅ Models: $($modelNames -join ', ')" -ForegroundColor Green
} catch {
  Write-Host "❌ Cannot list models" -ForegroundColor Red
}

# Test 3: Simple generate
Write-Host "3️⃣ Test generate..." -ForegroundColor Yellow
$generatePayload = @{
  model = $Model
  prompt = "Hello, respond with just 'Hi'"
  stream = $false
} | ConvertTo-Json

try {
  $generate = Invoke-WebRequest -Uri "$BaseUrl/api/generate" `
    -Method POST -ContentType "application/json" -Body $generatePayload -TimeoutSec 30
  $result = $generate.Content | ConvertFrom-Json
  Write-Host "✅ Generate: $($result.response)" -ForegroundColor Green
} catch {
  Write-Host "❌ Generate failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Chat API
Write-Host "4️⃣ Test chat..." -ForegroundColor Yellow
$chatPayload = @{
  model = $Model
  messages = @(
    @{ role = "user"; content = "Say hi" }
  )
  stream = $false
} | ConvertTo-Json -Depth 3

try {
  $chat = Invoke-WebRequest -Uri "$BaseUrl/api/chat" `
    -Method POST -ContentType "application/json" -Body $chatPayload -TimeoutSec 30
  $chatResult = $chat.Content | ConvertFrom-Json
  Write-Host "✅ Chat: $($chatResult.message.content)" -ForegroundColor Green
} catch {
  Write-Host "❌ Chat failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "🎉 API testing hoàn thành!" -ForegroundColor Green
```

---

## 8️⃣ CLI Tool (tùy chọn)

### File: `cli/deepseek-agent.ps1`

```powershell
# CLI wrapper cho DeepSeek Agent

param(
  [Parameter(Mandatory=$true, Position=0)]
  [ValidateSet("review", "debug", "optimize", "test", "document")]
  [string]$Task,
  
  [Parameter(Mandatory=$true, Position=1)]
  [string]$FilePath,
  
  [string]$Model = "gpt-oss:20b",
  [string]$BaseUrl = "http://127.0.0.1:11434",
  [switch]$Stream,
  [switch]$Verbose
)

if (-not (Test-Path $FilePath)) {
  Write-Error "File không tồn tại: $FilePath"
  exit 1
}

$code = Get-Content $FilePath -Raw
$language = [System.IO.Path]::GetExtension($FilePath).TrimStart('.')

$prompt = switch ($Task) {
  "review" { "Code review chi tiết cho file này, tập trung vào quality, security và performance:" }
  "debug" { "Phân tích và tìm bugs trong code này:" }
  "optimize" { "Tối ưu hóa code này về performance và readability:" }
  "test" { "Tạo unit tests đầy đủ cho code này:" }
  "document" { "Tạo documentation chi tiết cho code này:" }
}

$fullPrompt = "$prompt`n`n\`\`\`$language`n$code`n\`\`\`"

$payload = @{
  model = $Model
  messages = @(
    @{ role = "user"; content = $fullPrompt }
  )
  stream = $Stream.IsPresent
} | ConvertTo-Json -Depth 3

if ($Verbose) {
  Write-Host "🚀 Task: $Task" -ForegroundColor Cyan
  Write-Host "📁 File: $FilePath" -ForegroundColor Cyan  
  Write-Host "🤖 Model: $Model" -ForegroundColor Cyan
  Write-Host "🌐 URL: $BaseUrl" -ForegroundColor Cyan
}

try {
  $response = Invoke-WebRequest -Uri "$BaseUrl/api/chat" `
    -Method POST -ContentType "application/json" -Body $payload -TimeoutSec 120

  $result = $response.Content | ConvertFrom-Json
  Write-Output $result.message.content

} catch {
  Write-Error "❌ API call failed: $($_.Exception.Message)"
  exit 1
}
```

**Cách sử dụng CLI:**
```powershell
# Review file
.\cli\deepseek-agent.ps1 review "src\app.py" -Verbose

# Debug với model khác  
.\cli\deepseek-agent.ps1 debug "src\buggy.js" -Model "deepseek-r1:latest"

# Optimize với stream
.\cli\deepseek-agent.ps1 optimize "src\slow.py" -Stream
```

---

## 9️⃣ Checklist triển khai

### ✅ Pre-deployment

- [ ] **Ollama cài đặt**: `ollama --version`
- [ ] **Service chạy**: `curl http://127.0.0.1:11434/api/tags`  
- [ ] **Models pulled**: `ollama list` có `deepseek-r1:latest`, `gpt-oss:20b`
- [ ] **Node.js ready**: `node -v >= 18`, `npm -v >= 9`

### ✅ Extension build

- [ ] **Dependencies**: `npm install` thành công
- [ ] **TypeScript compile**: `npm run compile` không lỗi
- [ ] **Package valid**: `vsce package` (tùy chọn) 

### ✅ VS Code integration

- [ ] **Extension load**: F5 mở Extension Development Host
- [ ] **Commands available**: Ctrl+Shift+P → `DeepSeek:`
- [ ] **Settings work**: `deepseek.agent.model` đọc được
- [ ] **Output channel**: View → Output → "DeepSeek Agent"

### ✅ Functional tests

- [ ] **Health check**: `DeepSeek: Health Check` → ✅
- [ ] **Review file**: Mở file → `DeepSeek: Review Current File`
- [ ] **Model switch**: `DeepSeek: Choose Model` → chọn model khác
- [ ] **Continuous mode**: `DeepSeek: Continuous Mode` → chạy 3 vòng

### ✅ Performance & Security

- [ ] **GPU utilization**: `nvidia-smi` (nếu có GPU)
- [ ] **Memory usage**: Task Manager → ollama.exe < 8GB RAM
- [ ] **Path traversal**: Không cho phép `../` trong file paths
- [ ] **Timeout handling**: API calls có timeout 120s
- [ ] **Error handling**: Lỗi hiển thị đúng trong Output Channel

---

## 🔧 Troubleshooting

| Vấn đề                          | Nguyên nhân                   | Giải pháp                        |
| ------------------------------- | ----------------------------- | -------------------------------- |
| `Ollama service không khả dụng` | Chưa chạy `ollama serve`      | `Start-Process ollama serve`     |
| `Model not found`               | Chưa pull model               | `ollama pull deepseek-r1:latest` |
| `Timeout 120s`                  | Model quá lớn/GPU yếu         | Dùng CPU: `OLLAMA_NUM_GPU=0`     |
| `Extension compile error`       | TypeScript lỗi syntax         | Sửa lỗi trong `.ts` files        |
| `Commands không hiện`           | `package.json` thiếu commands | Thêm vào `contributes.commands`  |
| `Out of vRAM`                   | GPU memory đầy                | `ollama serve --low-vram`        |

---

## 🚀 Script tổng hợp

### File: `scripts/setup-complete.ps1`

```powershell
# Setup hoàn chỉnh DeepSeek + VS Code Extension

Write-Host "🚀 SETUP DEEPSEEK + VSCODE EXTENSION" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# 1. Install prerequisites  
Write-Host "`n1️⃣ Cài đặt prerequisites..." -ForegroundColor Yellow
& .\scripts\install-ollama.ps1 -Models @("gpt-oss:20b", "deepseek-r1:latest") -StartService
& .\scripts\install-node.ps1 -InstallYarn

# 2. Build extension
Write-Host "`n2️⃣ Build VS Code Extension..." -ForegroundColor Yellow
Push-Location "deepseek-extension"
npm install
npm run compile
Pop-Location

# 3. Test Ollama API
Write-Host "`n3️⃣ Test Ollama API..." -ForegroundColor Yellow  
& .\scripts\test-ollama-api.ps1 -Model "gpt-oss:20b"

# 4. Launch VS Code
Write-Host "`n4️⃣ Launch VS Code..." -ForegroundColor Yellow
code deepseek-extension

Write-Host "`n✅ SETUP HOÀN THÀNH!" -ForegroundColor Green
Write-Host "Bước tiếp theo:" -ForegroundColor Yellow
Write-Host "1. Trong VS Code: nhấn F5 để mở Extension Development Host" -ForegroundColor White
Write-Host "2. Chạy command: DeepSeek: Health Check" -ForegroundColor White  
Write-Host "3. Test: DeepSeek: Review Current File" -ForegroundColor White
```

**Chạy setup tổng hợp:**
```powershell
.\scripts\setup-complete.ps1
```

Quy trình này cung cấp đầy đủ automation từ cài đặt đến kiểm thử, với offline support hoàn toàn và integration mạnh mẽ với VS Code! 🎉
