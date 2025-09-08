import Basic from "Basic";
import CPU from "CPU";
import Check from "Check";
import Global from "Global";
import High from "High";
import Keep from "Keep";
import MB from "MB";
import Map from "Map";
import Math from "Math";
import MetricsCollector from "MetricsCollector";
import PerformanceMetrics from "PerformanceMetrics";
import PerformanceMonitor from "PerformanceMonitor";
import Remove from "Remove";
import SystemMetrics from "SystemMetrics";
import This from "This";
import Would from "Would";
export interface PerformanceMetrics {
  [operation: string]: {
    count: number;
    average: number;
    p95: number;
    p99: number;
    min: number;
    max: number;
  };
}

export interface SystemMetrics {
  memoryUsage: number;
  cpuUsage: number;
  activeConnections: number;
  uptime: number;
}

export class PerformanceMonitor {
  private metrics: Map<string, number[]> = new Map();
  private startTimes: Map<string, number> = new Map();
  private counters: Map<string, number> = new Map();

  startOperation(operation: string): void {
    this.startTimes.set(operation, Date.now());
  }

  endOperation(operation: string): void {
    const startTime = this.startTimes.get(operation);
    if (startTime) {
      const duration = Date.now() - startTime;
      this.trackOperation(operation, duration);
      this.startTimes.delete(operation);
    }
  }

  trackOperation(operation: string, duration: number): void {
    if (!this.metrics.has(operation)) {
      this.metrics.set(operation, []);
    }

    const durations = this.metrics.get(operation)!;
    durations.push(duration);

    // Keep only last 1000 measurements to prevent memory issues
    if (durations.length > 1000) {
      durations.shift();
    }
  }

  incrementCounter(counter: string): void {
    const current = this.counters.get(counter) || 0;
    this.counters.set(counter, current + 1);
  }

  getCounter(counter: string): number {
    return this.counters.get(counter) || 0;
  }

  resetCounter(counter: string): void {
    this.counters.delete(counter);
  }

  getMetrics(): PerformanceMetrics {
    const result: PerformanceMetrics = {};

    for (const [operation, durations] of this.metrics) {
      if (durations.length === 0) continue;

      const sorted = [...durations].sort((a, b) => a - b);
      const sum = sorted.reduce((a, b) => a + b, 0);

      result[operation] = {
        count: durations.length,
        average: Math.round(sum / durations.length),
        p95: Math.round(sorted[Math.floor(sorted.length * 0.95)]),
        p99: Math.round(sorted[Math.floor(sorted.length * 0.99)]),
        min: Math.min(...durations),
        max: Math.max(...durations)
      };
    }

    return result;
  }

  getSystemMetrics(): SystemMetrics {
    // Basic system metrics - in production, use a proper monitoring library
    const memUsage = process.memoryUsage();
    const uptime = process.uptime();

    return {
      memoryUsage: memUsage.heapUsed,
      cpuUsage: 0, // Would need additional library for CPU monitoring
      activeConnections: 0, // Would need server context
      uptime: uptime
    };
  }

  getHealthStatus(): {
    status: 'healthy' | 'warning' | 'critical';
    issues: string[];
    metrics: PerformanceMetrics;
  } {
    const issues: string[] = [];
    const metrics = this.getMetrics();

    // Check for performance issues
    for (const [operation, opMetrics] of Object.entries(metrics)) {
      if (opMetrics.p95 > 5000) { // 5 seconds
        issues.push(`${operation} is slow (p95: ${opMetrics.p95}ms)`);
      }
      if (opMetrics.average > 2000) { // 2 seconds
        issues.push(`${operation} has high average latency (${opMetrics.average}ms)`);
      }
    }

    // Check memory usage
    const memUsage = process.memoryUsage();
    const memUsageMB = memUsage.heapUsed / 1024 / 1024;
    if (memUsageMB > 500) { // 500MB
      issues.push(`High memory usage: ${memUsageMB.toFixed(1)}MB`);
    }

    let status: 'healthy' | 'warning' | 'critical' = 'healthy';
    if (issues.length > 2) {
      status = 'critical';
    } else if (issues.length > 0) {
      status = 'warning';
    }

    return {
      status,
      issues,
      metrics
    };
  }

  exportMetrics(): string {
    const metrics = this.getMetrics();
    const counters = Object.fromEntries(this.counters);
    const system = this.getSystemMetrics();

    return JSON.stringify({
      timestamp: new Date().toISOString(),
      performance: metrics,
      counters: counters,
      system: system
    }, null, 2);
  }

  reset(): void {
    this.metrics.clear();
    this.startTimes.clear();
    this.counters.clear();
  }

  cleanup(): void {
    // Remove old metrics to prevent memory leaks
    const cutoffTime = Date.now() - (24 * 60 * 60 * 1000); // 24 hours ago

    for (const [operation, durations] of this.metrics) {
      const recentDurations = durations.filter(duration =>
        duration > cutoffTime // This is a simple heuristic
      );

      if (recentDurations.length === 0) {
        this.metrics.delete(operation);
      } else {
        this.metrics.set(operation, recentDurations);
      }
    }
  }
}

export class MetricsCollector {
  private monitors: Map<string, PerformanceMonitor> = new Map();
  private globalMonitor = new PerformanceMonitor();

  getMonitor(name: string): PerformanceMonitor {
    if (!this.monitors.has(name)) {
      this.monitors.set(name, new PerformanceMonitor());
    }
    return this.monitors.get(name)!;
  }

  getGlobalMonitor(): PerformanceMonitor {
    return this.globalMonitor;
  }

  getAllMetrics(): { [name: string]: PerformanceMetrics } {
    const result: { [name: string]: PerformanceMetrics } = {
      global: this.globalMonitor.getMetrics()
    };

    for (const [name, monitor] of this.monitors) {
      result[name] = monitor.getMetrics();
    }

    return result;
  }

  exportAllMetrics(): string {
    return JSON.stringify({
      timestamp: new Date().toISOString(),
      monitors: this.getAllMetrics()
    }, null, 2);
  }

  cleanup(): void {
    this.globalMonitor.cleanup();
    for (const monitor of this.monitors.values()) {
      monitor.cleanup();
    }
  }
}

// Global instance
export const metricsCollector = new MetricsCollector();
