/**
 * Tool Executor Engine
 * Provides actual implementations for tools used by ReAct planner
 * Handles Git, Shell, File operations với safety controls
 */

import { spawn } from 'child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join, resolve } from 'path';
import Additional from "Additional";
import Build from "Build";
import Check from "Check";
import Clean from "Clean";
import Command from "Command";
import D from "D";
import DIR from "DIR";
import Device from "Device";
import Directory from "Directory";
import Engine from "Engine";
import Error from "Error";
import Execute from "Execute";
import ExecutionResult from "ExecutionResult";
import Executor from "Executor";
import FILE from "FILE";
import File from "File";
import Get from "Get";
import Git from "Git";
import Handles from "Handles";
import Ignore from "Ignore";
import Insufficient from "Insufficient";
import List from "List";
import MODERATE from "MODERATE";
import Only from "Only";
import PERMISSIVE from "PERMISSIVE";
import Parse from "Parse";
import Partial from "Partial";
import Process from "Process";
import Provides from "Provides";
import ReAct from "ReAct";
import Read from "Read";
import Record from "Record";
import Resolve from "Resolve";
import SIGTERM from "SIGTERM";
import STRICT from "STRICT";
import Safety from "Safety";
import Set from "Set";
import Shell from "Shell";
import Simple from "Simple";
import System from "System";
import Temp from "Temp";
import Tool from "Tool";
import ToolExecutionContext from "ToolExecutionContext";
import ToolExecutor from "./ToolExecutor";
import Update from "Update";
import Validate from "Validate";
import Working from "Working";
import Write from "Write";
import Writing from "Writing";

export interface ToolExecutionContext {
  workingDirectory: string;
  environment: Record<string, string>;
  timeoutMs: number;
  safetyLevel: 'STRICT' | 'MODERATE' | 'PERMISSIVE';
}

export interface ExecutionResult {
  success: boolean;
  output: string;
  error?: string;
  exitCode?: number;
  executionTime: number;
  metadata?: Record<string, any>;
}

export class ToolExecutor {
  private readonly defaultContext: ToolExecutionContext = {
    workingDirectory: process.cwd(),
    environment: process.env as Record<string, string>,
    timeoutMs: 30000, // 30 seconds default timeout
    safetyLevel: 'MODERATE'
  };

  /**
   * Execute Git command với safety checks
   */
  async executeGitCommand(
    command: string, 
    args: Record<string, any>,
    context?: Partial<ToolExecutionContext>
  ): Promise<ExecutionResult> {
    const ctx = { ...this.defaultContext, ...context };
    
    // Build git command
    const gitArgs = this.buildGitArgs(command, args);
    
    // Safety checks for git commands
    if (!this.isGitCommandSafe(command, gitArgs, ctx.safetyLevel)) {
      return {
        success: false,
        error: `Git command '${command}' blocked by safety policy`,
        output: '',
        executionTime: 0
      };
    }

    return await this.executeCommand('git', gitArgs, ctx);
  }

  /**
   * Execute shell command với sandboxing
   */
  async executeShellCommand(
    command: string,
    context?: Partial<ToolExecutionContext>
  ): Promise<ExecutionResult> {
    const ctx = { ...this.defaultContext, ...context };

    // Safety checks for shell commands
    if (!this.isShellCommandSafe(command, ctx.safetyLevel)) {
      return {
        success: false,
        error: `Shell command blocked by safety policy: ${command}`,
        output: '',
        executionTime: 0
      };
    }

    // Parse command and arguments
    const [cmd, ...args] = this.parseShellCommand(command);
    
    return await this.executeCommand(cmd, args, ctx);
  }

