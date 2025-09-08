import * as vscode from 'vscode';
import { AIAgent } from '../core/agent/agent';
import AI from "AI";
import Add from "Add";
import Agent from "Agent";
import CancellationToken from "CancellationToken";
import CompletionContext from "CompletionContext";
import CompletionItem from "CompletionItem";
import CompletionItemKind from "CompletionItemKind";
import CompletionItemProvider from "CompletionItemProvider";
import Ctrl from "Ctrl";
import ExtensionContext from "ExtensionContext";
import For from "For";
import In from "In";
import Method from "Method";
import P from "P";
import Position from "Position";
import Register from "Register";
import Shift from "Shift";
import TextDocument from "TextDocument";
import Use from "Use";
import Zeta from "Zeta";
import ZetaCompletionProvider from "ZetaCompletionProvider";

export function activate(context: vscode.ExtensionContext) {
  console.log('Zeta AI Agent is now active!');

  const agent = new AIAgent(context);

  // Register commands
  context.subscriptions.push(
    vscode.commands.registerCommand('zeta.agent.review', () => agent.reviewCode()),
    vscode.commands.registerCommand('zeta.agent.debug', () => agent.debugCode()),
    vscode.commands.registerCommand('zeta.agent.optimize', () => agent.optimizeCode()),
    vscode.commands.registerCommand('zeta.agent.chat', () => agent.openChat())
  );

  // Register completion provider
  const completionProvider = new ZetaCompletionProvider(agent);
  context.subscriptions.push(
    vscode.languages.registerCompletionItemProvider(
      ['typescript', 'javascript', 'python', 'java', 'csharp', 'cpp', 'go', 'rust'],
      completionProvider,
      '.', '(', '[', '"', "'"
    )
  );

  vscode.window.showInformationMessage('Zeta AI Agent activated! Use Ctrl+Shift+P and search for "Zeta" to get started.');
}

export function deactivate() {
  console.log('Zeta AI Agent deactivated');
}

class ZetaCompletionProvider implements vscode.CompletionItemProvider {
  constructor(private agent: AIAgent) {}

  async provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position,
    token: vscode.CancellationToken,
    context: vscode.CompletionContext
  ): Promise<vscode.CompletionItem[]> {
    // For now, return basic completions
    // In the future, this will use AI to provide intelligent completions
    const completions: vscode.CompletionItem[] = [];

    // Add some example completions
    const linePrefix = document.lineAt(position).text.substr(0, position.character);

    if (linePrefix.endsWith('console.')) {
      completions.push(new vscode.CompletionItem('log', vscode.CompletionItemKind.Method));
      completions.push(new vscode.CompletionItem('error', vscode.CompletionItemKind.Method));
      completions.push(new vscode.CompletionItem('warn', vscode.CompletionItemKind.Method));
    }

    return completions;
  }
}
