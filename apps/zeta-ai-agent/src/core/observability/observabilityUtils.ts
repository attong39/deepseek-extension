/**
 * Observability Utils
 * Helper functions and decorators for easy observability integration
 */

import { ObservabilitySystem, LogLevel, SpanType } from './observabilitySystem';
import AbortSignal from "AbortSignal";
import Add from "Add";
import COMPLETED from "COMPLETED";
import COUNTER from "COUNTER";
import Class from "Class";
import Common from "Common";
import Completed from "Completed";
import Create from "Create";
import DEBUG from "DEBUG";
import DEGRADED from "DEGRADED";
import ERROR from "ERROR";
import Error from "Error";
import Execute from "Execute";
import Execution from "Execution";
import Export from "Export";
import FAILED from "FAILED";
import FATAL from "FATAL";
import Failed from "Failed";
import Finish from "Finish";
import GAUGE from "GAUGE";
import Get from "Get";
import HEAD from "HEAD";
import HEALTHY from "HEALTHY";
import HISTOGRAM from "HISTOGRAM";
import HTTP from "HTTP";
import Health from "Health";
import HealthCheckUtils from "HealthCheckUtils";
import Helper from "Helper";
import INFO from "INFO";
import Initialize from "Initialize";
import Logger from "Logger";
import Method from "Method";
import Metrics from "Metrics";
import MetricsRecorder from "MetricsRecorder";
import Monitor from "Monitor";
import Observability from "Observability";
import ObservabilityPatterns from "ObservabilityPatterns";
import OperationLogger from "OperationLogger";
import Performance from "Performance";
import PerformanceMonitoringUtils from "PerformanceMonitoringUtils";
import PropertyDescriptor from "PropertyDescriptor";
import Record from "Record";
import SYSTEM_OPERATION from "SYSTEM_OPERATION";
import Singleton from "Singleton";
import Standard from "Standard";
import Start from "Start";
import Starting from "Starting";
import System from "System";
import T from "T";
import TIMER from "TIMER";
import Timed from "Timed";
import TraceLogger from "TraceLogger";
import Traced from "Traced";
import Tracer from "Tracer";
import UNHEALTHY from "UNHEALTHY";
import Utils from "../../../../desktop/src/Utils/index";
import WARN from "WARN";
import WithLogger from "WithLogger";

/**
 * Singleton observability instance
 */
let globalObservability: ObservabilitySystem | null = null;

/**
 * Initialize global observability system
 */
export function initializeObservability(): ObservabilitySystem {
  globalObservability ??= new ObservabilitySystem();
  return globalObservability;
}

/**
 * Get global observability instance
 */
export function getObservability(): ObservabilitySystem {
  return globalObservability ?? initializeObservability();
}

/**
 * Logger wrapper for easy structured logging
 */
export class Logger {
  constructor(protected readonly component: string) {}

  debug(message: string, metadata?: Record<string, any>, operation?: string): void {
    this.log('DEBUG', message, metadata, operation);
  }

  info(message: string, metadata?: Record<string, any>, operation?: string): void {
    this.log('INFO', message, metadata, operation);
  }

  warn(message: string, metadata?: Record<string, any>, operation?: string): void {
    this.log('WARN', message, metadata, operation);
  }

  error(message: string, error?: Error, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('ERROR', message, {
      component: this.component,
      operation
    }, metadata || {}, error);
  }

  fatal(message: string, error?: Error, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('FATAL', message, {
      component: this.component,
      operation
    }, metadata || {}, error);
  }

  private log(level: LogLevel, message: string, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log(level, message, {
      component: this.component,
      operation
    }, metadata || {});
  }

  /**
   * Create child logger with operation context
   */
  withOperation(operation: string): Logger {
    return new OperationLogger(this.component, operation);
  }

  /**
   * Create child logger with trace context
   */
  withTrace(traceId: string, spanId?: string): Logger {
    return new TraceLogger(this.component, traceId, spanId);
  }
}

/**
 * Logger with operation context
 */
class OperationLogger extends Logger {
  constructor(
    component: string,
    private readonly operation: string
  ) {
    super(component);
  }

  debug(message: string, metadata?: Record<string, any>): void {
    super.debug(message, metadata, this.operation);
  }

  info(message: string, metadata?: Record<string, any>): void {
    super.info(message, metadata, this.operation);
  }

  warn(message: string, metadata?: Record<string, any>): void {
    super.warn(message, metadata, this.operation);
  }

  error(message: string, error?: Error, metadata?: Record<string, any>): void {
    super.error(message, error, metadata, this.operation);
  }

  fatal(message: string, error?: Error, metadata?: Record<string, any>): void {
    super.fatal(message, error, metadata, this.operation);
  }
}

/**
 * Logger with trace context
 */
class TraceLogger extends Logger {
  constructor(
    component: string,
    private readonly traceId: string,
    private readonly spanId?: string
  ) {
    super(component);
  }

  debug(message: string, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('DEBUG', message, {
      component: this.component,
      operation,
      traceId: this.traceId,
      spanId: this.spanId
    }, metadata || {});
  }

