import AI from "AI";
import AdaptiveRateLimiter from "AdaptiveRateLimiter";
import Add from "Add";
import Adjust from "Adjust";
import BurstRateLimiter from "BurstRateLimiter";
import Default from "Default";
import Exponential from "Exponential";
import Map from "Map";
import Math from "Math";
import More from "More";
import RateLimiter from "./RateLimiter";
import Remove from "Remove";
export class RateLimiter {
  private requests = new Map<string, number[]>();
  private limits: Map<string, { maxRequests: number; windowMs: number }>;

  constructor() {
    this.limits = new Map();
    // Default limits
    this.setLimit('default', 60, 60000); // 60 requests per minute
    this.setLimit('ai_chat', 30, 60000); // 30 AI chats per minute
    this.setLimit('code_review', 10, 60000); // 10 code reviews per minute
    this.setLimit('file_operations', 100, 60000); // 100 file operations per minute
  }

  setLimit(
    key: string,
    maxRequests: number,
    windowMs: number
  ): void {
    this.limits.set(key, { maxRequests, windowMs });
  }

  checkRateLimit(
    identifier: string,
    limitKey: string = 'default'
  ): { allowed: boolean; remaining: number; resetTime: number } {
    const limit = this.limits.get(limitKey);
    if (!limit) {
      return { allowed: true, remaining: 0, resetTime: 0 };
    }

    const now = Date.now();
    const key = `${limitKey}:${identifier}`;

    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }

    const timestamps = this.requests.get(key)!;

    // Remove old timestamps outside the window
    const validTimestamps = timestamps.filter(
      ts => now - ts < limit.windowMs
    );

    if (validTimestamps.length >= limit.maxRequests) {
      const oldestTimestamp = Math.min(...validTimestamps);
      const resetTime = oldestTimestamp + limit.windowMs;
      return {
        allowed: false,
        remaining: 0,
        resetTime
      };
    }

    // Add current request
    validTimestamps.push(now);
    this.requests.set(key, validTimestamps);

    const remaining = limit.maxRequests - validTimestamps.length;
    const resetTime = now + limit.windowMs;

    return {
      allowed: true,
      remaining,
      resetTime
    };
  }

  getRemainingRequests(identifier: string, limitKey: string = 'default'): number {
    return this.checkRateLimit(identifier, limitKey).remaining;
  }

  getResetTime(identifier: string, limitKey: string = 'default'): number {
    return this.checkRateLimit(identifier, limitKey).resetTime;
  }

  isAllowed(identifier: string, limitKey: string = 'default'): boolean {
    return this.checkRateLimit(identifier, limitKey).allowed;
  }

  reset(identifier: string, limitKey: string = 'default'): void {
    const key = `${limitKey}:${identifier}`;
    this.requests.delete(key);
  }

  resetAll(): void {
    this.requests.clear();
  }

  getStats(): { [key: string]: { activeRequests: number; limits: any } } {
    const stats: { [key: string]: { activeRequests: number; limits: any } } = {};

    for (const [limitKey, limit] of this.limits) {
      stats[limitKey] = {
        activeRequests: 0,
        limits: limit
      };
    }

    for (const [key, timestamps] of this.requests) {
      const [limitKey] = key.split(':');
      if (stats[limitKey]) {
        stats[limitKey].activeRequests += timestamps.length;
      }
    }

    return stats;
  }

  cleanup(): void {
    const now = Date.now();

    for (const [key, timestamps] of this.requests) {
      const limit = this.limits.get(key.split(':')[0]);
      if (limit) {
        const validTimestamps = timestamps.filter(
          ts => now - ts < limit.windowMs
        );

        if (validTimestamps.length === 0) {
          this.requests.delete(key);
        } else {
          this.requests.set(key, validTimestamps);
        }
      }
    }
  }
}

export class BurstRateLimiter extends RateLimiter {
  constructor() {
    super();
    // More restrictive burst limits
    this.setLimit('burst_ai_chat', 5, 10000); // 5 requests per 10 seconds
    this.setLimit('burst_file_ops', 20, 10000); // 20 file operations per 10 seconds
  }
}

export class AdaptiveRateLimiter extends RateLimiter {
  private successRates = new Map<string, number>();
  private adjustmentFactor = 0.1;

  checkRateLimit(
    identifier: string,
    limitKey: string = 'default'
  ): { allowed: boolean; remaining: number; resetTime: number; adjustedLimit?: number } {
    const baseResult = super.checkRateLimit(identifier, limitKey);
    const successRate = this.successRates.get(`${limitKey}:${identifier}`) || 1.0;

    // Adjust limit based on success rate
    const limit = this['limits'].get(limitKey);
    if (limit) {
      const adjustedMaxRequests = Math.max(
        1,
        Math.round(limit.maxRequests * (0.5 + successRate * 0.5))
      );

      return {
        ...baseResult,
        adjustedLimit: adjustedMaxRequests
      };
    }

    return baseResult;
  }

  recordResult(identifier: string, limitKey: string, success: boolean): void {
    const key = `${limitKey}:${identifier}`;
    const currentRate = this.successRates.get(key) || 1.0;

    // Exponential moving average
    const newRate = currentRate * (1 - this.adjustmentFactor) +
                   (success ? 1 : 0) * this.adjustmentFactor;

    this.successRates.set(key, newRate);
  }
}
