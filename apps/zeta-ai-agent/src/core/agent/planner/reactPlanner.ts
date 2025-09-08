/**
 * ReAct (Reasoning + Acting) Planner
 * Implements systematic thought-action-observation cycles for autonomous execution
 * 
 * Based on ReAct paper: https://arxiv.org/abs/2210.03629
 * Integrates with Chain-of-Thought reasoner for advanced planning
 */

import { ToolExecutor } from './toolExecutor';
import A from "A";
import AI from "AI";
import Abort from "Abort";
import Acting from "Acting";
import Action from "Action";
import Adapt from "Adapt";
import Add from "Add";
import Additional from "Additional";
import Available from "Available";
import Base from "Base";
import Based from "Based";
import Begin from "Begin";
import Break from "Break";
import COMPLETED from "COMPLETED";
import CRITICAL from "CRITICAL";
import Calculate from "Calculate";
import Chain from "Chain";
import Check from "Check";
import Command from "Command";
import Commit from "Commit";
import Complex from "Complex";
import Create from "Create";
import Current from "Current";
import DOCKER from "DOCKER";
import Delegate from "Delegate";
import Directory from "Directory";
import EXECUTING from "EXECUTING";
import Error from "Error";
import Execute from "Execute";
import Execution from "Execution";
import FAILED from "FAILED";
import FILE from "FILE";
import FINAL_ANSWER from "FINAL_ANSWER";
import Failed from "Failed";
import File from "File";
import Files from "Files";
import For from "For";
import Format from "Format";
import GIT from "GIT";
import Generate from "Generate";
import Get from "Get";
import HIGH from "HIGH";
import Higher from "Higher";
import ID from "ID";
import If from "If";
import Implements from "Implements";
import Initialize from "Initialize";
import Instructions from "Instructions";
import Integrates from "Integrates";
import LLM from "LLM";
import Length from "Length";
import Limit from "Limit";
import List from "List";
import MODERATE from "MODERATE";
import Main from "../../../../../desktop/src/Main";
import Map from "Map";
import Math from "Math";
import Medium from "Medium";
import Model from "Model";
import Multi from "Multi";
import N from "N";
import NETWORK from "NETWORK";
import NO_CHANGE from "NO_CHANGE";
import Never from "Never";
import Next from "Next";
import OBSERVATION from "OBSERVATION";
import Observation from "Observation";
import OllamaClient from "OllamaClient";
import Original from "Original";
import PAUSED from "PAUSED";
import PLANNING from "PLANNING";
import Parse from "Parse";
import Pause from "Pause";
import Phase from "Phase";
import Planner from "Planner";
import Planning from "Planning";
import Preserve from "Preserve";
import Previous from "Previous";
import Provide from "Provide";
import Query from "Query";
import REASONING from "REASONING";
import ReAct from "ReAct";
import ReActPlan from "ReActPlan";
import ReActPlanner from "./ReActPlanner";
import ReActStep from "ReActStep";
import Read from "Read";
import Reasoning from "Reasoning";
import Record from "Record";
import Remove from "Remove";
import Resume from "Resume";
import SAFE from "SAFE";
import SHELL from "SHELL";
import SYSTEM from "SYSTEM";
import Safety from "Safety";
import Select from "Select";
import Selected from "Selected";
import Should from "Should";
import Simple from "Simple";
import Step from "Step";
import Summary from "Summary";
import TOOL_CALL from "TOOL_CALL";
import Task from "Task";
import Temporary from "Temporary";
import The from "The";
import Think from "Think";
import Thought from "Thought";
import Tool from "Tool";
import ToolDefinition from "ToolDefinition";
import ToolExecutionResult from "ToolExecutionResult";
import Tools from "Tools";
import Updated from "Updated";
import Use from "Use";
import Vietnamese from "Vietnamese";
import Write from "Write";
import X from "X";
import You from "You";
import Your from "Your";

// Temporary interface until OllamaClient is available
interface OllamaClient {
  generateCompletion(params: {
    prompt: string;
    model: string;
    options: {
      temperature?: number;
      max_tokens?: number;
    };
  }): Promise<{ content: string }>;
}

export interface ReActStep {
  stepNumber: number;
  thought: string;
  action: string;
  actionType: 'TOOL_CALL' | 'REASONING' | 'OBSERVATION' | 'FINAL_ANSWER';
  toolName?: string;
  toolArgs?: Record<string, any>;
  observation?: string;
  confidence: number;
  timestamp: Date;
}

