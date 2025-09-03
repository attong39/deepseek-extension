// SPDX-License-Identifier: MIT
 
import * as vscode from 'vscode';

interface OllamaMessage { 
  role: 'system' | 'user' | 'assistant'; 
  content: string;
}

type Lang = 'ts' | 'py';
type InsertPosition = 'above' | 'below';
type TaskType = 'review' | 'debug' | 'optimize';

interface AgentPlan {
  summary: string;
  rationale?: string;
  actions: Array<{
    type: 'upsert_file' | 'append' | 'replace' | 'insert' | 'optimize_imports';
    path?: string; 
    content?: string;
    pattern?: string;
    replacement?: string;
    flags?: string;
    anchor?: string;
    position?: InsertPosition;
    language?: Lang;
  }>;
}

interface AgentAction {
  type: 'upsert_file' | 'append' | 'replace' | 'insert' | 'optimize_imports';
  path: string; 
  content?: string;
  pattern?: string;
  replacement?: string;
  flags?: string;
  anchor?: string;
  position?: InsertPosition;
  language?: Lang;
}

/** ===== Ollama Service ===== */
export class OllamaService {
  constructor(
    private readonly baseUrl = 'http://127.0.0.1:11434',
    private readonly model = 'deepseek-r1:latest'
  ) {}

  async chat(messages: OllamaMessage[], stream = false): Promise<string> {
    try {
      const res = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ model: this.model, messages, stream })
      });
      
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      }
      const data = await res.json();
      return data.message?.content || '';
    } catch (e) {
      console.error('Ollama connection failed:', e);
      throw e;
    }
  }
}

/** ===== Main AI Agent Class ===== */
export class AIAgent {
  private readonly outputChannel: vscode.OutputChannel;
  private ollamaSvc: OllamaService;
  private model: string;

  constructor(private readonly context: vscode.ExtensionContext, name = 'DeepSeek Agent') {
    this.outputChannel = vscode.window.createOutputChannel(name);
    
    // 1. Lấy model đã được lưu (nếu có) hoặc mặc định (deepseek-r1:latest)
    this.model = this.context.globalState.get('deepseek.model', 'deepseek-r1:latest');
    
    // Khởi tạo OllamaService với model này
    this.ollamaSvc = new OllamaService(undefined, this.model);
  }

  /** Update model when user changes selection */
  updateModel(): void {
    const newModel = this.context.globalState.get('deepseek.model', 'deepseek-r1:latest');
    if (newModel !== this.model) {
      this.model = newModel;
      this.ollamaSvc = new OllamaService(undefined, newModel);
      this.outputChannel.appendLine(`Model updated to: ${newModel}`);
    }
  }

  private getRoot(): vscode.Uri {
    const f = vscode.workspace.workspaceFolders?.[0];
    if (!f) {
      throw new Error('No workspace folder found');
    }
    return f.uri;
  }

  /** Infer task type từ prompt */
  inferTask(prompt: string): TaskType {
    const p = (prompt || '').toLowerCase();
    if (p.includes('debug') || p.includes('sửa lỗi') || p.includes('fix')) {
      return 'debug';
    }
    if (p.includes('optimize') || p.includes('tối ưu') || p.includes('refactor')) {
      return 'optimize';
    }
    return 'review';
  }

  /** Thu thập context từ workspace */
  private async collectContext(uris: vscode.Uri[]): Promise<string> {
    let content = '';
    for (const uri of uris.slice(0, 40)) {
      try {
        const bin = await vscode.workspace.fs.readFile(uri);
        const text = new TextDecoder().decode(bin);
        const relativePath = vscode.workspace.asRelativePath(uri, false);
        content += `// FILE: ${relativePath}\n${text}\n\n`;
        
        // Limit context size
        if (content.length > 40000) {
          break;
        }
      } catch {
        content += `// FILE: ${vscode.workspace.asRelativePath(uri, false)} (unreadable)\n\n`;
      }
    }
    
    return content || 'No files could be read';
  }

  /** Extract JSON từ markdown response */
  private extractJsonFromMarkdown(text: string): string | null {
    const jsonMatch = /```json\s*([\s\S]+?)\s*```/i.exec(text);
    if (jsonMatch) {
      return jsonMatch[1];
    }
    
    // Fallback: tìm object JSON đầu tiên
    const objMatch = /({[\s\S]*})/.exec(text);
    return objMatch ? objMatch[1] : null;
  }

