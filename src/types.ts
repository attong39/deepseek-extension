/**
 * Type definitions for the DeepSeek AI Agent
 */

export interface IOllamaClient {
    chat(messages: OllamaMessage[], stream?: boolean): Promise<string>;
    isAvailable(): Promise<boolean>;
}

export interface OllamaMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}

export interface OllamaConfig {
    baseUrl: string;
    model: string;
    timeout: number;
    temperature?: number;
}

export interface AgentAction {
    type: 'upsert_file' | 'append' | 'replace' | 'insert' | 'optimize_imports';
    path: string;
    content?: string;
    pattern?: string;
    flags?: string;
    anchor?: string;
    position?: 'above' | 'below';
}

export interface AgentPlan {
    summary: string;
    rationale: string;
    actions: AgentAction[];
}

export interface IAIAgent {
    runTask(goal: string, uris?: string[]): Promise<AgentPlan>;
    reviewActiveFile(): Promise<AgentPlan>;
    continuous(maxIterations?: number): Promise<void>;
}

export interface ConfigOptions {
    ollamaUrl: string;
    ollamaModel: string;
    ollamaTimeout: number;
    autoApply: boolean;
    maxContextBytes: number;
    promptTemplateFolder: string;
}

export interface ContextFile {
    path: string;
    content: string;
    relativePath: string;
}