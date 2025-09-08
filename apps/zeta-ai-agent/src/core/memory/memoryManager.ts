/**
 * Memory Manager
 * High-level interface for managing AI agent memory
 * Integrates episodic, semantic, và procedural memory systems
 */

import { VectorStoreMemory, MemoryEntry, MemoryQueryResult } from './vectorStore';
import AI from "AI";
import Active from "Active";
import Add from "Add";
import Analyze from "Analyze";
import Automatic from "Automatic";
import Base from "Base";
import CONTEXTUAL from "CONTEXTUAL";
import Check from "Check";
import Cleanup from "Cleanup";
import Consider from "Consider";
import Conversation from "Conversation";
import ConversationContext from "ConversationContext";
import Convert from "Convert";
import Days from "Days";
import Default from "Default";
import Determine from "Determine";
import EPISODIC from "EPISODIC";
import Error from "Error";
import Export from "Export";
import Extract from "Extract";
import Feedback from "Feedback";
import Generate from "Generate";
import Get from "Get";
import HIGH from "HIGH";
import High from "High";
import Hours from "Hours";
import IDs from "IDs";
import IMPROVEMENT_OPPORTUNITY from "IMPROVEMENT_OPPORTUNITY";
import Initialize from "Initialize";
import Integrates from "Integrates";
import Intent from "Intent";
import KNOWLEDGE_GAP from "KNOWLEDGE_GAP";
import LOW from "LOW";
import Learn from "Learn";
import Learning from "Learning";
import LearningInsight from "LearningInsight";
import Length from "Length";
import MEDIUM from "MEDIUM";
import Main from "../../../../desktop/src/Main";
import Manager from "Manager";
import Map from "Map";
import Mark from "Mark";
import Math from "Math";
import Memory from "../../../../desktop/src/Memory/index";
import MemoryManager from "./MemoryManager";
import NLP from "NLP";
import Negative from "Negative";
import No from "No";
import PATTERN from "PATTERN";
import PREFERENCE from "PREFERENCE";
import PROCEDURAL from "PROCEDURAL";
import Partial from "Partial";
import Private from "Private";
import Procedural from "Procedural";
import Procedure from "Procedure";
import Remove from "Remove";
import Retrieve from "Retrieve";
import SEMANTIC from "SEMANTIC";
import Sentiment from "Sentiment";
import Set from "Set";
import Simple from "Simple";
import Start from "Start";
import Started from "Started";
import Store from "Store";
import Top from "Top";
import Update from "Update";
import User from "User";

/**
 * Memory context for conversations
 */
export interface ConversationContext {
  conversationId: string;
  userId?: string;
  startTime: Date;
  lastActivity: Date;
  messageCount: number;
  topics: string[];
  summary?: string;
  importantMoments: string[]; // IDs of important memory entries
}

/**
 * Learning insight từ memory analysis
 */
export interface LearningInsight {
  type: 'PATTERN' | 'PREFERENCE' | 'KNOWLEDGE_GAP' | 'IMPROVEMENT_OPPORTUNITY';
  description: string;
  confidence: number;
  evidence: string[]; // Memory IDs supporting this insight
  actionable: boolean;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
}

/**
 * Memory Manager implementation
 */
export class MemoryManager {
  private readonly vectorStore: VectorStoreMemory;
  private readonly conversationContexts: Map<string, ConversationContext> = new Map();
  private currentConversationId?: string;
  private readonly maxConversationMemories: number = 50;
  private readonly consolidationInterval: number = 60 * 60 * 1000; // 1 hour

  constructor(storageDir?: string) {
    this.vectorStore = new VectorStoreMemory(storageDir);
    this.startConsolidationTimer();
  }

  /**
   * Initialize memory system
   */
  async initialize(): Promise<void> {
    await this.vectorStore.initialize();
    console.log('Memory Manager initialized');
  }

  /**
   * Start new conversation context
   */
  async startConversation(userId?: string): Promise<string> {
    const conversationId = this.generateConversationId();
    
    const context: ConversationContext = {
      conversationId,
      userId,
      startTime: new Date(),
      lastActivity: new Date(),
      messageCount: 0,
      topics: [],
      importantMoments: []
    };

    this.conversationContexts.set(conversationId, context);
    this.currentConversationId = conversationId;

    // Store conversation start as memory
    const startMessage = `Started conversation ${conversationId}`;
    const userInfo = userId ? ` with user ${userId}` : '';
    await this.storeMemory(
      startMessage + userInfo,
      'EPISODIC',
      {
        source: 'conversation_system',
        tags: ['conversation_start', userId || 'anonymous'],
        importance: 0.3
      }
    );

    return conversationId;
  }

