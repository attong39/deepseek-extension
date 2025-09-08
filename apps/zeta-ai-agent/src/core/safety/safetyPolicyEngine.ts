import AI from "AI";
import Add from "Add";
import Apply from "Apply";
import Assess from "Assess";
import Attempt from "Attempt";
import BEHAVIORAL from "BEHAVIORAL";
import BLOCK from "BLOCK";
import BLOCKED from "BLOCKED";
import CONTENT from "CONTENT";
import CONTENT_FILTERING from "CONTENT_FILTERING";
import CPU from "CPU";
import CRITICAL from "CRITICAL";
import Calculate from "Calculate";
import Check from "Check";
import Cleanup from "Cleanup";
import Comprehensive from "Comprehensive";
import Concurrent from "Concurrent";
import Consider from "Consider";
import Content from "Content";
import ContentFilter from "ContentFilter";
import Count from "Count";
import Critical from "Critical";
import DATA_PRIVACY from "DATA_PRIVACY";
import DECREASING from "DECREASING";
import Dangerous from "Dangerous";
import DangerousPattern from "DangerousPattern";
import Default from "Default";
import ESCALATED from "ESCALATED";
import Engine from "Engine";
import Exploitation from "Exploitation";
import Export from "Export";
import FAILURE from "FAILURE";
import FILTERED from "FILTERED";
import FLAG from "FLAG";
import Filter from "Filter";
import Fire from "Fire";
import Function from "Function";
import Generate from "Generate";
import Get from "Get";
import Global from "Global";
import HIGH from "HIGH";
import Harmful from "Harmful";
import High from "High";
import How from "How";
import INCREASING from "INCREASING";
import Immediate from "Immediate";
import Implements from "Implements";
import Include from "Include";
import KEYWORD from "KEYWORD";
import Keep from "Keep";
import LOGGED from "LOGGED";
import LOW from "LOW";
import Limit from "Limit";
import MB from "MB";
import MEDIUM from "MEDIUM";
import ML from "ML";
import MODIFY from "MODIFY";
import MONITOR from "MONITOR";
import Map from "Map";
import Math from "Math";
import Maximum from "Maximum";
import Memory from "../../../../desktop/src/Memory/index";
import Monitor from "Monitor";
import OPERATIONAL_SAFETY from "OPERATIONAL_SAFETY";
import Operation from "Operation";
import Operations from "Operations";
import PATTERN_DETECTION from "PATTERN_DETECTION";
import Partial from "Partial";
import Per from "Per";
import Percentage from "Percentage";
import Policy from "Policy";
import PolicyType from "PolicyType";
import Potential from "Potential";
import Private from "Private";
import RATE_LIMITING from "RATE_LIMITING";
import REGEX from "REGEX";
import RESOURCE_USAGE from "RESOURCE_USAGE";
import Rapid from "Rapid";
import Rate from "Rate";
import RateLimit from "RateLimit";
import Record from "Record";
import RegExp from "RegExp";
import Remove from "Remove";
import Requests from "Requests";
import Resolve from "Resolve";
import Resource from "Resource";
import ResourceLimits from "ResourceLimits";
import Review from "Review";
import RiskLevel from "RiskLevel";
import SEMANTIC from "SEMANTIC";
import STABLE from "STABLE";
import SUCCESS from "SUCCESS";
import SYSTEM from "SYSTEM";
import Safety from "Safety";
import SafetyAssessment from "SafetyAssessment";
import SafetyContext from "SafetyContext";
import SafetyPolicyEngine from "./SafetyPolicyEngine";
import SafetyViolation from "SafetyViolation";
import Seconds from "Seconds";
import Simplified from "Simplified";
import Split from "Split";
import System from "System";
import THROTTLE from "THROTTLE";
import THROTTLED from "THROTTLED";
import Time from "Time";
import Unusual from "Unusual";
import Update from "Update";
import Usage from "Usage";
/**
 * Safety Policy Engine
 * Comprehensive safety system for autonomous AI operations
 * Implements rate limiting, pattern detection, content filtering, and risk assessment
 */