  /** Parse plan từ AI response */
  private parsePlan(text: string): AgentPlan | null {
    const jsonBlock = this.extractJsonFromMarkdown(text);
    if (!jsonBlock) {
      this.outputChannel.appendLine('No JSON found in response');
      return null;
    }
    
    try {
      const parsed = JSON.parse(jsonBlock);
      
      // Validate structure
      if (typeof parsed.summary !== 'string') {
        throw new Error('"summary" must be string');
      }
      if (!Array.isArray(parsed.actions)) {
        throw new Error('"actions" must be array');
      }
      
      // Validate actions
      const validActions: AgentAction[] = [];
      for (const action of parsed.actions) {
        if (this.validateAction(action)) {
          validActions.push(action as AgentAction);
        }
      }
      
      return {
        summary: parsed.summary,
        rationale: parsed.rationale,
        actions: validActions
      } as AgentPlan;
    } catch (e) {
      this.outputChannel.appendLine(`JSON parse error: ${e}`);
      return null;
    }
  }

  /** Validate action structure */
  private validateAction(action: unknown): action is AgentAction {
    if (typeof action !== 'object' || action === null) {
      return false;
    }
    
    const obj = action as Record<string, unknown>;
    if (typeof obj.type !== 'string' || typeof obj.path !== 'string') {
      return false;
    }
    
    switch (obj.type) {
      case 'upsert_file':
      case 'append':
        return typeof obj.content === 'string';
      case 'replace':
        return typeof obj.pattern === 'string' && obj.replacement !== undefined;
      case 'insert':
        return typeof obj.anchor === 'string' && 
               typeof obj.content === 'string' && 
               (obj.position === 'above' || obj.position === 'below');
      case 'optimize_imports':
        return obj.language === 'ts' || obj.language === 'py';
      default:
        return false;
    }
  }

