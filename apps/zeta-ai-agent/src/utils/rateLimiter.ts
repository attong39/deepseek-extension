import API from "../../../desktop/src/API/index";
import APIRateLimiter from "APIRateLimiter";
import Add from "Add";
import BurstRateLimiter from "BurstRateLimiter";
import Clean from "Clean";
import Decorator from "Decorator";
import Error from "Error";
import Filter from "Filter";
import Get from "Get";
import Map from "Map";
import Math from "Math";
import Maximum from "Maximum";
import OperationRateLimiter from "OperationRateLimiter";
import Please from "Please";
import PropertyDescriptor from "PropertyDescriptor";
import Rate from "Rate";
import RateLimitConfig from "RateLimitConfig";
import RateLimitError from "RateLimitError";
import RateLimitInfo from "RateLimitInfo";
import RateLimiter from "./RateLimiter";
import Record from "Record";
import RequestRecord from "RequestRecord";
import Specialized from "Specialized";
import Time from "Time";
import Too from "Too";
import Update from "Update";
import User from "User";
import UserRateLimiter from "UserRateLimiter";
import Utility from "Utility";
export interface RateLimitConfig {
  windowMs: number; // Time window in milliseconds
  maxRequests: number; // Maximum requests per window
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
  message?: string;
}

export interface RateLimitInfo {
  total: number;
  remaining: number;
  resetTime: number;
  limit: number;
}

interface RequestRecord {
  timestamp: number;
  success: boolean;
}

export class RateLimiter {
  private readonly requests = new Map<string, RequestRecord[]>();
  private readonly config: RateLimitConfig;

  constructor(config: RateLimitConfig) {
    this.config = {
      message: 'Too many requests, please try again later.',
      ...config
    };

    // Clean up old records every minute
    setInterval(() => {
      this.cleanup();
    }, 60000);
  }

  async checkLimit(key: string): Promise<{ allowed: boolean; info: RateLimitInfo }> {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;
    
    // Get or create request history for this key
    let requestHistory = this.requests.get(key) || [];
    
    // Filter out old requests
    requestHistory = requestHistory.filter(req => req.timestamp > windowStart);
    
    // Filter based on configuration
    let filteredRequests = requestHistory;
    if (this.config.skipSuccessfulRequests && this.config.skipFailedRequests) {
      filteredRequests = [];
    } else if (this.config.skipSuccessfulRequests) {
      filteredRequests = requestHistory.filter(req => !req.success);
    } else if (this.config.skipFailedRequests) {
      filteredRequests = requestHistory.filter(req => req.success);
    }

    const requestCount = filteredRequests.length;
    const allowed = requestCount < this.config.maxRequests;
    
    const info: RateLimitInfo = {
      total: requestCount,
      remaining: Math.max(0, this.config.maxRequests - requestCount),
      resetTime: windowStart + this.config.windowMs,
      limit: this.config.maxRequests
    };

    return { allowed, info };
  }

  async recordRequest(key: string, success = true): Promise<void> {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;
    
    // Get or create request history
    let requestHistory = this.requests.get(key) || [];
    
    // Add new request
    requestHistory.push({ timestamp: now, success });
    
    // Filter out old requests
    requestHistory = requestHistory.filter(req => req.timestamp > windowStart);
    
    // Update the map
    this.requests.set(key, requestHistory);
  }

  async consume(key: string): Promise<{ allowed: boolean; info: RateLimitInfo }> {
    const result = await this.checkLimit(key);
    
    if (result.allowed) {
      await this.recordRequest(key, true);
      // Update the remaining count after recording
      result.info.remaining = Math.max(0, result.info.remaining - 1);
    }
    
    return result;
  }

  async reset(key: string): Promise<void> {
    this.requests.delete(key);
  }

  async resetAll(): Promise<void> {
    this.requests.clear();
  }

  getStats(): {
    totalKeys: number;
    totalRequests: number;
    averageRequestsPerKey: number;
    } {
    const totalKeys = this.requests.size;
    let totalRequests = 0;
    
    for (const history of this.requests.values()) {
      totalRequests += history.length;
    }
    
    return {
      totalKeys,
      totalRequests,
      averageRequestsPerKey: totalKeys > 0 ? totalRequests / totalKeys : 0
    };
  }

