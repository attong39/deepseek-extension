import { execSync } from 'child_process';
import * as fs from 'fs';
import ollama from 'ollama';
import * as path from 'path';
import * as vscode from 'vscode';
import { AIAgent } from './aiAgent';

// Interfaces for better type safety
interface WebviewMessage {
	command: string;
	text?: string;
}

interface OllamaModel {
	name: string;
	modified_at?: string;
	size?: number;
}

// ---------- Helper: fetch available models ----------
const fetchOllamaModels = async (): Promise<string[]> => {
  try {
    const stdout = execSync('curl -s http://127.0.0.1:11434/api/tags')
                     .toString();
    const obj = JSON.parse(stdout);
    if (obj?.models && Array.isArray(obj.models)) {
      return obj.models
        .map((m: OllamaModel) => m?.name)
        .filter((name: string | undefined): name is string => name !== null && name !== undefined && typeof name === 'string');
    }
  } catch (error) {
    console.warn('Failed to fetch models from Ollama:', error);
  }

  // Fallback: common DeepSeek and other models
  return [
    'deepseek-r1:latest',
    'deepseek-r1:1.5b',
    'deepseek-r1:7b',
    'deepseek-r1:14b',
    'deepseek-r1:32b',
    'deepseek-r1:70b',
    'deepseek-coder:latest',
    'deepseek-coder:1.3b',
    'deepseek-coder:6.7b',
    'deepseek-coder:33b',
    'llama2:7b',
    'llama2:13b',
    'llama2:70b',
    'codellama:7b',
    'codellama:13b',
    'codellama:34b'
  ];
};

// AI Agent instance
let aiAgent: AIAgent;

// Python Development Workflow Integration
const PYTHON_FILE_PATTERNS = ['**/*.py', '**/*.pyi', '**/*.pyx', '**/*.pxd'];
const PYTHON_COMMANDS = {
	'deep-seek.python.start': 'Start Python Chat',
	'deep-seek.python.review': 'Review Current Python File',
	'deep-seek.python.debug': 'Debug Python Code',
	'deep-seek.python.optimize': 'Optimize Python Code',
	'deep-seek.python.document': 'Generate Documentation',
	'deep-seek.python.test': 'Generate Tests'
};

// Custom Prompts for Code Review
const CODE_REVIEW_PROMPTS = {
	security: `
Please review this Python code for security vulnerabilities:
- SQL injection risks
- Command injection
- Path traversal
- Authentication bypass
- Data exposure
- Input validation issues

Code to review:
{code}

Provide specific recommendations with code examples for fixes.
`,
	performance: `
Analyze this Python code for performance optimizations:
- Algorithm complexity
- Memory usage patterns
- I/O operations
- Database queries
- Caching opportunities
- Async/await usage

Code to review:
{code}

Suggest specific optimizations with before/after code examples.
`,
	best_practices: `
Review this Python code against best practices:
- PEP 8 compliance
- Type hints usage
- Error handling
- Code structure
- Naming conventions
- Documentation

Code to review:
{code}

Provide detailed feedback with improvement suggestions.
`,
	testing: `
Analyze this Python code for testability and suggest testing improvements:
- Unit test coverage
- Integration test needs
- Mock requirements
- Edge cases
- Error scenarios

Code to review:
{code}

Suggest comprehensive testing strategy with code examples.
`
};


class PythonProjectDetector {
	isPythonFile(document: vscode.TextDocument): boolean {
		return PYTHON_FILE_PATTERNS.some(pattern =>
			vscode.languages.match({ pattern }, document) !== 0
		);
	}

	isPythonProject(): boolean {
		const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
		if (!workspaceFolder) {
			return false;
		}

		const pythonFiles = [
			'requirements.txt',
			'pyproject.toml',
			'setup.py',
			'Pipfile',
			'poetry.lock'
		];

		return pythonFiles.some(file =>
			fs.existsSync(path.join(workspaceFolder.uri.fsPath, file))
		);
	}
}

class PythonWorkflowManager {
	private pythonChatStarted = false;

	handlePythonFileOpen(document: vscode.TextDocument): void {
		if (this.pythonChatStarted) {
			return;
		}

		const detector = new PythonProjectDetector();
		if (detector.isPythonProject()) {
			this.pythonChatStarted = true;
			vscode.window.showInformationMessage(
				'Python project detected! Starting DeepSeek Python Assistant...',
				'Start Chat', 'Later'
			).then(selection => {
				if (selection === 'Start Chat') {
					vscode.commands.executeCommand('deep-seek.python.start');
				}
			});
		}
	}
}