/**
 * Safety risk levels
 */
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

/**
 * Safety policy types
 */
export type PolicyType = 
  | 'RATE_LIMITING'
  | 'CONTENT_FILTERING'
  | 'PATTERN_DETECTION'
  | 'RESOURCE_USAGE'
  | 'DATA_PRIVACY'
  | 'OPERATIONAL_SAFETY';

/**
 * Safety violation record
 */
export interface SafetyViolation {
  id: string;
  timestamp: Date;
  policyType: PolicyType;
  riskLevel: RiskLevel;
  description: string;
  context: {
    userId?: string;
    operation: string;
    parameters: Record<string, any>;
    triggeredRule: string;
  };
  action: 'BLOCKED' | 'THROTTLED' | 'LOGGED' | 'ESCALATED';
  resolved: boolean;
  resolution?: {
    timestamp: Date;
    action: string;
    notes: string;
  };
}

/**
 * Rate limiting configuration
 */
export interface RateLimit {
  id: string;
  name: string;
  windowMs: number; // Time window in milliseconds
  maxRequests: number; // Maximum requests per window
  keyGenerator: (context: SafetyContext) => string; // Function to generate rate limit key
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
  message?: string;
  onLimitReached?: (key: string, violations: number) => void;
}

/**
 * Content filter configuration
 */
export interface ContentFilter {
  id: string;
  name: string;
  patterns: Array<{
    pattern: string | RegExp;
    type: 'REGEX' | 'KEYWORD' | 'SEMANTIC';
    severity: RiskLevel;
  }>;
  categories: Array<{
    category: string;
    threshold: number; // 0-1 confidence threshold
    action: 'BLOCK' | 'FLAG' | 'MODIFY';
  }>;
  enabled: boolean;
}

/**
 * Dangerous pattern definition
 */
export interface DangerousPattern {
  id: string;
  name: string;
  description: string;
  pattern: {
    type: 'BEHAVIORAL' | 'CONTENT' | 'SYSTEM';
    indicators: string[];
    threshold: number; // How many indicators needed to trigger
    timeWindow?: number; // Time window for behavioral patterns
  };
  riskLevel: RiskLevel;
  response: {
    immediate: 'BLOCK' | 'THROTTLE' | 'MONITOR';
    escalation?: string;
    notification: boolean;
  };
  enabled: boolean;
}

/**
 * Safety context for evaluation
 */
export interface SafetyContext {
  userId?: string;
  sessionId?: string;
  operation: string;
  input: string;
  parameters: Record<string, any>;
  timestamp: Date;
  userHistory?: Array<{
    timestamp: Date;
    operation: string;
    result: 'SUCCESS' | 'FAILURE' | 'BLOCKED';
  }>;
  systemMetrics?: {
    cpuUsage: number;
    memoryUsage: number;
    requestCount: number;
  };
}

/**
 * Safety assessment result
 */
export interface SafetyAssessment {
  allowed: boolean;
  riskLevel: RiskLevel;
  violations: Array<{
    policyType: PolicyType;
    rule: string;
    severity: RiskLevel;
    message: string;
  }>;
  modifications?: {
    filteredInput?: string;
    adjustedParameters?: Record<string, any>;
    addedConstraints?: string[];
  };
  recommendations: string[];
  requiresEscalation: boolean;
}

/**
 * Resource usage limits
 */
export interface ResourceLimits {
  maxCpuUsage: number; // Percentage
  maxMemoryUsage: number; // MB
  maxExecutionTime: number; // Seconds
  maxConcurrentOperations: number;
  maxDailyOperations: number;
  maxFileSize: number; // MB
}

/**
 * Safety Policy Engine implementation
 */
export class SafetyPolicyEngine {
  private readonly rateLimits: Map<string, RateLimit> = new Map();
  private readonly contentFilters: Map<string, ContentFilter> = new Map();
  private readonly dangerousPatterns: Map<string, DangerousPattern> = new Map();
  private readonly violations: SafetyViolation[] = [];
  private readonly requestCounts: Map<string, Array<{ timestamp: number; count: number }>> = new Map();
  private readonly behavioralHistory: Map<string, Array<{ timestamp: Date; indicators: string[] }>> = new Map();
  private readonly resourceLimits: ResourceLimits;
  private readonly maxViolationHistory: number = 1000;

