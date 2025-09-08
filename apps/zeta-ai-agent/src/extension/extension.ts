import * as vscode from 'vscode';
import { AIAgent } from '../core/agent/agent';
import { ZetaCodeViewProvider } from './providers/codeViewProvider';
import { ZetaChatProvider } from './providers/chatProvider';
import { ZetaStatusBarProvider } from './providers/statusBarProvider';
import { ExtensionConfig } from '../types/shared';
import AI from "AI";
import Action from "Action";
import Activating from "Activating";
import Activity from "Activity";
import Agent from "Agent";
import Ask from "Ask";
import Cannot from "Cannot";
import Chat from "../../../desktop/src/pages/Chat";
import Code from "Code";
import Command from "Command";
import Configuration from "Configuration";
import Deactivating from "Deactivating";
import Debug from "Debug";
import Debugging from "Debugging";
import Describe from "Describe";
import ExtensionContext from "ExtensionContext";
import FAILED from "FAILED";
import Failed from "Failed";
import Focus from "Focus";
import Get from "Get";
import Getting from "Getting";
import Initialize from "Initialize";
import Memory from "../../../desktop/src/Memory/index";
import No from "No";
import Optimization from "Optimization";
import Optimize from "Optimize";
import Optimizing from "Optimizing";
import Plan from "Plan";
import Planning from "Planning";
import Recent from "Recent";
import Refactor from "Refactor";
import Register from "Register";
import Review from "Review";
import Reviewing from "Reviewing";
import SUCCESS from "SUCCESS";
import Select from "Select";
import Show from "Show";
import Statistics from "Statistics";
import Stats from "Stats";
import Success from "Success";
import Total from "Total";
import TypeError from "TypeError";
import Zeta from "Zeta";

let agent: AIAgent;
let codeViewProvider: ZetaCodeViewProvider;
let chatProvider: ZetaChatProvider;
let statusBarProvider: ZetaStatusBarProvider;

export async function activate(context: vscode.ExtensionContext) {
  console.log('Activating Zeta AI Agent extension...');

  try {
    // Initialize AI Agent
    const config = getExtensionConfig();
    agent = new AIAgent(config);
    await agent.initialize();

    // Initialize providers
    codeViewProvider = new ZetaCodeViewProvider(agent);
    chatProvider = new ZetaChatProvider(agent, context.extensionUri);
    statusBarProvider = new ZetaStatusBarProvider(agent);

    // Register webview providers
    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        'zetaCodeView',
        codeViewProvider
      )
    );

    context.subscriptions.push(
      vscode.window.registerWebviewViewProvider(
        'zetaChatView',
        chatProvider
      )
    );

    // Register commands
    registerCommands(context);

    // Initialize status bar
    statusBarProvider.initialize();

    // Register configuration change listener
    context.subscriptions.push(
      vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('zetaAI')) {
          const newConfig = getExtensionConfig();
          agent.updateConfig(newConfig);
          vscode.window.showInformationMessage('Zeta AI configuration updated');
        }
      })
    );

    vscode.window.showInformationMessage('Zeta AI Agent activated successfully!');
    console.log('Zeta AI Agent extension activated');

  } catch (error) {
    console.error('Failed to activate Zeta AI Agent:', error);
    vscode.window.showErrorMessage(`Failed to activate Zeta AI Agent: ${error}`);
  }
}

export function deactivate() {
  console.log('Deactivating Zeta AI Agent extension...');
  statusBarProvider?.dispose();
}

