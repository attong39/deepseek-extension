import { OllamaChatMessage, OllamaManager } from './ollama-manager';
import Anthropic from "Anthropic";
import Chat from "../../../apps/desktop/src/pages/Chat";
import Embedding from "Embedding";
import Failed from "Failed";
import Fallback from "Fallback";
import For from "For";
import Generate from "Generate";
import Get from "Get";
import Health from "Health";
import LLM from "LLM";
import List from "List";
import No from "No";
import Ollama from "Ollama";
import OllamaResponse from "OllamaResponse";
import OllamaService from "OllamaService";
import OllamaServiceConfig from "OllamaServiceConfig";
import OpenAI from "OpenAI";
import Partial from "Partial";
import Pull from "Pull";
import Remove from "Remove";
import Required from "Required";
import Start from "Start";
import Stop from "Stop";
import T from "T";
import This from "This";
import Unexpected from "Unexpected";
import Update from "Update";
import Wait from "Wait";

export interface OllamaServiceConfig {
  baseUrl?: string;
  timeout?: number;
  defaultModel?: string;
  fallbackToRemote?: boolean;
  maxRetries?: number;
}

export interface OllamaResponse<T = string> {
  success: boolean;
  data?: T;
  error?: string;
  source: 'ollama' | 'fallback';
  latency?: number;
}

export class OllamaService {
  private manager: OllamaManager;
  private config: Required<OllamaServiceConfig>;

  constructor(config: OllamaServiceConfig = {}) {
    this.config = {
      baseUrl: config.baseUrl || 'http://127.0.0.1:11434',
      timeout: config.timeout || 30000,
      defaultModel: config.defaultModel || 'phi3:mini',
      fallbackToRemote: config.fallbackToRemote || false,
      maxRetries: config.maxRetries || 3
    };

    this.manager = new OllamaManager(this.config.baseUrl, this.config.timeout);
  }

  /**
   * Generate text with automatic retry and fallback
   */
  async generate(
    prompt: string, 
    model?: string, 
    system?: string
  ): Promise<OllamaResponse<string>> {
    const startTime = Date.now();
    const targetModel = model || this.config.defaultModel;

    for (let attempt = 1; attempt <= this.config.maxRetries; attempt++) {
      try {
        const response = await this.manager.ask(prompt, targetModel, system);
        
        if (response) {
          return {
            success: true,
            data: response,
            source: 'ollama',
            latency: Date.now() - startTime
          };
        }
      } catch (error) {
        console.warn(`Ollama attempt ${attempt} failed:`, error);
        
        if (attempt === this.config.maxRetries) {
          if (this.config.fallbackToRemote) {
            return await this.fallbackToRemote(prompt, system);
          }
          
          return {
            success: false,
            error: `Failed after ${this.config.maxRetries} attempts: ${error}`,
            source: 'ollama',
            latency: Date.now() - startTime
          };
        }
        
        // Wait before retry (exponential backoff)
        await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
      }
    }

    return {
      success: false,
      error: 'Unexpected error in retry loop',
      source: 'ollama'
    };
  }

