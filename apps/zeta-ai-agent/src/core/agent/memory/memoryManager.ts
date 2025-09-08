import {
import Add from "Add";
import Analyze from "Analyze";
import Check from "Check";
import Consider from "Consider";
import ContextWindow from "ContextWindow";
import File from "File";
import If from "If";
import Keep from "Keep";
import Last from "Last";
import Map from "Map";
import Math from "Math";
import MemoryManager from "./MemoryManager";
import Record from "Record";
import Remove from "Remove";
import Review from "Review";
import Simple from "Simple";
import Sort from "Sort";
import Top from "Top";
import Track from "Track";
import Update from "Update";
  AgentInteraction,
  RelevantContext,
  ContextItem,
  AgentAction
} from '../../../types/shared';

export class MemoryManager {
  private contextWindow: ContextWindow;
  private longTermMemory: Map<string, any>;
  private recentActions: AgentAction[] = [];
  private maxRecentActions = 50;
  private interactionHistory: AgentInteraction[] = [];
  private maxInteractions = 1000;

  constructor(maxContextSize = 1000) {
    this.contextWindow = new ContextWindow(maxContextSize);
    this.longTermMemory = new Map();
  }

  async getRelevantContext(query: string): Promise<RelevantContext> {
    const contextItems = this.contextWindow.getAll();
    const recentActions = this.recentActions.slice(-10); // Last 10 actions

    // Simple relevance scoring based on keyword matching
    const relevantItems = contextItems.filter(item =>
      this.calculateRelevance(query, item.content) > 0.3
    );

    // Sort by relevance and timestamp
    relevantItems.sort((a, b) => {
      const relevanceA = this.calculateRelevance(query, a.content);
      const relevanceB = this.calculateRelevance(query, b.content);
      
      if (Math.abs(relevanceA - relevanceB) < 0.1) {
        // If relevance is similar, prefer more recent items
        return b.timestamp.getTime() - a.timestamp.getTime();
      }
      
      return relevanceB - relevanceA;
    });

    return {
      items: relevantItems.slice(0, 10), // Top 10 most relevant
      recent_actions: recentActions,
      query: query,
      relevance_score: relevantItems.length > 0 ? 
        relevantItems[0].relevance || 0 : 0,
      suggestions: this.generateContextualSuggestions(relevantItems, query)
    };
  }

  async updateMemory(interaction: AgentInteraction): Promise<void> {
    // Add to context window
    this.contextWindow.add({
      content: interaction.user_input + ' ' + interaction.agent_response,
      timestamp: new Date(),
      type: 'interaction',
      metadata: {
        success: interaction.success,
        feedback: interaction.feedback,
        context: interaction.context
      }
    });

    // Add to interaction history
    this.interactionHistory.push(interaction);
    if (this.interactionHistory.length > this.maxInteractions) {
      this.interactionHistory = this.interactionHistory.slice(-this.maxInteractions);
    }

    // Add action to recent actions
    const actionType = this.mapInteractionTypeToActionType(interaction.type);
    const action: AgentAction = {
      type: actionType,
      target: interaction.target,
      timestamp: new Date(),
      result: interaction.result,
      success: interaction.success
    };

    this.recentActions.push(action);

    // Keep only recent actions
    if (this.recentActions.length > this.maxRecentActions) {
      this.recentActions = this.recentActions.slice(-this.maxRecentActions);
    }

    // Update long-term memory patterns
    await this.updateLongTermMemory(interaction);
  }

  async storeCodeContext(filePath: string, code: string, analysis?: any): Promise<void> {
    this.contextWindow.add({
      content: `File: ${filePath}\n${code}`,
      timestamp: new Date(),
      type: 'code',
      metadata: {
        filePath,
        analysis,
        language: this.extractLanguageFromPath(filePath)
      }
    });
  }

  async getCodeHistory(filePath?: string): Promise<ContextItem[]> {
    const codeItems = this.contextWindow.getByType('code');
    
    if (filePath) {
      return codeItems.filter(item => 
        item.metadata?.filePath === filePath
      );
    }
    
    return codeItems;
  }

  async getInteractionHistory(limit = 50): Promise<AgentInteraction[]> {
    return this.interactionHistory.slice(-limit);
  }

  async getSuccessfulPatterns(actionType?: string): Promise<AgentInteraction[]> {
    let interactions = this.interactionHistory.filter(i => i.success);
    
    if (actionType) {
      interactions = interactions.filter(i => i.type === actionType);
    }
    
    // Sort by feedback if available, then by recency
    return interactions.sort((a, b) => {
      if (a.feedback && b.feedback) {
        return b.feedback - a.feedback;
      }
      return b.timestamp.getTime() - a.timestamp.getTime();
    });
  }

  async clearMemory(): Promise<void> {
    this.contextWindow.clear();
    this.recentActions = [];
    this.interactionHistory = [];
    this.longTermMemory.clear();
  }

  async exportMemory(): Promise<any> {
    return {
      contextWindow: this.contextWindow.export(),
      recentActions: this.recentActions,
      interactionHistory: this.interactionHistory,
      longTermMemory: Object.fromEntries(this.longTermMemory),
      timestamp: new Date().toISOString()
    };
  }

