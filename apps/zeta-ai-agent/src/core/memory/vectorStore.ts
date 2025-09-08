/**
 * Vector Store Memory System
 * Implements semantic memory using FAISS for long-term context and knowledge retrieval
 * Supports episodic memory, semantic knowledge, và contextual retrieval
 */

import * as fs from 'fs';
import * as path from 'path';
import API from "../../../../desktop/src/API/index";
import Add from "Add";
import Apply from "Apply";
import Build from "Build";
import CONTEXTUAL from "CONTEXTUAL";
import Calculate from "Calculate";
import Check from "Check";
import Combine from "Combine";
import Consolidate from "Consolidate";
import ConsolidationOptions from "ConsolidationOptions";
import Convert from "Convert";
import Days from "Days";
import Default from "Default";
import Delete from "Delete";
import Detect from "Detect";
import EPISODIC from "EPISODIC";
import Ensure from "Ensure";
import Error from "Error";
import Export from "Export";
import FAISS from "FAISS";
import Failed from "Failed";
import Fill from "Fill";
import Find from "Find";
import Generate from "Generate";
import Get from "Get";
import ID from "ID";
import IDs from "IDs";
import If from "If";
import Implements from "Implements";
import Import from "Import";
import Initial from "Initial";
import Initialize from "Initialize";
import Invalid from "Invalid";
import Load from "Load";
import Look from "Look";
import Map from "Map";
import Math from "Math";
import Max from "Max";
import Maximum from "Maximum";
import Memory from "../../../../desktop/src/Memory/index";
import MemoryEntry from "MemoryEntry";
import MemoryQueryResult from "MemoryQueryResult";
import Merge from "Merge";
import Minimum from "Minimum";
import Mock from "Mock";
import Normalize from "Normalize";
import OpenAI from "OpenAI";
import PROCEDURAL from "PROCEDURAL";
import Partial from "Partial";
import Persist from "Persist";
import Preserve from "Preserve";
import Query from "Query";
import Record from "Record";
import Remove from "Remove";
import Retrieve from "Retrieve";
import Return from "Return";
import SEMANTIC from "SEMANTIC";
import Same from "Same";
import Save from "Save";
import Search from "Search";
import Set from "Set";
import Simple from "Simple";
import Sort from "Sort";
import Store from "Store";
import Supports from "Supports";
import System from "System";
import Threshold from "Threshold";
import Top from "Top";
import Update from "Update";
import Validate from "Validate";
import Vector from "Vector";
import VectorStoreMemory from "VectorStoreMemory";
import Will from "Will";

/**
 * Memory entry structure
 */
export interface MemoryEntry {
  id: string;
  content: string;
  embedding: number[];
  metadata: {
    timestamp: Date;
    type: 'EPISODIC' | 'SEMANTIC' | 'PROCEDURAL' | 'CONTEXTUAL';
    source: string;
    tags: string[];
    importance: number; // 0-1 scale
    accessCount: number;
    lastAccessed: Date;
  };
  relationships?: {
    related: string[]; // IDs of related memories
    causal: string[]; // IDs of causal relationships
    temporal: string[]; // IDs of temporal relationships
  };
}

/**
 * Query result với similarity scores
 */
export interface MemoryQueryResult {
  entries: MemoryEntry[];
  similarities: number[];
  query: string;
  searchTime: number;
  totalResults: number;
}

/**
 * Memory consolidation options
 */
export interface ConsolidationOptions {
  maxAge: number; // Max age in hours before consolidation
  minImportance: number; // Minimum importance to keep
  maxSize: number; // Maximum number of entries
  similarityThreshold: number; // Threshold for merging similar memories
}

/**
 * Vector Store Memory implementation
 */
export class VectorStoreMemory {
  private readonly storageDir: string;
  private readonly indexFile: string;
  private readonly metadataFile: string;
  private readonly embeddingDim: number = 768; // Default embedding dimension
  
  private readonly memories: Map<string, MemoryEntry> = new Map();
  private faissIndex: any = null; // Will hold FAISS index when available
  private isInitialized = false;

  constructor(storageDir = './memory_store') {
    this.storageDir = storageDir;
    this.indexFile = path.join(storageDir, 'faiss_index.idx');
    this.metadataFile = path.join(storageDir, 'metadata.json');
    this.ensureStorageDirectory();
  }

  /**
   * Initialize memory system
   */
  async initialize(): Promise<void> {
    if (this.isInitialized) return;

    try {
      // Load existing memories
      await this.loadMemories();
      
      // Initialize FAISS index (mock implementation for now)
      await this.initializeFaissIndex();
      
      this.isInitialized = true;
      console.log(`Vector memory initialized with ${this.memories.size} entries`);
      
    } catch (error) {
      console.error('Failed to initialize vector memory:', error);
      throw error;
    }
  }

