import ACTIVE from "ACTIVE";
import AI from "AI";
import AI_MODELS from "AI_MODELS";
import API from "../../../../desktop/src/API/index";
import Apply from "Apply";
import CAPABILITY from "CAPABILITY";
import CUSTOM_REASONING from "CUSTOM_REASONING";
import Cannot from "Cannot";
import Capability from "Capability";
import Check from "Check";
import Clean from "Clean";
import Cleanup from "Cleanup";
import Configuration from "Configuration";
import Create from "Create";
import DATABASE_ACCESS from "DATABASE_ACCESS";
import DATA_PROCESSING from "DATA_PROCESSING";
import DEBUG from "DEBUG";
import DEPENDENCY from "DEPENDENCY";
import DISABLED from "DISABLED";
import Destroy from "Destroy";
import Discover from "Discover";
import Distribution from "Distribution";
import Dynamic from "Dynamic";
import ERROR from "ERROR";
import EXECUTED from "EXECUTED";
import EXECUTION_ERROR from "EXECUTION_ERROR";
import EXTERNAL_API from "EXTERNAL_API";
import Enables from "Enables";
import Error from "Error";
import Exclusive from "Exclusive";
import Execute from "Execute";
import FILE_OPERATIONS from "FILE_OPERATIONS";
import Failed from "Failed";
import Fast from "Fast";
import Find from "Find";
import For from "For";
import Generate from "Generate";
import Get from "Get";
import Health from "Health";
import High from "High";
import INACTIVE from "INACTIVE";
import INFO from "INFO";
import ISOLATED from "ISOLATED";
import In from "In";
import Initialize from "Initialize";
import Isolated from "Isolated";
import It from "It";
import LOADING from "LOADING";
import List from "List";
import Map from "Map";
import Math from "Math";
import Missing from "Missing";
import NETWORK_ACCESS from "NETWORK_ACCESS";
import NodeJS from "NodeJS";
import PRIVATE from "PRIVATE";
import PUBLIC from "PUBLIC";
import Partial from "Partial";
import Plugin from "Plugin";
import PluginAPI from "PluginAPI";
import PluginCapability from "PluginCapability";
import PluginConfigSchema from "PluginConfigSchema";
import PluginConflictType from "PluginConflictType";
import PluginDependency from "PluginDependency";
import PluginDiscoveryResult from "PluginDiscoveryResult";
import PluginEnvironment from "PluginEnvironment";
import PluginExecutionContext from "PluginExecutionContext";
import PluginExecutionResult from "PluginExecutionResult";
import PluginMetadata from "PluginMetadata";
import PluginMetric from "PluginMetric";
import PluginRegistration from "PluginRegistration";
import PluginRegistry from "./PluginRegistry";
import PluginSandbox from "PluginSandbox";
import PluginStatus from "PluginStatus";
import Private from "Private";
import REGISTERED from "REGISTERED";
import RESTRICTED from "RESTRICTED";
import Record from "Record";
import RegExp from "RegExp";
import Register from "Register";
import Registry from "Registry";
import Remove from "Remove";
import Required from "Required";
import Resolve from "Resolve";
import SANDBOX from "SANDBOX";
import SECURITY from "SECURITY";
import SYSTEM from "SYSTEM";
import SYSTEM_COMMANDS from "SYSTEM_COMMANDS";
import SecurityLevel from "SecurityLevel";
import Semantic from "Semantic";
import Set from "Set";
import Simplified from "Simplified";
import Supports from "Supports";
import System from "System";
import T from "T";
import TRUSTED from "TRUSTED";
import This from "This";
import Timeout from "Timeout";
import UNREGISTERED from "UNREGISTERED";
import USER_INTERFACE from "USER_INTERFACE";
import Unregister from "Unregister";
import Update from "Update";
import Usage from "Usage";
import Validate from "Validate";
import Version from "Version";
import WARN from "WARN";
import WORKFLOW_AUTOMATION from "WORKFLOW_AUTOMATION";
import Wait from "Wait";
/**
 * Plugin Registry System
 * Dynamic plugin management with capability discovery, dependency resolution, and sandboxing
 * Enables the autonomous AI to extend its capabilities through plugins
 */

/**
 * Plugin capability types
 */
export type PluginCapability = 
  | 'DATA_PROCESSING'
  | 'EXTERNAL_API'
  | 'FILE_OPERATIONS'
  | 'NETWORK_ACCESS'
  | 'DATABASE_ACCESS'
  | 'SYSTEM_COMMANDS'
  | 'AI_MODELS'
  | 'CUSTOM_REASONING'
  | 'USER_INTERFACE'
  | 'WORKFLOW_AUTOMATION';

/**
 * Plugin execution environment
 */
export type PluginEnvironment = 'SANDBOX' | 'ISOLATED' | 'TRUSTED' | 'SYSTEM';

/**
 * Plugin status
 */
export type PluginStatus = 'INACTIVE' | 'LOADING' | 'ACTIVE' | 'ERROR' | 'DISABLED';

