/**
 * Performance Monitor
 * Tracks and analyzes AI agent performance metrics
 * Integrates with Auto-Tuner for optimization feedback
 */

import { PerformanceMetrics } from './autoTuner';
import AI from "AI";
import Alert from "Alert";
import Analysis from "Analysis";
import Analyze from "Analyze";
import Auto from "Auto";
import BETWEEN from "BETWEEN";
import CONVERSATION from "CONVERSATION";
import CRITICAL from "CRITICAL";
import Call from "Call";
import Check from "Check";
import Cleanup from "Cleanup";
import Configure from "Configure";
import Consider from "Consider";
import DECLINING from "DECLINING";
import Declining from "Declining";
import Determine from "Determine";
import EQUALS from "EQUALS";
import End from "End";
import Error from "Error";
import Export from "Export";
import For from "For";
import GREATER_THAN from "GREATER_THAN";
import Generate from "Generate";
import Get from "Get";
import HIGH from "HIGH";
import High from "High";
import ID from "ID";
import IMPROVING from "IMPROVING";
import In from "In";
import Integrates from "Integrates";
import LESS_THAN from "LESS_THAN";
import LOW from "LOW";
import Low from "Low";
import MEDIUM from "MEDIUM";
import Map from "Map";
import Math from "Math";
import Monitor from "Monitor";
import Need from "Need";
import No from "No";
import NodeJS from "NodeJS";
import Omit from "Omit";
import PLANNING from "PLANNING";
import Partial from "Partial";
import Performance from "Performance";
import PerformanceAlert from "PerformanceAlert";
import PerformanceMonitor from "./PerformanceMonitor";
import PerformanceSession from "PerformanceSession";
import PerformanceTrend from "PerformanceTrend";
import Periodic from "Periodic";
import Private from "Private";
import REASONING from "REASONING";
import Rate from "Rate";
import Record from "Record";
import Remove from "Remove";
import Response from "Response";
import Review from "Review";
import Run from "Run";
import STABLE from "STABLE";
import Satisfaction from "Satisfaction";
import Simple from "Simple";
import Sort from "Sort";
import Start from "Start";
import Stop from "Stop";
import TASK_EXECUTION from "TASK_EXECUTION";
import Time from "Time";
import Timeout from "Timeout";
import Tracks from "Tracks";
import Trend from "Trend";
import Tuner from "Tuner";
import Update from "Update";
import User from "User";
import X from "X";

/**
 * Performance monitoring session
 */
export interface PerformanceSession {
  id: string;
  startTime: Date;
  endTime?: Date;
  metrics: PerformanceMetrics[];
  context: {
    operation: string;
    parameters: Record<string, any>;
    userId?: string;
    sessionType: 'CONVERSATION' | 'TASK_EXECUTION' | 'REASONING' | 'PLANNING';
  };
  summary?: {
    averageResponseTime: number;
    totalRequests: number;
    errorCount: number;
    satisfactionScore: number;
  };
}

/**
 * Performance alert configuration
 */
export interface PerformanceAlert {
  id: string;
  name: string;
  condition: {
    metric: keyof PerformanceMetrics;
    operator: 'GREATER_THAN' | 'LESS_THAN' | 'EQUALS' | 'BETWEEN';
    threshold: number | [number, number];
    duration?: number; // Alert if condition persists for X milliseconds
  };
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  enabled: boolean;
  lastTriggered?: Date;
}

/**
 * Performance trend analysis
 */
export interface PerformanceTrend {
  metric: keyof PerformanceMetrics;
  direction: 'IMPROVING' | 'DECLINING' | 'STABLE';
  magnitude: number; // Rate of change
  confidence: number; // 0-1 scale
  timeWindow: number; // Analysis window in hours
  significance: 'HIGH' | 'MEDIUM' | 'LOW';
}

/**
 * Performance Monitor implementation
 */
export class PerformanceMonitor {
  private readonly sessions: Map<string, PerformanceSession> = new Map();
  private readonly alerts: Map<string, PerformanceAlert> = new Map();
  private currentSession?: PerformanceSession;
  private readonly maxSessionHistory: number = 100;
  private readonly alertCheckInterval: number = 5000; // 5 seconds
  private alertTimer?: NodeJS.Timeout;

  constructor() {
    this.initializeDefaultAlerts();
    this.startAlertMonitoring();
  }

  /**
   * Start new performance monitoring session
   */
  startSession(
    operation: string,
    sessionType: PerformanceSession['context']['sessionType'],
    parameters: Record<string, any> = {},
    userId?: string
  ): string {
    const sessionId = this.generateSessionId();
    
    const session: PerformanceSession = {
      id: sessionId,
      startTime: new Date(),
      metrics: [],
      context: {
        operation,
        parameters,
        userId,
        sessionType
      }
    };

    this.sessions.set(sessionId, session);
    this.currentSession = session;

    return sessionId;
  }

