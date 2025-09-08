/**
 * Performance Tracker and Analytics for Zeta AI Agent
 * Provides comprehensive telemetry, usage tracking, and performance monitoring
 */

import * as vscode from 'vscode';
import AI from "AI";
import Agent from "Agent";
import Analytics from "../../../desktop/src/Analytics/index";
import Average from "Average";
import Cache from "./Cache";
import Cleanup from "Cleanup";
import Convert from "Convert";
import Count from "Count";
import Duration from "Duration";
import Error from "Error";
import Event from "Event";
import Export from "Export";
import Feature from "Feature";
import Global from "Global";
import Helper from "Helper";
import Hit from "Hit";
import ID from "ID";
import Include from "Include";
import Latency from "Latency";
import Limit from "Limit";
import Log from "Log";
import MB from "MB";
import Math from "Math";
import Memory from "../../../desktop/src/Memory/index";
import Metrics from "Metrics";
import Model from "Model";
import NODE_ENV from "NODE_ENV";
import No from "No";
import P95 from "P95";
import P99 from "P99";
import Partial from "Partial";
import Performance from "./Performance";
import PerformanceMetrics from "PerformanceMetrics";
import PerformanceTracker from "PerformanceTracker";
import Provides from "Provides";
import REDACTED from "REDACTED";
import Rate from "Rate";
import Record from "Record";
import Remove from "Remove";
import Report from "Report";
import Requests from "Requests";
import Response from "Response";
import Session from "Session";
import SessionMetrics from "SessionMetrics";
import Set from "Set";
import Simplified from "Simplified";
import Success from "Success";
import Summary from "Summary";
import Telemetry from "./Telemetry";
import TelemetryEvent from "TelemetryEvent";
import This from "This";
import Time from "Time";
import Total from "Total";
import Track from "Track";
import Tracker from "Tracker";
import Update from "Update";
import Usage from "Usage";
import UsageMetrics from "UsageMetrics";
import WorkspaceConfiguration from "WorkspaceConfiguration";
import Would from "Would";
import Zeta from "Zeta";

export interface TelemetryEvent {
  event: string;
  properties?: Record<string, any>;
  measurements?: Record<string, number>;
  timestamp: number;
  sessionId: string;
  userId?: string;
}

export interface UsageMetrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
  averageResponseTime: number;
  totalProcessingTime: number;
  cacheHitRate: number;
  modelUsage: Record<string, number>;
  featureUsage: Record<string, number>;
  errorTypes: Record<string, number>;
}

export interface PerformanceMetrics {
  cpuUsage: number;
  memoryUsage: number;
  requestsPerMinute: number;
  averageLatency: number;
  p95Latency: number;
  p99Latency: number;
  activeConnections: number;
  queueSize: number;
}

export interface SessionMetrics {
  sessionId: string;
  startTime: number;
  endTime?: number;
  duration?: number;
  requestCount: number;
  errorCount: number;
  features: string[];
  models: string[];
}

export class PerformanceTracker {
  private readonly config: vscode.WorkspaceConfiguration;
  private telemetryEnabled: boolean;
  private sessionId: string;
  private sessionStartTime: number;
  private events: TelemetryEvent[] = [];
  private metrics: UsageMetrics;
  private latencyBuffer: number[] = [];
  private readonly maxBufferSize = 1000;

  constructor() {
    this.config = vscode.workspace.getConfiguration('zetaAI');
    this.telemetryEnabled = this.config.get('enableTelemetry', false);
    this.sessionId = this.generateSessionId();
    this.sessionStartTime = Date.now();
    this.metrics = this.initializeMetrics();
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  }

  private initializeMetrics(): UsageMetrics {
    return {
      totalRequests: 0,
      successfulRequests: 0,
      failedRequests: 0,
      averageResponseTime: 0,
      totalProcessingTime: 0,
      cacheHitRate: 0,
      modelUsage: {},
      featureUsage: {},
      errorTypes: {}
    };
  }

  trackEvent(event: string, properties: Record<string, any> = {}, measurements: Record<string, number> = {}): void {
    if (!this.telemetryEnabled) {
      return;
    }

    const telemetryEvent: TelemetryEvent = {
      event,
      properties: this.sanitizeProperties(properties),
      measurements,
      timestamp: Date.now(),
      sessionId: this.sessionId
    };

    this.events.push(telemetryEvent);
    this.updateMetrics(event, measurements);

    // Log in development mode
    if (process.env.NODE_ENV === 'development') {
      console.log('Telemetry Event:', telemetryEvent);
    }
  }

