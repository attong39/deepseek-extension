import { OllamaClient } from '../../ollama/client';
import { ChatMessage } from '../../ollama/types';
import {
import AI from "AI";
import Action from "Action";
import ActionPlanner from "./ActionPlanner";
import Address from "Address";
import Adjust from "Adjust";
import Always from "Always";
import Analyze from "Analyze";
import Assess from "Assess";
import Available from "Available";
import Basic from "Basic";
import Break from "Break";
import Check from "Check";
import Clear from "Clear";
import Code from "Code";
import CodeAnalyzer from "CodeAnalyzer";
import Complexity from "Complexity";
import Confidence from "Confidence";
import Consider from "Consider";
import Context from "../../../../../desktop/src/Context/index";
import Create from "Create";
import Current from "Current";
import Dependencies from "Dependencies";
import Ensure from "Ensure";
import Error from "Error";
import Estimated from "Estimated";
import Failed from "Failed";
import Feedback from "Feedback";
import File from "File";
import Files from "Files";
import Format from "Format";
import Framework from "Framework";
import Guidelines from "Guidelines";
import If from "If";
import Improve from "Improve";
import Include from "Include";
import Instructions from "Instructions";
import Language from "Language";
import Maintain from "Maintain";
import No from "No";
import Placeholder from "Placeholder";
import Plan from "Plan";
import Potential from "Potential";
import Programming from "Programming";
import Project from "Project";
import Provide from "Provide";
import Recent from "Recent";
import Refine from "Refine";
import Remove from "Remove";
import Request from "Request";
import Required from "Required";
import Respond from "Respond";
import Response from "Response";
import S from "S";
import Step from "Step";
import Testing from "Testing";
import This from "This";
import Tool from "Tool";
import Type from "Type";
import Unknown from "Unknown";
import Update from "Update";
import User from "User";
import Validate from "Validate";
import Validation from "Validation";
import What from "What";
import Would from "Would";
import You from "You";
  ActionStep,
  ActionPlan
} from '../../../types/shared';

