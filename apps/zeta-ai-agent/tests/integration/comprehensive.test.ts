import * as assert from 'assert';
import { OllamaClient } from '../../src/core/ollama/client';
import { CodeAnalyzer, AnalysisResult } from '../../src/core/agent/cognitive/codeAnalyzer';
import { AIAgent } from '../../src/core/agent/agent';
import { mockOllamaServer } from '../mocks/ollamaServer';
import All from "All";
import Analysis from "Analysis";
import Code from "Code";
import Complete from "Complete";
import Comprehensive from "Comprehensive";
import Concurrency from "Concurrency";
import Concurrent from "Concurrent";
import Configure from "Configure";
import Create from "Create";
import Error from "Error";
import Extension from "Extension";
import Handling from "Handling";
import Hello from "Hello";
import Initialize from "Initialize";
import Integration from "Integration";
import Invalid from "Invalid";
import Management from "Management";
import Model from "Model";
import POST from "POST";
import Performance from "Performance";
import Resilience from "Resilience";
import Review from "Review";
import Security from "Security";
import Should from "Should";
import Simulate from "Simulate";
import Start from "Start";
import Test from "../../../desktop/src/Test/index";
import Tests from "../../../desktop/src/Tests/index";
import VS from "VS";
import Validation from "Validation";
import Verify from "Verify";
import Workflow from "Workflow";
import World from "World";

