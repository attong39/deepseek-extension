/**
 * MemoryPage - Main Memory Management Page
 * Container cho Memory Management features
 */

import React, { useCallback, useState } from 'react';

import KnowledgeExplorer from './components/KnowledgeExplorer';
import { useMemoryAPI } from './hooks/useMemoryAPI';
import { Memory } from './types/memory';

import './MemoryPage.css';
import AI from "AI";
import Access from "Access";
import Accessed from "Accessed";
import Analytics from "../Analytics/index";
import Auto from "Auto";
import Avg from "Avg";
import Cleanup from "Cleanup";
import Container from "Container";
import Content from "Content";
import Context from "../Context/index";
import Created from "Created";
import Delete from "Delete";
import Detail from "Detail";
import Detailed from "Detailed";
import Details from "Details";
import Display from "Display";
import Edit from "Edit";
import Error from "Error";
import Explore from "Explore";
import Export from "Export";
import FC from "FC";
import Handle from "Handle";
import Import from "Import";
import Importance from "Importance";
import Knowledge from "Knowledge";
import MB from "MB";
import Main from "../Main";
import Management from "Management";
import Math from "Math";
import Memories from "Memories";
import MemoryPage from "./MemoryPage";
import Navigation from "../components/Navigation";
import Overview from "Overview";
import Page from "Page";
import Phase from "Phase";
import Planned from "Planned";
import Quick from "Quick";
import Rate from "Rate";
import Settings from "../pages/Settings";
import Share from "Share";
import Sidebar from "../components/nav/Sidebar";
import Stats from "Stats";
import Storage from "Storage";
import Tab from "Tab";
import Tags from "Tags";
import Top from "Top";
import Total from "Total";
import Type from "Type";
import Types from "./Types/index";
import Used from "Used";
import Week from "Week";
import ZETA from "ZETA";