/**
 * Plugin security level
 */
export type SecurityLevel = 'PUBLIC' | 'RESTRICTED' | 'PRIVATE' | 'SYSTEM';

/**
 * Plugin metadata
 */
export interface PluginMetadata {
  id: string;
  name: string;
  version: string;
  description: string;
  author: string;
  homepage?: string;
  repository?: string;
  license: string;
  keywords: string[];
  capabilities: PluginCapability[];
  securityLevel: SecurityLevel;
  environment: PluginEnvironment;
  createdAt: Date;
  updatedAt: Date;
}

/**
 * Plugin dependency specification
 */
export interface PluginDependency {
  pluginId: string;
  version: string; // Semantic version or range
  optional: boolean;
  reason: string;
}

/**
 * Plugin configuration schema
 */
export interface PluginConfigSchema {
  properties: Record<string, {
    type: 'string' | 'number' | 'boolean' | 'object' | 'array';
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
  }>;
  required: string[];
}

/**
 * Plugin API definition
 */
export interface PluginAPI {
  initialize?(config: Record<string, any>): Promise<void>;
  execute(input: any, context: PluginExecutionContext): Promise<any>;
  cleanup?(): Promise<void>;
  getCapabilities(): PluginCapability[];
  getConfigSchema(): PluginConfigSchema;
  healthCheck?(): Promise<{ status: 'healthy' | 'unhealthy'; message?: string }>;
}

/**
 * Plugin execution context
 */
export interface PluginExecutionContext {
  requestId: string;
  userId?: string;
  sessionId?: string;
  timestamp: Date;
  environment: PluginEnvironment;
  permissions: {
    allowNetworkAccess: boolean;
    allowFileAccess: boolean;
    allowSystemAccess: boolean;
    allowDatabaseAccess: boolean;
    maxExecutionTime: number; // milliseconds
    maxMemoryUsage: number; // bytes
  };
  logger: {
    debug(message: string, metadata?: any): void;
    info(message: string, metadata?: any): void;
    warn(message: string, metadata?: any): void;
    error(message: string, error?: Error, metadata?: any): void;
  };
  metrics: {
    counter(name: string, value?: number, labels?: Record<string, string>): void;
    gauge(name: string, value: number, labels?: Record<string, string>): void;
    timer(name: string, value: number, labels?: Record<string, string>): void;
  };
}

/**
 * Plugin execution result
 */
export interface PluginExecutionResult {
  success: boolean;
  data?: any;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  metadata: {
    executionTime: number;
    memoryUsed: number;
    warnings: string[];
    capabilities: PluginCapability[];
  };
}

/**
 * Plugin registration info
 */
export interface PluginRegistration {
  metadata: PluginMetadata;
  api: PluginAPI;
  dependencies: PluginDependency[];
  configuration: Record<string, any>;
  status: PluginStatus;
  sandbox?: PluginSandbox;
  loadedAt?: Date;
  lastUsed?: Date;
  usageCount: number;
  errorCount: number;
  performanceMetrics: {
    averageExecutionTime: number;
    totalExecutions: number;
    successRate: number;
  };
}

/**
 * Plugin sandbox for isolation
 */
export interface PluginSandbox {
  id: string;
  environment: PluginEnvironment;
  permissions: PluginExecutionContext['permissions'];
  resourceLimits: {
    maxCpuUsage: number;
    maxMemoryUsage: number;
    maxExecutionTime: number;
    maxConcurrentExecutions: number;
  };
  isolatedContext: any; // Isolated execution context
  activeExecutions: Set<string>;
}

/**
 * Plugin conflict type
 */
export type PluginConflictType = 'DEPENDENCY' | 'CAPABILITY' | 'SECURITY';

/**
 * Plugin discovery result
 */
export interface PluginDiscoveryResult {
  availablePlugins: PluginMetadata[];
  compatiblePlugins: PluginMetadata[];
  recommendations: Array<{
    plugin: PluginMetadata;
    reason: string;
    confidence: number;
  }>;
  conflicts: Array<{
    pluginId: string;
    conflictType: PluginConflictType;
    description: string;
  }>;
}

/**
 * Plugin Registry implementation
 */
export class PluginRegistry {
  private readonly plugins: Map<string, PluginRegistration> = new Map();
  private readonly sandboxes: Map<string, PluginSandbox> = new Map();
  private readonly capabilityIndex: Map<PluginCapability, Set<string>> = new Map();
  private readonly dependencyGraph: Map<string, Set<string>> = new Map();
  private readonly executionQueue: Array<{ 
    pluginId: string; 
    context: PluginExecutionContext; 
    resolve: (value: PluginExecutionResult) => void; 
    reject: (reason: any) => void;
  }> = [];
  
  private readonly maxConcurrentExecutions: number = 10;
  private readonly defaultTimeout: number = 30000; // 30 seconds
  private readonly sandboxCleanupInterval: number = 300000; // 5 minutes
  
  private cleanupTimer?: NodeJS.Timeout;
  private executingCount = 0;

