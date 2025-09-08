import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import React, { useState, useEffect, useMemo, useRef } from "react";
/**
 * Memory Module Tests
 * Test suite cho Memory Management components
 */

import { beforeEach, describe, expect, it, vi } from 'vitest';

import KnowledgeExplorer from '../components/KnowledgeExplorer';
import MemoryPage from '../MemoryPage';
import { Memory, MemoryImportance, MemoryType } from '../types/memory';
import Access from "Access";
import Avg from "Avg";
import CRITICAL from "CRITICAL";
import Check from "Check";
import Click from "Click";
import Component from "Component";
import EPISODIC from "EPISODIC";
import Enums from "Enums";
import Filter from "Filter";
import Go from "Go";
import Grid from "Grid";
import HIGH from "HIGH";
import Hook from "Hook";
import Importance from "Importance";
import Integration from "Integration";
import LONG_TERM from "LONG_TERM";
import LOW from "LOW";
import Level from "Level";
import List from "List";
import MB from "MB";
import MEDIUM from "MEDIUM";
import Management from "Management";
import Memories from "Memories";
import Mock from "Mock";
import Module from "Module";
import Open from "Open";
import PROCEDURAL from "PROCEDURAL";
import Rate from "Rate";
import SEMANTIC from "SEMANTIC";
import Sample from "Sample";
import Search from "Search";
import Select from "Select";
import Should from "Should";
import Storage from "Storage";
import Switch from "Switch";
import Tags from "Tags";
import Test from "../../Test/index";
import Tests from "../../Tests/index";
import This from "This";
import Timeline from "Timeline";
import Total from "Total";
import Type from "Type";
import Types from "../../Types/index";
import Used from "Used";
import View from "View";
import WORKING from "WORKING";
import Wait from "Wait";

// Mock useMemoryAPI hook
vi.mock('../hooks/useMemoryAPI', () => ({
  useMemoryAPI: vi.fn(() => ({
    memories: [],
    isLoading: false,
    error: null,
    metrics: {
      total_memories: 150,
      storage_usage_mb: 12.5,
      avg_access_frequency: 0.85,
      memories_by_type: {
        episodic: 75,
        semantic: 50,
        working: 15,
        procedural: 8,
        long_term: 2
      },
      top_tags: [
        { tag: 'ai', count: 45 },
        { tag: 'python', count: 32 },
        { tag: 'conversation', count: 28 }
      ]
    },
    searchMemories: vi.fn(),
    createMemory: vi.fn(),
    updateMemory: vi.fn(),
    deleteMemory: vi.fn(),
    getMemoryById: vi.fn(),
    getMemoryMetrics: vi.fn(),
    refreshMemories: vi.fn()
  }))
}));

// Sample memory data for testing
const sampleMemory: Memory = {
  id: 'test-memory-1',
  content: 'This is a test memory content for unit testing purposes.',
  summary: 'Test memory content',
  type: MemoryType.EPISODIC,
  status: 'active' as any,
  importance: MemoryImportance.MEDIUM,
  tags: ['test', 'memory', 'ai'],
  context: { source: 'test', session: 'unit-test' },
  user_id: 'test-user',
  agent_id: 'test-agent',
  linked_memories: [],
  embedding: {
    vector: [0.1, 0.2, 0.3],
    model: 'test-model',
    dimension: 3
  },
  metrics: {
    access_count: 5,
    last_accessed: '2025-01-01T00:00:00Z',
    relevance_score: 0.85
  },
  created_at: '2025-01-01T00:00:00Z',
  updated_at: '2025-01-01T00:00:00Z'
};

