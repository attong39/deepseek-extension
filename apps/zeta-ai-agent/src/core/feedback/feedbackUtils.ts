/**
 * Human Feedback Loop Utilities
 * Helper functions and tools for working with human feedback
 */

import { 
import A from "A";
import ACTIVE from "ACTIVE";
import AI_DECIDES from "AI_DECIDES";
import Achieved from "Achieved";
import Active from "Active";
import Address from "Address";
import Adjust from "Adjust";
import Aggregate from "Aggregate";
import Analyze from "Analyze";
import B from "B";
import BATCH_LEARNING from "BATCH_LEARNING";
import Build from "Build";
import COLLABORATIVE from "COLLABORATIVE";
import COMPREHENSIVE from "COMPREHENSIVE";
import CONSENSUS from "CONSENSUS";
import CONTINUOUS from "CONTINUOUS";
import Calculate from "Calculate";
import Cannot from "Cannot";
import Check from "Check";
import Collaboration from "Collaboration";
import CollaborationPatternGenerator from "CollaborationPatternGenerator";
import Collect from "Collect";
import Confidence from "Confidence";
import Consider from "Consider";
import Context from "../../../../desktop/src/Context/index";
import Convert from "Convert";
import Create from "Create";
import DECLINING from "DECLINING";
import DETAILED from "DETAILED";
import Default from "Default";
import Demonstration from "Demonstration";
import Determine from "Determine";
import EXPERT from "EXPERT";
import EXPLANATION from "EXPLANATION";
import Earlier from "Earlier";
import Error from "Error";
import Example from "Example";
import Expected from "Expected";
import Extended from "Extended";
import Extract from "Extract";
import Feedback from "Feedback";
import FeedbackAnalyzer from "FeedbackAnalyzer";
import FeedbackBuilder from "FeedbackBuilder";
import FeedbackCollector from "FeedbackCollector";
import FeedbackTestUtils from "FeedbackTestUtils";
import Focus from "Focus";
import Found from "Found";
import Generate from "Generate";
import Good from "Good";
import HIGH from "HIGH";
import HUMAN from "HUMAN";
import HUMAN_DECIDES from "HUMAN_DECIDES";
import Helper from "Helper";
import High from "High";
import Human from "Human";
import IMPROVING from "IMPROVING";
import INTERMEDIATE from "INTERMEDIATE";
import Identify from "Identify";
import Improve from "Improve";
import Increase from "Increase";
import Inferred from "Inferred";
import Insufficient from "Insufficient";
import LOW from "LOW";
import Learn from "Learn";
import Learning from "Learning";
import LearningSessionUtils from "LearningSessionUtils";
import Limit from "Limit";
import Limited from "Limited";
import Long from "Long";
import Loop from "Loop";
import Low from "Low";
import MEDIUM from "MEDIUM";
import MILESTONE from "MILESTONE";
import MINIMAL from "MINIMAL";
import Map from "Map";
import Math from "Math";
import Meeting from "Meeting";
import Merge from "Merge";
import Minimum from "Minimum";
import More from "More";
import NEUTRAL from "NEUTRAL";
import NOVICE from "NOVICE";
import Normalize from "Normalize";
import ON_DEMAND from "ON_DEMAND";
import Omit from "Omit";
import Outcome from "Outcome";
import PASSIVE from "PASSIVE";
import PERIODIC from "PERIODIC";
import PREFERENCE from "PREFERENCE";
import Partial from "Partial";
import Pattern from "Pattern";
import Preference from "Preference";
import PreferenceModelUtils from "PreferenceModelUtils";
import Query from "Query";
import QueryGenerator from "QueryGenerator";
import QueryOmitFields from "QueryOmitFields";
import Quick from "Quick";
import RATING from "RATING";
import Rapid from "Rapid";
import Record from "Record";
import Repeated from "Repeated";
import STABLE from "STABLE";
import STANDARD from "STANDARD";
import Set from "Set";
import Significant from "Significant";
import Strength from "Strength";
import UNCERTAIN from "UNCERTAIN";
import Use from "Use";
import Utilities from "Utilities";
import VALIDATION from "VALIDATION";
import Validate from "Validate";
  HumanFeedback, 
  FeedbackType, 
  FeedbackQuality, 
  CollaborationPattern,
  ActiveLearningQuery,
  PreferenceModel,
  LearningSession,
  EffortLevel,
  ExpertiseLevel,
  InteractionMode,
  ComplexityLevel,
  StakesLevel
} from './humanFeedbackLoop';

