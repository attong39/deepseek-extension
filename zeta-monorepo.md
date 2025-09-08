🚀 Tối ưu hóa dự án Zeta AI: Tập trung vào AI Agent với Ollama
Dựa trên yêu cầu của bạn, tôi sẽ đề xuất cấu trúc tối ưu cho dự án Zeta AI, tập trung vào:

Loại bỏ các thành phần không cần thiết
Tập trung vào AI Agent sử dụng Ollama
Thiết kế agent thông minh như Copilot
Sử dụng các công nghệ hiện đại nhất
📦 Cấu trúc dự án đề xuất
zeta-monorepo/
├── src/
│   ├── core/                    # Core AI agent functionality
│   │   ├── ollama/              # Ollama integration
│   │   │   ├── client.ts        # Ollama API client
│   │   │   ├── models.ts        # Model management
│   │   │   └── types.ts         # Type definitions
│   │   ├── agent/               # Main agent logic
│   │   │   ├── cognitive/       # Cognitive capabilities
│   │   │   ├── memory/          # Memory management
│   │   │   └── planner/         # Action planning
│   │   ├── tools/               # Agent tools
│   │   │   ├── code/            # Code analysis tools
│   │   │   ├── file/            # File operations
│   │   │   └── system/          # System tools
│   │   └── utils/               # Utilities
│   ├── extension/               # VS Code extension
│   │   ├── provider/            # Language provider
│   │   ├── webview/             # Webview UI
│   │   └── commands.ts          # Extension commands
│   └── types/                   # Shared types
├── scripts/                     # Build and utility scripts
├── tests/                       # Test suite
├── package.json                 # Package configuration
├── tsconfig.json               # TypeScript config
└── README.md                   # Project documentation
🗑️ Các thành phần LOẠI BỎ
❌ Backend API (FastAPI)
Lý do: Sử dụng Ollama local, không cần server apps/backend phức tạp
Thay thế: Direct Ollama API calls từ extension
❌ Desktop Application (Electron)
Lý do: Tập trung vào VS Code extension là đủ
Thay thế: Extension có thể chạy độc lập
❌ PostgreSQL Database
Lý do: Agent có memory ngắn hạn, không cần database phức tạp
Thay thế: In-memory storage + file-based caching
❌ Complex Authentication
Lý do: Local Ollama không cần authentication
Thay thế: Simple API key management (nếu cần)
🎯 Core AI Agent Architecture
1. Ollama Client Layer
// src/core/ollama/client.ts
export class OllamaClient {
  private baseUrl: string;
  
  async chat(messages: ChatMessage[], options?: ChatOptions): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: options?.model || 'deepseek-coder',
        messages,
        stream: false
      })
    });
    return response.json();
  }
  
  async streamChat(messages: ChatMessage[], options?: ChatOptions): Promise<ReadableStream> {
    // Streaming implementation
  }
}
2. Cognitive Capabilities
// src/core/agent/cognitive/codeAnalyzer.ts
export class CodeAnalyzer {
  async reviewCode(code: string, context: CodeContext): Promise<CodeReview> {
    const prompt = this.buildReviewPrompt(code, context);
    const response = await ollama.chat([{ role: 'user', content: prompt }]);
    return this.parseReviewResponse(response);
  }
  
  async debugCode(error: string, code: string): Promise<DebugSolution> {
    // Debugging implementation
  }
  
  async optimizeCode(code: string, metrics: OptimizationMetrics): Promise<CodeOptimization> {
    // Optimization implementation
  }
}
3. Memory Management
// src/core/agent/memory/memoryManager.ts
export class MemoryManager {
  private contextWindow: ContextWindow;
  private longTermMemory: Map<string, any>;
  
  async getRelevantContext(query: string): Promise<RelevantContext> {
    // Semantic search through past interactions
  }
  
  async updateMemory(interaction: AgentInteraction): Promise<void> {
    // Update memory based on interaction results
  }
}
4. Action Planning
// src/core/agent/planner/actionPlanner.ts
export class ActionPlanner {
  async planActions(userRequest: string, context: AgentContext): Promise<ActionPlan> {
    const prompt = this.buildPlanningPrompt(userRequest, context);
    const response = await ollama.chat([{ role: 'user', content: prompt }]);
    return this.parseActionPlan(response);
  }
}
🛠️ Tools Implementation
Code Tools
// src/core/tools/code/codeTools.ts
export class CodeTools {
  async extractFunctions(code: string): Promise<FunctionDefinition[]> {
    // AST parsing to extract functions
  }
  
  async generateTests(code: string, framework: TestFramework): Promise<string> {
    // Test generation implementation
  }
  
  async refactorCode(code: string, pattern: RefactorPattern): Promise<string> {
    // Code refactoring implementation
  }
}
File Tools
// src/core/tools/file/fileTools.ts
export class FileTools {
  async readFile(path: string): Promise<string> {
    // File reading with error handling
  }
  
  async writeFile(path: string, content: string): Promise<void> {
    // File writing with backup
  }
  