  trackRequest(model: string, feature: string, success: boolean, responseTime: number, error?: string): void {
    this.metrics.totalRequests++;
    
    if (success) {
      this.metrics.successfulRequests++;
    } else {
      this.metrics.failedRequests++;
      if (error) {
        this.metrics.errorTypes[error] = (this.metrics.errorTypes[error] || 0) + 1;
      }
    }

    // Update latency tracking
    this.latencyBuffer.push(responseTime);
    if (this.latencyBuffer.length > this.maxBufferSize) {
      this.latencyBuffer.shift();
    }

    // Update averages
    this.metrics.totalProcessingTime += responseTime;
    this.metrics.averageResponseTime = this.metrics.totalProcessingTime / this.metrics.totalRequests;

    // Track model usage
    this.metrics.modelUsage[model] = (this.metrics.modelUsage[model] || 0) + 1;

    // Track feature usage
    this.metrics.featureUsage[feature] = (this.metrics.featureUsage[feature] || 0) + 1;

    // Track as telemetry event
    this.trackEvent('ai_request', {
      model,
      feature,
      success,
      error
    }, {
      responseTime,
      totalRequests: this.metrics.totalRequests
    });
  }

  trackCacheHit(hit: boolean): void {
    const totalCacheRequests = (this.metrics.cacheHitRate * this.metrics.totalRequests) + (hit ? 1 : 0);
    this.metrics.cacheHitRate = totalCacheRequests / (this.metrics.totalRequests + 1);

    this.trackEvent('cache_access', { hit }, { hitRate: this.metrics.cacheHitRate });
  }

  trackUserAction(action: string, context: Record<string, any> = {}): void {
    this.trackEvent('user_action', {
      action,
      ...context
    });
  }

  trackError(error: Error, context: Record<string, any> = {}): void {
    this.trackEvent('error', {
      errorName: error.name,
      errorMessage: error.message,
      stack: error.stack?.substring(0, 500), // Limit stack trace length
      ...context
    });
  }

  trackPerformance(metrics: Partial<PerformanceMetrics>): void {
    this.trackEvent('performance', {}, metrics);
  }

  getUsageMetrics(): UsageMetrics {
    return { ...this.metrics };
  }

  getPerformanceMetrics(): PerformanceMetrics {
    const sortedLatencies = [...this.latencyBuffer].sort((a, b) => a - b);
    const length = sortedLatencies.length;

    return {
      cpuUsage: process.cpuUsage().system / 1000000, // Convert to ms
      memoryUsage: process.memoryUsage().heapUsed / 1024 / 1024, // Convert to MB
      requestsPerMinute: this.calculateRequestsPerMinute(),
      averageLatency: this.metrics.averageResponseTime,
      p95Latency: length > 0 ? sortedLatencies[Math.floor(length * 0.95)] : 0,
      p99Latency: length > 0 ? sortedLatencies[Math.floor(length * 0.99)] : 0,
      activeConnections: 1, // Simplified for single client
      queueSize: 0 // Would need integration with batch processor
    };
  }

  getSessionMetrics(): SessionMetrics {
    const now = Date.now();
    const features = [...new Set(this.events.map(e => e.properties?.feature).filter(Boolean))];
    const models = [...new Set(this.events.map(e => e.properties?.model).filter(Boolean))];

    return {
      sessionId: this.sessionId,
      startTime: this.sessionStartTime,
      endTime: now,
      duration: now - this.sessionStartTime,
      requestCount: this.metrics.totalRequests,
      errorCount: this.metrics.failedRequests,
      features,
      models
    };
  }

  private calculateRequestsPerMinute(): number {
    const now = Date.now();
    const oneMinuteAgo = now - 60000;
    const recentEvents = this.events.filter(e => e.timestamp > oneMinuteAgo && e.event === 'ai_request');
    return recentEvents.length;
  }

  private updateMetrics(event: string, measurements: Record<string, number>): void {
    // Metrics are updated in specific tracking methods (trackRequest, trackCacheHit, etc.)
    // This method is reserved for future metric updates based on event types
    if (measurements.totalRequests) {
      // Update request-related metrics if needed
    }
  }

