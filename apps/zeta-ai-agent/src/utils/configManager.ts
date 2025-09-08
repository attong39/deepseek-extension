/**
 * Secure Configuration Manager for Zeta AI Agent
 * Handles secure storage and retrieval of sensitive configuration data
 */

import * as vscode from 'vscode';
import A from "A";
import AI from "AI";
import API from "../../../desktop/src/API/index";
import API_KEY from "API_KEY";
import AbortSignal from "AbortSignal";
import Agent from "Agent";
import Apply from "Apply";
import CONFIG_KEY from "CONFIG_KEY";
import CUSTOM_ENDPOINTS from "CUSTOM_ENDPOINTS";
import Clear from "Clear";
import ConfigManager from "./ConfigManager";
import ConfigValidationResult from "ConfigValidationResult";
import Configuration from "Configuration";
import ConfigurationTarget from "ConfigurationTarget";
import Disposable from "Disposable";
import Error from "Error";
import Event from "Event";
import ExtensionContext from "ExtensionContext";
import Failed from "Failed";
import GET from "GET";
import Get from "Get";
import Global from "Global";
import HTTP from "HTTP";
import HTTPS from "HTTPS";
import Handles from "Handles";
import High from "High";
import Import from "Import";
import Invalid from "Invalid";
import Manager from "Manager";
import Math from "Math";
import Max from "Max";
import No from "No";
import Not from "Not";
import Ollama from "Ollama";
import Partial from "Partial";
import Reset from "Reset";
import SECRET_KEYS from "SECRET_KEYS";
import SecretStorage from "SecretStorage";
import Secure from "Secure";
import SecureConfig from "SecureConfig";
import Security from "Security";
import Store from "Store";
import URL from "URL";
import Update from "Update";
import Using from "Using";
import Utility from "Utility";
import Validate from "Validate";
import Workspace from "Workspace";
import Za from "Za";
import Zeta from "Zeta";

export interface SecureConfig {
  ollamaUrl?: string;
  apiKey?: string;
  modelName?: string;
  enableTelemetry?: boolean;
  maxRequestsPerMinute?: number;
  securityLevel?: 'strict' | 'moderate' | 'relaxed';
}

export interface ConfigValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export class ConfigManager {
  private readonly context: vscode.ExtensionContext;
  private readonly secretStorage: vscode.SecretStorage;
  private readonly CONFIG_KEY = 'zetaAI.config';
  private readonly SECRET_KEYS = {
    API_KEY: 'zetaAI.apiKey',
    CUSTOM_ENDPOINTS: 'zetaAI.customEndpoints'
  };

  constructor(context: vscode.ExtensionContext) {
    this.context = context;
    this.secretStorage = context.secrets;
  }

  async getSecureConfig(): Promise<SecureConfig> {
    try {
      // Get public configuration from workspace settings
      const workspaceConfig = vscode.workspace.getConfiguration('zetaAI');
      
      // Get sensitive data from secret storage
      const apiKey = await this.secretStorage.get(this.SECRET_KEYS.API_KEY);
      const customEndpoints = await this.secretStorage.get(this.SECRET_KEYS.CUSTOM_ENDPOINTS);

      const config: SecureConfig = {
        ollamaUrl: workspaceConfig.get('ollamaUrl', 'http://localhost:11434'),
        modelName: workspaceConfig.get('defaultModel', 'deepseek-coder'),
        enableTelemetry: workspaceConfig.get('enableTelemetry', false),
        maxRequestsPerMinute: workspaceConfig.get('maxRequestsPerMinute', 60),
        securityLevel: workspaceConfig.get('securityLevel', 'moderate'),
        apiKey: apiKey || undefined
      };

      // Apply custom endpoints if available
      if (customEndpoints) {
        try {
          const endpoints = JSON.parse(customEndpoints);
          if (endpoints.ollama) {
            config.ollamaUrl = endpoints.ollama;
          }
        } catch (error) {
          console.warn('Failed to parse custom endpoints:', error);
        }
      }

      return config;
    } catch (error) {
      throw new Error(`Failed to retrieve secure configuration: ${error}`);
    }
  }

  async setSecureConfig(config: Partial<SecureConfig>): Promise<void> {
    try {
      const workspaceConfig = vscode.workspace.getConfiguration('zetaAI');

      // Update public settings
      if (config.ollamaUrl !== undefined) {
        await workspaceConfig.update('ollamaUrl', config.ollamaUrl, vscode.ConfigurationTarget.Workspace);
      }
      if (config.modelName !== undefined) {
        await workspaceConfig.update('defaultModel', config.modelName, vscode.ConfigurationTarget.Workspace);
      }
      if (config.enableTelemetry !== undefined) {
        await workspaceConfig.update('enableTelemetry', config.enableTelemetry, vscode.ConfigurationTarget.Global);
      }
      if (config.maxRequestsPerMinute !== undefined) {
        await workspaceConfig.update('maxRequestsPerMinute', config.maxRequestsPerMinute, vscode.ConfigurationTarget.Workspace);
      }
      if (config.securityLevel !== undefined) {
        await workspaceConfig.update('securityLevel', config.securityLevel, vscode.ConfigurationTarget.Workspace);
      }

      // Store sensitive data in secret storage
      if (config.apiKey !== undefined) {
        if (config.apiKey) {
          await this.secretStorage.store(this.SECRET_KEYS.API_KEY, config.apiKey);
        } else {
          await this.secretStorage.delete(this.SECRET_KEYS.API_KEY);
        }
      }
    } catch (error) {
      throw new Error(`Failed to save secure configuration: ${error}`);
    }
  }

