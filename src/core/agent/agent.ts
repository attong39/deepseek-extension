import * as vscode from 'vscode';
import { OllamaClient } from '../ollama/client';
import { ModelManager } from '../ollama/models';
import { CodeAnalyzer } from './cognitive/codeAnalyzer';
import { MemoryManager } from './memory/memoryManager';
import { ActionPlanner } from './planner/actionPlanner';
import { CodeContext } from '../../types/shared';
import AI from "AI";
import AIAgent from "AIAgent";
import Analyzing from "Analyzing";
import Arial from "Arial";
import Ask from "Ask";
import CODE from "CODE";
import Chat from "../../../apps/desktop/src/pages/Chat";
import ChatView from "ChatView";
import Code from "Code";
import Confidence from "Confidence";
import DEBUG from "DEBUG";
import DOCTYPE from "DOCTYPE";
import Debug from "Debug";
import Debugging from "Debugging";
import Display from "Display";
import Enter from "Enter";
import Expected from "Expected";
import ExtensionContext from "ExtensionContext";
import Found from "Found";
import Get from "Get";
import Here from "Here";
import ISSUES from "ISSUES";
import Initialize from "Initialize";
import Issues from "Issues";
import Math from "Math";
import No from "No";
import Ollama from "Ollama";
import One from "One";
import Optimization from "Optimization";
import Optimizing from "Optimizing";
import Overall from "Overall";
import Please from "Please";
import Processing from "Processing";
import RESULTS from "RESULTS";
import REVIEW from "REVIEW";
import Range from "Range";
import Review from "Review";
import SOLUTION from "SOLUTION";
import STEPS from "STEPS";
import SUGGESTIONS from "SUGGESTIONS";
import Score from "Score";
import Send from "Send";
import Show from "Show";
import Simple from "Simple";
import Suggestions from "Suggestions";
import UTF from "UTF";
import Uri from "Uri";
import ViewColumn from "ViewColumn";
import WebviewPanel from "WebviewPanel";
import WorkspaceEdit from "WorkspaceEdit";
import Zeta from "Zeta";

export class AIAgent {
  private ollama: OllamaClient;
  private modelManager: ModelManager;
  private codeAnalyzer: CodeAnalyzer;
  private memoryManager: MemoryManager;
  private actionPlanner: ActionPlanner;
  private context: vscode.ExtensionContext;

  constructor(context: vscode.ExtensionContext) {
    this.context = context;

    // Initialize Ollama client
    const config = vscode.workspace.getConfiguration('zeta.agent');
    const baseUrl = config.get<string>('ollamaUrl', 'http://localhost:11434');
    this.ollama = new OllamaClient(baseUrl);

    // Initialize components
    this.modelManager = new ModelManager(this.ollama);
    this.codeAnalyzer = new CodeAnalyzer(this.ollama);
    this.memoryManager = new MemoryManager();
    this.actionPlanner = new ActionPlanner(this.ollama);
  }

  async reviewCode(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    const code = document.getText();
    const context: CodeContext = {
      language: document.languageId,
      filePath: document.fileName,
      projectType: this.detectProjectType(document.fileName)
    };

    try {
      vscode.window.showInformationMessage('Analyzing code...');
      const review = await this.codeAnalyzer.reviewCode(code, context);

      // Display results
      const output = vscode.window.createOutputChannel('Zeta AI Review');
      output.clear();
      output.appendLine('=== CODE REVIEW RESULTS ===');
      output.appendLine(`Overall Score: ${review.overall_score}/10`);
      output.appendLine(`Issues Found: ${review.issues.length}`);
      output.appendLine(`Suggestions: ${review.suggestions.length}`);
      output.appendLine('');
      output.appendLine('ISSUES:');
      review.issues.forEach((issue, i) => {
        output.appendLine(`${i + 1}. [${issue.severity.toUpperCase()}] ${issue.message}`);
      });
      output.appendLine('');
      output.appendLine('SUGGESTIONS:');
      review.suggestions.forEach((suggestion, i) => {
        output.appendLine(`${i + 1}. ${suggestion.description}`);
      });
      output.show();

      vscode.window.showInformationMessage(`Code review complete! Score: ${review.overall_score}/10`);
    } catch (error) {
      vscode.window.showErrorMessage(`Review failed: ${error}`);
    }
  }