  /**
   * Record performance metrics for current session
   */
  recordMetrics(metrics: Partial<PerformanceMetrics>): void {
    if (!this.currentSession) {
      console.warn('No active performance session. Call startSession() first.');
      return;
    }

    const fullMetrics: PerformanceMetrics = {
      responseTime: 0,
      accuracy: 0.5,
      coherence: 0.5,
      relevance: 0.5,
      efficiency: 0,
      userSatisfaction: 0.5,
      memoryUsage: 0,
      errorRate: 0,
      completionRate: 1.0,
      timestamp: new Date(),
      ...metrics
    };

    this.currentSession.metrics.push(fullMetrics);

    // Check for alert conditions
    this.checkAlerts(fullMetrics);
  }

  /**
   * End current session and generate summary
   */
  endSession(): PerformanceSession | null {
    if (!this.currentSession) {
      return null;
    }

    this.currentSession.endTime = new Date();
    this.currentSession.summary = this.generateSessionSummary(this.currentSession);

    const session = this.currentSession;
    this.currentSession = undefined;

    // Cleanup old sessions
    this.cleanupOldSessions();

    return session;
  }

  /**
   * Get session by ID
   */
  getSession(sessionId: string): PerformanceSession | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * Get recent sessions
   */
  getRecentSessions(limit = 10): PerformanceSession[] {
    const sessions = Array.from(this.sessions.values());
    sessions.sort((a, b) => b.startTime.getTime() - a.startTime.getTime());
    return sessions.slice(0, limit);
  }

  /**
   * Analyze performance trends
   */
  analyzePerformanceTrends(timeWindowHours = 24): PerformanceTrend[] {
    const cutoffTime = new Date(Date.now() - timeWindowHours * 60 * 60 * 1000);
    const recentSessions = Array.from(this.sessions.values())
      .filter(session => session.startTime > cutoffTime);

    if (recentSessions.length < 2) {
      return [];
    }

    const allMetrics = recentSessions.flatMap(session => session.metrics);
    const trends: PerformanceTrend[] = [];

    // Analyze each metric
    const metricsToAnalyze: (keyof PerformanceMetrics)[] = [
      'responseTime', 'accuracy', 'coherence', 'relevance', 
      'efficiency', 'userSatisfaction', 'errorRate'
    ];

    for (const metric of metricsToAnalyze) {
      const trend = this.calculateMetricTrend(allMetrics, metric, timeWindowHours);
      if (trend) {
        trends.push(trend);
      }
    }

    return trends.sort((a, b) => {
      const significanceOrder = { HIGH: 3, MEDIUM: 2, LOW: 1 };
      return significanceOrder[b.significance] - significanceOrder[a.significance];
    });
  }

  /**
   * Get performance summary for time period
   */
  getPerformanceSummary(timeWindowHours = 24): {
    totalSessions: number;
    totalRequests: number;
    averageMetrics: Partial<PerformanceMetrics>;
    trends: PerformanceTrend[];
    alerts: Array<{ alert: PerformanceAlert; triggeredCount: number }>;
    recommendations: string[];
  } {
    const cutoffTime = new Date(Date.now() - timeWindowHours * 60 * 60 * 1000);
    const recentSessions = Array.from(this.sessions.values())
      .filter(session => session.startTime > cutoffTime);

    const allMetrics = recentSessions.flatMap(session => session.metrics);
    const averageMetrics = this.calculateAverageMetrics(allMetrics);
    const trends = this.analyzePerformanceTrends(timeWindowHours);
    
    // Get alert summary
    const alertSummary = this.getAlertSummary(timeWindowHours);
    
    // Generate recommendations
    const recommendations = this.generatePerformanceRecommendations(averageMetrics, trends);

    return {
      totalSessions: recentSessions.length,
      totalRequests: allMetrics.length,
      averageMetrics,
      trends,
      alerts: alertSummary,
      recommendations
    };
  }

  /**
   * Configure performance alert
   */
  addAlert(alert: Omit<PerformanceAlert, 'id'>): string {
    const alertId = this.generateAlertId();
    const fullAlert: PerformanceAlert = {
      id: alertId,
      ...alert
    };

    this.alerts.set(alertId, fullAlert);
    return alertId;
  }

  /**
   * Update alert configuration
   */
  updateAlert(alertId: string, updates: Partial<PerformanceAlert>): boolean {
    const alert = this.alerts.get(alertId);
    if (!alert) return false;

    Object.assign(alert, updates);
    return true;
  }

  /**
   * Remove alert
   */
  removeAlert(alertId: string): boolean {
    return this.alerts.delete(alertId);
  }

  /**
   * Get all alerts
   */
  getAlerts(): PerformanceAlert[] {
    return Array.from(this.alerts.values());
  }

