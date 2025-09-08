/**
 * KnowledgeExplorer - Knowledge Base Browser Component
 * Interface để browse, search và quản lý knowledge base
 */

import React, { useCallback, useEffect, useState } from 'react';

import { useMemoryAPI } from '../hooks/useMemoryAPI';
import {
    Memory,
    MemoryImportance,
    MemorySearchQuery,
    MemorySearchResult,
    MemoryType
} from '../types/memory';
import './KnowledgeExplorer.css';
import Add from "Add";
import Auto from "Auto";
import Base from "Base";
import Browser from "Browser";
import Component from "Component";
import Controls from "Controls";
import Display from "Display";
import Enter from "Enter";
import Error from "Error";
import FC from "FC";
import Filter from "Filter";
import Filters from "Filters";
import Found from "Found";
import HTMLInputElement from "HTMLInputElement";
import Header from "Header";
import Helper from "Helper";
import Importance from "Importance";
import Interface from "Interface";
import Knowledge from "Knowledge";
import KnowledgeExplorer from "./KnowledgeExplorer";
import KnowledgeExplorerProps from "KnowledgeExplorerProps";
import Level from "Level";
import Loading from "Loading";
import Math from "Math";
import MemoryCard from "MemoryCard";
import No from "No";
import Panel from "Panel";
import Relevance from "Relevance";
import Results from "Results";
import Search from "Search";
import Searching from "Searching";
import Select from "Select";
import Sort from "Sort";
import State from "State";
import Suggestions from "Suggestions";
import Switch from "Switch";
import Tag from "Tag";
import Tags from "Tags";
import Try from "Try";
import Type from "Type";
import Types from "../../Types/index";
import UI from "../../UI/index";
import View from "View";

interface KnowledgeExplorerProps {
  className?: string;
  onMemorySelect?: (memory: Memory) => void;
  initialQuery?: string;
}

