/**
 * useMemoryAPI - Hook for Memory API operations
 * Kết nối với backend ZETA memory endpoints
 */

import { useCallback, useEffect, useState } from 'react';

import {
import API from "../../API/index";
import API_BASE_URL from "API_BASE_URL";
import Actions from "Actions";
import Add from "Add";
import Base from "Base";
import Build from "Build";
import Content from "Content";
import Create from "Create";
import DELETE from "DELETE";
import Delete from "Delete";
import Error from "Error";
import Failed from "Failed";
import Generic from "Generic";
import Get from "Get";
import HTTP from "HTTP";
import Hook from "Hook";
import ID from "ID";
import Load from "Load";
import POST from "POST";
import PUT from "PUT";
import Partial from "Partial";
import Refresh from "Refresh";
import Remove from "Remove";
import RequestInit from "RequestInit";
import Search from "Search";
import State from "State";
import T from "T";
import Type from "Type";
import URL from "URL";
import URLSearchParams from "URLSearchParams";
import Unknown from "Unknown";
import Update from "Update";
import UseMemoryAPIReturn from "UseMemoryAPIReturn";
import ZETA from "ZETA";
    CreateMemoryRequest,
    Memory,
    MemoryMetrics,
    MemorySearchQuery,
    MemorySearchResult
} from '../types/memory';

// API Base URL (will be from config)
const API_BASE_URL = 'http://localhost:8000/api/v1';

interface UseMemoryAPIReturn {
  // State
  memories: Memory[];
  isLoading: boolean;
  error: string | null;
  metrics: MemoryMetrics | null;
  
  // Actions
  searchMemories: (query: MemorySearchQuery) => Promise<MemorySearchResult>;
  createMemory: (request: CreateMemoryRequest) => Promise<Memory>;
  updateMemory: (id: string, updates: Partial<Memory>) => Promise<Memory>;
  deleteMemory: (id: string) => Promise<void>;
  getMemoryById: (id: string) => Promise<Memory | null>;
  getMemoryMetrics: () => Promise<MemoryMetrics>;
  refreshMemories: () => Promise<void>;
}

export const useMemoryAPI = (): UseMemoryAPIReturn => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<MemoryMetrics | null>(null);

  // Error handler
  const handleError = useCallback((error: any) => {
    const message = error?.response?.data?.detail || error?.message || 'Unknown error occurred';
    setError(message);
    console.error('Memory API Error:', error);
  }, []);

  // Generic API call wrapper
  const apiCall = useCallback(async <T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> => {
    setError(null);
    
    const url = `${API_BASE_URL}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      handleError(error);
      throw error;
    }
  }, [handleError]);

  // Search memories
  const searchMemories = useCallback(async (query: MemorySearchQuery): Promise<MemorySearchResult> => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      
      // Build query parameters
      params.append('query', query.query);
      if (query.types?.length) params.append('types', query.types.join(','));
      if (query.importance?.length) params.append('importance', query.importance.join(','));
      if (query.tags?.length) params.append('tags', query.tags.join(','));
      if (query.date_range) {
        params.append('start_date', query.date_range.start);
        params.append('end_date', query.date_range.end);
      }
      params.append('limit', String(query.limit || 20));
      params.append('offset', String(query.offset || 0));

      const result = await apiCall<MemorySearchResult>(`/memories/search?${params}`);
      setMemories(result.memories);
      return result;
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Create memory
  const createMemory = useCallback(async (request: CreateMemoryRequest): Promise<Memory> => {
    setIsLoading(true);
    try {
      const memory = await apiCall<Memory>('/memories', {
        method: 'POST',
        body: JSON.stringify(request),
      });
      
      // Add to local state
      setMemories(prev => [memory, ...prev]);
      return memory;
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Update memory
  const updateMemory = useCallback(async (id: string, updates: Partial<Memory>): Promise<Memory> => {
    setIsLoading(true);
    try {
      const memory = await apiCall<Memory>(`/memories/${id}`, {
        method: 'PUT',
        body: JSON.stringify(updates),
      });
      
      // Update local state
      setMemories(prev => prev.map(m => m.id === id ? memory : m));
      return memory;
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Delete memory
  const deleteMemory = useCallback(async (id: string): Promise<void> => {
    setIsLoading(true);
    try {
      await apiCall(`/memories/${id}`, { method: 'DELETE' });
      
      // Remove from local state
      setMemories(prev => prev.filter(m => m.id !== id));
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Get memory by ID
  const getMemoryById = useCallback(async (id: string): Promise<Memory | null> => {
    setIsLoading(true);
    try {
      return await apiCall<Memory>(`/memories/${id}`);
    } catch (error: any) {
      if (error?.message?.includes('404')) {
        return null;
      }
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Get memory metrics
  const getMemoryMetrics = useCallback(async (): Promise<MemoryMetrics> => {
    setIsLoading(true);
    try {
      const metrics = await apiCall<MemoryMetrics>('/memories/metrics');
      setMetrics(metrics);
      return metrics;
    } finally {
      setIsLoading(false);
    }
  }, [apiCall]);

  // Refresh memories (get recent)
  const refreshMemories = useCallback(async (): Promise<void> => {
    const result = await searchMemories({ 
      query: '', 
      limit: 50,
      offset: 0 
    });
    setMemories(result.memories);
  }, [searchMemories]);

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        await Promise.all([
          refreshMemories(),
          getMemoryMetrics()
        ]);
      } catch (error) {
        console.error('Failed to load initial memory data:', error);
      }
    };

    loadInitialData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return {
    // State
    memories,
    isLoading,
    error,
    metrics,
    
    // Actions
    searchMemories,
    createMemory,
    updateMemory,
    deleteMemory,
    getMemoryById,
    getMemoryMetrics,
    refreshMemories,
  };
};

export default useMemoryAPI;