  constructor() {
    this.initializeCapabilityIndex();
    this.startSandboxCleanup();
  }

  /**
   * Register a new plugin
   */
  async registerPlugin(
    metadata: PluginMetadata,
    api: PluginAPI,
    dependencies: PluginDependency[] = [],
    configuration: Record<string, any> = {}
  ): Promise<void> {
    // Validate plugin metadata
    this.validatePluginMetadata(metadata);
    
    // Check for conflicts
    const conflicts = await this.checkPluginConflicts(metadata, dependencies);
    if (conflicts.length > 0) {
      throw new Error(`Plugin conflicts detected: ${conflicts.map(c => c.description).join(', ')}`);
    }

    // Resolve dependencies
    await this.resolveDependencies(metadata.id, dependencies);

    // Create sandbox if needed
    let sandbox: PluginSandbox | undefined;
    if (metadata.environment !== 'TRUSTED') {
      sandbox = await this.createSandbox(metadata);
    }

    // Validate configuration against schema
    const configSchema = api.getConfigSchema();
    this.validateConfiguration(configuration, configSchema);

    // Initialize plugin
    try {
      if (api.initialize) {
        await this.executeInSandbox(metadata.id, async () => {
          await api.initialize!(configuration);
        }, sandbox);
      }

      const registration: PluginRegistration = {
        metadata,
        api,
        dependencies,
        configuration,
        status: 'ACTIVE',
        sandbox,
        loadedAt: new Date(),
        usageCount: 0,
        errorCount: 0,
        performanceMetrics: {
          averageExecutionTime: 0,
          totalExecutions: 0,
          successRate: 1.0
        }
      };

      this.plugins.set(metadata.id, registration);
      
      // Update capability index
      this.updateCapabilityIndex(metadata);
      
      // Update dependency graph
      this.updateDependencyGraph(metadata.id, dependencies);

      this.logPluginEvent('REGISTERED', metadata.id, { 
        version: metadata.version,
        capabilities: metadata.capabilities,
        environment: metadata.environment 
      });

    } catch (error) {
      if (sandbox) {
        await this.destroySandbox(sandbox.id);
      }
      throw new Error(`Failed to initialize plugin ${metadata.id}: ${(error as Error).message}`);
    }
  }

  /**
   * Unregister a plugin
   */
  async unregisterPlugin(pluginId: string): Promise<void> {
    const plugin = this.plugins.get(pluginId);
    if (!plugin) {
      throw new Error(`Plugin ${pluginId} not found`);
    }

    // Check for dependent plugins
    const dependents = this.findDependentPlugins(pluginId);
    if (dependents.length > 0) {
      throw new Error(`Cannot unregister plugin ${pluginId}. It is required by: ${dependents.join(', ')}`);
    }

    // Cleanup plugin
    try {
      if (plugin.api.cleanup) {
        await this.executeInSandbox(pluginId, async () => {
          await plugin.api.cleanup!();
        }, plugin.sandbox);
      }
    } catch (error) {
      console.warn(`Plugin ${pluginId} cleanup failed: ${(error as Error).message}`);
    }

    // Destroy sandbox
    if (plugin.sandbox) {
      await this.destroySandbox(plugin.sandbox.id);
    }

    // Remove from indexes
    this.removeFromCapabilityIndex(plugin.metadata);
    this.dependencyGraph.delete(pluginId);

    this.plugins.delete(pluginId);

    this.logPluginEvent('UNREGISTERED', pluginId);
  }

  /**
   * Execute plugin with input
   */
  async executePlugin(
    pluginId: string,
    input: any,
    context?: Partial<PluginExecutionContext>
  ): Promise<PluginExecutionResult> {
    const plugin = this.plugins.get(pluginId);
    if (!plugin) {
      throw new Error(`Plugin ${pluginId} not found`);
    }

    if (plugin.status !== 'ACTIVE') {
      throw new Error(`Plugin ${pluginId} is not active (status: ${plugin.status})`);
    }

    const executionContext = this.createExecutionContext(plugin, context);
    const startTime = Date.now();
    let memoryBefore = 0;

    try {
      // Check concurrent execution limits
      if (this.executingCount >= this.maxConcurrentExecutions) {
        return new Promise((resolve, reject) => {
          this.executionQueue.push({ pluginId, context: executionContext, resolve, reject });
        });
      }

      this.executingCount++;
      memoryBefore = this.getCurrentMemoryUsage();

      // Execute plugin
      const result = await this.executeInSandbox(pluginId, async () => {
        return await plugin.api.execute(input, executionContext);
      }, plugin.sandbox);

      const executionTime = Date.now() - startTime;
      const memoryUsed = this.getCurrentMemoryUsage() - memoryBefore;

      // Update plugin statistics
      this.updatePluginStatistics(plugin, executionTime, true);

      const executionResult: PluginExecutionResult = {
        success: true,
        data: result,
        metadata: {
          executionTime,
          memoryUsed,
          warnings: [],
          capabilities: plugin.api.getCapabilities()
        }
      };

      this.logPluginEvent('EXECUTED', pluginId, { 
        executionTime,
        memoryUsed,
        success: true 
      });

      return executionResult;

    } catch (error) {
      const executionTime = Date.now() - startTime;
      const memoryUsed = this.getCurrentMemoryUsage() - memoryBefore;

      // Update plugin statistics
      this.updatePluginStatistics(plugin, executionTime, false);

      const executionResult: PluginExecutionResult = {
        success: false,
        error: {
          code: 'EXECUTION_ERROR',
          message: (error as Error).message,
          details: error
        },
        metadata: {
          executionTime,
          memoryUsed,
          warnings: [],
          capabilities: plugin.api.getCapabilities()
        }
      };

      this.logPluginEvent('EXECUTION_ERROR', pluginId, { 
        error: (error as Error).message,
        executionTime,
        memoryUsed 
      });

      return executionResult;

    } finally {
      this.executingCount--;
      this.processExecutionQueue();
    }
  }

