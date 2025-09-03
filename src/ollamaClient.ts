import { IOllamaClient, OllamaMessage, OllamaConfig } from './types';
import { Config } from './config';

/**
 * Ollama client for communicating with the local Ollama service
 */
export class OllamaClient implements IOllamaClient {
    private config: Config;
    
    constructor() {
        this.config = Config.getInstance();
    }
    
    /**
     * Check if Ollama service is available
     */
    async isAvailable(): Promise<boolean> {
        try {
            const response = await fetch(`${this.config.getOllamaUrl()}/api/tags`, {
                method: 'GET',
                signal: AbortSignal.timeout(5000)
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Send chat messages to Ollama and return response
     */
    async chat(messages: OllamaMessage[], stream: boolean = false): Promise<string> {
        const url = `${this.config.getOllamaUrl()}/api/chat`;
        
        const payload = {
            model: this.config.getOllamaModel(),
            messages,
            stream,
            options: {
                temperature: this.config.getTemperature()
            }
        };
        
        try {
            if (stream) {
                return await this.handleStreamingResponse(url, payload);
            } else {
                return await this.handleNonStreamingResponse(url, payload);
            }
        } catch (error) {
            throw new Error(`Ollama request failed: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    
    private async handleNonStreamingResponse(url: string, payload: any): Promise<string> {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            signal: AbortSignal.timeout(this.config.getOllamaTimeout())
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data.message?.content || '';
    }
    
    private async handleStreamingResponse(url: string, payload: any): Promise<string> {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            signal: AbortSignal.timeout(this.config.getOllamaTimeout())
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const reader = response.body?.getReader();
        if (!reader) {
            throw new Error('Response body is not readable');
        }
        
        const decoder = new TextDecoder();
        let result = '';
        
        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done) {break;}
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\n').filter(line => line.trim());
                
                for (const line of lines) {
                    try {
                        const data = JSON.parse(line);
                        if (data.message?.content) {
                            result += data.message.content;
                        }
                    } catch (parseError) {
                        // Skip invalid JSON lines
                        continue;
                    }
                }
            }
        } finally {
            reader.releaseLock();
        }
        
        return result;
    }
    
    /**
     * Filter out think tags from DeepSeek responses
     */
    static filterThinkTags(content: string): string {
        return content.replace(/<think>.*?<\/think>/gs, '').trim();
    }
    
    /**
     * Pull a model if it doesn't exist
     */
    async pullModel(model: string): Promise<void> {
        const url = `${this.config.getOllamaUrl()}/api/pull`;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ model }),
            signal: AbortSignal.timeout(120000) // 2 minute timeout for pulling
        });
        
        if (!response.ok) {
            throw new Error(`Failed to pull model ${model}: ${response.statusText}`);
        }
    }
}