  constructor(resourceLimits?: Partial<ResourceLimits>) {
    this.resourceLimits = {
      maxCpuUsage: 80,
      maxMemoryUsage: 1024,
      maxExecutionTime: 300,
      maxConcurrentOperations: 10,
      maxDailyOperations: 10000,
      maxFileSize: 100,
      ...resourceLimits
    };

    this.initializeDefaultPolicies();
  }

  /**
   * Assess safety of operation
   */
  async assessSafety(context: SafetyContext): Promise<SafetyAssessment> {
    const violations: SafetyAssessment['violations'] = [];
    const recommendations: string[] = [];
    let modifications: SafetyAssessment['modifications'] = {};
    let highestRisk: RiskLevel = 'LOW';

    // Check rate limits
    const rateLimitViolation = this.checkRateLimits(context);
    if (rateLimitViolation) {
      violations.push(rateLimitViolation);
      highestRisk = this.escalateRiskLevel(highestRisk, rateLimitViolation.severity);
    }

    // Check content filters
    const contentViolations = await this.checkContentFilters(context);
    violations.push(...contentViolations.violations);
    if (contentViolations.modifications) {
      modifications = { ...modifications, ...contentViolations.modifications };
    }
    for (const violation of contentViolations.violations) {
      highestRisk = this.escalateRiskLevel(highestRisk, violation.severity);
    }

    // Check dangerous patterns
    const patternViolations = this.checkDangerousPatterns(context);
    violations.push(...patternViolations);
    for (const violation of patternViolations) {
      highestRisk = this.escalateRiskLevel(highestRisk, violation.severity);
    }

    // Check resource usage
    const resourceViolation = this.checkResourceUsage(context);
    if (resourceViolation) {
      violations.push(resourceViolation);
      highestRisk = this.escalateRiskLevel(highestRisk, resourceViolation.severity);
    }

    // Generate recommendations
    recommendations.push(...this.generateSafetyRecommendations(violations, context));

    // Record violations
    if (violations.length > 0) {
      this.recordViolations(violations, context);
    }

    const allowed = violations.length === 0 || violations.every(v => v.severity !== 'CRITICAL');
    const requiresEscalation = violations.some(v => v.severity === 'CRITICAL' || v.severity === 'HIGH');

    return {
      allowed,
      riskLevel: highestRisk,
      violations,
      modifications: Object.keys(modifications).length > 0 ? modifications : undefined,
      recommendations,
      requiresEscalation
    };
  }

  /**
   * Add rate limit policy
   */
  addRateLimit(rateLimit: RateLimit): void {
    this.rateLimits.set(rateLimit.id, rateLimit);
  }

  /**
   * Add content filter
   */
  addContentFilter(filter: ContentFilter): void {
    this.contentFilters.set(filter.id, filter);
  }

  /**
   * Add dangerous pattern
   */
  addDangerousPattern(pattern: DangerousPattern): void {
    this.dangerousPatterns.set(pattern.id, pattern);
  }

