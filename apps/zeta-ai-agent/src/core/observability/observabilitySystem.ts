import AI from "AI";
import ALERT from "ALERT";
import Active from "Active";
import Add from "Add";
import Alert from "Alert";
import AlertRule from "AlertRule";
import AlertSystem from "AlertSystem";
import AnomalyDetection from "AnomalyDetection";
import Apply from "Apply";
import Attempted from "Attempted";
import COMPLETED from "COMPLETED";
import CONTAINS from "CONTAINS";
import COUNTER from "COUNTER";
import CRITICAL from "CRITICAL";
import Check from "Check";
import Clean from "Clean";
import Cleanup from "Cleanup";
import Collect from "Collect";
import Comprehensive from "Comprehensive";
import Console from "Console";
import Critical from "Critical";
import DEBUG from "DEBUG";
import DEGRADED from "DEGRADED";
import Determine from "Determine";
import EMAIL from "EMAIL";
import EQ from "EQ";
import ERROR from "ERROR";
import ESCALATE from "ESCALATE";
import Error from "Error";
import Execute from "Execute";
import Export from "Export";
import FAILED from "FAILED";
import FATAL from "FATAL";
import Finish from "Finish";
import Finished from "Finished";
import GAUGE from "GAUGE";
import GT from "GT";
import GTE from "GTE";
import Get from "Get";
import HEALTHY from "HEALTHY";
import HIGH from "HIGH";
import HISTOGRAM from "HISTOGRAM";
import Health from "Health";
import HealthCheck from "HealthCheck";
import HealthStatus from "HealthStatus";
import Heap from "Heap";
import High from "High";
import How from "How";
import ID from "ID";
import INFO from "INFO";
import In from "In";
import LEARNING from "LEARNING";
import LOG from "LOG";
import LOW from "LOW";
import LT from "LT";
import LTE from "LTE";
import Last from "Last";
import Log from "Log";
import LogEntry from "LogEntry";
import LogLevel from "LogLevel";
import MEDIUM from "MEDIUM";
import MEMORY_ACCESS from "MEMORY_ACCESS";
import Map from "Map";
import Math from "Math";
import Memory from "../../../../desktop/src/Memory/index";
import Metric from "Metric";
import MetricType from "MetricType";
import Minimum from "Minimum";
import NodeJS from "NodeJS";
import OPTIMIZATION from "OPTIMIZATION";
import Observability from "Observability";
import ObservabilitySystem from "./ObservabilitySystem";
import Omit from "Omit";
import P50 from "P50";
import P95 from "P95";
import P99 from "P99";
import PLANNING from "PLANNING";
import PLUGIN_EXECUTION from "PLUGIN_EXECUTION";
import Performance from "Performance";
import PerformanceBaseline from "PerformanceBaseline";
import Private from "Private";
import Process from "Process";
import Provides from "Provides";
import Query from "Query";
import RATE from "RATE";
import REASONING from "REASONING";
import Rate from "Rate";
import Record from "Record";
import Remove from "Remove";
import SAFETY_CHECK from "SAFETY_CHECK";
import STARTED from "STARTED";
import SYSTEM_OPERATION from "SYSTEM_OPERATION";
import Simple from "Simple";
import Smoothing from "Smoothing";
import Sort from "Sort";
import SpanType from "SpanType";
import Start from "Start";
import Started from "Started";
import Structured from "Structured";
import System from "System";
import SystemMetric from "SystemMetric";
import TIMER from "TIMER";
import Timeout from "Timeout";
import Total from "Total";
import Trace from "Trace";
import TraceSpan from "TraceSpan";
import UNHEALTHY from "UNHEALTHY";
import USER_INTERACTION from "USER_INTERACTION";
import Update from "Update";
import Usage from "Usage";
import WARN from "WARN";
import WEBHOOK from "WEBHOOK";
import Warning from "Warning";
/**
 * Observability System
 * Comprehensive monitoring, logging, tracing, and health checks for autonomous AI
 * Provides deep insights into system behavior and performance
 */

