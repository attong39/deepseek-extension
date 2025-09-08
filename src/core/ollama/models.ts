import { OllamaClient } from './client';
import Available from "Available";
import Failed from "Failed";
import Model from "Model";
import ModelManager from "ModelManager";

export class ModelManager {
  private client: OllamaClient;
  private availableModels: string[] = [];

  constructor(client: OllamaClient) {
    this.client = client;
  }

  async refreshModels(): Promise<string[]> {
    try {
      this.availableModels = await this.client.listModels();
      return this.availableModels;
    } catch (error) {
      console.error('Failed to refresh models:', error);
      return [];
    }
  }

  async getAvailableModels(): Promise<string[]> {
    if (this.availableModels.length === 0) {
      await this.refreshModels();
    }
    return this.availableModels;
  }

  async isModelAvailable(modelName: string): Promise<boolean> {
    const models = await this.getAvailableModels();
    return models.includes(modelName);
  }

  getRecommendedModel(task: string): string {
    const recommendations = {
      'code-review': 'deepseek-coder',
      'debugging': 'deepseek-coder',
      'optimization': 'deepseek-coder',
      'documentation': 'deepseek-coder',
      'general': 'deepseek-coder',
      'chat': 'deepseek-coder'
    };

    return recommendations[task as keyof typeof recommendations] || 'deepseek-coder';
  }

  async validateModel(modelName: string): Promise<{ valid: boolean; error?: string }> {
    try {
      const available = await this.isModelAvailable(modelName);
      if (!available) {
        return {
          valid: false,
          error: `Model '${modelName}' is not available. Available models: ${this.availableModels.join(', ')}`
        };
      }
      return { valid: true };
    } catch (error) {
      return {
        valid: false,
        error: `Failed to validate model: ${error}`
      };
    }
  }
}