export interface ReActPlan {
  planId: string;
  query: string;
  steps: ReActStep[];
  currentStep: number;
  status: 'PLANNING' | 'EXECUTING' | 'COMPLETED' | 'FAILED' | 'PAUSED';
  finalAnswer?: string;
  confidence: number;
  startTime: Date;
  endTime?: Date;
  metadata: {
    totalSteps: number;
    successfulSteps: number;
    failedSteps: number;
    toolsUsed: string[];
  };
}

export interface ToolDefinition {
  name: string;
  description: string;
  parameters: Record<string, {
    type: string;
    description: string;
    required?: boolean;
    enum?: string[];
  }>;
  dangerLevel: 'SAFE' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  category: 'GIT' | 'SHELL' | 'DOCKER' | 'FILE' | 'NETWORK' | 'AI' | 'SYSTEM';
}

export interface ToolExecutionResult {
  success: boolean;
  output: string;
  error?: string;
  executionTime: number;
  metadata?: Record<string, any>;
}

export class ReActPlanner {
  private readonly ollamaClient: OllamaClient;
  private readonly toolExecutor: ToolExecutor;
  private readonly availableTools: Map<string, ToolDefinition> = new Map();
  private readonly activePlans: Map<string, ReActPlan> = new Map();
  private maxSteps = 10;
  private readonly safetyChecksEnabled: boolean = true;

  // Model selection configuration
  private readonly config = {
    defaultModel: 'starcoder',
    highQualityModel: 'attong39/zeta', 
    heavyModel: 'codellama:13b-instruct',
    complexityThreshold: 0.6,
    enableTurbo: true
  };

  constructor(ollamaClient: OllamaClient, toolExecutor?: ToolExecutor) {
    this.ollamaClient = ollamaClient;
    this.toolExecutor = toolExecutor || new ToolExecutor();
    this.initializeDefaultTools();
  }

  /**
   * Select appropriate model based on task complexity
   */
  private selectModel(taskComplexity = 0.5, taskType: 'planning' | 'reasoning' | 'coding' = 'planning'): string {
    // Simple tasks use default fast model
    if (taskComplexity < 0.3) {
      return this.config.defaultModel;
    }
    
    // Medium complexity tasks use high-quality Vietnamese model
    if (taskComplexity < this.config.complexityThreshold) {
      return this.config.highQualityModel;
    }
    
    // Complex tasks use heavy model
    return this.config.heavyModel;
  }

  /**
   * Calculate task complexity based on query characteristics
   */
  private calculateTaskComplexity(query: string): number {
    let complexity = 0.3; // Base complexity
    
    // Vietnamese language detection increases complexity (use specialized model)
    const vietnameseChars = /[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]/;
    if (vietnameseChars.test(query)) {
      complexity += 0.3;
    }
    
    // Complex programming tasks
    const programmingKeywords = ['algorithm', 'optimization', 'architecture', 'design pattern', 'thuật toán', 'tối ưu'];
    const hasComplexProgramming = programmingKeywords.some(keyword => 
      query.toLowerCase().includes(keyword)
    );
    if (hasComplexProgramming) {
      complexity += 0.2;
    }
    
    // Multi-step or reasoning tasks
    const reasoningIndicators = ['analyze', 'compare', 'evaluate', 'design', 'phân tích', 'so sánh', 'đánh giá'];
    const hasReasoning = reasoningIndicators.some(indicator => 
      query.toLowerCase().includes(indicator)
    );
    if (hasReasoning) {
      complexity += 0.2;
    }
    
    // Length-based complexity
    if (query.length > 200) {
      complexity += 0.1;
    }
    
    return Math.min(complexity, 1.0);
  }

  /**
   * Main entry point: Create và execute ReAct plan
   */
  async createAndExecutePlan(
    query: string,
    options?: {
      maxSteps?: number;
      enableSafetyChecks?: boolean;
      allowedToolCategories?: string[];
    }
  ): Promise<ReActPlan> {
    const planId = this.generatePlanId();
    const plan: ReActPlan = {
      planId,
      query,
      steps: [],
      currentStep: 0,
      status: 'PLANNING',
      confidence: 0,
      startTime: new Date(),
      metadata: {
        totalSteps: 0,
        successfulSteps: 0,
        failedSteps: 0,
        toolsUsed: []
      }
    };

    this.activePlans.set(planId, plan);

    try {
      // Phase 1: Planning
      await this.generateInitialPlan(plan, options);
      
      // Phase 2: Execution
      plan.status = 'EXECUTING';
      await this.executePlan(plan);
      
      plan.status = 'COMPLETED';
      plan.endTime = new Date();
      
    } catch (error) {
      plan.status = 'FAILED';
      plan.endTime = new Date();
      console.error(`ReAct plan ${planId} failed:`, error);
    }

    return plan;
  }