  info(message: string, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('INFO', message, {
      component: this.component,
      operation,
      traceId: this.traceId,
      spanId: this.spanId
    }, metadata || {});
  }

  warn(message: string, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('WARN', message, {
      component: this.component,
      operation,
      traceId: this.traceId,
      spanId: this.spanId
    }, metadata || {});
  }

  error(message: string, error?: Error, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('ERROR', message, {
      component: this.component,
      operation,
      traceId: this.traceId,
      spanId: this.spanId
    }, metadata || {}, error);
  }

  fatal(message: string, error?: Error, metadata?: Record<string, any>, operation?: string): void {
    const obs = getObservability();
    obs.log('FATAL', message, {
      component: this.component,
      operation,
      traceId: this.traceId,
      spanId: this.spanId
    }, metadata || {}, error);
  }
}

/**
 * Tracer for distributed tracing
 */
export class Tracer {
  constructor(private readonly component: string) {}

  /**
   * Start a new trace span
   */
  startSpan(
    operationName: string,
    spanType: SpanType,
    parentSpanId?: string,
    tags?: Record<string, string>
  ): string {
    const obs = getObservability();
    return obs.startTrace(operationName, spanType, parentSpanId, {
      component: this.component,
      ...tags
    });
  }

  /**
   * Finish a trace span
   */
  finishSpan(spanId: string, status: 'COMPLETED' | 'FAILED' = 'COMPLETED', error?: Error): void {
    const obs = getObservability();
    obs.finishTrace(spanId, status, error);
  }

  /**
   * Add log to trace span
   */
  addSpanLog(spanId: string, level: LogLevel, message: string, fields?: Record<string, any>): void {
    const obs = getObservability();
    obs.addTraceLog(spanId, level, message, fields);
  }

  /**
   * Execute function with automatic tracing
   */
  async withSpan<T>(
    operationName: string,
    spanType: SpanType,
    fn: (spanId: string, logger: TraceLogger) => Promise<T>,
    parentSpanId?: string,
    tags?: Record<string, string>
  ): Promise<T> {
    const spanId = this.startSpan(operationName, spanType, parentSpanId, tags);
    const logger = new TraceLogger(this.component, spanId, spanId);
    
    try {
      logger.info(`Starting ${operationName}`, { spanType, tags });
      const result = await fn(spanId, logger);
      logger.info(`Completed ${operationName}`, { success: true });
      this.finishSpan(spanId, 'COMPLETED');
      return result;
    } catch (error) {
      logger.error(`Failed ${operationName}`, error as Error, { success: false });
      this.finishSpan(spanId, 'FAILED', error as Error);
      throw error;
    }
  }
}

/**
 * Metrics recorder
 */
export class MetricsRecorder {
  constructor(private readonly component: string) {}

  /**
   * Record a counter metric
   */
  counter(name: string, value = 1, labels?: Record<string, string>): void {
    const obs = getObservability();
    obs.recordMetric(name, 'COUNTER', value, {
      component: this.component,
      ...labels
    });
  }

  /**
   * Record a gauge metric
   */
  gauge(name: string, value: number, labels?: Record<string, string>): void {
    const obs = getObservability();
    obs.recordMetric(name, 'GAUGE', value, {
      component: this.component,
      ...labels
    });
  }

  /**
   * Record a histogram metric
   */
  histogram(name: string, value: number, labels?: Record<string, string>): void {
    const obs = getObservability();
    obs.recordMetric(name, 'HISTOGRAM', value, {
      component: this.component,
      ...labels
    });
  }

  /**
   * Record execution time
   */
  timer<T>(name: string, fn: () => T, labels?: Record<string, string>): T;
  timer<T>(name: string, fn: () => Promise<T>, labels?: Record<string, string>): Promise<T>;
  timer<T>(name: string, fn: () => T | Promise<T>, labels?: Record<string, string>): T | Promise<T> {
    const startTime = Date.now();
    
    const recordTime = () => {
      const duration = Date.now() - startTime;
      const obs = getObservability();
      obs.recordMetric(name, 'TIMER', duration, {
        component: this.component,
        ...labels
      }, 'ms', `Execution time for ${name}`);
    };

    try {
      const result = fn();
      
      if (result instanceof Promise) {
        return result
          .then(value => {
            recordTime();
            return value;
          })
          .catch(error => {
            recordTime();
            throw error;
          });
      } else {
        recordTime();
        return result;
      }
    } catch (error) {
      recordTime();
      throw error;
    }
  }
}

/**
 * Method decorator for automatic tracing
 */
export function Traced(
  operationName?: string,
  spanType: SpanType = 'SYSTEM_OPERATION',
  tags?: Record<string, string>
) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    const className = target.constructor.name;
    const finalOperationName = operationName || `${className}.${propertyKey}`;

    descriptor.value = async function (...args: any[]) {
      const tracer = new Tracer(className);
      
      return tracer.withSpan(
        finalOperationName,
        spanType,
        async (spanId, logger) => {
          logger.debug('Method invocation', { 
            method: propertyKey,
            args: args.length,
            tags 
          });
          
          return originalMethod.apply(this, args);
        },
        undefined,
        tags
      );
    };

    return descriptor;
  };
}

