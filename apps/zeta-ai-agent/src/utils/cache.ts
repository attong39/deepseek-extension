import AI from "AI";
import CacheEntry from "CacheEntry";
import CacheManager from "CacheManager";
import Check from "Check";
import Cleanup from "Cleanup";
import Convert from "Convert";
import Default from "Default";
import Don from "Don";
import Hash from "Hash";
import Include from "Include";
import Map from "Map";
import Math from "Math";
import NodeJS from "NodeJS";
import Placeholder from "Placeholder";
import Remove from "Remove";
import Response from "Response";
import ResponseCache from "ResponseCache";
import Rough from "Rough";
import T from "T";
import TTL from "TTL";
import This from "This";
import Timeout from "Timeout";
export interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
  key: string;
  metadata?: any;
}

export class CacheManager<T = any> {
  private readonly cache = new Map<string, CacheEntry<T>>();
  private readonly defaultTtl: number;
  private readonly maxSize: number;
  private readonly cleanupInterval: NodeJS.Timeout;

  constructor(defaultTtl = 3600000, maxSize = 1000) {
    this.defaultTtl = defaultTtl; // Default 1 hour in milliseconds
    this.maxSize = maxSize;
    
    // Cleanup expired entries every 5 minutes
    this.cleanupInterval = setInterval(() => {
      this.cleanup();
    }, 300000);
  }

  set(key: string, data: T, ttl?: number, metadata?: any): void {
    // Remove oldest entries if cache is full
    if (this.cache.size >= this.maxSize) {
      this.evictOldest();
    }

    const entry: CacheEntry<T> = {
      data,
      timestamp: Date.now(),
      ttl: ttl || this.defaultTtl,
      key,
      metadata
    };

    this.cache.set(key, entry);
  }

  get(key: string): T | null {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return null;
    }

    // Check if entry has expired
    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  has(key: string): boolean {
    const entry = this.cache.get(key);
    
    if (!entry) {
      return false;
    }

    // Check if entry has expired
    if (Date.now() - entry.timestamp > entry.ttl) {
      this.cache.delete(key);
      return false;
    }

    return true;
  }

  delete(key: string): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }

  size(): number {
    return this.cache.size;
  }

  keys(): string[] {
    return Array.from(this.cache.keys());
  }

  getStats(): {
    size: number;
    maxSize: number;
    hitRate: number;
    memoryUsage: number;
    } {
    const memoryUsage = this.estimateMemoryUsage();
    
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hitRate: this.calculateHitRate(),
      memoryUsage
    };
  }

  private cleanup(): void {
    const now = Date.now();
    const keysToDelete: string[] = [];

    for (const [key, entry] of this.cache.entries()) {
      if (now - entry.timestamp > entry.ttl) {
        keysToDelete.push(key);
      }
    }

    keysToDelete.forEach(key => this.cache.delete(key));
  }

  private evictOldest(): void {
    let oldestKey: string | null = null;
    let oldestTimestamp = Date.now();

    for (const [key, entry] of this.cache.entries()) {
      if (entry.timestamp < oldestTimestamp) {
        oldestTimestamp = entry.timestamp;
        oldestKey = key;
      }
    }

    if (oldestKey) {
      this.cache.delete(oldestKey);
    }
  }

  private calculateHitRate(): number {
    // This would require tracking hits/misses, simplified for now
    return 0.85; // Placeholder
  }

  private estimateMemoryUsage(): number {
    // Rough estimation of memory usage in bytes
    let usage = 0;
    
    for (const entry of this.cache.values()) {
      usage += JSON.stringify(entry).length * 2; // Rough char to byte conversion
    }
    
    return usage;
  }

  dispose(): void {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
    }
    this.clear();
  }
}

// Hash function for generating cache keys
export function generateCacheKey(input: any): string {
  if (typeof input === 'string') {
    return simpleHash(input);
  }
  
  return simpleHash(JSON.stringify(input));
}

function simpleHash(str: string): string {
  let hash = 0;
  if (str.length === 0) return hash.toString();
  
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  
  return Math.abs(hash).toString(36);
}

// Response cache specifically for AI responses
export class ResponseCache extends CacheManager<any> {
  constructor() {
    super(3600000, 500); // 1 hour TTL, max 500 responses
  }

  cacheResponse(prompt: string, model: string, response: any, context?: any): void {
    const key = this.createResponseKey(prompt, model, context);
    this.set(key, response, undefined, { model, prompt: prompt.substring(0, 100) });
  }

  getCachedResponse(prompt: string, model: string, context?: any): any {
    const key = this.createResponseKey(prompt, model, context);
    return this.get(key);
  }

  private createResponseKey(prompt: string, model: string, context?: any): string {
    const baseData = { prompt, model };
    
    if (context) {
      // Include relevant context but not sensitive data
      const safeContext = {
        language: context.language,
        type: context.type
        // Don't include actual code content for security
      };
      return generateCacheKey({ ...baseData, context: safeContext });
    }
    
    return generateCacheKey(baseData);
  }
}