  /**
   * Store new memory entry
   */
  async storeMemory(
    content: string,
    type: MemoryEntry['metadata']['type'],
    metadata?: Partial<MemoryEntry['metadata']>
  ): Promise<string> {
    const id = this.generateMemoryId();
    const embedding = await this.generateEmbedding(content);
    
    const entry: MemoryEntry = {
      id,
      content,
      embedding,
      metadata: {
        timestamp: new Date(),
        type,
        source: metadata?.source || 'user_input',
        tags: metadata?.tags || [],
        importance: metadata?.importance || 0.5,
        accessCount: 0,
        lastAccessed: new Date(),
        ...metadata
      }
    };

    // Store in memory map
    this.memories.set(id, entry);

    // Add to FAISS index
    await this.addToIndex(entry);

    // Save to disk periodically
    if (this.memories.size % 10 === 0) {
      await this.persistMemories();
    }

    return id;
  }

  /**
   * Query memories by semantic similarity
   */
  async queryMemories(
    query: string,
    options?: {
      limit?: number;
      type?: MemoryEntry['metadata']['type'];
      tags?: string[];
      minImportance?: number;
      timeRange?: { start: Date; end: Date };
    }
  ): Promise<MemoryQueryResult> {
    const startTime = Date.now();
    const limit = options?.limit || 10;

    // Generate query embedding
    const queryEmbedding = await this.generateEmbedding(query);

    // Search FAISS index
    const searchResults = await this.searchIndex(queryEmbedding, limit * 2); // Get more results for filtering

    // Apply filters
    const filteredResults = this.applyFilters(searchResults, options);

    // Update access counts
    filteredResults.entries.forEach(entry => {
      entry.metadata.accessCount++;
      entry.metadata.lastAccessed = new Date();
    });

    const searchTime = Date.now() - startTime;

    return {
      entries: filteredResults.entries.slice(0, limit),
      similarities: filteredResults.similarities.slice(0, limit),
      query,
      searchTime,
      totalResults: this.memories.size
    };
  }

  /**
   * Retrieve specific memory by ID
   */
  async getMemory(id: string): Promise<MemoryEntry | null> {
    const memory = this.memories.get(id);
    if (memory) {
      memory.metadata.accessCount++;
      memory.metadata.lastAccessed = new Date();
    }
    return memory || null;
  }

  /**
   * Update existing memory
   */
  async updateMemory(id: string, updates: Partial<MemoryEntry>): Promise<boolean> {
    const existing = this.memories.get(id);
    if (!existing) return false;

    const updated = {
      ...existing,
      ...updates,
      id, // Preserve ID
      metadata: {
        ...existing.metadata,
        ...updates.metadata
      }
    };

    this.memories.set(id, updated);

    // Update in FAISS index if embedding changed
    if (updates.embedding) {
      await this.updateInIndex(updated);
    }

    return true;
  }

  /**
   * Delete memory entry
   */
  async deleteMemory(id: string): Promise<boolean> {
    const memory = this.memories.get(id);
    if (!memory) return false;

    this.memories.delete(id);
    await this.removeFromIndex(id);

    return true;
  }

  /**
   * Consolidate memories (remove old, unimportant ones)
   */
  async consolidateMemories(options?: ConsolidationOptions): Promise<number> {
    const opts: ConsolidationOptions = {
      maxAge: 24 * 7, // 1 week
      minImportance: 0.2,
      maxSize: 10000,
      similarityThreshold: 0.95,
      ...options
    };

    let removed = 0;
    const now = new Date();
    const cutoffTime = new Date(now.getTime() - opts.maxAge * 60 * 60 * 1000);

    // Remove old, unimportant memories
    for (const [id, memory] of this.memories) {
      if (
        memory.metadata.timestamp < cutoffTime &&
        memory.metadata.importance < opts.minImportance &&
        memory.metadata.accessCount < 2
      ) {
        await this.deleteMemory(id);
        removed++;
      }
    }

    // If still too many, remove by importance score
    if (this.memories.size > opts.maxSize) {
      const sorted = Array.from(this.memories.values())
        .sort((a, b) => this.calculateMemoryScore(a) - this.calculateMemoryScore(b));

      const toRemove = sorted.slice(0, this.memories.size - opts.maxSize);
      for (const memory of toRemove) {
        await this.deleteMemory(memory.id);
        removed++;
      }
    }

    // Merge very similar memories
    removed += await this.mergeSimilarMemories(opts.similarityThreshold);

    await this.persistMemories();
    return removed;
  }

