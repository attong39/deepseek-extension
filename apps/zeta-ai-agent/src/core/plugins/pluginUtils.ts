/**
 * Plugin Registry Utilities
 * Helper functions and base classes for plugin development
 */

import { 
  PluginAPI, 
  PluginMetadata, 
  PluginExecutionContext, 
  PluginCapability,
  PluginConfigSchema,
  SecurityLevel,
  PluginEnvironment
} from './pluginRegistry';

/**
 * Base plugin implementation with common functionality
 */
export abstract class BasePlugin implements PluginAPI {
  protected readonly metadata: PluginMetadata;
  protected config: Record<string, any> = {};
  protected initialized = false;

  constructor(metadata: PluginMetadata) {
    this.metadata = metadata;
  }

  /**
   * Plugin initialization - override for custom setup
   */
  async initialize(config: Record<string, any>): Promise<void> {
    this.validateConfig(config);
    this.config = config;
    this.initialized = true;
    await this.onInitialize();
  }

  /**
   * Main execution method - must be implemented by subclasses
   */
  abstract execute(input: any, context: PluginExecutionContext): Promise<any>;

  /**
   * Plugin cleanup - override for custom cleanup
   */
  async cleanup(): Promise<void> {
    await this.onCleanup();
    this.initialized = false;
    this.config = {};
  }

  /**
   * Get plugin capabilities
   */
  getCapabilities(): PluginCapability[] {
    return this.metadata.capabilities;
  }

  /**
   * Get configuration schema - must be implemented by subclasses
   */
  abstract getConfigSchema(): PluginConfigSchema;

  /**
   * Health check implementation
   */
  async healthCheck(): Promise<{ status: 'healthy' | 'unhealthy'; message?: string }> {
    if (!this.initialized) {
      return { status: 'unhealthy', message: 'Plugin not initialized' };
    }

    try {
      const healthy = await this.performHealthCheck();
      return healthy 
        ? { status: 'healthy', message: 'Plugin is operating normally' }
        : { status: 'unhealthy', message: 'Plugin health check failed' };
    } catch (error) {
      return { 
        status: 'unhealthy', 
        message: `Health check error: ${(error as Error).message}` 
      };
    }
  }

  /**
   * Protected methods for subclass customization
   */
  protected async onInitialize(): Promise<void> {
    // Override in subclasses for custom initialization
  }

  protected async onCleanup(): Promise<void> {
    // Override in subclasses for custom cleanup
  }

  protected async performHealthCheck(): Promise<boolean> {
    // Override in subclasses for custom health checks
    return true;
  }

  protected validateConfig(config: Record<string, any>): void {
    const schema = this.getConfigSchema();
    
    // Check required properties
    for (const required of schema.required) {
      if (!(required in config)) {
        throw new Error(`Required configuration property '${required}' is missing`);
      }
    }

    // Validate property types
    for (const [key, value] of Object.entries(config)) {
      const propSchema = schema.properties[key];
      if (!propSchema) continue;

      const actualType = Array.isArray(value) ? 'array' : typeof value;
      if (actualType !== propSchema.type) {
        throw new Error(`Configuration property '${key}' must be of type ${propSchema.type}`);
      }
    }
  }

  protected assertInitialized(): void {
    if (!this.initialized) {
      throw new Error('Plugin not initialized. Call initialize() first.');
    }
  }

  protected getMetadata(): PluginMetadata {
    return { ...this.metadata };
  }

  protected getConfig(): Record<string, any> {
    return { ...this.config };
  }
}

/**
 * Plugin builder for easy plugin creation
 */
export class PluginBuilder {
  private metadata: Partial<PluginMetadata> = {};
  private configSchema: PluginConfigSchema = { properties: {}, required: [] };
  private executeFn?: (input: any, context: PluginExecutionContext) => Promise<any>;
  private initializeFn?: (config: Record<string, any>) => Promise<void>;
  private cleanupFn?: () => Promise<void>;
  private healthCheckFn?: () => Promise<boolean>;

