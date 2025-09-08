import { describe, it, expect, beforeEach, afterEach } from '../testRunner';
import { CacheManager, ResponseCache, generateCacheKey } from '../../utils/cache';
import Add from "Add";
import Fill from "Fill";
import First from "First";
import JS from "JS";
import New from "New";
import Python from "Python";
import Response from "Response";
import Should from "Should";
import TTL from "TTL";
import Test from "../../../../desktop/src/Test/index";
import Use from "Use";

describe('CacheManager', () => {
  let cache: CacheManager<string>;

  beforeEach(() => {
    cache = new CacheManager<string>(1000, 10); // 1 second TTL, max 10 items
  });

  afterEach(() => {
    cache.dispose();
  });

  describe('basic operations', () => {
    it('should store and retrieve values', () => {
      cache.set('key1', 'value1');
      expect(cache.get('key1')).toBe('value1');
    });

    it('should return null for non-existent keys', () => {
      expect(cache.get('nonexistent')).toBeNull();
    });

    it('should check if key exists', () => {
      cache.set('key1', 'value1');
      expect(cache.has('key1')).toBe(true);
      expect(cache.has('nonexistent')).toBe(false);
    });

    it('should delete keys', () => {
      cache.set('key1', 'value1');
      expect(cache.delete('key1')).toBe(true);
      expect(cache.get('key1')).toBeNull();
      expect(cache.delete('nonexistent')).toBe(false);
    });

    it('should clear all entries', () => {
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      cache.clear();
      expect(cache.size()).toBe(0);
    });
  });

  describe('TTL functionality', () => {
    it('should expire entries after TTL', async () => {
      cache.set('key1', 'value1', 50); // 50ms TTL
      expect(cache.get('key1')).toBe('value1');
      
      await new Promise(resolve => setTimeout(resolve, 100));
      expect(cache.get('key1')).toBeNull();
    });

    it('should use default TTL when not specified', async () => {
      cache.set('key1', 'value1'); // Use default 1000ms TTL
      expect(cache.get('key1')).toBe('value1');
      
      await new Promise(resolve => setTimeout(resolve, 50));
      expect(cache.get('key1')).toBe('value1'); // Should still exist
    });
  });

  describe('size limits', () => {
    it('should respect max size by evicting oldest entries', () => {
      // Fill cache to max capacity
      for (let i = 0; i < 10; i++) {
        cache.set(`key${i}`, `value${i}`);
      }
      expect(cache.size()).toBe(10);

      // Add one more to trigger eviction
      cache.set('key10', 'value10');
      expect(cache.size()).toBe(10);
      expect(cache.get('key0')).toBeNull(); // First entry should be evicted
      expect(cache.get('key10')).toBe('value10'); // New entry should exist
    });
  });

  describe('statistics', () => {
    it('should return correct stats', () => {
      cache.set('key1', 'value1');
      cache.set('key2', 'value2');
      
      const stats = cache.getStats();
      expect(stats.size).toBe(2);
      expect(stats.maxSize).toBe(10);
      expect(typeof stats.hitRate).toBe('number');
      expect(typeof stats.memoryUsage).toBe('number');
    });
  });

  describe('metadata', () => {
    it('should store metadata with entries', () => {
      const metadata = { source: 'test', priority: 1 };
      cache.set('key1', 'value1', undefined, metadata);
      expect(cache.get('key1')).toBe('value1');
    });
  });
});

describe('ResponseCache', () => {
  let responseCache: ResponseCache;

  beforeEach(() => {
    responseCache = new ResponseCache();
  });

  afterEach(() => {
    responseCache.dispose();
  });

  it('should cache and retrieve responses', () => {
    const prompt = 'Test prompt';
    const model = 'test-model';
    const response = { content: 'Test response' };
    
    responseCache.cacheResponse(prompt, model, response);
    const cached = responseCache.getCachedResponse(prompt, model);
    
    expect(cached).toEqual(response);
  });

  it('should generate different keys for different prompts', () => {
    const model = 'test-model';
    const response1 = { content: 'Response 1' };
    const response2 = { content: 'Response 2' };
    
    responseCache.cacheResponse('prompt1', model, response1);
    responseCache.cacheResponse('prompt2', model, response2);
    
    expect(responseCache.getCachedResponse('prompt1', model)).toEqual(response1);
    expect(responseCache.getCachedResponse('prompt2', model)).toEqual(response2);
  });

  it('should generate different keys for different models', () => {
    const prompt = 'Test prompt';
    const response1 = { content: 'Response 1' };
    const response2 = { content: 'Response 2' };
    
    responseCache.cacheResponse(prompt, 'model1', response1);
    responseCache.cacheResponse(prompt, 'model2', response2);
    
    expect(responseCache.getCachedResponse(prompt, 'model1')).toEqual(response1);
    expect(responseCache.getCachedResponse(prompt, 'model2')).toEqual(response2);
  });

  it('should include context in key generation', () => {
    const prompt = 'Test prompt';
    const model = 'test-model';
    const context1 = { language: 'javascript' };
    const context2 = { language: 'python' };
    const response1 = { content: 'JS Response' };
    const response2 = { content: 'Python Response' };
    
    responseCache.cacheResponse(prompt, model, response1, context1);
    responseCache.cacheResponse(prompt, model, response2, context2);
    
    expect(responseCache.getCachedResponse(prompt, model, context1)).toEqual(response1);
    expect(responseCache.getCachedResponse(prompt, model, context2)).toEqual(response2);
  });
});

describe('generateCacheKey', () => {
  it('should generate consistent keys for same input', () => {
    const input = 'test input';
    const key1 = generateCacheKey(input);
    const key2 = generateCacheKey(input);
    expect(key1).toBe(key2);
  });

  it('should generate different keys for different inputs', () => {
    const key1 = generateCacheKey('input1');
    const key2 = generateCacheKey('input2');
    expect(key1).not.toBe(key2);
  });

  it('should handle object inputs', () => {
    const obj1 = { prop: 'value1' };
    const obj2 = { prop: 'value2' };
    const key1 = generateCacheKey(obj1);
    const key2 = generateCacheKey(obj2);
    expect(key1).not.toBe(key2);
  });

  it('should generate same key for equivalent objects', () => {
    const obj1 = { prop: 'value', num: 42 };
    const obj2 = { prop: 'value', num: 42 };
    const key1 = generateCacheKey(obj1);
    const key2 = generateCacheKey(obj2);
    expect(key1).toBe(key2);
  });
});