  private cleanup(): void {
    const now = Date.now();
    const cutoff = now - this.config.windowMs;
    
    for (const [key, history] of this.requests.entries()) {
      const filteredHistory = history.filter(req => req.timestamp > cutoff);
      
      if (filteredHistory.length === 0) {
        this.requests.delete(key);
      } else {
        this.requests.set(key, filteredHistory);
      }
    }
  }
}

// Specialized rate limiters for different use cases
export class APIRateLimiter extends RateLimiter {
  constructor(requestsPerMinute = 60) {
    super({
      windowMs: 60 * 1000, // 1 minute
      maxRequests: requestsPerMinute,
      message: 'API rate limit exceeded. Please wait before making more requests.'
    });
  }
}

export class UserRateLimiter extends RateLimiter {
  constructor(requestsPerHour = 100) {
    super({
      windowMs: 60 * 60 * 1000, // 1 hour
      maxRequests: requestsPerHour,
      message: 'User rate limit exceeded. Please try again later.'
    });
  }
}

export class BurstRateLimiter extends RateLimiter {
  constructor(requestsPerSecond = 10) {
    super({
      windowMs: 1000, // 1 second
      maxRequests: requestsPerSecond,
      message: 'Too many requests in a short time. Please slow down.'
    });
  }
}

// Rate limiter for specific operations
export class OperationRateLimiter {
  private readonly limiters = new Map<string, RateLimiter>();
  
  constructor(private readonly defaultConfig: RateLimitConfig) {}

  getLimiter(operation: string, config?: RateLimitConfig): RateLimiter {
    if (!this.limiters.has(operation)) {
      this.limiters.set(operation, new RateLimiter(config || this.defaultConfig));
    }
    return this.limiters.get(operation)!;
  }

  async checkLimit(operation: string, key: string, config?: RateLimitConfig): Promise<{ allowed: boolean; info: RateLimitInfo }> {
    const limiter = this.getLimiter(operation, config);
    return limiter.checkLimit(key);
  }

  async consume(operation: string, key: string, config?: RateLimitConfig): Promise<{ allowed: boolean; info: RateLimitInfo }> {
    const limiter = this.getLimiter(operation, config);
    return limiter.consume(key);
  }

  async reset(operation: string, key: string): Promise<void> {
    const limiter = this.limiters.get(operation);
    if (limiter) {
      await limiter.reset(key);
    }
  }

  async resetAll(): Promise<void> {
    for (const limiter of this.limiters.values()) {
      await limiter.resetAll();
    }
  }

  getOperationStats(): Record<string, any> {
    const stats: Record<string, any> = {};
    
    for (const [operation, limiter] of this.limiters.entries()) {
      stats[operation] = limiter.getStats();
    }
    
    return stats;
  }
}

// Error class for rate limit exceeded
export class RateLimitError extends Error {
  public retryAfter: number;
  public limit: number;
  public current: number;

  constructor(message: string, retryAfter: number, limit: number, current: number) {
    super(message);
    this.name = 'RateLimitError';
    this.retryAfter = retryAfter;
    this.limit = limit;
    this.current = current;
  }
}

// Utility function to create a rate limit key
export function createRateLimitKey(userId: string, operation?: string, resource?: string): string {
  const parts = [userId];
  if (operation) parts.push(operation);
  if (resource) parts.push(resource);
  return parts.join(':');
}

// Decorator for rate limiting methods
export function rateLimit(limiter: RateLimiter, keyExtractor: (args: any[]) => string) {
  return function (target: any, propertyName: string, descriptor: PropertyDescriptor) {
    const method = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const key = keyExtractor(args);
      const result = await limiter.consume(key);
      
      if (!result.allowed) {
        throw new RateLimitError(
          'Rate limit exceeded',
          result.info.resetTime,
          result.info.limit,
          result.info.total
        );
      }
      
      try {
        const methodResult = await method.apply(this, args);
        await limiter.recordRequest(key, true);
        return methodResult;
      } catch (error) {
        await limiter.recordRequest(key, false);
        throw error;
      }
    };

    return descriptor;
  };
}