  /**
   * Read file contents với path validation
   */
  async readFile(filePath: string, context?: Partial<ToolExecutionContext>): Promise<ExecutionResult> {
    const ctx = { ...this.defaultContext, ...context };
    const startTime = Date.now();

    try {
      // Resolve and validate path
      const resolvedPath = resolve(ctx.workingDirectory, filePath);
      
      if (!this.isPathSafe(resolvedPath, ctx.safetyLevel)) {
        return {
          success: false,
          error: `File path blocked by safety policy: ${filePath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      if (!existsSync(resolvedPath)) {
        return {
          success: false,
          error: `File not found: ${filePath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      const content = readFileSync(resolvedPath, 'utf-8');
      
      return {
        success: true,
        output: content,
        executionTime: Date.now() - startTime,
        metadata: {
          filePath: resolvedPath,
          size: content.length
        }
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        output: '',
        executionTime: Date.now() - startTime
      };
    }
  }

  /**
   * Write file với safety checks
   */
  async writeFile(
    filePath: string, 
    content: string,
    context?: Partial<ToolExecutionContext>
  ): Promise<ExecutionResult> {
    const ctx = { ...this.defaultContext, ...context };
    const startTime = Date.now();

    try {
      // Resolve and validate path
      const resolvedPath = resolve(ctx.workingDirectory, filePath);
      
      if (!this.isPathSafe(resolvedPath, ctx.safetyLevel)) {
        return {
          success: false,
          error: `File path blocked by safety policy: ${filePath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      // Additional safety checks for file writing
      if (ctx.safetyLevel === 'STRICT' && this.isSystemFile(resolvedPath)) {
        return {
          success: false,
          error: `Writing to system file blocked: ${filePath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      writeFileSync(resolvedPath, content, 'utf-8');
      
      return {
        success: true,
        output: `File written successfully: ${filePath} (${content.length} bytes)`,
        executionTime: Date.now() - startTime,
        metadata: {
          filePath: resolvedPath,
          size: content.length
        }
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        output: '',
        executionTime: Date.now() - startTime
      };
    }
  }

  /**
   * List directory contents
   */
  async listDirectory(
    dirPath = '.',
    context?: Partial<ToolExecutionContext>
  ): Promise<ExecutionResult> {
    const ctx = { ...this.defaultContext, ...context };
    const startTime = Date.now();

    try {
      const resolvedPath = resolve(ctx.workingDirectory, dirPath);
      
      if (!this.isPathSafe(resolvedPath, ctx.safetyLevel)) {
        return {
          success: false,
          error: `Directory path blocked by safety policy: ${dirPath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      if (!existsSync(resolvedPath)) {
        return {
          success: false,
          error: `Directory not found: ${dirPath}`,
          output: '',
          executionTime: Date.now() - startTime
        };
      }

      const entries = readdirSync(resolvedPath, { withFileTypes: true });
      const listing = entries.map(entry => {
        const type = entry.isDirectory() ? 'DIR' : 'FILE';
        return `${type}: ${entry.name}`;
      }).join('\n');

      return {
        success: true,
        output: listing,
        executionTime: Date.now() - startTime,
        metadata: {
          dirPath: resolvedPath,
          count: entries.length
        }
      };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        output: '',
        executionTime: Date.now() - startTime
      };
    }
  }

  /**
   * Execute command với process spawning
   */
  private async executeCommand(
    command: string,
    args: string[],
    context: ToolExecutionContext
  ): Promise<ExecutionResult> {
    const startTime = Date.now();

    return new Promise((resolve) => {
      const child = spawn(command, args, {
        cwd: context.workingDirectory,
        env: context.environment,
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let stdout = '';
      let stderr = '';

      child.stdout?.on('data', (data) => {
        stdout += data.toString();
      });

      child.stderr?.on('data', (data) => {
        stderr += data.toString();
      });

      // Set timeout
      const timeout = setTimeout(() => {
        child.kill('SIGTERM');
        resolve({
          success: false,
          error: `Command timed out after ${context.timeoutMs}ms`,
          output: stdout,
          executionTime: Date.now() - startTime
        });
      }, context.timeoutMs);

      child.on('close', (code) => {
        clearTimeout(timeout);
        
        const executionTime = Date.now() - startTime;
        const success = code === 0;

        resolve({
          success,
          output: stdout,
          error: success ? undefined : stderr,
          exitCode: code || undefined,
          executionTime,
          metadata: {
            command,
            args
          }
        });
      });

      child.on('error', (error) => {
        clearTimeout(timeout);
        resolve({
          success: false,
          error: error.message,
          output: stdout,
          executionTime: Date.now() - startTime
        });
      });
    });
  }

  /**
   * Build git arguments from command and parameters
   */
  private buildGitArgs(command: string, args: Record<string, any>): string[] {
    const gitArgs = [command];

    switch (command) {
    case 'status':
      return this.buildStatusArgs(gitArgs, args);
    case 'commit':
      return this.buildCommitArgs(gitArgs, args);
    case 'add':
      return this.buildAddArgs(gitArgs, args);
    case 'push':
    case 'pull':
      return this.buildRemoteArgs(gitArgs, args);
    default:
      return gitArgs;
    }
  }

  private buildStatusArgs(gitArgs: string[], args: Record<string, any>): string[] {
    gitArgs.push('--porcelain');
    return gitArgs;
  }

  private buildCommitArgs(gitArgs: string[], args: Record<string, any>): string[] {
    if (args.message) {
      gitArgs.push('-m', args.message);
    }
    if (args.all) {
      gitArgs.push('-a');
    }
    return gitArgs;
  }

  private buildAddArgs(gitArgs: string[], args: Record<string, any>): string[] {
    if (args.files) {
      gitArgs.push(...(Array.isArray(args.files) ? args.files : [args.files]));
    } else {
      gitArgs.push('.');
    }
    return gitArgs;
  }

  private buildRemoteArgs(gitArgs: string[], args: Record<string, any>): string[] {
    if (args.remote) gitArgs.push(args.remote);
    if (args.branch) gitArgs.push(args.branch);
    return gitArgs;
  }

  /**
   * Parse shell command into command and arguments
   */
  private parseShellCommand(command: string): string[] {
    // Simple parsing - can be enhanced for more complex scenarios
    return command.trim().split(/\s+/);
  }

  /**
   * Check if git command is safe to execute
   */
  private isGitCommandSafe(command: string, args: string[], safetyLevel: string): boolean {
    const dangerousCommands = ['reset --hard', 'clean -fd', 'branch -D'];
    const commandString = [command, ...args].join(' ');

    if (safetyLevel === 'STRICT') {
      // Only allow read-only operations
      const readOnlyCommands = ['status', 'log', 'show', 'diff', 'branch', 'ls-files'];
      return readOnlyCommands.includes(command);
    }

    // Check for dangerous operations
    return !dangerousCommands.some(dangerous => commandString.includes(dangerous));
  }

  /**
   * Check if shell command is safe to execute
   */
  private isShellCommandSafe(command: string, safetyLevel: string): boolean {
    const dangerousPatterns = [
      /rm\s+-rf/,
      /del\s+\/[sf]/i,
      /format/i,
      /fdisk/,
      /dd\s+if=/,
      />\s*\/dev\/null/,
      /sudo/,
      /chmod\s+777/,
      /curl.*\|\s*sh/,
      /wget.*\|\s*sh/
    ];

    if (safetyLevel === 'STRICT') {
      // Only allow very basic commands
      const allowedCommands = ['ls', 'pwd', 'echo', 'cat', 'head', 'tail', 'grep', 'find'];
      const firstCommand = command.trim().split(/\s+/)[0];
      return allowedCommands.includes(firstCommand);
    }

    // Check for dangerous patterns
    return !dangerousPatterns.some(pattern => pattern.test(command));
  }

  /**
   * Check if file path is safe
   */
  private isPathSafe(path: string, safetyLevel: string): boolean {
    const dangerousPatterns = [
      /\.\./,           // Directory traversal
      /\/etc\//,        // System configs
      /\/proc\//,       // Process info
      /\/sys\//,        // System info
      /\/dev\//,        // Device files
      /\/var\/log\//,   // System logs
      /\/tmp\//         // Temp files (in strict mode)
    ];

    if (safetyLevel === 'STRICT') {
      // Only allow files in current working directory and subdirectories
      const workingDir = resolve(this.defaultContext.workingDirectory);
      const resolvedPath = resolve(path);
      if (!resolvedPath.startsWith(workingDir)) {
        return false;
      }
    }

    return !dangerousPatterns.some(pattern => pattern.test(path));
  }

  /**
   * Check if file is a system file
   */
  private isSystemFile(path: string): boolean {
    const systemPaths = [
      '/etc/',
      '/usr/',
      '/bin/',
      '/sbin/',
      '/var/',
      '/proc/',
      '/sys/',
      '/dev/'
    ];

    return systemPaths.some(systemPath => path.startsWith(systemPath));
  }

  /**
   * Get current execution context
   */
  getDefaultContext(): ToolExecutionContext {
    return { ...this.defaultContext };
  }

  /**
   * Update default context
   */
  updateDefaultContext(updates: Partial<ToolExecutionContext>): void {
    Object.assign(this.defaultContext, updates);
  }

  /**
   * Validate tool execution environment
   */
  async validateEnvironment(): Promise<{ valid: boolean; issues: string[] }> {
    const issues: string[] = [];

    // Check git availability
    try {
      await this.executeCommand('git', ['--version'], this.defaultContext);
    } catch {
      issues.push('Git not available');
    }

    // Check working directory
    if (!existsSync(this.defaultContext.workingDirectory)) {
      issues.push('Working directory does not exist');
    }

    // Check permissions
    try {
      const testFile = join(this.defaultContext.workingDirectory, '.tool-test');
      writeFileSync(testFile, 'test');
      readFileSync(testFile);
      // Clean up
      try {
        require('fs').unlinkSync(testFile);
      } catch {
        // Ignore cleanup errors
      }
    } catch {
      issues.push('Insufficient file system permissions');
    }

    return {
      valid: issues.length === 0,
      issues
    };
  }
}