/**
 * Query omit type for reuse
 */
type QueryOmitFields = 'id' | 'timestamp' | 'status';

/**
 * Feedback builder for easy feedback creation
 */
export class FeedbackBuilder {
  private readonly feedback: Partial<HumanFeedback['feedback']> = {};
  private readonly metadata: Partial<HumanFeedback['metadata']> = {};
  private context: Partial<HumanFeedback['context']> = {};

  /**
   * Set preference feedback
   */
  setPreference(preference: 'A' | 'B' | 'NEUTRAL', explanation?: string): this {
    this.feedback.preference = preference;
    if (explanation) {
      this.feedback.explanation = explanation;
    }
    return this;
  }

  /**
   * Set rating feedback
   */
  setRating(rating: number, explanation?: string): this {
    this.feedback.rating = Math.max(1, Math.min(10, rating));
    if (explanation) {
      this.feedback.explanation = explanation;
    }
    return this;
  }

  /**
   * Set binary feedback
   */
  setBinary(value: boolean, explanation?: string): this {
    this.feedback.binary = value;
    if (explanation) {
      this.feedback.explanation = explanation;
    }
    return this;
  }

  /**
   * Set correction feedback
   */
  setCorrection(incorrect: string, correct: string, explanation?: string): this {
    this.feedback.correction = {
      incorrect,
      correct,
      explanation
    };
    return this;
  }

  /**
   * Set ranking feedback
   */
  setRanking(ranking: string[], explanation?: string): this {
    this.feedback.ranking = ranking;
    if (explanation) {
      this.feedback.explanation = explanation;
    }
    return this;
  }

  /**
   * Set demonstration feedback
   */
  setDemonstration(steps: Array<{
    action: string;
    reasoning: string;
    expected_outcome: string;
  }>): this {
    this.feedback.demonstration = { steps };
    return this;
  }

  /**
   * Set critique feedback
   */
  setCritique(
    aspects: Array<{
      aspect: string;
      score: number;
      comment: string;
    }>,
    overall_comment: string
  ): this {
    this.feedback.critique = {
      aspects,
      overall_comment
    };
    return this;
  }

  /**
   * Set human confidence
   */
  setConfidence(confidence: number): this {
    this.metadata.confidence = Math.max(0, Math.min(1, confidence));
    return this;
  }

  /**
   * Set effort level
   */
  setEffortLevel(effort: EffortLevel): this {
    this.metadata.effort_level = effort;
    return this;
  }

  /**
   * Set expertise level
   */
  setExpertiseLevel(expertise: ExpertiseLevel): this {
    this.metadata.expertise_level = expertise;
    return this;
  }

  /**
   * Set time spent
   */
  setTimeSpent(milliseconds: number): this {
    this.metadata.time_spent = milliseconds;
    return this;
  }

  /**
   * Set interaction mode
   */
  setInteractionMode(mode: InteractionMode): this {
    this.metadata.interaction_mode = mode;
    return this;
  }

  /**
   * Set task context
   */
  setContext(
    agentAction: string,
    environmentState: Record<string, any>,
    decisionPoint: string,
    options?: {
      taskId?: string;
      sessionId?: string;
      userId?: string;
      alternatives?: string[];
    }
  ): this {
    this.context = {
      agentAction,
      environmentState,
      decisionPoint,
      ...options
    };
    return this;
  }

  /**
   * Build the feedback data
   */
  build(): {
    context: HumanFeedback['context'];
    feedback: HumanFeedback['feedback'];
    metadata: HumanFeedback['metadata'];
    } {
    // Validate required fields
    if (!this.context.agentAction || !this.context.environmentState || !this.context.decisionPoint) {
      throw new Error('Context must include agentAction, environmentState, and decisionPoint');
    }

    // Set defaults
    const metadata: HumanFeedback['metadata'] = {
      confidence: this.metadata.confidence ?? 0.7,
      effort_level: this.metadata.effort_level ?? 'MEDIUM',
      expertise_level: this.metadata.expertise_level ?? 'INTERMEDIATE',
      time_spent: this.metadata.time_spent ?? 0,
      interaction_mode: this.metadata.interaction_mode ?? 'ACTIVE'
    };

    return {
      context: this.context as HumanFeedback['context'],
      feedback: this.feedback,
      metadata
    };
  }
}

/**
 * Feedback analyzer for extracting insights
 */