  /**
   * Export performance data
   */
  exportPerformanceData(): string {
    const recentSessions = this.getRecentSessions(50);
    const trends = this.analyzePerformanceTrends(168); // 1 week
    const summary = this.getPerformanceSummary(24);

    return JSON.stringify({
      version: '1.0',
      timestamp: new Date().toISOString(),
      sessions: recentSessions,
      trends,
      summary,
      alerts: Array.from(this.alerts.values())
    }, null, 2);
  }

  /**
   * Private helper methods
   */

  private generateSessionId(): string {
    return `perf_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  private generateAlertId(): string {
    return `alert_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }

  private generateSessionSummary(session: PerformanceSession): PerformanceSession['summary'] {
    if (session.metrics.length === 0) {
      return {
        averageResponseTime: 0,
        totalRequests: 0,
        errorCount: 0,
        satisfactionScore: 0
      };
    }

    const metrics = session.metrics;
    const totalRequests = metrics.length;
    const averageResponseTime = metrics.reduce((sum, m) => sum + m.responseTime, 0) / totalRequests;
    const errorCount = metrics.filter(m => m.errorRate > 0).length;
    const satisfactionScore = metrics.reduce((sum, m) => sum + m.userSatisfaction, 0) / totalRequests;

    return {
      averageResponseTime,
      totalRequests,
      errorCount,
      satisfactionScore
    };
  }

  private calculateAverageMetrics(metrics: PerformanceMetrics[]): Partial<PerformanceMetrics> {
    if (metrics.length === 0) return {};

    const sums: Partial<Record<keyof PerformanceMetrics, number>> = {};
    const keys = Object.keys(metrics[0]) as (keyof PerformanceMetrics)[];

    keys.forEach(key => {
      if (key !== 'timestamp') {
        sums[key] = metrics.reduce((sum, metric) => {
          const value = metric[key];
          return sum + (typeof value === 'number' ? value : 0);
        }, 0);
      }
    });

    const averages: Partial<PerformanceMetrics> = {};
    Object.entries(sums).forEach(([key, sum]) => {
      if (typeof sum === 'number') {
        averages[key as keyof PerformanceMetrics] = sum / metrics.length as any;
      }
    });

    return averages;
  }