  /**
   * Discover plugins by capability
   */
  async discoverPlugins(
    capabilities: PluginCapability[],
    filters?: {
      securityLevel?: SecurityLevel[];
      environment?: PluginEnvironment[];
      keywords?: string[];
    }
  ): Promise<PluginDiscoveryResult> {
    const availablePlugins: PluginMetadata[] = [];
    const compatiblePlugins: PluginMetadata[] = [];

    // Find plugins with matching capabilities
    for (const capability of capabilities) {
      const pluginIds = this.capabilityIndex.get(capability) || new Set();
      
      for (const pluginId of pluginIds) {
        const plugin = this.plugins.get(pluginId);
        if (!plugin) continue;

        const metadata = plugin.metadata;
        
        // Apply filters using helper method
        if (!this.isPluginMatchingFilters(metadata, filters)) {
          continue;
        }

        availablePlugins.push(metadata);
        
        // Check if plugin supports all required capabilities
        if (this.doesPluginSupportAllCapabilities(metadata, capabilities)) {
          compatiblePlugins.push(metadata);
        }
      }
    }

    // Generate recommendations
    const recommendations = this.generatePluginRecommendations(capabilities, availablePlugins);

    // Check for conflicts
    const conflicts = await this.checkMultiplePluginConflicts(compatiblePlugins.map(p => p.id));

    return {
      availablePlugins: Array.from(new Set(availablePlugins)),
      compatiblePlugins: Array.from(new Set(compatiblePlugins)),
      recommendations,
      conflicts
    };
  }

  /**
   * Get plugin information
   */
  getPlugin(pluginId: string): PluginRegistration | undefined {
    return this.plugins.get(pluginId);
  }

  /**
   * List all registered plugins
   */
  listPlugins(filters?: {
    status?: PluginStatus[];
    capabilities?: PluginCapability[];
    securityLevel?: SecurityLevel[];
  }): PluginRegistration[] {
    const plugins = Array.from(this.plugins.values());
    
    if (!filters) return plugins;

    return plugins.filter(plugin => {
      if (filters.status && !filters.status.includes(plugin.status)) {
        return false;
      }
      
      if (filters.capabilities) {
        const hasMatchingCapability = filters.capabilities.some(cap => 
          plugin.metadata.capabilities.includes(cap)
        );
        if (!hasMatchingCapability) return false;
      }
      
      if (filters.securityLevel && !filters.securityLevel.includes(plugin.metadata.securityLevel)) {
        return false;
      }
      
      return true;
    });
  }

  /**
   * Get plugin performance metrics
   */
  getPluginMetrics(pluginId: string): PluginRegistration['performanceMetrics'] | undefined {
    const plugin = this.plugins.get(pluginId);
    return plugin?.performanceMetrics;
  }

  /**
   * Health check for all plugins
   */
  async performHealthCheck(): Promise<Record<string, { status: 'healthy' | 'unhealthy'; message?: string; error?: string }>> {
    const results: Record<string, any> = {};

    const healthCheckPromises = Array.from(this.plugins.entries()).map(async ([pluginId, plugin]) => {
      if (plugin.status !== 'ACTIVE' || !plugin.api.healthCheck) {
        results[pluginId] = { 
          status: 'unhealthy', 
          message: `Plugin ${pluginId} is not active or does not support health checks` 
        };
        return;
      }

      try {
        const result = await this.executeInSandbox(pluginId, async () => {
          return await plugin.api.healthCheck!();
        }, plugin.sandbox);
        
        results[pluginId] = result;
      } catch (error) {
        results[pluginId] = { 
          status: 'unhealthy', 
          error: (error as Error).message 
        };
      }
    });

    await Promise.allSettled(healthCheckPromises);
    return results;
  }