describe('KnowledgeExplorer Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders knowledge explorer with search interface', () => {
    render(<KnowledgeExplorer />);
    
    // Check main elements
    expect(screen.getByPlaceholderText(/search memories/i)).toBeInTheDocument();
    expect(screen.getByText(/filters/i)).toBeInTheDocument();
    expect(screen.getByText(/search your knowledge base/i)).toBeInTheDocument();
  });

  it('shows search input and filter controls', () => {
    render(<KnowledgeExplorer />);
    
    // Search input should be present
    const searchInput = screen.getByPlaceholderText(/search memories/i);
    expect(searchInput).toBeInTheDocument();
    
    // Filter button should be present
    const filterButton = screen.getByText(/filters/i);
    expect(filterButton).toBeInTheDocument();
    
    // View mode buttons should be present
    expect(screen.getByText('📄')).toBeInTheDocument(); // List view
    expect(screen.getByText('⊞')).toBeInTheDocument();  // Grid view
    expect(screen.getByText('📅')).toBeInTheDocument(); // Timeline view
  });

  it('expands filters when filter button is clicked', async () => {
    render(<KnowledgeExplorer />);
    
    // Click filter button
    const filterButton = screen.getByText(/filters/i);
    fireEvent.click(filterButton);
    
    // Filter panel should appear
    await waitFor(() => {
      expect(screen.getByText('Memory Types')).toBeInTheDocument();
      expect(screen.getByText('Importance Level')).toBeInTheDocument();
      expect(screen.getByText('Tags')).toBeInTheDocument();
    });
  });

  it('handles memory type filter selection', async () => {
    render(<KnowledgeExplorer />);
    
    // Open filters
    fireEvent.click(screen.getByText(/filters/i));
    
    // Click on episodic filter
    await waitFor(() => {
      const episodicFilter = screen.getByText('episodic');
      fireEvent.click(episodicFilter);
      expect(episodicFilter).toHaveClass('active');
    });
  });

  it('handles search input changes', () => {
    render(<KnowledgeExplorer />);
    
    const searchInput = screen.getByPlaceholderText(/search memories/i);
    fireEvent.change(searchInput, { target: { value: 'test query' } });
    
    expect(searchInput).toHaveValue('test query');
  });

  it('calls onMemorySelect when memory is selected', async () => {
    const mockOnSelect = vi.fn();
    const { useMemoryAPI } = await import('../hooks/useMemoryAPI');
    
    // Mock search results
    const mockSearchMemories = vi.fn().mockResolvedValue({
      memories: [sampleMemory],
      total: 1,
      query_time: 50
    });

    vi.mocked(useMemoryAPI).mockReturnValue({
      memories: [sampleMemory],
      isLoading: false,
      error: null,
      metrics: null,
      searchMemories: mockSearchMemories,
      createMemory: vi.fn(),
      updateMemory: vi.fn(),
      deleteMemory: vi.fn(),
      getMemoryById: vi.fn(),
      getMemoryMetrics: vi.fn(),
      refreshMemories: vi.fn()
    });

    render(<KnowledgeExplorer onMemorySelect={mockOnSelect} />);
    
    // Type in search and wait for results
    const searchInput = screen.getByPlaceholderText(/search memories/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    
    // Wait for search results and click on memory
    await waitFor(() => {
      const memoryCard = screen.getByLabelText(/Select memory: Test memory content/);
      expect(memoryCard).toBeInTheDocument();
      fireEvent.click(memoryCard);
      expect(mockOnSelect).toHaveBeenCalledWith(sampleMemory);
    });
  });

  it('changes view mode when view buttons are clicked', () => {
    render(<KnowledgeExplorer />);
    
    // Click grid view
    const gridViewBtn = screen.getByText('⊞');
    fireEvent.click(gridViewBtn);
    expect(gridViewBtn).toHaveClass('active');
    
    // Click timeline view
    const timelineViewBtn = screen.getByText('📅');
    fireEvent.click(timelineViewBtn);
    expect(timelineViewBtn).toHaveClass('active');
  });
});