  async importMemory(data: any): Promise<void> {
    if (data.contextWindow) {
      this.contextWindow.import(data.contextWindow);
    }
    
    if (data.recentActions) {
      this.recentActions = data.recentActions.map((action: any) => ({
        ...action,
        timestamp: new Date(action.timestamp)
      }));
    }
    
    if (data.interactionHistory) {
      this.interactionHistory = data.interactionHistory.map((interaction: any) => ({
        ...interaction,
        timestamp: new Date(interaction.timestamp)
      }));
    }
    
    if (data.longTermMemory) {
      this.longTermMemory = new Map(Object.entries(data.longTermMemory));
    }
  }

  private calculateRelevance(query: string, content: string): number {
    const queryWords = query.toLowerCase().split(/\s+/);
    const contentWords = content.toLowerCase().split(/\s+/);
    
    let matches = 0;
    for (const queryWord of queryWords) {
      if (contentWords.some(contentWord => 
        contentWord.includes(queryWord) || queryWord.includes(contentWord)
      )) {
        matches++;
      }
    }
    
    return matches / queryWords.length;
  }

  private generateContextualSuggestions(items: ContextItem[], query: string): string[] {
    const suggestions: string[] = [];
    
    // Analyze patterns in relevant items
    const codeItems = items.filter(item => item.type === 'code');
    const interactionItems = items.filter(item => item.type === 'interaction');
    
    if (codeItems.length > 0) {
      suggestions.push('Consider reviewing similar code patterns from previous sessions');
    }
    
    if (interactionItems.length > 0) {
      suggestions.push('Check previous solutions for similar problems');
    }
    
    // Add query-specific suggestions
    if (query.toLowerCase().includes('error') || query.toLowerCase().includes('debug')) {
      suggestions.push('Review error patterns and debugging approaches');
    }
    
    if (query.toLowerCase().includes('optimize') || query.toLowerCase().includes('performance')) {
      suggestions.push('Consider performance optimization techniques used before');
    }
    
    return suggestions;
  }

  private async updateLongTermMemory(interaction: AgentInteraction): Promise<void> {
    // Track success patterns by language
    const language = interaction.context.language;
    if (language && interaction.success) {
      const langKey = `success_patterns_${language}`;
      const patterns = this.longTermMemory.get(langKey) || [];
      patterns.push({
        type: interaction.type,
        timestamp: interaction.timestamp,
        feedback: interaction.feedback
      });
      
      // Keep only recent successful patterns
      if (patterns.length > 100) {
        patterns.splice(0, patterns.length - 100);
      }
      
      this.longTermMemory.set(langKey, patterns);
    }
    
    // Track common error patterns
    if (!interaction.success) {
      const errorKey = 'error_patterns';
      const errors = this.longTermMemory.get(errorKey) || [];
      errors.push({
        type: interaction.type,
        context: interaction.context,
        timestamp: interaction.timestamp
      });
      
      if (errors.length > 50) {
        errors.splice(0, errors.length - 50);
      }
      
      this.longTermMemory.set(errorKey, errors);
    }
  }

  private extractLanguageFromPath(filePath: string): string {
    const extension = filePath.split('.').pop()?.toLowerCase();
    const languageMap: Record<string, string> = {
      'ts': 'typescript',
      'js': 'javascript',
      'py': 'python',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'cs': 'csharp',
      'php': 'php',
      'rb': 'ruby',
      'go': 'go',
      'rs': 'rust'
    };
    
    return languageMap[extension || ''] || 'unknown';
  }

  private mapInteractionTypeToActionType(interactionType: string): 'code_review' | 'debug' | 'chat' | 'optimize' | 'generate' | 'refactor' {
    const mapping: Record<string, 'code_review' | 'debug' | 'chat' | 'optimize' | 'generate' | 'refactor'> = {
      'code_review': 'code_review',
      'debug': 'debug',
      'optimization': 'optimize',
      'chat': 'chat',
      'completion': 'generate'
    };
    
    return mapping[interactionType] || 'chat';
  }
}

class ContextWindow {
  private items: ContextItem[] = [];
  private maxSize: number;

  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }

  add(item: ContextItem): void {
    this.items.push(item);
    
    if (this.items.length > this.maxSize) {
      this.items.shift(); // Remove oldest item
    }
  }

  getAll(): ContextItem[] {
    return [...this.items];
  }

  getByType(type: string): ContextItem[] {
    return this.items.filter(item => item.type === type);
  }

  getRecent(count: number): ContextItem[] {
    return this.items.slice(-count);
  }

  clear(): void {
    this.items = [];
  }

  export(): any {
    return {
      items: this.items,
      maxSize: this.maxSize
    };
  }

  import(data: any): void {
    if (data.items) {
      this.items = data.items.map((item: any) => ({
        ...item,
        timestamp: new Date(item.timestamp)
      }));
    }
    if (data.maxSize) {
      this.maxSize = data.maxSize;
    }
  }

  size(): number {
    return this.items.length;
  }
}