async function handlePythonCommand(commandId: string, context: vscode.ExtensionContext): Promise<void> {
	const activeEditor = vscode.window.activeTextEditor;
	if (!activeEditor) {
		vscode.window.showErrorMessage('No active Python file found');
		return;
	}

	const document = activeEditor.document;
	const code = document.getText();
	const fileName = path.basename(document.fileName);

	let prompt = '';

	switch (commandId) {
		case 'deep-seek.python.start':
			prompt = `You are a Python development assistant. I have opened a Python file: ${fileName}. Please help me with Python development tasks.`;
			break;
		case 'deep-seek.python.review':
			prompt = `Please review this Python code for best practices, security, and performance:\n\n${code}`;
			break;
		case 'deep-seek.python.debug':
			prompt = `Please help debug this Python code. Analyze for potential issues:\n\n${code}`;
			break;
		case 'deep-seek.python.optimize':
			prompt = `Please optimize this Python code for better performance:\n\n${code}`;
			break;
		case 'deep-seek.python.document':
			prompt = `Please generate comprehensive documentation for this Python code:\n\n${code}`;
			break;
		case 'deep-seek.python.test':
			prompt = `Please generate unit tests for this Python code:\n\n${code}`;
			break;
	}

	if (prompt) {
		await startDeepSeekChatWithPrompt(prompt, context);
	}
}

async function startDeepSeekChatWithPrompt(initialPrompt: string, context: vscode.ExtensionContext): Promise<void> {
	try {
		// Get the currently selected model
		const selectedModel = context.globalState.get('deepseek.model', 'deepseek-r1:latest');
		await pullModel(selectedModel);
		const panel = vscode.window.createWebviewPanel(
			'deep-seek-python',
			'DeepSeek Python Assistant',
			vscode.ViewColumn.Beside,
			{
				enableScripts: true
			}
		);
		panel.webview.html = getWebviewContent(context);

		// Send initial prompt
		setTimeout(() => {
			panel.webview.postMessage({ command: 'setInitialPrompt', text: initialPrompt });
		}, 1000);

		// Handle chat messages
		panel.webview.onDidReceiveMessage(async (message: WebviewMessage) => {
			if (message.command === 'chat' && message.text) {
				const userPrompt = message.text;
				let responseText = '';

				try {
					const streamResponse = await ollama.chat({
						model: selectedModel,
						messages: [{ role: 'user', content: userPrompt}],
						stream: true
					});

					for await (const part of streamResponse) {
						const filteredContent = filterThinkTags(part.message.content);
						if (filteredContent) {
							responseText += filteredContent + ' ';
						}
					}
					responseText = filterThinkTags(responseText);
					panel.webview.postMessage({ command: 'chatResponse', text: responseText.trim() });

				} catch (error) {
					panel.webview.postMessage({ command: 'chatResponse', text: `Error: ${String(error)}` });
				}
			}
		});
	} catch (error) {
		vscode.window.showErrorMessage(`Failed to start DeepSeek Python Chat: ${String(error)}`);
	}
}


async function pullModel(model: string) {
	try {
		await ollama.pull({ model });
	} catch (error) {
		vscode.window.showErrorMessage(`Failed to pull model: ${String(error)}`);
		throw error; 
	}
}


function filterThinkTags(content: string): string {
	return content.replace(/<think>.*?<\/think>/gs, '').trim();
}


function getWebviewContent(context: vscode.ExtensionContext): string {
	const htmlPath = path.join(context.extensionPath, 'webview.html');
	return fs.readFileSync(htmlPath, 'utf8');
}