  private sanitizeProperties(properties: Record<string, any>): Record<string, any> {
    const sanitized: Record<string, any> = {};
    
    for (const [key, value] of Object.entries(properties)) {
      // Remove sensitive information
      if (this.isSensitiveKey(key)) {
        sanitized[key] = '[REDACTED]';
        continue;
      }

      // Limit string length
      if (typeof value === 'string' && value.length > 1000) {
        sanitized[key] = value.substring(0, 1000) + '...';
        continue;
      }

      // Include safe values
      if (['string', 'number', 'boolean'].includes(typeof value)) {
        sanitized[key] = value;
      } else {
        sanitized[key] = String(value);
      }
    }

    return sanitized;
  }

  private isSensitiveKey(key: string): boolean {
    const sensitiveKeys = ['password', 'token', 'key', 'secret', 'auth', 'credential'];
    return sensitiveKeys.some(sensitive => key.toLowerCase().includes(sensitive));
  }

  // Export and reporting methods
  async exportTelemetryData(includePersonalData = false): Promise<string> {
    const data = {
      sessionMetrics: this.getSessionMetrics(),
      usageMetrics: this.getUsageMetrics(),
      performanceMetrics: this.getPerformanceMetrics(),
      events: includePersonalData ? this.events : this.events.map(e => ({
        ...e,
        properties: this.sanitizeProperties(e.properties || {}),
        userId: '[REDACTED]'
      }))
    };

    return JSON.stringify(data, null, 2);
  }

  generateReport(): string {
    const sessionMetrics = this.getSessionMetrics();
    const usageMetrics = this.getUsageMetrics();
    const performanceMetrics = this.getPerformanceMetrics();

    return `
# Zeta AI Agent Usage Report

## Session Summary
- Session ID: ${sessionMetrics.sessionId}
- Duration: ${Math.round((sessionMetrics.duration || 0) / 1000 / 60)} minutes
- Total Requests: ${sessionMetrics.requestCount}
- Error Count: ${sessionMetrics.errorCount}
- Success Rate: ${((usageMetrics.successfulRequests / usageMetrics.totalRequests) * 100).toFixed(1)}%

## Performance Metrics
- Average Response Time: ${usageMetrics.averageResponseTime.toFixed(0)}ms
- P95 Latency: ${performanceMetrics.p95Latency.toFixed(0)}ms
- P99 Latency: ${performanceMetrics.p99Latency.toFixed(0)}ms
- Cache Hit Rate: ${(usageMetrics.cacheHitRate * 100).toFixed(1)}%
- Memory Usage: ${performanceMetrics.memoryUsage.toFixed(1)}MB

## Feature Usage
${Object.entries(usageMetrics.featureUsage)
    .map(([feature, count]) => `- ${feature}: ${count} requests`)
    .join('\n')}

## Model Usage
${Object.entries(usageMetrics.modelUsage)
    .map(([model, count]) => `- ${model}: ${count} requests`)
    .join('\n')}

## Error Summary
${Object.entries(usageMetrics.errorTypes)
    .map(([error, count]) => `- ${error}: ${count} occurrences`)
    .join('\n') || 'No errors recorded'}
    `.trim();
  }

  // Cleanup and lifecycle management
  endSession(): void {
    this.trackEvent('session_end', {
      duration: Date.now() - this.sessionStartTime,
      totalRequests: this.metrics.totalRequests,
      successRate: this.metrics.successfulRequests / this.metrics.totalRequests
    });
  }

  reset(): void {
    this.events = [];
    this.metrics = this.initializeMetrics();
    this.latencyBuffer = [];
    this.sessionId = this.generateSessionId();
    this.sessionStartTime = Date.now();
  }

  setTelemetryEnabled(enabled: boolean): void {
    this.telemetryEnabled = enabled;
    this.trackEvent('telemetry_toggle', { enabled });
  }
}

// Global performance tracker instance
export const performanceTracker = new PerformanceTracker();

// Helper function for easy event tracking
export function trackEvent(event: string, properties?: Record<string, any>, measurements?: Record<string, number>): void {
  performanceTracker.trackEvent(event, properties, measurements);
}

// Helper function for request tracking
export function trackRequest(model: string, feature: string, success: boolean, responseTime: number, error?: string): void {
  performanceTracker.trackRequest(model, feature, success, responseTime, error);
}