/**
 * Method decorator for automatic metrics recording
 */
export function Timed(metricName?: string, labels?: Record<string, string>) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    const className = target.constructor.name;
    const finalMetricName = metricName || `${className.toLowerCase()}.${propertyKey}.duration`;

    descriptor.value = function (...args: any[]) {
      const metrics = new MetricsRecorder(className);
      
      return metrics.timer(finalMetricName, () => {
        return originalMethod.apply(this, args);
      }, labels);
    };

    return descriptor;
  };
}

/**
 * Class decorator for automatic logger injection
 */
export function WithLogger(component?: string) {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    return class extends constructor {
      public readonly logger: Logger;

      constructor(...args: any[]) {
        super(...args);
        this.logger = new Logger(component || constructor.name);
      }
    };
  };
}

/**
 * Health check utilities
 */
export class HealthCheckUtils {
  /**
   * Create a simple ping health check
   */
  static ping(component: string): () => Promise<any> {
    return async () => ({
      status: 'HEALTHY' as const,
      message: `${component} is responsive`,
      duration: 1
    });
  }

  /**
   * Create a database connection health check
   */
  static database(component: string, testQuery: () => Promise<void>): () => Promise<any> {
    return async () => {
      const startTime = Date.now();
      try {
        await testQuery();
        return {
          status: 'HEALTHY' as const,
          message: `${component} database connection is healthy`,
          duration: Date.now() - startTime
        };
      } catch (error) {
        return {
          status: 'UNHEALTHY' as const,
          message: `${component} database connection failed: ${(error as Error).message}`,
          duration: Date.now() - startTime
        };
      }
    };
  }

  /**
   * Create a HTTP endpoint health check
   */
  static httpEndpoint(component: string, url: string): () => Promise<any> {
    return async () => {
      const startTime = Date.now();
      try {
        const response = await fetch(url, { 
          method: 'HEAD',
          signal: AbortSignal.timeout(5000)
        });
        
        const statusValue = response.ok ? 'HEALTHY' : 'DEGRADED';
        return {
          status: statusValue,
          message: `${component} endpoint returned ${response.status}`,
          duration: Date.now() - startTime,
          details: { statusCode: response.status, url }
        };
      } catch (error) {
        return {
          status: 'UNHEALTHY' as const,
          message: `${component} endpoint unreachable: ${(error as Error).message}`,
          duration: Date.now() - startTime,
          details: { url, error: (error as Error).message }
        };
      }
    };
  }
}

/**
 * Performance monitoring utilities
 */
export class PerformanceMonitoringUtils {
  /**
   * Monitor function execution performance
   */
  static async monitorFunction<T>(
    functionName: string,
    component: string,
    fn: () => Promise<T>
  ): Promise<T> {
    const tracer = new Tracer(component);
    const metrics = new MetricsRecorder(component);

    return tracer.withSpan(
      functionName,
      'SYSTEM_OPERATION',
      async (spanId, traceLogger) => {
        const startTime = Date.now();
        
        try {
          traceLogger.info(`Starting ${functionName}`, { startTime });
          
          const result = await fn();
          
          const duration = Date.now() - startTime;
          metrics.timer(`${functionName}.success.duration`, () => duration);
          metrics.counter(`${functionName}.success.count`);
          
          traceLogger.info(`Completed ${functionName}`, { 
            duration,
            success: true 
          });
          
          return result;
        } catch (error) {
          const duration = Date.now() - startTime;
          metrics.timer(`${functionName}.error.duration`, () => duration);
          metrics.counter(`${functionName}.error.count`);
          
          traceLogger.error(`Failed ${functionName}`, error as Error, { 
            duration,
            success: false 
          });
          
          throw error;
        }
      }
    );
  }

  /**
   * Create a performance baseline
   */
  static createBaseline(
    metricName: string,
    component: string,
    sampleData: number[]
  ): void {
    const obs = getObservability();
    
    sampleData.forEach(value => {
      obs.recordMetric(metricName, 'HISTOGRAM', value, {
        component,
        baseline: 'true'
      });
    });
  }
}

/**
 * Common observability patterns
 */
export const ObservabilityPatterns = {
  /**
   * Standard component initialization pattern
   */
  initializeComponent: (component: string) => ({
    logger: new Logger(component),
    tracer: new Tracer(component),
    metrics: new MetricsRecorder(component)
  }),

  /**
   * Standard error handling pattern
   */
  handleError: (
    error: Error,
    logger: Logger,
    operation: string,
    metadata?: Record<string, any>
  ) => {
    logger.error(`Error in ${operation}: ${error.message}`, error, {
      operation,
      errorType: error.constructor.name,
      ...metadata
    });
  },

  /**
   * Standard performance monitoring pattern
   */
  monitorPerformance: async <T>(
    operation: string,
    component: string,
    fn: () => Promise<T>
  ): Promise<T> => {
    return PerformanceMonitoringUtils.monitorFunction(operation, component, fn);
  }
};

/**
 * Export commonly used instances
 */
export const systemLogger = new Logger('System');
export const systemTracer = new Tracer('System');
export const systemMetrics = new MetricsRecorder('System');