describe('MemoryPage Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders memory page with header and navigation', () => {
    render(<MemoryPage />);
    
    // Check header elements
    expect(screen.getByText(/memory management/i)).toBeInTheDocument();
    expect(screen.getByText(/explore và quản lý knowledge base/i)).toBeInTheDocument();
    
    // Check navigation tabs
    expect(screen.getByText(/explore knowledge/i)).toBeInTheDocument();
    expect(screen.getByText(/analytics/i)).toBeInTheDocument();
    expect(screen.getByText(/settings/i)).toBeInTheDocument();
  });

  it('displays memory metrics in header stats', () => {
    render(<MemoryPage />);
    
    // Check stats are displayed
    expect(screen.getByText('150')).toBeInTheDocument(); // total memories
    expect(screen.getByText('12.5 MB')).toBeInTheDocument(); // storage usage
    expect(screen.getByText('85%')).toBeInTheDocument(); // access rate
    
    // Check stat labels
    expect(screen.getByText('Total Memories')).toBeInTheDocument();
    expect(screen.getByText('Storage Used')).toBeInTheDocument();
    expect(screen.getByText('Avg Access Rate')).toBeInTheDocument();
  });

  it('switches tabs when navigation buttons are clicked', () => {
    render(<MemoryPage />);
    
    // Click analytics tab
    const analyticsTab = screen.getByText(/analytics/i);
    fireEvent.click(analyticsTab);
    expect(analyticsTab).toHaveClass('active');
    expect(screen.getByText(/memory analytics/i)).toBeInTheDocument();
    
    // Click settings tab
    const settingsTab = screen.getByText(/settings/i);
    fireEvent.click(settingsTab);
    expect(settingsTab).toHaveClass('active');
    expect(screen.getByText(/memory settings/i)).toBeInTheDocument();
    
    // Go back to explore tab
    const exploreTab = screen.getByText(/explore knowledge/i);
    fireEvent.click(exploreTab);
    expect(exploreTab).toHaveClass('active');
  });

  it('shows analytics preview when analytics tab is active', () => {
    render(<MemoryPage />);
    
    // Switch to analytics tab
    fireEvent.click(screen.getByText(/analytics/i));
    
    // Check analytics content
    expect(screen.getByText(/memory analytics/i)).toBeInTheDocument();
    expect(screen.getByText(/quick overview/i)).toBeInTheDocument();
    expect(screen.getByText(/memory types/i)).toBeInTheDocument();
    expect(screen.getByText(/top tags/i)).toBeInTheDocument();
  });

  it('shows settings preview when settings tab is active', () => {
    render(<MemoryPage />);
    
    // Switch to settings tab
    fireEvent.click(screen.getByText(/settings/i));
    
    // Check settings content
    expect(screen.getByText(/memory settings/i)).toBeInTheDocument();
    expect(screen.getByText(/planned settings/i)).toBeInTheDocument();
    expect(screen.getByText(/memory retention policies/i)).toBeInTheDocument();
    expect(screen.getByText(/auto-compression settings/i)).toBeInTheDocument();
  });

  it('renders knowledge explorer in explore tab', () => {
    render(<MemoryPage />);
    
    // Should be in explore tab by default
    expect(screen.getByPlaceholderText(/search memories/i)).toBeInTheDocument();
  });
});

describe('Memory Types and Enums', () => {
  it('exports correct memory type enum values', () => {
    expect(MemoryType.EPISODIC).toBe('episodic');
    expect(MemoryType.SEMANTIC).toBe('semantic');
    expect(MemoryType.WORKING).toBe('working');
    expect(MemoryType.PROCEDURAL).toBe('procedural');
    expect(MemoryType.LONG_TERM).toBe('long_term');
  });

  it('exports correct memory importance enum values', () => {
    expect(MemoryImportance.LOW).toBe('low');
    expect(MemoryImportance.MEDIUM).toBe('medium');
    expect(MemoryImportance.HIGH).toBe('high');
    expect(MemoryImportance.CRITICAL).toBe('critical');
  });
});

describe('useMemoryAPI Hook Integration', () => {
  it('should be properly mocked for testing', async () => {
    const { useMemoryAPI } = await import('../hooks/useMemoryAPI');
    const hookResult = useMemoryAPI();
    
    expect(hookResult).toHaveProperty('memories');
    expect(hookResult).toHaveProperty('isLoading');
    expect(hookResult).toHaveProperty('error');
    expect(hookResult).toHaveProperty('metrics');
    expect(hookResult).toHaveProperty('searchMemories');
    expect(hookResult).toHaveProperty('createMemory');
    expect(hookResult).toHaveProperty('updateMemory');
    expect(hookResult).toHaveProperty('deleteMemory');
  });
});