  /**
   * Get memory statistics
   */
  getStatistics(): {
    totalMemories: number;
    byType: Record<string, number>;
    averageImportance: number;
    oldestMemory: Date | null;
    newestMemory: Date | null;
    totalAccessCount: number;
    } {
    const memories = Array.from(this.memories.values());
    
    const byType = memories.reduce((acc, memory) => {
      acc[memory.metadata.type] = (acc[memory.metadata.type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const timestamps = memories.map(m => m.metadata.timestamp);
    const importances = memories.map(m => m.metadata.importance);
    const accessCounts = memories.map(m => m.metadata.accessCount);

    return {
      totalMemories: memories.length,
      byType,
      averageImportance: importances.length > 0 
        ? importances.reduce((sum, imp) => sum + imp, 0) / importances.length 
        : 0,
      oldestMemory: timestamps.length > 0 ? new Date(Math.min(...timestamps.map(d => d.getTime()))) : null,
      newestMemory: timestamps.length > 0 ? new Date(Math.max(...timestamps.map(d => d.getTime()))) : null,
      totalAccessCount: accessCounts.reduce((sum, count) => sum + count, 0)
    };
  }

  /**
   * Build associative relationships between memories
   */
  async buildRelationships(): Promise<void> {
    const memories = Array.from(this.memories.values());
    
    for (const memory of memories) {
      const related = await this.findRelatedMemories(memory, 0.7); // 70% similarity threshold
      const temporal = this.findTemporallyRelated(memory, memories);
      
      memory.relationships = {
        related: related.slice(0, 5).map(r => r.id), // Top 5 related
        causal: this.findCausalRelationships(memory, memories), // Detect causal relationships
        temporal: temporal.slice(0, 3).map(r => r.id) // Top 3 temporal
      };
    }
  }

  /**
   * Export memories to JSON
   */
  async exportMemories(): Promise<string> {
    const exportData = {
      version: '1.0',
      timestamp: new Date().toISOString(),
      memories: Array.from(this.memories.values()),
      statistics: this.getStatistics()
    };

    return JSON.stringify(exportData, null, 2);
  }

  /**
   * Import memories from JSON
   */
  async importMemories(jsonData: string): Promise<number> {
    try {
      const data = JSON.parse(jsonData);
      let imported = 0;

      if (data.memories && Array.isArray(data.memories)) {
        for (const memory of data.memories) {
          // Validate memory structure
          if (this.isValidMemoryEntry(memory)) {
            this.memories.set(memory.id, memory);
            await this.addToIndex(memory);
            imported++;
          }
        }
      }

      await this.persistMemories();
      return imported;
    } catch (error) {
      console.error('Failed to import memories:', error);
      throw new Error('Invalid import data format');
    }
  }

  /**
   * Generate embedding for text (mock implementation)
   */
  private async generateEmbedding(text: string): Promise<number[]> {
    // Mock embedding generation - in real implementation, would use
    // sentence transformers or OpenAI embeddings API
    const embedding = new Array(this.embeddingDim).fill(0);
    
    // Simple hash-based mock embedding
    let hash = 0;
    for (let i = 0; i < text.length; i++) {
      const char = text.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }

    // Fill embedding with pseudo-random values based on hash
    for (let i = 0; i < this.embeddingDim; i++) {
      const seed = hash + i;
      embedding[i] = (Math.sin(seed) + 1) / 2; // Normalize to [0, 1]
    }

    // Normalize embedding
    const magnitude = Math.sqrt(embedding.reduce((sum, val) => sum + val * val, 0));
    return embedding.map(val => val / magnitude);
  }

  /**
   * Initialize FAISS index (mock implementation)
   */
  private async initializeFaissIndex(): Promise<void> {
    // Mock FAISS index - in real implementation would use faiss-node
    this.faissIndex = {
      dimension: this.embeddingDim,
      entries: new Map<string, { embedding: number[]; id: string }>()
    };

    // Load existing entries into index
    for (const memory of this.memories.values()) {
      this.faissIndex.entries.set(memory.id, {
        embedding: memory.embedding,
        id: memory.id
      });
    }
  }

  /**
   * Add entry to FAISS index
   */
  private async addToIndex(entry: MemoryEntry): Promise<void> {
    if (this.faissIndex) {
      this.faissIndex.entries.set(entry.id, {
        embedding: entry.embedding,
        id: entry.id
      });
    }
  }

  /**
   * Search FAISS index
   */
  private async searchIndex(
    queryEmbedding: number[], 
    limit: number
  ): Promise<{ entries: MemoryEntry[]; similarities: number[] }> {
    if (!this.faissIndex) {
      return { entries: [], similarities: [] };
    }

    // Calculate similarities with all entries
    const similarities: Array<{ id: string; similarity: number }> = [];
    
    for (const [id, indexEntry] of this.faissIndex.entries) {
      const similarity = this.cosineSimilarity(queryEmbedding, indexEntry.embedding);
      similarities.push({ id, similarity });
    }

    // Sort by similarity (descending)
    similarities.sort((a, b) => b.similarity - a.similarity);

    // Get top results
    const topResults = similarities.slice(0, limit);
    const entries = topResults
      .map(result => this.memories.get(result.id))
      .filter((entry): entry is MemoryEntry => entry !== undefined);

    return {
      entries,
      similarities: topResults.map(result => result.similarity)
    };
  }

  /**
   * Update entry in index
   */
  private async updateInIndex(entry: MemoryEntry): Promise<void> {
    await this.addToIndex(entry); // Same operation for mock implementation
  }

  /**
   * Remove entry from index
   */
  private async removeFromIndex(id: string): Promise<void> {
    if (this.faissIndex) {
      this.faissIndex.entries.delete(id);
    }
  }

  /**
   * Calculate cosine similarity between two vectors
   */
  private cosineSimilarity(a: number[], b: number[]): number {
    if (a.length !== b.length) return 0;

    let dotProduct = 0;
    let normA = 0;
    let normB = 0;

    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }

    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }

  /**
   * Apply filters to search results
   */
  private applyFilters(
    results: { entries: MemoryEntry[]; similarities: number[] },
    options?: {
      type?: MemoryEntry['metadata']['type'];
      tags?: string[];
      minImportance?: number;
      timeRange?: { start: Date; end: Date };
    }
  ): { entries: MemoryEntry[]; similarities: number[] } {
    if (!options) return results;

    const filtered: { entry: MemoryEntry; similarity: number }[] = [];

    for (let i = 0; i < results.entries.length; i++) {
      const entry = results.entries[i];
      const similarity = results.similarities[i];

      if (this.shouldIncludeEntry(entry, options)) {
        filtered.push({ entry, similarity });
      }
    }

    return {
      entries: filtered.map(f => f.entry),
      similarities: filtered.map(f => f.similarity)
    };
  }

  /**
   * Check if entry should be included based on filters
   */
  private shouldIncludeEntry(
    entry: MemoryEntry,
    options: {
      type?: MemoryEntry['metadata']['type'];
      tags?: string[];
      minImportance?: number;
      timeRange?: { start: Date; end: Date };
    }
  ): boolean {
    if (options.type && entry.metadata.type !== options.type) return false;
    if (options.minImportance && entry.metadata.importance < options.minImportance) return false;
    if (options.tags && !this.hasMatchingTags(entry.metadata.tags, options.tags)) return false;
    if (options.timeRange && !this.isWithinTimeRange(entry.metadata.timestamp, options.timeRange)) return false;
    
    return true;
  }

  /**
   * Check if entry has matching tags
   */
  private hasMatchingTags(entryTags: string[], filterTags: string[]): boolean {
    return filterTags.some(tag => entryTags.includes(tag));
  }

  /**
   * Check if timestamp is within time range
   */
  private isWithinTimeRange(timestamp: Date, timeRange: { start: Date; end: Date }): boolean {
    return timestamp >= timeRange.start && timestamp <= timeRange.end;
  }

  /**
   * Find causal relationships between memories
   */
  private findCausalRelationships(memory: MemoryEntry, allMemories: MemoryEntry[]): string[] {
    const causalKeywords = ['because', 'therefore', 'as a result', 'consequently', 'leads to', 'causes'];
    const causalRelated: string[] = [];

    // Look for causal patterns in content
    for (const other of allMemories) {
      if (other.id === memory.id) continue;

      // Check if this memory mentions causal relationships
      const hasCausalLanguage = causalKeywords.some(keyword => 
        memory.content.toLowerCase().includes(keyword) ||
        other.content.toLowerCase().includes(keyword)
      );

      if (hasCausalLanguage) {
        // Simple causal detection based on temporal order and semantic similarity
        const timeDiff = other.metadata.timestamp.getTime() - memory.metadata.timestamp.getTime();
        const similarity = this.cosineSimilarity(memory.embedding, other.embedding);

        // If other memory is later and similar enough, it might be causally related
        if (timeDiff > 0 && timeDiff < 24 * 60 * 60 * 1000 && similarity > 0.6) {
          causalRelated.push(other.id);
        }
      }
    }

    return causalRelated.slice(0, 3); // Return top 3 causal relationships
  }

  /**
   * Calculate memory importance score
   */
  private calculateMemoryScore(memory: MemoryEntry): number {
    const age = (Date.now() - memory.metadata.timestamp.getTime()) / (1000 * 60 * 60 * 24); // Days
    const accessFrequency = memory.metadata.accessCount / Math.max(age, 1);
    
    return memory.metadata.importance * 0.4 + 
           accessFrequency * 0.4 + 
           (memory.metadata.tags.length > 0 ? 0.1 : 0) +
           (memory.relationships?.related.length || 0) * 0.1;
  }

  /**
   * Find related memories based on similarity
   */
  private async findRelatedMemories(
    memory: MemoryEntry, 
    threshold: number
  ): Promise<MemoryEntry[]> {
    const results = await this.searchIndex(memory.embedding, 20);
    return results.entries.filter((entry, index) => 
      entry.id !== memory.id && results.similarities[index] >= threshold
    );
  }

  /**
   * Find temporally related memories
   */
  private findTemporallyRelated(
    memory: MemoryEntry, 
    allMemories: MemoryEntry[]
  ): MemoryEntry[] {
    const timeWindow = 60 * 60 * 1000; // 1 hour window
    const memoryTime = memory.metadata.timestamp.getTime();

    return allMemories.filter(other => 
      other.id !== memory.id &&
      Math.abs(other.metadata.timestamp.getTime() - memoryTime) <= timeWindow
    );
  }

  /**
   * Merge similar memories
   */
  private async mergeSimilarMemories(threshold: number): Promise<number> {
    let merged = 0;
    const processed = new Set<string>();

    for (const memory of this.memories.values()) {
      if (processed.has(memory.id)) continue;

      const similar = await this.findRelatedMemories(memory, threshold);
      if (similar.length > 0) {
        // Merge the most important similar memory
        const mostImportant = similar.reduce((best, current) => 
          current.metadata.importance > best.metadata.importance ? current : best,
        similar[0] // Initial value
        );

        // Combine content and metadata
        const mergedContent = `${memory.content}\n---\n${mostImportant.content}`;
        const mergedTags = [...new Set([...memory.metadata.tags, ...mostImportant.metadata.tags])];

        await this.updateMemory(memory.id, {
          content: mergedContent,
          metadata: {
            ...memory.metadata,
            importance: Math.max(memory.metadata.importance, mostImportant.metadata.importance),
            tags: mergedTags,
            accessCount: memory.metadata.accessCount + mostImportant.metadata.accessCount
          }
        });

        // Remove the merged memory
        await this.deleteMemory(mostImportant.id);
        processed.add(mostImportant.id);
        merged++;
      }

      processed.add(memory.id);
    }

    return merged;
  }

  /**
   * Validate memory entry structure
   */
  private isValidMemoryEntry(entry: any): entry is MemoryEntry {
    return entry &&
           typeof entry.id === 'string' &&
           typeof entry.content === 'string' &&
           Array.isArray(entry.embedding) &&
           entry.metadata &&
           typeof entry.metadata.type === 'string';
  }

  /**
   * Generate unique memory ID
   */
  private generateMemoryId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  }

  /**
   * Ensure storage directory exists
   */
  private ensureStorageDirectory(): void {
    if (!fs.existsSync(this.storageDir)) {
      fs.mkdirSync(this.storageDir, { recursive: true });
    }
  }

  /**
   * Load memories from disk
   */
  private async loadMemories(): Promise<void> {
    try {
      if (fs.existsSync(this.metadataFile)) {
        const data = fs.readFileSync(this.metadataFile, 'utf-8');
        const memories = JSON.parse(data);
        
        if (Array.isArray(memories)) {
          memories.forEach(memory => {
            if (this.isValidMemoryEntry(memory)) {
              // Convert timestamp strings back to Date objects
              memory.metadata.timestamp = new Date(memory.metadata.timestamp);
              memory.metadata.lastAccessed = new Date(memory.metadata.lastAccessed);
              this.memories.set(memory.id, memory);
            }
          });
        }
      }
    } catch (error) {
      console.warn('Failed to load existing memories:', error);
    }
  }

  /**
   * Persist memories to disk
   */
  private async persistMemories(): Promise<void> {
    try {
      const memories = Array.from(this.memories.values());
      fs.writeFileSync(this.metadataFile, JSON.stringify(memories, null, 2));
    } catch (error) {
      console.error('Failed to persist memories:', error);
    }
  }
}
