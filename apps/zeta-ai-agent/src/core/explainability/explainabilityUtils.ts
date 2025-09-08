/**
 * Explainability Utilities
 * Helper functions and utilities for generating clear explanations
 */

import {
import AI from "AI";
import ANALYSIS from "ANALYSIS";
import AUDITOR from "AUDITOR";
import Add from "Add";
import Analyzed from "Analyzed";
import Audience from "Audience";
import Base from "Base";
import Based from "Based";
import CALCULATION from "CALCULATION";
import CONCLUSION from "CONCLUSION";
import COUNTERFACTUAL from "COUNTERFACTUAL";
import Calculate from "Calculate";
import Changes from "Changes";
import Check from "Check";
import Confidence from "Confidence";
import Contains from "Contains";
import Convert from "Convert";
import Counterfactual from "Counterfactual";
import Create from "Create";
import DATA from "DATA";
import DETAILED from "DETAILED";
import DEVELOPER from "DEVELOPER";
import Decision from "Decision";
import Default from "Default";
import Description from "Description";
import Direction from "Direction";
import Distribution from "Distribution";
import END_USER from "END_USER";
import EXPERT from "EXPERT";
import Ensure from "Ensure";
import Escape from "Escape";
import Evaluated from "Evaluated";
import Evidence from "Evidence";
import Examples from "Examples";
import Explainability from "Explainability";
import Explanation from "Explanation";
import ExplanationFormatter from "ExplanationFormatter";
import ExplanationHelpers from "ExplanationHelpers";
import ExplanationMetrics from "ExplanationMetrics";
import ExplanationValidator from "ExplanationValidator";
import FEATURE_IMPORTANCE from "FEATURE_IMPORTANCE";
import Feature from "Feature";
import Focus from "Focus";
import Format from "Format";
import Generate from "Generate";
import Generated from "Generated";
import HTML from "HTML";
import Helper from "Helper";
import ID from "ID";
import Impact from "Impact";
import Importance from "Importance";
import Important from "Important";
import Include from "Include";
import Inconsistent from "Inconsistent";
import Input from "Input";
import Insufficient from "Insufficient";
import Key from "Key";
import Level from "Level";
import Lower from "Lower";
import MARKDOWN from "MARKDOWN";
import Made from "Made";
import Markdown from "Markdown";
import Math from "Math";
import Note from "Note";
import Notes from "Notes";
import OBSERVATION from "OBSERVATION";
import Partial from "Partial";
import Points from "Points";
import Process from "Process";
import Provide from "Provide";
import REASONING_CHAIN from "REASONING_CHAIN";
import RESEARCHER from "RESEARCHER";
import RULE from "RULE";
import Reasoning from "Reasoning";
import Recommendations from "Recommendations";
import Record from "Record";
import RegExp from "RegExp";
import Reliability from "Reliability";
import Replace from "Replace";
import Shorten from "Shorten";
import Simplify from "Simplify";
import Step from "Step";
import Steps from "Steps";
import Summary from "Summary";
import TECHNICAL from "TECHNICAL";
import TEXT from "TEXT";
import This from "This";
import Timestamp from "Timestamp";
import Totals from "Totals";
import Type from "Type";
import Utilities from "Utilities";
import Validate from "Validate";
import Verify from "Verify";
import Would from "Would";
  DecisionContext,
  ExplanationAudience,
  ExplanationLevel,
  ExplanationRequest,
  ExplanationResult,
  ExplanationType,
  NaturalLanguageExplanation,
  ReasoningStep
} from './explainabilityEngine';

/**
 * Explanation formatting utilities
 */
export class ExplanationFormatter {
  /**
   * Format explanation for different output types
   */
  static formatExplanation(
    explanation: ExplanationResult,
    format: 'TEXT' | 'JSON' | 'HTML' | 'MARKDOWN' = 'TEXT'
  ): string {
    switch (format) {
    case 'JSON':
      return JSON.stringify(explanation, null, 2);
      
    case 'HTML':
      return this.formatAsHTML(explanation);
      
    case 'MARKDOWN':
      return this.formatAsMarkdown(explanation);
      
    case 'TEXT':
    default:
      return this.formatAsText(explanation);
    }
  }