  /**
   * Set plugin metadata
   */
  setMetadata(metadata: {
    id: string;
    name: string;
    version: string;
    description: string;
    author: string;
    capabilities: PluginCapability[];
    securityLevel?: SecurityLevel;
    environment?: PluginEnvironment;
    keywords?: string[];
    license?: string;
  }): this {
    this.metadata = {
      ...metadata,
      securityLevel: metadata.securityLevel || 'RESTRICTED',
      environment: metadata.environment || 'SANDBOX',
      keywords: metadata.keywords || [],
      license: metadata.license || 'MIT',
      createdAt: new Date(),
      updatedAt: new Date()
    };
    return this;
  }

  /**
   * Set configuration schema
   */
  setConfigSchema(schema: PluginConfigSchema): this {
    this.configSchema = schema;
    return this;
  }

  /**
   * Add configuration property
   */
  addConfigProperty(
    name: string,
    type: 'string' | 'number' | 'boolean' | 'object' | 'array',
    options: {
      description: string;
      required?: boolean;
      default?: any;
      enum?: any[];
      validation?: {
        min?: number;
        max?: number;
        pattern?: string;
        format?: string;
      };
    }
  ): this {
    this.configSchema.properties[name] = {
      type,
      description: options.description,
      required: options.required,
      default: options.default,
      enum: options.enum,
      validation: options.validation
    };

    if (options.required) {
      this.configSchema.required.push(name);
    }

    return this;
  }

  /**
   * Set execute function
   */
  setExecute(fn: (input: any, context: PluginExecutionContext) => Promise<any>): this {
    this.executeFn = fn;
    return this;
  }

  /**
   * Set initialize function
   */
  setInitialize(fn: (config: Record<string, any>) => Promise<void>): this {
    this.initializeFn = fn;
    return this;
  }

  /**
   * Set cleanup function
   */
  setCleanup(fn: () => Promise<void>): this {
    this.cleanupFn = fn;
    return this;
  }

  /**
   * Set health check function
   */
  setHealthCheck(fn: () => Promise<boolean>): this {
    this.healthCheckFn = fn;
    return this;
  }

  /**
   * Build the plugin
   */
  build(): PluginAPI {
    if (!this.metadata.id || !this.metadata.name || !this.metadata.version) {
      throw new Error('Plugin must have id, name, and version');
    }

    if (!this.executeFn) {
      throw new Error('Plugin must have an execute function');
    }

    if (!this.metadata.capabilities || this.metadata.capabilities.length === 0) {
      throw new Error('Plugin must declare at least one capability');
    }

    const metadata = this.metadata as PluginMetadata;
    const executeFn = this.executeFn;
    const initializeFn = this.initializeFn;
    const cleanupFn = this.cleanupFn;
    const healthCheckFn = this.healthCheckFn;
    const configSchema = this.configSchema;

    return {
      async initialize(config: Record<string, any>): Promise<void> {
        if (initializeFn) {
          await initializeFn(config);
        }
      },

      async execute(input: any, context: PluginExecutionContext): Promise<any> {
        return await executeFn(input, context);
      },

      async cleanup(): Promise<void> {
        if (cleanupFn) {
          await cleanupFn();
        }
      },

      getCapabilities(): PluginCapability[] {
        return metadata.capabilities;
      },

      getConfigSchema(): PluginConfigSchema {
        return configSchema;
      },

      async healthCheck(): Promise<{ status: 'healthy' | 'unhealthy'; message?: string }> {
        if (healthCheckFn) {
          try {
            const healthy = await healthCheckFn();
            return healthy 
              ? { status: 'healthy', message: 'Plugin is operating normally' }
              : { status: 'unhealthy', message: 'Health check failed' };
          } catch (error) {
            return { 
              status: 'unhealthy', 
              message: `Health check error: ${(error as Error).message}` 
            };
          }
        }
        return { status: 'healthy', message: 'No health check implemented' };
      }
    };
  }
}

/**
 * Plugin utilities
 */