/**
 * Log levels for structured logging
 */
export type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR' | 'FATAL';

/**
 * Trace span types
 */
export type SpanType = 
  | 'REASONING'
  | 'PLANNING' 
  | 'MEMORY_ACCESS'
  | 'OPTIMIZATION'
  | 'SAFETY_CHECK'
  | 'LEARNING'
  | 'PLUGIN_EXECUTION'
  | 'USER_INTERACTION'
  | 'SYSTEM_OPERATION';

/**
 * Health check status
 */
export type HealthStatus = 'HEALTHY' | 'DEGRADED' | 'UNHEALTHY' | 'CRITICAL';

/**
 * Metric types
 */
export type MetricType = 'COUNTER' | 'GAUGE' | 'HISTOGRAM' | 'TIMER' | 'RATE';

/**
 * Log entry structure
 */
export interface LogEntry {
  id: string;
  timestamp: Date;
  level: LogLevel;
  message: string;
  context: {
    component: string;
    operation?: string;
    userId?: string;
    sessionId?: string;
    traceId?: string;
    spanId?: string;
  };
  metadata: Record<string, any>;
  error?: {
    name: string;
    message: string;
    stack?: string;
    code?: string;
  };
  duration?: number; // milliseconds
  tags: string[];
}

/**
 * Trace span for distributed tracing
 */
export interface TraceSpan {
  id: string;
  traceId: string;
  parentSpanId?: string;
  operationName: string;
  spanType: SpanType;
  startTime: Date;
  endTime?: Date;
  duration?: number;
  status: 'STARTED' | 'COMPLETED' | 'FAILED';
  tags: Record<string, string>;
  logs: Array<{
    timestamp: Date;
    level: LogLevel;
    message: string;
    fields?: Record<string, any>;
  }>;
  metrics: Record<string, number>;
  error?: {
    message: string;
    stack?: string;
  };
}

/**
 * System metric definition
 */
export interface SystemMetric {
  id: string;
  name: string;
  type: MetricType;
  value: number;
  timestamp: Date;
  labels: Record<string, string>;
  unit?: string;
  description?: string;
}

/**
 * Health check configuration
 */
export interface HealthCheck {
  id: string;
  name: string;
  component: string;
  checkFunction: () => Promise<{
    status: HealthStatus;
    message?: string;
    details?: Record<string, any>;
    duration: number;
  }>;
  interval: number; // milliseconds
  timeout: number; // milliseconds
  retries: number;
  enabled: boolean;
  lastCheck?: {
    timestamp: Date;
    status: HealthStatus;
    duration: number;
    message?: string;
  };
}

/**
 * Alert rule configuration
 */
export interface AlertRule {
  id: string;
  name: string;
  description: string;
  condition: {
    metric: string;
    operator: 'GT' | 'LT' | 'EQ' | 'GTE' | 'LTE' | 'CONTAINS';
    threshold: number | string;
    duration?: number; // How long condition must persist
  };
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  actions: Array<{
    type: 'LOG' | 'EMAIL' | 'WEBHOOK' | 'ESCALATE';
    config: Record<string, any>;
  }>;
  enabled: boolean;
  cooldown: number; // Minimum time between alerts
  lastTriggered?: Date;
}

/**
 * Performance baseline for anomaly detection
 */
export interface PerformanceBaseline {
  component: string;
  metric: string;
  baseline: {
    mean: number;
    stdDev: number;
    percentiles: Record<string, number>; // P50, P95, P99
    sampleSize: number;
    lastUpdated: Date;
  };
  thresholds: {
    warning: number;
    critical: number;
  };
}

/**
 * Observability System implementation
 */
export class ObservabilitySystem {
  private readonly logs: LogEntry[] = [];
  private readonly traces: Map<string, TraceSpan[]> = new Map();
  private readonly metrics: Map<string, SystemMetric[]> = new Map();
  private readonly healthChecks: Map<string, HealthCheck> = new Map();
  private readonly alertRules: Map<string, AlertRule> = new Map();
  private readonly baselines: Map<string, PerformanceBaseline> = new Map();
  private readonly activeSpans: Map<string, TraceSpan> = new Map();
  
