import { OllamaClient } from './client';
import { ModelInfo, ModelListResponse } from './types';
import DefaultModelManager from "DefaultModelManager";
import Error from "Error";
import Failed from "Failed";
import Fallback from "Fallback";
import ModelManager from "ModelManager";
import Record from "Record";

export interface ModelManager {
  listAvailable(): Promise<ModelInfo[]>;
  isInstalled(modelName: string): Promise<boolean>;
  install(modelName: string): Promise<void>;
  remove(modelName: string): Promise<void>;
  getRecommended(): string[];
}

export class DefaultModelManager implements ModelManager {
  private client: OllamaClient;
  private recommendedModels = [
    'deepseek-coder',
    'codellama',
    'starcoder',
    'phi',
    'mistral'
  ];

  constructor(client: OllamaClient) {
    this.client = client;
  }

  async listAvailable(): Promise<ModelInfo[]> {
    try {
      const response: ModelListResponse = await this.client.listModels();
      return response.models;
    } catch (error) {
      console.error('Failed to list available models:', error);
      return [];
    }
  }

  async isInstalled(modelName: string): Promise<boolean> {
    return this.client.validateModel(modelName);
  }

  async install(modelName: string): Promise<void> {
    try {
      await this.client.pullModel(modelName);
    } catch (error) {
      throw new Error(`Failed to install model ${modelName}: ${error}`);
    }
  }

  async remove(modelName: string): Promise<void> {
    try {
      await this.client.deleteModel(modelName);
    } catch (error) {
      throw new Error(`Failed to remove model ${modelName}: ${error}`);
    }
  }

  getRecommended(): string[] {
    return [...this.recommendedModels];
  }

  async findBestModel(task: 'code' | 'chat' | 'general'): Promise<string> {
    const available = await this.listAvailable();
    const availableNames = available.map(model => model.name);

    const preferences: Record<string, string[]> = {
      code: ['deepseek-coder', 'codellama', 'starcoder'],
      chat: ['mistral', 'phi', 'deepseek-coder'],
      general: ['mistral', 'phi', 'deepseek-coder']
    };

    const taskPreferences = preferences[task] || preferences.general;

    for (const preferred of taskPreferences) {
      if (availableNames.includes(preferred)) {
        return preferred;
      }
    }

    // Fallback to first available model
    return availableNames[0] || 'deepseek-coder';
  }

  async getModelInfo(modelName: string): Promise<ModelInfo | null> {
    const models = await this.listAvailable();
    return models.find(model => model.name === modelName) || null;
  }

  async ensureModelAvailable(modelName: string): Promise<boolean> {
    const isInstalled = await this.isInstalled(modelName);
    
    if (!isInstalled) {
      try {
        await this.install(modelName);
        return true;
      } catch (error) {
        console.error(`Failed to ensure model ${modelName} is available:`, error);
        return false;
      }
    }
    
    return true;
  }
}