export class FeedbackAnalyzer {
  /**
   * Analyze feedback patterns
   */
  static analyzeFeedbackPatterns(feedback_list: HumanFeedback[]): {
    common_issues: Array<{
      issue: string;
      frequency: number;
      severity: number;
      examples: string[];
    }>;
    user_preferences: Array<{
      preference: string;
      strength: number;
      consistency: number;
    }>;
    learning_opportunities: Array<{
      opportunity: string;
      potential_impact: number;
      difficulty: number;
    }>;
    quality_metrics: {
      average_quality: number;
      quality_trend: 'IMPROVING' | 'STABLE' | 'DECLINING';
      confidence_distribution: Record<string, number>;
    };
  } {
    const common_issues = FeedbackAnalyzer.extractCommonIssues(feedback_list);
    const user_preferences = FeedbackAnalyzer.extractUserPreferences(feedback_list);
    const learning_opportunities = FeedbackAnalyzer.identifyLearningOpportunities(feedback_list);
    const quality_metrics = FeedbackAnalyzer.calculateQualityMetrics(feedback_list);

    return {
      common_issues,
      user_preferences,
      learning_opportunities,
      quality_metrics
    };
  }

  /**
   * Extract common issues from feedback
   */
  private static extractCommonIssues(feedback_list: HumanFeedback[]) {
    const issues = new Map<string, { count: number; severity: number; examples: string[] }>();

    for (const feedback of feedback_list) {
      if (feedback.feedback.correction) {
        const issue = feedback.feedback.correction.incorrect;
        const current = issues.get(issue) || { count: 0, severity: 0, examples: [] };
        current.count++;
        current.severity += (feedback.feedback.rating && feedback.feedback.rating < 5) ? 2 : 1;
        current.examples.push(feedback.id);
        issues.set(issue, current);
      }

      if (feedback.feedback.rating && feedback.feedback.rating < 4) {
        const issue = feedback.context.agentAction;
        const current = issues.get(issue) || { count: 0, severity: 0, examples: [] };
        current.count++;
        current.severity += 10 - feedback.feedback.rating;
        current.examples.push(feedback.id);
        issues.set(issue, current);
      }
    }

    return Array.from(issues.entries()).map(([issue, data]) => ({
      issue,
      frequency: data.count,
      severity: data.severity / data.count,
      examples: data.examples.slice(0, 5) // Limit examples
    })).sort((a, b) => (b.frequency * b.severity) - (a.frequency * a.severity));
  }

  /**
   * Extract user preferences
   */
  private static extractUserPreferences(feedback_list: HumanFeedback[]) {
    const preferences = new Map<string, { positive: number; negative: number; total: number }>();

    for (const feedback of feedback_list) {
      const action = feedback.context.agentAction;
      const current = preferences.get(action) || { positive: 0, negative: 0, total: 0 };
      current.total++;

      FeedbackAnalyzer.updatePreferenceScores(feedback, current);
      preferences.set(action, current);
    }

    return FeedbackAnalyzer.filterAndSortPreferences(preferences);
  }

  private static updatePreferenceScores(
    feedback: HumanFeedback, 
    current: { positive: number; negative: number; total: number }
  ): void {
    if (feedback.feedback.rating) {
      if (feedback.feedback.rating >= 7) current.positive++;
      else if (feedback.feedback.rating <= 4) current.negative++;
    }

    if (feedback.feedback.binary !== undefined) {
      if (feedback.feedback.binary) current.positive++;
      else current.negative++;
    }

    if (feedback.feedback.preference === 'A') current.positive++;
    else if (feedback.feedback.preference === 'B') current.negative++;
  }

  private static filterAndSortPreferences(
    preferences: Map<string, { positive: number; negative: number; total: number }>
  ) {
    return Array.from(preferences.entries())
      .filter(([, data]) => data.total >= 3) // Minimum sample size
      .map(([preference, data]) => ({
        preference,
        strength: (data.positive - data.negative) / data.total,
        consistency: Math.abs(data.positive - data.negative) / data.total
      }))
      .sort((a, b) => b.strength - a.strength);
  }