  /**
   * Store conversation message as memory
   */
  async storeMessage(
    content: string,
    role: 'user' | 'assistant',
    metadata?: {
      intent?: string;
      entities?: string[];
      sentiment?: 'positive' | 'negative' | 'neutral';
      importance?: number;
    }
  ): Promise<string> {
    const context = this.getCurrentContext();
    if (!context) {
      throw new Error('No active conversation context');
    }

    // Update conversation context
    context.lastActivity = new Date();
    context.messageCount++;

    // Extract topics from content
    const extractedTopics = this.extractTopics(content);
    context.topics.push(...extractedTopics);
    context.topics = [...new Set(context.topics)]; // Remove duplicates

    // Determine memory importance
    const importance = metadata?.importance || this.calculateMessageImportance(content, role, metadata);

    // Store as memory
    const memoryId = await this.storeMemory(
      content,
      'EPISODIC',
      {
        source: `conversation_${role}`,
        tags: [
          'conversation',
          role,
          context.conversationId,
          ...(extractedTopics || []),
          ...(metadata?.entities || [])
        ],
        importance,
        ...metadata
      }
    );

    // Mark as important moment if high importance
    if (importance > 0.7) {
      context.importantMoments.push(memoryId);
    }

    return memoryId;
  }

  /**
   * Store memory with automatic categorization
   */
  async storeMemory(
    content: string,
    type?: MemoryEntry['metadata']['type'],
    metadata?: Partial<MemoryEntry['metadata']>
  ): Promise<string> {
    const memoryType = type || this.inferMemoryType(content);
    
    return await this.vectorStore.storeMemory(content, memoryType, {
      source: 'memory_manager',
      ...metadata
    });
  }

  /**
   * Retrieve relevant memories for context
   */
  async getRelevantMemories(
    query: string,
    options?: {
      conversationId?: string;
      includeTypes?: MemoryEntry['metadata']['type'][];
      timeWindow?: number; // Hours
      maxResults?: number;
    }
  ): Promise<MemoryQueryResult> {
    const queryOptions: any = {
      limit: options?.maxResults || 10
    };

    // Add conversation filter if specified
    if (options?.conversationId) {
      queryOptions.tags = [options.conversationId];
    }

    // Add type filter
    if (options?.includeTypes && options.includeTypes.length === 1) {
      queryOptions.type = options.includeTypes[0];
    }

    // Add time window filter
    if (options?.timeWindow) {
      const now = new Date();
      const startTime = new Date(now.getTime() - options.timeWindow * 60 * 60 * 1000);
      queryOptions.timeRange = { start: startTime, end: now };
    }

    return await this.vectorStore.queryMemories(query, queryOptions);
  }

  /**
   * Get conversation summary với key memories
   */
  async getConversationSummary(conversationId?: string): Promise<{
    context: ConversationContext | null;
    keyMemories: MemoryEntry[];
    summary: string;
    insights: LearningInsight[];
  }> {
    const targetId = conversationId || this.currentConversationId;
    if (!targetId) {
      return { context: null, keyMemories: [], summary: '', insights: [] };
    }

    const context = this.conversationContexts.get(targetId);
    if (!context) {
      return { context: null, keyMemories: [], summary: '', insights: [] };
    }

    // Get important memories from this conversation
    const keyMemories: MemoryEntry[] = [];
    for (const memoryId of context.importantMoments) {
      const memory = await this.vectorStore.getMemory(memoryId);
      if (memory) keyMemories.push(memory);
    }

    // Generate conversation summary
    const summary = await this.generateConversationSummary(context, keyMemories);

    // Extract learning insights
    const insights = await this.extractLearningInsights(keyMemories);

    return { context, keyMemories, summary, insights };
  }

  /**
   * Learn from user feedback
   */
  async learnFromFeedback(
    feedback: string,
    context: string,
    rating: number, // 1-5 scale
    metadata?: {
      category?: string;
      tags?: string[];
    }
  ): Promise<string> {
    const importance = this.calculateFeedbackImportance(rating, feedback);
    
    return await this.storeMemory(
      `Feedback (${rating}/5): ${feedback}\nContext: ${context}`,
      'SEMANTIC',
      {
        source: 'user_feedback',
        tags: ['feedback', `rating_${rating}`, ...(metadata?.tags || [])],
        importance,
        ...metadata
      }
    );
  }

