import {
import API from "../../../../desktop/src/API/index";
import AbortSignal from "AbortSignal";
import AsyncGenerator from "AsyncGenerator";
import Configuration from "Configuration";
import Content from "Content";
import Continue from "Continue";
import DELETE from "DELETE";
import End from "End";
import Error from "Error";
import Exponential from "Exponential";
import Failed from "Failed";
import GET from "GET";
import HTTP from "HTTP";
import Health from "Health";
import Math from "Math";
import No from "No";
import Ollama from "Ollama";
import OllamaClient from "OllamaClient";
import POST from "POST";
import Partial from "Partial";
import ReadableStreamDefaultReader from "ReadableStreamDefaultReader";
import Request from "Request";
import TextDecoder from "TextDecoder";
import Type from "Type";
import Uint8Array from "Uint8Array";
  ChatMessage,
  ChatOptions,
  ChatResponse,
  EmbeddingsRequest,
  EmbeddingsResponse,
  GenerateRequest,
  GenerateResponse,
  ModelListResponse,
  OllamaConfig,
  OllamaError,
  PullRequest
} from './types';

export class OllamaClient {
  private readonly config: OllamaConfig;

  constructor(config: Partial<OllamaConfig> = {}) {
    this.config = {
      baseUrl: config.baseUrl || 'http://localhost:11434',
      timeout: config.timeout || 30000,
      defaultModel: config.defaultModel || 'deepseek-coder',
      maxRetries: config.maxRetries || 3,
      retryDelay: config.retryDelay || 1000
    };
  }

  async chat(messages: ChatMessage[], options?: ChatOptions): Promise<ChatResponse> {
    const url = `${this.config.baseUrl}/api/chat`;
    const body = {
      model: options?.model || this.config.defaultModel,
      messages,
      stream: false,
      options: {
        temperature: options?.temperature || 0.7,
        num_predict: options?.maxTokens || 2048,
        top_p: options?.topP || 0.9,
        top_k: options?.topK || 40,
        stop: options?.stop || []
      }
    };

    return this.requestWithRetry(url, body);
  }