  /**
   * Generate initial planning using ReAct prompting
   */
  private async generateInitialPlan(
    plan: ReActPlan,
    options?: { maxSteps?: number; allowedToolCategories?: string[] }
  ): Promise<void> {
    this.maxSteps = options?.maxSteps || 10;
    
    const availableToolsDesc = this.getAvailableToolsDescription(options?.allowedToolCategories);
    
    // Calculate task complexity and select appropriate model
    const taskComplexity = this.calculateTaskComplexity(plan.query);
    const selectedModel = this.selectModel(taskComplexity, 'planning');
    
    console.log(`[ReActPlanner] Task complexity: ${taskComplexity.toFixed(2)}, Selected model: ${selectedModel}`);
    
    const planningPrompt = `
You are an intelligent AI agent using ReAct (Reasoning + Acting) methodology.
Your task: ${plan.query}

Available Tools:
${availableToolsDesc}

Instructions:
1. Break down the task into logical steps
2. For each step, follow the pattern: Thought -> Action -> Observation
3. Use tools when needed to gather information or take actions
4. Think step by step and be precise
5. Limit to ${this.maxSteps} steps maximum
6. Provide Vietnamese comments when applicable

Format your response as:
Step X:
Thought: [Your reasoning about what to do next]
Action: [The action to take - either use a tool or provide reasoning]
Tool: [If using a tool, specify: tool_name(param1=value1, param2=value2)]

Begin planning:
    `.trim();

    const response = await this.ollamaClient.generateCompletion({
      prompt: planningPrompt,
      model: selectedModel,
      options: {
        temperature: taskComplexity > 0.7 ? 0.3 : 0.1, // Higher temp for complex tasks
        max_tokens: 2000
      }
    });

    // Parse the planning response into steps
    const steps = this.parsePlanningResponse(response.content);
    plan.steps = steps;
    plan.metadata.totalSteps = steps.length;
  }

  /**
   * Execute the planned steps
   */
  private async executePlan(plan: ReActPlan): Promise<void> {
    for (let i = 0; i < plan.steps.length && i < this.maxSteps; i++) {
      const success = await this.executeStep(plan, i);
      
      if (!success && this.shouldAbortPlan(plan, new Error('Step execution failed'))) {
        break;
      }

      // Generate next step if needed
      if (i < plan.steps.length - 1) {
        await this.adaptNextStep(plan, i);
      }
    }

    // Generate final answer
    plan.finalAnswer = await this.generateFinalAnswer(plan);
    plan.confidence = this.calculatePlanConfidence(plan);
  }

  /**
   * Execute individual step
   */
  private async executeStep(plan: ReActPlan, stepIndex: number): Promise<boolean> {
    const step = plan.steps[stepIndex];
    plan.currentStep = stepIndex;

    try {
      if (step.actionType === 'TOOL_CALL' && step.toolName) {
        return await this.executeToolStep(step, plan);
      } else if (step.actionType === 'REASONING') {
        return this.executeReasoningStep(step, plan);
      }
      return true;
    } catch (error) {
      step.observation = `Execution error: ${error}`;
      plan.metadata.failedSteps++;
      return false;
    }
  }

  /**
   * Execute tool-based step
   */
  private async executeToolStep(step: ReActStep, plan: ReActPlan): Promise<boolean> {
    if (!step.toolName) return false;

    const result = await this.executeToolCall(step.toolName, step.toolArgs || {});
    
    if (result.success) {
      step.observation = result.output;
      plan.metadata.successfulSteps++;
      plan.metadata.toolsUsed.push(step.toolName);
      return true;
    } else {
      step.observation = `Error: ${result.error}`;
      plan.metadata.failedSteps++;
      return false;
    }
  }

  /**
   * Execute reasoning step
   */
  private executeReasoningStep(step: ReActStep, plan: ReActPlan): boolean {
    step.observation = 'Reasoning completed';
    plan.metadata.successfulSteps++;
    return true;
  }

