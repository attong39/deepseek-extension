/**
 * Mock Ollama Server for Testing
 * Provides a complete mock implementation of the Ollama API for testing purposes
 */

import { 
import API from "../../../desktop/src/API/index";
import Add from "Add";
import AsyncGenerator from "AsyncGenerator";
import Cannot from "Cannot";
import Check from "Check";
import Consider from "Consider";
import Create from "Create";
import Debug from "Debug";
import Default from "Default";
import Error from "Error";
import Extract from "Extract";
import GET from "GET";
import Global from "Global";
import Health from "Health";
import Here from "Here";
import JSDoc from "JSDoc";
import Map from "Map";
import Mock from "Mock";
import MockClass from "MockClass";
import MockOllamaServer from "MockOllamaServer";
import MockResponse from "MockResponse";
import No from "No";
import Ollama from "Ollama";
import POST from "POST";
import Pre from "Pre";
import Provides from "Provides";
import Q4_0 from "Q4_0";
import Record from "Record";
import Return from "Return";
import Server from "Server";
import Simulate from "Simulate";
import Test from "../../../desktop/src/Test/index";
import Testing from "Testing";
import The from "The";
import This from "This";
import TypeError from "TypeError";
import Unused from "Unused";
  ChatResponse, 
  GenerateResponse 
} from '../../src/core/ollama/types';

export interface MockResponse {
  endpoint: string;
  method: string;
  response: any;
  delay?: number;
  shouldFail?: boolean;
  statusCode?: number;
}

export class MockOllamaServer {
  private responses = new Map<string, MockResponse>();
  private requestHistory: Array<{
    endpoint: string;
    method: string;
    data: any;
    timestamp: number;
  }> = [];
  private isRunning = false;

  constructor() {
    this.setupDefaultResponses();
  }

  private setupDefaultResponses(): void {
    // Default chat response
    this.setResponse('/api/chat', 'POST', {
      model: 'deepseek-coder',
      created_at: new Date().toISOString(),
      message: {
        role: 'assistant',
        content: 'This is a mock response from the Ollama server for testing purposes.'
      },
      done: true,
      total_duration: 1000000000,
      load_duration: 500000000,
      prompt_eval_count: 10,
      prompt_eval_duration: 200000000,
      eval_count: 20,
      eval_duration: 300000000
    });

    // Default model list response
    this.setResponse('/api/tags', 'GET', {
      models: [
        {
          name: 'deepseek-coder:latest',
          modified_at: '2024-01-01T00:00:00Z',
          size: 3825819519,
          digest: 'sha256:1234567890abcdef',
          details: {
            format: 'gguf',
            family: 'deepseek',
            families: ['deepseek'],
            parameter_size: '6.7B',
            quantization_level: 'Q4_0'
          }
        },
        {
          name: 'codellama:latest',
          modified_at: '2024-01-01T00:00:00Z',
          size: 3825819519,
          digest: 'sha256:abcdef1234567890',
          details: {
            format: 'gguf',
            family: 'llama',
            families: ['llama'],
            parameter_size: '7B',
            quantization_level: 'Q4_0'
          }
        }
      ]
    });

    // Default generate response
    this.setResponse('/api/generate', 'POST', {
      model: 'deepseek-coder',
      created_at: new Date().toISOString(),
      response: 'This is a generated response.',
      done: true
    });

    // Health check response
    this.setResponse('/api/version', 'GET', {
      version: '0.1.17'
    });
  }

  setResponse(
    endpoint: string, 
    method: string, 
    response: any, 
    options: {
      delay?: number;
      shouldFail?: boolean;
      statusCode?: number;
    } = {}
  ): void {
    const key = `${method.toUpperCase()}:${endpoint}`;
    this.responses.set(key, {
      endpoint,
      method: method.toUpperCase(),
      response,
      delay: options.delay || 0,
      shouldFail: options.shouldFail || false,
      statusCode: options.statusCode || 200
    });
  }

