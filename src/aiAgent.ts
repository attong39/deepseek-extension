import * as vscode from 'vscode';
import * as path from 'path';
import { IAIAgent, IOllamaClient, AgentPlan, AgentAction, ContextFile, OllamaMessage } from './types';
import { Config } from './config';
import { OllamaClient } from './ollamaClient';

/**
 * AI Agent for understanding and modifying VS Code workspace
 */
export class AIAgent implements IAIAgent {
    private client: IOllamaClient;
    private config: Config;
    private output: vscode.OutputChannel;
    
    constructor() {
        this.client = new OllamaClient();
        this.config = Config.getInstance();
        this.output = vscode.window.createOutputChannel('DeepSeek Agent');
    }
    
    /**
     * Run an AI task with optional file URIs
     */
    async runTask(goal: string, uris?: string[]): Promise<AgentPlan> {
        this.output.show();
        this.output.appendLine(`🚀 Starting task: ${goal}`);
        
        try {
            // Collect context from workspace
            const context = await this.collectContext(uris);
            
            // Create system prompt
            const systemPrompt = this.createSystemPrompt(goal);
            
            // Create user prompt with context
            const userPrompt = this.createUserPrompt(goal, context);
            
            this.output.appendLine(`📝 System prompt length: ${systemPrompt.length} chars`);
            this.output.appendLine(`📝 User prompt length: ${userPrompt.length} chars`);
            
            // Send to AI
            const messages: OllamaMessage[] = [
                { role: 'system', content: systemPrompt },
                { role: 'user', content: userPrompt }
            ];
            
            const response = await this.client.chat(messages);
            const filteredResponse = OllamaClient.filterThinkTags(response);
            
            this.output.appendLine(`🤖 AI Response:\n${filteredResponse}`);
            
            // Parse the plan
            const plan = this.parsePlan(filteredResponse);
            
            this.output.appendLine(`📋 Plan summary: ${plan.summary}`);
            this.output.appendLine(`📋 Actions count: ${plan.actions.length}`);
            
            return plan;
            
        } catch (error) {
            const errorMsg = `❌ Task failed: ${error instanceof Error ? error.message : String(error)}`;
            this.output.appendLine(errorMsg);
            throw new Error(errorMsg);
        }
    }
    
    /**
     * Review the currently active file
     */
    async reviewActiveFile(): Promise<AgentPlan> {
        const activeEditor = vscode.window.activeTextEditor;
        if (!activeEditor) {
            throw new Error('No active file to review');
        }
        
        const fileUri = activeEditor.document.uri.fsPath;
        return this.runTask('Review code, phát hiện vấn đề và đề xuất sửa', [fileUri]);
    }
    
    /**
     * Run continuous optimization with multiple iterations
     */
    async continuous(maxIterations: number = 3): Promise<void> {
        this.output.appendLine(`🔄 Starting continuous optimization (max ${maxIterations} iterations)`);
        
        for (let i = 0; i < maxIterations; i++) {
            this.output.appendLine(`\n--- Iteration ${i + 1}/${maxIterations} ---`);
            
            try {
                const plan = await this.runTask(`Iteration ${i + 1}: Continuous code improvement and optimization`);
                
                if (plan.actions.length === 0) {
                    this.output.appendLine(`✅ No more improvements needed. Stopping at iteration ${i + 1}.`);
                    break;
                }
                
                // Apply or confirm plan
                if (this.config.getAutoApply()) {
                    await this.applyActions(plan.actions);
                } else {
                    await this.confirmAndApply(plan);
                }
                
            } catch (error) {
                this.output.appendLine(`❌ Iteration ${i + 1} failed: ${error instanceof Error ? error.message : String(error)}`);
                break;
            }
        }
        
        this.output.appendLine(`🏁 Continuous optimization completed`);
    }
    