  /**
   * Parse LLM response thành ReAct steps
   */
  private parsePlanningResponse(response: string): ReActStep[] {
    const steps: ReActStep[] = [];
    const stepSections = response.split(/(?=Step\s+\d+:)/);
    
    for (const section of stepSections) {
      if (!section.trim()) continue;
      
      const step = this.parseStepSection(section);
      if (step) {
        steps.push(step);
      }
    }

    return steps;
  }

  /**
   * Parse individual step section
   */
  private parseStepSection(section: string): ReActStep | null {
    const stepMatch = /Step\s+(\d+):/.exec(section);
    if (!stepMatch) return null;
    
    const stepNumber = parseInt(stepMatch[1]);
    const thoughtMatch = /Thought:\s*(.*?)(?=Action:|$)/s.exec(section);
    const actionMatch = /Action:\s*(.*?)(?=Tool:|$)/s.exec(section);
    
    if (!thoughtMatch || !actionMatch) return null;

    const { actionType, toolName, toolArgs } = this.parseToolInformation(section);

    return {
      stepNumber,
      thought: thoughtMatch[1].trim(),
      action: actionMatch[1].trim(),
      actionType,
      toolName,
      toolArgs,
      confidence: 0.8,
      timestamp: new Date()
    };
  }

  /**
   * Parse tool information from step section
   */
  private parseToolInformation(section: string): {
    actionType: ReActStep['actionType'];
    toolName?: string;
    toolArgs?: Record<string, any>;
  } {
    const toolMatch = /Tool:\s*(.*?)$/s.exec(section);
    
    if (!toolMatch) {
      return { actionType: 'REASONING' };
    }

    const toolCall = toolMatch[1].trim();
    const toolCallMatch = /(\w+)\((.*?)\)/.exec(toolCall);
    
    if (!toolCallMatch) {
      return { actionType: 'REASONING' };
    }

    const toolName = toolCallMatch[1];
    let toolArgs: Record<string, any> | undefined;

    try {
      const argsStr = toolCallMatch[2];
      toolArgs = this.parseToolArguments(argsStr);
    } catch (error) {
      console.warn(`Failed to parse tool arguments for ${toolName}: ${toolCall}`, error);
      toolArgs = { rawArgs: toolCall };
    }

    return {
      actionType: 'TOOL_CALL',
      toolName,
      toolArgs
    };
  }

  /**
   * Parse tool arguments từ string format
   */
  private parseToolArguments(argsStr: string): Record<string, any> {
    const args: Record<string, any> = {};
    
    // Simple parsing for key=value pairs
    const argPairs = argsStr.split(',').map(pair => pair.trim());
    
    for (const pair of argPairs) {
      const [key, ...valueParts] = pair.split('=');
      if (key && valueParts.length > 0) {
        const value = valueParts.join('=').trim();
        
        // Remove quotes if present - simplified approach
        const cleanValue = value.startsWith('"') || value.startsWith('\'') 
          ? value.slice(1, -1) 
          : value;
        args[key.trim()] = cleanValue;
      }
    }

    return args;
  }

