import { ChildProcess, spawn } from 'child_process';
import fetch from 'node-fetch';
import * as os from 'os';
import AbortController from "AbortController";
import Chat from "../../../apps/desktop/src/pages/Chat";
import Check from "Check";
import Content from "Content";
import DELETE from "DELETE";
import Error from "Error";
import F from "F";
import Failed from "Failed";
import For from "For";
import GET from "GET";
import Generate from "Generate";
import Get from "Get";
import HTTP from "HTTP";
import Health from "Health";
import IM from "IM";
import Ignore from "Ignore";
import List from "List";
import Ollama from "Ollama";
import OllamaChatMessage from "OllamaChatMessage";
import OllamaChatRequest from "OllamaChatRequest";
import OllamaChatResponse from "OllamaChatResponse";
import OllamaGenerateRequest from "OllamaGenerateRequest";
import OllamaGenerateResponse from "OllamaGenerateResponse";
import OllamaManager from "OllamaManager";
import OllamaModel from "OllamaModel";
import POST from "POST";
import Pull from "Pull";
import Quick from "Quick";
import Record from "Record";
import Remove from "Remove";
import Start from "Start";
import Stop from "Stop";
import TextDecoder from "TextDecoder";
import Try from "Try";
import Type from "Type";
import Wait from "Wait";
import Windows from "Windows";

export interface OllamaModel {
  name: string;
  modified_at: string;
  size: number;
  digest: string;
}

export interface OllamaGenerateRequest {
  model: string;
  prompt: string;
  stream?: boolean;
  system?: string;
  template?: string;
  context?: number[];
  options?: Record<string, any>;
}

export interface OllamaGenerateResponse {
  model: string;
  created_at: string;
  response: string;
  done: boolean;
  context?: number[];
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  prompt_eval_duration?: number;
  eval_count?: number;
  eval_duration?: number;
}

export interface OllamaChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface OllamaChatRequest {
  model: string;
  messages: OllamaChatMessage[];
  stream?: boolean;
  options?: Record<string, any>;
}

export interface OllamaChatResponse {
  model: string;
  created_at: string;
  message: OllamaChatMessage;
  done: boolean;
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  prompt_eval_duration?: number;
  eval_count?: number;
  eval_duration?: number;
}

export class OllamaManager {
  public readonly baseUrl: string;
  private readonly timeout: number;
  private serviceProcess?: ChildProcess;

  constructor(baseUrl = 'http://127.0.0.1:11434', timeout = 30000) {
    this.baseUrl = baseUrl.replace(/\/$/, ''); // Remove trailing slash
    this.timeout = timeout;
  }

