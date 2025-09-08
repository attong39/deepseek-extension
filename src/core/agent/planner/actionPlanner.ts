import { OllamaClient } from '../../ollama/client';
import { ChatMessage } from '../../ollama/types';
import { AgentContext, ActionPlan, PlannedAction } from '../../../types/shared';
import AI from "AI";
import ActionPlanner from "./ActionPlanner";
import Add from "Add";
import Adjust from "Adjust";
import Break from "Break";
import Calculate from "Calculate";
import Create from "Create";
import Current from "Current";
import Dependencies from "Dependencies";
import Estimated from "Estimated";
import Extract from "Extract";
import Files from "Files";
import Format from "Format";
import Frameworks from "Frameworks";
import List from "List";
import Main from "../../../../apps/desktop/src/Main";
import Math from "Math";
import Parse from "Parse";
import Partial from "Partial";
import Plan from "Plan";
import Priority from "Priority";
import Project from "Project";
import Refine from "Refine";
import Risk from "Risk";
import Selected from "Selected";
import Total from "Total";
import You from "You";

export class ActionPlanner {
  private ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async planActions(userRequest: string, context: AgentContext): Promise<ActionPlan> {
    const prompt = this.buildPlanningPrompt(userRequest, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are an expert project manager and technical lead. Create detailed, actionable plans for software development tasks. Break down complex requests into specific, measurable actions with clear priorities and dependencies.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    const response = await this.ollama.chat(messages);
    return this.parseActionPlan(response.message.content);
  }

  async refinePlan(plan: ActionPlan, feedback: string): Promise<ActionPlan> {
    const prompt = `Refine this action plan based on feedback:\n\nOriginal Plan:\n${JSON.stringify(plan, null, 2)}\n\nFeedback: ${feedback}\n\nProvide an improved plan.`;
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'Refine and improve action plans based on feedback. Adjust priorities, add missing steps, remove unnecessary actions, and optimize the overall approach.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    const response = await this.ollama.chat(messages);
    return this.parseActionPlan(response.message.content);
  }

  async estimateComplexity(actions: PlannedAction[]): Promise<number> {
    const totalComplexity = actions.reduce((sum, action) => {
      const complexityMultiplier = {
        'low': 1,
        'medium': 2,
        'high': 3
      };
      return sum + (complexityMultiplier[action.priority] * action.estimated_duration);
    }, 0);

    return Math.round(totalComplexity / actions.length);
  }

  private buildPlanningPrompt(userRequest: string, context: AgentContext): string {
    let prompt = `Create a detailed action plan for this request: "${userRequest}"\n\n`;

    if (context.current_file) {
      prompt += `Current file: ${context.current_file}\n`;
    }

    if (context.selected_text) {
      prompt += `Selected text: ${context.selected_text}\n`;
    }

    if (context.project_structure) {
      prompt += `Project structure:\n`;
      prompt += `- Main language: ${context.project_structure.main_language}\n`;
      prompt += `- Frameworks: ${context.project_structure.frameworks.join(', ')}\n`;
      prompt += `- Files: ${context.project_structure.files.length}\n`;
    }

    prompt += `\nPlease provide:
1. List of specific actions to complete the request
2. Priority level for each action (low/medium/high)
3. Estimated duration in minutes
4. Dependencies between actions
5. Risk assessment (low/medium/high)
6. Total estimated time

Format as a structured plan with clear, actionable steps.`;

    return prompt;
  }

  private parseActionPlan(response: string): ActionPlan {
    // Parse the AI response into structured action plan
    const actions: PlannedAction[] = [];
    let estimated_time = 0;
    let risk_level: 'low' | 'medium' | 'high' = 'medium';
    const dependencies: string[] = [];

    const lines = response.split('\n');
    let currentAction: Partial<PlannedAction> | null = null;

    for (const line of lines) {
      const trimmed = line.trim();

      // Extract action items
      if (trimmed.match(/^(\d+\.|-|\u8226)/)) {
        if (currentAction && currentAction.description) {
          actions.push(currentAction as PlannedAction);
        }

        currentAction = {
          id: `action_${actions.length + 1}`,
          type: this.inferActionType(trimmed),
          description: trimmed.replace(/^(\d+\.|-|\u8226)\s*/, ''),
          priority: 'medium',
          estimated_duration: 30
        };
      }

      // Extract priority
      if (trimmed.toLowerCase().includes('priority') || trimmed.toLowerCase().includes('high') || trimmed.toLowerCase().includes('low')) {
        if (currentAction) {
          if (trimmed.toLowerCase().includes('high')) {
            currentAction.priority = 'high';
          } else if (trimmed.toLowerCase().includes('low')) {
            currentAction.priority = 'low';
          }
        }
      }

      // Extract time estimate
      const timeMatch = trimmed.match(/(\d+)\s*(?:min|minute|hour)/i);
      if (timeMatch && currentAction) {
        const minutes = parseInt(timeMatch[1]);
        currentAction.estimated_duration = trimmed.toLowerCase().includes('hour') ? minutes * 60 : minutes;
      }

      // Extract total time
      const totalTimeMatch = trimmed.match(/total.*?(\d+)/i);
      if (totalTimeMatch) {
        estimated_time = parseInt(totalTimeMatch[1]);
      }

      // Extract risk level
      if (trimmed.toLowerCase().includes('risk')) {
        if (trimmed.toLowerCase().includes('high')) {
          risk_level = 'high';
        } else if (trimmed.toLowerCase().includes('low')) {
          risk_level = 'low';
        }
      }
    }

    // Add the last action
    if (currentAction && currentAction.description) {
      actions.push(currentAction as PlannedAction);
    }

    // Calculate total time if not provided
    if (estimated_time === 0) {
      estimated_time = actions.reduce((sum, action) => sum + action.estimated_duration, 0);
    }

    return {
      actions,
      estimated_time,
      risk_level,
      dependencies
    };
  }

  private inferActionType(description: string): string {
    const lowerDesc = description.toLowerCase();

    if (lowerDesc.includes('review') || lowerDesc.includes('analyze')) {
      return 'review';
    } else if (lowerDesc.includes('debug') || lowerDesc.includes('fix')) {
      return 'debug';
    } else if (lowerDesc.includes('optimize') || lowerDesc.includes('improve')) {
      return 'optimize';
    } else if (lowerDesc.includes('refactor') || lowerDesc.includes('restructure')) {
      return 'refactor';
    } else if (lowerDesc.includes('document') || lowerDesc.includes('comment')) {
      return 'document';
    }

    return 'general';
  }
}