  private readonly maxLogEntries: number = 10000;
  private readonly maxTraceHistory: number = 1000;
  private readonly maxMetricHistory: number = 5000;
  private readonly healthCheckInterval: number = 30000; // 30 seconds
  
  private healthCheckTimer?: NodeJS.Timeout;
  private metricsCollectionTimer?: NodeJS.Timeout;

  constructor() {
    this.initializeDefaultHealthChecks();
    this.initializeDefaultAlertRules();
    this.startHealthChecks();
    this.startMetricsCollection();
  }

  /**
   * Structured logging
   */
  log(
    level: LogLevel,
    message: string,
    context: LogEntry['context'],
    metadata: Record<string, any> = {},
    error?: Error
  ): string {
    const logId = this.generateLogId();
    
    const entry: LogEntry = {
      id: logId,
      timestamp: new Date(),
      level,
      message,
      context,
      metadata,
      error: error ? {
        name: error.name,
        message: error.message,
        stack: error.stack,
        code: (error as any).code
      } : undefined,
      tags: this.generateLogTags(level, context)
    };

    this.logs.push(entry);
    this.cleanupLogs();

    // Check for alert conditions
    this.checkAlerts(entry);

    // Console output for immediate visibility
    this.outputToConsole(entry);

    return logId;
  }

  /**
   * Start distributed trace
   */
  startTrace(
    operationName: string,
    spanType: SpanType,
    parentSpanId?: string,
    tags: Record<string, string> = {}
  ): string {
    const traceId = parentSpanId ? this.getTraceIdFromSpan(parentSpanId) : this.generateTraceId();
    const spanId = this.generateSpanId();

    const span: TraceSpan = {
      id: spanId,
      traceId,
      parentSpanId,
      operationName,
      spanType,
      startTime: new Date(),
      status: 'STARTED',
      tags,
      logs: [],
      metrics: {}
    };

    this.activeSpans.set(spanId, span);
    
    // Add to trace collection
    const traceSpans = this.traces.get(traceId) || [];
    traceSpans.push(span);
    this.traces.set(traceId, traceSpans);

    this.log('DEBUG', `Started trace span: ${operationName}`, {
      component: 'ObservabilitySystem',
      operation: 'startTrace',
      traceId,
      spanId
    }, { spanType, tags });

    return spanId;
  }

  /**
   * Finish trace span
   */
  finishTrace(
    spanId: string,
    status: 'COMPLETED' | 'FAILED' = 'COMPLETED',
    error?: Error
  ): void {
    const span = this.activeSpans.get(spanId);
    if (!span) {
      this.log('WARN', `Attempted to finish non-existent span: ${spanId}`, {
        component: 'ObservabilitySystem',
        operation: 'finishTrace'
      });
      return;
    }

    span.endTime = new Date();
    span.duration = span.endTime.getTime() - span.startTime.getTime();
    span.status = status;

    if (error) {
      span.error = {
        message: error.message,
        stack: error.stack
      };
    }

    this.activeSpans.delete(spanId);

    this.log('DEBUG', `Finished trace span: ${span.operationName}`, {
      component: 'ObservabilitySystem',
      operation: 'finishTrace',
      traceId: span.traceId,
      spanId
    }, { 
      duration: span.duration,
      status,
      spanType: span.spanType 
    });

    // Clean up old traces
    this.cleanupTraces();
  }

  /**
   * Add log to trace span
   */
  addTraceLog(
    spanId: string,
    level: LogLevel,
    message: string,
    fields?: Record<string, any>
  ): void {
    const span = this.activeSpans.get(spanId);
    if (!span) return;

    span.logs.push({
      timestamp: new Date(),
      level,
      message,
      fields
    });
  }