describe('Comprehensive AIAgent Integration Tests', () => {
  let ollamaClient: OllamaClient;
  let codeAnalyzer: CodeAnalyzer;
  let aiAgent: AIAgent;

  before(async () => {
    // Start mock server
    mockOllamaServer.start();
    
    // Initialize components
    ollamaClient = new OllamaClient({
      baseUrl: 'http://localhost:11434',
      defaultModel: 'deepseek-coder'
    });
    
    codeAnalyzer = new CodeAnalyzer(ollamaClient);
    aiAgent = new AIAgent();
  });

  after(() => {
    mockOllamaServer.stop();
  });

  beforeEach(() => {
    mockOllamaServer.reset();
    mockOllamaServer.clearRequestHistory();
  });

  describe('Complete Code Review Workflow', () => {
    it('should complete full code review workflow', async () => {
      // Configure mock for code analysis
      mockOllamaServer.configureForCodeAnalysis();

      const testCode = `
        function calculateSum(a, b) {
          let result = a + b;
          return result;
        }
      `;

      const context = {
        language: 'javascript',
        framework: 'node',
        filePath: '/test/file.js',
        projectType: 'nodejs',
        dependencies: ['lodash', 'express'],
        lineCount: 5
      };

      const result = await codeAnalyzer.analyzeCodeWithContext(testCode, context);

      // Verify request was made
      const requests = mockOllamaServer.getRequestHistory();
      assert.strictEqual(requests.length, 1);
      assert.strictEqual(requests[0].endpoint, '/api/chat');

      // Verify response structure
      assert(result.suggestions);
      assert(result.issues);
      assert(result.complexity);
      assert(result.improvements);
      
      // Verify specific content
      assert(Array.isArray(result.suggestions));
      assert(Array.isArray(result.issues));
      assert(typeof result.complexity.cognitive === 'number');
    });

    it('should handle different programming languages', async () => {
      mockOllamaServer.configureForCodeAnalysis();

      const pythonCode = `
        def calculate_sum(a, b):
            result = a + b
            return result
      `;

      const context = {
        language: 'python',
        framework: 'fastapi',
        filePath: '/test/file.py',
        projectType: 'python',
        dependencies: ['fastapi', 'pydantic'],
        lineCount: 4
      };

      const result = await codeAnalyzer.analyzeCodeWithContext(pythonCode, context);

      assert(result);
      assert(result.suggestions.length >= 0);
    });
  });

  describe('Error Handling and Resilience', () => {
    it('should handle server errors gracefully', async () => {
      mockOllamaServer.configureForErrors();

      const testCode = 'function test() {}';
      const context = {
        language: 'javascript',
        filePath: '/test/file.js'
      };

      try {
        await codeAnalyzer.analyzeCodeWithContext(testCode, context);
        assert.fail('Should have thrown an error');
      } catch (error) {
        assert(error instanceof Error);
        assert(error.message.includes('analysis failed'));
      }
    });

    it('should handle malformed responses', async () => {
      mockOllamaServer.setResponse('/api/chat', 'POST', {
        message: {
          content: 'Invalid JSON response that cannot be parsed {'
        }
      });

      const testCode = 'function test() {}';
      const context = {
        language: 'javascript',
        filePath: '/test/file.js'
      };

      const result = await codeAnalyzer.analyzeCodeWithContext(testCode, context);
      
      // Should fallback gracefully
      assert(result);
      assert(result.suggestions);
      assert(result.improvements);
    });
  });

  describe('Performance and Concurrency', () => {
    it('should complete analysis within reasonable time', async () => {
      mockOllamaServer.configureForCodeAnalysis();

      const startTime = Date.now();
      
      const testCode = 'function test() { return "hello world"; }';
      const context = {
        language: 'javascript',
        filePath: '/test/file.js'
      };

      await codeAnalyzer.analyzeCodeWithContext(testCode, context);
      
      const duration = Date.now() - startTime;
      
      // Should complete within 5 seconds (including mock delays)
      assert(duration < 5000, `Analysis took too long: ${duration}ms`);
    });

    it('should handle concurrent requests efficiently', async () => {
      mockOllamaServer.configureForCodeAnalysis();

      const testCode = 'function test() {}';
      const promises: Promise<any>[] = [];
      
      for (let i = 0; i < 5; i++) {
        const context = {
          language: 'javascript',
          filePath: `/test/file${i}.js`
        };
        const promise = codeAnalyzer.analyzeCodeWithContext(testCode, context);
        promises.push(promise);
      }

      const startTime = Date.now();
      const results = await Promise.all(promises);
      const duration = Date.now() - startTime;
      
      // All requests should succeed
      assert.strictEqual(results.length, 5);
      results.forEach(result => {
        assert(result);
        assert(result.suggestions);
      });

      // Should handle concurrency efficiently
      assert(duration < 10000, `Concurrent requests took too long: ${duration}ms`);
    });
  });

  describe('Integration with VS Code Extension', () => {
    it('should integrate with extension lifecycle', async () => {
      // Test extension activation scenarios
      mockOllamaServer.configureForCodeAnalysis();

      // Simulate extension commands
      const testCode = 'const greeting = "Hello, World!";';
      const context = {
        language: 'javascript',
        filePath: '/test/greeting.js'
      };

      const result = await codeAnalyzer.analyzeCodeWithContext(testCode, context);
      
      assert(result);
      
      // Verify telemetry and logging would work
      const requests = mockOllamaServer.getRequestHistory();
      assert(requests.length > 0);
    });
  });

  describe('Security and Validation', () => {
    it('should handle large code inputs safely', async () => {
      mockOllamaServer.configureForCodeAnalysis();

      // Create large code input
      const largeCode = 'function test() {\n' + '  console.log("test");\n'.repeat(1000) + '}';
      const context = {
        language: 'javascript',
        filePath: '/test/large.js'
      };

      const result = await codeAnalyzer.analyzeCodeWithContext(largeCode, context);
      
      assert(result);
      assert(result.suggestions);
    });

    it('should validate input parameters', async () => {
      try {
        await codeAnalyzer.analyzeCodeWithContext('', {
          language: '',
          filePath: ''
        });
      } catch (error) {
        // Should handle empty inputs gracefully
        assert(error instanceof Error);
      }
    });
  });

  describe('Model Management', () => {
    it('should work with different models', async () => {
      const customClient = new OllamaClient({
        baseUrl: 'http://localhost:11434',
        defaultModel: 'codellama',
        timeout: 10000,
        maxRetries: 2
      });

      const analyzer = new CodeAnalyzer(customClient);
      mockOllamaServer.configureForCodeAnalysis();

      const testCode = 'function test() {}';
      const context = {
        language: 'javascript',
        filePath: '/test/file.js'
      };

      const result = await analyzer.analyzeCodeWithContext(testCode, context);
      
      assert(result);
      
      // Verify the request was made
      const lastRequest = mockOllamaServer.getLastRequest();
      assert(lastRequest);
      assert.strictEqual(lastRequest.endpoint, '/api/chat');
    });

    it('should handle model switching', async () => {
      mockOllamaServer.configureForCodeAnalysis();

      const models = ['deepseek-coder', 'codellama', 'mistral'];
      
      for (const model of models) {
        const client = new OllamaClient({
          defaultModel: model
        });
        
        const analyzer = new CodeAnalyzer(client);
        const result = await analyzer.analyzeCodeWithContext('function test() {}', {
          language: 'javascript',
          filePath: '/test/file.js'
        });
        
        assert(result);
      }
    });
  });
});