export class PluginUtils {
  /**
   * Create simple data processing plugin
   */
  static createDataProcessor(
    metadata: {
      id: string;
      name: string;
      version: string;
      description: string;
      author: string;
      keywords?: string[];
    },
    processor: (data: any, context: PluginExecutionContext) => Promise<any>
  ): PluginAPI {
    return new PluginBuilder()
      .setMetadata({
        ...metadata,
        capabilities: ['DATA_PROCESSING'],
        securityLevel: 'RESTRICTED',
        environment: 'SANDBOX'
      })
      .addConfigProperty('inputFormat', 'string', {
        description: 'Expected input data format',
        required: false,
        default: 'json'
      })
      .addConfigProperty('outputFormat', 'string', {
        description: 'Output data format',
        required: false,
        default: 'json'
      })
      .setExecute(processor)
      .build();
  }

  /**
   * Create external API plugin
   */
  static createAPIClient(
    metadata: {
      id: string;
      name: string;
      version: string;
      description: string;
      author: string;
      keywords?: string[];
    },
    apiHandler: (input: any, context: PluginExecutionContext) => Promise<any>
  ): PluginAPI {
    return new PluginBuilder()
      .setMetadata({
        ...metadata,
        capabilities: ['EXTERNAL_API', 'NETWORK_ACCESS'],
        securityLevel: 'RESTRICTED',
        environment: 'ISOLATED'
      })
      .addConfigProperty('apiKey', 'string', {
        description: 'API authentication key',
        required: true
      })
      .addConfigProperty('baseUrl', 'string', {
        description: 'API base URL',
        required: true
      })
      .addConfigProperty('timeout', 'number', {
        description: 'Request timeout in milliseconds',
        required: false,
        default: 30000,
        validation: { min: 1000, max: 120000 }
      })
      .addConfigProperty('retries', 'number', {
        description: 'Number of retry attempts',
        required: false,
        default: 3,
        validation: { min: 0, max: 10 }
      })
      .setExecute(apiHandler)
      .build();
  }

  /**
   * Create file operations plugin
   */
  static createFileProcessor(
    metadata: {
      id: string;
      name: string;
      version: string;
      description: string;
      author: string;
      keywords?: string[];
    },
    fileHandler: (input: any, context: PluginExecutionContext) => Promise<any>
  ): PluginAPI {
    return new PluginBuilder()
      .setMetadata({
        ...metadata,
        capabilities: ['FILE_OPERATIONS'],
        securityLevel: 'RESTRICTED',
        environment: 'SANDBOX'
      })
      .addConfigProperty('allowedExtensions', 'array', {
        description: 'Allowed file extensions',
        required: false,
        default: ['.txt', '.json', '.csv']
      })
      .addConfigProperty('maxFileSize', 'number', {
        description: 'Maximum file size in bytes',
        required: false,
        default: 10485760, // 10MB
        validation: { min: 1024, max: 104857600 } // 1KB to 100MB
      })
      .addConfigProperty('workingDirectory', 'string', {
        description: 'Working directory for file operations',
        required: false,
        default: './temp'
      })
      .setExecute(fileHandler)
      .build();
  }

  /**
   * Create AI model plugin
   */
  static createAIModel(
    metadata: {
      id: string;
      name: string;
      version: string;
      description: string;
      author: string;
      keywords?: string[];
    },
    modelHandler: (input: any, context: PluginExecutionContext) => Promise<any>
  ): PluginAPI {
    return new PluginBuilder()
      .setMetadata({
        ...metadata,
        capabilities: ['AI_MODELS', 'CUSTOM_REASONING'],
        securityLevel: 'PRIVATE',
        environment: 'ISOLATED'
      })
      .addConfigProperty('modelName', 'string', {
        description: 'AI model name or identifier',
        required: true
      })
      .addConfigProperty('temperature', 'number', {
        description: 'Model temperature (creativity level)',
        required: false,
        default: 0.7,
        validation: { min: 0, max: 2 }
      })
      .addConfigProperty('maxTokens', 'number', {
        description: 'Maximum number of tokens to generate',
        required: false,
        default: 1000,
        validation: { min: 1, max: 8192 }
      })
      .addConfigProperty('enableStreaming', 'boolean', {
        description: 'Enable streaming responses',
        required: false,
        default: false
      })
      .setExecute(modelHandler)
      .build();
  }