  /**
   * Record metric
   */
  recordMetric(
    name: string,
    type: MetricType,
    value: number,
    labels: Record<string, string> = {},
    unit?: string,
    description?: string
  ): void {
    const metricId = this.generateMetricId();
    
    const metric: SystemMetric = {
      id: metricId,
      name,
      type,
      value,
      timestamp: new Date(),
      labels,
      unit,
      description
    };

    const metricHistory = this.metrics.get(name) || [];
    metricHistory.push(metric);
    this.metrics.set(name, metricHistory);

    // Update performance baselines
    this.updateBaseline(name, value, labels);

    // Check for anomalies
    this.checkAnomalies(name, value, labels);

    // Cleanup old metrics
    this.cleanupMetrics();
  }

  /**
   * Get system health status
   */
  async getSystemHealth(): Promise<{
    overall: HealthStatus;
    components: Record<string, {
      status: HealthStatus;
      message?: string;
      lastCheck: Date;
      duration: number;
    }>;
    summary: {
      healthy: number;
      degraded: number;
      unhealthy: number;
      critical: number;
    };
  }> {
    const components: Record<string, any> = {};
    const summary = { healthy: 0, degraded: 0, unhealthy: 0, critical: 0 };

    for (const healthCheck of this.healthChecks.values()) {
      if (!healthCheck.enabled || !healthCheck.lastCheck) continue;

      const component = {
        status: healthCheck.lastCheck.status,
        message: healthCheck.lastCheck.message,
        lastCheck: healthCheck.lastCheck.timestamp,
        duration: healthCheck.lastCheck.duration
      };

      components[healthCheck.component] = component;
      summary[healthCheck.lastCheck.status.toLowerCase() as keyof typeof summary]++;
    }

    // Determine overall health
    let overall: HealthStatus = 'HEALTHY';
    if (summary.critical > 0) overall = 'CRITICAL';
    else if (summary.unhealthy > 0) overall = 'UNHEALTHY';
    else if (summary.degraded > 0) overall = 'DEGRADED';

    return { overall, components, summary };
  }

  /**
   * Query logs with filters
   */
  queryLogs(filters: {
    level?: LogLevel[];
    component?: string[];
    timeRange?: { start: Date; end: Date };
    traceId?: string;
    searchText?: string;
    limit?: number;
  }): LogEntry[] {
    let filteredLogs = [...this.logs];

    // Apply filters
    if (filters.level) {
      filteredLogs = filteredLogs.filter(log => filters.level!.includes(log.level));
    }

    if (filters.component) {
      filteredLogs = filteredLogs.filter(log => 
        filters.component!.includes(log.context.component)
      );
    }

    if (filters.timeRange) {
      filteredLogs = filteredLogs.filter(log => 
        log.timestamp >= filters.timeRange!.start && 
        log.timestamp <= filters.timeRange!.end
      );
    }

    if (filters.traceId) {
      filteredLogs = filteredLogs.filter(log => 
        log.context.traceId === filters.traceId
      );
    }

    if (filters.searchText) {
      const searchLower = filters.searchText.toLowerCase();
      filteredLogs = filteredLogs.filter(log => 
        log.message.toLowerCase().includes(searchLower) ||
        JSON.stringify(log.metadata).toLowerCase().includes(searchLower)
      );
    }

    // Sort by timestamp (newest first)
    const sortedLogs = [...filteredLogs];
    sortedLogs.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());