  /**
   * Get plugin registry statistics
   */
  getRegistryStatistics(): {
    totalPlugins: number;
    activePlugins: number;
    totalExecutions: number;
    averageExecutionTime: number;
    successRate: number;
    capabilityDistribution: Record<PluginCapability, number>;
    securityLevelDistribution: Record<SecurityLevel, number>;
    environmentDistribution: Record<PluginEnvironment, number>;
    } {
    const plugins = Array.from(this.plugins.values());
    const activePlugins = plugins.filter(p => p.status === 'ACTIVE');
    
    const totalExecutions = plugins.reduce((sum, p) => sum + p.performanceMetrics.totalExecutions, 0);
    const totalExecutionTime = plugins.reduce((sum, p) => 
      sum + (p.performanceMetrics.averageExecutionTime * p.performanceMetrics.totalExecutions), 0
    );
    const successfulExecutions = plugins.reduce((sum, p) => 
      sum + (p.performanceMetrics.totalExecutions * p.performanceMetrics.successRate), 0
    );

    // Distribution calculations
    const capabilityDistribution: Record<PluginCapability, number> = {} as any;
    const securityLevelDistribution: Record<SecurityLevel, number> = {} as any;
    const environmentDistribution: Record<PluginEnvironment, number> = {} as any;

    plugins.forEach(plugin => {
      plugin.metadata.capabilities.forEach(cap => {
        capabilityDistribution[cap] = (capabilityDistribution[cap] || 0) + 1;
      });
      
      securityLevelDistribution[plugin.metadata.securityLevel] = 
        (securityLevelDistribution[plugin.metadata.securityLevel] || 0) + 1;
      
      environmentDistribution[plugin.metadata.environment] = 
        (environmentDistribution[plugin.metadata.environment] || 0) + 1;
    });

    return {
      totalPlugins: plugins.length,
      activePlugins: activePlugins.length,
      totalExecutions,
      averageExecutionTime: totalExecutions > 0 ? totalExecutionTime / totalExecutions : 0,
      successRate: totalExecutions > 0 ? successfulExecutions / totalExecutions : 0,
      capabilityDistribution,
      securityLevelDistribution,
      environmentDistribution
    };
  }

  /**
   * Private helper methods
   */

  private validatePluginMetadata(metadata: PluginMetadata): void {
    if (!metadata.id || !metadata.name || !metadata.version) {
      throw new Error('Plugin metadata must include id, name, and version');
    }

    if (this.plugins.has(metadata.id)) {
      throw new Error(`Plugin ${metadata.id} is already registered`);
    }

    if (!metadata.capabilities || metadata.capabilities.length === 0) {
      throw new Error('Plugin must declare at least one capability');
    }
  }

  private isPluginMatchingFilters(
    metadata: PluginMetadata, 
    filters?: {
      securityLevel?: SecurityLevel[];
      environment?: PluginEnvironment[];
      keywords?: string[];
    }
  ): boolean {
    if (!filters) return true;

    if (filters.securityLevel && !filters.securityLevel.includes(metadata.securityLevel)) {
      return false;
    }
    
    if (filters.environment && !filters.environment.includes(metadata.environment)) {
      return false;
    }
    
    if (filters.keywords) {
      const hasMatchingKeyword = filters.keywords.some(keyword => 
        metadata.keywords.includes(keyword) || 
        metadata.name.toLowerCase().includes(keyword.toLowerCase()) ||
        metadata.description.toLowerCase().includes(keyword.toLowerCase())
      );
      if (!hasMatchingKeyword) return false;
    }

    return true;
  }

  private doesPluginSupportAllCapabilities(metadata: PluginMetadata, capabilities: PluginCapability[]): boolean {
    return capabilities.every(cap => metadata.capabilities.includes(cap));
  }

  private async checkPluginConflicts(
    metadata: PluginMetadata,
    dependencies: PluginDependency[]
  ): Promise<Array<{ pluginId: string; conflictType: PluginConflictType; description: string }>> {
    const conflicts: Array<{ pluginId: string; conflictType: PluginConflictType; description: string }> = [];

    // Check dependency conflicts
    for (const dep of dependencies) {
      const depPlugin = this.plugins.get(dep.pluginId);
      if (!depPlugin && !dep.optional) {
        conflicts.push({
          pluginId: dep.pluginId,
          conflictType: 'DEPENDENCY',
          description: `Required dependency ${dep.pluginId} not found`
        });
      }
      
      if (depPlugin && !this.isVersionCompatible(depPlugin.metadata.version, dep.version)) {
        conflicts.push({
          pluginId: dep.pluginId,
          conflictType: 'DEPENDENCY',
          description: `Version conflict: required ${dep.version}, found ${depPlugin.metadata.version}`
        });
      }
    }

    // Check capability conflicts (e.g., two plugins can't both handle system commands)
    const exclusiveCapabilities: PluginCapability[] = ['SYSTEM_COMMANDS'];
    for (const capability of metadata.capabilities) {
      if (exclusiveCapabilities.includes(capability)) {
        const existingPlugins = this.capabilityIndex.get(capability) || new Set();
        if (existingPlugins.size > 0) {
          conflicts.push({
            pluginId: Array.from(existingPlugins)[0],
            conflictType: 'CAPABILITY',
            description: `Exclusive capability ${capability} already claimed by another plugin`
          });
        }
      }
    }

    return conflicts;
  }