export class ActionPlanner {
  private ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async createPlan(userRequest: string, context?: any): Promise<ActionPlan> {
    const prompt = this.buildPlanningPrompt(userRequest, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: `You are an AI action planner for software development tasks. 
                 Break down complex requests into executable steps with clear dependencies and outcomes.
                 Always respond in JSON format only.`
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    try {
      const response = await this.ollama.chat(messages, {
        model: 'deepseek-coder',
        temperature: 0.3,
        format: 'json'
      });

      return this.parseActionPlan(response.message.content);
    } catch (error) {
      throw new Error(`Action planning failed: ${error}`);
    }
  }

  async validatePlan(plan: ActionPlan): Promise<{ valid: boolean; issues: string[] }> {
    const issues: string[] = [];

    // Check if plan has steps
    if (!plan.steps || plan.steps.length === 0) {
      issues.push('Plan must contain at least one step');
    }

    // Check step dependencies
    const stepTypes = plan.steps.map(step => step.type);
    for (const step of plan.steps) {
      if (step.dependencies) {
        for (const dependency of step.dependencies) {
          if (!stepTypes.includes(dependency as any)) {
            issues.push(`Step "${step.description}" has unresolved dependency: ${dependency}`);
          }
        }
      }
    }

    // Check estimated time is reasonable
    if (plan.estimated_time <= 0) {
      issues.push('Estimated time must be positive');
    }

    // Check confidence level
    if (plan.confidence < 0 || plan.confidence > 100) {
      issues.push('Confidence must be between 0 and 100');
    }

    return {
      valid: issues.length === 0,
      issues
    };
  }

  async refinePlan(plan: ActionPlan, feedback: string): Promise<ActionPlan> {
    const prompt = this.buildRefinementPrompt(plan, feedback);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are refining an action plan based on user feedback. Improve the plan while maintaining its core structure. Respond in JSON format only.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    try {
      const response = await this.ollama.chat(messages, {
        model: 'deepseek-coder',
        temperature: 0.2,
        format: 'json'
      });

      return this.parseActionPlan(response.message.content);
    } catch (error) {
      throw new Error(`Plan refinement failed: ${error}`);
    }
  }

  async executeStep(step: ActionStep, context?: any): Promise<{ success: boolean; result: any; nextStep?: ActionStep }> {
    // This is a placeholder - actual execution would depend on the step type
    switch (step.type) {
    case 'code_analysis':
      return this.executeCodeAnalysis(step, context);
    case 'file_operation':
      return this.executeFileOperation(step, context);
    case 'tool_use':
      return this.executeToolUse(step, context);
    case 'user_query':
      return this.executeUserQuery(step, context);
    case 'validation':
      return this.executeValidation(step, context);
    default:
      return {
        success: false,
        result: { error: `Unknown step type: ${step.type}` }
      };
    }
  }

  async estimateComplexity(userRequest: string): Promise<{ complexity: 'low' | 'medium' | 'high'; reasoning: string }> {
    const prompt = `
Analyze the complexity of this software development request:

Request: "${userRequest}"

Consider:
1. Number of files that might need to be modified
2. Complexity of the logic required
3. Dependencies and integrations
4. Testing requirements
5. Potential risks and edge cases

Respond in JSON format:
{
  "complexity": "low|medium|high",
  "reasoning": "explanation of complexity assessment"
}
`;

    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are a software complexity analyzer. Assess development task complexity accurately.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    try {
      const response = await this.ollama.chat(messages, {
        model: 'deepseek-coder',
        temperature: 0.3,
        format: 'json'
      });

      const parsed = JSON.parse(this.cleanJsonResponse(response.message.content));
      return {
        complexity: parsed.complexity || 'medium',
        reasoning: parsed.reasoning || 'No reasoning provided'
      };
    } catch (error) {
      console.warn('Failed to analyze complexity:', error);
      return {
        complexity: 'medium',
        reasoning: 'Failed to analyze complexity due to parsing error'
      };
    }
  }

  private buildPlanningPrompt(userRequest: string, context?: any): string {
    const contextInfo = this.formatContext(context);

    return `
Create a detailed action plan for this software development request:

**User Request:** ${userRequest}

**Available Context:**
${contextInfo}

**Required JSON Response Format:**
{
  "goal": "Clear description of what needs to be accomplished",
  "steps": [
    {
      "type": "code_analysis|file_operation|tool_use|user_query|validation",
      "description": "Clear description of what this step does",
      "parameters": {
        "key": "value pairs for step execution"
      },
      "expected_outcome": "What should happen after this step",
      "dependencies": ["list of prerequisite step types"],
      "estimated_duration": 15
    }
  ],
  "estimated_time": 120,
  "confidence": 85,
  "prerequisites": ["things needed before starting"],
  "risks": ["potential problems or challenges"],
  "success_criteria": ["how to know when the goal is achieved"]
}

**Guidelines:**
1. Break complex tasks into manageable steps
2. Ensure logical step ordering
3. Include validation steps for critical operations
4. Consider error handling and rollback scenarios
5. Provide realistic time estimates (in minutes)
6. Include necessary context gathering steps
`;
  }

  private buildRefinementPrompt(plan: ActionPlan, feedback: string): string {
    return `
Refine this action plan based on the provided feedback:

**Current Plan:**
${JSON.stringify(plan, null, 2)}

**User Feedback:**
${feedback}

**Instructions:**
1. Address the specific feedback provided
2. Maintain the overall goal and structure
3. Improve step clarity and ordering
4. Adjust time estimates if needed
5. Update risk assessment if necessary

Respond with the improved plan in the same JSON format.
`;
  }

  private formatContext(context?: any): string {
    if (!context) return 'No specific context provided';

    let formatted = '';

    if (context.language) {
      formatted += `- Programming Language: ${context.language}\n`;
    }

    if (context.framework) {
      formatted += `- Framework: ${context.framework}\n`;
    }

    if (context.projectType) {
      formatted += `- Project Type: ${context.projectType}\n`;
    }

    if (context.dependencies && context.dependencies.length > 0) {
      formatted += `- Dependencies: ${context.dependencies.join(', ')}\n`;
    }

    if (context.recentFiles && context.recentFiles.length > 0) {
      formatted += `- Recent Files: ${context.recentFiles.join(', ')}\n`;
    }

    if (context.filePath) {
      formatted += `- Current File: ${context.filePath}\n`;
    }

    return formatted || 'Basic context available';
  }

  private parseActionPlan(response: string): ActionPlan {
    try {
      const cleanResponse = this.cleanJsonResponse(response);
      const parsed = JSON.parse(cleanResponse);

      // Validate and set defaults
      return {
        goal: parsed.goal || 'No goal specified',
        steps: parsed.steps || [],
        estimated_time: parsed.estimated_time || 0,
        confidence: parsed.confidence || 0,
        prerequisites: parsed.prerequisites || [],
        risks: parsed.risks || [],
        success_criteria: parsed.success_criteria || []
      };
    } catch (error) {
      throw new Error(`Failed to parse action plan: ${error}`);
    }
  }

  private cleanJsonResponse(response: string): string {
    // Remove markdown code blocks if present
    let cleaned = response.replace(/```json\n?|\n?```/g, '');
    
    // Remove any leading/trailing whitespace
    cleaned = cleaned.trim();
    
    // If response doesn't start with {, try to find the JSON part
    if (!cleaned.startsWith('{')) {
      const jsonMatch = cleaned.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        cleaned = jsonMatch[0];
      }
    }
    
    return cleaned;
  }

  // Placeholder execution methods - these would be implemented based on actual capabilities
  private async executeCodeAnalysis(step: ActionStep, context?: any): Promise<{ success: boolean; result: any }> {
    // Would integrate with CodeAnalyzer
    return {
      success: true,
      result: { analysis: 'Code analysis completed', step: step.description }
    };
  }

  private async executeFileOperation(step: ActionStep, context?: any): Promise<{ success: boolean; result: any }> {
    // Would integrate with file system operations
    return {
      success: true,
      result: { operation: 'File operation completed', step: step.description }
    };
  }

  private async executeToolUse(step: ActionStep, context?: any): Promise<{ success: boolean; result: any }> {
    // Would integrate with various development tools
    return {
      success: true,
      result: { tool: 'Tool executed', step: step.description }
    };
  }

  private async executeUserQuery(step: ActionStep, context?: any): Promise<{ success: boolean; result: any }> {
    // Would prompt user for additional information
    return {
      success: true,
      result: { query: 'User query handled', step: step.description }
    };
  }

  private async executeValidation(step: ActionStep, context?: any): Promise<{ success: boolean; result: any }> {
    // Would validate current state or results
    return {
      success: true,
      result: { validation: 'Validation completed', step: step.description }
    };
  }
}
