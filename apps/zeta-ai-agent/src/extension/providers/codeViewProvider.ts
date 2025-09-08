import * as vscode from 'vscode';
import { AIAgent } from '../../core/agent/agent';
import { CodeReview, DebugSolution, CodeOptimization, ActionPlan } from '../../types/shared';
import AI from "AI";
import Action from "Action";
import After from "After";
import Analysis from "Analysis";
import Before from "Before";
import BlinkMacSystemFont from "BlinkMacSystemFont";
import CancellationToken from "CancellationToken";
import Cause from "Cause";
import Code from "Code";
import Complexity from "Complexity";
import Consolas from "Consolas";
import Content from "Content";
import Copy from "Copy";
import Courier from "Courier";
import Current from "Current";
import DOCTYPE from "DOCTYPE";
import Debug from "Debug";
import Dependencies from "Dependencies";
import Estimated from "Estimated";
import Failed from "Failed";
import Files from "Files";
import Fix from "Fix";
import Found from "Found";
import Impact from "Impact";
import Improvements from "Improvements";
import Issues from "Issues";
import Line from "Line";
import Metrics from "Metrics";
import Monaco from "Monaco";
import New from "New";
import No from "No";
import Optimization from "Optimization";
import Overall from "Overall";
import Plan from "Plan";
import Policy from "Policy";
import Position from "Position";
import Prerequisites from "Prerequisites";
import Problem from "Problem";
import Range from "Range";
import Results from "Results";
import Review from "Review";
import Roboto from "Roboto";
import Root from "Root";
import Run from "Run";
import Score from "Score";
import Security from "Security";
import Segoe from "Segoe";
import Solution from "Solution";
import Step from "Step";
import Steps from "Steps";
import Suggestion from "Suggestion";
import Suggestions from "Suggestions";
import UI from "../../../../desktop/src/UI/index";
import UTF from "UTF";
import Uri from "Uri";
import Webview from "Webview";
import WebviewView from "WebviewView";
import WebviewViewProvider from "WebviewViewProvider";
import WebviewViewResolveContext from "WebviewViewResolveContext";
import WorkspaceEdit from "WorkspaceEdit";
import Zeta from "Zeta";
import ZetaCodeViewProvider from "ZetaCodeViewProvider";

export class ZetaCodeViewProvider implements vscode.WebviewViewProvider {
  public static readonly viewType = 'zetaCodeView';

  private _view?: vscode.WebviewView;

  constructor(private agent: AIAgent) {}

  public resolveWebviewView(
    webviewView: vscode.WebviewView,
    _context: vscode.WebviewViewResolveContext,
    _token: vscode.CancellationToken
  ) {
    this._view = webviewView;

    webviewView.webview.options = {
      enableScripts: true,
      localResourceRoots: []
    };

    webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);