  async findFiles(pattern: string): Promise<string[]> {
    // File search implementation
  }
}
🔌 VS Code Extension
Extension Core
// src/extension/extension.ts
export function activate(context: vscode.ExtensionContext) {
  // Register commands
  const agent = new AIAgent(context);
  
  context.subscriptions.push(
    vscode.commands.registerCommand('zeta.agent.review', () => agent.reviewCode()),
    vscode.commands.registerCommand('zeta.agent.debug', () => agent.debugCode()),
    vscode.commands.registerCommand('zeta.agent.optimize', () => agent.optimizeCode()),
    vscode.commands.registerCommand('zeta.agent.chat', () => agent.openChat())
  );
}
Language Provider
// src/extension/provider/completionProvider.ts
export class AICompletionProvider implements vscode.CompletionItemProvider {
  async provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position
  ): Promise<vscode.CompletionItem[]> {
    const context = this.buildCompletionContext(document, position);
    const suggestions = await agent.suggestCompletions(context);
    return this.convertToCompletionItems(suggestions);
  }
}
📋 Package.json Configuration
{
  "name": "apps/zeta-ai-agent",
  "displayName": "Zeta AI Agent",
  "description": "AI-powered coding assistant using Ollama",
  "version": "1.0.0",
  "engines": { "vscode": "^1.85.0" },
  "categories": ["Programming Languages", "AI"],
  "activationEvents": [
    "onCommand:zeta.agent.review",
    "onCommand:zeta.agent.debug",
    "onCommand:zeta.agent.optimize",
    "onCommand:zeta.agent.chat"
  ],
  "main": "./out/extension.js",
  "contributes": {
    "commands": [
      { "command": "zeta.agent.review", "title": "Zeta: Review Code" },
      { "command": "zeta.agent.debug", "title": "Zeta: Debug Code" },
      { "command": "zeta.agent.optimize", "title": "Zeta: Optimize Code" },
      { "command": "zeta.agent.chat", "title": "Zeta: Open AI Chat" }
    ],
    "configuration": {
      "title": "Zeta AI Agent",
      "properties": {
        "zeta.ollamaUrl": {
          "type": "string",
          "default": "http://localhost:11434",
          "description": "Ollama server URL"
        },
        "zeta.defaultModel": {
          "type": "string",
          "default": "deepseek-coder",
          "description": "Default model for code tasks"
        }
      }
    }
  },
  "scripts": {
    "compile": "tsc -p .",
    "watch": "tsc -watch -p .",
    "package": "vsce package",
    "test": "vitest run"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/vscode": "^1.85.0",
    "typescript": "^5.3.0",
    "vitest": "^1.0.0"
  }
}
🧪 Testing Strategy
Unit Tests
// tests/unit/ollamaClient.test.ts
describe('OllamaClient', () => {
  let client: OllamaClient;
  let mockFetch: jest.Mock;

  beforeEach(() => {
    mockFetch = jest.fn();
    global.fetch = mockFetch;
    client = new OllamaClient('http://localhost:11434');
  });

  test('should send chat request', async () => {
    mockFetch.mockResolvedValue(createMockResponse({ message: { content: 'test' } }));
    
    const response = await client.chat([{ role: 'user', content: 'hello' }]);
    
    expect(mockFetch).toHaveBeenCalledWith(
      'http://localhost:11434/api/chat',
      expect.any(Object)
    );
    expect(response).toEqual({ message: { content: 'test' } });
  });
});
Integration Tests
// tests/integration/agent.test.ts
describe('AIAgent', () => {
  let agent: AIAgent;
  let mockOllama: jest.Mocked<OllamaClient>;

  beforeEach(() => {
    mockOllama = {
      chat: jest.fn(),
      streamChat: jest.fn()
    } as any;
    
    agent = new AIAgent(mockOllama);
  });

  test('should review code and provide suggestions', async () => {
    const code = `function test() { return 1; }`;
    const suggestions = await agent.reviewCode(code);
    
    expect(suggestions).toHaveProperty('issues');
    expect(suggestions).toHaveProperty('suggestions');
  });
});
🚀 Deployment & Distribution
Build Process
{
  "scripts": {
    "compile": "tsc -p .",
    "watch": "tsc -watch -p .",
    "package": "vsce package",
    "publish": "vsce publish",
    "test": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
CI/CD Pipeline
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
        with: { node-version: '18' }
      - run: npm ci
      - run: npm run compile
      - run: npm test
      - run: npm run package

  release:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run package
      - uses: JS-DevTools/npm-publish@v1
        with: { token: ${{ secrets.NPM_TOKEN } }
📊 Performance Optimization
1. Caching Layer
// src/core/utils/cache.ts
export class ResponseCache {
  private cache = new Map<string, { response: any; timestamp: number }>();
  private ttl: number;

  async getOrSet(key: string, fetcher: () => Promise<any>): Promise<any> {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.response;
    }
    
    const response = await fetcher();
    this.cache.set(key, { response, timestamp: Date.now() });
    return response;
  }
}
2. Request Batching
// src/core/utils/batcher.ts
export class RequestBatcher {
  private batch: Array<{ request: any; resolve: (value: any) => void }> = [];
  private batchTimeout: NodeJS.Timeout | null = null;

  async batchRequest(request: any): Promise<any> {
    return new Promise((resolve) => {
      this.batch.push({ request, resolve });
      
      if (!this.batchTimeout) {
        this.batchTimeout = setTimeout(() => this.processBatch(), 50);
      }
    });
  }

  private async processBatch(): Promise<void> {
    const batch = this.batch;
    this.batch = [];
    this.batchTimeout = null;

    const responses = await this.sendBatch(batch.map(b => b.request));
    batch.forEach((item, index) => item.resolve(responses[index]));
  }
}
🔒 Security Considerations
1. Input Validation
// src/core/utils/validation.ts
export class InputValidator {
  static validateCodeInput(code: string): void {
    if (code.length > 100000) {
      throw new Error('Code too large');
    }
    
    if (/system\(|exec\(|eval\(/i.test(code)) {
      throw new Error('Potentially dangerous code detected');
    }
  }

  static validatePath(path: string): void {
    if (path.includes('..') || path.includes('/etc/') || path.includes('/root/')) {
      throw new Error('Invalid path');
    }
  }
}
2. Rate Limiting
// src/core/utils/rateLimiter.ts
export class RateLimiter {
  private requests = new Map<string, number[]>();
  
  checkRateLimit(key: string, limit: number, windowMs: number): boolean {
    const now = Date.now();
    const timestamps = this.requests.get(key) || [];
    const validTimestamps = timestamps.filter(ts => now - ts < windowMs);
    
    if (validTimestamps.length >= limit) {
      return false;
    }
    
    validTimestamps.push(now);
    this.requests.set(key, validTimestamps);
    return true;
  }
}
📈 Monitoring & Analytics
Performance Monitoring
// src/core/utils/monitoring.ts
export class PerformanceMonitor {
  private metrics: Map<string, number[]> = new Map();

  trackOperation(operation: string, duration: number): void {
    if (!this.metrics.has(operation)) {
      this.metrics.set(operation, []);
    }
    this.metrics.get(operation)!.push(duration);
  }

  getMetrics(): PerformanceMetrics {
    const result: PerformanceMetrics = {};
    
    for (const [operation, durations] of this.metrics) {
      result[operation] = {
        count: durations.length,
        average: durations.reduce((a, b) => a + b, 0) / durations.length,
        p95: this.calculatePercentile(durations, 95)
      };
    }
    
    return result;
  }
}
🎯 Kết luận
Cấu trúc mới này tập trung vào:

AI Agent core với Ollama integration
VS Code extension nhẹ và mạnh mẽ
Công cụ hiện đại cho code analysis và generation
Hệ thống testing toàn diện
Performance optimization và security
Đề xuất này loại bỏ 70% codebase không cần thiết, tập trung vào core functionality và đảm bảo agent hoạt động như một Copilot đầy đủ tính năng với hiệu năng cao.

đề xuất chi tiết triển khai tốt nhất
edit
Thought for 4.1 seconds








🚀 Triển khai Chi tiết Dự án Zeta AI Agent với Ollama
📋 Tổng quan Triển khai
Dưới đây là kế hoạch triển khai chi tiết từng bước cho dự án Zeta AI Agent tập trung vào Ollama, được thiết kế để tối ưu hóa hiệu suất, bảo mật và khả năng mở rộng.

🏗️ Bước 1: Thiết lập Dự án
1.1 Khởi tạo Repository
# Tạo thư mục dự án
mkdir apps/zeta-ai-agent
cd apps/zeta-ai-agent

# Khởi tạo Git
git init
echo "# Zeta AI Agent - AI-Powered Coding Assistant with Ollama" > README.md

# Khởi tạo npm
npm init -y

# Khởi tạo TypeScript
npx tsc --init
1.2 Cấu trúc Thư mục
# Tạo cấu trúc thư mục
mkdir -p src/core/ollama
mkdir -p src/core/agent/cognitive
mkdir -p src/core/agent/memory
mkdir -p src/core/agent/planner
mkdir -p src/core/tools/code
mkdir -p src/core/tools/file
mkdir -p src/core/tools/system
mkdir -p src/core/utils
mkdir -p src/extension/provider
mkdir -p src/extension/webview
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p scripts
1.3 Cài đặt Dependencies
# Production dependencies
npm install axios lodash nanoid

# Development dependencies
npm install -D @types/vscode typescript @types/node @types/lodash
npm install -D vitest @vitest/coverage-v8 jsdom @testing-library/dom
npm install -D @vscode/vsce vsce

# Global tools (optional)
npm install -g @vscode/vsce typescript
1.4 Cấu hình TypeScript
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022", "DOM"],
    "outDir": "./out",
    "rootDir": "./src",
    "strict": true,
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "out", "tests"]
}
1.5 Cấu hình npm Scripts
// package.json
{
  "scripts": {
    "compile": "tsc -p .",
    "watch": "tsc -watch -p .",
    "test": "vitest run",
    "test:watch": "vitest watch",
    "test:coverage": "vitest run --coverage",
    "package": "vsce package",
    "publish": "vsce publish",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "build": "npm run compile && npm run test",
    "prepublishOnly": "npm run build"
  }
}
🧩 Bước 2: Triển khai Core Modules
2.1 Ollama Client Implementation
// src/core/ollama/client.ts
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { EventEmitter } from 'events';

export interface OllamaOptions {
  baseUrl?: string;
  timeout?: number;
  defaultModel?: string;
}

export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface ChatOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

export interface ChatResponse {
  message: ChatMessage;
  created: Date;
  model: string;
  done: boolean;
}

export class OllamaClient extends EventEmitter {
  private client: AxiosInstance;
  private options: Required<OllamaOptions>;

  constructor(options: OllamaOptions = {}) {
    super();
    this.options = {
      baseUrl: options.baseUrl || 'http://localhost:11434',
      timeout: options.timeout || 30000,
      defaultModel: options.defaultModel || 'deepseek-coder'
    };

    this.client = axios.create({
      baseURL: this.options.baseUrl,
      timeout: this.options.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  async chat(messages: ChatMessage[], options?: ChatOptions): Promise<ChatResponse> {
    try {
      const response: AxiosResponse = await this.client.post('/api/chat', {
        model: options?.model || this.options.defaultModel,
        messages,
        temperature: options?.temperature || 0.7,
        max_tokens: options?.maxTokens || 2048,
        stream: false
      });

      return {
        ...response.data,
        created: new Date()
      };
    } catch (error) {
      throw new Error(`Ollama chat error: ${error.message}`);
    }
  }

  async *streamChat(messages: ChatMessage[], options?: ChatOptions): AsyncGenerator<string> {
    try {
      const response = await this.client.post('/api/chat', {
        model: options?.model || this.options.defaultModel,
        messages,
        temperature: options?.temperature || 0.7,
        max_tokens: options?.maxTokens || 2048,
        stream: true
      }, {
        responseType: 'stream'
      });

      for await (const chunk of response.data) {
        const data = chunk.toString();
        const lines = data.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonStr = line.slice(6);
            if (jsonStr === '[DONE]') break;
            
            try {
              const data = JSON.parse(jsonStr);
              yield data.message?.content || '';
            } catch (e) {
              // Continue processing other lines
            }
          }
        }
      }
    } catch (error) {
      throw new Error(`Ollama stream error: ${error.message}`);
    }
  }

  async listModels(): Promise<string[]> {
    try {
      const response = await this.client.get('/api/tags');
      return response.data.models.map((m: any) => m.name);
    } catch (error) {
      throw new Error(`Failed to list models: ${error.message}`);
    }
  }

  async pullModel(model: string): Promise<void> {
    try {
      await this.client.post('/api/pull', { name: model, stream: false });
    } catch (error) {
      throw new Error(`Failed to pull model ${model}: ${error.message}`);
    }
  }
}
2.2 Cognitive Capabilities Implementation
// src/core/agent/cognitive/codeAnalyzer.ts
import { OllamaClient } from '../../ollama/client';

export interface CodeContext {
  language: string;
  framework?: string;
  dependencies?: string[];
  styleGuide?: string;
}

export interface CodeIssue {
  line: number;
  column: number;
  message: string;
  severity: 'error' | 'warning' | 'info';
  suggestion: string;
}

export interface CodeReview {
  issues: CodeIssue[];
  suggestions: string[];
  summary: string;
}

export interface DebugSolution {
  cause: string;
  solution: string;
  fixedCode: string;
}

export interface CodeOptimization {
  original: string;
  optimized: string;
  improvements: string[];
  metrics: {
    timeSaved?: string;
    memorySaved?: string;
    complexityReduced?: string;
  };
}

export class CodeAnalyzer {
  private ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async reviewCode(code: string, context: CodeContext): Promise<CodeReview> {
    const prompt = this.buildReviewPrompt(code, context);
    const response = await this.ollama.chat([
      { role: 'system', content: 'You are an expert code reviewer. Provide detailed analysis and suggestions.' },
      { role: 'user', content: prompt }
    ]);

    return this.parseReviewResponse(response.message.content, code);
  }

  async debugCode(error: string, code: string, context: CodeContext): Promise<DebugSolution> {
    const prompt = this.buildDebugPrompt(error, code, context);
    const response = await this.ollama.chat([
      { role: 'system', content: 'You are a debugging expert. Analyze errors and provide solutions.' },
      { role: 'user', content: prompt }
    ]);

    return this.parseDebugResponse(response.message.content);
  }

  async optimizeCode(code: string, context: CodeContext, metrics: string[]): Promise<CodeOptimization> {
    const prompt = this.buildOptimizationPrompt(code, context, metrics);
    const response = await this.ollama.chat([
      { role: 'system', content: 'You are a performance optimization expert. Optimize code for better performance.' },
      { role: 'user', content: prompt }
    ]);

    return this.parseOptimizationResponse(response.message.content, code);
  }

  private buildReviewPrompt(code: string, context: CodeContext): string {
    return `
Code Review Request:
Language: ${context.language}
Framework: ${context.framework || 'None'}
Dependencies: ${context.dependencies?.join(', ') || 'None'}
Style Guide: ${context.styleGuide || 'Standard'}

Code to Review:
\`\`\`${context.language}
${code}
\`\`\`

Please provide:
1. Code issues with line numbers and severity
2. Specific suggestions for improvement
3. Overall summary
`;
  }

  private parseReviewResponse(response: string, originalCode: string): CodeReview {
    // Implementation for parsing LLM response
    // This would include sophisticated parsing logic
    return {
      issues: [],
      suggestions: [],
      summary: ''
    };
  }

  // Similar implementations for debug and optimization methods
}
2.3 Memory Management Implementation
// src/core/agent/memory/memoryManager.ts
import { EmbeddingCalculator } from '../utils/embeddingCalculator';

export interface AgentInteraction {
  timestamp: Date;
  type: 'code_review' | 'debug' | 'optimization' | 'chat';
  input: string;
  output: string;
  context: any;
  success: boolean;
}

export interface RelevantContext {
  interactions: AgentInteraction[];
  relatedCode?: string;
  suggestions?: string[];
}

export class MemoryManager {
  private interactions: AgentInteraction[] = [];
  private embeddingCalculator: EmbeddingCalculator;
  private maxInteractions: number = 1000;

  constructor() {
    this.embeddingCalculator = new EmbeddingCalculator();
  }

  async addInteraction(interaction: AgentInteraction): Promise<void> {
    this.interactions.push(interaction);
    
    // Maintain memory limit
    if (this.interactions.length > this.maxInteractions) {
      this.interactions = this.interactions.slice(-this.maxInteractions);
    }
  }

  async getRelevantContext(query: string, limit: number = 5): Promise<RelevantContext> {
    const queryEmbedding = await this.embeddingCalculator.calculateEmbedding(query);
    
    // Find similar past interactions
    const scoredInteractions = await Promise.all(
      this.interactions.map(async (interaction) => {
        const similarity = await this.embeddingCalculator.calculateSimilarity(
          queryEmbedding,
          await this.embeddingCalculator.calculateEmbedding(interaction.input)
        );
        return { interaction, similarity };
      })
    );

    // Sort by similarity and take top N
    const relevant = scoredInteractions
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, limit)
      .map(item => item.interaction);

    return {
      interactions: relevant,
      suggestions: this.generateSuggestions(relevant)
    };
  }

  private generateSuggestions(interactions: AgentInteraction[]): string[] {
    // Generate context-aware suggestions based on history
    return [];
  }

  async saveToDisk(path: string): Promise<void> {
    // Save memory to disk for persistence
    const data = JSON.stringify({
      interactions: this.interactions,
      savedAt: new Date().toISOString()
    });
    
    await require('fs').promises.writeFile(path, data);
  }

  async loadFromDisk(path: string): Promise<void> {
    try {
      const data = await require('fs').promises.readFile(path, 'utf8');
      const parsed = JSON.parse(data);
      this.interactions = parsed.interactions.map((i: any) => ({
        ...i,
        timestamp: new Date(i.timestamp)
      }));
    } catch (error) {
      console.warn('Failed to load memory from disk:', error);
    }
  }
}
2.4 Action Planning Implementation
// src/core/agent/planner/actionPlanner.ts
import { OllamaClient } from '../../ollama/client';

export interface ActionStep {
  type: 'code_analysis' | 'file_operation' | 'tool_use' | 'user_query';
  description: string;
  parameters: any;
  expectedOutcome: string;
}

export interface ActionPlan {
  goal: string;
  steps: ActionStep[];
  estimatedTime: number;
  confidence: number;
}

export class ActionPlanner {
  private ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async planActions(userRequest: string, context: any): Promise<ActionPlan> {
    const prompt = this.buildPlanningPrompt(userRequest, context);
    
    const response = await this.ollama.chat([
      { 
        role: 'system', 
        content: `You are an AI action planner. Break down requests into executable steps. 
                 Respond with JSON format only.` 
      },
      { role: 'user', content: prompt }
    ]);

    return this.parseActionPlan(response.message.content);
  }

  private buildPlanningPrompt(userRequest: string, context: any): string {
    return `
User Request: ${userRequest}

Available Context:
- Language: ${context.language}
- Framework: ${context.framework || 'None'}
- Dependencies: ${context.dependencies?.join(', ') || 'None'}
- Recent Files: ${context.recentFiles?.join(', ') || 'None'}

Please create a detailed action plan with:
1. Clear goal description
2. Sequential steps with types and parameters
3. Estimated time requirement
4. Confidence level (0-100)

Respond with JSON only:
{
  "goal": "string",
  "steps": [
    {
      "type": "string",
      "description": "string",
      "parameters": {},
      "expectedOutcome": "string"
    }
  ],
  "estimatedTime": number,
  "confidence": number
}
`;
  }

  private parseActionPlan(response: string): ActionPlan {
    try {
      const cleanResponse = response.replace(/```json\n?|\n?```/g, '');
      return JSON.parse(cleanResponse);
    } catch (error) {
      throw new Error(`Failed to parse action plan: ${error.message}`);
    }
  }
}
🔌 Bước 3: Triển khai VS Code Extension
3.1 Extension Entry Point
// src/extension/extension.ts
import * as vscode from 'vscode';
import { OllamaClient } from '../core/ollama/client';
import { CodeAnalyzer } from '../core/agent/cognitive/codeAnalyzer';
import { MemoryManager } from '../core/agent/memory/memoryManager';
import { ActionPlanner } from '../core/agent/planner/actionPlanner';
import { ChatProvider } from './provider/chatProvider';

export class AIAgent {
  private ollama: OllamaClient;
  private codeAnalyzer: CodeAnalyzer;
  private memoryManager: MemoryManager;
  private actionPlanner: ActionPlanner;
  private chatProvider: ChatProvider;

  constructor(private context: vscode.ExtensionContext) {
    this.ollama = new OllamaClient();
    this.codeAnalyzer = new CodeAnalyzer(this.ollama);
    this.memoryManager = new MemoryManager();
    this.actionPlanner = new ActionPlanner(this.ollama);
    this.chatProvider = new ChatProvider(this.ollama, this.memoryManager);
  }

  async activate(): Promise<void> {
    // Initialize components
    await this.memoryManager.loadFromDisk(this.context.globalStorageUri.fsPath + '/memory.json');

    // Register commands
    this.registerCommands();

    // Register providers
    this.registerProviders();

    // Start periodic memory saving
    this.setupMemoryPersistence();
  }

  private registerCommands(): void {
    const commands = [
      vscode.commands.registerCommand('zeta.agent.review', () => this.reviewCode()),
      vscode.commands.registerCommand('zeta.agent.debug', () => this.debugCode()),
      vscode.commands.registerCommand('zeta.agent.optimize', () => this.optimizeCode()),
      vscode.commands.registerCommand('zeta.agent.chat', () => this.openChat()),
      vscode.commands.registerCommand('zeta.agent.plan', () => this.planActions())
    ];

    this.context.subscriptions.push(...commands);
  }

  private registerProviders(): void {
    // Register completion provider
    const completionProvider = vscode.languages.registerCompletionItemProvider(
      { pattern: '**' },
      {
        provideCompletionItems: async (document, position) => {
          return this.chatProvider.provideCompletionItems(document, position);
        }
      }
    );

    this.context.subscriptions.push(completionProvider);
  }

  private setupMemoryPersistence(): void {
    // Save memory every 5 minutes
    setInterval(async () => {
      await this.memoryManager.saveToDisk(
        this.context.globalStorageUri.fsPath + '/memory.json'
      );
    }, 5 * 60 * 1000);
  }

  async reviewCode(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active editor');
      return;
    }

    const code = editor.document.getText();
    const context = await this.getCodeContext(editor.document);

    try {
      const review = await this.codeAnalyzer.reviewCode(code, context);
      this.showReviewResults(review);
    } catch (error) {
      vscode.window.showErrorMessage(`Review failed: ${error.message}`);
    }
  }

  private async getCodeContext(document: vscode.TextDocument): Promise<any> {
    // Extract context from document
    return {
      language: document.languageId,
      fileName: document.fileName,
      lineCount: document.lineCount
    };
  }

  private showReviewResults(review: any): void {
    // Implement results display
    const panel = vscode.window.createWebviewPanel(
      'codeReview',
      'Code Review Results',
      vscode.ViewColumn.Beside,
      { enableScripts: true }
    );

    panel.webview.html = this.getReviewHtml(review);
  }

  private getReviewHtml(review: any): string {
    // Generate HTML content for review results
    return `
      <html>
        <body>
          <h1>Code Review Results</h1>
          <pre>${JSON.stringify(review, null, 2)}</pre>
        </body>
      </html>
    `;
  }

  // Implement other methods similarly...
}

export function activate(context: vscode.ExtensionContext) {
  const agent = new AIAgent(context);
  agent.activate();
}

export function deactivate() {
  // Cleanup resources
}
3.2 Chat Provider Implementation
// src/extension/provider/chatProvider.ts
import * as vscode from 'vscode';
import { OllamaClient } from '../../core/ollama/client';
import { MemoryManager } from '../../core/agent/memory/memoryManager';

export class ChatProvider implements vscode.CompletionItemProvider {
  constructor(
    private ollama: OllamaClient,
    private memoryManager: MemoryManager
  ) {}

  async provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position
  ): Promise<vscode.CompletionItem[]> {
    const context = await this.buildCompletionContext(document, position);
    const suggestions = await this.generateCompletions(context);
    
    return suggestions.map(suggestion => {
      const item = new vscode.CompletionItem(suggestion.label, vscode.CompletionItemKind.Snippet);
      item.insertText = new vscode.SnippetString(suggestion.code);
      item.documentation = new vscode.MarkdownString(suggestion.documentation);
      return item;
    });
  }

  private async buildCompletionContext(
    document: vscode.TextDocument,
    position: vscode.Position
  ): Promise<any> {
    const textBefore = document.getText(
      new vscode.Range(new vscode.Position(0, 0), position)
    );
    
    const textAfter = document.getText(
      new vscode.Range(position, document.positionAt(document.getText().length))
    );

    return {
      language: document.languageId,
      textBefore,
      textAfter,
      line: position.line,
      character: position.character,
      fileName: document.fileName
    };
  }

  private async generateCompletions(context: any): Promise<any[]> {
    const prompt = this.buildCompletionPrompt(context);
    const relevantContext = await this.memoryManager.getRelevantContext(prompt);
    
    const response = await this.ollama.chat([
      {
        role: 'system',
        content: `You are a code completion expert. Provide relevant code suggestions.
                 Available context: ${JSON.stringify(relevantContext)}`
      },
      { role: 'user', content: prompt }
    ]);

    return this.parseCompletionResponse(response.message.content);
  }

  private buildCompletionPrompt(context: any): string {
    return `
Complete the code at line ${context.line}, character ${context.character}:

File: ${context.fileName}
Language: ${context.language}

Code before cursor:
${context.textBefore}

Code after cursor:
${context.textAfter}

Provide 3 completion suggestions in JSON format:
[
  {
    "label": "suggestion description",
    "code": "completion code",
    "documentation": "markdown documentation"
  }
]
`;
  }

  private parseCompletionResponse(response: string): any[] {
    try {
      const cleanResponse = response.replace(/```json\n?|\n?```/g, '');
      return JSON.parse(cleanResponse);
    } catch (error) {
      return [];
    }
  }
}
🧪 Bước 4: Testing Strategy
4.1 Unit Tests
// tests/unit/ollamaClient.test.ts
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { OllamaClient } from '../../src/core/ollama/client';
import axios from 'axios';

vi.mock('axios');

describe('OllamaClient', () => {
  let client: OllamaClient;
  const mockAxios = axios as vi.Mocked<typeof axios>;

  beforeEach(() => {
    client = new OllamaClient();
    vi.clearAllMocks();
  });

  test('should initialize with default options', () => {
    expect(client).toBeInstanceOf(OllamaClient);
  });

  test('should send chat request correctly', async () => {
    const mockResponse = {
      data: {
        message: { content: 'Test response' },
        model: 'test-model',
        done: true
      }
    };

    mockAxios.post.mockResolvedValue(mockResponse);

    const messages = [{ role: 'user' as const, content: 'Hello' }];
    const response = await client.chat(messages);

    expect(mockAxios.post).toHaveBeenCalledWith(
      '/api/chat',
      expect.objectContaining({
        messages,
        stream: false
      })
    );
    expect(response.message.content).toBe('Test response');
  });

  test('should handle chat errors', async () => {
    mockAxios.post.mockRejectedValue(new Error('Network error'));

    await expect(client.chat([{ role: 'user', content: 'Hello' }]))
      .rejects
      .toThrow('Ollama chat error: Network error');
  });
});
4.2 Integration Tests
// tests/integration/codeAnalyzer.test.ts
import { describe, test, expect, beforeEach, vi } from 'vitest';
import { CodeAnalyzer } from '../../src/core/agent/cognitive/codeAnalyzer';
import { OllamaClient } from '../../src/core/ollama/client';

vi.mock('../../src/core/ollama/client');

describe('CodeAnalyzer', () => {
  let analyzer: CodeAnalyzer;
  let mockOllama: vi.Mocked<OllamaClient>;

  beforeEach(() => {
    mockOllama = new OllamaClient() as vi.Mocked<OllamaClient>;
    analyzer = new CodeAnalyzer(mockOllama);
  });

  test('should review code successfully', async () => {
    const mockResponse = {
      message: {
        content: JSON.stringify({
          issues: [],
          suggestions: ['Add comments'],
          summary: 'Good code'
        })
      }
    };

    mockOllama.chat.mockResolvedValue(mockResponse as any);

    const review = await analyzer.reviewCode('function test() { return 1; }', {
      language: 'javascript'
    });

    expect(review.suggestions).toContain('Add comments');
    expect(mockOllama.chat).toHaveBeenCalled();
  });

  test('should handle review errors', async () => {
    mockOllama.chat.mockRejectedValue(new Error('Model not found'));

    await expect(
      analyzer.reviewCode('function test() { return 1; }', {
        language: 'javascript'
      })
    ).rejects.toThrow();
  });
});
📦 Bước 5: Build và Packaging
5.1 Build Configuration
// package.json (additional configurations)
{
  "main": "./out/extension.js",
  "activationEvents": [
    "onCommand:zeta.agent.review",
    "onCommand:zeta.agent.debug",
    "onCommand:zeta.agent.optimize",
    "onCommand:zeta.agent.chat",
    "onCommand:zeta.agent.plan"
  ],
  "contributes": {
    "commands": [
      {
        "command": "zeta.agent.review",
        "title": "Zeta: Review Code",
        "category": "Zeta AI"
      },
      {
        "command": "zeta.agent.debug",
        "title": "Zeta: Debug Code",
        "category": "Zeta AI"
      },
      {
        "command": "zeta.agent.optimize",
        "title": "Zeta: Optimize Code",
        "category": "Zeta AI"
      },
      {
        "command": "zeta.agent.chat",
        "title": "Zeta: Open AI Chat",
        "category": "Zeta AI"
      },
      {
        "command": "zeta.agent.plan",
        "title": "Zeta: Plan Actions",
        "category": "Zeta AI"
      }
    ],
    "configuration": {
      "title": "Zeta AI Agent",
      "properties": {
        "zeta.ollamaUrl": {
          "type": "string",
          "default": "http://localhost:11434",
          "description": "Ollama server URL"
        },
        "zeta.defaultModel": {
          "type": "string",
          "default": "deepseek-coder",
          "description": "Default model for code tasks"
        },
        "zeta.enableTelemetry": {
          "type": "boolean",
          "default": true,
          "description": "Enable telemetry collection"
        }
      }
    }
  }
}
5.2 Build Scripts
#!/bin/bash
# scripts/build.sh

echo "Building Zeta AI Agent..."

# Clean previous builds
rm -rf out
rm -f *.vsix

# Compile TypeScript
echo "Compiling TypeScript..."
npm run compile

# Run tests
echo "Running tests..."
npm run test

# Package extension
echo "Packaging extension..."
npm run package

echo "Build completed successfully!"
🚀 Bước 6: Deployment và CI/CD
6.1 GitHub Actions CI
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
    - name: Run linting
      run: npm run lint
    
    - name: Build package
      run: npm run build

  release:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - run: npm ci
    - run: npm run package
    
    - name: Publish to VS Marketplace
      run: npx vsce publish -p ${{ secrets.VSCE_TOKEN }}
6.2 Docker Configuration
# Dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy built code
COPY out/ ./out/

# Install vsce globally
RUN npm install -g @vscode/vsce

# Set default command
CMD ["npm", "run", "package"]
📊 Monitoring và Analytics
7.1 Performance Monitoring
// src/core/utils/monitoring.ts
export interface PerformanceMetrics {
  [key: string]: {
    count: number;
    average: number;
    p95: number;
    errors: number;
  };
}

export class PerformanceMonitor {
  private metrics: Map<string, number[]> = new Map();
  private errors: Map<string, number> = new Map();

  trackOperation(operation: string, duration: number): void {
    if (!this.metrics.has(operation)) {
      this.metrics.set(operation, []);
    }
    this.metrics.get(operation)!.push(duration);
  }

  trackError(operation: string): void {
    this.errors.set(operation, (this.errors.get(operation) || 0) + 1);
  }

  getMetrics(): PerformanceMetrics {
    const result: PerformanceMetrics = {};
    
    for (const [operation, durations] of this.metrics) {
      const sorted = durations.sort((a, b) => a - b);
      const p95Index = Math.floor(sorted.length * 0.95);
      
      result[operation] = {
        count: durations.length,
        average: durations.reduce((a, b) => a + b, 0) / durations.length,
        p95: sorted[p95Index],
        errors: this.errors.get(operation) || 0
      };
    }
    
    return result;
  }

  generateReport(): string {
    const metrics = this.getMetrics();
    return JSON.stringify(metrics, null, 2);
  }
}
🔒 Security Considerations
8.1 Security Implementation
// src/core/utils/security.ts
export class SecurityValidator {
  static validateCode(code: string): void {
    const dangerousPatterns = [
      /system\(/i,
      /exec\(/i,
      /eval\(/i,
      /child_process/i,
      /fs\.promises/i,
      /require\(/i,
      /process\.env/i
    ];

    for (const pattern of dangerousPatterns) {
      if (pattern.test(code)) {
        throw new Error(`Potentially dangerous code pattern detected: ${pattern}`);
      }
    }

    if (code.length > 100000) {
      throw new Error('Code exceeds maximum allowed size');
    }
  }

  static validatePath(path: string): void {
    const forbiddenPatterns = [
      /\.\.\//, // Path traversal
      /\/etc\//,
      /\/root\//,
      /\/proc\//,
      /\/sys\//
    ];

    for (const pattern of forbiddenPatterns) {
      if (pattern.test(path)) {
        throw new Error(`Forbidden path pattern: ${pattern}`);
      }
    }
  }

  static sanitizeInput(input: string): string {
    return input
      .replace(/[<>]/g, '')
      .replace(/javascript:/gi, '')
      .replace(/onerror/gi, '')
      .replace(/onload/gi, '')
      .slice(0, 10000); // Limit input length
  }
}
🎯 Kết luận
Triển khai này cung cấp một hệ thống đầy đủ cho Zeta AI Agent với:

**Kiến trúc module rõ r
