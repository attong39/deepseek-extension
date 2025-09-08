import { AgentAction } from '../../../types/shared';
import Add from "Add";
import AgentInteraction from "AgentInteraction";
import ContextItem from "ContextItem";
import ContextWindow from "ContextWindow";
import Keep from "Keep";
import Last from "Last";
import Map from "Map";
import MemoryManager from "./MemoryManager";
import RelevantContext from "RelevantContext";
import Remove from "Remove";
import Simple from "Simple";
import Store from "Store";

export class MemoryManager {
  private contextWindow: ContextWindow;
  private longTermMemory: Map<string, any>;
  private recentActions: AgentAction[] = [];
  private maxRecentActions = 50;

  constructor(maxContextSize: number = 1000) {
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

    return {
      items: relevantItems,
      recent_actions: recentActions,
      query: query
    };
  }

  async updateMemory(interaction: AgentInteraction): Promise<void> {
    // Add to context window
    this.contextWindow.add({
      content: interaction.user_input + ' ' + interaction.agent_response,
      timestamp: new Date(),
      type: 'interaction'
    });

    // Add action to recent actions
    const action: AgentAction = {
      type: interaction.action_type,
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

    // Store important learnings in long-term memory
    if (interaction.success && interaction.important) {
      const key = `${interaction.action_type}_${Date.now()}`;
      this.longTermMemory.set(key, {
        pattern: interaction.pattern,
        solution: interaction.result,
        confidence: interaction.confidence
      });
    }
  }

  async getLearnedPatterns(actionType: string): Promise<any[]> {
    const patterns = [];
    for (const [key, value] of this.longTermMemory) {
      if (key.startsWith(actionType)) {
        patterns.push(value);
      }
    }
    return patterns;
  }

  async clearContext(): Promise<void> {
    this.contextWindow.clear();
    this.recentActions = [];
  }

  private calculateRelevance(query: string, content: string): number {
    const queryWords = query.toLowerCase().split(/\s+/);
    const contentWords = content.toLowerCase().split(/\s+/);

    let matches = 0;
    for (const queryWord of queryWords) {
      if (contentWords.some(contentWord => contentWord.includes(queryWord))) {
        matches++;
      }
    }

    return matches / queryWords.length;
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

    // Remove oldest items if exceeding max size
    if (this.items.length > this.maxSize) {
      this.items = this.items.slice(-this.maxSize);
    }
  }

  getAll(): ContextItem[] {
    return [...this.items];
  }

  getRecent(count: number): ContextItem[] {
    return this.items.slice(-count);
  }

  clear(): void {
    this.items = [];
  }
}

interface ContextItem {
  content: string;
  timestamp: Date;
  type: string;
}

interface AgentInteraction {
  user_input: string;
  agent_response: string;
  action_type: 'review' | 'debug' | 'optimize' | 'refactor' | 'document';
  target: string;
  result: any;
  success: boolean;
  important: boolean;
  pattern?: string;
  confidence?: number;
}

interface RelevantContext {
  items: ContextItem[];
  recent_actions: AgentAction[];
  query: string;
}