  async handleRequest(
    endpoint: string, 
    method: string, 
    data?: any
  ): Promise<any> {
    const key = `${method.toUpperCase()}:${endpoint}`;
    const mockResponse = this.responses.get(key);

    // Record request
    this.requestHistory.push({
      endpoint,
      method: method.toUpperCase(),
      data,
      timestamp: Date.now()
    });

    if (!mockResponse) {
      throw new Error(`No mock response configured for ${method} ${endpoint}`);
    }

    // Simulate network delay
    if (mockResponse.delay) {
      await new Promise(resolve => setTimeout(resolve, mockResponse.delay));
    }

    // Simulate failure
    if (mockResponse.shouldFail) {
      throw new Error(`Mock failure for ${method} ${endpoint}`);
    }

    // Return response based on endpoint
    if (endpoint === '/api/chat') {
      return this.handleChatRequest(data, mockResponse);
    } else if (endpoint === '/api/generate') {
      return this.handleGenerateRequest(data, mockResponse);
    } else {
      return mockResponse.response;
    }
  }

  private handleChatRequest(data: any, mockResponse: MockResponse): ChatResponse {
    const messages = data?.messages || [];
    const lastMessage = messages[messages.length - 1];
    
    // Create contextual response based on input
    let content = mockResponse.response.message.content;
    
    if (lastMessage?.content.includes('code')) {
      content = 'Here is a code analysis: The function looks good but could be optimized for better performance.';
    } else if (lastMessage?.content.includes('debug')) {
      content = 'Debug suggestion: Check for null pointer exceptions on line 42.';
    } else if (lastMessage?.content.includes('test')) {
      content = 'Test recommendation: Add unit tests for edge cases and error handling.';
    }

    return {
      ...mockResponse.response,
      message: {
        role: 'assistant',
        content
      }
    };
  }

  private handleGenerateRequest(data: any, mockResponse: MockResponse): GenerateResponse {
    const prompt = data?.prompt || '';
    let response = mockResponse.response.response;

    if (prompt.includes('function')) {
      response = 'function mockFunction() { return "test"; }';
    } else if (prompt.includes('class')) {
      response = 'class MockClass { constructor() { this.name = "mock"; } }';
    }

    return {
      ...mockResponse.response,
      response
    };
  }

  // Test utilities
  getRequestHistory(): typeof this.requestHistory {
    return [...this.requestHistory];
  }

  clearRequestHistory(): void {
    this.requestHistory = [];
  }

  getLastRequest(): typeof this.requestHistory[0] | undefined {
    return this.requestHistory[this.requestHistory.length - 1];
  }

  simulateStreamingResponse(
    endpoint: string,
    chunks: string[]
  ): AsyncGenerator<string> {
    return (async function* () {
      for (const chunk of chunks) {
        await new Promise(resolve => setTimeout(resolve, 50));
        yield chunk;
      }
    })();
  }

  reset(): void {
    this.responses.clear();
    this.requestHistory = [];
    this.setupDefaultResponses();
  }

  start(): void {
    this.isRunning = true;
  }

  stop(): void {
    this.isRunning = false;
  }

  isServerRunning(): boolean {
    return this.isRunning;
  }

  // Pre-configured test scenarios
  configureForCodeAnalysis(): void {
    this.setResponse('/api/chat', 'POST', {
      model: 'deepseek-coder',
      created_at: new Date().toISOString(),
      message: {
        role: 'assistant',
        content: JSON.stringify({
          suggestions: [
            'Consider using const instead of let for variables that don\'t change',
            'Add error handling for async operations'
          ],
          issues: [
            {
              severity: 'warning',
              message: 'Unused variable detected',
              line: 15,
              column: 10
            }
          ],
          complexity: {
            cognitive: 12,
            cyclomatic: 8,
            maintainability: 'good'
          },
          improvements: [
            'Extract large function into smaller methods',
            'Add JSDoc documentation'
          ]
        })
      },
      done: true
    });
  }

  configureForDebugging(): void {
    this.setResponse('/api/chat', 'POST', {
      model: 'deepseek-coder',
      created_at: new Date().toISOString(),
      message: {
        role: 'assistant',
        content: JSON.stringify({
          problem: 'TypeError: Cannot read property of undefined',
          cause: 'The variable \'user\' is undefined at line 42',
          solution: 'Add null check before accessing user properties',
          steps: [
            'Check if user exists before accessing properties',
            'Add default values or fallbacks',
            'Consider using optional chaining operator'
          ],
          code_fix: 'if (user && user.name) { console.log(user.name); }'
        })
      },
      done: true
    });
  }

  configureForErrors(): void {
    this.setResponse('/api/chat', 'POST', {}, {
      shouldFail: true,
      statusCode: 500
    });
  }
}

// Global mock instance for tests
export const mockOllamaServer = new MockOllamaServer();