  /**
   * Execute tool call với safety checks
   */
  private async executeToolCall(
    toolName: string,
    args: Record<string, any>
  ): Promise<ToolExecutionResult> {
    const tool = this.availableTools.get(toolName);
    
    if (!tool) {
      return {
        success: false,
        error: `Tool '${toolName}' not found`,
        output: '',
        executionTime: 0
      };
    }

    // Safety checks
    if (this.safetyChecksEnabled && !this.isToolExecutionSafe(tool, args)) {
      return {
        success: false,
        error: `Tool execution blocked by safety policy`,
        output: '',
        executionTime: 0
      };
    }

    const startTime = Date.now();

    try {
      // Delegate to specific tool executor
      const result = await this.delegateToolExecution(toolName, args);
      const executionTime = Date.now() - startTime;

      return {
        success: true,
        output: result,
        executionTime,
        metadata: { tool: toolName, args }
      };

    } catch (error) {
      const executionTime = Date.now() - startTime;
      
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error),
        output: '',
        executionTime
      };
    }
  }

  /**
   * Delegate tool execution to appropriate handler
   */
  private async delegateToolExecution(toolName: string, args: Record<string, any>): Promise<string> {
    const result = await this.executeTool(toolName, args);
    
    if (!result.success) {
      throw new Error(result.error || 'Tool execution failed');
    }
    
    return result.output;
  }

  /**
   * Execute tool using ToolExecutor
   */
  private async executeTool(toolName: string, args: Record<string, any>) {
    switch (toolName) {
    case 'git_status':
      return await this.toolExecutor.executeGitCommand('status', args);
      
    case 'git_commit':
      return await this.toolExecutor.executeGitCommand('commit', args);
      
    case 'git_add':
      return await this.toolExecutor.executeGitCommand('add', args);
      
    case 'shell_command':
      return await this.toolExecutor.executeShellCommand(args.command || '');
      
    case 'read_file':
      return await this.toolExecutor.readFile(args.path || '');
      
    case 'write_file':
      return await this.toolExecutor.writeFile(args.path || '', args.content || '');
      
    case 'list_directory':
      return await this.toolExecutor.listDirectory(args.path || '.');
      
    default:
      return {
        success: false,
        error: `Tool '${toolName}' execution not implemented`,
        output: '',
        executionTime: 0
      };
    }
  }

  /**
   * Safety check for tool execution
   */
  private isToolExecutionSafe(tool: ToolDefinition, args: Record<string, any>): boolean {
    // Check danger level
    if (tool.dangerLevel === 'CRITICAL') {
      return false; // Never allow critical tools in autonomous mode
    }

    // Additional safety checks based on tool type and arguments
    if (tool.category === 'SHELL') {
      const command = args.command || '';
      const dangerousCommands = ['rm -rf', 'del /f', 'format', 'fdisk', 'dd if='];
      
      if (dangerousCommands.some(dangerous => command.includes(dangerous))) {
        return false;
      }
    }

    return true;
  }

  /**
   * Adapt next step based on current observations
   */
  private async adaptNextStep(plan: ReActPlan, currentStepIndex: number): Promise<void> {
    const currentStep = plan.steps[currentStepIndex];
    const nextStep = plan.steps[currentStepIndex + 1];

    if (!nextStep || !currentStep.observation) {
      return;
    }

    // Generate adaptation prompt
    const adaptationPrompt = `
Based on the observation from the previous step, adapt the next action if needed.

Previous Step:
Thought: ${currentStep.thought}
Action: ${currentStep.action}
Observation: ${currentStep.observation}

Current Next Step:
Thought: ${nextStep.thought}
Action: ${nextStep.action}

Should this step be modified based on the observation? If yes, provide the updated step.
If no changes needed, respond with "NO_CHANGE".

Format:
Thought: [Updated thought]
Action: [Updated action]
Tool: [If tool needed: tool_name(args)]
    `.trim();

    const response = await this.ollamaClient.generateCompletion({
      prompt: adaptationPrompt,
      model: this.selectModel(0.4, 'reasoning'), // Medium complexity for adaptation
      options: {
        temperature: 0.2,
        max_tokens: 500
      }
    });

    if (response.content.trim() !== 'NO_CHANGE') {
      // Parse and update the next step
      const updatedSteps = this.parsePlanningResponse(`Step ${nextStep.stepNumber}:\n${response.content}`);
      if (updatedSteps.length > 0) {
        plan.steps[currentStepIndex + 1] = {
          ...nextStep,
          ...updatedSteps[0],
          stepNumber: nextStep.stepNumber // Preserve original step number
        };
      }
    }
  }

  /**
   * Generate final answer từ execution results
   */
  private async generateFinalAnswer(plan: ReActPlan): Promise<string> {
    const executionSummary = plan.steps.map(step => 
      `Step ${step.stepNumber}: ${step.thought}\nAction: ${step.action}\nResult: ${step.observation || 'N/A'}`
    ).join('\n\n');

    const summaryPrompt = `
Based on the ReAct execution below, provide a comprehensive final answer to the original query.

Original Query: ${plan.query}

Execution Summary:
${executionSummary}

Provide a clear, concise final answer that addresses the original query:
    `.trim();

    const response = await this.ollamaClient.generateCompletion({
      prompt: summaryPrompt,
      model: this.selectModel(0.5, 'reasoning'), // Medium complexity for summarization
      options: {
        temperature: 0.1,
        max_tokens: 1000
      }
    });

    return response.content.trim();
  }

  /**
   * Calculate overall plan confidence
   */
  private calculatePlanConfidence(plan: ReActPlan): number {
    const successRate = plan.metadata.totalSteps > 0 
      ? plan.metadata.successfulSteps / plan.metadata.totalSteps 
      : 0;
    
    const stepConfidences = plan.steps.map(step => step.confidence);
    const avgStepConfidence = stepConfidences.length > 0
      ? stepConfidences.reduce((sum, conf) => sum + conf, 0) / stepConfidences.length
      : 0;

    return (successRate + avgStepConfidence) / 2;
  }

  /**
   * Check if plan should be aborted
   */
  private shouldAbortPlan(plan: ReActPlan, error: Error): boolean {
    // Abort if too many consecutive failures
    const recentSteps = plan.steps.slice(-3);
    const recentFailures = recentSteps.filter(step => 
      step.observation?.includes('Error') || step.observation?.includes('error')
    ).length;

    return recentFailures >= 2; // Abort after 2 consecutive failures
  }

  /**
   * Initialize default tools
   */
  private initializeDefaultTools(): void {
    const defaultTools: ToolDefinition[] = [
      {
        name: 'git_status',
        description: 'Get git repository status',
        parameters: {},
        dangerLevel: 'SAFE',
        category: 'GIT'
      },
      {
        name: 'git_add',
        description: 'Add files to git staging area',
        parameters: {
          files: { type: 'array', description: 'Files to add (optional, defaults to all)' }
        },
        dangerLevel: 'SAFE',
        category: 'GIT'
      },
      {
        name: 'git_commit',
        description: 'Commit changes to git repository',
        parameters: {
          message: { type: 'string', description: 'Commit message', required: true },
          all: { type: 'boolean', description: 'Commit all tracked files' }
        },
        dangerLevel: 'MODERATE',
        category: 'GIT'
      },
      {
        name: 'shell_command',
        description: 'Execute shell command',
        parameters: {
          command: { type: 'string', description: 'Command to execute', required: true }
        },
        dangerLevel: 'HIGH',
        category: 'SHELL'
      },
      {
        name: 'read_file',
        description: 'Read file contents',
        parameters: {
          path: { type: 'string', description: 'File path', required: true }
        },
        dangerLevel: 'SAFE',
        category: 'FILE'
      },
      {
        name: 'write_file',
        description: 'Write content to file',
        parameters: {
          path: { type: 'string', description: 'File path', required: true },
          content: { type: 'string', description: 'File content', required: true }
        },
        dangerLevel: 'MODERATE',
        category: 'FILE'
      },
      {
        name: 'list_directory',
        description: 'List directory contents',
        parameters: {
          path: { type: 'string', description: 'Directory path' }
        },
        dangerLevel: 'SAFE',
        category: 'FILE'
      }
    ];

    defaultTools.forEach(tool => {
      this.availableTools.set(tool.name, tool);
    });
  }

  /**
   * Get available tools description for prompting
   */
  private getAvailableToolsDescription(allowedCategories?: string[]): string {
    const tools = Array.from(this.availableTools.values());
    const filteredTools = allowedCategories 
      ? tools.filter(tool => allowedCategories.includes(tool.category))
      : tools;

    return filteredTools.map(tool => {
      const params = Object.entries(tool.parameters)
        .map(([name, config]) => `${name}: ${config.description}`)
        .join(', ');
      
      const description = `- ${tool.name}: ${tool.description}`;
      return params ? `${description} (${params})` : description;
    }).join('\n');
  }

  /**
   * Generate unique plan ID
   */
  private generatePlanId(): string {
    return `react_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  /**
   * Get active plan by ID
   */
  getActivePlan(planId: string): ReActPlan | undefined {
    return this.activePlans.get(planId);
  }

  /**
   * List all active plans
   */
  getActivePlans(): ReActPlan[] {
    return Array.from(this.activePlans.values());
  }

  /**
   * Pause plan execution
   */
  pausePlan(planId: string): boolean {
    const plan = this.activePlans.get(planId);
    if (plan && plan.status === 'EXECUTING') {
      plan.status = 'PAUSED';
      return true;
    }
    return false;
  }

  /**
   * Resume paused plan
   */
  async resumePlan(planId: string): Promise<boolean> {
    const plan = this.activePlans.get(planId);
    if (plan && plan.status === 'PAUSED') {
      plan.status = 'EXECUTING';
      await this.executePlan(plan);
      return true;
    }
    return false;
  }

  /**
   * Add custom tool to available tools
   */
  registerTool(tool: ToolDefinition): void {
    this.availableTools.set(tool.name, tool);
  }

  /**
   * Remove tool from available tools
   */
  unregisterTool(toolName: string): boolean {
    return this.availableTools.delete(toolName);
  }
}