// Activate the extension
export function activate(context: vscode.ExtensionContext) {
	console.log('DeepSeek extension is now active!');

	// Initialize AI Agent
	try {
		aiAgent = new AIAgent(context);
		console.log('AI Agent initialized successfully');
	} catch (error) {
		console.error('Failed to initialize AI Agent:', error);
		vscode.window.showErrorMessage(`AI Agent initialization failed: ${error}`);
	}

	// Register AI Agent commands
	const aiAgentCommands = [
		vscode.commands.registerCommand('deepseek.ai.interactive', () => aiAgent?.interactiveMode()),
		vscode.commands.registerCommand('deepseek.ai.review', () => aiAgent?.runTaskOnActiveFile('review')),
		vscode.commands.registerCommand('deepseek.ai.debug', () => aiAgent?.runTaskOnActiveFile('debug')),
		vscode.commands.registerCommand('deepseek.ai.optimize', () => aiAgent?.runTaskOnActiveFile('optimize')),
		vscode.commands.registerCommand('deepseek.ai.status', () => aiAgent?.showStatus())
	];
	
	context.subscriptions.push(...aiAgentCommands);

	// New command: "DeepSeek: Choose Model"
	const chooseModelCmd = vscode.commands.registerCommand('deepseek.agent.chooseModel', async () => {
		try {
			// Show loading message
			await vscode.window.withProgress({
				location: vscode.ProgressLocation.Notification,
				title: 'Loading available models...',
				cancellable: false
			}, async (progress) => {
				const models = await fetchOllamaModels();

				if (models.length === 0) {
					vscode.window.showErrorMessage('❌ No models found. Please ensure Ollama is running and has models installed.');
					return;
				}

				// Get current model
				const currentModel = context.globalState.get('deepseek.model', 'deepseek-r1:latest');

				// Add current model indicator
				const modelItems = models.map(model => ({
					label: model,
					description: model === currentModel ? 'Currently selected' : undefined,
					detail: model === currentModel ? '✓' : undefined
				}));

				const chosen = await vscode.window.showQuickPick(modelItems, {
					placeHolder: `Chọn model DeepSeek để sử dụng (Current: ${currentModel})`,
					matchOnDescription: true,
					matchOnDetail: true
				});

				if (chosen) {
					context.globalState.update('deepseek.model', chosen.label);
					
					// Update AI Agent model if it exists
					if (aiAgent) {
						aiAgent.updateModel();
					}
					
					vscode.window.showInformationMessage(`✅ Chọn model: ${chosen.label}`);

					// Ask user if they want to reload immediately
					const reloadChoice = await vscode.window.showInformationMessage(
						`Model changed to ${chosen.label}. Reload VS Code to apply changes?`,
						'Reload Now',
						'Later'
					);

					if (reloadChoice === 'Reload Now') {
						vscode.commands.executeCommand('workbench.action.reloadWindow');
					}
				}
			});
		} catch (error) {
			vscode.window.showErrorMessage(`❌ Failed to load models: ${error}`);
		}
	});

	context.subscriptions.push(chooseModelCmd);

	// Command to show current model
	const showCurrentModelCmd = vscode.commands.registerCommand('deepseek.agent.showCurrentModel', async () => {
		const currentModel = context.globalState.get('deepseek.model', 'deepseek-r1:latest');
		const modelInfo = `Current model: ${currentModel}`;

		vscode.window.showInformationMessage(modelInfo, 'Change Model', 'OK').then(selection => {
			if (selection === 'Change Model') {
				vscode.commands.executeCommand('deepseek.agent.chooseModel');
			}
		});
	});

	context.subscriptions.push(showCurrentModelCmd);

	// Python Development Workflow Integration
	const pythonProjectDetector = new PythonProjectDetector();
	const pythonWorkflowManager = new PythonWorkflowManager();

	// Auto-start Python chat when opening Python files
	vscode.workspace.onDidOpenTextDocument((document) => {
		if (pythonProjectDetector.isPythonFile(document)) {
			pythonWorkflowManager.handlePythonFileOpen(document);
		}
	});

	// Check current open files on activation
	vscode.workspace.textDocuments.forEach((document) => {
		if (pythonProjectDetector.isPythonFile(document)) {
			pythonWorkflowManager.handlePythonFileOpen(document);
		}
	});

	// Register Python-specific commands
	Object.entries(PYTHON_COMMANDS).forEach(([commandId, commandName]) => {
		const disposable = vscode.commands.registerCommand(commandId, async () => {
			await handlePythonCommand(commandId, context);
		});
		context.subscriptions.push(disposable);
	});

	const disposable = vscode.commands.registerCommand('deep-seek.start', async () => {
		try {
			// Get the currently selected model
			const selectedModel = context.globalState.get('deepseek.model', 'deepseek-r1:latest');
			await pullModel(selectedModel);
			const panel = vscode.window.createWebviewPanel(
				'deep-seek',
				'Deep Seek Chat',
				vscode.ViewColumn.Beside,
				{
					enableScripts: true
				}
			);
			panel.webview.html = getWebviewContent(context);
			panel.webview.onDidReceiveMessage(async (message: WebviewMessage) => {
				if (message.command === 'chat' && message.text) {
					const userPrompt = message.text;
					let responseText = '';

					try {
						const streamResponse = await ollama.chat({
							model: selectedModel,
							messages: [{ role: 'user', content: userPrompt}],
							stream: true
						});

						for await (const part of streamResponse) {
							const filteredContent = filterThinkTags(part.message.content);
							if (filteredContent) {
								responseText += filteredContent + ' ';
							}
						}
						responseText = filterThinkTags(responseText);
						panel.webview.postMessage({ command: 'chatResponse', text: responseText.trim() });
					
					} catch (error) {
						panel.webview.postMessage({ command: 'chatResponse', text: `Error: ${String(error)}` });
					}
				}
			});
		} catch (error) {
			vscode.window.showErrorMessage(`Failed to start Deep Seek Chat: ${String(error)}`);
		}
	});

	context.subscriptions.push(disposable);
}

// Deactivate the extension
export function deactivate() {
	// Extension cleanup if needed
}