  /**
   * Format as plain text
   */
  private static formatAsText(explanation: ExplanationResult): string {
    let text = '';
    
    text += `Decision Explanation\n`;
    text += `==================\n\n`;
    
    text += `Summary: ${explanation.summary.summary}\n\n`;
    
    if (explanation.summary.keyPoints.length > 0) {
      text += `Key Points:\n`;
      explanation.summary.keyPoints.forEach(point => {
        text += `• ${point}\n`;
      });
      text += '\n';
    }
    
    if (explanation.summary.reasoning.length > 0) {
      text += `Reasoning Steps:\n`;
      explanation.summary.reasoning.forEach((step, index) => {
        text += `${index + 1}. ${step}\n`;
      });
      text += '\n';
    }
    
    if (explanation.summary.caveats.length > 0) {
      text += `Important Notes:\n`;
      explanation.summary.caveats.forEach(caveat => {
        text += `⚠ ${caveat}\n`;
      });
      text += '\n';
    }
    
    text += `Confidence: ${explanation.summary.confidence}\n`;
    
    if (explanation.summary.recommendations && explanation.summary.recommendations.length > 0) {
      text += `\nRecommendations:\n`;
      explanation.summary.recommendations.forEach(rec => {
        text += `→ ${rec}\n`;
      });
    }
    
    return text;
  }

  /**
   * Format as HTML
   */
  private static formatAsHTML(explanation: ExplanationResult): string {
    let html = '';
    
    html += `<div class="explanation-result">\n`;
    html += `  <h1>Decision Explanation</h1>\n`;
    html += `  <div class="metadata">\n`;
    html += `    <span class="decision-id">ID: ${explanation.decisionId}</span>\n`;
    html += `    <span class="timestamp">${explanation.timestamp.toLocaleString()}</span>\n`;
    html += `    <span class="type">${explanation.type}</span>\n`;
    html += `    <span class="level">${explanation.level}</span>\n`;
    html += `  </div>\n\n`;
    
    html += `  <div class="summary">\n`;
    html += `    <h2>Summary</h2>\n`;
    html += `    <p>${this.escapeHtml(explanation.summary.summary)}</p>\n`;
    html += `  </div>\n\n`;
    
    if (explanation.summary.keyPoints.length > 0) {
      html += `  <div class="key-points">\n`;
      html += `    <h3>Key Points</h3>\n`;
      html += `    <ul>\n`;
      explanation.summary.keyPoints.forEach(point => {
        html += `      <li>${this.escapeHtml(point)}</li>\n`;
      });
      html += `    </ul>\n`;
      html += `  </div>\n\n`;
    }
    
    if (explanation.reasoningChain && explanation.reasoningChain.length > 0) {
      html += `  <div class="reasoning-chain">\n`;
      html += `    <h3>Reasoning Process</h3>\n`;
      html += `    <ol>\n`;
      explanation.reasoningChain.forEach(step => {
        html += `      <li>\n`;
        html += `        <strong>${step.type}:</strong> ${this.escapeHtml(step.description)}<br>\n`;
        html += `        <em>Reasoning:</em> ${this.escapeHtml(step.reasoning)}<br>\n`;
        html += `        <span class="confidence">Confidence: ${Math.round(step.confidence * 100)}%</span>\n`;
        html += `      </li>\n`;
      });
      html += `    </ol>\n`;
      html += `  </div>\n\n`;
    }
    
    if (explanation.featureImportance && explanation.featureImportance.length > 0) {
      html += `  <div class="feature-importance">\n`;
      html += `    <h3>Feature Importance</h3>\n`;
      html += `    <table>\n`;
      html += `      <thead>\n`;
      html += `        <tr><th>Feature</th><th>Importance</th><th>Direction</th><th>Explanation</th></tr>\n`;
      html += `      </thead>\n`;
      html += `      <tbody>\n`;
      explanation.featureImportance.forEach(feature => {
        html += `        <tr>\n`;
        html += `          <td>${this.escapeHtml(feature.feature)}</td>\n`;
        html += `          <td>${Math.round(feature.importance * 100)}%</td>\n`;
        html += `          <td>${feature.direction}</td>\n`;
        html += `          <td>${this.escapeHtml(feature.explanation)}</td>\n`;
        html += `        </tr>\n`;
      });
      html += `      </tbody>\n`;
      html += `    </table>\n`;
      html += `  </div>\n\n`;
    }
    
    if (explanation.summary.caveats.length > 0) {
      html += `  <div class="caveats">\n`;
      html += `    <h3>Important Notes</h3>\n`;
      html += `    <ul class="warning-list">\n`;
      explanation.summary.caveats.forEach(caveat => {
        html += `      <li class="warning">${this.escapeHtml(caveat)}</li>\n`;
      });
      html += `    </ul>\n`;
      html += `  </div>\n\n`;
    }
    
    html += `  <div class="confidence-section">\n`;
    html += `    <h3>Confidence Level</h3>\n`;
    html += `    <p>${this.escapeHtml(explanation.summary.confidence)}</p>\n`;
    html += `  </div>\n`;
    
    html += `</div>\n`;
    
    return html;
  }

