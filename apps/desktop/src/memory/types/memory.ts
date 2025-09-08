/**
 * Memory Management Types
 * Định nghĩa types cho Memory Management system
 */

import { z } from 'zod';
import ACTIVE from "ACTIVE";
import ARCHIVED from "ARCHIVED";
import Analytics from "../../Analytics/index";
import COMPRESSED from "COMPRESSED";
import CRITICAL from "CRITICAL";
import CreateMemoryRequest from "CreateMemoryRequest";
import DELETED from "DELETED";
import EPISODIC from "EPISODIC";
import Embeddings from "Embeddings";
import Entity from "Entity";
import Filter from "Filter";
import General from "General";
import Graph from "Graph";
import HIGH from "HIGH";
import How from "How";
import Interface from "Interface";
import Knowledge from "Knowledge";
import KnowledgeEdge from "KnowledgeEdge";
import KnowledgeGraph from "KnowledgeGraph";
import KnowledgeNode from "KnowledgeNode";
import LONG_TERM from "LONG_TERM";
import LOW from "LOW";
import MEDIUM from "MEDIUM";
import Management from "Management";
import Memory from "./Memory";
import MemoryImportance from "MemoryImportance";
import MemoryMetrics from "MemoryMetrics";
import MemorySearchQuery from "MemorySearchQuery";
import MemorySearchRequest from "MemorySearchRequest";
import MemorySearchResult from "MemorySearchResult";
import MemoryStatus from "MemoryStatus";
import MemoryType from "MemoryType";
import Metadata from "Metadata";
import Metrics from "Metrics";
import PROCEDURAL from "PROCEDURAL";
import Persistent from "Persistent";
import Record from "Record";
import Relationships from "Relationships";
import SEMANTIC from "SEMANTIC";
import Schemas from "Schemas";
import Search from "Search";
import Specific from "Specific";
import Temporary from "Temporary";
import Timestamps from "Timestamps";
import Types from "../../Types/index";
import Validation from "Validation";
import WORKING from "WORKING";
import Zod from "Zod";

// Memory Types matching backend entities
export enum MemoryType {
  EPISODIC = 'episodic',     // Specific events/conversations
  SEMANTIC = 'semantic',     // General knowledge/facts
  WORKING = 'working',       // Temporary/active info
  PROCEDURAL = 'procedural', // How-to knowledge/skills
  LONG_TERM = 'long_term'    // Persistent important memories
}

export enum MemoryStatus {
  ACTIVE = 'active',
  ARCHIVED = 'archived',
  COMPRESSED = 'compressed',
  DELETED = 'deleted'
}

export enum MemoryImportance {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

// Memory Entity Interface
export interface Memory {
  id: string;
  content: string;
  summary: string;
  type: MemoryType;
  status: MemoryStatus;
  importance: MemoryImportance;
  
  // Metadata
  tags: string[];
  context: Record<string, any>;
  
  // Relationships
  user_id?: string;
  agent_id?: string;
  linked_memories: string[];
  
  // Embeddings
  embedding?: {
    vector: number[];
    model: string;
    dimension: number;
  };
  
  // Metrics
  metrics: {
    access_count: number;
    last_accessed?: string;
    relevance_score: number;
  };
  
  // Timestamps
  created_at: string;
  updated_at: string;
}

// Search & Filter Types
export interface MemorySearchQuery {
  query: string;
  types?: MemoryType[];
  importance?: MemoryImportance[];
  tags?: string[];
  date_range?: {
    start: string;
    end: string;
  };
  limit?: number;
  offset?: number;
}

export interface MemorySearchResult {
  memories: Memory[];
  total: number;
  query_time: number;
  suggestions?: string[];
}

// Knowledge Graph Types
export interface KnowledgeNode {
  id: string;
  label: string;
  type: 'memory' | 'concept' | 'entity';
  importance: number;
  memory_count?: number;
  memory_ids: string[];
}

export interface KnowledgeEdge {
  source: string;
  target: string;
  relationship: string;
  strength: number;
  metadata?: Record<string, any>;
}

export interface KnowledgeGraph {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  metadata: {
    total_memories: number;
    concepts_count: number;
    last_updated: string;
  };
}

// Memory Analytics
export interface MemoryMetrics {
  total_memories: number;
  memories_by_type: Record<MemoryType, number>;
  memories_by_importance: Record<MemoryImportance, number>;
  storage_usage_mb: number;
  avg_access_frequency: number;
  top_tags: Array<{ tag: string; count: number }>;
  growth_trends: Array<{
    date: string;
    count: number;
    size_mb: number;
  }>;
}

// Zod Validation Schemas
export const memorySearchSchema = z.object({
  query: z.string().min(1),
  types: z.array(z.enum(['episodic', 'semantic', 'working', 'procedural', 'long_term'])).optional(),
  importance: z.array(z.enum(['low', 'medium', 'high', 'critical'])).optional(),
  tags: z.array(z.string()).optional(),
  date_range: z.object({
    start: z.string(),
    end: z.string()
  }).optional(),
  limit: z.number().min(1).max(100).default(20),
  offset: z.number().min(0).default(0)
});

export const createMemorySchema = z.object({
  content: z.string().min(1),
  type: z.enum(['episodic', 'semantic', 'working', 'procedural', 'long_term']).default('episodic'),
  importance: z.enum(['low', 'medium', 'high', 'critical']).default('medium'),
  tags: z.array(z.string()).default([]),
  context: z.record(z.string(), z.any()).default({}),
  agent_id: z.string().optional(),
  user_id: z.string().optional()
});

export type MemorySearchRequest = z.infer<typeof memorySearchSchema>;
export type CreateMemoryRequest = z.infer<typeof createMemorySchema>;
