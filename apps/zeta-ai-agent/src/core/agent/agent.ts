import {
  ActionPlan,
  AgentConfig,
  AgentInteraction,
  CodeContext,
  CodeOptimization,
  CodeReview,
  DebugSolution
} from '../../types/shared';
import { OllamaClient } from '../ollama/client';
import { CodeAnalyzer } from './cognitive/codeAnalyzer';
import { MemoryManager } from './memory/memoryManager';
import { ActionPlanner } from './planner/actionPlanner';
import AI from "AI";
import AIAgent from "AIAgent";
import Action from "Action";
import Agent from "./Agent";
import Available from "Available";
import Build from "Build";
import Cannot from "Cannot";
import Chat from "../../../../desktop/src/pages/Chat";
import Check from "Check";
import Code from "Code";
import Configuration from "Configuration";
import Debug from "Debug";
import Default from "Default";
import Error from "Error";
import Failed from "Failed";
import Generated from "Generated";
import Get from "Get";
import Math from "Math";
import Memory from "../../../../desktop/src/Memory/index";
import Ollama from "Ollama";
import Optimize from "Optimize";
import Partial from "Partial";
import Perform from "Perform";
import Plan from "Plan";
import Please from "Please";
import Provide from "Provide";
import Review from "Review";
import Store from "Store";
import Validate from "Validate";
import Verify from "Verify";
import You from "You";
import Zeta from "Zeta";

export class AIAgent {
  private ollama: OllamaClient;
  private codeAnalyzer: CodeAnalyzer;
  private memoryManager: MemoryManager;
  private actionPlanner: ActionPlanner;
  private config: AgentConfig;

  constructor(config: Partial<AgentConfig> = {}) {
    this.config = {
      ollama_url: config.ollama_url || 'http://localhost:11434',
      default_model: config.default_model || 'deepseek-coder',
      max_context_size: config.max_context_size || 1000,
      enable_caching: config.enable_caching ?? true,
      cache_ttl: config.cache_ttl || 3600,
      rate_limit: config.rate_limit || 60,
      security_policy: config.security_policy || {
        max_code_size: 100000,
        allowed_file_extensions: ['.ts', '.js', '.py', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.rs'],
        blocked_patterns: [/eval\(/i, /exec\(/i, /system\(/i],
        max_context_size: 10000,
        rate_limit_per_minute: 60
      },
      performance_monitoring: config.performance_monitoring ?? true,
      log_level: config.log_level || 'info'
    };

    this.ollama = new OllamaClient({
      baseUrl: this.config.ollama_url,
      defaultModel: this.config.default_model
    });

    this.codeAnalyzer = new CodeAnalyzer(this.ollama);
    this.memoryManager = new MemoryManager(this.config.max_context_size);
    this.actionPlanner = new ActionPlanner(this.ollama);
  }

  async initialize(): Promise<void> {
    // Check Ollama connection
    const isHealthy = await this.ollama.healthCheck();
    if (!isHealthy) {
      throw new Error('Cannot connect to Ollama server. Please ensure Ollama is running.');
    }

    // Verify default model is available
    const isModelAvailable = await this.ollama.validateModel(this.config.default_model);
    if (!isModelAvailable) {
      console.warn(`Default model ${this.config.default_model} not found. Available models:`);
      const models = await this.ollama.listModels();
      console.log(models.models.map(m => m.name));
    }

    this.log('info', 'Zeta AI Agent initialized successfully');
  }

  async reviewCode(code: string, context: CodeContext): Promise<CodeReview> {
    const startTime = Date.now();
    
    try {
      // Validate input
      this.validateCodeInput(code);
      
      // Get relevant context from memory (for future context-aware improvements)
      await this.memoryManager.getRelevantContext(
        `code review ${context.language} ${context.filePath}`
      );

      // Perform code review
      const review = await this.codeAnalyzer.reviewCode(code, context);

      // Store interaction in memory
      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'code_review',
        user_input: `Review code in ${context.filePath}`,
        agent_response: JSON.stringify(review),
        context,
        success: true,
        action_type: 'code_review',
        target: context.filePath,
        result: review
      });

      this.log('info', `Code review completed for ${context.filePath} in ${Date.now() - startTime}ms`);
      return review;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'code_review',
        user_input: `Review code in ${context.filePath}`,
        agent_response: `Error: ${errorMessage}`,
        context,
        success: false,
        action_type: 'code_review',
        target: context.filePath,
        result: { error: errorMessage }
      });

      throw error;
    }
  }

  async debugCode(error: string, code: string, context: CodeContext): Promise<DebugSolution> {
    const startTime = Date.now();
    
    try {
      this.validateCodeInput(code);

      // Get relevant debugging context (for future context-aware improvements)
      await this.memoryManager.getRelevantContext(
        `debug error ${error} ${context.language}`
      );

      const solution = await this.codeAnalyzer.debugCode(error, code, context);

      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'debug',
        user_input: `Debug error: ${error}`,
        agent_response: JSON.stringify(solution),
        context,
        success: true,
        action_type: 'debug',
        target: context.filePath,
        result: solution
      });