  /**
   * Format as Markdown
   */
  private static formatAsMarkdown(explanation: ExplanationResult): string {
    let md = '';
    
    md += `# Decision Explanation\n\n`;
    md += `**Decision ID:** ${explanation.decisionId}  \n`;
    md += `**Timestamp:** ${explanation.timestamp.toISOString()}  \n`;
    md += `**Type:** ${explanation.type}  \n`;
    md += `**Level:** ${explanation.level}  \n`;
    md += `**Audience:** ${explanation.audience}  \n\n`;
    
    md += `## Summary\n\n`;
    md += `${explanation.summary.summary}\n\n`;
    
    if (explanation.summary.keyPoints.length > 0) {
      md += `## Key Points\n\n`;
      explanation.summary.keyPoints.forEach(point => {
        md += `- ${point}\n`;
      });
      md += '\n';
    }
    
    if (explanation.reasoningChain && explanation.reasoningChain.length > 0) {
      md += `## Reasoning Process\n\n`;
      explanation.reasoningChain.forEach((step, index) => {
        md += `### Step ${index + 1}: ${step.type}\n\n`;
        md += `**Description:** ${step.description}\n\n`;
        md += `**Reasoning:** ${step.reasoning}\n\n`;
        md += `**Confidence:** ${Math.round(step.confidence * 100)}%\n\n`;
        
        if (step.evidence.length > 0) {
          md += `**Evidence:**\n`;
          step.evidence.forEach(evidence => {
            md += `- ${evidence.type}: ${evidence.source} (Reliability: ${Math.round(evidence.reliability * 100)}%)\n`;
          });
          md += '\n';
        }
      });
    }
    
    if (explanation.featureImportance && explanation.featureImportance.length > 0) {
      md += `## Feature Importance\n\n`;
      md += `| Feature | Importance | Direction | Explanation |\n`;
      md += `|---------|------------|-----------|-------------|\n`;
      explanation.featureImportance.forEach(feature => {
        md += `| ${feature.feature} | ${Math.round(feature.importance * 100)}% | ${feature.direction} | ${feature.explanation} |\n`;
      });
      md += '\n';
    }
    
    if (explanation.counterfactuals && explanation.counterfactuals.length > 0) {
      md += `## Counterfactual Examples\n\n`;
      explanation.counterfactuals.forEach((cf, index) => {
        md += `### Counterfactual ${index + 1}\n\n`;
        md += `${cf.explanation}\n\n`;
        md += `**Changes:**\n`;
        cf.changes.forEach(change => {
          md += `- ${change.feature}: ${change.originalValue} → ${change.newValue} (Impact: ${Math.round(change.impact * 100)}%)\n`;
        });
        md += '\n';
      });
    }
    
    if (explanation.summary.caveats.length > 0) {
      md += `## ⚠️ Important Notes\n\n`;
      explanation.summary.caveats.forEach(caveat => {
        md += `> ${caveat}\n\n`;
      });
    }
    
    md += `## Confidence Level\n\n`;
    md += `${explanation.summary.confidence}\n\n`;
    
    if (explanation.summary.recommendations && explanation.summary.recommendations.length > 0) {
      md += `## Recommendations\n\n`;
      explanation.summary.recommendations.forEach(rec => {
        md += `- ${rec}\n`;
      });
    }
    
    return md;
  }