  /**
   * Get safety statistics
   */
  getSafetyStatistics(timeWindow: number = 24 * 60 * 60 * 1000): {
    totalViolations: number;
    violationsByType: Record<PolicyType, number>;
    violationsByRisk: Record<RiskLevel, number>;
    topViolatedRules: Array<{ rule: string; count: number }>;
    riskTrend: 'INCREASING' | 'DECREASING' | 'STABLE';
    recommendations: string[];
  } {
    const cutoffTime = Date.now() - timeWindow;
    const recentViolations = this.violations.filter(v => v.timestamp.getTime() > cutoffTime);

    const violationsByType: Record<PolicyType, number> = {
      RATE_LIMITING: 0,
      CONTENT_FILTERING: 0,
      PATTERN_DETECTION: 0,
      RESOURCE_USAGE: 0,
      DATA_PRIVACY: 0,
      OPERATIONAL_SAFETY: 0
    };

    const violationsByRisk: Record<RiskLevel, number> = {
      LOW: 0,
      MEDIUM: 0,
      HIGH: 0,
      CRITICAL: 0
    };

    const ruleCount: Map<string, number> = new Map();

    recentViolations.forEach(violation => {
      violationsByType[violation.policyType]++;
      violationsByRisk[violation.riskLevel]++;
      
      const rule = violation.context.triggeredRule;
      ruleCount.set(rule, (ruleCount.get(rule) || 0) + 1);
    });

    const topViolatedRules = Array.from(ruleCount.entries())
      .map(([rule, count]) => ({ rule, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    // Calculate risk trend
    const riskTrend = this.calculateRiskTrend(timeWindow);

    // Generate recommendations
    const recommendations = this.generateSystemRecommendations(violationsByType, violationsByRisk);

    return {
      totalViolations: recentViolations.length,
      violationsByType,
      violationsByRisk,
      topViolatedRules,
      riskTrend,
      recommendations
    };
  }

  /**
   * Update policy configuration
   */
  updateRateLimit(id: string, updates: Partial<RateLimit>): boolean {
    const rateLimit = this.rateLimits.get(id);
    if (!rateLimit) return false;

    Object.assign(rateLimit, updates);
    return true;
  }

  updateContentFilter(id: string, updates: Partial<ContentFilter>): boolean {
    const filter = this.contentFilters.get(id);
    if (!filter) return false;

    Object.assign(filter, updates);
    return true;
  }

  updateDangerousPattern(id: string, updates: Partial<DangerousPattern>): boolean {
    const pattern = this.dangerousPatterns.get(id);
    if (!pattern) return false;

    Object.assign(pattern, updates);
    return true;
  }

  /**
   * Get all violations
   */
  getViolations(limit = 100): SafetyViolation[] {
    const sortedViolations = [...this.violations];
    sortedViolations.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
    return sortedViolations.slice(0, limit);
  }

  /**
   * Resolve violation
   */
  resolveViolation(violationId: string, action: string, notes: string): boolean {
    const violation = this.violations.find(v => v.id === violationId);
    if (!violation) return false;

    violation.resolved = true;
    violation.resolution = {
      timestamp: new Date(),
      action,
      notes
    };

    return true;
  }

  /**
   * Export safety configuration
   */
  exportSafetyConfig(): string {
    return JSON.stringify({
      version: '1.0',
      timestamp: new Date().toISOString(),
      rateLimits: Array.from(this.rateLimits.values()),
      contentFilters: Array.from(this.contentFilters.values()),
      dangerousPatterns: Array.from(this.dangerousPatterns.values()),
      resourceLimits: this.resourceLimits,
      recentViolations: this.violations.slice(-50) // Include recent violations
    }, null, 2);
  }

  /**
   * Private helper methods
   */

  private checkRateLimits(context: SafetyContext): SafetyAssessment['violations'][0] | null {
    for (const rateLimit of this.rateLimits.values()) {
      const key = rateLimit.keyGenerator(context);
      const now = Date.now();
      
      // Get or create request history for this key
      let requests = this.requestCounts.get(key) || [];
      
      // Remove old requests outside the window
      requests = requests.filter(req => now - req.timestamp < rateLimit.windowMs);
      
      // Count current requests
      const currentCount = requests.reduce((sum, req) => sum + req.count, 0);
      
      if (currentCount >= rateLimit.maxRequests) {
        return {
          policyType: 'RATE_LIMITING',
          rule: rateLimit.name,
          severity: 'MEDIUM',
          message: rateLimit.message || `Rate limit exceeded: ${currentCount}/${rateLimit.maxRequests} requests in ${rateLimit.windowMs}ms`
        };
      }
      
      // Record this request
      requests.push({ timestamp: now, count: 1 });
      this.requestCounts.set(key, requests);
    }
    
    return null;
  }

  private async checkContentFilters(context: SafetyContext): Promise<{
    violations: SafetyAssessment['violations'];
    modifications?: SafetyAssessment['modifications'];
  }> {
    const violations: SafetyAssessment['violations'] = [];
    const modifications: SafetyAssessment['modifications'] = {};

    for (const filter of this.contentFilters.values()) {
      if (!filter.enabled) continue;

      // Check patterns
      const patternResults = this.checkFilterPatterns(filter, context.input);
      violations.push(...patternResults.violations);
      if (patternResults.modifications) {
        Object.assign(modifications, patternResults.modifications);
      }

      // Check categories
      const categoryResults = this.checkFilterCategories(filter, context.input);
      violations.push(...categoryResults.violations);
      if (categoryResults.modifications) {
        Object.assign(modifications, categoryResults.modifications);
      }
    }

    return {
      violations,
      modifications: Object.keys(modifications).length > 0 ? modifications : undefined
    };
  }

  private checkFilterPatterns(filter: ContentFilter, input: string): {
    violations: SafetyAssessment['violations'];
    modifications?: SafetyAssessment['modifications'];
  } {
    const violations: SafetyAssessment['violations'] = [];
    const modifications: SafetyAssessment['modifications'] = {};

    for (const patternConfig of filter.patterns) {
      const { pattern, type, severity } = patternConfig;
      const matches = this.checkPatternMatch(pattern, type, input);

      if (matches) {
        violations.push({
          policyType: 'CONTENT_FILTERING',
          rule: `${filter.name} - ${type} pattern`,
          severity,
          message: `Content matched ${type.toLowerCase()} pattern: ${pattern}`
        });

        // Apply content modification if needed
        if (severity !== 'CRITICAL') {
          modifications.filteredInput = this.filterContent(input, pattern);
        }
      }
    }

    return { violations, modifications };
  }

  private checkFilterCategories(filter: ContentFilter, input: string): {
    violations: SafetyAssessment['violations'];
    modifications?: SafetyAssessment['modifications'];
  } {
    const violations: SafetyAssessment['violations'] = [];
    const modifications: SafetyAssessment['modifications'] = {};

    for (const categoryConfig of filter.categories) {
      const confidence = this.calculateCategoryConfidence(input, categoryConfig.category);
      
      if (confidence > categoryConfig.threshold) {
        const severity = confidence > 0.8 ? 'HIGH' : 'MEDIUM';
        
        violations.push({
          policyType: 'CONTENT_FILTERING',
          rule: `${filter.name} - ${categoryConfig.category}`,
          severity,
          message: `Content categorized as ${categoryConfig.category} with ${Math.round(confidence * 100)}% confidence`
        });

        if (categoryConfig.action === 'MODIFY') {
          modifications.filteredInput = this.sanitizeContent(input, categoryConfig.category);
        }
      }
    }

    return { violations, modifications };
  }

  private checkPatternMatch(pattern: string | RegExp, type: string, input: string): boolean {
    if (type === 'REGEX' && pattern instanceof RegExp) {
      return pattern.test(input);
    } else if (type === 'KEYWORD' && typeof pattern === 'string') {
      return input.toLowerCase().includes(pattern.toLowerCase());
    } else if (type === 'SEMANTIC') {
      return this.semanticMatch(input, pattern as string);
    }
    return false;
  }

  private checkDangerousPatterns(context: SafetyContext): SafetyAssessment['violations'] {
    const violations: SafetyAssessment['violations'] = [];

    for (const pattern of this.dangerousPatterns.values()) {
      if (!pattern.enabled) continue;

      const { type, indicators, threshold, timeWindow } = pattern.pattern;
      let indicatorCount = 0;

      if (type === 'CONTENT') {
        // Check content-based indicators
        indicatorCount = indicators.filter(indicator => 
          context.input.toLowerCase().includes(indicator.toLowerCase())
        ).length;
      } else if (type === 'BEHAVIORAL') {
        // Check behavioral patterns
        indicatorCount = this.checkBehavioralIndicators(context, indicators, timeWindow);
      } else if (type === 'SYSTEM') {
        // Check system-level indicators
        indicatorCount = this.checkSystemIndicators(context, indicators);
      }

      if (indicatorCount >= threshold) {
        violations.push({
          policyType: 'PATTERN_DETECTION',
          rule: pattern.name,
          severity: pattern.riskLevel,
          message: `Dangerous pattern detected: ${pattern.description} (${indicatorCount}/${indicators.length} indicators)`
        });

        // Record behavioral history
        if (type === 'BEHAVIORAL' && context.userId) {
          this.recordBehavioralIndicators(context.userId, indicators.slice(0, indicatorCount));
        }
      }
    }

    return violations;
  }

  private checkResourceUsage(context: SafetyContext): SafetyAssessment['violations'][0] | null {
    const metrics = context.systemMetrics;
    if (!metrics) return null;

    if (metrics.cpuUsage > this.resourceLimits.maxCpuUsage) {
      return {
        policyType: 'RESOURCE_USAGE',
        rule: 'CPU Usage Limit',
        severity: 'HIGH',
        message: `CPU usage ${metrics.cpuUsage}% exceeds limit of ${this.resourceLimits.maxCpuUsage}%`
      };
    }

    if (metrics.memoryUsage > this.resourceLimits.maxMemoryUsage) {
      return {
        policyType: 'RESOURCE_USAGE',
        rule: 'Memory Usage Limit',
        severity: 'HIGH',
        message: `Memory usage ${metrics.memoryUsage}MB exceeds limit of ${this.resourceLimits.maxMemoryUsage}MB`
      };
    }

    if (metrics.requestCount > this.resourceLimits.maxConcurrentOperations) {
      return {
        policyType: 'RESOURCE_USAGE',
        rule: 'Concurrent Operations Limit',
        severity: 'MEDIUM',
        message: `Concurrent operations ${metrics.requestCount} exceeds limit of ${this.resourceLimits.maxConcurrentOperations}`
      };
    }

    return null;
  }

  private escalateRiskLevel(current: RiskLevel, new_level: RiskLevel): RiskLevel {
    const levels = { LOW: 1, MEDIUM: 2, HIGH: 3, CRITICAL: 4 };
    return levels[new_level] > levels[current] ? new_level : current;
  }

  private recordViolations(violations: SafetyAssessment['violations'], context: SafetyContext): void {
    violations.forEach(violation => {
      const safetyViolation: SafetyViolation = {
        id: this.generateViolationId(),
        timestamp: new Date(),
        policyType: violation.policyType,
        riskLevel: violation.severity,
        description: violation.message,
        context: {
          userId: context.userId,
          operation: context.operation,
          parameters: context.parameters,
          triggeredRule: violation.rule
        },
        action: this.determineAction(violation.severity),
        resolved: false
      };

      this.violations.push(safetyViolation);
    });

    // Cleanup old violations
    if (this.violations.length > this.maxViolationHistory) {
      this.violations.splice(0, this.violations.length - this.maxViolationHistory);
    }
  }

  private determineAction(severity: RiskLevel): SafetyViolation['action'] {
    switch (severity) {
    case 'CRITICAL':
      return 'BLOCKED';
    case 'HIGH':
      return 'ESCALATED';
    case 'MEDIUM':
      return 'THROTTLED';
    case 'LOW':
      return 'LOGGED';
    default:
      return 'LOGGED';
    }
  }

  private generateViolationId(): string {
    return `violation_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }

  private semanticMatch(text: string, pattern: string): boolean {
    // Simplified semantic matching - in production, use proper embedding models
    const textWords = text.toLowerCase().split(/\s+/);
    const patternWords = pattern.toLowerCase().split(/\s+/);
    
    const commonWords = textWords.filter(word => patternWords.includes(word));
    return commonWords.length / patternWords.length > 0.5;
  }

  private filterContent(content: string, pattern: string | RegExp): string {
    if (pattern instanceof RegExp) {
      return content.replace(pattern, '[FILTERED]');
    } else {
      return content.replace(new RegExp(pattern, 'gi'), '[FILTERED]');
    }
  }

  private sanitizeContent(content: string, category: string): string {
    // Simplified content sanitization
    return `[Content filtered - ${category} detected]`;
  }

  private calculateCategoryConfidence(content: string, category: string): number {
    // Simplified category classification - in production, use ML models
    const keywords: Record<string, string[]> = {
      'harmful': ['harm', 'damage', 'hurt', 'violence', 'attack'],
      'inappropriate': ['inappropriate', 'offensive', 'vulgar'],
      'private': ['password', 'secret', 'confidential', 'private']
    };

    const categoryKeywords = keywords[category.toLowerCase()] || [];
    const contentWords = content.toLowerCase().split(/\s+/);
    const matches = contentWords.filter(word => categoryKeywords.includes(word));
    
    return Math.min(matches.length / categoryKeywords.length, 1.0);
  }

  private checkBehavioralIndicators(context: SafetyContext, indicators: string[], timeWindow?: number): number {
    if (!context.userId || !context.userHistory) return 0;

    const window = timeWindow || 60 * 60 * 1000; // 1 hour default
    const cutoffTime = new Date(Date.now() - window);
    
    const recentHistory = context.userHistory.filter(h => h.timestamp > cutoffTime);
    let indicatorCount = 0;

    indicators.forEach(indicator => {
      const hasIndicator = recentHistory.some(h => 
        h.operation.toLowerCase().includes(indicator.toLowerCase())
      );
      if (hasIndicator) indicatorCount++;
    });

    return indicatorCount;
  }

  private checkSystemIndicators(context: SafetyContext, indicators: string[]): number {
    let indicatorCount = 0;

    for (const indicator of indicators) {
      let hasIndicator = false;
      
      if (indicator === 'high_frequency' && context.systemMetrics?.requestCount && context.systemMetrics.requestCount > 50) {
        hasIndicator = true;
      } else if (indicator === 'resource_intensive' && context.systemMetrics?.cpuUsage && context.systemMetrics.cpuUsage > 70) {
        hasIndicator = true;
      } else if (indicator === 'unusual_parameters' && this.hasUnusualParameters(context.parameters)) {
        hasIndicator = true;
      }
      
      if (hasIndicator) {
        indicatorCount++;
      }
    }

    return indicatorCount;
  }

  private hasUnusualParameters(parameters: Record<string, any>): boolean {
    // Check for unusual parameter combinations or values
    if (parameters.temperature && (parameters.temperature < 0 || parameters.temperature > 2)) {
      return true;
    }
    if (parameters.max_tokens && parameters.max_tokens > 4000) {
      return true;
    }
    return false;
  }

  private recordBehavioralIndicators(userId: string, indicators: string[]): void {
    const history = this.behavioralHistory.get(userId) || [];
    history.push({
      timestamp: new Date(),
      indicators
    });

    // Keep only recent history
    const cutoffTime = new Date(Date.now() - 24 * 60 * 60 * 1000); // 24 hours
    const recentHistory = history.filter(h => h.timestamp > cutoffTime);
    
    this.behavioralHistory.set(userId, recentHistory);
  }

  private calculateRiskTrend(timeWindow: number): 'INCREASING' | 'DECREASING' | 'STABLE' {
    const cutoffTime = Date.now() - timeWindow;
    const recentViolations = this.violations.filter(v => v.timestamp.getTime() > cutoffTime);
    
    if (recentViolations.length < 10) return 'STABLE';

    // Split into two halves and compare
    const midpoint = Math.floor(recentViolations.length / 2);
    const firstHalf = recentViolations.slice(0, midpoint);
    const secondHalf = recentViolations.slice(midpoint);

    const firstHalfScore = this.calculateViolationScore(firstHalf);
    const secondHalfScore = this.calculateViolationScore(secondHalf);

    const difference = secondHalfScore - firstHalfScore;
    
    if (difference > 0.2) return 'INCREASING';
    if (difference < -0.2) return 'DECREASING';
    return 'STABLE';
  }

  private calculateViolationScore(violations: SafetyViolation[]): number {
    const weights = { LOW: 1, MEDIUM: 2, HIGH: 3, CRITICAL: 4 };
    return violations.reduce((sum, v) => sum + weights[v.riskLevel], 0) / violations.length;
  }

  private generateSafetyRecommendations(violations: SafetyAssessment['violations'], context: SafetyContext): string[] {
    const recommendations: string[] = [];

    if (violations.some(v => v.policyType === 'RATE_LIMITING')) {
      recommendations.push('Consider implementing exponential backoff or request queuing');
    }

    if (violations.some(v => v.policyType === 'CONTENT_FILTERING')) {
      recommendations.push('Review and refine content filtering rules for better accuracy');
    }

    if (violations.some(v => v.policyType === 'PATTERN_DETECTION')) {
      recommendations.push('Monitor user behavior patterns and adjust thresholds if needed');
    }

    if (violations.some(v => v.severity === 'CRITICAL')) {
      recommendations.push('Immediate escalation required - review security protocols');
    }

    return recommendations;
  }

  private generateSystemRecommendations(
    violationsByType: Record<PolicyType, number>,
    violationsByRisk: Record<RiskLevel, number>
  ): string[] {
    const recommendations: string[] = [];

    if (violationsByType.RATE_LIMITING > 10) {
      recommendations.push('High rate limiting violations detected - consider adjusting limits or improving caching');
    }

    if (violationsByRisk.CRITICAL > 0) {
      recommendations.push('Critical safety violations detected - immediate security review recommended');
    }

    if (violationsByType.RESOURCE_USAGE > 5) {
      recommendations.push('Resource usage violations suggest need for capacity planning');
    }

    return recommendations;
  }

  private initializeDefaultPolicies(): void {
    // Default rate limits
    this.addRateLimit({
      id: 'global_rate_limit',
      name: 'Global Rate Limit',
      windowMs: 60 * 1000, // 1 minute
      maxRequests: 100,
      keyGenerator: (context) => context.userId || 'anonymous'
    });

    this.addRateLimit({
      id: 'per_operation_limit',
      name: 'Per Operation Limit',
      windowMs: 10 * 1000, // 10 seconds
      maxRequests: 10,
      keyGenerator: (context) => `${context.userId || 'anonymous'}_${context.operation}`
    });

    // Default content filters
    this.addContentFilter({
      id: 'harmful_content',
      name: 'Harmful Content Filter',
      patterns: [
        { pattern: /\b(hack|attack|exploit|vulnerability)\b/i, type: 'REGEX', severity: 'HIGH' },
        { pattern: 'malicious code', type: 'KEYWORD', severity: 'HIGH' }
      ],
      categories: [
        { category: 'harmful', threshold: 0.7, action: 'BLOCK' },
        { category: 'inappropriate', threshold: 0.8, action: 'FLAG' }
      ],
      enabled: true
    });

    // Default dangerous patterns
    this.addDangerousPattern({
      id: 'rapid_fire_requests',
      name: 'Rapid Fire Requests',
      description: 'Unusual high-frequency request pattern',
      pattern: {
        type: 'BEHAVIORAL',
        indicators: ['high_frequency', 'repeated_operation', 'short_intervals'],
        threshold: 2,
        timeWindow: 60 * 1000 // 1 minute
      },
      riskLevel: 'MEDIUM',
      response: {
        immediate: 'THROTTLE',
        notification: true
      },
      enabled: true
    });

    this.addDangerousPattern({
      id: 'system_exploitation',
      name: 'System Exploitation Attempt',
      description: 'Potential system exploitation or privilege escalation',
      pattern: {
        type: 'CONTENT',
        indicators: ['system', 'admin', 'root', 'escalate', 'bypass'],
        threshold: 3
      },
      riskLevel: 'CRITICAL',
      response: {
        immediate: 'BLOCK',
        escalation: 'security_team',
        notification: true
      },
      enabled: true
    });
  }
}
