import Avg from "Avg";
import B from "B";
import Count from "Count";
import Counter from "Counter";
import Decorator from "Decorator";
import Export from "Export";
import GB from "GB";
import Generate from "Generate";
import Group from "Group";
import Histogram from "Histogram";
import Import from "Import";
import KB from "KB";
import Keep from "Keep";
import Last from "Last";
import MB from "MB";
import Map from "Map";
import Math from "Math";
import Max from "Max";
import Measure from "Measure";
import MemoryUsage from "MemoryUsage";
import Metric from "Metric";
import Metrics from "Metrics";
import Min from "Min";
import No from "No";
import P95 from "P95";
import Performance from "./Performance";
import PerformanceMetric from "PerformanceMetric";
import PerformanceMonitor from "PerformanceMonitor";
import Period from "Period";
import Prevent from "Prevent";
import PropertyDescriptor from "PropertyDescriptor";
import Record from "Record";
import Report from "Report";
import Reset from "Reset";
import Return from "Return";
import Singleton from "Singleton";
import Statistics from "Statistics";
import System from "System";
import SystemMetrics from "SystemMetrics";
import T from "T";
import TB from "TB";
import Time from "Time";
import Timer from "Timer";
import TimingResult from "TimingResult";
import Total from "Total";
import Utility from "Utility";
export interface PerformanceMetric {
  name: string;
  value: number;
  unit: string;
  timestamp: number;
  tags?: Record<string, string>;
}

export interface TimingResult {
  duration: number;
  startTime: number;
  endTime: number;
}

export interface MemoryUsage {
  heapUsed: number;
  heapTotal: number;
  external: number;
  rss: number;
}

export interface SystemMetrics {
  memory: MemoryUsage;
  cpu: number;
  timestamp: number;
}

export class PerformanceMonitor {
  private readonly metrics: PerformanceMetric[] = [];
  private readonly timers = new Map<string, number>();
  private readonly counters = new Map<string, number>();
  private readonly histograms = new Map<string, number[]>();
  private readonly maxMetricsHistory = 1000;

  // Timer methods
  startTimer(name: string): void {
    this.timers.set(name, Date.now());
  }

  endTimer(name: string, tags?: Record<string, string>): TimingResult | null {
    const startTime = this.timers.get(name);
    if (!startTime) {
      return null;
    }

    const endTime = Date.now();
    const duration = endTime - startTime;

    this.addMetric({
      name: `${name}_duration`,
      value: duration,
      unit: 'ms',
      timestamp: endTime,
      tags
    });

    this.timers.delete(name);

    return {
      duration,
      startTime,
      endTime
    };
  }

  // Measure execution time of a function
  async measureAsync<T>(name: string, fn: () => Promise<T>, tags?: Record<string, string>): Promise<T> {
    this.startTimer(name);
    try {
      const result = await fn();
      this.endTimer(name, { ...tags, status: 'success' });
      return result;
    } catch (error) {
      this.endTimer(name, { ...tags, status: 'error' });
      throw error;
    }
  }

  measure<T>(name: string, fn: () => T, tags?: Record<string, string>): T {
    this.startTimer(name);
    try {
      const result = fn();
      this.endTimer(name, { ...tags, status: 'success' });
      return result;
    } catch (error) {
      this.endTimer(name, { ...tags, status: 'error' });
      throw error;
    }
  }

  // Counter methods
  increment(name: string, value = 1, tags?: Record<string, string>): void {
    const currentValue = this.counters.get(name) || 0;
    const newValue = currentValue + value;
    this.counters.set(name, newValue);

    this.addMetric({
      name: `${name}_count`,
      value: newValue,
      unit: 'count',
      timestamp: Date.now(),
      tags
    });
  }

  decrement(name: string, value = 1, tags?: Record<string, string>): void {
    this.increment(name, -value, tags);
  }

  // Histogram methods
  recordValue(name: string, value: number, tags?: Record<string, string>): void {
    const values = this.histograms.get(name) || [];
    values.push(value);
    
    // Keep only recent values to prevent memory growth
    if (values.length > 100) {
      values.shift();
    }
    
    this.histograms.set(name, values);

    this.addMetric({
      name,
      value,
      unit: 'value',
      timestamp: Date.now(),
      tags
    });
  }

  // System metrics
  recordMemoryUsage(): MemoryUsage {
    const memUsage = process.memoryUsage();
    
    this.addMetric({
      name: 'memory_heap_used',
      value: memUsage.heapUsed,
      unit: 'bytes',
      timestamp: Date.now()
    });

    this.addMetric({
      name: 'memory_heap_total',
      value: memUsage.heapTotal,
      unit: 'bytes',
      timestamp: Date.now()
    });

    this.addMetric({
      name: 'memory_external',
      value: memUsage.external,
      unit: 'bytes',
      timestamp: Date.now()
    });

    this.addMetric({
      name: 'memory_rss',
      value: memUsage.rss,
      unit: 'bytes',
      timestamp: Date.now()
    });

    return memUsage;
  }

  // Metric management
  addMetric(metric: PerformanceMetric): void {
    this.metrics.push(metric);
    
    // Prevent memory growth
    if (this.metrics.length > this.maxMetricsHistory) {
      this.metrics.shift();
    }
  }