  /**
   * Escape HTML special characters
   */
  private static escapeHtml(text: string): string {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

/**
 * Explanation validation utilities
 */
export class ExplanationValidator {
  /**
   * Validate explanation completeness
   */
  static validateCompleteness(explanation: ExplanationResult): {
    score: number;
    missing: string[];
    recommendations: string[];
  } {
    const missing: string[] = [];
    const recommendations: string[] = [];
    let score = 100;

    // Check required fields
    if (!explanation.summary.summary) {
      missing.push('summary');
      score -= 30;
    }

    if (!explanation.summary.keyPoints || explanation.summary.keyPoints.length === 0) {
      missing.push('key points');
      recommendations.push('Add key decision points for better clarity');
      score -= 15;
    }

    if (!explanation.reasoningChain || explanation.reasoningChain.length === 0) {
      missing.push('reasoning chain');
      recommendations.push('Include step-by-step reasoning process');
      score -= 20;
    }

    if (!explanation.summary.confidence) {
      missing.push('confidence level');
      score -= 10;
    }

    // Check for depth based on level
    if (explanation.level === 'DETAILED' || explanation.level === 'TECHNICAL') {
      if (!explanation.featureImportance) {
        missing.push('feature importance');
        recommendations.push('Add feature importance analysis for technical audiences');
        score -= 15;
      }
    }

    if (explanation.level === 'EXPERT') {
      if (!explanation.causalFactors) {
        missing.push('causal analysis');
        recommendations.push('Include causal factor analysis for expert level');
        score -= 10;
      }
    }

    return {
      score: Math.max(0, score),
      missing,
      recommendations
    };
  }

  /**
   * Validate explanation accuracy
   */
  static validateAccuracy(
    explanation: ExplanationResult,
    context: DecisionContext
  ): {
    score: number;
    issues: string[];
    suggestions: string[];
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;

    // Check consistency between explanation and context
    if (explanation.decisionId !== context.decisionId) {
      issues.push('Decision ID mismatch');
      score -= 20;
    }

    // Check confidence consistency
    if (explanation.reasoningChain) {
      const avgStepConfidence = explanation.reasoningChain.reduce(
        (sum, step) => sum + step.confidence, 0
      ) / explanation.reasoningChain.length;

      if (Math.abs(avgStepConfidence - context.confidence) > 0.3) {
        issues.push('Inconsistent confidence between steps and final decision');
        suggestions.push('Ensure reasoning step confidence aligns with final decision confidence');
        score -= 15;
      }
    }

    // Check evidence reliability
    if (explanation.reasoningChain) {
      const lowReliabilityEvidence = explanation.reasoningChain
        .flatMap(step => step.evidence)
        .filter(evidence => evidence.reliability < 0.5);

      if (lowReliabilityEvidence.length > 0) {
        issues.push(`${lowReliabilityEvidence.length} pieces of low-reliability evidence`);
        suggestions.push('Verify and strengthen evidence sources');
        score -= 10;
      }
    }

    return {
      score: Math.max(0, score),
      issues,
      suggestions
    };
  }

  /**
   * Validate explanation clarity
   */
  static validateClarity(
    explanation: ExplanationResult,
    audience: ExplanationAudience
  ): {
    score: number;
    issues: string[];
    suggestions: string[];
  } {
    const issues: string[] = [];
    const suggestions: string[] = [];
    let score = 100;

    // Check summary length based on audience
    const summaryLength = explanation.summary.summary.length;
    const maxLengths = {
      END_USER: 200,
      DEVELOPER: 400,
      AUDITOR: 600,
      RESEARCHER: 800
    };

    if (summaryLength > maxLengths[audience]) {
      issues.push('Summary too long for target audience');
      suggestions.push(`Shorten summary to under ${maxLengths[audience]} characters`);
      score -= 15;
    }

    // Check for technical jargon for end users
    if (audience === 'END_USER') {
      const technicalTerms = [
        'algorithm', 'model', 'vector', 'matrix', 'neural', 'gradient',
        'optimization', 'hyperparameter', 'regularization', 'embedding'
      ];

      const foundTerms = technicalTerms.filter(term => 
        explanation.summary.summary.toLowerCase().includes(term)
      );

      if (foundTerms.length > 0) {
        issues.push('Contains technical jargon inappropriate for end users');
        suggestions.push('Replace technical terms with simpler language');
        score -= 20;
      }
    }

    // Check for sufficient detail for technical audiences
    if ((audience === 'DEVELOPER' || audience === 'RESEARCHER') && summaryLength < 100) {
      issues.push('Insufficient detail for technical audience');
      suggestions.push('Provide more technical details and specifics');
      score -= 15;
    }

    return {
      score: Math.max(0, score),
      issues,
      suggestions
    };
  }
}

/**
 * Explanation generation helpers
 */
export class ExplanationHelpers {
  /**
   * Create a simple decision context for testing
   */
  static createTestDecisionContext(overrides?: Partial<DecisionContext>): DecisionContext {
    return {
      decisionId: `test_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
      timestamp: new Date(),
      module: 'test-module',
      action: 'test-action',
      inputs: { param1: 'value1', param2: 42 },
      outputs: { result: 'success' },
      confidence: 0.85,
      executionTime: 150,
      resources: {
        memoryUsed: 1024 * 1024 * 50, // 50MB
        cpuTime: 100,
        networkCalls: 2
      },
      ...overrides
    };
  }

  /**
   * Create sample reasoning steps
   */
  static createSampleReasoningSteps(): ReasoningStep[] {
    return [
      {
        stepId: 'step_1',
        type: 'OBSERVATION',
        description: 'Analyzed input parameters',
        inputs: ['param1', 'param2'],
        outputs: ['analysis_result'],
        confidence: 0.9,
        reasoning: 'Input parameters are within expected ranges and format',
        evidence: [
          {
            type: 'DATA',
            source: 'input_validation',
            content: { valid: true, format: 'correct' },
            reliability: 0.95,
            relevance: 0.9,
            timestamp: new Date()
          }
        ],
        duration: 50
      },
      {
        stepId: 'step_2',
        type: 'ANALYSIS',
        description: 'Evaluated decision criteria',
        inputs: ['analysis_result'],
        outputs: ['decision_score'],
        confidence: 0.8,
        reasoning: 'Decision criteria evaluation shows positive indicators',
        evidence: [
          {
            type: 'CALCULATION',
            source: 'decision_engine',
            content: { score: 0.85, factors: ['factor1', 'factor2'] },
            reliability: 0.85,
            relevance: 0.95,
            timestamp: new Date()
          }
        ],
        duration: 75,
        alternatives: [
          {
            action: 'alternative-action',
            confidence: 0.6,
            reasoning: 'Lower confidence alternative',
            pros: ['simpler', 'faster'],
            cons: ['less accurate', 'limited scope'],
            risk: 0.4,
            feasibility: 0.8
          }
        ]
      },
      {
        stepId: 'step_3',
        type: 'CONCLUSION',
        description: 'Made final decision',
        inputs: ['decision_score'],
        outputs: ['final_decision'],
        confidence: 0.85,
        reasoning: 'Based on analysis, proceeding with primary action',
        evidence: [
          {
            type: 'RULE',
            source: 'decision_policy',
            content: { rule: 'proceed_if_score_above_threshold', threshold: 0.8 },
            reliability: 1.0,
            relevance: 1.0,
            timestamp: new Date()
          }
        ],
        duration: 25
      }
    ];
  }

  /**
   * Create explanation request templates
   */
  static createExplanationRequest(
    decisionId: string,
    type: ExplanationType[] = ['REASONING_CHAIN'],
    level: ExplanationLevel = 'DETAILED',
    audience: ExplanationAudience = 'DEVELOPER'
  ): ExplanationRequest {
    return {
      decisionId,
      type,
      level,
      audience,
      language: 'en',
      format: 'TEXT',
      includeVisuals: false,
      maxLength: 1000
    };
  }

  /**
   * Generate explanation summary statistics
   */
  static generateSummaryStatistics(explanations: ExplanationResult[]): {
    totalExplanations: number;
    averageGenerationTime: number;
    averageReliability: number;
    averageComplexity: number;
    typeDistribution: Record<ExplanationType, number>;
    levelDistribution: Record<ExplanationLevel, number>;
    audienceDistribution: Record<ExplanationAudience, number>;
    qualityScores: {
      averageCompleteness: number;
      averageAccuracy: number;
      averageClarity: number;
    };
  } {
    if (explanations.length === 0) {
      return {
        totalExplanations: 0,
        averageGenerationTime: 0,
        averageReliability: 0,
        averageComplexity: 0,
        typeDistribution: {} as Record<ExplanationType, number>,
        levelDistribution: {} as Record<ExplanationLevel, number>,
        audienceDistribution: {} as Record<ExplanationAudience, number>,
        qualityScores: {
          averageCompleteness: 0,
          averageAccuracy: 0,
          averageClarity: 0
        }
      };
    }

    const typeDistribution: Record<ExplanationType, number> = {} as any;
    const levelDistribution: Record<ExplanationLevel, number> = {} as any;
    const audienceDistribution: Record<ExplanationAudience, number> = {} as any;

    let totalGenerationTime = 0;
    let totalReliability = 0;
    let totalComplexity = 0;

    explanations.forEach(explanation => {
      // Distribution counts
      typeDistribution[explanation.type] = (typeDistribution[explanation.type] || 0) + 1;
      levelDistribution[explanation.level] = (levelDistribution[explanation.level] || 0) + 1;
      audienceDistribution[explanation.audience] = (audienceDistribution[explanation.audience] || 0) + 1;

      // Totals for averages
      totalGenerationTime += explanation.metadata.generationTime;
      totalReliability += explanation.metadata.reliability;
      totalComplexity += explanation.metadata.complexity;
    });

    return {
      totalExplanations: explanations.length,
      averageGenerationTime: totalGenerationTime / explanations.length,
      averageReliability: totalReliability / explanations.length,
      averageComplexity: totalComplexity / explanations.length,
      typeDistribution,
      levelDistribution,
      audienceDistribution,
      qualityScores: {
        averageCompleteness: 0.85, // Would calculate from validation
        averageAccuracy: 0.90,     // Would calculate from validation
        averageClarity: 0.80       // Would calculate from validation
      }
    };
  }

  /**
   * Convert explanation to different audiences
   */
  static adaptExplanationForAudience(
    explanation: NaturalLanguageExplanation,
    targetAudience: ExplanationAudience
  ): NaturalLanguageExplanation {
    const adapted = { ...explanation };

    switch (targetAudience) {
    case 'END_USER':
      // Simplify language and remove technical details
      adapted.summary = this.simplifyLanguage(explanation.summary);
      adapted.detailed = this.simplifyLanguage(explanation.detailed);
      adapted.reasoning = explanation.reasoning.map(r => this.simplifyLanguage(r));
      break;

    case 'DEVELOPER':
      // Add technical context but keep it accessible
      adapted.summary = this.addTechnicalContext(explanation.summary);
      break;

    case 'AUDITOR':
      // Focus on compliance and validation aspects
      adapted.caveats = [...explanation.caveats, 'Ensure compliance with applicable regulations'];
      break;

    case 'RESEARCHER':
      // Add methodological details
      adapted.detailed += '\n\nMethodological Note: This explanation was generated using automated reasoning analysis with confidence scoring.';
      break;
    }

    return adapted;
  }

  private static simplifyLanguage(text: string): string {
    const replacements: Record<string, string> = {
      'algorithm': 'method',
      'optimization': 'improvement',
      'parameter': 'setting',
      'vector': 'data point',
      'matrix': 'data table',
      'neural network': 'AI system',
      'machine learning': 'AI learning',
      'confidence score': 'certainty level',
      'threshold': 'limit'
    };

    let simplified = text;
    Object.entries(replacements).forEach(([technical, simple]) => {
      simplified = simplified.replace(new RegExp(technical, 'gi'), simple);
    });

    return simplified;
  }

  private static addTechnicalContext(text: string): string {
    return text + ' (Generated via automated explanation engine with multi-step reasoning analysis)';
  }
}

/**
 * Explanation quality metrics
 */
export class ExplanationMetrics {
  /**
   * Calculate explanation quality score
   */
  static calculateQualityScore(
    explanation: ExplanationResult,
    context?: DecisionContext
  ): {
    overallScore: number;
    componentScores: {
      completeness: number;
      accuracy: number;
      clarity: number;
      relevance: number;
      consistency: number;
    };
    feedback: string[];
  } {
    const completeness = ExplanationValidator.validateCompleteness(explanation);
    let accuracy: { score: number; issues: string[]; suggestions: string[] } = { score: 85, issues: [], suggestions: [] }; // Default if no context
    if (context) {
      accuracy = ExplanationValidator.validateAccuracy(explanation, context);
    }
    const clarity = ExplanationValidator.validateClarity(explanation, explanation.audience);

    // Calculate relevance (simplified)
    const relevance = this.calculateRelevance(explanation);

    // Calculate consistency (simplified)
    const consistency = this.calculateConsistency(explanation);

    const componentScores = {
      completeness: completeness.score,
      accuracy: accuracy.score,
      clarity: clarity.score,
      relevance,
      consistency
    };

    const overallScore = Object.values(componentScores).reduce((sum, score) => sum + score, 0) / 5;

    const feedback: string[] = [
      ...completeness.recommendations,
      ...accuracy.suggestions,
      ...clarity.suggestions
    ];

    return {
      overallScore,
      componentScores,
      feedback
    };
  }

  private static calculateRelevance(explanation: ExplanationResult): number {
    let relevanceScore = 70; // Base score

    // Check if explanation has relevant components for the type
    if (explanation.type === 'REASONING_CHAIN' && explanation.reasoningChain) {
      relevanceScore += 15;
    }

    if (explanation.type === 'FEATURE_IMPORTANCE' && explanation.featureImportance) {
      relevanceScore += 15;
    }

    if (explanation.type === 'COUNTERFACTUAL' && explanation.counterfactuals) {
      relevanceScore += 15;
    }

    return Math.min(100, relevanceScore);
  }

  private static calculateConsistency(explanation: ExplanationResult): number {
    let consistencyScore = 80; // Base score

    // Check for consistency between summary and detailed explanation
    if (explanation.summary.summary && explanation.summary.detailed) {
      const summaryWords = explanation.summary.summary.toLowerCase().split(' ');
      const detailedWords = explanation.summary.detailed.toLowerCase().split(' ');
      
      const overlap = summaryWords.filter(word => detailedWords.includes(word)).length;
      const overlapRatio = overlap / summaryWords.length;
      
      if (overlapRatio > 0.3) {
        consistencyScore += 10;
      } else {
        consistencyScore -= 10;
      }
    }

    // Check reasoning step consistency
    if (explanation.reasoningChain && explanation.reasoningChain.length > 1) {
      const confidenceVariation = this.calculateConfidenceVariation(explanation.reasoningChain);
      if (confidenceVariation < 0.2) {
        consistencyScore += 10;
      } else {
        consistencyScore -= 5;
      }
    }

    return Math.min(100, Math.max(0, consistencyScore));
  }

  private static calculateConfidenceVariation(steps: ReasoningStep[]): number {
    const confidences = steps.map(step => step.confidence);
    const mean = confidences.reduce((sum, conf) => sum + conf, 0) / confidences.length;
    const variance = confidences.reduce((sum, conf) => sum + Math.pow(conf - mean, 2), 0) / confidences.length;
    return Math.sqrt(variance);
  }
}