  async debugCode(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const selection = editor.selection;
    const selectedText = editor.document.getText(selection);
    const fullCode = editor.document.getText();

    if (!selectedText) {
      vscode.window.showErrorMessage('Please select the code/error to debug');
      return;
    }

    try {
      vscode.window.showInformationMessage('Debugging code...');
      const solution = await this.codeAnalyzer.debugCode(selectedText, fullCode);

      const output = vscode.window.createOutputChannel('Zeta AI Debug');
      output.clear();
      output.appendLine('=== DEBUG SOLUTION ===');
      output.appendLine(`Confidence: ${(solution.confidence * 100).toFixed(1)}%`);
      output.appendLine('');
      output.appendLine('STEPS:');
      solution.steps.forEach((step, i) => {
        output.appendLine(`${i + 1}. ${step.description}`);
        if (step.code_change) {
          output.appendLine(`   Code: ${step.code_change}`);
        }
        output.appendLine(`   Expected: ${step.expected_result}`);
        output.appendLine('');
      });
      output.show();

      vscode.window.showInformationMessage('Debug solution generated!');
    } catch (error) {
      vscode.window.showErrorMessage(`Debug failed: ${error}`);
    }
  }

  async optimizeCode(): Promise<void> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    const code = document.getText();

    try {
      vscode.window.showInformationMessage('Optimizing code...');

      // Get basic metrics
      const metrics = {
        lines: code.split('\n').length,
        characters: code.length,
        functions: (code.match(/function\s+\w+/g) || []).length,
        complexity: this.calculateComplexity(code)
      };

      const optimization = await this.codeAnalyzer.optimizeCode(code, metrics);

      // Show diff
      const optimizedUri = vscode.Uri.parse(`zeta-optimized:${document.fileName}`);
      const optimizedDoc = await vscode.workspace.openTextDocument(optimizedUri);
      const edit = new vscode.WorkspaceEdit();
      edit.replace(optimizedUri, new vscode.Range(0, 0, optimizedDoc.lineCount, 0), optimization.optimized_code);
      await vscode.workspace.applyEdit(edit);

      vscode.window.showTextDocument(optimizedUri, { preview: true });

      vscode.window.showInformationMessage('Code optimization complete!');
    } catch (error) {
      vscode.window.showErrorMessage(`Optimization failed: ${error}`);
    }
  }

  async openChat(): Promise<void> {
    const chatView = new ChatView(this.context, this);
    chatView.show();
  }

  private detectProjectType(filePath: string): string {
    const path = filePath.toLowerCase();

    if (path.includes('package.json')) return 'node';
    if (path.includes('requirements.txt') || path.includes('pyproject.toml')) return 'python';
    if (path.includes('.csproj') || path.includes('.sln')) return 'csharp';
    if (path.includes('cargo.toml')) return 'rust';
    if (path.includes('go.mod')) return 'go';

    return 'unknown';
  }

  private calculateComplexity(code: string): number {
    // Simple complexity calculation
    const lines = code.split('\n').length;
    const functions = (code.match(/function\s+\w+|def\s+\w+|class\s+\w+/g) || []).length;
    const loops = (code.match(/for\s*\(|while\s*\(|if\s*\(/g) || []).length;

    return Math.round((functions * 2) + (loops * 1.5) + (lines / 10));
  }
}

class ChatView {
  private panel: vscode.WebviewPanel | undefined;
  private context: vscode.ExtensionContext;
  private agent: AIAgent;

  constructor(context: vscode.ExtensionContext, agent: AIAgent) {
    this.context = context;
    this.agent = agent;
  }

  show(): void {
    if (this.panel) {
      this.panel.reveal(vscode.ViewColumn.One);
      return;
    }

    this.panel = vscode.window.createWebviewPanel(
      'zetaChat',
      'Zeta AI Chat',
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        localResourceRoots: []
      }
    );

    this.panel.webview.html = this.getWebviewContent();
    this.panel.onDidDispose(() => this.panel = undefined);
  }

  private getWebviewContent(): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Zeta AI Chat</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          #chat { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
          #input { width: 100%; padding: 8px; }
          button { padding: 8px 16px; margin-top: 10px; }
          .message { margin: 5px 0; padding: 8px; border-radius: 4px; }
          .user { background: #e3f2fd; }
          .assistant { background: #f5f5f5; }
        </style>
      </head>
      <body>
        <h2>Zeta AI Chat</h2>
        <div id="chat"></div>
        <input type="text" id="input" placeholder="Ask me anything...">
        <button onclick="sendMessage()">Send</button>

        <script>
          const vscode = acquireVsCodeApi();
          const chat = document.getElementById('chat');
          const input = document.getElementById('input');

          function addMessage(text, sender) {
            const div = document.createElement('div');
            div.className = 'message ' + sender;
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
          }

          function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'user');
            input.value = '';

            // Here you would send to the agent
            addMessage('Processing your request...', 'assistant');
          }

          input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
              sendMessage();
            }
          });
        </script>
      </body>
      </html>
    `;
  }
}