    webviewView.webview.onDidReceiveMessage(
      message => {
        switch (message.command) {
        case 'applyFix':
          this.applyFix(message.fix);
          break;
        case 'copyCode':
          vscode.env.clipboard.writeText(message.code);
          vscode.window.showInformationMessage('Code copied to clipboard');
          break;
        case 'openFile':
          if (message.filePath) {
            vscode.commands.executeCommand('vscode.open', vscode.Uri.file(message.filePath));
          }
          break;
        }
      }
    );
  }

  public async showCodeReview(review: CodeReview) {
    if (this._view) {
      this._view.show?.(true);
      this._view.webview.postMessage({
        command: 'showCodeReview',
        review: review
      });
    }
  }

  public async showDebugSolution(solution: DebugSolution) {
    if (this._view) {
      this._view.show?.(true);
      this._view.webview.postMessage({
        command: 'showDebugSolution',
        solution: solution
      });
    }
  }

  public async showOptimization(optimization: CodeOptimization) {
    if (this._view) {
      this._view.show?.(true);
      this._view.webview.postMessage({
        command: 'showOptimization',
        optimization: optimization
      });
    }
  }

  public async showActionPlan(plan: ActionPlan) {
    if (this._view) {
      this._view.show?.(true);
      this._view.webview.postMessage({
        command: 'showActionPlan',
        plan: plan
      });
    }
  }

  private async applyFix(fix: any) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    try {
      const edit = new vscode.WorkspaceEdit();
      
      if (fix.type === 'replace') {
        const document = editor.document;
        const range = new vscode.Range(
          new vscode.Position(fix.line - 1, 0),
          new vscode.Position(fix.line, 0)
        );
        edit.replace(document.uri, range, fix.newCode + '\n');
      } else if (fix.type === 'insert') {
        const position = new vscode.Position(fix.line - 1, 0);
        edit.insert(editor.document.uri, position, fix.newCode + '\n');
      }

      await vscode.workspace.applyEdit(edit);
      vscode.window.showInformationMessage('Fix applied successfully');

    } catch (error) {
      vscode.window.showErrorMessage(`Failed to apply fix: ${error}`);
    }
  }

  private getHtmlForWebview(_webview: vscode.Webview): string {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Security-Policy" content="default-src 'none'; 
          style-src 'unsafe-inline' vscode-resource:; 
          script-src 'unsafe-inline' vscode-resource:; 
          connect-src http://localhost:9100 http://127.0.0.1:9100 https://localhost:9100 https://127.0.0.1:9100; 
          img-src vscode-resource: data:;">
        <title>Zeta AI Code Analysis</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 16px;
                background-color: var(--vscode-editor-background);
                color: var(--vscode-editor-foreground);
                font-size: 13px;
                line-height: 1.4;
            }
            
            .header {
                display: flex;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 8px;
                border-bottom: 1px solid var(--vscode-panel-border);
            }
            
            .title {
                font-size: 16px;
                font-weight: 600;
                margin: 0;
                color: var(--vscode-titleBar-activeForeground);
            }
            
            .content {
                display: none;
            }
            
            .content.active {
                display: block;
            }
            
            .issue {
                background-color: var(--vscode-inputValidation-errorBackground);
                border: 1px solid var(--vscode-inputValidation-errorBorder);
                border-radius: 4px;
                padding: 12px;
                margin-bottom: 12px;
            }
            
            .suggestion {
                background-color: var(--vscode-inputValidation-infoBackground);
                border: 1px solid var(--vscode-inputValidation-infoBorder);
                border-radius: 4px;
                padding: 12px;
                margin-bottom: 12px;
            }
            
            .improvement {
                background-color: var(--vscode-inputValidation-warningBackground);
                border: 1px solid var(--vscode-inputValidation-warningBorder);
                border-radius: 4px;
                padding: 12px;
                margin-bottom: 12px;
            }
            
            .step {
                background-color: var(--vscode-editor-background);
                border: 1px solid var(--vscode-panel-border);
                border-radius: 4px;
                padding: 12px;
                margin-bottom: 8px;
            }
            
            .severity-high { border-left: 4px solid #ff6b6b; }
            .severity-medium { border-left: 4px solid #ffa500; }
            .severity-low { border-left: 4px solid #4ecdc4; }
            
            .code-block {
                background-color: var(--vscode-textCodeBlock-background);
                border: 1px solid var(--vscode-panel-border);
                border-radius: 4px;
                padding: 12px;
                margin: 8px 0;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                overflow-x: auto;
                white-space: pre;
            }
            
            .button {
                background-color: var(--vscode-button-background);
                color: var(--vscode-button-foreground);
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                margin: 4px 4px 4px 0;
                cursor: pointer;
                font-size: 12px;
            }
            
            .button:hover {
                background-color: var(--vscode-button-hoverBackground);
            }
            
            .button.secondary {
                background-color: var(--vscode-button-secondaryBackground);
                color: var(--vscode-button-secondaryForeground);
            }
            
            .metric {
                display: inline-block;
                background-color: var(--vscode-badge-background);
                color: var(--vscode-badge-foreground);
                padding: 2px 6px;
                border-radius: 12px;
                font-size: 11px;
                margin-right: 6px;
            }
            
            .empty-state {
                text-align: center;
                padding: 40px 20px;
                color: var(--vscode-descriptionForeground);
            }
            
            .empty-state .icon {
                font-size: 48px;
                margin-bottom: 16px;
                opacity: 0.6;
            }
            
            h3 {
                margin: 16px 0 8px 0;
                font-size: 14px;
                font-weight: 600;
            }
            
            .complexity-score {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }
            
            .complexity-low { background-color: #28a745; color: white; }
            .complexity-medium { background-color: #ffc107; color: black; }
            .complexity-high { background-color: #dc3545; color: white; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="title">🤖 Zeta AI Analysis</h1>
        </div>
        
        <div id="emptyState" class="empty-state">
            <div class="icon">🔍</div>
            <p>No analysis available</p>
            <p>Run a code review, debug, or optimization command to see results here.</p>
        </div>
        
        <div id="codeReviewContent" class="content">
            <h3>Code Review Results</h3>
            <div id="reviewResults"></div>
        </div>
        
        <div id="debugContent" class="content">
            <h3>Debug Solution</h3>
            <div id="debugResults"></div>
        </div>
        
        <div id="optimizationContent" class="content">
            <h3>Code Optimization</h3>
            <div id="optimizationResults"></div>
        </div>
        
        <div id="actionPlanContent" class="content">
            <h3>Action Plan</h3>
            <div id="actionPlanResults"></div>
        </div>

        <script>
            const vscode = acquireVsCodeApi();
            
            window.addEventListener('message', event => {
                const message = event.data;
                
                switch (message.command) {
                    case 'showCodeReview':
                        showCodeReview(message.review);
                        break;
                    case 'showDebugSolution':
                        showDebugSolution(message.solution);
                        break;
                    case 'showOptimization':
                        showOptimization(message.optimization);
                        break;
                    case 'showActionPlan':
                        showActionPlan(message.plan);
                        break;
                }
            });
            
            function hideAllContent() {
                document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
                document.getElementById('emptyState').style.display = 'none';
            }
            
            function showCodeReview(review) {
                hideAllContent();
                document.getElementById('codeReviewContent').classList.add('active');
                
                const container = document.getElementById('reviewResults');
                container.innerHTML = '';
                
                // Overall score
                if (review.overall_score !== undefined) {
                    const scoreDiv = document.createElement('div');
                    scoreDiv.className = 'metric';
                    scoreDiv.textContent = \`Score: \${review.overall_score}/10\`;
                    container.appendChild(scoreDiv);
                }
                
                // Issues
                if (review.issues && review.issues.length > 0) {
                    const issuesHeader = document.createElement('h3');
                    issuesHeader.textContent = 'Issues Found';
                    container.appendChild(issuesHeader);
                    
                    review.issues.forEach(issue => {
                        const issueDiv = document.createElement('div');
                        issueDiv.className = \`issue severity-\${issue.severity}\`;
                        issueDiv.innerHTML = \`
                            <strong>\${issue.type}</strong> (Line \${issue.line})
                            <p>\${issue.description}</p>
                            \${issue.suggestion ? \`<p><em>Suggestion: \${issue.suggestion}</em></p>\` : ''}
                        \`;
                        container.appendChild(issueDiv);
                    });
                }
                
                // Suggestions
                if (review.suggestions && review.suggestions.length > 0) {
                    const suggestionsHeader = document.createElement('h3');
                    suggestionsHeader.textContent = 'Suggestions';
                    container.appendChild(suggestionsHeader);
                    
                    review.suggestions.forEach(suggestion => {
                        const suggestionDiv = document.createElement('div');
                        suggestionDiv.className = 'suggestion';
                        suggestionDiv.innerHTML = \`
                            <strong>\${suggestion.category}</strong>
                            <p>\${suggestion.description}</p>
                            \${suggestion.example ? \`<div class="code-block">\${suggestion.example}</div>\` : ''}
                        \`;
                        container.appendChild(suggestionDiv);
                    });
                }
            }
            
            function showDebugSolution(solution) {
                hideAllContent();
                document.getElementById('debugContent').classList.add('active');
                
                const container = document.getElementById('debugResults');
                container.innerHTML = '';
                
                // Problem analysis
                if (solution.problem_analysis) {
                    const analysisDiv = document.createElement('div');
                    analysisDiv.innerHTML = \`
                        <h3>Problem Analysis</h3>
                        <p>\${solution.problem_analysis}</p>
                    \`;
                    container.appendChild(analysisDiv);
                }
                
                // Root cause
                if (solution.root_cause) {
                    const causeDiv = document.createElement('div');
                    causeDiv.innerHTML = \`
                        <h3>Root Cause</h3>
                        <p>\${solution.root_cause}</p>
                    \`;
                    container.appendChild(causeDiv);
                }
                
                // Solution steps
                if (solution.solution_steps && solution.solution_steps.length > 0) {
                    const stepsHeader = document.createElement('h3');
                    stepsHeader.textContent = 'Solution Steps';
                    container.appendChild(stepsHeader);
                    
                    solution.solution_steps.forEach((step, index) => {
                        const stepDiv = document.createElement('div');
                        stepDiv.className = 'step';
                        stepDiv.innerHTML = \`
                            <strong>Step \${index + 1}:</strong> \${step.description}
                            \${step.code ? \`<div class="code-block">\${step.code}</div>\` : ''}
                            \${step.code ? \`<button class="button" onclick="copyCode('\${escapeHtml(step.code)}')">Copy Code</button>\` : ''}
                        \`;
                        container.appendChild(stepDiv);
                    });
                }
            }
            
            function showOptimization(optimization) {
                hideAllContent();
                document.getElementById('optimizationContent').classList.add('active');
                
                const container = document.getElementById('optimizationResults');
                container.innerHTML = '';
                
                // Current metrics
                if (optimization.current_metrics) {
                    const metricsDiv = document.createElement('div');
                    metricsDiv.innerHTML = '<h3>Current Metrics</h3>';
                    Object.entries(optimization.current_metrics).forEach(([key, value]) => {
                        const metric = document.createElement('span');
                        metric.className = 'metric';
                        metric.textContent = \`\${key}: \${value}\`;
                        metricsDiv.appendChild(metric);
                    });
                    container.appendChild(metricsDiv);
                }
                
                // Improvements
                if (optimization.improvements && optimization.improvements.length > 0) {
                    const improvementsHeader = document.createElement('h3');
                    improvementsHeader.textContent = 'Improvements';
                    container.appendChild(improvementsHeader);
                    
                    optimization.improvements.forEach(improvement => {
                        const improvementDiv = document.createElement('div');
                        improvementDiv.className = 'improvement';
                        improvementDiv.innerHTML = \`
                            <strong>\${improvement.type}</strong>
                            <p>\${improvement.description}</p>
                            \${improvement.before_code ? \`
                                <div>
                                    <strong>Before:</strong>
                                    <div class="code-block">\${improvement.before_code}</div>
                                </div>
                            \` : ''}
                            \${improvement.after_code ? \`
                                <div>
                                    <strong>After:</strong>
                                    <div class="code-block">\${improvement.after_code}</div>
                                    <button class="button" onclick="copyCode('\${escapeHtml(improvement.after_code)}')">Copy Code</button>
                                </div>
                            \` : ''}
                            \${improvement.impact ? \`<p><em>Impact: \${improvement.impact}</em></p>\` : ''}
                        \`;
                        container.appendChild(improvementDiv);
                    });
                }
            }
            
            function showActionPlan(plan) {
                hideAllContent();
                document.getElementById('actionPlanContent').classList.add('active');
                
                const container = document.getElementById('actionPlanResults');
                container.innerHTML = '';
                
                // Plan overview
                const overviewDiv = document.createElement('div');
                overviewDiv.innerHTML = \`
                    <h3>\${plan.title}</h3>
                    <p>\${plan.description}</p>
                    <div class="metric">Estimated time: \${plan.estimated_time}</div>
                    <div class="complexity-score complexity-\${plan.complexity}">Complexity: \${plan.complexity}</div>
                \`;
                container.appendChild(overviewDiv);
                
                // Steps
                if (plan.steps && plan.steps.length > 0) {
                    const stepsHeader = document.createElement('h3');
                    stepsHeader.textContent = 'Steps';
                    container.appendChild(stepsHeader);
                    
                    plan.steps.forEach((step, index) => {
                        const stepDiv = document.createElement('div');
                        stepDiv.className = 'step';
                        stepDiv.innerHTML = \`
                            <strong>Step \${index + 1}:</strong> \${step.description}
                            <div class="metric">Estimated: \${step.estimated_time}</div>
                            \${step.dependencies && step.dependencies.length > 0 ? 
                                \`<p><em>Dependencies: \${step.dependencies.join(', ')}</em></p>\` : ''}
                            \${step.files && step.files.length > 0 ? 
                                \`<p><strong>Files:</strong> \${step.files.join(', ')}</p>\` : ''}
                        \`;
                        container.appendChild(stepDiv);
                    });
                }
                
                // Prerequisites
                if (plan.prerequisites && plan.prerequisites.length > 0) {
                    const prereqHeader = document.createElement('h3');
                    prereqHeader.textContent = 'Prerequisites';
                    container.appendChild(prereqHeader);
                    
                    const prereqList = document.createElement('ul');
                    plan.prerequisites.forEach(prereq => {
                        const li = document.createElement('li');
                        li.textContent = prereq;
                        prereqList.appendChild(li);
                    });
                    container.appendChild(prereqList);
                }
            }
            
            function copyCode(code) {
                vscode.postMessage({
                    command: 'copyCode',
                    code: code
                });
            }
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML.replace(/'/g, "\\\\'");
            }
        </script>
    </body>
    </html>`;
  }
}