  /**
   * Identify learning opportunities
   */
  private static identifyLearningOpportunities(feedback_list: HumanFeedback[]) {
    const opportunities: Array<{
      opportunity: string;
      potential_impact: number;
      difficulty: number;
    }> = [];

    // High-correction areas
    const corrections = feedback_list.filter(f => f.feedback.correction);
    if (corrections.length > 0) {
      opportunities.push({
        opportunity: 'Improve reasoning in corrected areas',
        potential_impact: 0.8,
        difficulty: 0.6
      });
    }

    // Low-rated actions
    const low_rated = feedback_list.filter(f => f.feedback.rating && f.feedback.rating < 5);
    if (low_rated.length > 0) {
      opportunities.push({
        opportunity: 'Address consistently low-rated actions',
        potential_impact: 0.7,
        difficulty: 0.5
      });
    }

    // Demonstration learning
    const demonstrations = feedback_list.filter(f => f.feedback.demonstration);
    if (demonstrations.length > 0) {
      opportunities.push({
        opportunity: 'Learn from human demonstrations',
        potential_impact: 0.9,
        difficulty: 0.7
      });
    }

    return opportunities.sort((a, b) => (b.potential_impact / b.difficulty) - (a.potential_impact / a.difficulty));
  }

  /**
   * Calculate quality metrics
   */
  private static calculateQualityMetrics(feedback_list: HumanFeedback[]) {
    if (feedback_list.length === 0) {
      return {
        average_quality: 0,
        quality_trend: 'STABLE' as const,
        confidence_distribution: {}
      };
    }

    const quality_scores = feedback_list.map(f => FeedbackAnalyzer.qualityToScore(f.quality));
    const average_quality = quality_scores.reduce((sum, score) => sum + score, 0) / quality_scores.length;

    // Calculate trend (compare first half vs second half)
    let quality_trend: 'IMPROVING' | 'STABLE' | 'DECLINING' = 'STABLE';
    if (feedback_list.length >= 10) {
      const mid = Math.floor(feedback_list.length / 2);
      const first_half = quality_scores.slice(0, mid);
      const second_half = quality_scores.slice(mid);
      
      const first_avg = first_half.reduce((sum, score) => sum + score, 0) / first_half.length;
      const second_avg = second_half.reduce((sum, score) => sum + score, 0) / second_half.length;
      
      if (second_avg > first_avg + 0.1) quality_trend = 'IMPROVING';
      else if (second_avg < first_avg - 0.1) quality_trend = 'DECLINING';
    }

    // Confidence distribution
    const confidence_buckets = { low: 0, medium: 0, high: 0 };
    for (const feedback of feedback_list) {
      if (feedback.metadata.confidence < 0.4) confidence_buckets.low++;
      else if (feedback.metadata.confidence < 0.7) confidence_buckets.medium++;
      else confidence_buckets.high++;
    }

    return {
      average_quality,
      quality_trend,
      confidence_distribution: confidence_buckets
    };
  }

  private static qualityToScore(quality: FeedbackQuality): number {
    const scores = { HIGH: 1.0, MEDIUM: 0.7, LOW: 0.4, UNCERTAIN: 0.2 };
    return scores[quality];
  }
}

/**
 * Collaboration pattern generator
 */
export class CollaborationPatternGenerator {
  /**
   * Generate collaboration pattern based on task characteristics
   */
  static generatePattern(
    task_type: string,
    complexity: ComplexityLevel,
    uncertainty: ComplexityLevel,
    stakes: StakesLevel,
    domain_expertise?: ExpertiseLevel
  ): CollaborationPattern {
    const pattern_id = `pattern_${task_type}_${complexity}_${uncertainty}_${stakes}`;
    
    // Calculate autonomy levels
    const autonomy_levels = CollaborationPatternGenerator.calculateAutonomyLevels(
      complexity, uncertainty, stakes, domain_expertise
    );

    // Determine pattern characteristics
    const pattern_characteristics = CollaborationPatternGenerator.determinePatternCharacteristics(
      stakes, uncertainty, complexity, autonomy_levels.ai_autonomy
    );

    return {
      id: pattern_id,
      name: `${task_type} Pattern (${complexity}/${uncertainty}/${stakes})`,
      description: `Collaboration pattern for ${task_type} tasks with ${complexity} complexity, ${uncertainty} uncertainty, and ${stakes} stakes`,
      context: {
        task_type,
        complexity_level: complexity,
        uncertainty_level: uncertainty,
        stakes
      },
      pattern: {
        ai_autonomy_level: autonomy_levels.ai_autonomy,
        human_involvement_level: autonomy_levels.human_involvement,
        ...pattern_characteristics
      },
      effectiveness_score: 0.7, // Default starting score
      usage_count: 0,
      last_used: new Date()
    };
  }