const KnowledgeExplorer: React.FC<KnowledgeExplorerProps> = ({
  className = '',
  onMemorySelect,
  initialQuery = ''
}) => {
  const { searchMemories, isLoading, error } = useMemoryAPI();
  
  // Search state
  const [searchQuery, setSearchQuery] = useState(initialQuery);
  const [searchResult, setSearchResult] = useState<MemorySearchResult | null>(null);
  const [selectedTypes, setSelectedTypes] = useState<MemoryType[]>([]);
  const [selectedImportance, setSelectedImportance] = useState<MemoryImportance[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  
  // UI state
  const [viewMode, setViewMode] = useState<'list' | 'grid' | 'timeline'>('list');
  const [sortBy, setSortBy] = useState<'relevance' | 'date' | 'importance'>('relevance');
  const [showFilters, setShowFilters] = useState(false);

  // Search handler
  const handleSearch = useCallback(async () => {
    if (!searchQuery.trim()) return;

    const query: MemorySearchQuery = {
      query: searchQuery,
      types: selectedTypes.length > 0 ? selectedTypes : undefined,
      importance: selectedImportance.length > 0 ? selectedImportance : undefined,
      tags: selectedTags.length > 0 ? selectedTags : undefined,
      limit: 50,
      offset: 0
    };

    try {
      const result = await searchMemories(query);
      setSearchResult(result);
    } catch (error) {
      console.error('Search failed:', error);
    }
  }, [searchQuery, selectedTypes, selectedImportance, selectedTags, searchMemories]);

  // Auto-search on query change (debounced)
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery.trim()) {
        handleSearch();
      }
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [searchQuery, handleSearch]);

  // Filter handlers
  const toggleType = (type: MemoryType) => {
    setSelectedTypes(prev => 
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const toggleImportance = (importance: MemoryImportance) => {
    setSelectedImportance(prev => 
      prev.includes(importance) ? prev.filter(i => i !== importance) : [...prev, importance]
    );
  };

  const addTag = (tag: string) => {
    if (tag && !selectedTags.includes(tag)) {
      setSelectedTags(prev => [...prev, tag]);
    }
  };

  const removeTag = (tag: string) => {
    setSelectedTags(prev => prev.filter(t => t !== tag));
  };

  // Helper function to get view mode icon
  const getViewModeIcon = (mode: 'list' | 'grid' | 'timeline') => {
    switch (mode) {
      case 'list': return '📄';
      case 'grid': return '⊞';
      case 'timeline': return '📅';
      default: return '📄';
    }
  };

  // Memory card component
  const MemoryCard: React.FC<{ memory: Memory }> = ({ memory }) => (
    <button 
      className="memory-card"
      onClick={() => onMemorySelect?.(memory)}
      aria-label={`Select memory: ${memory.summary || memory.content.substring(0, 50)}`}
    >
      <div className="memory-card__header">
        <div className="memory-card__type-badge" data-type={memory.type}>
          {memory.type}
        </div>
        <div className="memory-card__importance" data-importance={memory.importance}>
          {memory.importance}
        </div>
      </div>
      
      <div className="memory-card__content">
        <div className="memory-card__summary">
          {memory.summary || memory.content.substring(0, 150)}...
        </div>
        
        {memory.tags.length > 0 && (
          <div className="memory-card__tags">
            {memory.tags.slice(0, 3).map(tag => (
              <span key={tag} className="memory-card__tag">#{tag}</span>
            ))}
            {memory.tags.length > 3 && (
              <span className="memory-card__tag-more">+{memory.tags.length - 3}</span>
            )}
          </div>
        )}
      </div>
      
      <div className="memory-card__footer">
        <div className="memory-card__metrics">
          <span>👁️ {memory.metrics.access_count}</span>
          <span>📊 {Math.round(memory.metrics.relevance_score * 100)}%</span>
        </div>
        <div className="memory-card__date">
          {new Date(memory.created_at).toLocaleDateString()}
        </div>
      </div>
    </button>
  );

  return (
    <div className={`knowledge-explorer ${className}`}>
      {/* Search Header */}
      <div className="knowledge-explorer__header">
        <div className="knowledge-explorer__search-section">
          <div className="search-input-group">
            <input
              type="text"
              className="search-input"
              placeholder="🔍 Search memories, concepts, or knowledge..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button 
              className="search-button"
              onClick={handleSearch}
              disabled={isLoading}
            >
              {isLoading ? '⏳' : '🔍'}
            </button>
          </div>
          
          <button 
            className={`filter-toggle ${showFilters ? 'active' : ''}`}
            onClick={() => setShowFilters(!showFilters)}
            aria-expanded={showFilters}
            aria-controls="filters-panel"
          >
            🎛️ Filters
          </button>
        </div>

        {/* View Controls */}
        <div className="knowledge-explorer__controls">
          <div className="view-mode-selector">
            {(['list', 'grid', 'timeline'] as const).map(mode => (
              <button
                key={mode}
                className={`view-mode-btn ${viewMode === mode ? 'active' : ''}`}
                onClick={() => setViewMode(mode)}
                aria-pressed={viewMode === mode}
                title={`Switch to ${mode} view`}
              >
                {getViewModeIcon(mode)}
              </button>
            ))}
          </div>
          
          <select 
            className="sort-selector"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
          >
            <option value="relevance">Sort by Relevance</option>
            <option value="date">Sort by Date</option>
            <option value="importance">Sort by Importance</option>
          </select>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="knowledge-explorer__filters">
          {/* Type Filters */}
          <div className="filter-group">
            <h4>Memory Types</h4>
            <div className="filter-chips">
              {Object.values(MemoryType).map(type => (
                <button
                  key={type}
                  className={`filter-chip ${selectedTypes.includes(type) ? 'active' : ''}`}
                  onClick={() => toggleType(type)}
                >
                  {type}
                </button>
              ))}
            </div>
          </div>

          {/* Importance Filters */}
          <div className="filter-group">
            <h4>Importance Level</h4>
            <div className="filter-chips">
              {Object.values(MemoryImportance).map(importance => (
                <button
                  key={importance}
                  className={`filter-chip ${selectedImportance.includes(importance) ? 'active' : ''}`}
                  onClick={() => toggleImportance(importance)}
                >
                  {importance}
                </button>
              ))}
            </div>
          </div>

          {/* Tag Filters */}
          <div className="filter-group">
            <h4>Tags</h4>
            <div className="tag-input-section">
              <input
                type="text"
                placeholder="Add tag filter..."
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    addTag((e.target as HTMLInputElement).value);
                    (e.target as HTMLInputElement).value = '';
                  }
                }}
              />
              <div className="selected-tags">
                {selectedTags.map(tag => (
                  <span key={tag} className="selected-tag">
                    #{tag} 
                    <button onClick={() => removeTag(tag)}>×</button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="knowledge-explorer__error">
          ⚠️ {error}
        </div>
      )}

      {/* Search Results */}
      <div className="knowledge-explorer__results">
        {searchResult && (
          <>
            <div className="results-header">
              <span className="results-count">
                Found {searchResult.total} memories 
                {Boolean(searchResult.query_time) && (
                  <span className="query-time">({searchResult.query_time}ms)</span>
                )}
              </span>
              
              {searchResult.suggestions && searchResult.suggestions.length > 0 && (
                <div className="search-suggestions">
                  <span>Suggestions:</span>
                  {searchResult.suggestions.map(suggestion => (
                    <button
                      key={suggestion}
                      className="suggestion-btn"
                      onClick={() => setSearchQuery(suggestion)}
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
            </div>

            <div className={`memories-container memories-container--${viewMode}`}>
              {searchResult.memories.map(memory => (
                <MemoryCard key={memory.id} memory={memory} />
              ))}
            </div>

            {searchResult.memories.length === 0 && (
              <div className="no-results">
                <div className="no-results__icon">🔍</div>
                <div className="no-results__text">
                  No memories found for "{searchQuery}"
                </div>
                <div className="no-results__suggestions">
                  Try adjusting your search terms or filters
                </div>
              </div>
            )}
          </>
        )}

        {!searchResult && !isLoading && (
          <div className="knowledge-explorer__placeholder">
            <div className="placeholder-icon">🧠</div>
            <div className="placeholder-text">
              Search your knowledge base to explore memories and insights
            </div>
          </div>
        )}
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="knowledge-explorer__loading">
          <div className="loading-spinner"></div>
          <div className="loading-text">Searching knowledge base...</div>
        </div>
      )}
    </div>
  );
};

export default KnowledgeExplorer;
