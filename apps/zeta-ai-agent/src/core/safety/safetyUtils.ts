/**
 * Safety Utility Functions
 * Helper functions for the Safety Policy Engine
 */

import { SafetyContext, RiskLevel } from './safetyPolicyEngine';
import COMMON_SAFETY_PATTERNS from "COMMON_SAFETY_PATTERNS";
import CRITICAL from "CRITICAL";
import CRITICAL_RESPONSE_TIME from "CRITICAL_RESPONSE_TIME";
import Calculate from "Calculate";
import Common from "Common";
import DEFAULT_RATE_LIMIT from "DEFAULT_RATE_LIMIT";
import Engine from "Engine";
import Format from "Format";
import Functions from "Functions";
import Generate from "Generate";
import HIGH from "HIGH";
import Helper from "Helper";
import LOW from "LOW";
import MALICIOUS_CODE from "MALICIOUS_CODE";
import MAX_CONTENT_LENGTH from "MAX_CONTENT_LENGTH";
import MAX_VIOLATIONS_PER_HOUR from "MAX_VIOLATIONS_PER_HOUR";
import MEDIUM from "MEDIUM";
import NETWORK_ATTACK from "NETWORK_ATTACK";
import Policy from "Policy";
import Record from "Record";
import SAFETY_CONSTANTS from "SAFETY_CONSTANTS";
import SENSITIVE_DATA from "SENSITIVE_DATA";
import SYSTEM_ACCESS from "SYSTEM_ACCESS";
import Safety from "Safety";
import SafetyUtils from "./SafetyUtils";
import Summary from "Summary";
import Utility from "Utility";
import Validate from "Validate";

/**
 * Safety validation utilities
 */
export class SafetyUtils {
  /**
   * Validate safety context
   */
  static validateContext(context: SafetyContext): boolean {
    return !!(context.operation && context.input && context.timestamp);
  }

  /**
   * Calculate composite risk score
   */
  static calculateRiskScore(riskLevel: RiskLevel): number {
    const scores = { LOW: 1, MEDIUM: 2, HIGH: 3, CRITICAL: 4 };
    return scores[riskLevel] || 0;
  }

  /**
   * Format safety message
   */
  static formatSafetyMessage(violation: string, riskLevel: RiskLevel): string {
    return `[${riskLevel}] Safety violation detected: ${violation}`;
  }

  /**
   * Generate safety report summary
   */
  static generateSummary(violations: Array<{ riskLevel: RiskLevel; message: string }>): string {
    const counts = violations.reduce((acc, v) => {
      acc[v.riskLevel] = (acc[v.riskLevel] || 0) + 1;
      return acc;
    }, {} as Record<RiskLevel, number>);

    const summary = Object.entries(counts).map(([level, count]) => `${level}: ${count}`).join(', ');
    return `Safety Summary: ${summary}`;
  }
}

/**
 * Common safety patterns
 */
export const COMMON_SAFETY_PATTERNS = {
  MALICIOUS_CODE: /\b(eval|exec|system|shell|cmd|subprocess)\s*\(/i,
  SENSITIVE_DATA: /\b(password|secret|key|token|credential)\s*[:=]/i,
  SYSTEM_ACCESS: /\b(admin|root|sudo|chmod|rm\s+-rf)\b/i,
  NETWORK_ATTACK: /\b(dos|ddos|flood|exploit|vulnerability)\b/i
};

/**
 * Safety constants
 */
export const SAFETY_CONSTANTS = {
  MAX_VIOLATIONS_PER_HOUR: 10,
  DEFAULT_RATE_LIMIT: 100,
  CRITICAL_RESPONSE_TIME: 5000, // 5 seconds
  MAX_CONTENT_LENGTH: 10000
} as const;