  getMetrics(name?: string, since?: number): PerformanceMetric[] {
    let filtered = this.metrics;

    if (name) {
      filtered = filtered.filter(m => m.name === name || m.name.startsWith(name));
    }

    if (since) {
      filtered = filtered.filter(m => m.timestamp >= since);
    }

    return [...filtered]; // Return copy
  }

  getLatestMetric(name: string): PerformanceMetric | null {
    for (let i = this.metrics.length - 1; i >= 0; i--) {
      if (this.metrics[i].name === name) {
        return this.metrics[i];
      }
    }
    return null;
  }

  // Statistics
  getStatistics(name: string, since?: number): {
    count: number;
    min: number;
    max: number;
    avg: number;
    sum: number;
    p50: number;
    p95: number;
    p99: number;
  } | null {
    const metrics = this.getMetrics(name, since);
    
    if (metrics.length === 0) {
      return null;
    }

    const values = metrics.map(m => m.value).sort((a, b) => a - b);
    const count = values.length;
    const min = values[0];
    const max = values[count - 1];
    const sum = values.reduce((a, b) => a + b, 0);
    const avg = sum / count;

    const p50 = this.percentile(values, 0.5);
    const p95 = this.percentile(values, 0.95);
    const p99 = this.percentile(values, 0.99);

    return {
      count,
      min,
      max,
      avg,
      sum,
      p50,
      p95,
      p99
    };
  }

  private percentile(values: number[], p: number): number {
    const index = Math.ceil(values.length * p) - 1;
    return values[Math.max(0, Math.min(index, values.length - 1))];
  }

  // Report generation
  generateReport(since?: number): string {
    const sinceTime = since || Date.now() - 3600000; // Last hour by default
    const relevantMetrics = this.getMetrics(undefined, sinceTime);
    
    if (relevantMetrics.length === 0) {
      return 'No metrics available for the specified time period.';
    }

    const report: string[] = [];
    report.push('=== Performance Report ===');
    report.push(`Time Period: ${new Date(sinceTime).toISOString()} - ${new Date().toISOString()}`);
    report.push(`Total Metrics: ${relevantMetrics.length}`);
    report.push('');

    // Group metrics by name
    const groupedMetrics = new Map<string, PerformanceMetric[]>();
    for (const metric of relevantMetrics) {
      const group = groupedMetrics.get(metric.name) || [];
      group.push(metric);
      groupedMetrics.set(metric.name, group);
    }

    // Generate statistics for each metric
    for (const [name, metrics] of groupedMetrics.entries()) {
      const stats = this.getStatistics(name, sinceTime);
      if (stats) {
        report.push(`${name}:`);
        report.push(`  Count: ${stats.count}`);
        report.push(`  Min: ${stats.min.toFixed(2)} ${metrics[0]?.unit || ''}`);
        report.push(`  Max: ${stats.max.toFixed(2)} ${metrics[0]?.unit || ''}`);
        report.push(`  Avg: ${stats.avg.toFixed(2)} ${metrics[0]?.unit || ''}`);
        report.push(`  P95: ${stats.p95.toFixed(2)} ${metrics[0]?.unit || ''}`);
        report.push('');
      }
    }

    return report.join('\n');
  }

  // Reset methods
  clearMetrics(): void {
    this.metrics.length = 0;
  }

  clearCounters(): void {
    this.counters.clear();
  }

  clearHistograms(): void {
    this.histograms.clear();
  }

  clearTimers(): void {
    this.timers.clear();
  }

  clearAll(): void {
    this.clearMetrics();
    this.clearCounters();
    this.clearHistograms();
    this.clearTimers();
  }

  // Export/Import
  exportData(): {
    metrics: PerformanceMetric[];
    counters: Record<string, number>;
    histograms: Record<string, number[]>;
    } {
    return {
      metrics: [...this.metrics],
      counters: Object.fromEntries(this.counters),
      histograms: Object.fromEntries(this.histograms)
    };
  }

  importData(data: {
    metrics?: PerformanceMetric[];
    counters?: Record<string, number>;
    histograms?: Record<string, number[]>;
  }): void {
    if (data.metrics) {
      this.metrics.push(...data.metrics);
    }

    if (data.counters) {
      for (const [key, value] of Object.entries(data.counters)) {
        this.counters.set(key, value);
      }
    }

    if (data.histograms) {
      for (const [key, values] of Object.entries(data.histograms)) {
        this.histograms.set(key, values);
      }
    }
  }
}

// Singleton instance for global performance monitoring
export const performanceMonitor = new PerformanceMonitor();

// Decorator for performance monitoring
export function monitor(name?: string) {
  return function (target: any, propertyName: string, descriptor: PropertyDescriptor) {
    const method = descriptor.value;
    const metricName = name || `${target.constructor.name}.${propertyName}`;

    descriptor.value = async function (...args: any[]) {
      return performanceMonitor.measureAsync(metricName, async () => {
        return method.apply(this, args);
      });
    };

    return descriptor;
  };
}

// Utility functions
export function formatBytes(bytes: number): string {
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let size = bytes;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex++;
  }

  return `${size.toFixed(2)} ${units[unitIndex]}`;
}

export function formatDuration(ms: number): string {
  if (ms < 1000) {
    return `${ms.toFixed(2)}ms`;
  } else if (ms < 60000) {
    return `${(ms / 1000).toFixed(2)}s`;
  } else {
    return `${(ms / 60000).toFixed(2)}m`;
  }
}