const MemoryPage: React.FC = () => {
  const { metrics, error } = useMemoryAPI();
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null);
  const [activeTab, setActiveTab] = useState<'explore' | 'analytics' | 'settings'>('explore');

  // Handle memory selection
  const handleMemorySelect = useCallback((memory: Memory) => {
    setSelectedMemory(memory);
  }, []);

  // Handle memory actions
  const handleCloseMemoryDetail = useCallback(() => {
    setSelectedMemory(null);
  }, []);

  return (
    <div className="memory-page">
      <div className="memory-page__header">
        <div className="memory-page__title-section">
          <h1 className="memory-page__title">🧠 Memory Management</h1>
          <p className="memory-page__subtitle">
            Explore và quản lý knowledge base của ZETA AI
          </p>
        </div>

        {/* Quick Stats */}
        {metrics && (
          <div className="memory-page__stats">
            <div className="stat-card">
              <div className="stat-card__value">{metrics.total_memories.toLocaleString()}</div>
              <div className="stat-card__label">Total Memories</div>
            </div>
            <div className="stat-card">
              <div className="stat-card__value">{metrics.storage_usage_mb.toFixed(1)} MB</div>
              <div className="stat-card__label">Storage Used</div>
            </div>
            <div className="stat-card">
              <div className="stat-card__value">{Math.round(metrics.avg_access_frequency * 100)}%</div>
              <div className="stat-card__label">Avg Access Rate</div>
            </div>
          </div>
        )}
      </div>

      {/* Tab Navigation */}
      <div className="memory-page__tabs">
        <button 
          className={`tab-button ${activeTab === 'explore' ? 'active' : ''}`}
          onClick={() => setActiveTab('explore')}
        >
          🔍 Explore Knowledge
        </button>
        <button 
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📊 Analytics
        </button>
        <button 
          className={`tab-button ${activeTab === 'settings' ? 'active' : ''}`}
          onClick={() => setActiveTab('settings')}
        >
          ⚙️ Settings
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="memory-page__error">
          ⚠️ {error}
        </div>
      )}

      {/* Main Content */}
      <div className="memory-page__content">
        {activeTab === 'explore' && (
          <div className="memory-page__explore">
            <KnowledgeExplorer 
              className="memory-page__knowledge-explorer"
              onMemorySelect={handleMemorySelect}
            />
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="memory-page__analytics">
            <div className="analytics-placeholder">
              <div className="placeholder-icon">📈</div>
              <div className="placeholder-title">Memory Analytics</div>
              <div className="placeholder-subtitle">
                Detailed analytics và insights sẽ được implement trong Phase 3 Week 2
              </div>
              
              {metrics && (
                <div className="analytics-preview">
                  <h3>Quick Overview:</h3>
                  <div className="metrics-grid">
                    <div className="metric-item">
                      <strong>Memory Types:</strong>
                      <ul>
                        {Object.entries(metrics.memories_by_type).map(([type, count]) => (
                          <li key={type}>{type}: {count}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="metric-item">
                      <strong>Top Tags:</strong>
                      <ul>
                        {metrics.top_tags.slice(0, 5).map(({ tag, count }) => (
                          <li key={tag}>#{tag}: {count}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'settings' && (
          <div className="memory-page__settings">
            <div className="settings-placeholder">
              <div className="placeholder-icon">⚙️</div>
              <div className="placeholder-title">Memory Settings</div>
              <div className="placeholder-subtitle">
                Memory optimization và retention settings sẽ được implement trong Phase 3 Week 2
              </div>
              
              <div className="settings-preview">
                <h3>Planned Settings:</h3>
                <ul>
                  <li>🗄️ Memory retention policies</li>
                  <li>🔄 Auto-compression settings</li>
                  <li>🎯 Importance thresholds</li>
                  <li>📤 Export/Import options</li>
                  <li>🧹 Cleanup utilities</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Memory Detail Sidebar */}
      {selectedMemory && (
        <div className="memory-page__detail-sidebar">
          <div className="memory-detail">
            <div className="memory-detail__header">
              <h3>Memory Details</h3>
              <button 
                className="close-button"
                onClick={handleCloseMemoryDetail}
              >
                ×
              </button>
            </div>

            <div className="memory-detail__content">
              <div className="memory-detail__meta">
                <div className="meta-item">
                  <strong>Type:</strong> 
                  <span className={`type-badge type-badge--${selectedMemory.type}`}>
                    {selectedMemory.type}
                  </span>
                </div>
                <div className="meta-item">
                  <strong>Importance:</strong>
                  <span className={`importance-badge importance-badge--${selectedMemory.importance}`}>
                    {selectedMemory.importance}
                  </span>
                </div>
                <div className="meta-item">
                  <strong>Created:</strong> 
                  {new Date(selectedMemory.created_at).toLocaleString()}
                </div>
                <div className="meta-item">
                  <strong>Accessed:</strong> {selectedMemory.metrics.access_count} times
                </div>
              </div>

              <div className="memory-detail__content-section">
                <strong>Content:</strong>
                <div className="content-text">
                  {selectedMemory.content}
                </div>
              </div>

              {selectedMemory.tags.length > 0 && (
                <div className="memory-detail__tags">
                  <strong>Tags:</strong>
                  <div className="tag-list">
                    {selectedMemory.tags.map(tag => (
                      <span key={tag} className="tag">#{tag}</span>
                    ))}
                  </div>
                </div>
              )}

              {Object.keys(selectedMemory.context).length > 0 && (
                <div className="memory-detail__context">
                  <strong>Context:</strong>
                  <pre className="context-data">
                    {JSON.stringify(selectedMemory.context, null, 2)}
                  </pre>
                </div>
              )}
            </div>

            <div className="memory-detail__actions">
              <button className="action-button action-button--edit">
                ✏️ Edit
              </button>
              <button className="action-button action-button--share">
                🔗 Share
              </button>
              <button className="action-button action-button--delete">
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MemoryPage;