  /**
   * Validate plugin metadata
   */
  static validateMetadata(metadata: PluginMetadata): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!metadata.id || metadata.id.trim().length === 0) {
      errors.push('Plugin ID is required');
    }

    if (!/^[a-zA-Z0-9-_]+$/.test(metadata.id)) {
      errors.push('Plugin ID must contain only alphanumeric characters, hyphens, and underscores');
    }

    if (!metadata.name || metadata.name.trim().length === 0) {
      errors.push('Plugin name is required');
    }

    if (!metadata.version || !/^\d+\.\d+\.\d+/.test(metadata.version)) {
      errors.push('Plugin version must follow semantic versioning (e.g., 1.0.0)');
    }

    if (!metadata.description || metadata.description.trim().length === 0) {
      errors.push('Plugin description is required');
    }

    if (!metadata.author || metadata.author.trim().length === 0) {
      errors.push('Plugin author is required');
    }

    if (!metadata.capabilities || metadata.capabilities.length === 0) {
      errors.push('Plugin must declare at least one capability');
    }

    if (!metadata.license || metadata.license.trim().length === 0) {
      errors.push('Plugin license is required');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Generate plugin template
   */
  static generateTemplate(
    type: 'data-processor' | 'api-client' | 'file-processor' | 'ai-model' | 'custom',
    pluginId: string,
    pluginName: string
  ): string {
    const templates = {
      'data-processor': `
import { PluginUtils, PluginExecutionContext } from '../pluginUtils';

// Data Processing Plugin: ${pluginName}
export const ${pluginId.replace(/-/g, '')}Plugin = PluginUtils.createDataProcessor(
  {
    id: '${pluginId}',
    name: '${pluginName}',
    version: '1.0.0',
    description: 'A data processing plugin',
    author: 'Your Name',
    keywords: ['data', 'processing']
  },
  async (data: any, context: PluginExecutionContext) => {
    context.logger.info('Processing data', { inputType: typeof data });
    
    // TODO: Implement your data processing logic here
    const result = {
      processed: true,
      timestamp: new Date().toISOString(),
      input: data
    };
    
    context.metrics.counter('data_processed');
    return result;
  }
);
      `,
      'api-client': `
import { PluginUtils, PluginExecutionContext } from '../pluginUtils';

// API Client Plugin: ${pluginName}
export const ${pluginId.replace(/-/g, '')}Plugin = PluginUtils.createAPIClient(
  {
    id: '${pluginId}',
    name: '${pluginName}',
    version: '1.0.0',
    description: 'An API client plugin',
    author: 'Your Name',
    keywords: ['api', 'client']
  },
  async (input: any, context: PluginExecutionContext) => {
    context.logger.info('Making API request', { endpoint: input.endpoint });
    
    // TODO: Implement your API client logic here
    const response = {
      success: true,
      data: 'API response data',
      timestamp: new Date().toISOString()
    };
    
    context.metrics.counter('api_requests');
    context.metrics.timer('api_response_time', Date.now() - context.timestamp.getTime());
    return response;
  }
);
      `,
      'file-processor': `
import { PluginUtils, PluginExecutionContext } from '../pluginUtils';

// File Processing Plugin: ${pluginName}
export const ${pluginId.replace(/-/g, '')}Plugin = PluginUtils.createFileProcessor(
  {
    id: '${pluginId}',
    name: '${pluginName}',
    version: '1.0.0',
    description: 'A file processing plugin',
    author: 'Your Name',
    keywords: ['file', 'processing']
  },
  async (input: any, context: PluginExecutionContext) => {
    context.logger.info('Processing file', { filename: input.filename });
    
    // TODO: Implement your file processing logic here
    const result = {
      processed: true,
      filename: input.filename,
      size: input.size || 0,
      timestamp: new Date().toISOString()
    };
    
    context.metrics.counter('files_processed');
    context.metrics.gauge('file_size', input.size || 0);
    return result;
  }
);
      `,
      'ai-model': `
import { PluginUtils, PluginExecutionContext } from '../pluginUtils';

// AI Model Plugin: ${pluginName}
export const ${pluginId.replace(/-/g, '')}Plugin = PluginUtils.createAIModel(
  {
    id: '${pluginId}',
    name: '${pluginName}',
    version: '1.0.0',
    description: 'An AI model plugin',
    author: 'Your Name',
    keywords: ['ai', 'model', 'ml']
  },
  async (input: any, context: PluginExecutionContext) => {
    context.logger.info('Running AI model', { prompt: input.prompt?.substring(0, 100) });
    
    // TODO: Implement your AI model logic here
    const result = {
      response: 'AI generated response',
      tokens: 150,
      model: 'your-model-name',
      timestamp: new Date().toISOString()
    };
    
    context.metrics.counter('ai_requests');
    context.metrics.gauge('tokens_generated', result.tokens);
    return result;
  }
);
      `,
      'custom': `
import { BasePlugin, PluginExecutionContext, PluginConfigSchema } from '../pluginUtils';
import A from "A";
import AI from "AI";
import AI_MODELS from "AI_MODELS";
import API from "../../../../desktop/src/API/index";
import Add from "Add";
import Allowed from "Allowed";
import An from "An";
import Base from "Base";
import Build from "Build";
import CUSTOM_REASONING from "CUSTOM_REASONING";
import Call from "Call";
import Check from "Check";
import Client from "Client";
import Configuration from "Configuration";
import Counter from "Counter";
import Create from "Create";
import Custom from "Custom";
import DATA_PROCESSING from "DATA_PROCESSING";
import Data from "Data";
import Define from "Define";
import EXTERNAL_API from "EXTERNAL_API";
import Enable from "Enable";
import Error from "Error";
import Example from "Example";
import Executing from "Executing";
import Expected from "Expected";
import FILE_OPERATIONS from "FILE_OPERATIONS";
import File from "File";
import Gauge from "Gauge";
import Generate from "Generate";
import Get from "Get";
import Health from "Health";
import Helper from "Helper";
import ID from "ID";
import ISOLATED from "ISOLATED";
import Implement from "Implement";
import METRIC from "METRIC";
import MIT from "MIT";
import Main from "../../../../desktop/src/Main";
import Making from "Making";
import Math from "Math";
import Maximum from "Maximum";
import Measure from "Measure";
import Model from "Model";
import NETWORK_ACCESS from "NETWORK_ACCESS";
import Name from "Name";
import No from "No";
import Output from "Output";
import Override from "Override";
import PRIVATE from "PRIVATE";
import Partial from "Partial";
import Plugin from "Plugin";
import PluginBuilder from "PluginBuilder";
import PluginHelpers from "PluginHelpers";
import Processing from "Processing";
import Protected from "Protected";
import RESTRICTED from "RESTRICTED";
import Record from "Record";
import Registry from "Registry";
import Request from "Request";
import Required from "Required";
import Running from "Running";
import SANDBOX from "SANDBOX";
import Set from "Set";
import T from "T";
import TEST from "../../../../desktop/src/TEST/index";
import TODO from "TODO";
import Timer from "Timer";
import URL from "URL";
import Update from "Update";
import Utilities from "Utilities";
import Validate from "Validate";
import Working from "Working";
import Your from "Your";
import Z0 from "Z0";

// Custom Plugin: ${pluginName}
export class ${pluginId.replace(/-/g, '')}Plugin extends BasePlugin {
  constructor() {
    super({
      id: '${pluginId}',
      name: '${pluginName}',
      version: '1.0.0',
      description: 'A custom plugin',
      author: 'Your Name',
      license: 'MIT',
      keywords: ['custom'],
      capabilities: ['CUSTOM_REASONING'], // Update as needed
      securityLevel: 'RESTRICTED',
      environment: 'SANDBOX',
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  getConfigSchema(): PluginConfigSchema {
    return {
      properties: {
        // TODO: Define your configuration schema
        setting1: {
          type: 'string',
          description: 'Example setting',
          required: false,
          default: 'default-value'
        }
      },
      required: []
    };
  }

  async execute(input: any, context: PluginExecutionContext): Promise<any> {
    this.assertInitialized();
    
    context.logger.info('Executing custom plugin', { input: typeof input });
    
    // TODO: Implement your custom logic here
    const result = {
      success: true,
      timestamp: new Date().toISOString(),
      input
    };
    
    context.metrics.counter('custom_executions');
    return result;
  }

  protected async performHealthCheck(): Promise<boolean> {
    // TODO: Implement your health check logic
    return true;
  }
}
      `
    };

    return templates[type].trim();
  }
}