  /**
   * Check if Ollama service is running and accessible
   */
  async isRunning(): Promise<boolean> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);
      
      const response = await fetch(`${this.baseUrl}/api/version`, {
        method: 'GET',
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get Ollama version information
   */
  async getVersion(): Promise<string | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/version`);
      if (!response.ok) return null;
      
      const data = await response.json() as { version: string };
      return data.version;
    } catch (error) {
      return null;
    }
  }

  /**
   * List all available models
   */
  async listModels(): Promise<OllamaModel[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json() as { models: OllamaModel[] };
      return data.models || [];
    } catch (error) {
      console.error('Failed to list models:', error);
      return [];
    }
  }

  /**
   * Pull/download a model
   */
  async pullModel(modelName: string, onProgress?: (progress: string) => void): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/pull`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: modelName, stream: !!onProgress }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      if (onProgress && response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(line => line.trim());
          
          for (const line of lines) {
            try {
              const data = JSON.parse(line);
              if (data.status) {
                onProgress(data.status);
              }
            } catch (e) {
              // Ignore parsing errors for individual lines
            }
          }
        }
      }
      
      return true;
    } catch (error) {
      console.error('Failed to pull model:', error);
      return false;
    }
  }

  /**
   * Remove a model
   */
  async removeModel(modelName: string): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/api/delete`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: modelName }),
      });
      
      return response.ok;
    } catch (error) {
      console.error('Failed to remove model:', error);
      return false;
    }
  }

  /**
   * Generate text completion
   */
  async generate(request: OllamaGenerateRequest): Promise<OllamaGenerateResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...request, stream: false }),
        timeout: this.timeout,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      return await response.json() as OllamaGenerateResponse;
    } catch (error) {
      console.error('Failed to generate:', error);
      return null;
    }
  }

  /**
   * Chat with conversation context
   */
  async chat(request: OllamaChatRequest): Promise<OllamaChatResponse | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...request, stream: false }),
        timeout: this.timeout,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      return await response.json() as OllamaChatResponse;
    } catch (error) {
      console.error('Failed to chat:', error);
      return null;
    }
  }

  /**
   * Generate embeddings for text
   */
  async embed(model: string, prompt: string): Promise<number[] | null> {
    try {
      const response = await fetch(`${this.baseUrl}/api/embeddings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, prompt }),
        timeout: this.timeout,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json() as { embedding: number[] };
      return data.embedding;
    } catch (error) {
      console.error('Failed to generate embeddings:', error);
      return null;
    }
  }

  /**
   * Start Ollama service (Windows)
   */
  async startService(): Promise<boolean> {
    if (await this.isRunning()) {
      console.log('Ollama service is already running');
      return true;
    }

    try {
      if (os.platform() === 'win32') {
        this.serviceProcess = spawn('ollama', ['serve'], {
          detached: true,
          stdio: 'ignore'
        });
        
        this.serviceProcess.unref();
        
        // Wait a bit and check if it started
        await new Promise(resolve => setTimeout(resolve, 3000));
        return await this.isRunning();
      } else {
        // For non-Windows platforms, assume systemd or similar
        const process = spawn('systemctl', ['start', 'ollama'], {
          stdio: 'ignore'
        });
        
        return new Promise((resolve) => {
          process.on('close', async (code) => {
            resolve(code === 0 && await this.isRunning());
          });
        });
      }
    } catch (error) {
      console.error('Failed to start Ollama service:', error);
      return false;
    }
  }

  /**
   * Stop Ollama service
   */
  async stopService(): Promise<boolean> {
    try {
      if (this.serviceProcess) {
        this.serviceProcess.kill();
        this.serviceProcess = undefined;
      }
      
      if (os.platform() === 'win32') {
        // Try to kill process by name on Windows
        spawn('taskkill', ['/F', '/IM', 'ollama.exe'], { stdio: 'ignore' });
      } else {
        spawn('systemctl', ['stop', 'ollama'], { stdio: 'ignore' });
      }
      
      // Wait a bit and verify it stopped
      await new Promise(resolve => setTimeout(resolve, 2000));
      return !(await this.isRunning());
    } catch (error) {
      console.error('Failed to stop Ollama service:', error);
      return false;
    }
  }

  /**
   * Health check with detailed information
   */
  async healthCheck(): Promise<{
    running: boolean;
    version?: string;
    modelCount?: number;
    models?: string[];
    latency?: number;
  }> {
    const startTime = Date.now();
    const running = await this.isRunning();
    const latency = Date.now() - startTime;

    if (!running) {
      return { running: false, latency };
    }

    try {
      const [version, models] = await Promise.all([
        this.getVersion(),
        this.listModels()
      ]);

      return {
        running: true,
        version: version || undefined,
        modelCount: models.length,
        models: models.map(m => m.name),
        latency
      };
    } catch (error) {
      return { running: true, latency };
    }
  }

  /**
   * Quick text generation helper
   */
  async ask(prompt: string, model = 'phi3:mini', system?: string): Promise<string | null> {
    const response = await this.generate({
      model,
      prompt,
      system,
      stream: false
    });
    
    return response?.response || null;
  }

  /**
   * Chat helper with conversation
   */
  async chatWithHistory(
    messages: OllamaChatMessage[], 
    model = 'phi3:mini'
  ): Promise<string | null> {
    const response = await this.chat({
      model,
      messages,
      stream: false
    });
    
    return response?.message.content || null;
  }
}
