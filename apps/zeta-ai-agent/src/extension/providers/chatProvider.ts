import * as vscode from 'vscode';
import { AIAgent } from '../../core/agent/agent';
import AI from "AI";
import Ask from "Ask";
import Auto from "Auto";
import BlinkMacSystemFont from "BlinkMacSystemFont";
import CancellationToken from "CancellationToken";
import Chat from "../../../../desktop/src/pages/Chat";
import Clear from "Clear";
import Consolas from "Consolas";
import Courier from "Courier";
import Create from "Create";
import DOCTYPE from "DOCTYPE";
import Enter from "Enter";
import Export from "Export";
import Exported from "Exported";
import Exporting from "Exporting";
import Failed from "Failed";
import Format from "Format";
import Generate from "Generate";
import Get from "Get";
import Hi from "Hi";
import Hide from "Hide";
import I from "I";
import Markdown from "Markdown";
import Math from "Math";
import Monaco from "Monaco";
import New from "New";
import Request from "Request";
import Roboto from "Roboto";
import S from "S";
import Save from "Save";
import Scroll from "Scroll";
import Segoe from "Segoe";
import Send from "Send";
import Shift from "Shift";
import Show from "Show";
import Simple from "Simple";
import Sorry from "Sorry";
import Store from "Store";
import Text from "Text";
import UI from "../../../../desktop/src/UI/index";
import UTF from "UTF";
import Uri from "Uri";
import Webview from "Webview";
import WebviewView from "WebviewView";
import WebviewViewProvider from "WebviewViewProvider";
import WebviewViewResolveContext from "WebviewViewResolveContext";
import You from "You";
import Zeta from "Zeta";
import ZetaChatProvider from "ZetaChatProvider";

