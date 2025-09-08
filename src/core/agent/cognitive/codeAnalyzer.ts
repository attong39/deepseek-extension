import { OllamaClient } from '../../ollama/client';
import { ChatMessage } from '../../ollama/types';
import {
import AI from "AI";
import Analyze from "Analyze";
import Best from "Best";
import Code from "Code";
import CodeAnalyzer from "./CodeAnalyzer";
import Debug from "Debug";
import Default from "Default";
import Dependencies from "Dependencies";
import Extract from "Extract";
import File from "File";
import Focus from "Focus";
import Format from "Format";
import Framework from "Framework";
import Language from "Language";
import Math from "Math";
import Optimize from "Optimize";
import Overall from "Overall";
import Parse from "Parse";
import Performance from "Performance";
import Placeholder from "Placeholder";
import Please from "Please";
import Potential from "Potential";
import Provide from "Provide";
import S from "S";
import Security from "Security";
import Simple from "Simple";
import Step from "Step";
import Suggestions from "Suggestions";
import You from "You";
  CodeContext,
  CodeReview,
  DebugSolution,
  CodeOptimization,
  CodeIssue,
  CodeSuggestion
} from '../../../types/shared';

export class CodeAnalyzer {
  private ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async reviewCode(code: string, context: CodeContext): Promise<CodeReview> {
    const prompt = this.buildReviewPrompt(code, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are an expert code reviewer. Provide detailed, actionable feedback on code quality, potential issues, and improvements. Focus on best practices, performance, security, and maintainability.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    const response = await this.ollama.chat(messages);
    return this.parseReviewResponse(response.message.content);
  }

  async debugCode(error: string, code: string): Promise<DebugSolution> {
    const prompt = `Debug this error: ${error}\n\nCode:\n${code}\n\nProvide a step-by-step solution with code fixes.`;
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are an expert debugger. Analyze the error and code, then provide a clear, step-by-step debugging solution with specific code changes.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    const response = await this.ollama.chat(messages);
    return this.parseDebugResponse(response.message.content);
  }

  async optimizeCode(code: string, metrics: any): Promise<CodeOptimization> {
    const prompt = `Optimize this code for better performance and maintainability:\n\n${code}\n\nCurrent metrics: ${JSON.stringify(metrics)}\n\nProvide optimized version with specific improvements.`;
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are a code optimization expert. Focus on performance improvements, algorithmic efficiency, memory usage, and code maintainability while preserving functionality.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    const response = await this.ollama.chat(messages);
    return this.parseOptimizationResponse(response.message.content, code);
  }

  private buildReviewPrompt(code: string, context: CodeContext): string {
    return `
Please review the following code:

Language: ${context.language}
File: ${context.filePath}
${context.framework ? `Framework: ${context.framework}` : ''}
${context.dependencies ? `Dependencies: ${context.dependencies.join(', ')}` : ''}

Code:
${code}

Please provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance concerns
4. Security vulnerabilities
5. Best practice violations
6. Suggestions for improvement
7. Overall score (1-10)

Format your response as a structured review.`;
  }

  private parseReviewResponse(response: string): CodeReview {
    // Parse the AI response into structured format
    const issues: CodeIssue[] = [];
    const suggestions: CodeSuggestion[] = [];
    let overall_score = 7; // Default score

    // Simple parsing logic - in production, use more sophisticated parsing
    const lines = response.split('\n');

    for (const line of lines) {
      if (line.toLowerCase().includes('error') || line.toLowerCase().includes('bug')) {
        issues.push({
          type: 'error',
          message: line.trim(),
          severity: 'high'
        });
      } else if (line.toLowerCase().includes('warning') || line.toLowerCase().includes('issue')) {
        issues.push({
          type: 'warning',
          message: line.trim(),
          severity: 'medium'
        });
      } else if (line.toLowerCase().includes('suggestion') || line.toLowerCase().includes('improve')) {
        suggestions.push({
          type: 'refactor',
          description: line.trim(),
          impact: 'medium'
        });
      }

      // Extract score if mentioned
      const scoreMatch = line.match(/score.*?(\d+)/i);
      if (scoreMatch) {
        overall_score = parseInt(scoreMatch[1]);
      }
    }

    return {
      issues,
      suggestions,
      overall_score: Math.min(10, Math.max(1, overall_score)),
      summary: response.substring(0, 200) + '...'
    };
  }

  private parseDebugResponse(response: string): DebugSolution {
    const steps = response.split('\n')
      .filter(line => line.trim().length > 0)
      .map((line, index) => ({
        description: line.trim(),
        expected_result: `Step ${index + 1} completed`
      }));

    return {
      solution: response,
      steps,
      confidence: 0.8
    };
  }

  private parseOptimizationResponse(response: string, originalCode: string): CodeOptimization {
    // Extract optimized code from response
    const codeMatch = response.match(/```\w*\n([\s\S]*?)\n```/);
    const optimizedCode = codeMatch ? codeMatch[1] : originalCode;

    return {
      optimized_code: optimizedCode,
      improvements: [{
        type: 'performance',
        description: 'Code optimization applied',
        impact: 'medium'
      }],
      performance_gain: 0.1 // Placeholder
    };
  }
}
