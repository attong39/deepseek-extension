import * as vscode from 'vscode';
import { OllamaClient } from '../../ollama/client';
import { ChatMessage } from '../../ollama/types';
import {
import Always from "Always";
import Analysis from "Analysis";
import AnalysisResult from "AnalysisResult";
import Analyze from "Analyze";
import Any from "Any";
import C from "C";
import Clear from "Clear";
import Code from "Code";
import CodeAnalyzer from "./CodeAnalyzer";
import CommonJS from "CommonJS";
import Complexity from "Complexity";
import Concerns from "Concerns";
import Context from "../../../../../desktop/src/Context/index";
import Current from "Current";
import Debug from "Debug";
import Dependencies from "Dependencies";
import Description from "Description";
import Documentation from "Documentation";
import ES6 from "ES6";
import Ensure from "Ensure";
import Error from "Error";
import Extract from "Extract";
import Failed from "Failed";
import Fallback from "Fallback";
import File from "File";
import Focus from "Focus";
import Format from "Format";
import Framework from "Framework";
import Function from "Function";
import Generate from "Generate";
import Guide from "Guide";
import High from "High";
import If from "If";
import Information from "Information";
import JSDoc from "JSDoc";
import Language from "Language";
import Limit from "Limit";
import Lines from "Lines";
import Maintainability from "Maintainability";
import Next from "Next";
import No from "No";
import None from "None";
import O from "O";
import Optimize from "Optimize";
import Overall from "Overall";
import Overview from "Overview";
import Parameter from "Parameter";
import Path from "Path";
import Performance from "Performance";
import Please from "Please";
import Project from "Project";
import Provide from "Provide";
import Python from "Python";
import Remove from "Remove";
import Required from "Required";
import Respond from "Respond";
import Response from "Response";
import Return from "Return";
import Review from "Review";
import Root from "Root";
import S from "S";
import Security from "Security";
import Set from "Set";
import Simple from "Simple";
import Standard from "Standard";
import Style from "Style";
import TextDocument from "TextDocument";
import Type from "Type";
import Unknown from "Unknown";
import Usage from "Usage";
import Validate from "Validate";
import Vue from "Vue";
import What from "What";
import You from "You";
  CodeContext,
  CodeReview,
  DebugSolution,
  CodeOptimization
} from '../../../types/shared';

export interface AnalysisResult {
  suggestions: string[];
  issues: Array<{
    severity: 'error' | 'warning' | 'info';
    message: string;
    line?: number;
    column?: number;
  }>;
  complexity: {
    cognitive: number;
    cyclomatic: number;
    maintainability: string;
  };
  improvements: string[];
}

export class CodeAnalyzer {
  private readonly ollama: OllamaClient;

  constructor(ollama: OllamaClient) {
    this.ollama = ollama;
  }

  async analyzeCurrentFile(): Promise<AnalysisResult> {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      throw new Error('No active editor found');
    }
    
    const code = editor.document.getText();
    const context = this.extractContext(editor.document);
    
