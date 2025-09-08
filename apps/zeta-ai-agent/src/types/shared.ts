import AI from "AI";
import ActionPlan from "ActionPlan";
import ActionStep from "ActionStep";
import Agent from "Agent";
import AgentAction from "AgentAction";
import AgentConfig from "AgentConfig";
import AgentInteraction from "AgentInteraction";
import CacheEntry from "CacheEntry";
import CodeContext from "CodeContext";
import CodeIssue from "CodeIssue";
import CodeOptimization from "CodeOptimization";
import CodeReview from "CodeReview";
import CodeSuggestion from "CodeSuggestion";
import CompletionContext from "CompletionContext";
import CompletionSuggestion from "CompletionSuggestion";
import ContextItem from "ContextItem";
import DebugSolution from "DebugSolution";
import DebugStep from "DebugStep";
import ExtensionConfig from "ExtensionConfig";
import ImpactLevel from "ImpactLevel";
import OptimizationImprovement from "OptimizationImprovement";
import OptimizationMetrics from "OptimizationMetrics";
import PerformanceMetrics from "PerformanceMetrics";
import PriorityLevel from "PriorityLevel";
import ProjectContext from "ProjectContext";
import RateLimitInfo from "RateLimitInfo";
import Record from "Record";
import RegExp from "RegExp";
import RelevantContext from "RelevantContext";
import RiskLevel from "RiskLevel";
import SecurityPolicy from "SecurityPolicy";
import SeverityLevel from "SeverityLevel";
import Shared from "./Shared";
import SystemMetrics from "SystemMetrics";
import T from "T";
import ValidationError from "ValidationError";
import ValidationResult from "ValidationResult";
import ValidationWarning from "ValidationWarning";
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
  fileName?: string;
  relativePath?: string;
  projectType?: string;
  dependencies?: string[];
  styleGuide?: string;
  lineCount?: number;
  complexity?: number;
}

export interface CodeReview {
  issues: CodeIssue[];
  suggestions: CodeSuggestion[];
  overall_score: number;
  summary: string;
  confidence: number;
  recommendations: string[];
}

export interface CodeIssue {
  type: 'error' | 'warning' | 'info' | 'style';
  message: string;
  line?: number;
  column?: number;
  severity: SeverityLevel;
  rule?: string;
  fixable?: boolean;
  suggestedFix?: string;
}

export interface CodeSuggestion {
  type: 'refactor' | 'optimization' | 'documentation' | 'security' | 'readability';
  description: string;
  code_example?: string;
  impact: ImpactLevel;
  effort: 'low' | 'medium' | 'high';
  priority: PriorityLevel;
}

export interface DebugSolution {
  problem: string;
  cause: string;
  solution: string;
  steps: DebugStep[];
  confidence: number;
  alternative_solutions?: string[];
  preventive_measures?: string[];
}

export interface DebugStep {
  step_number: number;
  description: string;
  code_change?: string;
  expected_result: string;
  verification?: string;
}

export interface CodeOptimization {
  original_code: string;
  optimized_code: string;
  improvements: OptimizationImprovement[];
  metrics: OptimizationMetrics;
  explanation: string;
  risk_level: RiskLevel;
}

export interface OptimizationImprovement {
  type: 'performance' | 'memory' | 'readability' | 'maintainability';
  description: string;
  impact: ImpactLevel;
  measurement?: string;
}

export interface OptimizationMetrics {
  time_complexity_before?: string;
  time_complexity_after?: string;
  space_complexity_before?: string;
  space_complexity_after?: string;
  estimated_performance_gain?: string;
  estimated_memory_savings?: string;
  readability_score?: number;
}

export interface AgentAction {
  type: 'code_review' | 'debug' | 'optimize' | 'chat' | 'generate' | 'refactor';
  target: string;
  timestamp: Date;
  result: any;
  success: boolean;
  duration?: number;
  error?: string;
}

export interface AgentInteraction {
  id: string;
  timestamp: Date;
  type: 'code_review' | 'debug' | 'optimization' | 'chat' | 'completion';
  user_input: string;
  agent_response: string;
  context: CodeContext;
  success: boolean;
  feedback?: number; // 1-5 rating
  action_type: string;
  target: string;
  result: any;
}

export interface RelevantContext {
  items: ContextItem[];
  recent_actions: AgentAction[];
  query: string;
  relevance_score?: number;
  suggestions?: string[];
}

export interface ContextItem {
  content: string;
  timestamp: Date;
  type: 'interaction' | 'code' | 'documentation' | 'error';
  relevance?: number;
  metadata?: Record<string, any>;
}

export interface ActionStep {
  type: 'code_analysis' | 'file_operation' | 'tool_use' | 'user_query' | 'validation';
  description: string;
  parameters: Record<string, any>;
  expected_outcome: string;
  dependencies?: string[];
  estimated_duration?: number;
}

export interface ActionPlan {
  goal: string;
  steps: ActionStep[];
  estimated_time: number;
  confidence: number;
  prerequisites?: string[];
  risks?: string[];
  success_criteria?: string[];
}

export interface CompletionContext {
  language: string;
  file_path: string;
  line: number;
  character: number;
  text_before: string;
  text_after: string;
  surrounding_code?: string;
  project_context?: ProjectContext;
}

export interface ProjectContext {
  name?: string;
  type?: string;
  frameworks?: string[];
  dependencies?: string[];
  recent_files?: string[];
  coding_patterns?: string[];
}

export interface CompletionSuggestion {
  label: string;
  code: string;
  documentation: string;
  confidence: number;
  type: 'function' | 'class' | 'variable' | 'import' | 'snippet';
  metadata?: Record<string, any>;
}

export interface PerformanceMetrics {
  [operation: string]: {
    count: number;
    average: number;
    p95: number;
    p99: number;
    min: number;
    max: number;
    errors: number;
    last_updated: Date;
  };
}

export interface SystemMetrics {
  memory_usage: number;
  cpu_usage: number;
  active_connections: number;
  uptime: number;
  requests_per_minute: number;
  error_rate: number;
}

export interface CacheEntry<T = any> {
  key: string;
  value: T;
  timestamp: Date;
  ttl: number;
  hits: number;
  size?: number;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions?: string[];
}

export interface ValidationError {
  code: string;
  message: string;
  line?: number;
  column?: number;
  severity: 'error' | 'warning';
}

export interface ValidationWarning {
  code: string;
  message: string;
  suggestion?: string;
  severity: 'low' | 'medium' | 'high';
}

export interface RateLimitInfo {
  allowed: boolean;
  remaining: number;
  reset_time: number;
  limit: number;
  window_size: number;
}

export interface SecurityPolicy {
  max_code_size: number;
  allowed_file_extensions: string[];
  blocked_patterns: RegExp[];
  max_context_size: number;
  rate_limit_per_minute: number;
}

export interface AgentConfig {
  ollama_url: string;
  default_model: string;
  max_context_size: number;
  enable_caching: boolean;
  cache_ttl: number;
  rate_limit: number;
  security_policy: SecurityPolicy;
  performance_monitoring: boolean;
  log_level: 'debug' | 'info' | 'warn' | 'error';
}

export type ExtensionConfig = AgentConfig