    /**
     * Collect context from workspace files
     */
    private async collectContext(uris?: string[]): Promise<string> {
        const maxBytes = this.config.getMaxContextBytes();
        const files: ContextFile[] = [];
        let totalBytes = 0;
        
        try {
            let filesToProcess: vscode.Uri[] = [];
            
            if (uris && uris.length > 0) {
                // Use provided URIs
                filesToProcess = uris.map(uri => vscode.Uri.file(uri));
            } else {
                // Find relevant files in workspace
                filesToProcess = await this.findRelevantFiles();
            }
            
            for (const uri of filesToProcess) {
                try {
                    const content = await vscode.workspace.fs.readFile(uri);
                    const text = new TextDecoder().decode(content);
                    const relativePath = vscode.workspace.asRelativePath(uri);
                    
                    const file: ContextFile = {
                        path: uri.fsPath,
                        content: text,
                        relativePath
                    };
                    
                    files.push(file);
                    totalBytes += text.length;
                    
                    if (totalBytes > maxBytes) {
                        this.output.appendLine(`⚠️ Context size limit reached (${maxBytes} bytes). Truncating...`);
                        break;
                    }
                    
                } catch (error) {
                    this.output.appendLine(`⚠️ Could not read file ${uri.fsPath}: ${error}`);
                }
            }
            
        } catch (error) {
            this.output.appendLine(`⚠️ Error collecting context: ${error}`);
        }
        
        // Format context
        const contextParts = files.map(file => 
            `// FILE: ${file.relativePath}\n${file.content}`
        );
        
        const context = contextParts.join('\n\n');
        this.output.appendLine(`📁 Collected ${files.length} files, ${context.length} total chars`);
        
        return context;
    }
    
    /**
     * Find relevant files in the workspace
     */
    private async findRelevantFiles(): Promise<vscode.Uri[]> {
        const patterns = [
            '**/*.{ts,tsx,js,jsx,py,pyi,json,md}',
            '**/package.json',
            '**/tsconfig.json',
            '**/pyproject.toml',
            '**/requirements.txt'
        ];
        
        const excludePatterns = '**/node_modules/**';
        const files: vscode.Uri[] = [];
        
        for (const pattern of patterns) {
            try {
                const found = await vscode.workspace.findFiles(pattern, excludePatterns, 50);
                files.push(...found);
            } catch (error) {
                this.output.appendLine(`⚠️ Error finding files with pattern ${pattern}: ${error}`);
            }
        }
        
        // Remove duplicates and sort by relevance
        const uniqueFiles = Array.from(new Set(files.map(f => f.fsPath)))
            .map(fsPath => vscode.Uri.file(fsPath))
            .sort((a, b) => {
                // Prioritize currently open files
                const aOpen = vscode.workspace.textDocuments.some(doc => doc.uri.fsPath === a.fsPath);
                const bOpen = vscode.workspace.textDocuments.some(doc => doc.uri.fsPath === b.fsPath);
                
                if (aOpen && !bOpen) {return -1;}
                if (!aOpen && bOpen) {return 1;}
                
                // Then prioritize by file type
                const aExt = path.extname(a.fsPath);
                const bExt = path.extname(b.fsPath);
                const priorities = ['.ts', '.tsx', '.js', '.jsx', '.py'];
                
                const aPriority = priorities.indexOf(aExt);
                const bPriority = priorities.indexOf(bExt);
                
                if (aPriority !== -1 && bPriority === -1) {return -1;}
                if (aPriority === -1 && bPriority !== -1) {return 1;}
                if (aPriority !== -1 && bPriority !== -1) {return aPriority - bPriority;}
                
                return a.fsPath.localeCompare(b.fsPath);
            });
        
        return uniqueFiles.slice(0, 30); // Limit to 30 files
    }
    
    /**
     * Create system prompt for the AI
     */
    private createSystemPrompt(goal: string): string {
        return [
            "Bạn là một AI lập trình viên (DeepSeek-R1) chạy cục bộ qua Ollama.",
            "Trả lời **CHỈ** trong khối ```json``` theo schema:",
            JSON.stringify({
                summary: "...",
                rationale: "...",
                actions: [
                    {
                        type: "upsert_file | append | replace | insert | optimize_imports",
                        path: "...",
                        content: "...",
                        pattern: "...",
                        flags: "...",
                        anchor: "...",
                        position: "above | below"
                    }
                ]
            }, null, 2),
            "",
            "Các hành động được hỗ trợ:",
            "- upsert_file: Tạo hoặc ghi đè file hoàn toàn",
            "- append: Thêm nội dung vào cuối file",
            "- replace: Thay thế theo regex pattern",
            "- insert: Chèn nội dung above/below anchor string",
            "- optimize_imports: Sắp xếp và tối ưu imports",
            "",
            "Nguyên tắc:",
            "- Thay đổi nhỏ, an toàn, không xóa logic nếu không chắc chắn",
            "- Ưu tiên import sạch, sửa lỗi rõ ràng",
            "- Luôn đảm bảo đường dẫn file hợp lệ trong workspace",
            "- Không sử dụng path traversal (../, ../)",
            "",
            `Mục tiêu: ${goal}`
        ].join('\n');
    }
    