    return this.analyzeCodeWithContext(code, context);
  }

  private extractContext(document: vscode.TextDocument): CodeContext {
    const workspaceFolder = vscode.workspace.getWorkspaceFolder(document.uri);
    const relativeFilePath = workspaceFolder ? 
      vscode.workspace.asRelativePath(document.uri) : 
      document.fileName;

    return {
      fileName: document.fileName,
      filePath: document.fileName,
      language: document.languageId,
      relativePath: relativeFilePath,
      lineCount: document.lineCount,
      projectType: this.detectProjectType(document),
      dependencies: this.extractDependencies(document),
      framework: this.detectFramework(document)
    };
  }

  private detectProjectType(document: vscode.TextDocument): string {
    const fileName = document.fileName.toLowerCase();
    const content = document.getText();

    if (fileName.includes('package.json')) return 'nodejs';
    if (fileName.includes('pyproject.toml') || fileName.includes('requirements.txt')) return 'python';
    if (fileName.includes('cargo.toml')) return 'rust';
    if (fileName.includes('go.mod')) return 'go';
    if (content.includes('import React') || content.includes('from react')) return 'react';
    if (content.includes('import Vue') || content.includes('from vue')) return 'vue';
    if (content.includes('@angular/')) return 'angular';
    
    return document.languageId;
  }

  private extractDependencies(document: vscode.TextDocument): string[] {
    const content = document.getText();
    const dependencies: string[] = [];

    // Extract imports for different languages
    const importRegexes = [
      /import\s+.*?\s+from\s+['"]([^'"]+)['"]/g, // ES6 imports
      /import\s+['"]([^'"]+)['"]/g, // Simple imports
      /require\(['"]([^'"]+)['"]\)/g, // CommonJS requires
      /from\s+([^\s]+)\s+import/g, // Python imports
      /#include\s*[<"]([^>"]+)[>"]/g // C/C++ includes
    ];

    importRegexes.forEach(regex => {
      let match;
      while ((match = regex.exec(content)) !== null) {
        dependencies.push(match[1]);
      }
    });

    return [...new Set(dependencies)].slice(0, 10); // Limit to 10 unique dependencies
  }

  private detectFramework(document: vscode.TextDocument): string {
    const content = document.getText();
    
    if (content.includes('express')) return 'express';
    if (content.includes('fastapi')) return 'fastapi';
    if (content.includes('django')) return 'django';
    if (content.includes('flask')) return 'flask';
    if (content.includes('spring')) return 'spring';
    if (content.includes('Next.js') || content.includes('next/')) return 'nextjs';
    if (content.includes('vite')) return 'vite';
    
    return 'unknown';
  }

  async analyzeCodeWithContext(code: string, context: CodeContext): Promise<AnalysisResult> {
    const prompt = this.buildAnalysisPrompt(code, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: `You are an expert code analyzer with deep knowledge of ${context.language} and ${context.framework}. 
        Analyze code for quality, security, performance, and maintainability. 
        Provide detailed analysis in JSON format with suggestions, issues, complexity metrics, and improvements.`
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

      return this.parseAnalysisResponse(response.message.content);
    } catch (error) {
      throw new Error(`Code analysis failed: ${error}`);
    }
  }

  private buildAnalysisPrompt(code: string, context: CodeContext): string {
    return `Analyze this ${context.language} code in the context of a ${context.framework} project:

**File Information:**
- File: ${context.relativePath}
- Language: ${context.language}
- Framework: ${context.framework}
- Lines: ${context.lineCount}
- Dependencies: ${context.dependencies?.join(', ') || 'none'}

**Code to Analyze:**
\`\`\`${context.language}
${code}
\`\`\`

**Analysis Required:**
1. Code quality and best practices
2. Security vulnerabilities
3. Performance optimizations
4. Maintainability issues
5. Complexity analysis
6. Framework-specific recommendations

**Response Format (JSON only):**
{
  "suggestions": ["improvement suggestion 1", "improvement suggestion 2"],
  "issues": [
    {
      "severity": "error|warning|info",
      "message": "issue description",
      "line": 10,
      "column": 5
    }
  ],
  "complexity": {
    "cognitive": 15,
    "cyclomatic": 8,
    "maintainability": "good|moderate|poor"
  },
  "improvements": ["specific improvement 1", "specific improvement 2"]
}`;
  }

  private parseAnalysisResponse(response: string): AnalysisResult {
    try {
      return JSON.parse(response);
    } catch {
      // Fallback if JSON parsing fails
      return {
        suggestions: ['Code analysis completed - see full response for details'],
        issues: [],
        complexity: {
          cognitive: 0,
          cyclomatic: 0,
          maintainability: 'unknown'
        },
        improvements: [response.substring(0, 200) + '...']
      };
    }
  }

  async reviewCode(code: string, context: CodeContext): Promise<CodeReview> {
    const prompt = this.buildReviewPrompt(code, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are an expert code reviewer with deep knowledge of software engineering best practices, security, performance optimization, and clean code principles. Provide detailed, actionable feedback in JSON format only.'
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

      return this.parseReviewResponse(response.message.content);
    } catch (error) {
      throw new Error(`Code review failed: ${error}`);
    }
  }

  async debugCode(error: string, code: string, context: CodeContext): Promise<DebugSolution> {
    const prompt = this.buildDebugPrompt(error, code, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are an expert debugging specialist. Analyze errors systematically and provide step-by-step solutions. Always respond in JSON format.'
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

      return this.parseDebugResponse(response.message.content);
    } catch (error) {
      throw new Error(`Code debugging failed: ${error}`);
    }
  }

  async optimizeCode(code: string, context: CodeContext, metrics?: string[]): Promise<CodeOptimization> {
    const prompt = this.buildOptimizationPrompt(code, context, metrics);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are a performance optimization expert. Focus on improving code efficiency, readability, and maintainability while preserving functionality. Respond in JSON format only.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    try {
      const response = await this.ollama.chat(messages, {
        model: 'deepseek-coder',
        temperature: 0.4,
        format: 'json'
      });

      return this.parseOptimizationResponse(response.message.content, code);
    } catch (error) {
      throw new Error(`Code optimization failed: ${error}`);
    }
  }

  async generateDocumentation(code: string, context: CodeContext): Promise<string> {
    const prompt = this.buildDocumentationPrompt(code, context);
    const messages: ChatMessage[] = [
      {
        role: 'system',
        content: 'You are a technical documentation expert. Generate clear, comprehensive documentation that follows best practices for the given programming language.'
      },
      {
        role: 'user',
        content: prompt
      }
    ];

    try {
      const response = await this.ollama.chat(messages, {
        model: 'deepseek-coder',
        temperature: 0.3
      });

      return response.message.content;
    } catch (error) {
      throw new Error(`Documentation generation failed: ${error}`);
    }
  }

  private buildReviewPrompt(code: string, context: CodeContext): string {
    return `
Please review the following ${context.language} code and provide detailed feedback:

**Context:**
- Language: ${context.language}
- Framework: ${context.framework || 'None'}
- Project Type: ${context.projectType || 'Unknown'}
- File Path: ${context.filePath}
- Dependencies: ${context.dependencies?.join(', ') || 'None'}
- Style Guide: ${context.styleGuide || 'Standard'}

**Code to Review:**
\`\`\`${context.language}
${code}
\`\`\`

**Required JSON Response Format:**
{
  "issues": [
    {
      "type": "error|warning|info|style",
      "message": "Description of the issue",
      "line": 1,
      "column": 1,
      "severity": "low|medium|high|critical",
      "rule": "rule name if applicable",
      "fixable": true,
      "suggestedFix": "code fix if applicable"
    }
  ],
  "suggestions": [
    {
      "type": "refactor|optimization|documentation|security|readability",
      "description": "What to improve",
      "code_example": "example code if applicable",
      "impact": "low|medium|high",
      "effort": "low|medium|high",
      "priority": "low|medium|high"
    }
  ],
  "overall_score": 85,
  "summary": "Overall assessment summary",
  "confidence": 90,
  "recommendations": ["priority recommendations"]
}

Focus on:
1. Code quality and best practices
2. Security vulnerabilities
3. Performance issues
4. Maintainability concerns
5. Language-specific conventions
`;
  }

  private buildDebugPrompt(error: string, code: string, context: CodeContext): string {
    return `
Debug the following ${context.language} code error:

**Error:**
${error}

**Context:**
- Language: ${context.language}
- Framework: ${context.framework || 'None'}
- File Path: ${context.filePath}

**Code:**
\`\`\`${context.language}
${code}
\`\`\`

**Required JSON Response Format:**
{
  "problem": "Clear description of the problem",
  "cause": "Root cause analysis",
  "solution": "High-level solution approach",
  "steps": [
    {
      "step_number": 1,
      "description": "What to do in this step",
      "code_change": "specific code changes if applicable",
      "expected_result": "what should happen",
      "verification": "how to verify this step worked"
    }
  ],
  "confidence": 95,
  "alternative_solutions": ["other possible approaches"],
  "preventive_measures": ["how to prevent similar issues"]
}

Provide a systematic debugging approach with actionable steps.
`;
  }

  private buildOptimizationPrompt(code: string, context: CodeContext, metrics?: string[]): string {
    const targetMetrics = metrics?.join(', ') || 'performance, memory usage, readability';
    
    return `
Optimize the following ${context.language} code focusing on: ${targetMetrics}

**Context:**
- Language: ${context.language}
- Framework: ${context.framework || 'None'}
- File Path: ${context.filePath}
- Current Performance Concerns: ${targetMetrics}

**Code to Optimize:**
\`\`\`${context.language}
${code}
\`\`\`

**Required JSON Response Format:**
{
  "original_code": "original code here",
  "optimized_code": "optimized version here",
  "improvements": [
    {
      "type": "performance|memory|readability|maintainability",
      "description": "what was improved",
      "impact": "low|medium|high",
      "measurement": "quantified improvement if possible"
    }
  ],
  "metrics": {
    "time_complexity_before": "O(n²)",
    "time_complexity_after": "O(n log n)",
    "space_complexity_before": "O(n)",
    "space_complexity_after": "O(1)",
    "estimated_performance_gain": "50% faster",
    "estimated_memory_savings": "30% less memory",
    "readability_score": 85
  },
  "explanation": "detailed explanation of optimizations",
  "risk_level": "low|medium|high"
}

Ensure the optimized code maintains the same functionality while improving the specified metrics.
`;
  }

  private buildDocumentationPrompt(code: string, context: CodeContext): string {
    return `
Generate comprehensive documentation for the following ${context.language} code:

**Context:**
- Language: ${context.language}
- Framework: ${context.framework || 'None'}
- File Path: ${context.filePath}

**Code:**
\`\`\`${context.language}
${code}
\`\`\`

Please provide:
1. Overview of what the code does
2. Function/class documentation
3. Parameter descriptions
4. Return value descriptions
5. Usage examples
6. Any important notes or warnings

Format the documentation according to ${context.language} conventions (JSDoc, docstrings, etc.).
`;
  }

  private parseReviewResponse(response: string): CodeReview {
    try {
      const cleanResponse = this.cleanJsonResponse(response);
      const parsed = JSON.parse(cleanResponse);
      
      // Validate and set defaults
      return {
        issues: parsed.issues || [],
        suggestions: parsed.suggestions || [],
        overall_score: parsed.overall_score || 0,
        summary: parsed.summary || 'No summary provided',
        confidence: parsed.confidence || 0,
        recommendations: parsed.recommendations || []
      };
    } catch (error) {
      throw new Error(`Failed to parse review response: ${error}`);
    }
  }

  private parseDebugResponse(response: string): DebugSolution {
    try {
      const cleanResponse = this.cleanJsonResponse(response);
      const parsed = JSON.parse(cleanResponse);
      
      return {
        problem: parsed.problem || 'Unknown problem',
        cause: parsed.cause || 'Unknown cause',
        solution: parsed.solution || 'No solution provided',
        steps: parsed.steps || [],
        confidence: parsed.confidence || 0,
        alternative_solutions: parsed.alternative_solutions || [],
        preventive_measures: parsed.preventive_measures || []
      };
    } catch (error) {
      throw new Error(`Failed to parse debug response: ${error}`);
    }
  }

  private parseOptimizationResponse(response: string, originalCode: string): CodeOptimization {
    try {
      const cleanResponse = this.cleanJsonResponse(response);
      const parsed = JSON.parse(cleanResponse);
      
      return {
        original_code: parsed.original_code || originalCode,
        optimized_code: parsed.optimized_code || originalCode,
        improvements: parsed.improvements || [],
        metrics: parsed.metrics || {},
        explanation: parsed.explanation || 'No explanation provided',
        risk_level: parsed.risk_level || 'medium'
      };
    } catch (error) {
      throw new Error(`Failed to parse optimization response: ${error}`);
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
}
