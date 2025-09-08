/**
 * Autonomous AI Facade
 * Consistent, typed entrypoint to the integrated autonomous AI system.
 *
 * Exposes a small surface that matches project conventions:
 * - Typed options with sensible defaults
 * - Singleton lifecycle helpers (get/init/reset)
 * - Thin delegation to IntegratedAutonomousAI
 * - Re-export of key types for cohesion
 */

import {
import AI from "AI";
import Autonomous from "Autonomous";
import AutonomousAIOptions from "AutonomousAIOptions";
import AutonomousAIService from "AutonomousAIService";
import AutonomousResult from "AutonomousResult";
import AutonomousTask from "AutonomousTask";
import Capabilities from "Capabilities";
import Consistent from "Consistent";
import Default from "Default";
import Exposes from "Exposes";
import Facade from "Facade";
import Get from "Get";
import Initialize from "Initialize";
import IntegratedAIConfig from "IntegratedAIConfig";
import Lifecycle from "Lifecycle";
import Map from "Map";
import Normalize from "Normalize";
import OLLAMA_BASE_URL from "OLLAMA_BASE_URL";
import OLLAMA_DEFAULT_MODEL from "OLLAMA_DEFAULT_MODEL";
import Ollama from "Ollama";
import Options from "Options";
import Partial from "Partial";
import Prefer from "Prefer";
import Re from "Re";
import Record from "Record";
import Shutdown from "Shutdown";
import Simple from "Simple";
import Singleton from "Singleton";
import Thin from "Thin";
import Typed from "Typed";
import URL from "URL";
      IntegratedAutonomousAI,
      createAutonomousAI,
      type AutonomousResult,
      type AutonomousTask,
      type IntegratedAIConfig,
} from './integratedAI';

/**
 * Options for creating/initializing an Autonomous AI instance
 */
export interface AutonomousAIOptions {
	baseUrl?: string; // Ollama base URL
	defaultModel?: string; // Default model to use
	features?: Partial<IntegratedAIConfig['features']>;
	performance?: Partial<IntegratedAIConfig['performance']>;
}

/**
 * Normalize options into the full IntegratedAIConfig
 */
function toConfig(opts: AutonomousAIOptions = {}): IntegratedAIConfig {
	const baseUrl =
		opts.baseUrl || process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
	const defaultModel =
		opts.defaultModel || process.env.OLLAMA_DEFAULT_MODEL || 'deepseek-coder';

	const defaultFeatures: IntegratedAIConfig['features'] = {
		reasoning: true,
		planning: true,
		memory: true,
		optimization: true,
		safety: true,
		learning: true,
		observability: true,
		plugins: true,
		explainability: true,
		humanFeedback: true,
	};

	const defaultPerf: IntegratedAIConfig['performance'] = {
		maxConcurrentTasks: 5,
		taskTimeout: 60_000,
		memoryLimit: 10_000,
	};

	return {
		ollama: { baseUrl, defaultModel },
		features: { ...defaultFeatures, ...(opts.features || {}) },
		performance: { ...defaultPerf, ...(opts.performance || {}) },
	};
}

/**
 * Thin service wrapper around IntegratedAutonomousAI
 */
export class AutonomousAIService {
	private readonly core: IntegratedAutonomousAI;

	constructor(arg: IntegratedAIConfig | IntegratedAutonomousAI) {
		this.core = arg instanceof IntegratedAutonomousAI ? arg : new IntegratedAutonomousAI(arg);
	}

	// Lifecycle
	async initialize(): Promise<void> {
		await this.core.initialize();
	}

	async shutdown(): Promise<void> {
		await this.core.shutdown();
	}

	// Capabilities (delegation)
	async reason(question: string): Promise<AutonomousResult> {
		return this.core.reason(question);
	}

	async plan(goal: string): Promise<AutonomousResult> {
		return this.core.plan(goal);
	}

	async analyze(data: unknown): Promise<AutonomousResult> {
		return this.core.analyze(data as any);
	}

	async optimize(parameters: unknown): Promise<AutonomousResult> {
		return this.core.optimize(parameters as any);
	}

	async learn(experience: unknown): Promise<AutonomousResult> {
		return this.core.learn(experience as any);
	}

	async explain(subject: unknown): Promise<AutonomousResult> {
		return this.core.explain(subject as any);
	}

	getSystemStatus(): Record<string, any> {
		return this.core.getSystemStatus();
	}

	getCore(): IntegratedAutonomousAI {
		return this.core;
	}
}

/**
 * Simple registry for named autonomous AI instances
 */
const instances = new Map<string, AutonomousAIService>();

/**
 * Get existing or create a new named Autonomous AI instance
 */
export function getAutonomousAI(
	name = 'default',
	options?: AutonomousAIOptions
): AutonomousAIService {
	const existing = instances.get(name);
	if (existing) return existing;

	// Prefer factory to keep parity with integratedAI.ts
	if (!options) {
	const ai = createAutonomousAI({
			baseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
			defaultModel: process.env.OLLAMA_DEFAULT_MODEL || 'deepseek-coder',
		});
	const service = new AutonomousAIService(ai);
		instances.set(name, service);
		return service;
	}

	const config = toConfig(options);
	const service = new AutonomousAIService(config);
	instances.set(name, service);
	return service;
}

/** Initialize and return a ready-to-use instance */
export async function initAutonomousAI(
	options?: AutonomousAIOptions,
	name = 'default'
): Promise<AutonomousAIService> {
	const svc = getAutonomousAI(name, options);
	await svc.initialize();
	return svc;
}

/** Shutdown and remove a named instance */
export async function resetAutonomousAI(name = 'default'): Promise<void> {
	const svc = instances.get(name);
	if (svc) {
		await svc.shutdown();
		instances.delete(name);
	}
}

// Re-exports for convenience and consistency
export type { AutonomousResult, AutonomousTask, IntegratedAIConfig };