  private calculateMetricTrend(
    metrics: PerformanceMetrics[],
    metricName: keyof PerformanceMetrics,
    timeWindowHours: number
  ): PerformanceTrend | null {
    if (metrics.length < 5) return null; // Need enough data points

    const values = metrics.map(m => {
      const value = m[metricName];
      return typeof value === 'number' ? value : 0;
    });

    // Simple linear regression to detect trend
    const n = values.length;
    const x = Array.from({ length: n }, (_, i) => i);
    const sumX = x.reduce((sum, val) => sum + val, 0);
    const sumY = values.reduce((sum, val) => sum + val, 0);
    const sumXY = x.reduce((sum, val, i) => sum + val * values[i], 0);
    const sumXX = x.reduce((sum, val) => sum + val * val, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const correlation = this.calculateCorrelation(x, values);

    // Determine trend direction and significance
    let direction: PerformanceTrend['direction'];
    let significance: PerformanceTrend['significance'];

    if (Math.abs(slope) < 0.01) {
      direction = 'STABLE';
    } else if (slope > 0) {
      direction = metricName === 'errorRate' || metricName === 'responseTime' ? 'DECLINING' : 'IMPROVING';
    } else {
      direction = metricName === 'errorRate' || metricName === 'responseTime' ? 'IMPROVING' : 'DECLINING';
    }

    if (Math.abs(correlation) > 0.7) {
      significance = 'HIGH';
    } else if (Math.abs(correlation) > 0.4) {
      significance = 'MEDIUM';
    } else {
      significance = 'LOW';
    }

    return {
      metric: metricName,
      direction,
      magnitude: Math.abs(slope),
      confidence: Math.abs(correlation),
      timeWindow: timeWindowHours,
      significance
    };
  }

  private calculateCorrelation(x: number[], y: number[]): number {
    const n = x.length;
    if (n === 0) return 0;

    const meanX = x.reduce((sum, val) => sum + val, 0) / n;
    const meanY = y.reduce((sum, val) => sum + val, 0) / n;

    let numerator = 0;
    let denomX = 0;
    let denomY = 0;

    for (let i = 0; i < n; i++) {
      const dx = x[i] - meanX;
      const dy = y[i] - meanY;
      numerator += dx * dy;
      denomX += dx * dx;
      denomY += dy * dy;
    }

    const denominator = Math.sqrt(denomX * denomY);
    return denominator === 0 ? 0 : numerator / denominator;
  }

  private checkAlerts(metrics: PerformanceMetrics): void {
    for (const alert of this.alerts.values()) {
      if (!alert.enabled) continue;

      const shouldTrigger = this.evaluateAlertCondition(alert, metrics);
      
      if (shouldTrigger) {
        this.triggerAlert(alert, metrics);
      }
    }
  }

  private evaluateAlertCondition(alert: PerformanceAlert, metrics: PerformanceMetrics): boolean {
    const metricValue = metrics[alert.condition.metric];
    if (typeof metricValue !== 'number') return false;

    const { operator, threshold } = alert.condition;

    switch (operator) {
    case 'GREATER_THAN':
      return metricValue > (threshold as number);
    case 'LESS_THAN':
      return metricValue < (threshold as number);
    case 'EQUALS':
      return Math.abs(metricValue - (threshold as number)) < 0.001;
    case 'BETWEEN': {
      const [min, max] = threshold as [number, number];
      return metricValue >= min && metricValue <= max;
    }
    default:
      return false;
    }
  }

  private triggerAlert(alert: PerformanceAlert, metrics: PerformanceMetrics): void {
    const now = new Date();
    alert.lastTriggered = now;

    console.warn(`Performance Alert: ${alert.name}`, {
      severity: alert.severity,
      condition: alert.condition,
      currentValue: metrics[alert.condition.metric],
      timestamp: now
    });

    // In a real implementation, you might send notifications here
  }

  private generatePerformanceRecommendations(
    averageMetrics: Partial<PerformanceMetrics>,
    trends: PerformanceTrend[]
  ): string[] {
    const recommendations: string[] = [];

    // Response time recommendations
    if (averageMetrics.responseTime && averageMetrics.responseTime > 2000) {
      recommendations.push('High response times detected. Consider optimizing model parameters or reducing context length.');
    }

    // Error rate recommendations
    if (averageMetrics.errorRate && averageMetrics.errorRate > 0.05) {
      recommendations.push('Error rate above 5%. Review error logs and consider parameter adjustments.');
    }

    // User satisfaction recommendations
    if (averageMetrics.userSatisfaction && averageMetrics.userSatisfaction < 0.6) {
      recommendations.push('Low user satisfaction scores. Consider quality-focused optimization strategy.');
    }

    // Trend-based recommendations
    const decliningTrends = trends.filter(t => t.direction === 'DECLINING' && t.significance === 'HIGH');
    if (decliningTrends.length > 0) {
      const metrics = decliningTrends.map(t => t.metric).join(', ');
      recommendations.push(`Declining performance in: ${metrics}. Run optimization cycle to address issues.`);
    }

    return recommendations;
  }

  private getAlertSummary(timeWindowHours: number): Array<{ alert: PerformanceAlert; triggeredCount: number }> {
    const cutoffTime = new Date(Date.now() - timeWindowHours * 60 * 60 * 1000);
    
    return Array.from(this.alerts.values()).map(alert => ({
      alert,
      triggeredCount: alert.lastTriggered && alert.lastTriggered > cutoffTime ? 1 : 0
    }));
  }

  private initializeDefaultAlerts(): void {
    // High response time alert
    this.addAlert({
      name: 'High Response Time',
      condition: {
        metric: 'responseTime',
        operator: 'GREATER_THAN',
        threshold: 5000 // 5 seconds
      },
      severity: 'HIGH',
      enabled: true
    });

    // High error rate alert
    this.addAlert({
      name: 'High Error Rate',
      condition: {
        metric: 'errorRate',
        operator: 'GREATER_THAN',
        threshold: 0.1 // 10%
      },
      severity: 'CRITICAL',
      enabled: true
    });

    // Low user satisfaction alert
    this.addAlert({
      name: 'Low User Satisfaction',
      condition: {
        metric: 'userSatisfaction',
        operator: 'LESS_THAN',
        threshold: 0.4 // 40%
      },
      severity: 'MEDIUM',
      enabled: true
    });
  }

  private startAlertMonitoring(): void {
    this.alertTimer = setInterval(() => {
      // Periodic alert checks could be implemented here
      // For now, alerts are checked when metrics are recorded
    }, this.alertCheckInterval);
  }

  private cleanupOldSessions(): void {
    const sessions = Array.from(this.sessions.entries());
    if (sessions.length <= this.maxSessionHistory) return;

    // Sort by start time and keep only the most recent sessions
    sessions.sort((a, b) => b[1].startTime.getTime() - a[1].startTime.getTime());
    const toRemove = sessions.slice(this.maxSessionHistory);

    toRemove.forEach(([sessionId]) => {
      this.sessions.delete(sessionId);
    });
  }

  /**
   * Stop alert monitoring (cleanup)
   */
  destroy(): void {
    if (this.alertTimer) {
      clearInterval(this.alertTimer);
      this.alertTimer = undefined;
    }
  }
}