  async validateConfig(config: SecureConfig): Promise<ConfigValidationResult> {
    const errors: string[] = [];
    const warnings: string[] = [];

    this.validateOllamaUrl(config.ollamaUrl, errors, warnings);
    this.validateModelName(config.modelName, warnings);
    this.validateSecurityLevel(config.securityLevel, errors);
    this.validateRateLimit(config.maxRequestsPerMinute, errors, warnings);
    this.validateApiKey(config.apiKey, warnings);

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  private validateOllamaUrl(ollamaUrl: string | undefined, errors: string[], warnings: string[]): void {
    if (!ollamaUrl) {
      errors.push('Ollama URL is required');
      return;
    }

    try {
      const url = new URL(ollamaUrl);
      if (!['http:', 'https:'].includes(url.protocol)) {
        errors.push('Ollama URL must use HTTP or HTTPS protocol');
      }
      if (url.protocol === 'http:' && !url.hostname.includes('localhost') && !url.hostname.includes('127.0.0.1')) {
        warnings.push('Using HTTP for non-local connections is not secure');
      }
    } catch {
      errors.push('Invalid Ollama URL format');
    }
  }

  private validateModelName(modelName: string | undefined, warnings: string[]): void {
    if (!modelName || modelName.trim().length === 0) {
      warnings.push('No model name specified, will use default');
    }
  }

  private validateSecurityLevel(securityLevel: string | undefined, errors: string[]): void {
    if (securityLevel && !['strict', 'moderate', 'relaxed'].includes(securityLevel)) {
      errors.push('Security level must be: strict, moderate, or relaxed');
    }
  }

  private validateRateLimit(maxRequestsPerMinute: number | undefined, errors: string[], warnings: string[]): void {
    if (maxRequestsPerMinute === undefined) return;

    if (maxRequestsPerMinute < 1 || maxRequestsPerMinute > 1000) {
      errors.push('Max requests per minute must be between 1 and 1000');
    }
    if (maxRequestsPerMinute > 100) {
      warnings.push('High request rate may impact performance');
    }
  }

  private validateApiKey(apiKey: string | undefined, warnings: string[]): void {
    if (!apiKey) return;

    if (apiKey.length < 8) {
      warnings.push('API key seems too short, ensure it\'s valid');
    }
    if (!/^[A-Za-z0-9\-_.]+$/.test(apiKey)) {
      warnings.push('API key contains unusual characters');
    }
  }

  async resetConfig(): Promise<void> {
    try {
      // Clear secret storage
      await this.secretStorage.delete(this.SECRET_KEYS.API_KEY);
      await this.secretStorage.delete(this.SECRET_KEYS.CUSTOM_ENDPOINTS);

      // Reset workspace configuration to defaults
      const workspaceConfig = vscode.workspace.getConfiguration('zetaAI');
      await workspaceConfig.update('ollamaUrl', undefined, vscode.ConfigurationTarget.Workspace);
      await workspaceConfig.update('defaultModel', undefined, vscode.ConfigurationTarget.Workspace);
      await workspaceConfig.update('maxRequestsPerMinute', undefined, vscode.ConfigurationTarget.Workspace);
      await workspaceConfig.update('securityLevel', undefined, vscode.ConfigurationTarget.Workspace);
    } catch (error) {
      throw new Error(`Failed to reset configuration: ${error}`);
    }
  }

  async exportConfig(includeSecrets = false): Promise<string> {
    try {
      const config = await this.getSecureConfig();
      
      const exportData = {
        ollamaUrl: config.ollamaUrl,
        modelName: config.modelName,
        enableTelemetry: config.enableTelemetry,
        maxRequestsPerMinute: config.maxRequestsPerMinute,
        securityLevel: config.securityLevel,
        ...(includeSecrets && { apiKey: config.apiKey })
      };

      return JSON.stringify(exportData, null, 2);
    } catch (error) {
      throw new Error(`Failed to export configuration: ${error}`);
    }
  }

  async importConfig(configJson: string, overwriteSecrets = false): Promise<ConfigValidationResult> {
    try {
      const config: SecureConfig = JSON.parse(configJson);
      
      // Validate before importing
      const validation = await this.validateConfig(config);
      if (!validation.isValid) {
        return validation;
      }

      // Import configuration
      if (overwriteSecrets || !config.apiKey) {
        await this.setSecureConfig(config);
      } else {
        // Import without secrets
        const { apiKey, ...publicConfig } = config;
        await this.setSecureConfig(publicConfig);
      }

      return validation;
    } catch (error) {
      return {
        isValid: false,
        errors: [`Failed to import configuration: ${error}`],
        warnings: []
      };
    }
  }

  // Event handlers for configuration changes
  onConfigurationChanged(callback: (config: SecureConfig) => void): vscode.Disposable {
    return vscode.workspace.onDidChangeConfiguration(async (event) => {
      if (event.affectsConfiguration('zetaAI')) {
        try {
          const config = await this.getSecureConfig();
          callback(config);
        } catch (error) {
          console.error('Error handling configuration change:', error);
        }
      }
    });
  }

  // Utility methods
  async testConnection(): Promise<boolean> {
    try {
      const config = await this.getSecureConfig();
      if (!config.ollamaUrl) {
        return false;
      }

      const response = await fetch(`${config.ollamaUrl}/api/version`, {
        method: 'GET',
        signal: AbortSignal.timeout(5000)
      });

      return response.ok;
    } catch {
      return false;
    }
  }

  async getApiKeyMasked(): Promise<string> {
    const apiKey = await this.secretStorage.get(this.SECRET_KEYS.API_KEY);
    if (!apiKey) {
      return 'Not set';
    }
    return apiKey.substring(0, 4) + '*'.repeat(Math.max(0, apiKey.length - 8)) + 
           (apiKey.length > 4 ? apiKey.substring(apiKey.length - 4) : '');
  }
}