  /**
   * Store procedural knowledge (how to do things)
   */
  async storeProceduralKnowledge(
    procedure: string,
    steps: string[],
    metadata?: {
      domain?: string;
      difficulty?: 'easy' | 'medium' | 'hard';
      success_rate?: number;
    }
  ): Promise<string> {
    const stepsList = steps.map((step, i) => `${i + 1}. ${step}`).join('\n');
    const content = `Procedure: ${procedure}\nSteps:\n${stepsList}`;
    
    return await this.storeMemory(
      content,
      'PROCEDURAL',
      {
        source: 'procedural_learning',
        tags: ['procedure', metadata?.domain || 'general'],
        importance: 0.8, // Procedural knowledge is generally important
        ...metadata
      }
    );
  }

  /**
   * Get memory statistics và insights
   */
  async getMemoryInsights(): Promise<{
    statistics: any;
    insights: LearningInsight[];
    recommendations: string[];
  }> {
    const statistics = this.vectorStore.getStatistics();
    
    // Analyze all memories for insights
    const allMemories = await this.getAllMemoriesSample();
    const insights = await this.extractLearningInsights(allMemories);
    
    // Generate recommendations
    const recommendations = this.generateMemoryRecommendations(statistics, insights);

    return { statistics, insights, recommendations };
  }

  /**
   * Export conversation history
   */
  async exportConversation(conversationId: string): Promise<string> {
    const memories = await this.vectorStore.queryMemories('', {
      tags: [conversationId],
      limit: 1000
    });

    const context = this.conversationContexts.get(conversationId);
    
    return JSON.stringify({
      conversationId,
      context,
      memories: memories.entries,
      exportTime: new Date().toISOString()
    }, null, 2);
  }

  /**
   * Cleanup old conversations và memories
   */
  async cleanup(options?: {
    maxAge?: number; // Days
    minImportance?: number;
    keepConversations?: number;
  }): Promise<{ removedMemories: number; removedConversations: number }> {
    const opts = {
      maxAge: 30, // 30 days default
      minImportance: 0.1,
      keepConversations: 10,
      ...options
    };

    // Cleanup memories
    const removedMemories = await this.vectorStore.consolidateMemories({
      maxAge: opts.maxAge * 24, // Convert to hours
      minImportance: opts.minImportance,
      maxSize: 50000,
      similarityThreshold: 0.95
    });

    // Cleanup old conversations
    const conversations = Array.from(this.conversationContexts.entries());
    conversations.sort((a, b) => b[1].lastActivity.getTime() - a[1].lastActivity.getTime());
    
    let removedConversations = 0;
    if (conversations.length > opts.keepConversations) {
      const toRemove = conversations.slice(opts.keepConversations);
      for (const [id] of toRemove) {
        this.conversationContexts.delete(id);
        removedConversations++;
      }
    }

    return { removedMemories, removedConversations };
  }

  /**
   * Private helper methods
   */

  private getCurrentContext(): ConversationContext | undefined {
    return this.currentConversationId ? 
      this.conversationContexts.get(this.currentConversationId) : 
      undefined;
  }