    // Apply limit
    const limit = filters.limit || 100;
    return sortedLogs.slice(0, limit);
  }

  /**
   * Get trace by ID
   */
  getTrace(traceId: string): TraceSpan[] | undefined {
    return this.traces.get(traceId);
  }

  /**
   * Get metrics for a specific name
   */
  getMetrics(
    name: string,
    timeRange?: { start: Date; end: Date },
    labels?: Record<string, string>
  ): SystemMetric[] {
    const metrics = this.metrics.get(name) || [];
    let filtered = metrics;

    if (timeRange) {
      filtered = filtered.filter(metric => 
        metric.timestamp >= timeRange.start && 
        metric.timestamp <= timeRange.end
      );
    }

    if (labels) {
      filtered = filtered.filter(metric => {
        return Object.entries(labels).every(([key, value]) => 
          metric.labels[key] === value
        );
      });
    }

    return filtered.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
  }

  /**
   * Add custom health check
   */
  addHealthCheck(healthCheck: Omit<HealthCheck, 'lastCheck'>): void {
    this.healthChecks.set(healthCheck.id, {
      ...healthCheck,
      lastCheck: undefined
    });
  }

  /**
   * Add alert rule
   */
  addAlertRule(rule: AlertRule): void {
    this.alertRules.set(rule.id, rule);
  }

  /**
   * Get system statistics
   */
  getSystemStatistics(): {
    logs: {
      total: number;
      byLevel: Record<LogLevel, number>;
      errorRate: number;
      recentErrors: number;
    };
    traces: {
      active: number;
      completed: number;
      averageDuration: number;
      errorRate: number;
    };
    metrics: {
      totalMetrics: number;
      uniqueNames: number;
      recentUpdates: number;
    };
    health: {
      totalChecks: number;
      passing: number;
      failing: number;
    };
    } {
    // Log statistics
    const logsByLevel: Record<LogLevel, number> = {
      DEBUG: 0, INFO: 0, WARN: 0, ERROR: 0, FATAL: 0
    };
    
    this.logs.forEach(log => {
      logsByLevel[log.level]++;
    });

    const errorLogs = this.logs.filter(log => log.level === 'ERROR' || log.level === 'FATAL');
    const recentTime = new Date(Date.now() - 60 * 60 * 1000); // Last hour
    const recentErrors = errorLogs.filter(log => log.timestamp > recentTime).length;

    // Trace statistics
    const allTraces = Array.from(this.traces.values()).flat();
    const completedTraces = allTraces.filter(span => span.status === 'COMPLETED' || span.status === 'FAILED');
    const failedTraces = allTraces.filter(span => span.status === 'FAILED');
    const averageDuration = completedTraces.length > 0 
      ? completedTraces.reduce((sum, span) => sum + (span.duration || 0), 0) / completedTraces.length
      : 0;

    // Metric statistics
    const allMetrics = Array.from(this.metrics.values()).flat();
    const recentMetrics = allMetrics.filter(metric => 
      metric.timestamp > new Date(Date.now() - 60 * 60 * 1000)
    );

    // Health statistics
    const healthChecks = Array.from(this.healthChecks.values());
    const passingChecks = healthChecks.filter(check => 
      check.lastCheck?.status === 'HEALTHY'
    );

    return {
      logs: {
        total: this.logs.length,
        byLevel: logsByLevel,
        errorRate: this.logs.length > 0 ? errorLogs.length / this.logs.length : 0,
        recentErrors: recentErrors
      },
      traces: {
        active: this.activeSpans.size,
        completed: completedTraces.length,
        averageDuration,
        errorRate: completedTraces.length > 0 ? failedTraces.length / completedTraces.length : 0
      },
      metrics: {
        totalMetrics: allMetrics.length,
        uniqueNames: this.metrics.size,
        recentUpdates: recentMetrics.length
      },
      health: {
        totalChecks: healthChecks.length,
        passing: passingChecks.length,
        failing: healthChecks.length - passingChecks.length
      }
    };
  }

  /**
   * Export observability data
   */
  exportData(options: {
    includeLogs?: boolean;
    includeTraces?: boolean;
    includeMetrics?: boolean;
    timeRange?: { start: Date; end: Date };
  } = {}): string {
    const data: any = {
      version: '1.0',
      timestamp: new Date().toISOString(),
      systemStats: this.getSystemStatistics()
    };

    if (options.includeLogs !== false) {
      data.logs = this.queryLogs({
        timeRange: options.timeRange,
        limit: 1000
      });
    }

    if (options.includeTraces !== false) {
      const traces: Record<string, TraceSpan[]> = {};
      this.traces.forEach((spans, traceId) => {
        if (options.timeRange) {
          const filteredSpans = spans.filter(span => 
            span.startTime >= options.timeRange!.start &&
            span.startTime <= options.timeRange!.end
          );
          if (filteredSpans.length > 0) {
            traces[traceId] = filteredSpans;
          }
        } else {
          traces[traceId] = spans;
        }
      });
      data.traces = traces;
    }

    if (options.includeMetrics !== false) {
      const metrics: Record<string, SystemMetric[]> = {};
      this.metrics.forEach((metricList, name) => {
        metrics[name] = this.getMetrics(name, options.timeRange);
      });
      data.metrics = metrics;
    }

    return JSON.stringify(data, null, 2);
  }

  /**
   * Private helper methods
   */

  private generateLogId(): string {
    return `log_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  private generateTraceId(): string {
    return `trace_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  }

  private generateSpanId(): string {
    return `span_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  private generateMetricId(): string {
    return `metric_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }

  private getTraceIdFromSpan(spanId: string): string {
    const span = this.activeSpans.get(spanId);
    return span?.traceId || this.generateTraceId();
  }

  private generateLogTags(level: LogLevel, context: LogEntry['context']): string[] {
    const tags = [level.toLowerCase(), context.component];
    
    if (context.operation) tags.push(context.operation);
    if (context.userId) tags.push('user');
    if (context.traceId) tags.push('traced');
    
    return tags;
  }

  private outputToConsole(entry: LogEntry): void {
    const timestamp = entry.timestamp.toISOString();
    const operationSuffix = entry.context.operation ? `:${entry.context.operation}` : '';
    const context = `[${entry.context.component}${operationSuffix}]`;
    const traceInfo = entry.context.traceId ? ` (trace:${entry.context.traceId.substring(0, 8)})` : '';
    
    const message = `${timestamp} ${entry.level} ${context}${traceInfo} ${entry.message}`;
    
    switch (entry.level) {
    case 'DEBUG':
      console.debug(message, entry.metadata);
      break;
    case 'INFO':
      console.info(message, entry.metadata);
      break;
    case 'WARN':
      console.warn(message, entry.metadata);
      break;
    case 'ERROR':
    case 'FATAL':
      console.error(message, entry.metadata, entry.error);
      break;
    }
  }

  private checkAlerts(entry: LogEntry): void {
    this.alertRules.forEach(rule => {
      if (!rule.enabled) return;

      // Check cooldown
      if (rule.lastTriggered && 
          Date.now() - rule.lastTriggered.getTime() < rule.cooldown) {
        return;
      }

      let shouldTrigger = false;

      // Simple alert conditions based on log levels
      if (rule.condition.metric === 'error_rate' && 
          (entry.level === 'ERROR' || entry.level === 'FATAL')) {
        shouldTrigger = true;
      }

      if (shouldTrigger) {
        this.triggerAlert(rule, entry);
      }
    });
  }

  private triggerAlert(rule: AlertRule, trigger: LogEntry | SystemMetric): void {
    rule.lastTriggered = new Date();

    this.log('WARN', `Alert triggered: ${rule.name}`, {
      component: 'ObservabilitySystem',
      operation: 'triggerAlert'
    }, {
      rule: rule.name,
      severity: rule.severity,
      condition: rule.condition,
      trigger: trigger
    });

    // Execute alert actions
    rule.actions.forEach(action => {
      switch (action.type) {
      case 'LOG':
        this.log('ERROR', `ALERT: ${rule.description}`, {
          component: 'AlertSystem'
        }, { rule: rule.name, severity: rule.severity });
        break;
      case 'EMAIL':
      case 'WEBHOOK':
      case 'ESCALATE':
        // In a real implementation, these would trigger external actions
        console.warn(`Alert action ${action.type} not implemented`);
        break;
      }
    });
  }

  private updateBaseline(
    metricName: string,
    value: number,
    labels: Record<string, string>
  ): void {
    const baselineKey = `${metricName}_${JSON.stringify(labels)}`;
    const existing = this.baselines.get(baselineKey);

    if (!existing) {
      this.baselines.set(baselineKey, {
        component: labels.component || 'unknown',
        metric: metricName,
        baseline: {
          mean: value,
          stdDev: 0,
          percentiles: { P50: value, P95: value, P99: value },
          sampleSize: 1,
          lastUpdated: new Date()
        },
        thresholds: {
          warning: value * 1.5,
          critical: value * 2.0
        }
      });
      return;
    }

    // Update baseline using exponential moving average
    const alpha = 0.1; // Smoothing factor
    existing.baseline.mean = existing.baseline.mean * (1 - alpha) + value * alpha;
    existing.baseline.sampleSize++;
    existing.baseline.lastUpdated = new Date();

    // Simple threshold updates
    existing.thresholds.warning = existing.baseline.mean * 1.5;
    existing.thresholds.critical = existing.baseline.mean * 2.0;
  }

  private checkAnomalies(
    metricName: string,
    value: number,
    labels: Record<string, string>
  ): void {
    const baselineKey = `${metricName}_${JSON.stringify(labels)}`;
    const baseline = this.baselines.get(baselineKey);

    if (!baseline || baseline.baseline.sampleSize < 10) return;

    if (value > baseline.thresholds.critical) {
      this.log('ERROR', `Critical anomaly detected in ${metricName}`, {
        component: 'AnomalyDetection'
      }, {
        metric: metricName,
        value,
        baseline: baseline.baseline.mean,
        threshold: baseline.thresholds.critical,
        labels
      });
    } else if (value > baseline.thresholds.warning) {
      this.log('WARN', `Warning anomaly detected in ${metricName}`, {
        component: 'AnomalyDetection'
      }, {
        metric: metricName,
        value,
        baseline: baseline.baseline.mean,
        threshold: baseline.thresholds.warning,
        labels
      });
    }
  }

  private cleanupLogs(): void {
    if (this.logs.length > this.maxLogEntries) {
      this.logs.splice(0, this.logs.length - this.maxLogEntries);
    }
  }

  private cleanupTraces(): void {
    if (this.traces.size > this.maxTraceHistory) {
      // Remove oldest traces
      const traceIds = Array.from(this.traces.keys());
      const toRemove = traceIds.slice(0, this.traces.size - this.maxTraceHistory);
      toRemove.forEach(traceId => this.traces.delete(traceId));
    }
  }

  private cleanupMetrics(): void {
    this.metrics.forEach((metricList, name) => {
      if (metricList.length > this.maxMetricHistory) {
        const sorted = [...metricList];
        sorted.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());
        this.metrics.set(name, sorted.slice(0, this.maxMetricHistory));
      }
    });
  }

  private async runHealthCheck(healthCheck: HealthCheck): Promise<void> {
    const startTime = Date.now();
    
    try {
      const result = await Promise.race([
        healthCheck.checkFunction(),
        new Promise<never>((_, reject) => 
          setTimeout(() => reject(new Error('Health check timeout')), healthCheck.timeout)
        )
      ]);

      healthCheck.lastCheck = {
        timestamp: new Date(),
        status: result.status,
        duration: Date.now() - startTime,
        message: result.message
      };

    } catch (error) {
      healthCheck.lastCheck = {
        timestamp: new Date(),
        status: 'CRITICAL',
        duration: Date.now() - startTime,
        message: error instanceof Error ? error.message : 'Health check failed'
      };
    }
  }

  private startHealthChecks(): void {
    this.healthCheckTimer = setInterval(async () => {
      const promises = Array.from(this.healthChecks.values())
        .filter(check => check.enabled)
        .map(check => this.runHealthCheck(check));

      await Promise.allSettled(promises);
    }, this.healthCheckInterval);
  }

  private startMetricsCollection(): void {
    this.metricsCollectionTimer = setInterval(() => {
      // System metrics
      this.recordMetric('system.memory.usage', 'GAUGE', process.memoryUsage().heapUsed, {
        component: 'system'
      }, 'bytes', 'Heap memory usage');

      this.recordMetric('system.uptime', 'GAUGE', process.uptime(), {
        component: 'system'
      }, 'seconds', 'Process uptime');

      // Observability system metrics
      this.recordMetric('observability.logs.total', 'GAUGE', this.logs.length, {
        component: 'observability'
      }, 'count', 'Total log entries');

      this.recordMetric('observability.traces.active', 'GAUGE', this.activeSpans.size, {
        component: 'observability'
      }, 'count', 'Active trace spans');

    }, 60000); // Collect every minute
  }

  private initializeDefaultHealthChecks(): void {
    // Memory usage health check
    this.addHealthCheck({
      id: 'memory_usage',
      name: 'Memory Usage',
      component: 'system',
      checkFunction: async () => {
        const memUsage = process.memoryUsage();
        const usagePercent = memUsage.heapUsed / memUsage.heapTotal;
        
        let status: HealthStatus = 'HEALTHY';
        if (usagePercent > 0.9) status = 'CRITICAL';
        else if (usagePercent > 0.8) status = 'UNHEALTHY';
        else if (usagePercent > 0.7) status = 'DEGRADED';

        return {
          status,
          message: `Memory usage: ${Math.round(usagePercent * 100)}%`,
          details: memUsage,
          duration: 1
        };
      },
      interval: 30000,
      timeout: 5000,
      retries: 3,
      enabled: true
    });

    // Log error rate health check
    this.addHealthCheck({
      id: 'log_error_rate',
      name: 'Log Error Rate',
      component: 'observability',
      checkFunction: async () => {
        const recentTime = new Date(Date.now() - 5 * 60 * 1000); // 5 minutes
        const recentLogs = this.logs.filter(log => log.timestamp > recentTime);
        const errorLogs = recentLogs.filter(log => log.level === 'ERROR' || log.level === 'FATAL');
        
        const errorRate = recentLogs.length > 0 ? errorLogs.length / recentLogs.length : 0;
        
        let status: HealthStatus = 'HEALTHY';
        if (errorRate > 0.1) status = 'CRITICAL';
        else if (errorRate > 0.05) status = 'UNHEALTHY';
        else if (errorRate > 0.02) status = 'DEGRADED';

        return {
          status,
          message: `Error rate: ${Math.round(errorRate * 100)}%`,
          details: { errorCount: errorLogs.length, totalLogs: recentLogs.length },
          duration: 2
        };
      },
      interval: 30000,
      timeout: 5000,
      retries: 3,
      enabled: true
    });
  }

  private initializeDefaultAlertRules(): void {
    // High error rate alert
    this.addAlertRule({
      id: 'high_error_rate',
      name: 'High Error Rate',
      description: 'Error rate exceeds acceptable threshold',
      condition: {
        metric: 'error_rate',
        operator: 'GT',
        threshold: 0.1
      },
      severity: 'HIGH',
      actions: [
        { type: 'LOG', config: {} }
      ],
      enabled: true,
      cooldown: 300000 // 5 minutes
    });

    // Memory usage alert
    this.addAlertRule({
      id: 'high_memory_usage',
      name: 'High Memory Usage',
      description: 'Memory usage exceeds critical threshold',
      condition: {
        metric: 'system.memory.usage',
        operator: 'GT',
        threshold: 0.9
      },
      severity: 'CRITICAL',
      actions: [
        { type: 'LOG', config: {} },
        { type: 'ESCALATE', config: {} }
      ],
      enabled: true,
      cooldown: 600000 // 10 minutes
    });
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    if (this.healthCheckTimer) {
      clearInterval(this.healthCheckTimer);
      this.healthCheckTimer = undefined;
    }

    if (this.metricsCollectionTimer) {
      clearInterval(this.metricsCollectionTimer);
      this.metricsCollectionTimer = undefined;
    }

    this.log('INFO', 'Observability system destroyed', {
      component: 'ObservabilitySystem',
      operation: 'destroy'
    });
  }
}