    /**
     * Create user prompt with context
     */
    private createUserPrompt(goal: string, context: string): string {
        const workspaceInfo = this.getWorkspaceInfo();
        
        return [
            `Dự án: ${workspaceInfo.name}`,
            `Framework: ${workspaceInfo.framework}`,
            `Dependencies: ${JSON.stringify(workspaceInfo.dependencies).slice(0, 200)}...`,
            "",
            "Context code:",
            context.slice(0, this.config.getMaxContextBytes() - 1000), // Leave room for other parts
            "",
            `Yêu cầu: ${goal}`,
            "",
            "Hãy phân tích code và đưa ra plan JSON để thực hiện mục tiêu."
        ].join('\n');
    }
    
    /**
     * Get workspace information
     */
    private getWorkspaceInfo(): { name: string; framework: string; dependencies: Record<string, any> } {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        const name = workspaceFolder?.name || 'Unknown';
        
        // Try to detect framework and dependencies
        let framework = 'Unknown';
        let dependencies: Record<string, any> = {};
        
        try {
            const packageJsonPath = path.join(workspaceFolder?.uri.fsPath || '', 'package.json');
            const packageJsonContent = require(packageJsonPath);
            
            dependencies = {
                ...packageJsonContent.dependencies,
                ...packageJsonContent.devDependencies
            };
            
            // Detect framework
            if (dependencies['react']) {framework = 'React';}
            else if (dependencies['vue']) {framework = 'Vue';}
            else if (dependencies['angular']) {framework = 'Angular';}
            else if (dependencies['svelte']) {framework = 'Svelte';}
            else if (dependencies['next']) {framework = 'Next.js';}
            else if (dependencies['express']) {framework = 'Express';}
            else if (dependencies['fastify']) {framework = 'Fastify';}
            
        } catch (error) {
            // Fallback to Python detection
            try {
                const pyprojectPath = path.join(workspaceFolder?.uri.fsPath || '', 'pyproject.toml');
                if (require('fs').existsSync(pyprojectPath)) {
                    framework = 'Python';
                }
            } catch (e) {
                // Continue with defaults
            }
        }
        
        return { name, framework, dependencies };
    }
    