  private generateConversationId(): string {
    return `conv_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  private extractTopics(content: string): string[] {
    // Simple topic extraction - could be enhanced with NLP
    const words = content.toLowerCase().match(/\b\w+\b/g) || [];
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']);
    
    return words
      .filter(word => word.length > 3 && !stopWords.has(word))
      .slice(0, 5); // Top 5 words as topics
  }

  private calculateMessageImportance(
    content: string,
    role: 'user' | 'assistant',
    metadata?: any
  ): number {
    let importance = 0.5; // Base importance

    // User messages generally more important for learning
    if (role === 'user') importance += 0.1;

    // Length-based importance
    if (content.length > 200) importance += 0.1;

    // Intent-based importance
    if (metadata?.intent) {
      const highImportanceIntents = ['question', 'complaint', 'compliment', 'request'];
      if (highImportanceIntents.includes(metadata.intent)) importance += 0.2;
    }

    // Sentiment-based importance
    if (metadata?.sentiment === 'negative') importance += 0.2; // Learn from problems
    if (metadata?.sentiment === 'positive') importance += 0.1; // Learn from success

    return Math.min(importance, 1.0);
  }

  private inferMemoryType(content: string): MemoryEntry['metadata']['type'] {
    const lowerContent = content.toLowerCase();
    
    // Check for procedural indicators
    if (lowerContent.includes('how to') || lowerContent.includes('step') || lowerContent.includes('procedure')) {
      return 'PROCEDURAL';
    }
    
    // Check for semantic knowledge indicators
    if (lowerContent.includes('definition') || lowerContent.includes('concept') || lowerContent.includes('fact')) {
      return 'SEMANTIC';
    }

    // Check for contextual indicators
    if (lowerContent.includes('context') || lowerContent.includes('background')) {
      return 'CONTEXTUAL';
    }

    // Default to episodic for conversations and events
    return 'EPISODIC';
  }

  private calculateFeedbackImportance(rating: number, _feedback: string): number {
    // Negative feedback is more important for learning
    if (rating <= 2) return 0.9;
    if (rating === 3) return 0.6;
    if (rating >= 4) return 0.7;
    
    return 0.5;
  }

  private async generateConversationSummary(
    context: ConversationContext,
    keyMemories: MemoryEntry[]
  ): Promise<string> {
    const duration = (context.lastActivity.getTime() - context.startTime.getTime()) / (1000 * 60);
    const topics = context.topics.slice(0, 5).join(', ');
    
    return `Conversation ${context.conversationId} lasted ${Math.round(duration)} minutes with ${context.messageCount} messages. Main topics: ${topics}. ${keyMemories.length} important moments recorded.`;
  }

  private async extractLearningInsights(memories: MemoryEntry[]): Promise<LearningInsight[]> {
    const insights: LearningInsight[] = [];

    // Analyze patterns in feedback
    const feedbackMemories = memories.filter(m => m.metadata.tags.includes('feedback'));
    if (feedbackMemories.length > 0) {
      const avgRating = this.calculateAverageRating(feedbackMemories);
      
      if (avgRating < 3) {
        insights.push({
          type: 'IMPROVEMENT_OPPORTUNITY',
          description: 'User feedback indicates areas for improvement',
          confidence: 0.8,
          evidence: feedbackMemories.map(m => m.id),
          actionable: true,
          priority: 'HIGH'
        });
      }
    }

    // Analyze conversation patterns
    const conversationMemories = memories.filter(m => m.metadata.tags.includes('conversation'));
    if (conversationMemories.length > 10) {
      insights.push({
        type: 'PATTERN',
        description: 'Active conversation engagement detected',
        confidence: 0.7,
        evidence: conversationMemories.slice(0, 5).map(m => m.id),
        actionable: false,
        priority: 'MEDIUM'
      });
    }

    return insights;
  }

  private calculateAverageRating(feedbackMemories: MemoryEntry[]): number {
    const ratingRegex = /rating_(\d)/;
    const ratings = feedbackMemories
      .map(m => {
        const match = ratingRegex.exec(m.content);
        return match ? parseInt(match[1]) : 3;
      });
    
    return ratings.length > 0 ? 
      ratings.reduce((sum, rating) => sum + rating, 0) / ratings.length : 
      3;
  }

  private generateMemoryRecommendations(statistics: any, insights: LearningInsight[]): string[] {
    const recommendations: string[] = [];

    if (statistics.totalMemories > 10000) {
      recommendations.push('Consider running memory consolidation to optimize storage');
    }

    if (statistics.averageImportance < 0.3) {
      recommendations.push('Memory importance scores are low - consider adjusting importance calculation');
    }

    const highPriorityInsights = insights.filter(i => i.priority === 'HIGH');
    if (highPriorityInsights.length > 0) {
      recommendations.push('High priority learning insights detected - review for actionable improvements');
    }

    return recommendations;
  }

  private async getAllMemoriesSample(): Promise<MemoryEntry[]> {
    // Get a sample of all memories for analysis
    const result = await this.vectorStore.queryMemories('', { limit: 100 });
    return result.entries;
  }

  private startConsolidationTimer(): void {
    setInterval(async () => {
      try {
        await this.vectorStore.consolidateMemories();
        console.log('Automatic memory consolidation completed');
      } catch (error) {
        console.error('Memory consolidation failed:', error);
      }
    }, this.consolidationInterval);
  }
}