  /** Normalize path để tránh path traversal */
  private normalizePath(filePath: string): string {
    return filePath.replace(/^\.\//, '').replace(/\.\./g, '');
  }

  /** Execute single action */
  private async executeAction(action: AgentAction): Promise<boolean> {
    if (!action.path || action.path.includes('..')) {
      return false;
    }
    
    try {
      const rootUri = this.getRoot();
      const targetUri = vscode.Uri.joinPath(rootUri, this.normalizePath(action.path));
      const edit = new vscode.WorkspaceEdit();
      
      const readFile = async (): Promise<string> => {
        try {
          return new TextDecoder().decode(await vscode.workspace.fs.readFile(targetUri));
        } catch {
          return '';
        }
      };
      
      const writeFile = (content: string) => {
        edit.replace(targetUri, new vscode.Range(0, 0, 1e9, 1e9), content);
      };

      switch (action.type) {
        case 'upsert_file':
          if (action.content !== undefined) {
            // Ensure file exists
            try {
              await vscode.workspace.fs.stat(targetUri);
            } catch {
              await vscode.workspace.fs.writeFile(targetUri, new Uint8Array());
            }
            writeFile(action.content);
          }
          break;
          
        case 'append':
          if (action.content !== undefined) {
            const current = await readFile();
            writeFile(current + (current.endsWith('\n') ? '' : '\n') + action.content);
          }
          break;
          
        case 'replace':
          if (action.pattern && action.replacement !== undefined) {
            const current = await readFile();
            const regex = new RegExp(action.pattern, action.flags ?? 'gms');
            writeFile(current.replace(regex, action.replacement));
          }
          break;
          
        case 'insert':
          if (action.anchor && action.content !== undefined && action.position) {
            const current = await readFile();
            const idx = current.indexOf(action.anchor);
            if (idx >= 0) {
              const before = current.slice(0, idx);
              const after = current.slice(idx + action.anchor.length);
              const newContent = action.position === 'above'
                ? `${before}${action.content}\n${action.anchor}${after}`
                : `${before}${action.anchor}\n${action.content}${after}`;
              writeFile(newContent);
            }
          }
          break;
          
        case 'optimize_imports':
          if (action.language) {
            const current = await readFile();
            const optimized = this.optimizeImports(current, action.language);
            writeFile(optimized);
          }
          break;
      }

      const success = await vscode.workspace.applyEdit(edit);
      if (success) {
        await vscode.workspace.saveAll();
        this.outputChannel.appendLine(`✅ Applied ${action.type} on ${action.path}`);
      }
      
      return success;
    } catch (error) {
      this.outputChannel.appendLine(`❌ Failed ${action.type} on ${action.path}: ${error}`);
      return false;
    }
  }

  /** Optimize imports based on language */
  private optimizeImports(code: string, language: Lang): string {
    const lines = code.split('\n');
    
    if (language === 'ts') {
      const isImport = (l: string) => 
        /^\s*import\s.+from\s+['"].+['"];?\s*$/.test(l) || 
        /^\s*import\s+['"].+['"];?\s*$/.test(l);
      
      const imports = lines.filter(isImport).map(s => s.trim());
      const others = lines.filter(l => !isImport(l));
      const unique = Array.from(new Set(imports)).sort((a, b) => a.localeCompare(b));
      
      return [...unique, '', ...others].join('\n');
    } else if (language === 'py') {
      const isImport = (l: string) => /^\s*(from\s+\S+\s+import\s+.+|import\s+\S+)/.test(l);
      
      const imports = lines.filter(isImport).map(s => s.trim());
      const others = lines.filter(l => !isImport(l));
      const unique = Array.from(new Set(imports)).sort((a, b) => a.localeCompare(b));
      
      return [...unique, '', ...others].join('\n');
    }
    
    return code;
  }

  /** Get system prompt based on task type */
  private getSystemPrompt(taskType: TaskType): string {
    const goals = {
      review: 'Review code, phát hiện vấn đề & đề xuất sửa nhỏ.',
      debug: 'Chuẩn đoán lỗi rõ ràng và đề xuất sửa tối thiểu.',
      optimize: 'Tối ưu import, loại trùng lặp, cải thiện cấu trúc.'
    };

    return [
      'Bạn là DeepSeek R1 chạy local qua Ollama. Trả lời DUY NHẤT JSON (đặt trong ```json ... ```).',
      'Schema:',
      '{',
      '  "summary": "...",',
      '  "rationale": "...",',
      '  "actions": [',
      '    {"type":"upsert_file","path":"src/file.ts","content":"..."},',
      '    {"type":"append","path":"src/a.ts","content":"..."},',
      '    {"type":"replace","path":"src/b.ts","pattern":"regex","replacement":"...","flags":"gms"},',
      '    {"type":"insert","path":"src/c.ts","anchor":"export ...","position":"above","content":"..."},',
      '    {"type":"optimize_imports","path":"src/d.ts","language":"ts"}',
      '  ]',
      '}',
      'Nguyên tắc: thay đổi nhỏ, an toàn, không xoá logic nếu không chắc.',
      `Mục tiêu: ${goals[taskType]}`
    ].join('\n');
  }

  /** Main run task function */
  async runTask(taskType: TaskType, files?: string[]): Promise<AgentPlan> {
    try {
      this.outputChannel.appendLine(`🎯 Starting ${taskType} task`);
      
      // Thu thập ngữ cảnh
      let contextText: string;
      if (files && files.length) {
        const uris = files.map(f => vscode.Uri.file(f));
        contextText = await this.collectContext(uris);
      } else {
        const uris = await vscode.workspace.findFiles('**/*.{ts,tsx,py}', '**/node_modules/**', 30);
        contextText = await this.collectContext(uris);
      }

      // Gọi AI
      const systemPrompt = this.getSystemPrompt(taskType);
      const rawPlan = await this.ollamaSvc.chat([
        { role: 'system', content: systemPrompt },
        { role: 'user', content: contextText }
      ]);

      // Parse và thực hiện
      const plan = this.parsePlan(rawPlan);
      if (!plan) {
        throw new Error('Could not parse plan from AI response');
      }

      let appliedCount = 0;
      for (const action of plan.actions) {
        const success = await this.executeAction(action as AgentAction);
        if (success) {
          appliedCount++;
        }
      }
      
      this.outputChannel.appendLine(`✅ Completed: ${plan.summary}`);
      this.outputChannel.appendLine(`📊 Applied ${appliedCount}/${plan.actions.length} actions`);
      
      return plan;
      
    } catch (error) {
      this.outputChannel.appendLine(`❌ Error: ${error}`);
      console.error('Error running AI task:', error);
      throw error;
    }
  }

  /** Interactive prompt mode */
  async interactiveMode(): Promise<void> {
    const input = await vscode.window.showInputBox({
      prompt: 'Nhập yêu cầu cho AI Agent (vd: "review code", "optimize imports", "fix bugs")',
      placeHolder: 'review all files'
    });

    if (!input) {
      return;
    }

    const taskType = this.inferTask(input);
    this.outputChannel.appendLine(`🎯 Inferred task: ${taskType} from input: "${input}"`);
    
    await this.runTask(taskType);
    this.outputChannel.show(true);
  }

  /** Run task on active file */
  async runTaskOnActiveFile(taskType: TaskType): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active file');
      return;
    }

    const filePath = editor.document.uri.fsPath;
    await this.runTask(taskType, [filePath]);
    this.outputChannel.show(true);
  }

  /** Show agent status */
  async showStatus(): Promise<void> {
    try {
      // Test Ollama connection
      await this.ollamaSvc.chat([
        { role: 'user', content: 'Test connection. Reply with "OK"' }
      ]);
      
      vscode.window.showInformationMessage('✅ AI Agent ready! Ollama connected.');
    } catch (error) {
      vscode.window.showErrorMessage(`❌ AI Agent not ready: ${error}`);
    }
  }
}