  private async checkMultiplePluginConflicts(pluginIds: string[]): Promise<Array<{ pluginId: string; conflictType: PluginConflictType; description: string }>> {
    // For now, return empty array - could implement complex conflict detection
    return [];
  }

  private async resolveDependencies(pluginId: string, dependencies: PluginDependency[]): Promise<void> {
    for (const dep of dependencies) {
      if (!dep.optional && !this.plugins.has(dep.pluginId)) {
        throw new Error(`Missing required dependency: ${dep.pluginId}`);
      }
    }
  }

  private async createSandbox(metadata: PluginMetadata): Promise<PluginSandbox> {
    const sandboxId = `sandbox_${metadata.id}_${Date.now()}`;
    
    const permissions: PluginExecutionContext['permissions'] = {
      allowNetworkAccess: metadata.capabilities.includes('NETWORK_ACCESS') || metadata.capabilities.includes('EXTERNAL_API'),
      allowFileAccess: metadata.capabilities.includes('FILE_OPERATIONS'),
      allowSystemAccess: metadata.capabilities.includes('SYSTEM_COMMANDS'),
      allowDatabaseAccess: metadata.capabilities.includes('DATABASE_ACCESS'),
      maxExecutionTime: this.getMaxExecutionTime(metadata.securityLevel),
      maxMemoryUsage: this.getMaxMemoryUsage(metadata.securityLevel)
    };

    const sandbox: PluginSandbox = {
      id: sandboxId,
      environment: metadata.environment,
      permissions,
      resourceLimits: {
        maxCpuUsage: this.getMaxCpuUsage(metadata.securityLevel),
        maxMemoryUsage: permissions.maxMemoryUsage,
        maxExecutionTime: permissions.maxExecutionTime,
        maxConcurrentExecutions: 3
      },
      isolatedContext: this.createIsolatedContext(metadata),
      activeExecutions: new Set()
    };

    this.sandboxes.set(sandboxId, sandbox);
    return sandbox;
  }

  private async destroySandbox(sandboxId: string): Promise<void> {
    const sandbox = this.sandboxes.get(sandboxId);
    if (!sandbox) return;

    // Wait for active executions to complete
    while (sandbox.activeExecutions.size > 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    this.sandboxes.delete(sandboxId);
  }

  private async executeInSandbox<T>(
    pluginId: string,
    fn: () => Promise<T>,
    sandbox?: PluginSandbox
  ): Promise<T> {
    if (!sandbox) {
      // Execute in trusted environment
      return await fn();
    }

    const executionId = `exec_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    sandbox.activeExecutions.add(executionId);

    try {
      // Set up execution timeout
      const timeoutPromise = new Promise<never>((_, reject) => {
        setTimeout(() => {
          reject(new Error(`Plugin execution timeout after ${sandbox.resourceLimits.maxExecutionTime}ms`));
        }, sandbox.resourceLimits.maxExecutionTime);
      });

      // Execute with timeout
      const result = await Promise.race([fn(), timeoutPromise]);
      return result;

    } finally {
      sandbox.activeExecutions.delete(executionId);
    }
  }

  private createExecutionContext(
    plugin: PluginRegistration,
    contextOverrides?: Partial<PluginExecutionContext>
  ): PluginExecutionContext {
    const baseContext: PluginExecutionContext = {
      requestId: `req_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
      timestamp: new Date(),
      environment: plugin.metadata.environment,
      permissions: plugin.sandbox?.permissions || {
        allowNetworkAccess: true,
        allowFileAccess: true,
        allowSystemAccess: true,
        allowDatabaseAccess: true,
        maxExecutionTime: this.defaultTimeout,
        maxMemoryUsage: 1024 * 1024 * 100 // 100MB
      },
      logger: {
        debug: (message, metadata) => this.logPluginEvent('DEBUG', plugin.metadata.id, { message, metadata }),
        info: (message, metadata) => this.logPluginEvent('INFO', plugin.metadata.id, { message, metadata }),
        warn: (message, metadata) => this.logPluginEvent('WARN', plugin.metadata.id, { message, metadata }),
        error: (message, error, metadata) => this.logPluginEvent('ERROR', plugin.metadata.id, { message, error, metadata })
      },
      metrics: {
        counter: (name, value?, labels?) => this.recordPluginMetric('counter', plugin.metadata.id, name, value ?? 1, labels),
        gauge: (name, value, labels?) => this.recordPluginMetric('gauge', plugin.metadata.id, name, value, labels),
        timer: (name, value, labels?) => this.recordPluginMetric('timer', plugin.metadata.id, name, value, labels)
      }
    };

    return { ...baseContext, ...contextOverrides };
  }

  private validateConfiguration(config: Record<string, any>, schema: PluginConfigSchema): void {
    this.validateRequiredProperties(config, schema);
    this.validatePropertyTypes(config, schema);
  }

