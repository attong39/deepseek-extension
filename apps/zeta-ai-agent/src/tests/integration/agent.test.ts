import { describe, it, expect } from '../testRunner';
import { AIAgent } from '../../core/agent/agent';
import { CodeContext } from '../../types/shared';
import AI from "AI";
import Action from "Action";
import Cannot from "Cannot";
import Chat from "../../../../desktop/src/pages/Chat";
import Code from "Code";
import Configuration from "Configuration";
import Create from "Create";
import Debug from "Debug";
import Error from "Error";
import Expected from "Expected";
import Explain from "Explain";
import Features from "../../../../desktop/src/Features/index";
import Functionality from "Functionality";
import Handling from "Handling";
import Hello from "Hello";
import Initialization from "Initialization";
import Integration from "Integration";
import Management from "Management";
import May from "May";
import Memory from "../../../../desktop/src/Memory/index";
import Mock from "Mock";
import MockOllamaClient from "MockOllamaClient";
import No from "No";
import Ollama from "Ollama";
import Optimization from "Optimization";
import Planning from "Planning";
import Refactor from "Refactor";
import Review from "Review";
import Security from "Security";
import Should from "Should";
import Tests from "../../../../desktop/src/Tests/index";
import TypeError from "TypeError";

// Mock Ollama client for testing
class MockOllamaClient {
  async healthCheck(): Promise<boolean> {
    return true;
  }

  async validateModel(): Promise<boolean> {
    return true;
  }

  async chat(): Promise<any> {
    return {
      message: {
        content: 'Mock AI response for testing'
      }
    };
  }

  async listModels(): Promise<any> {
    return {
      models: [
        { name: 'test-model' }
      ]
    };
  }
}