  private static calculateAutonomyLevels(
    complexity: ComplexityLevel,
    uncertainty: ComplexityLevel,
    stakes: StakesLevel,
    domain_expertise?: ExpertiseLevel
  ) {
    let ai_autonomy = 0.5;

    // Adjust for complexity
    if (complexity === 'LOW') ai_autonomy += 0.2;
    else if (complexity === 'HIGH') ai_autonomy -= 0.2;

    // Adjust for uncertainty
    if (uncertainty === 'LOW') ai_autonomy += 0.1;
    else if (uncertainty === 'HIGH') ai_autonomy -= 0.3;

    // Adjust for stakes
    if (stakes === 'LOW') ai_autonomy += 0.1;
    else if (stakes === 'HIGH') ai_autonomy -= 0.4;

    // Normalize values
    ai_autonomy = Math.max(0, Math.min(1, ai_autonomy));
    let human_involvement = 1 - ai_autonomy + 0.3;

    // Adjust for domain expertise (but don't reassign if already calculated)
    if (domain_expertise === 'EXPERT') {
      human_involvement = Math.min(1, human_involvement + 0.2);
    } else if (domain_expertise === 'NOVICE') {
      human_involvement = Math.max(0, human_involvement - 0.1);
    }

    human_involvement = Math.max(0, Math.min(1, human_involvement));

    return { ai_autonomy, human_involvement };
  }

  private static determinePatternCharacteristics(
    stakes: StakesLevel,
    uncertainty: ComplexityLevel,
    complexity: ComplexityLevel,
    ai_autonomy: number
  ): {
    feedback_frequency: 'CONTINUOUS' | 'PERIODIC' | 'ON_DEMAND' | 'MILESTONE';
    decision_authority: 'AI_DECIDES' | 'HUMAN_DECIDES' | 'COLLABORATIVE' | 'CONSENSUS';
    explanation_detail: 'MINIMAL' | 'STANDARD' | 'DETAILED' | 'COMPREHENSIVE';
  } {
    // Determine feedback frequency
    let feedback_frequency: 'CONTINUOUS' | 'PERIODIC' | 'ON_DEMAND' | 'MILESTONE';
    if (stakes === 'HIGH') {
      feedback_frequency = 'CONTINUOUS';
    } else if (stakes === 'MEDIUM') {
      feedback_frequency = 'PERIODIC';
    } else {
      feedback_frequency = 'ON_DEMAND';
    }

    // Determine decision authority
    let decision_authority: 'AI_DECIDES' | 'HUMAN_DECIDES' | 'COLLABORATIVE' | 'CONSENSUS';
    if (ai_autonomy > 0.7) {
      decision_authority = 'AI_DECIDES';
    } else if (ai_autonomy < 0.3) {
      decision_authority = 'HUMAN_DECIDES';
    } else {
      decision_authority = 'COLLABORATIVE';
    }

    // Determine explanation detail
    let explanation_detail: 'MINIMAL' | 'STANDARD' | 'DETAILED' | 'COMPREHENSIVE';
    if (stakes === 'HIGH') {
      explanation_detail = 'COMPREHENSIVE';
    } else if (uncertainty === 'HIGH') {
      explanation_detail = 'DETAILED';
    } else if (complexity === 'HIGH') {
      explanation_detail = 'STANDARD';
    } else {
      explanation_detail = 'MINIMAL';
    }

    return {
      feedback_frequency,
      decision_authority,
      explanation_detail
    };
  }
}

/**
 * Active learning query generator
 */
export class QueryGenerator {
  /**
   * Generate preference query
   */
  static createPreferenceQuery(
    context: string,
    optionA: { action: string; description: string; confidence: number },
    optionB: { action: string; description: string; confidence: number }
  ): Omit<ActiveLearningQuery, QueryOmitFields> {
    return {
      context,
      query_type: 'PREFERENCE',
      priority: 1 - Math.min(optionA.confidence, optionB.confidence),
      alternatives: [
        {
          id: 'A',
          action: optionA.action,
          description: optionA.description,
          ai_confidence: optionA.confidence,
          expected_outcome: 'Outcome A'
        },
        {
          id: 'B',
          action: optionB.action,
          description: optionB.description,
          ai_confidence: optionB.confidence,
          expected_outcome: 'Outcome B'
        }
      ],
      uncertainty_metrics: {
        epistemic_uncertainty: 1 - Math.max(optionA.confidence, optionB.confidence),
        aleatoric_uncertainty: Math.abs(optionA.confidence - optionB.confidence),
        total_uncertainty: 1 - Math.min(optionA.confidence, optionB.confidence)
      },
      expected_information_gain: Math.abs(optionA.confidence - optionB.confidence),
      cost_estimate: 1.0,
      deadline: new Date(Date.now() + 24 * 60 * 60 * 1000)
    };
  }

