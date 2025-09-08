import { describe, test, expect, beforeEach } from 'vitest';
import { OllamaClient } from '../src/core/ollama/client';
import { CodeAnalyzer } from '../src/core/agent/cognitive/codeAnalyzer';
import { MemoryManager } from '../src/core/agent/memory/memoryManager';
import { ActionPlanner } from '../src/core/agent/planner/actionPlanner';
import { ResponseCache } from '../src/core/utils/cache';
import { InputValidator } from '../src/core/utils/validation';
import { RateLimiter } from '../src/core/utils/rateLimiter';
import { PerformanceMonitor } from '../src/core/utils/monitoring';
import { CodeContext } from '../src/types/shared';
import AI from "AI";
import Agent from "Agent";
import Components from "../apps/desktop/src/Components/index";
import Core from "Core";
import Hello from "Hello";
import URL from "URL";
import World from "World";
import Zeta from "Zeta";

describe('Zeta AI Agent Core Components', () => {
  let ollamaClient: OllamaClient;
  let codeAnalyzer: CodeAnalyzer;
  let memoryManager: MemoryManager;
  let actionPlanner: ActionPlanner;
  let cache: ResponseCache;
  let rateLimiter: RateLimiter;
  let monitor: PerformanceMonitor;

  beforeEach(() => {
    ollamaClient = new OllamaClient('http://localhost:11434');
    codeAnalyzer = new CodeAnalyzer(ollamaClient);
    memoryManager = new MemoryManager();
    actionPlanner = new ActionPlanner(ollamaClient);
    cache = new ResponseCache();
    rateLimiter = new RateLimiter();
    monitor = new PerformanceMonitor();
  });

  describe('OllamaClient', () => {
    test('should initialize with correct URL', () => {
      expect(ollamaClient).toBeDefined();
    });

    test('should list available models', async () => {
      const models = await ollamaClient.listModels();
      expect(Array.isArray(models)).toBe(true);
    });
  });

  describe('CodeAnalyzer', () => {
    test('should analyze code and return review', async () => {
      const code = 'function test() { return true; }';
      const context: CodeContext = {
        language: 'typescript',
        filePath: 'test.ts'
      };
      const review = await codeAnalyzer.reviewCode(code, context);
      expect(review).toHaveProperty('issues');
      expect(review).toHaveProperty('suggestions');
    });
  });

  describe('MemoryManager', () => {
    test('should get relevant context', async () => {
      const query = 'test query';
      const context = await memoryManager.getRelevantContext(query);
      expect(context).toHaveProperty('items');
      expect(context).toHaveProperty('recent_actions');
    });
  });

  describe('ActionPlanner', () => {
    test('should initialize', () => {
      expect(actionPlanner).toBeDefined();
    });
  });

  describe('ResponseCache', () => {
    test('should cache and retrieve responses', async () => {
      const key = 'test-key';
      const value = { result: 'test response' };

      await cache.set(key, value);
      const retrieved = await cache.get(key);
      expect(retrieved).toEqual(value);
    });
  });

  describe('InputValidator', () => {
    test('should validate safe input', () => {
      const safeInput = 'console.log("Hello World");';
      const result = InputValidator.validateCodeInput(safeInput);
      expect(result.valid).toBe(true);
    });

    test('should reject dangerous input', () => {
      const dangerousInput = 'require("child_process").exec("rm -rf /");';
      const result = InputValidator.validateCodeInput(dangerousInput);
      expect(result.valid).toBe(false);
    });
  });

  describe('RateLimiter', () => {
    test('should allow requests within limit', () => {
      const result = rateLimiter.checkRateLimit('test-user');
      expect(result.allowed).toBe(true);
    });
  });

  describe('PerformanceMonitor', () => {
    test('should track operations', () => {
      monitor.startOperation('test-op');
      monitor.endOperation('test-op');
      expect(monitor).toBeDefined();
    });
  });
});
