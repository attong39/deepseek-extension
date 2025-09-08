import AI from "AI";
import ActionPlan from "ActionPlan";
import Agent from "Agent";
import AgentAction from "AgentAction";
import AgentContext from "AgentContext";
import CodeContext from "CodeContext";
import CodeIssue from "CodeIssue";
import CodeOptimization from "CodeOptimization";
import CodeReview from "CodeReview";
import CodeSuggestion from "CodeSuggestion";
import CompletionContext from "CompletionContext";
import CompletionSuggestion from "CompletionSuggestion";
import DebugSolution from "DebugSolution";
import DebugStep from "DebugStep";
import FunctionDefinition from "FunctionDefinition";
import ImpactLevel from "ImpactLevel";
import OptimizationImprovement from "OptimizationImprovement";
import Parameter from "Parameter";
import PerformanceMetrics from "PerformanceMetrics";
import PlannedAction from "PlannedAction";
import PriorityLevel from "PriorityLevel";
import ProjectStructure from "ProjectStructure";
import RefactorPattern from "RefactorPattern";
import RiskLevel from "RiskLevel";
import SeverityLevel from "SeverityLevel";
import Shared from "./Shared";
import TestFramework from "TestFramework";
import Zeta from "Zeta";
// Shared types for the Zeta AI Agent

export type SeverityLevel = 'low' | 'medium' | 'high' | 'critical';
export type ImpactLevel = 'low' | 'medium' | 'high';
export type PriorityLevel = 'low' | 'medium' | 'high';
export type RiskLevel = 'low' | 'medium' | 'high';

export interface CodeContext {
  language: string;
  framework?: string;
  filePath: string;
  projectType?: string;
  dependencies?: string[];
}

export interface CodeReview {
  issues: CodeIssue[];
  suggestions: CodeSuggestion[];
  overall_score: number;
  summary: string;
}

export interface CodeIssue {
  type: 'error' | 'warning' | 'info';
  message: string;
  line?: number;
  column?: number;
  severity: SeverityLevel;
}

export interface CodeSuggestion {
  type: 'refactor' | 'optimization' | 'documentation' | 'security';
  description: string;
  code_example?: string;
  impact: ImpactLevel;
}

export interface DebugSolution {
  solution: string;
  steps: DebugStep[];
  confidence: number;
  alternative_solutions?: string[];
}

export interface DebugStep {
  description: string;
  code_change?: string;
  expected_result: string;
}

export interface CodeOptimization {
  optimized_code: string;
  improvements: OptimizationImprovement[];
  performance_gain?: number;
  complexity_reduction?: number;
}

export interface OptimizationImprovement {
  type: 'performance' | 'readability' | 'maintainability' | 'security';
  description: string;
  impact: ImpactLevel;
}

export interface AgentContext {
  current_file?: string;
  selected_text?: string;
  project_structure?: ProjectStructure;
  recent_actions?: AgentAction[];
}

export interface ProjectStructure {
  root_path: string;
  files: string[];
  directories: string[];
  main_language: string;
  frameworks: string[];
}

export interface AgentAction {
  type: 'review' | 'debug' | 'optimize' | 'refactor' | 'document';
  target: string;
  timestamp: Date;
  result: any;
  success: boolean;
}

export interface ActionPlan {
  actions: PlannedAction[];
  estimated_time: number;
  risk_level: RiskLevel;
  dependencies: string[];
}

export interface PlannedAction {
  id: string;
  type: string;
  description: string;
  priority: PriorityLevel;
  estimated_duration: number;
}

export interface FunctionDefinition {
  name: string;
  parameters: Parameter[];
  return_type?: string;
  docstring?: string;
  complexity: number;
  lines: number;
}

export interface Parameter {
  name: string;
  type?: string;
  default_value?: any;
  description?: string;
}

export interface TestFramework {
  name: string;
  language: string;
  template: string;
}

export interface RefactorPattern {
  name: string;
  description: string;
  before_pattern: string;
  after_pattern: string;
}

export interface PerformanceMetrics {
  [operation: string]: {
    count: number;
    average: number;
    p95: number;
    p99: number;
  };
}

export interface CompletionContext {
  prefix: string;
  suffix: string;
  language: string;
  file_path: string;
  cursor_position: {
    line: number;
    column: number;
  };
}

export interface CompletionSuggestion {
  text: string;
  type: 'function' | 'variable' | 'class' | 'method' | 'keyword';
  confidence: number;
  documentation?: string;
}