  /**
   * Generate validation query
   */
  static createValidationQuery(
    context: string,
    action: string,
    description: string,
    confidence: number
  ): Omit<ActiveLearningQuery, QueryOmitFields> {
    return {
      context,
      query_type: 'VALIDATION',
      priority: 1 - confidence,
      alternatives: [
        {
          id: 'proposed',
          action,
          description,
          ai_confidence: confidence,
          expected_outcome: 'Expected outcome of proposed action'
        }
      ],
      uncertainty_metrics: {
        epistemic_uncertainty: 1 - confidence,
        aleatoric_uncertainty: 0.1,
        total_uncertainty: 1 - confidence + 0.1
      },
      expected_information_gain: 1 - confidence,
      cost_estimate: 0.5,
      deadline: new Date(Date.now() + 12 * 60 * 60 * 1000)
    };
  }

  /**
   * Generate explanation request
   */
  static createExplanationQuery(
    context: string,
    action: string,
    reasoning: string
  ): Omit<ActiveLearningQuery, QueryOmitFields> {
    return {
      context,
      query_type: 'EXPLANATION',
      priority: 0.7,
      alternatives: [
        {
          id: 'reasoning',
          action,
          description: reasoning,
          ai_confidence: 0.8,
          expected_outcome: 'Human feedback on reasoning quality'
        }
      ],
      uncertainty_metrics: {
        epistemic_uncertainty: 0.3,
        aleatoric_uncertainty: 0.2,
        total_uncertainty: 0.5
      },
      expected_information_gain: 0.6,
      cost_estimate: 2.0,
      deadline: new Date(Date.now() + 48 * 60 * 60 * 1000)
    };
  }
}

/**
 * Feedback collection utilities
 */
export class FeedbackCollector {
  /**
   * Collect implicit feedback from user behavior
   */
  static collectImplicitFeedback(
    user_actions: Array<{
      action: string;
      timestamp: Date;
      context: Record<string, any>;
    }>,
    ai_suggestions: Array<{
      suggestion: string;
      timestamp: Date;
      accepted: boolean;
      time_to_decision: number;
    }>
  ): Array<{
    type: 'implicit';
    signal: string;
    strength: number;
    context: Record<string, any>;
  }> {
    const implicit_feedback = [];

    // Quick acceptance suggests good suggestion
    for (const suggestion of ai_suggestions) {
      if (suggestion.accepted && suggestion.time_to_decision < 5000) { // < 5 seconds
        implicit_feedback.push({
          type: 'implicit' as const,
          signal: 'quick_acceptance',
          strength: 0.8,
          context: {
            suggestion: suggestion.suggestion,
            decision_time: suggestion.time_to_decision
          }
        });
      }
      
      // Long delay before rejection suggests poor suggestion
      if (!suggestion.accepted && suggestion.time_to_decision > 30000) { // > 30 seconds
        implicit_feedback.push({
          type: 'implicit' as const,
          signal: 'slow_rejection',
          strength: -0.6,
          context: {
            suggestion: suggestion.suggestion,
            decision_time: suggestion.time_to_decision
          }
        });
      }
    }

    // Repeated similar actions suggest preference
    const action_counts = new Map<string, number>();
    for (const user_action of user_actions) {
      const count = action_counts.get(user_action.action) || 0;
      action_counts.set(user_action.action, count + 1);
    }

    for (const [action, count] of action_counts.entries()) {
      if (count >= 3) {
        implicit_feedback.push({
          type: 'implicit' as const,
          signal: 'repeated_action',
          strength: Math.min(0.9, count * 0.1),
          context: { action, frequency: count }
        });
      }
    }

    return implicit_feedback;
  }