    /**
     * Parse JSON plan from AI response
     */
    private parsePlan(response: string): AgentPlan {
        try {
            // Extract JSON from markdown code block
            const jsonMatch = response.match(/```json\s*([\s\S]*?)\s*```/);
            if (!jsonMatch) {
                throw new Error('No JSON plan found in response');
            }
            
            const jsonStr = jsonMatch[1];
            const parsed = JSON.parse(jsonStr);
            
            // Validate schema
            if (!parsed.summary || !parsed.rationale || !Array.isArray(parsed.actions)) {
                throw new Error('Invalid plan schema');
            }
            
            // Validate actions
            for (const action of parsed.actions) {
                if (!action.type || !action.path) {
                    throw new Error('Invalid action schema');
                }
                
                // Sanitize path to prevent traversal
                action.path = this.sanitizePath(action.path);
            }
            
            return parsed as AgentPlan;
            
        } catch (error) {
            throw new Error(`Failed to parse plan: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    
    /**
     * Sanitize file path to prevent traversal attacks
     */
    private sanitizePath(inputPath: string): string {
        // Remove any path traversal attempts
        let sanitized = inputPath.replace(/\.\.[\\/]/g, '').replace(/^[\\/]/, '');
        
        // Ensure path is within workspace
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            if (!path.isAbsolute(sanitized)) {
                sanitized = path.join(workspaceFolder.uri.fsPath, sanitized);
            }
            
            // Ensure it's within workspace
            const relativePath = path.relative(workspaceFolder.uri.fsPath, sanitized);
            if (relativePath.startsWith('..')) {
                throw new Error(`Path ${inputPath} is outside workspace`);
            }
        }
        
        return sanitized;
    }
    
    /**
     * Apply actions from a plan
     */
    async applyActions(actions: AgentAction[]): Promise<number> {
        let appliedCount = 0;
        
        this.output.appendLine(`🔧 Applying ${actions.length} actions...`);
        
        for (const action of actions) {
            try {
                await this.applyAction(action);
                appliedCount++;
                this.output.appendLine(`✅ Applied: ${action.type} ${action.path}`);
            } catch (error) {
                this.output.appendLine(`❌ Failed to apply ${action.type} ${action.path}: ${error}`);
            }
        }
        
        this.output.appendLine(`📊 Applied ${appliedCount}/${actions.length} actions`);
        return appliedCount;
    }
    
    /**
     * Apply a single action
     */
    private async applyAction(action: AgentAction): Promise<void> {
        const uri = vscode.Uri.file(action.path);
        const edit = new vscode.WorkspaceEdit();
        
        switch (action.type) {
            case 'upsert_file':
                await this.actionUpsertFile(edit, uri, action.content || '');
                break;
                
            case 'append':
                await this.actionAppend(edit, uri, action.content || '');
                break;
                
            case 'replace':
                await this.actionReplace(edit, uri, action.pattern || '', action.content || '', action.flags);
                break;
                
            case 'insert':
                await this.actionInsert(edit, uri, action.anchor || '', action.content || '', action.position || 'below');
                break;
                
            case 'optimize_imports':
                await this.actionOptimizeImports(edit, uri);
                break;
                
            default:
                throw new Error(`Unknown action type: ${(action as any).type}`);
        }
        
        const success = await vscode.workspace.applyEdit(edit);
        if (!success) {
            throw new Error('Failed to apply workspace edit');
        }
    }
    
    /**
     * Upsert file action implementation
     */
    private async actionUpsertFile(edit: vscode.WorkspaceEdit, uri: vscode.Uri, content: string): Promise<void> {
        try {
            await vscode.workspace.fs.stat(uri);
            // File exists, replace content
            edit.createFile(uri, { overwrite: true });
        } catch {
            // File doesn't exist, create it
            edit.createFile(uri, { ignoreIfExists: false });
        }
        
        edit.insert(uri, new vscode.Position(0, 0), content);
    }
    
    /**
     * Append action implementation
     */
    private async actionAppend(edit: vscode.WorkspaceEdit, uri: vscode.Uri, content: string): Promise<void> {
        try {
            const fileContent = await vscode.workspace.fs.readFile(uri);
            const text = new TextDecoder().decode(fileContent);
            const lines = text.split('\n');
            const lastLine = lines.length - 1;
            const lastChar = lines[lastLine].length;
            
            const appendText = text.endsWith('\n') ? content : '\n' + content;
            edit.insert(uri, new vscode.Position(lastLine, lastChar), appendText);
            
        } catch (error) {
            throw new Error(`Cannot append to file: ${error}`);
        }
    }
    
    /**
     * Replace action implementation
     */
    private async actionReplace(edit: vscode.WorkspaceEdit, uri: vscode.Uri, pattern: string, replacement: string, flags?: string): Promise<void> {
        try {
            const fileContent = await vscode.workspace.fs.readFile(uri);
            const text = new TextDecoder().decode(fileContent);
            
            const regex = new RegExp(pattern, flags || 'g');
            const newText = text.replace(regex, replacement);
            
            if (newText === text) {
                throw new Error('Pattern not found');
            }
            
            const document = await vscode.workspace.openTextDocument(uri);
            const fullRange = new vscode.Range(
                document.positionAt(0),
                document.positionAt(text.length)
            );
            
            edit.replace(uri, fullRange, newText);
            
        } catch (error) {
            throw new Error(`Cannot replace in file: ${error}`);
        }
    }
    
    /**
     * Insert action implementation
     */
    private async actionInsert(edit: vscode.WorkspaceEdit, uri: vscode.Uri, anchor: string, content: string, position: 'above' | 'below'): Promise<void> {
        try {
            const fileContent = await vscode.workspace.fs.readFile(uri);
            const text = new TextDecoder().decode(fileContent);
            const lines = text.split('\n');
            
            let insertLineIndex = -1;
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].includes(anchor)) {
                    insertLineIndex = position === 'above' ? i : i + 1;
                    break;
                }
            }
            
            if (insertLineIndex === -1) {
                throw new Error(`Anchor "${anchor}" not found`);
            }
            
            const insertText = content + '\n';
            edit.insert(uri, new vscode.Position(insertLineIndex, 0), insertText);
            
        } catch (error) {
            throw new Error(`Cannot insert in file: ${error}`);
        }
    }
    
    /**
     * Optimize imports action implementation
     */
    private async actionOptimizeImports(edit: vscode.WorkspaceEdit, uri: vscode.Uri): Promise<void> {
        try {
            const fileContent = await vscode.workspace.fs.readFile(uri);
            const text = new TextDecoder().decode(fileContent);
            const ext = path.extname(uri.fsPath);
            
            let optimizedText = text;
            
            if (['.ts', '.tsx', '.js', '.jsx'].includes(ext)) {
                optimizedText = this.optimizeJSImports(text);
            } else if (ext === '.py') {
                optimizedText = this.optimizePythonImports(text);
            }
            
            if (optimizedText !== text) {
                const document = await vscode.workspace.openTextDocument(uri);
                const fullRange = new vscode.Range(
                    document.positionAt(0),
                    document.positionAt(text.length)
                );
                
                edit.replace(uri, fullRange, optimizedText);
            }
            
        } catch (error) {
            throw new Error(`Cannot optimize imports: ${error}`);
        }
    }
    
    /**
     * Optimize JavaScript/TypeScript imports
     */
    private optimizeJSImports(text: string): string {
        const lines = text.split('\n');
        const imports: string[] = [];
        const rest: string[] = [];
        let inImportSection = true;
        
        for (const line of lines) {
            if (inImportSection && (line.trim().startsWith('import ') || line.trim().startsWith('export '))) {
                imports.push(line);
            } else {
                if (line.trim() && inImportSection) {
                    inImportSection = false;
                }
                rest.push(line);
            }
        }
        
        // Sort imports
        imports.sort((a, b) => {
            // Built-in modules first
            const aBuiltin = !a.includes('./') && !a.includes('../');
            const bBuiltin = !b.includes('./') && !b.includes('../');
            
            if (aBuiltin && !bBuiltin) {return -1;}
            if (!aBuiltin && bBuiltin) {return 1;}
            
            return a.localeCompare(b);
        });
        
        return [...imports, '', ...rest].join('\n');
    }
    
    /**
     * Optimize Python imports
     */
    private optimizePythonImports(text: string): string {
        const lines = text.split('\n');
        const standardImports: string[] = [];
        const thirdPartyImports: string[] = [];
        const localImports: string[] = [];
        const rest: string[] = [];
        let inImportSection = true;
        
        for (const line of lines) {
            if (inImportSection && (line.trim().startsWith('import ') || line.trim().startsWith('from '))) {
                // Categorize imports
                if (line.includes(' import ') && line.includes('.')) {
                    localImports.push(line);
                } else if (this.isStandardLibrary(line)) {
                    standardImports.push(line);
                } else {
                    thirdPartyImports.push(line);
                }
            } else {
                if (line.trim() && inImportSection) {
                    inImportSection = false;
                }
                rest.push(line);
            }
        }
        
        // Sort each category
        [standardImports, thirdPartyImports, localImports].forEach(arr => arr.sort());
        
        const result = [];
        if (standardImports.length) {result.push(...standardImports, '');}
        if (thirdPartyImports.length) {result.push(...thirdPartyImports, '');}
        if (localImports.length) {result.push(...localImports, '');}
        result.push(...rest);
        
        return result.join('\n');
    }
    
    /**
     * Check if import is from standard library
     */
    private isStandardLibrary(importLine: string): boolean {
        const standardLibs = [
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'typing',
            'collections', 'itertools', 'functools', 're', 'math', 'random'
        ];
        
        return standardLibs.some(lib => importLine.includes(`import ${lib}`) || importLine.includes(`from ${lib}`));
    }
    
    /**
     * Show confirmation dialog and diff preview
     */
    async confirmAndApply(plan: AgentPlan): Promise<void> {
        const options = ['Apply', 'Show diff', 'Cancel'];
        const choice = await vscode.window.showQuickPick(options, {
            placeHolder: `Plan: ${plan.summary} – ${plan.actions.length} actions`
        });
        
        switch (choice) {
            case 'Apply':
                await this.applyActions(plan.actions);
                break;
                
            case 'Show diff':
                await this.showPlanDiff(plan);
                break;
                
            case 'Cancel':
                this.output.appendLine('❌ Plan cancelled by user');
                break;
                
            default:
                // User dismissed dialog
                break;
        }
    }
    
    /**
     * Show diff preview of the plan
     */
    private async showPlanDiff(plan: AgentPlan): Promise<void> {
        const tempDir = path.join(require('os').tmpdir(), 'deepseek-plan');
        
        try {
            require('fs').mkdirSync(tempDir, { recursive: true });
            
            const planPath = path.join(tempDir, 'plan.json');
            require('fs').writeFileSync(planPath, JSON.stringify(plan, null, 2));
            
            const planUri = vscode.Uri.file(planPath);
            const document = await vscode.workspace.openTextDocument(planUri);
            await vscode.window.showTextDocument(document);
            
        } catch (error) {
            vscode.window.showErrorMessage(`Failed to show diff: ${error}`);
        }
    }
}