  private validateRequiredProperties(config: Record<string, any>, schema: PluginConfigSchema): void {
    for (const required of schema.required) {
      if (!(required in config)) {
        throw new Error(`Required configuration property '${required}' is missing`);
      }
    }
  }

  private validatePropertyTypes(config: Record<string, any>, schema: PluginConfigSchema): void {
    for (const [key, value] of Object.entries(config)) {
      const propSchema = schema.properties[key];
      if (!propSchema) continue;

      this.validatePropertyType(key, value, propSchema);
      this.validatePropertyConstraints(key, value, propSchema);
      this.validatePropertyEnum(key, value, propSchema);
    }
  }

  private validatePropertyType(key: string, value: any, propSchema: any): void {
    const actualType = Array.isArray(value) ? 'array' : typeof value;
    if (actualType !== propSchema.type) {
      throw new Error(`Configuration property '${key}' must be of type ${propSchema.type}, got ${actualType}`);
    }
  }

  private validatePropertyConstraints(key: string, value: any, propSchema: any): void {
    if (!propSchema.validation) return;

    const validation = propSchema.validation;
    
    if (typeof value === 'number') {
      this.validateNumberConstraints(key, value, validation);
    }
    
    if (typeof value === 'string') {
      this.validateStringConstraints(key, value, validation);
    }
  }

  private validateNumberConstraints(key: string, value: number, validation: any): void {
    if (validation.min !== undefined && value < validation.min) {
      throw new Error(`Configuration property '${key}' must be >= ${validation.min}`);
    }
    if (validation.max !== undefined && value > validation.max) {
      throw new Error(`Configuration property '${key}' must be <= ${validation.max}`);
    }
  }

  private validateStringConstraints(key: string, value: string, validation: any): void {
    if (validation.pattern && !new RegExp(validation.pattern).test(value)) {
      throw new Error(`Configuration property '${key}' does not match required pattern`);
    }
  }

  private validatePropertyEnum(key: string, value: any, propSchema: any): void {
    if (propSchema.enum && !propSchema.enum.includes(value)) {
      throw new Error(`Configuration property '${key}' must be one of: ${propSchema.enum.join(', ')}`);
    }
  }

  private updateCapabilityIndex(metadata: PluginMetadata): void {
    for (const capability of metadata.capabilities) {
      const plugins = this.capabilityIndex.get(capability) || new Set();
      plugins.add(metadata.id);
      this.capabilityIndex.set(capability, plugins);
    }
  }

  private removeFromCapabilityIndex(metadata: PluginMetadata): void {
    for (const capability of metadata.capabilities) {
      const plugins = this.capabilityIndex.get(capability);
      if (plugins) {
        plugins.delete(metadata.id);
        if (plugins.size === 0) {
          this.capabilityIndex.delete(capability);
        }
      }
    }
  }

  private updateDependencyGraph(pluginId: string, dependencies: PluginDependency[]): void {
    const deps = new Set(dependencies.map(d => d.pluginId));
    this.dependencyGraph.set(pluginId, deps);
  }

  private findDependentPlugins(pluginId: string): string[] {
    const dependents: string[] = [];
    
    for (const [dependent, dependencies] of this.dependencyGraph.entries()) {
      if (dependencies.has(pluginId)) {
        dependents.push(dependent);
      }
    }
    
    return dependents;
  }

  private generatePluginRecommendations(
    capabilities: PluginCapability[],
    availablePlugins: PluginMetadata[]
  ): Array<{ plugin: PluginMetadata; reason: string; confidence: number }> {
    const recommendations: Array<{ plugin: PluginMetadata; reason: string; confidence: number }> = [];

    for (const plugin of availablePlugins) {
      let confidence = 0;
      const reasons: string[] = [];

      // Capability matching
      const matchingCapabilities = capabilities.filter(cap => plugin.capabilities.includes(cap));
      const capabilityScore = matchingCapabilities.length / capabilities.length;
      confidence += capabilityScore * 0.6;
      
      if (matchingCapabilities.length > 0) {
        reasons.push(`Supports ${matchingCapabilities.length}/${capabilities.length} required capabilities`);
      }

      // Usage-based scoring
      const pluginRegistration = this.plugins.get(plugin.id);
      if (pluginRegistration) {
        const usageScore = Math.min(pluginRegistration.usageCount / 100, 1) * 0.2;
        confidence += usageScore;
        
        if (pluginRegistration.performanceMetrics.successRate > 0.9) {
          confidence += 0.1;
          reasons.push('High success rate');
        }
        
        if (pluginRegistration.performanceMetrics.averageExecutionTime < 1000) {
          confidence += 0.1;
          reasons.push('Fast execution');
        }
      }

      if (confidence > 0.3) {
        recommendations.push({
          plugin,
          reason: reasons.join(', '),
          confidence: Math.min(confidence, 1)
        });
      }
    }

    const sortedRecommendations = [...recommendations].sort((a, b) => b.confidence - a.confidence);
    return sortedRecommendations.slice(0, 10);
  }