  /**
   * Convert implicit signals to feedback
   */
  static implicitToFeedback(
    implicit_signals: Array<{
      signal: string;
      strength: number;
      context: Record<string, any>;
    }>,
    task_context: {
      agentAction: string;
      environmentState: Record<string, any>;
      decisionPoint: string;
    }
  ): {
    context: HumanFeedback['context'];
    feedback: HumanFeedback['feedback'];
    metadata: HumanFeedback['metadata'];
  } {
    // Aggregate signals
    const total_strength = implicit_signals.reduce((sum, signal) => sum + signal.strength, 0);
    const avg_strength = total_strength / implicit_signals.length;

    // Convert to explicit feedback
    const rating = Math.round(5 + avg_strength * 5); // Convert -1/+1 to 1-10 scale
    const confidence = Math.abs(avg_strength); // Strength indicates confidence

    return {
      context: task_context,
      feedback: {
        rating: Math.max(1, Math.min(10, rating)),
        explanation: `Inferred from ${implicit_signals.length} implicit signals`
      },
      metadata: {
        confidence,
        effort_level: 'LOW',
        expertise_level: 'INTERMEDIATE',
        time_spent: 0,
        interaction_mode: 'PASSIVE'
      }
    };
  }
}

/**
 * Preference model utilities
 */
export class PreferenceModelUtils {
  /**
   * Merge multiple preference models
   */
  static mergeModels(models: PreferenceModel[]): PreferenceModel {
    if (models.length === 0) {
      throw new Error('Cannot merge empty model list');
    }

    if (models.length === 1) {
      return { ...models[0] };
    }

    const merged_id = `merged_${models.map(m => m.id).join('_')}`;
    const merged_features: Record<string, number> = {};
    const merged_preferences = new Map<string, {
      weight: number;
      confidence: number;
      examples: string[];
      count: number;
    }>();

    // Merge features (weighted average by reliability)
    const total_reliability = models.reduce((sum, m) => sum + m.reliability, 0);
    
    for (const model of models) {
      const weight = model.reliability / total_reliability;
      
      for (const [feature, value] of Object.entries(model.features)) {
        merged_features[feature] = (merged_features[feature] || 0) + value * weight;
      }
      
      // Merge preferences
      for (const pref of model.preferences) {
        const existing = merged_preferences.get(pref.feature);
        if (existing) {
          existing.weight = (existing.weight * existing.count + pref.weight) / (existing.count + 1);
          existing.confidence = Math.max(existing.confidence, pref.confidence);
          existing.examples.push(...pref.examples);
          existing.count++;
        } else {
          merged_preferences.set(pref.feature, {
            weight: pref.weight,
            confidence: pref.confidence,
            examples: [...pref.examples],
            count: 1
          });
        }
      }
    }

    return {
      id: merged_id,
      domain: models[0].domain, // Use first model's domain
      features: merged_features,
      preferences: Array.from(merged_preferences.entries()).map(([feature, data]) => ({
        feature,
        weight: data.weight,
        confidence: data.confidence,
        examples: data.examples.slice(0, 10) // Limit examples
      })),
      reliability: total_reliability / models.length,
      last_updated: new Date(),
      training_samples: models.reduce((sum, m) => sum + m.training_samples, 0),
      validation_score: models.reduce((sum, m) => sum + m.validation_score, 0) / models.length
    };
  }

  /**
   * Validate preference model consistency
   */
  static validateConsistency(model: PreferenceModel): {
    consistent: boolean;
    issues: string[];
    confidence_score: number;
  } {
    const issues: string[] = [];
    let confidence_score = 1.0;

    // Check for conflicting preferences
    const conflicting_pairs = [];
    for (let i = 0; i < model.preferences.length; i++) {
      for (let j = i + 1; j < model.preferences.length; j++) {
        const pref1 = model.preferences[i];
        const pref2 = model.preferences[j];
        
        if (pref1.feature === pref2.feature && Math.abs(pref1.weight - pref2.weight) > 0.5) {
          conflicting_pairs.push([pref1.feature, pref2.feature]);
        }
      }
    }

    if (conflicting_pairs.length > 0) {
      issues.push(`Found ${conflicting_pairs.length} conflicting preference pairs`);
      confidence_score -= 0.2;
    }

    // Check confidence levels
    const low_confidence_prefs = model.preferences.filter(p => p.confidence < 0.3);
    if (low_confidence_prefs.length > model.preferences.length * 0.5) {
      issues.push('More than 50% of preferences have low confidence');
      confidence_score -= 0.3;
    }

    // Check training samples
    if (model.training_samples < 10) {
      issues.push('Insufficient training samples for reliable model');
      confidence_score -= 0.2;
    }

    // Check validation score
    if (model.validation_score < 0.6) {
      issues.push('Low validation score indicates poor model quality');
      confidence_score -= 0.3;
    }

    return {
      consistent: issues.length === 0,
      issues,
      confidence_score: Math.max(0, confidence_score)
    };
  }
}