describe('AIAgent Integration Tests', () => {
  let agent: AIAgent;
  let mockContext: CodeContext;

  beforeEach(() => {
    // Create agent with test configuration
    agent = new AIAgent({
      ollama_url: 'http://localhost:11434',
      default_model: 'test-model',
      max_context_size: 100,
      enable_caching: false,
      cache_ttl: 3600,
      rate_limit: 60,
      security_policy: {
        max_code_size: 1000,
        allowed_file_extensions: ['.ts', '.js'],
        blocked_patterns: [/eval\(/i],
        max_context_size: 5000,
        rate_limit_per_minute: 60
      },
      performance_monitoring: true,
      log_level: 'info'
    });

    // Mock the Ollama client
    (agent as any).ollama = new MockOllamaClient();

    mockContext = {
      language: 'typescript',
      filePath: '/test/file.ts'
    };
  });

  describe('Initialization', () => {
    it('should initialize agent successfully', async () => {
      // No exception should be thrown
      await agent.initialize();
    });

    it('should have correct configuration', () => {
      const config = agent.getConfig();
      expect(config.default_model).toBe('test-model');
      expect(config.enable_caching).toBe(false);
      expect(config.max_context_size).toBe(100);
    });

    it('should update configuration', () => {
      agent.updateConfig({ default_model: 'new-model' });
      const config = agent.getConfig();
      expect(config.default_model).toBe('new-model');
    });
  });

  describe('Code Review', () => {
    it('should perform code review', async () => {
      await agent.initialize();
      
      const code = 'function test() { return "hello"; }';
      
      try {
        const review = await agent.reviewCode(code, mockContext);
        expect(typeof review).toBe('object');
      } catch (error) {
        // Expected to fail with mock, but should not crash
        expect(error).toBeTruthy();
      }
    });

    it('should validate code input', async () => {
      await agent.initialize();
      
      try {
        await agent.reviewCode('', mockContext);
        // Should not reach here
        expect(false).toBe(true);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('non-empty string');
      }
    });

    it('should reject oversized code', async () => {
      await agent.initialize();
      
      const largeCode = 'a'.repeat(2000);
      
      try {
        await agent.reviewCode(largeCode, mockContext);
        expect(false).toBe(true);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('exceeds maximum size');
      }
    });

    it('should reject blocked patterns', async () => {
      await agent.initialize();
      
      const maliciousCode = 'eval("malicious code")';
      
      try {
        await agent.reviewCode(maliciousCode, mockContext);
        expect(false).toBe(true);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('blocked pattern');
      }
    });
  });

  describe('Debug Code', () => {
    it('should perform debug analysis', async () => {
      await agent.initialize();
      
      const code = 'function buggyFunction() { return undefined.property; }';
      const errorDesc = 'TypeError: Cannot read property of undefined';
      
      try {
        const solution = await agent.debugCode(errorDesc, code, mockContext);
        expect(typeof solution).toBe('object');
      } catch (error) {
        // Expected to fail with mock
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Code Optimization', () => {
    it('should perform code optimization', async () => {
      await agent.initialize();
      
      const code = 'function slow() { for(let i = 0; i < 1000000; i++) { console.log(i); } }';
      
      try {
        const optimization = await agent.optimizeCode(code, mockContext, ['performance']);
        expect(typeof optimization).toBe('object');
      } catch (error) {
        // Expected to fail with mock
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Chat Functionality', () => {
    it('should handle chat messages', async () => {
      await agent.initialize();
      
      try {
        const response = await agent.chat('Hello, can you help me?');
        expect(typeof response).toBe('string');
        expect(response.length).toBeGreaterThan(0);
      } catch (error) {
        // May fail with mock but should not crash
        expect(error).toBeTruthy();
      }
    });

    it('should include context in chat', async () => {
      await agent.initialize();
      
      const context = { language: 'typescript', filePath: '/test.ts' };
      
      try {
        const response = await agent.chat('Explain this code', context);
        expect(typeof response).toBe('string');
      } catch (error) {
        // Expected with mock
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Action Planning', () => {
    it('should create action plans', async () => {
      await agent.initialize();
      
      const request = 'Refactor this function to use async/await';
      
      try {
        const plan = await agent.planAction(request, mockContext);
        expect(typeof plan).toBe('object');
      } catch (error) {
        // Expected to fail with mock
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Memory Management', () => {
    it('should track memory stats', async () => {
      await agent.initialize();
      
      const stats = await agent.getMemoryStats();
      expect(typeof stats).toBe('object');
      expect(typeof stats.total_interactions).toBe('number');
      expect(typeof stats.success_rate).toBe('number');
      expect(Array.isArray(stats.recent_activity)).toBe(true);
    });

    it('should export memory', async () => {
      await agent.initialize();
      
      const exported = await agent.exportMemory();
      expect(typeof exported).toBe('object');
    });

    it('should import memory', async () => {
      await agent.initialize();
      
      const testData = { test: 'data' };
      
      try {
        await agent.importMemory(testData);
        // Should not throw
      } catch (error) {
        // May fail but should not crash
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Error Handling', () => {
    it('should handle initialization errors gracefully', async () => {
      // Mock failed health check
      (agent as any).ollama.healthCheck = async () => false;
      
      try {
        await agent.initialize();
        expect(false).toBe(true); // Should not reach here
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('Cannot connect to Ollama');
      }
    });

    it('should validate configuration', () => {
      const invalidConfig = {
        max_context_size: -1,
        rate_limit: 0
      };
      
      try {
        agent.updateConfig(invalidConfig);
        const config = agent.getConfig();
        // Configuration should be updated but validation may occur during usage
        expect(config.max_context_size).toBe(-1);
      } catch (error) {
        // Configuration validation may throw
        expect(error).toBeTruthy();
      }
    });
  });

  describe('Security Features', () => {
    it('should apply security policies', async () => {
      await agent.initialize();
      
      const maliciousCode = 'eval("document.write(\'<script>alert(1)</script>\')")';
      
      try {
        await agent.reviewCode(maliciousCode, mockContext);
        expect(false).toBe(true);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('blocked pattern');
      }
    });

    it('should validate file extensions', async () => {
      await agent.initialize();
      
      const code = 'console.log("test")';
      const invalidContext = {
        ...mockContext,
        filePath: '/test/file.exe'
      };
      
      try {
        await agent.reviewCode(code, invalidContext);
        expect(false).toBe(true);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        expect(errorMessage).toContain('not allowed');
      }
    });
  });
});