      this.log('info', `Debug completed for ${context.filePath} in ${Date.now() - startTime}ms`);
      return solution;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'debug',
        user_input: `Debug error: ${errorMessage}`,
        agent_response: `Error: ${errorMessage}`,
        context,
        success: false,
        action_type: 'debug',
        target: context.filePath,
        result: { error: errorMessage }
      });

      throw error;
    }
  }

  async optimizeCode(code: string, context: CodeContext, metrics?: string[]): Promise<CodeOptimization> {
    const startTime = Date.now();
    
    try {
      this.validateCodeInput(code);

      const optimization = await this.codeAnalyzer.optimizeCode(code, context, metrics);

      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'optimization',
        user_input: `Optimize code in ${context.filePath}`,
        agent_response: JSON.stringify(optimization),
        context,
        success: true,
        action_type: 'optimize',
        target: context.filePath,
        result: optimization
      });

      this.log('info', `Code optimization completed for ${context.filePath} in ${Date.now() - startTime}ms`);
      return optimization;

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'optimization',
        user_input: `Optimize code in ${context.filePath}`,
        agent_response: `Error: ${errorMessage}`,
        context,
        success: false,
        action_type: 'optimize',
        target: context.filePath,
        result: { error: errorMessage }
      });

      throw error;
    }
  }

  async chat(message: string, context?: any): Promise<string> {
    const startTime = Date.now();
    
    try {
      // Get relevant conversation context
      const relevantContext = await this.memoryManager.getRelevantContext(message);

      // Build context-aware prompt
      const contextPrompt = this.buildContextualPrompt(message, relevantContext, context);

      const response = await this.ollama.chat([
        {
          role: 'system',
          content: 'You are Zeta AI, an intelligent coding assistant. Provide helpful, accurate, and contextual responses about software development.'
        },
        {
          role: 'user',
          content: contextPrompt
        }
      ]);

      const responseText = response.message.content;

      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'chat',
        user_input: message,
        agent_response: responseText,
        context: context || {},
        success: true,
        action_type: 'chat',
        target: 'conversation',
        result: { response: responseText }
      });

      this.log('info', `Chat response generated in ${Date.now() - startTime}ms`);
      return responseText;

    } catch (error) {
      this.log('error', `Chat failed: ${error}`);
      throw error;
    }
  }

  async planAction(request: string, context?: any): Promise<ActionPlan> {
    try {
      const plan = await this.actionPlanner.createPlan(request, context);
      
      // Validate the plan
      const validation = await this.actionPlanner.validatePlan(plan);
      if (!validation.valid) {
        this.log('warn', `Generated plan has issues: ${validation.issues.join(', ')}`);
      }

      await this.recordInteraction({
        id: this.generateId(),
        timestamp: new Date(),
        type: 'chat',
        user_input: `Plan action: ${request}`,
        agent_response: JSON.stringify(plan),
        context: context || {},
        success: validation.valid,
        action_type: 'generate',
        target: 'action_plan',
        result: plan
      });

      return plan;

    } catch (error) {
      this.log('error', `Action planning failed: ${error}`);
      throw error;
    }
  }

  async getMemoryStats(): Promise<any> {
    const history = await this.memoryManager.getInteractionHistory(100);
    const successRate = history.length > 0 ? 
      history.filter(i => i.success).length / history.length : 0;

    return {
      total_interactions: history.length,
      success_rate: successRate,
      recent_activity: history.slice(-10),
      memory_usage: 'Memory stats would be calculated here'
    };
  }

  async exportMemory(): Promise<any> {
    return this.memoryManager.exportMemory();
  }

  async importMemory(data: any): Promise<void> {
    return this.memoryManager.importMemory(data);
  }

  private validateCodeInput(code: string): void {
    if (!code || typeof code !== 'string') {
      throw new Error('Code input must be a non-empty string');
    }

    if (code.length > this.config.security_policy.max_code_size) {
      throw new Error(`Code exceeds maximum size of ${this.config.security_policy.max_code_size} characters`);
    }

    // Check for blocked patterns
    for (const pattern of this.config.security_policy.blocked_patterns) {
      if (pattern.test(code)) {
        throw new Error(`Code contains blocked pattern: ${pattern}`);
      }
    }
  }

  private buildContextualPrompt(message: string, relevantContext: any, context?: any): string {
    let prompt = message;

    if (relevantContext.items.length > 0) {
      prompt += '\n\nRelevant context from previous interactions:\n';
      relevantContext.items.slice(0, 3).forEach((item: any, index: number) => {
        prompt += `${index + 1}. ${item.content.substring(0, 200)}...\n`;
      });
    }

    if (relevantContext.suggestions.length > 0) {
      prompt += '\nSuggestions:\n';
      relevantContext.suggestions.forEach((suggestion: string, index: number) => {
        prompt += `- ${suggestion}\n`;
      });
    }

    if (context) {
      prompt += `\nCurrent context: ${JSON.stringify(context, null, 2)}`;
    }

    return prompt;
  }

  private async recordInteraction(interaction: AgentInteraction): Promise<void> {
    try {
      await this.memoryManager.updateMemory(interaction);
    } catch (error) {
      this.log('error', `Failed to record interaction: ${error}`);
    }
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private log(level: string, message: string): void {
    const timestamp = new Date().toISOString();
    const logLevels = ['debug', 'info', 'warn', 'error'];
    const currentLevelIndex = logLevels.indexOf(this.config.log_level);
    const messageLevelIndex = logLevels.indexOf(level);

    if (messageLevelIndex >= currentLevelIndex) {
      console[level === 'error' || level === 'warn' ? level : 'log'](`[${timestamp}] [${level.toUpperCase()}] ${message}`);
    }
  }

  // Configuration methods
  updateConfig(config: Partial<AgentConfig>): void {
    this.config = { ...this.config, ...config };
    
    if (config.ollama_url || config.default_model) {
      this.ollama = new OllamaClient({
        baseUrl: this.config.ollama_url,
        defaultModel: this.config.default_model
      });
    }
  }

  getConfig(): AgentConfig {
    return { ...this.config };
  }
}