  /**
   * Chat with conversation context
   */
  async chat(
    messages: OllamaChatMessage[], 
    model?: string
  ): Promise<OllamaResponse<string>> {
    const startTime = Date.now();
    const targetModel = model || this.config.defaultModel;

    try {
      const response = await this.manager.chatWithHistory(messages, targetModel);
      
      if (response) {
        return {
          success: true,
          data: response,
          source: 'ollama',
          latency: Date.now() - startTime
        };
      }
      
      if (this.config.fallbackToRemote) {
        return await this.fallbackChatToRemote(messages);
      }
      
      return {
        success: false,
        error: 'No response from Ollama',
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      if (this.config.fallbackToRemote) {
        return await this.fallbackChatToRemote(messages);
      }
      
      return {
        success: false,
        error: `Chat failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Generate embeddings
   */
  async embed(text: string, model = 'nomic-embed-text'): Promise<OllamaResponse<number[]>> {
    const startTime = Date.now();

    try {
      const embeddings = await this.manager.embed(model, text);
      
      if (embeddings) {
        return {
          success: true,
          data: embeddings,
          source: 'ollama',
          latency: Date.now() - startTime
        };
      }
      
      return {
        success: false,
        error: 'No embeddings generated',
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Embedding failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<OllamaResponse<{
    version?: string;
    modelCount?: number;
    models?: string[];
  }>> {
    const startTime = Date.now();

    try {
      const health = await this.manager.healthCheck();
      
      return {
        success: health.running,
        data: health.running ? {
          version: health.version,
          modelCount: health.modelCount,
          models: health.models
        } : undefined,
        error: health.running ? undefined : 'Ollama service not running',
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Health check failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * List available models
   */
  async listModels(): Promise<OllamaResponse<string[]>> {
    const startTime = Date.now();

    try {
      const models = await this.manager.listModels();
      
      return {
        success: true,
        data: models.map(m => m.name),
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to list models: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Pull/download a model
   */
  async pullModel(
    modelName: string, 
    onProgress?: (progress: string) => void
  ): Promise<OllamaResponse<boolean>> {
    const startTime = Date.now();

    try {
      const success = await this.manager.pullModel(modelName, onProgress);
      
      return {
        success,
        data: success,
        error: success ? undefined : `Failed to pull model ${modelName}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Pull model failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Remove a model
   */
  async removeModel(modelName: string): Promise<OllamaResponse<boolean>> {
    const startTime = Date.now();

    try {
      const success = await this.manager.removeModel(modelName);
      
      return {
        success,
        data: success,
        error: success ? undefined : `Failed to remove model ${modelName}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Remove model failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Start Ollama service
   */
  async startService(): Promise<OllamaResponse<boolean>> {
    const startTime = Date.now();

    try {
      const success = await this.manager.startService();
      
      return {
        success,
        data: success,
        error: success ? undefined : 'Failed to start Ollama service',
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Start service failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Stop Ollama service
   */
  async stopService(): Promise<OllamaResponse<boolean>> {
    const startTime = Date.now();

    try {
      const success = await this.manager.stopService();
      
      return {
        success,
        data: success,
        error: success ? undefined : 'Failed to stop Ollama service',
        source: 'ollama',
        latency: Date.now() - startTime
      };
    } catch (error) {
      return {
        success: false,
        error: `Stop service failed: ${error}`,
        source: 'ollama',
        latency: Date.now() - startTime
      };
    }
  }

  /**
   * Fallback to remote LLM (placeholder - implement with your remote provider)
   */
  private async fallbackToRemote(
    prompt: string, 
    system?: string
  ): Promise<OllamaResponse<string>> {
    // This would integrate with OpenAI, Anthropic, or other remote providers
    // For now, return a fallback response
    console.warn('Fallback to remote LLM not implemented');
    
    return {
      success: false,
      error: 'Ollama unavailable and remote fallback not configured',
      source: 'fallback'
    };
  }

  /**
   * Fallback chat to remote LLM (placeholder)
   */
  private async fallbackChatToRemote(
    messages: OllamaChatMessage[]
  ): Promise<OllamaResponse<string>> {
    console.warn('Fallback chat to remote LLM not implemented');
    
    return {
      success: false,
      error: 'Ollama unavailable and remote chat fallback not configured',
      source: 'fallback'
    };
  }

  /**
   * Get service configuration
   */
  getConfig(): Required<OllamaServiceConfig> {
    return { ...this.config };
  }

  /**
   * Update service configuration
   */
  updateConfig(newConfig: Partial<OllamaServiceConfig>): void {
    this.config = { ...this.config, ...newConfig };
    
    if (newConfig.baseUrl || newConfig.timeout) {
      this.manager = new OllamaManager(
        this.config.baseUrl, 
        this.config.timeout
      );
    }
  }
}