export class ZetaChatProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'zetaChatView';

  private _view?: vscode.WebviewView;

  constructor(
    private agent: AIAgent,
    private readonly _extensionUri: vscode.Uri
  ) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: [this._extensionUri]
    };

    webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage(
      async message => {
        switch (message.command) {
        case 'sendMessage':
          await this.handleChatMessage(message.text);
          break;
        case 'clearChat':
          this.clearChat();
          break;
        case 'exportChat':
          await this.exportChat();
          break;
        }
      }
    );
  }

  private async handleChatMessage(message: string) {
    if (!this._view) return;

    // Show user message
    this._view.webview.postMessage({
      command: 'addMessage',
      message: {
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
      }
    });

    // Show typing indicator
    this._view.webview.postMessage({
      command: 'showTyping'
    });

    try {
      // Get current editor context
      const editor = vscode.window.activeTextEditor;
      const context = editor ? {
        language: editor.document.languageId,
        filePath: editor.document.uri.fsPath,
        project: vscode.workspace.getWorkspaceFolder(editor.document.uri)?.name || 'unknown',
        selection: editor.selection.isEmpty ? null : editor.document.getText(editor.selection)
      } : {};

      // Get AI response
      const response = await this.agent.chat(message, context);

      // Hide typing indicator
      this._view.webview.postMessage({
        command: 'hideTyping'
      });

      // Show AI response
      this._view.webview.postMessage({
        command: 'addMessage',
        message: {
          role: 'assistant',
          content: response,
          timestamp: new Date().toISOString()
        }
      });

    } catch (error) {
      // Hide typing indicator
      this._view.webview.postMessage({
        command: 'hideTyping'
      });

      // Show error message
      this._view.webview.postMessage({
        command: 'addMessage',
        message: {
          role: 'assistant',
          content: `Sorry, I encountered an error: ${error}`,
          timestamp: new Date().toISOString(),
          isError: true
        }
      });
    }
  }

  private clearChat() {
    if (this._view) {
      this._view.webview.postMessage({
        command: 'clearMessages'
      });
    }
  }

  private async exportChat() {
    try {
      const uri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file('zeta-chat-export.md'),
        filters: {
          'Markdown': ['md'],
          'Text': ['txt']
        }
      });

      if (uri) {
        // Request chat history from webview
        this._view?.webview.postMessage({
          command: 'exportChat',
          filePath: uri.fsPath
        });
      }
    } catch (error) {
      vscode.window.showErrorMessage(`Failed to export chat: ${error}`);
    }
  }

  private getHtmlForWebview(_webview: vscode.Webview): string {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zeta AI Chat</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--vscode-editor-background);
                color: var(--vscode-editor-foreground);
                font-size: 13px;
                line-height: 1.4;
                height: 100vh;
                display: flex;
                flex-direction: column;
            }
            
            .header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 16px;
                border-bottom: 1px solid var(--vscode-panel-border);
                background-color: var(--vscode-sideBar-background);
            }
            
            .title {
                font-size: 16px;
                font-weight: 600;
                margin: 0;
                color: var(--vscode-titleBar-activeForeground);
            }
            
            .header-buttons {
                display: flex;
                gap: 8px;
            }
            
            .chat-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .message {
                max-width: 85%;
                padding: 12px 16px;
                border-radius: 12px;
                position: relative;
                word-wrap: break-word;
            }
            
            .message.user {
                align-self: flex-end;
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
            }
            
            .message.assistant {
                align-self: flex-start;
                background-color: var(--vscode-input-background);
                border: 1px solid var(--vscode-input-border);
            }
            
            .message.error {
                background-color: var(--vscode-inputValidation-errorBackground);
                border: 1px solid var(--vscode-inputValidation-errorBorder);
            }
            
            .message-content {
                margin: 0;
                white-space: pre-wrap;
            }
            
            .message-timestamp {
                font-size: 11px;
                opacity: 0.7;
                margin-top: 4px;
                text-align: right;
            }
            
            .message.assistant .message-timestamp {
                text-align: left;
            }
            
            .typing-indicator {
                align-self: flex-start;
                padding: 12px 16px;
                background-color: var(--vscode-input-background);
                border: 1px solid var(--vscode-input-border);
                border-radius: 12px;
                display: none;
            }
            
            .typing-dots {
                display: flex;
                gap: 4px;
            }
            
            .typing-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background-color: var(--vscode-editor-foreground);
                opacity: 0.4;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dot:nth-child(1) { animation-delay: -0.32s; }
            .typing-dot:nth-child(2) { animation-delay: -0.16s; }
            
            @keyframes typing {
                0%, 80%, 100% {
                    opacity: 0.4;
                    transform: scale(0.8);
                }
                40% {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            .input-container {
                border-top: 1px solid var(--vscode-panel-border);
                padding: 16px;
                background-color: var(--vscode-sideBar-background);
            }
            
            .input-wrapper {
                display: flex;
                gap: 8px;
                align-items: flex-end;
            }
            
            .message-input {
                flex: 1;
                min-height: 36px;
                max-height: 120px;
                padding: 8px 12px;
                border: 1px solid var(--vscode-input-border);
                border-radius: 6px;
                background-color: var(--vscode-input-background);
                color: var(--vscode-input-foreground);
                font-family: inherit;
                font-size: 13px;
                resize: none;
                outline: none;
            }
            
            .message-input:focus {
                border-color: var(--vscode-focusBorder);
            }
            
            .send-button {
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                cursor: pointer;
                font-size: 13px;
                min-width: 60px;
                height: 36px;
            }
            
            .send-button:hover:not(:disabled) {
                background-color: var(--vscode-button-hoverBackground);
            }
            
            .send-button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            .button {
                background-color: var(--vscode-button-secondaryBackground);
                color: var(--vscode-button-secondaryForeground);
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                cursor: pointer;
                font-size: 11px;
            }
            
            .button:hover {
                background-color: var(--vscode-button-secondaryHoverBackground);
            }
            
            .empty-state {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 40px 20px;
                color: var(--vscode-descriptionForeground);
            }
            
            .empty-state .icon {
                font-size: 48px;
                margin-bottom: 16px;
                opacity: 0.6;
            }
            
            .code-block {
                background-color: var(--vscode-textCodeBlock-background);
                border: 1px solid var(--vscode-panel-border);
                border-radius: 4px;
                padding: 8px;
                margin: 8px 0;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                overflow-x: auto;
                white-space: pre;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="title">💬 Zeta AI Chat</h1>
            <div class="header-buttons">
                <button class="button" onclick="exportChat()">Export</button>
                <button class="button" onclick="clearChat()">Clear</button>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="empty-state" id="emptyState">
                    <div class="icon">🤖</div>
                    <p>Hi! I'm Zeta AI, your coding assistant.</p>
                    <p>Ask me anything about your code, and I'll help you debug, optimize, or understand it better.</p>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
        
        <div class="input-container">
            <div class="input-wrapper">
                <textarea 
                    class="message-input" 
                    id="messageInput" 
                    placeholder="Ask me anything about your code..."
                    rows="1"
                ></textarea>
                <button class="send-button" id="sendButton" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            const vscode = acquireVsCodeApi();
            let chatHistory = [];
            
            // Auto-resize textarea
            const messageInput = document.getElementById('messageInput');
            messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
            
            // Send message on Enter (but not Shift+Enter)
            messageInput.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
            
            window.addEventListener('message', event => {
                const message = event.data;
                
                switch (message.command) {
                    case 'addMessage':
                        addMessage(message.message);
                        break;
                    case 'showTyping':
                        showTypingIndicator();
                        break;
                    case 'hideTyping':
                        hideTypingIndicator();
                        break;
                    case 'clearMessages':
                        clearMessages();
                        break;
                    case 'exportChat':
                        handleExportChat(message.filePath);
                        break;
                }
            });
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const text = input.value.trim();
                
                if (!text) return;
                
                // Clear input
                input.value = '';
                input.style.height = 'auto';
                
                // Send to extension
                vscode.postMessage({
                    command: 'sendMessage',
                    text: text
                });
            }
            
            function addMessage(message) {
                const messagesContainer = document.getElementById('messages');
                const emptyState = document.getElementById('emptyState');
                
                // Hide empty state
                if (emptyState) {
                    emptyState.style.display = 'none';
                }
                
                // Create message element
                const messageDiv = document.createElement('div');
                messageDiv.className = \`message \${message.role}\${message.isError ? ' error' : ''}\`;
                
                const contentDiv = document.createElement('div');
                contentDiv.className = 'message-content';
                
                // Format content (simple markdown-like formatting)
                const formattedContent = formatContent(message.content);
                contentDiv.innerHTML = formattedContent;
                
                const timestampDiv = document.createElement('div');
                timestampDiv.className = 'message-timestamp';
                timestampDiv.textContent = new Date(message.timestamp).toLocaleTimeString();
                
                messageDiv.appendChild(contentDiv);
                messageDiv.appendChild(timestampDiv);
                
                messagesContainer.appendChild(messageDiv);
                
                // Store in history
                chatHistory.push(message);
                
                // Scroll to bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function formatContent(content) {
                // Simple formatting for code blocks and basic markdown
                return content
                    .replace(/\`\`\`([^\\n]*?)\\n([\\s\\S]*?)\`\`\`/g, '<div class="code-block">$2</div>')
                    .replace(/\`([^\`]+)\`/g, '<code style="background-color: var(--vscode-textCodeBlock-background); padding: 2px 4px; border-radius: 3px;">$1</code>')
                    .replace(/\\*\\*([^\\*]+)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/\\*([^\\*]+)\\*/g, '<em>$1</em>')
                    .replace(/\\n/g, '<br>');
            }
            
            function showTypingIndicator() {
                const indicator = document.getElementById('typingIndicator');
                indicator.style.display = 'block';
                
                const messagesContainer = document.getElementById('messages');
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
            
            function hideTypingIndicator() {
                const indicator = document.getElementById('typingIndicator');
                indicator.style.display = 'none';
            }
            
            function clearChat() {
                vscode.postMessage({
                    command: 'clearChat'
                });
            }
            
            function clearMessages() {
                const messagesContainer = document.getElementById('messages');
                messagesContainer.innerHTML = '';
                
                const emptyState = document.createElement('div');
                emptyState.className = 'empty-state';
                emptyState.id = 'emptyState';
                emptyState.innerHTML = \`
                    <div class="icon">🤖</div>
                    <p>Hi! I'm Zeta AI, your coding assistant.</p>
                    <p>Ask me anything about your code, and I'll help you debug, optimize, or understand it better.</p>
                \`;
                
                messagesContainer.appendChild(emptyState);
                
                chatHistory = [];
            }
            
            function exportChat() {
                vscode.postMessage({
                    command: 'exportChat'
                });
            }
            
            function handleExportChat(filePath) {
                // Generate markdown content
                let content = '# Zeta AI Chat Export\\n\\n';
                content += \`Exported on: \${new Date().toLocaleString()}\\n\\n\`;
                
                chatHistory.forEach((message, index) => {
                    const role = message.role === 'user' ? 'You' : 'Zeta AI';
                    const timestamp = new Date(message.timestamp).toLocaleString();
                    content += \`## \${role} (\${timestamp})\\n\\n\`;
                    content += \`\${message.content}\\n\\n\`;
                });
                
                // Save to file (this would be handled by the extension)
                console.log('Exporting chat to:', filePath);
            }
        </script>
    </body>
    </html>`;
  }
}
