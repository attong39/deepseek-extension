import * as vscode from 'vscode';
import * as dotenv from 'dotenv';
import { ConfigOptions } from './types';

// Load environment variables from .env file if it exists
dotenv.config();

/**
 * Configuration management for the DeepSeek extension
 */
export class Config {
    private static instance: Config;
    
    private constructor() {}
    
    public static getInstance(): Config {
        if (!Config.instance) {
            Config.instance = new Config();
        }
        return Config.instance;
    }
    
    public getOllamaUrl(): string {
        return process.env.OLLAMA_URL ?? 
               vscode.workspace.getConfiguration('deepseek').get('ollamaUrl') ?? 
               'http://127.0.0.1:11434';
    }
    
    public getOllamaModel(): string {
        return process.env.OLLAMA_MODEL ?? 
               vscode.workspace.getConfiguration('deepseek').get('ollamaModel') ?? 
               'deepseek-r1:latest';
    }
    
    public getOllamaTimeout(): number {
        return Number(process.env.OLLAMA_TIMEOUT_MS) || 
               vscode.workspace.getConfiguration('deepseek').get('ollamaTimeout') || 
               15000;
    }
    
    public getAutoApply(): boolean {
        return vscode.workspace.getConfiguration('deepseek').get('autoApply') ?? false;
    }
    
    public getMaxContextBytes(): number {
        return vscode.workspace.getConfiguration('deepseek').get('maxContextBytes') ?? 40000;
    }
    
    public getPromptTemplateFolder(): string {
        return vscode.workspace.getConfiguration('deepseek').get('promptTemplateFolder') ?? 
               '~/.deepseek/templates';
    }
    
    public getTemperature(): number {
        return vscode.workspace.getConfiguration('deepseek').get('temperature') ?? 0;
    }
    
    public getAllConfig(): ConfigOptions {
        return {
            ollamaUrl: this.getOllamaUrl(),
            ollamaModel: this.getOllamaModel(),
            ollamaTimeout: this.getOllamaTimeout(),
            autoApply: this.getAutoApply(),
            maxContextBytes: this.getMaxContextBytes(),
            promptTemplateFolder: this.getPromptTemplateFolder()
        };
    }
}