function registerCommands(context: vscode.ExtensionContext) {
  // Code Review Command
  const reviewCodeCommand = vscode.commands.registerCommand('zetaAI.reviewCode', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    const selection = editor.selection;
    const code = selection.isEmpty ? document.getText() : document.getText(selection);

    if (!code.trim()) {
      vscode.window.showErrorMessage('No code selected or file is empty');
      return;
    }

    try {
      vscode.window.showInformationMessage('Reviewing code...');
      
      const context = {
        language: document.languageId,
        filePath: document.uri.fsPath,
        fileExtension: document.uri.fsPath.split('.').pop() || '',
        project: vscode.workspace.getWorkspaceFolder(document.uri)?.name || 'unknown'
      };

      const review = await agent.reviewCode(code, context);
      
      // Show results in code view
      await codeViewProvider.showCodeReview(review);
      
      // Focus on the code view
      vscode.commands.executeCommand('zetaCodeView.focus');

    } catch (error) {
      vscode.window.showErrorMessage(`Code review failed: ${error}`);
    }
  });

  // Debug Code Command
  const debugCodeCommand = vscode.commands.registerCommand('zetaAI.debugCode', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    // Get error description from user
    const errorDescription = await vscode.window.showInputBox({
      prompt: 'Describe the error or issue you\'re experiencing',
      placeHolder: 'e.g., "Getting TypeError: Cannot read property of undefined"'
    });

    if (!errorDescription) {
      return;
    }

    const document = editor.document;
    const selection = editor.selection;
    const code = selection.isEmpty ? document.getText() : document.getText(selection);

    try {
      vscode.window.showInformationMessage('Debugging code...');
      
      const context = {
        language: document.languageId,
        filePath: document.uri.fsPath,
        fileExtension: document.uri.fsPath.split('.').pop() || '',
        project: vscode.workspace.getWorkspaceFolder(document.uri)?.name || 'unknown'
      };

      const solution = await agent.debugCode(errorDescription, code, context);
      
      // Show results in code view
      await codeViewProvider.showDebugSolution(solution);
      
      // Focus on the code view
      vscode.commands.executeCommand('zetaCodeView.focus');

    } catch (error) {
      vscode.window.showErrorMessage(`Debug failed: ${error}`);
    }
  });

  // Optimize Code Command
  const optimizeCodeCommand = vscode.commands.registerCommand('zetaAI.optimizeCode', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    const selection = editor.selection;
    const code = selection.isEmpty ? document.getText() : document.getText(selection);

    if (!code.trim()) {
      vscode.window.showErrorMessage('No code selected or file is empty');
      return;
    }

    // Ask for optimization metrics
    const metrics = await vscode.window.showQuickPick([
      'performance',
      'readability',
      'memory',
      'security',
      'maintainability'
    ], {
      canPickMany: true,
      placeHolder: 'Select optimization metrics (optional)'
    });

    try {
      vscode.window.showInformationMessage('Optimizing code...');
      
      const context = {
        language: document.languageId,
        filePath: document.uri.fsPath,
        fileExtension: document.uri.fsPath.split('.').pop() || '',
        project: vscode.workspace.getWorkspaceFolder(document.uri)?.name || 'unknown'
      };

      const optimization = await agent.optimizeCode(code, context, metrics);
      
      // Show results in code view
      await codeViewProvider.showOptimization(optimization);
      
      // Focus on the code view
      vscode.commands.executeCommand('zetaCodeView.focus');

    } catch (error) {
      vscode.window.showErrorMessage(`Optimization failed: ${error}`);
    }
  });

  // Chat Command
  const chatCommand = vscode.commands.registerCommand('zetaAI.openChat', async () => {
    // Focus on the chat view
    vscode.commands.executeCommand('zetaChatView.focus');
  });

  // Plan Action Command
  const planActionCommand = vscode.commands.registerCommand('zetaAI.planAction', async () => {
    const request = await vscode.window.showInputBox({
      prompt: 'Describe the task you want to plan',
      placeHolder: 'e.g., "Refactor this component to use hooks"'
    });

    if (!request) {
      return;
    }

    const editor = vscode.window.activeTextEditor;
    const context = editor ? {
      language: editor.document.languageId,
      filePath: editor.document.uri.fsPath,
      project: vscode.workspace.getWorkspaceFolder(editor.document.uri)?.name || 'unknown'
    } : {};

    try {
      vscode.window.showInformationMessage('Planning action...');
      
      const plan = await agent.planAction(request, context);
      
      // Show results in code view
      await codeViewProvider.showActionPlan(plan);
      
      // Focus on the code view
      vscode.commands.executeCommand('zetaCodeView.focus');

    } catch (error) {
      vscode.window.showErrorMessage(`Action planning failed: ${error}`);
    }
  });

  // Memory Stats Command
  const memoryStatsCommand = vscode.commands.registerCommand('zetaAI.showMemoryStats', async () => {
    try {
      const stats = await agent.getMemoryStats();
      
      // Show in output channel
      const outputChannel = vscode.window.createOutputChannel('Zeta AI Memory Stats');
      outputChannel.clear();
      outputChannel.appendLine('=== Zeta AI Memory Statistics ===');
      outputChannel.appendLine(`Total interactions: ${stats.total_interactions}`);
      outputChannel.appendLine(`Success rate: ${(stats.success_rate * 100).toFixed(1)}%`);
      outputChannel.appendLine('\n=== Recent Activity ===');
      
      stats.recent_activity.forEach((activity: any, index: number) => {
        outputChannel.appendLine(`${index + 1}. [${activity.timestamp}] ${activity.type}: ${activity.success ? 'SUCCESS' : 'FAILED'}`);
      });
      
      outputChannel.show();

    } catch (error) {
      vscode.window.showErrorMessage(`Failed to get memory stats: ${error}`);
    }
  });

  // Configuration Command
  const configureCommand = vscode.commands.registerCommand('zetaAI.configure', async () => {
    vscode.commands.executeCommand('workbench.action.openSettings', 'zetaAI');
  });

  // Register all commands
  context.subscriptions.push(
    reviewCodeCommand,
    debugCodeCommand,
    optimizeCodeCommand,
    chatCommand,
    planActionCommand,
    memoryStatsCommand,
    configureCommand
  );
}

function getExtensionConfig(): ExtensionConfig {
  const config = vscode.workspace.getConfiguration('zetaAI');
  
  return {
    ollama_url: config.get('ollamaUrl', 'http://localhost:11434'),
    default_model: config.get('defaultModel', 'deepseek-coder'),
    max_context_size: config.get('maxContextSize', 1000),
    enable_caching: config.get('enableCaching', true),
    cache_ttl: config.get('cacheTtl', 3600),
    rate_limit: config.get('rateLimit', 60),
    security_policy: {
      max_code_size: config.get('security.maxCodeSize', 100000),
      allowed_file_extensions: config.get('security.allowedFileExtensions', [
        '.ts', '.js', '.py', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs'
      ]),
      blocked_patterns: [/eval\(/i, /exec\(/i, /system\(/i],
      max_context_size: config.get('security.maxContextSize', 10000),
      rate_limit_per_minute: config.get('security.rateLimitPerMinute', 60)
    },
    performance_monitoring: config.get('performanceMonitoring', true),
    log_level: config.get('logLevel', 'info')
  };
}