/**
 * Learning session utilities
 */
export class LearningSessionUtils {
  /**
   * Generate learning session report
   */
  static generateReport(session: LearningSession): {
    summary: string;
    key_metrics: Record<string, any>;
    insights: string[];
    recommendations: string[];
  } {
    const improvement = session.learning_metrics.improvement_rate * 100;
    const duration_hours = session.learning_metrics.convergence_time / (1000 * 60 * 60);
    
    const summary = `Learning session for ${session.task_domain} using ${session.strategy} strategy. ` +
                   `Achieved ${improvement.toFixed(1)}% improvement over ${duration_hours.toFixed(1)} hours ` +
                   `with ${session.feedback_count} feedback interactions.`;

    const key_metrics = {
      improvement_percentage: improvement,
      duration_hours: duration_hours,
      feedback_count: session.feedback_count,
      feedback_quality: session.learning_metrics.feedback_quality_avg,
      final_performance: session.learning_metrics.final_performance,
      efficiency: improvement / duration_hours // improvement per hour
    };

    const insights = [];
    const recommendations = [];

    // Generate insights
    if (improvement > 20) {
      insights.push('Significant improvement achieved during session');
    } else if (improvement < 5) {
      insights.push('Limited improvement observed - may need different approach');
    }

    if (session.learning_metrics.feedback_quality_avg > 0.8) {
      insights.push('High quality feedback provided throughout session');
    } else if (session.learning_metrics.feedback_quality_avg < 0.5) {
      insights.push('Feedback quality was suboptimal');
    }

    if (duration_hours < 1) {
      insights.push('Rapid learning session - quick convergence');
    } else if (duration_hours > 8) {
      insights.push('Extended learning session - slow convergence');
    }

    // Generate recommendations
    if (improvement < 10) {
      recommendations.push('Consider alternative learning strategies for better results');
    }

    if (session.learning_metrics.feedback_quality_avg < 0.6) {
      recommendations.push('Focus on collecting higher quality feedback');
    }

    if (session.feedback_count < 5) {
      recommendations.push('Increase feedback frequency for better learning outcomes');
    }

    if (session.strategy === 'BATCH_LEARNING' && duration_hours > 4) {
      recommendations.push('Consider switching to immediate update strategy for faster convergence');
    }

    return {
      summary,
      key_metrics,
      insights,
      recommendations
    };
  }
}

/**
 * Example usage and testing utilities
 */
export class FeedbackTestUtils {
  /**
   * Create sample feedback for testing
   */
  static createSampleFeedback(): HumanFeedback[] {
    const samples: Array<{
      context: HumanFeedback['context'];
      feedback: HumanFeedback['feedback'];
      metadata: HumanFeedback['metadata'];
    }> = [
      {
        context: {
          agentAction: 'recommend_product',
          environmentState: { user_preferences: ['quality', 'price'] },
          decisionPoint: 'product_selection',
          taskId: 'task_1'
        },
        feedback: {
          rating: 8,
          explanation: 'Good recommendation, matches my preferences'
        },
        metadata: {
          confidence: 0.9,
          effort_level: 'LOW',
          expertise_level: 'INTERMEDIATE',
          time_spent: 5000,
          interaction_mode: 'ACTIVE'
        }
      },
      {
        context: {
          agentAction: 'schedule_meeting',
          environmentState: { calendar_conflicts: 2 },
          decisionPoint: 'time_selection',
          taskId: 'task_2'
        },
        feedback: {
          correction: {
            incorrect: 'Meeting at 3pm',
            correct: 'Meeting at 2pm',
            explanation: 'Earlier time works better for all participants'
          }
        },
        metadata: {
          confidence: 0.8,
          effort_level: 'MEDIUM',
          expertise_level: 'EXPERT',
          time_spent: 15000,
          interaction_mode: 'ACTIVE'
        }
      }
    ];

    return samples.map((sample, index) => ({
      id: `sample_${index}`,
      type: 'RATING' as FeedbackType,
      source: 'HUMAN' as const,
      quality: 'HIGH' as FeedbackQuality,
      timestamp: new Date(Date.now() - index * 60000),
      ...sample,
      processed: false
    }));
  }
}
