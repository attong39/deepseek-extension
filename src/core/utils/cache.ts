import Convert from "Convert";
import Failed from "Failed";
import Map from "Map";
import MemoryCache from "MemoryCache";
import PersistentCache from "PersistentCache";
import Remove from "Remove";
import ResponseCache from "ResponseCache";
import Simple from "Simple";
import T from "T";
export class ResponseCache {
  private cache = new Map<string, { response: any; timestamp: number; ttl: number }>();
  private defaultTTL: number;

  constructor(defaultTTL: number = 300000) { // 5 minutes default
    this.defaultTTL = defaultTTL;
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    const cacheKey = this.hashKey(key);
    const cached = this.cache.get(cacheKey);
    const now = Date.now();
    const effectiveTTL = ttl || this.defaultTTL;

    if (cached && (now - cached.timestamp) < cached.ttl) {
      return cached.response;
    }

    const response = await fetcher();
    this.cache.set(cacheKey, {
      response,
      timestamp: now,
      ttl: effectiveTTL
    });

    return response;
  }

  get<T>(key: string): T | undefined {
    const cacheKey = this.hashKey(key);
    const cached = this.cache.get(cacheKey);

    if (cached && (Date.now() - cached.timestamp) < cached.ttl) {
      return cached.response;
    }

    // Remove expired entry
    if (cached) {
      this.cache.delete(cacheKey);
    }

    return undefined;
  }

  set<T>(key: string, value: T, ttl?: number): void {
    const cacheKey = this.hashKey(key);
    this.cache.set(cacheKey, {
      response: value,
      timestamp: Date.now(),
      ttl: ttl || this.defaultTTL
    });
  }

  delete(key: string): boolean {
    const cacheKey = this.hashKey(key);
    return this.cache.delete(cacheKey);
  }

  clear(): void {
    this.cache.clear();
  }

  size(): number {
    return this.cache.size;
  }

  cleanup(): void {
    const now = Date.now();
    for (const [key, value] of this.cache.entries()) {
      if ((now - value.timestamp) >= value.ttl) {
        this.cache.delete(key);
      }
    }
  }

  private hashKey(key: string): string {
    // Simple hash function for cache keys
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      const char = key.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return hash.toString();
  }
}

export class MemoryCache extends ResponseCache {
  constructor() {
    super(1800000); // 30 minutes for memory cache
  }
}

export class PersistentCache {
  private cache = new Map<string, any>();
  private filePath: string;

  constructor(filePath: string = './.zeta-cache.json') {
    this.filePath = filePath;
    this.loadFromFile();
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    const cached = this.get<T>(key);
    if (cached !== undefined) {
      return cached;
    }

    const response = await fetcher();
    this.set(key, response, ttl);
    return response;
  }

  get<T>(key: string): T | undefined {
    const item = this.cache.get(key);
    if (!item) return undefined;

    const now = Date.now();
    if (item.expiry && now > item.expiry) {
      this.delete(key);
      return undefined;
    }

    return item.value;
  }

  set<T>(key: string, value: T, ttl?: number): void {
    const expiry = ttl ? Date.now() + ttl : undefined;
    this.cache.set(key, { value, expiry });
    this.saveToFile();
  }

  delete(key: string): boolean {
    const deleted = this.cache.delete(key);
    if (deleted) {
      this.saveToFile();
    }
    return deleted;
  }

  clear(): void {
    this.cache.clear();
    this.saveToFile();
  }

  private loadFromFile(): void {
    try {
      const fs = require('fs');
      if (fs.existsSync(this.filePath)) {
        const data = fs.readFileSync(this.filePath, 'utf8');
        const parsed = JSON.parse(data);
        this.cache = new Map(Object.entries(parsed));
      }
    } catch (error) {
      console.warn('Failed to load cache from file:', error);
    }
  }

  private saveToFile(): void {
    try {
      const fs = require('fs');
      const data = Object.fromEntries(this.cache);
      fs.writeFileSync(this.filePath, JSON.stringify(data, null, 2));
    } catch (error) {
      console.warn('Failed to save cache to file:', error);
    }
  }
}
