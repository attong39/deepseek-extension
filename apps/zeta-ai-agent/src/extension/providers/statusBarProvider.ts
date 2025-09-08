import * as vscode from 'vscode';
import { AIAgent } from '../../core/agent/agent';
import AI from "AI";
import Chat from "../../../../desktop/src/pages/Chat";
import Check from "Check";
import Click from "Click";
import Ollama from "Ollama";
import Open from "Open";
import Right from "Right";
import StatusBarAlignment from "StatusBarAlignment";
import StatusBarItem from "StatusBarItem";
import ThemeColor from "ThemeColor";
import Update from "Update";
import Zeta from "Zeta";
import ZetaStatusBarProvider from "ZetaStatusBarProvider";

export class ZetaStatusBarProvider {
  private statusBarItem: vscode.StatusBarItem;
  private isInitialized = false;

  constructor(private agent: AIAgent) {
    this.statusBarItem = vscode.window.createStatusBarItem(
      vscode.StatusBarAlignment.Right,
      100
    );
  }

  public initialize() {
    this.statusBarItem.command = 'zetaAI.openChat';
    this.statusBarItem.tooltip = 'Open Zeta AI Chat';
    this.updateStatus();
    this.statusBarItem.show();
    this.isInitialized = true;

    // Update status periodically
    setInterval(() => {
      if (this.isInitialized) {
        this.updateStatus();
      }
    }, 5000);
  }

  private async updateStatus() {
    try {
      // Check Ollama connection
      const isHealthy = await this.agent['ollama'].healthCheck();
      
      if (isHealthy) {
        this.statusBarItem.text = '$(robot) Zeta AI';
        this.statusBarItem.backgroundColor = undefined;
        this.statusBarItem.tooltip = 'Zeta AI is ready - Click to open chat';
      } else {
        this.statusBarItem.text = '$(warning) Zeta AI';
        this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        this.statusBarItem.tooltip = 'Zeta AI connection issue - Check Ollama server';
      }
    } catch (error) {
      this.statusBarItem.text = '$(error) Zeta AI';
      this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.errorBackground');
      this.statusBarItem.tooltip = `Zeta AI error: ${error}`;
    }
  }

  public showProgress(message: string) {
    this.statusBarItem.text = `$(loading~spin) ${message}`;
    this.statusBarItem.tooltip = message;
  }

  public hideProgress() {
    this.updateStatus();
  }

  public dispose() {
    this.isInitialized = false;
    this.statusBarItem.dispose();
  }
}