  private updatePluginStatistics(plugin: PluginRegistration, executionTime: number, success: boolean): void {
    plugin.usageCount++;
    plugin.lastUsed = new Date();
    
    if (!success) {
      plugin.errorCount++;
    }

    const metrics = plugin.performanceMetrics;
    const totalTime = metrics.averageExecutionTime * metrics.totalExecutions + executionTime;
    metrics.totalExecutions++;
    metrics.averageExecutionTime = totalTime / metrics.totalExecutions;
    
    const successfulExecutions = metrics.totalExecutions * metrics.successRate;
    const newSuccessfulExecutions = success ? successfulExecutions + 1 : successfulExecutions;
    metrics.successRate = newSuccessfulExecutions / metrics.totalExecutions;
  }

  private processExecutionQueue(): void {
    if (this.executionQueue.length === 0 || this.executingCount >= this.maxConcurrentExecutions) {
      return;
    }

    const next = this.executionQueue.shift();
    if (next) {
      this.executePlugin(next.pluginId, {}, next.context)
        .then(next.resolve)
        .catch(next.reject);
    }
  }

  private initializeCapabilityIndex(): void {
    const capabilities: PluginCapability[] = [
      'DATA_PROCESSING', 'EXTERNAL_API', 'FILE_OPERATIONS', 'NETWORK_ACCESS',
      'DATABASE_ACCESS', 'SYSTEM_COMMANDS', 'AI_MODELS', 'CUSTOM_REASONING',
      'USER_INTERFACE', 'WORKFLOW_AUTOMATION'
    ];

    capabilities.forEach(capability => {
      this.capabilityIndex.set(capability, new Set());
    });
  }

  private startSandboxCleanup(): void {
    this.cleanupTimer = setInterval(() => {
      // Clean up inactive sandboxes
      const now = Date.now();
      for (const [sandboxId, sandbox] of this.sandboxes.entries()) {
        if (sandbox.activeExecutions.size === 0) {
          // Check if sandbox hasn't been used recently
          const plugin = Array.from(this.plugins.values()).find(p => p.sandbox?.id === sandboxId);
          if (plugin?.lastUsed && now - plugin.lastUsed.getTime() > this.sandboxCleanupInterval) {
            this.destroySandbox(sandboxId);
          }
        }
      }
    }, this.sandboxCleanupInterval);
  }

  private getCurrentMemoryUsage(): number {
    return process.memoryUsage().heapUsed;
  }

  private getMaxExecutionTime(securityLevel: SecurityLevel): number {
    const timeouts = {
      PUBLIC: 10000,    // 10 seconds
      RESTRICTED: 30000, // 30 seconds
      PRIVATE: 60000,   // 1 minute
      SYSTEM: 300000    // 5 minutes
    };
    return timeouts[securityLevel] || this.defaultTimeout;
  }

  private getMaxMemoryUsage(securityLevel: SecurityLevel): number {
    const limits = {
      PUBLIC: 50 * 1024 * 1024,    // 50MB
      RESTRICTED: 100 * 1024 * 1024, // 100MB
      PRIVATE: 200 * 1024 * 1024,   // 200MB
      SYSTEM: 500 * 1024 * 1024     // 500MB
    };
    return limits[securityLevel] || 100 * 1024 * 1024;
  }

  private getMaxCpuUsage(securityLevel: SecurityLevel): number {
    const limits = {
      PUBLIC: 50,    // 50%
      RESTRICTED: 70, // 70%
      PRIVATE: 80,   // 80%
      SYSTEM: 90     // 90%
    };
    return limits[securityLevel] || 70;
  }

  private createIsolatedContext(metadata: PluginMetadata): any {
    // Create isolated execution context based on environment
    // This would be more sophisticated in a real implementation
    return {
      pluginId: metadata.id,
      environment: metadata.environment,
      capabilities: metadata.capabilities
    };
  }

  private isVersionCompatible(actualVersion: string, requiredVersion: string): boolean {
    // Simplified version matching - in production, use semver library
    return actualVersion === requiredVersion || requiredVersion === '*';
  }

  private logPluginEvent(event: string, pluginId: string, metadata?: any): void {
    console.log(`[PluginRegistry] ${event}: ${pluginId}`, metadata);
  }

  private recordPluginMetric(type: string, pluginId: string, name: string, value: number, labels?: Record<string, string>): void {
    // In a real implementation, this would integrate with the observability system
    console.debug(`[PluginMetric] ${type}: ${pluginId}.${name} = ${value}`, labels);
  }

  /**
   * Cleanup resources
   */
  destroy(): void {
    if (this.cleanupTimer) {
      clearInterval(this.cleanupTimer);
      this.cleanupTimer = undefined;
    }

    // Cleanup all plugins
    const pluginIds = Array.from(this.plugins.keys());
    Promise.allSettled(pluginIds.map(id => this.unregisterPlugin(id)));
  }
}