  private async requestWithRetry(
    endpoint: string,
    data: any,
    retries?: number
  ): Promise<any> {
    const maxRetries = retries || this.config.maxRetries;
    let lastError: Error | null = null;

    for (let i = 0; i < maxRetries; i++) {
      try {
        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
          signal: AbortSignal.timeout(this.config.timeout)
        });

        if (!response.ok) {
          throw new OllamaError(
            `HTTP ${response.status}: ${response.statusText}`,
            response.status,
            endpoint
          );
        }

        return await response.json();
      } catch (error) {
        lastError = error instanceof Error ? error : new Error(String(error));
        
        if (i === maxRetries - 1) {
          throw new OllamaError(
            `Request failed after ${maxRetries} retries: ${lastError.message}`,
            0,
            endpoint,
            lastError
          );
        }

        const delay = this.config.retryDelay * Math.pow(2, i); // Exponential backoff
        await this.delay(delay);
      }
    }

    throw new OllamaError('Request failed after all retries', 0, endpoint, lastError || undefined);
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async *streamChat(messages: ChatMessage[], options?: ChatOptions): AsyncGenerator<string> {
    const url = `${this.config.baseUrl}/api/chat`;
    const body = this.buildStreamChatBody(messages, options);

    const reader = await this.initializeStream(url, body);
    const decoder = new TextDecoder();

    try {
      yield* this.processStreamResponse(reader, decoder, 'chat');
    } finally {
      reader.releaseLock();
    }
  }

  private buildStreamChatBody(messages: ChatMessage[], options?: ChatOptions) {
    return {
      model: options?.model || this.config.defaultModel,
      messages,
      stream: true,
      options: {
        temperature: options?.temperature || 0.7,
        num_predict: options?.maxTokens || 2048,
        top_p: options?.topP || 0.9,
        top_k: options?.topK || 40
      }
    };
  }

  private async initializeStream(url: string, body: any): Promise<ReadableStreamDefaultReader<Uint8Array>> {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    if (!response.body) {
      throw new Error('No response body available for streaming');
    }

    return response.body.getReader();
  }

  private async *processStreamResponse(
    reader: ReadableStreamDefaultReader<Uint8Array>, 
    decoder: TextDecoder, 
    type: 'chat' | 'generate'
  ): AsyncGenerator<string> {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n').filter((line: string) => line.trim());

      for (const line of lines) {
        const content = this.parseStreamLine(line, type);
        if (content) {
          yield content;
        }
      }
    }
  }

  private parseStreamLine(line: string, type: 'chat' | 'generate'): string | null {
    try {
      const data = JSON.parse(line);
      
      if (type === 'chat' && data.message?.content) {
        return data.message.content;
      }
      
      if (type === 'generate' && data.response) {
        return data.response;
      }
      
      if (data.done) {
        return null; // End of stream
      }
      
      return null;
    } catch (error) {
      console.warn('Failed to parse streaming response line:', line, error);
      return null; // Continue processing other lines
    }
  }

  async generate(request: GenerateRequest): Promise<GenerateResponse> {
    const url = `${this.config.baseUrl}/api/generate`;
    return this.makeRequest(url, 'POST', request);
  }

  async *streamGenerate(request: GenerateRequest): AsyncGenerator<string> {
    const url = `${this.config.baseUrl}/api/generate`;
    const streamRequest = { ...request, stream: true };

    const reader = await this.initializeStream(url, streamRequest);
    const decoder = new TextDecoder();

    try {
      yield* this.processStreamResponse(reader, decoder, 'generate');
    } finally {
      reader.releaseLock();
    }
  }

  async listModels(): Promise<ModelListResponse> {
    const url = `${this.config.baseUrl}/api/tags`;
    return this.makeRequest(url, 'GET');
  }

  async pullModel(name: string, insecure = false): Promise<void> {
    const url = `${this.config.baseUrl}/api/pull`;
    const body: PullRequest = { name, insecure, stream: false };
    return this.makeRequest(url, 'POST', body);
  }

  async deleteModel(name: string): Promise<void> {
    const url = `${this.config.baseUrl}/api/delete`;
    const body = { name };
    return this.makeRequest(url, 'DELETE', body);
  }

  async copyModel(source: string, destination: string): Promise<void> {
    const url = `${this.config.baseUrl}/api/copy`;
    const body = { source, destination };
    return this.makeRequest(url, 'POST', body);
  }

  async embeddings(request: EmbeddingsRequest): Promise<EmbeddingsResponse> {
    const url = `${this.config.baseUrl}/api/embeddings`;
    return this.makeRequest(url, 'POST', request);
  }

  async validateModel(model: string): Promise<boolean> {
    try {
      const models = await this.listModels();
      return models.models.some(m => m.name === model);
    } catch (error) {
      console.warn(`Failed to validate model ${model}:`, error);
      return false;
    }
  }

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.baseUrl}/api/tags`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000)
      });
      return response.ok;
    } catch (error) {
      console.warn('Health check failed:', error);
      return false;
    }
  }

  private async makeRequest(
    url: string,
    method: string,
    body?: any,
    retryCount = 0
  ): Promise<any> {
    try {
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: AbortSignal.timeout(this.config.timeout)
      });

      if (!response.ok) {
        const errorText = await response.text();
        let parsedError: any;
        
        try {
          parsedError = JSON.parse(errorText);
        } catch {
          parsedError = { error: errorText || `HTTP ${response.status}: ${response.statusText}` };
        }

        throw new OllamaError(
          `Ollama API Error: ${parsedError.error || errorText}`,
          response.status,
          url
        );
      }

      const responseText = await response.text();
      
      if (!responseText.trim()) {
        return {};
      }

      try {
        return JSON.parse(responseText);
      } catch (parseError) {
        throw new Error(`Failed to parse response JSON: ${parseError}`);
      }
    } catch (error) {
      if (retryCount < this.config.maxRetries) {
        console.warn(`Request failed, retrying (${retryCount + 1}/${this.config.maxRetries}):`, error);
        await this.delay(this.config.retryDelay * Math.pow(2, retryCount));
        return this.makeRequest(url, method, body, retryCount + 1);
      }
      throw error;
    }
  }

  // Configuration methods (note: config is readonly, these methods shouldn't modify it)
  getBaseUrl(): string {
    return this.config.baseUrl;
  }

  getDefaultModel(): string {
    return this.config.defaultModel;
  }

  setTimeout(timeout: number): void {
    this.config.timeout = timeout;
  }

  getConfig(): OllamaConfig {
    return { ...this.config };
  }
}