/**
 * Plugin development helpers
 */
export const PluginHelpers = {
  /**
   * Create a simple execution context for testing
   */
  createTestContext(overrides?: Partial<PluginExecutionContext>): PluginExecutionContext {
    return {
      requestId: 'test-request-' + Math.random().toString(36).substring(2, 9),
      timestamp: new Date(),
      environment: 'SANDBOX',
      permissions: {
        allowNetworkAccess: false,
        allowFileAccess: false,
        allowSystemAccess: false,
        allowDatabaseAccess: false,
        maxExecutionTime: 10000,
        maxMemoryUsage: 50 * 1024 * 1024 // 50MB
      },
      logger: {
        debug: (message, metadata) => console.debug(`[TEST] ${message}`, metadata),
        info: (message, metadata) => console.info(`[TEST] ${message}`, metadata),
        warn: (message, metadata) => console.warn(`[TEST] ${message}`, metadata),
        error: (message, error, metadata) => console.error(`[TEST] ${message}`, error, metadata)
      },
      metrics: {
        counter: (name, value, labels) => console.debug(`[METRIC] Counter: ${name} = ${value}`, labels),
        gauge: (name, value, labels) => console.debug(`[METRIC] Gauge: ${name} = ${value}`, labels),
        timer: (name, value, labels) => console.debug(`[METRIC] Timer: ${name} = ${value}ms`, labels)
      },
      ...overrides
    };
  },

  /**
   * Measure plugin execution time
   */
  async measureExecution<T>(
    plugin: PluginAPI,
    input: any,
    context: PluginExecutionContext
  ): Promise<{ result: T; executionTime: number; memoryUsed: number }> {
    const startTime = Date.now();
    const startMemory = process.memoryUsage().heapUsed;

    const result = await plugin.execute(input, context);

    const executionTime = Date.now() - startTime;
    const memoryUsed = process.memoryUsage().heapUsed - startMemory;

    return { result, executionTime, memoryUsed };
  },

  /**
   * Validate plugin against test cases
   */
  async validatePlugin(
    plugin: PluginAPI,
    testCases: Array<{
      name: string;
      input: any;
      expectedOutput?: any;
      shouldFail?: boolean;
      context?: Partial<PluginExecutionContext>;
    }>
  ): Promise<Array<{ name: string; passed: boolean; error?: string; result?: any }>> {
    const results = [];

    for (const testCase of testCases) {
      const context = this.createTestContext(testCase.context);
      
      try {
        const result = await plugin.execute(testCase.input, context);
        
        if (testCase.shouldFail) {
          results.push({
            name: testCase.name,
            passed: false,
            error: 'Expected test to fail but it succeeded',
            result
          });
        } else if (testCase.expectedOutput) {
          const passed = JSON.stringify(result) === JSON.stringify(testCase.expectedOutput);
          results.push({
            name: testCase.name,
            passed,
            error: passed ? undefined : 'Output does not match expected result',
            result
          });
        } else {
          results.push({
            name: testCase.name,
            passed: true,
            result
          });
        }
      } catch (error) {
        if (testCase.shouldFail) {
          results.push({
            name: testCase.name,
            passed: true,
            result: { error: (error as Error).message }
          });
        } else {
          results.push({
            name: testCase.name,
            passed: false,
            error: (error as Error).message
          });
        }
      }
    }

    return results;
  }
};
