/**
 * AutomationPage - Automation Workflow Builder Page
 * Trang chính cho automation system với workflow management
 */

import React, { useCallback, useState } from 'react';

import WorkflowEditor from './components/WorkflowEditor';
import { Workflow } from './types/workflow';

import './AutomationPage.css';
import AI from "AI";
import Add from "Add";
import Automation from "./index";
import AutomationPage from "./AutomationPage";
import Builder from "Builder";
import Check from "Check";
import Created from "Created";
import Desktop from "Desktop";
import Executing from "Executing";
import FC from "FC";
import Failed from "Failed";
import Handle from "Handle";
import Load from "Load";
import New from "New";
import Page from "Page";
import Save from "Save";
import Saved from "Saved";
import Select from "Select";
import Show from "Show";
import Trang from "Trang";
import Update from "Update";
import Updated from "Updated";
import Workflows from "Workflows";
import ZETA from "ZETA";

const AutomationPage: React.FC = () => {
  const [currentWorkflow, setCurrentWorkflow] = useState<Workflow | undefined>();
  const [savedWorkflows, setSavedWorkflows] = useState<Workflow[]>([]);

  // Handle saving workflow
  const handleSaveWorkflow = useCallback((workflow: Workflow) => {
    // Save to localStorage for now (later will be backend)
    const existingIndex = savedWorkflows.findIndex(w => w.id === workflow.id);
    
    if (existingIndex >= 0) {
      // Update existing workflow
      const updatedWorkflows = [...savedWorkflows];
      updatedWorkflows[existingIndex] = workflow;
      setSavedWorkflows(updatedWorkflows);
    } else {
      // Add new workflow
      setSavedWorkflows(prev => [...prev, workflow]);
    }

    // Update current workflow
    setCurrentWorkflow(workflow);

    // Save to localStorage
    localStorage.setItem('zeta-workflows', JSON.stringify([...savedWorkflows]));
    
    console.log('Workflow saved:', workflow);
    
    // Show success message (later implement proper notification system)
    alert('Workflow saved successfully!');
  }, [savedWorkflows]);

  // Handle executing workflow
  const handleExecuteWorkflow = useCallback((workflowId: string) => {
    console.log('Executing workflow:', workflowId);
    
    // Show success message
    alert(`Workflow ${workflowId} execution started! Check console for details.`);
  }, []);

  // Load workflows from localStorage on component mount
  React.useEffect(() => {
    const saved = localStorage.getItem('zeta-workflows');
    if (saved) {
      try {
        const workflows = JSON.parse(saved);
        setSavedWorkflows(workflows);
      } catch (error) {
        console.error('Failed to load saved workflows:', error);
      }
    }
  }, []);

  return (
    <div className="automation-page">
      <div className="automation-page__header">
        <div className="automation-page__title-section">
          <h1 className="automation-page__title">🤖 Automation Builder</h1>
          <p className="automation-page__subtitle">
            Tạo và quản lý workflows tự động cho ZETA AI Desktop
          </p>
        </div>

        <div className="automation-page__actions">
          <button
            className="btn btn--secondary"
            onClick={() => {
              const newWorkflow: Workflow = {
                id: `workflow-${Date.now()}`,
                name: 'New Workflow',
                description: 'Created with Automation Builder',
                nodes: [],
                edges: [],
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                isActive: false,
                tags: ['new'],
              };
              setCurrentWorkflow(newWorkflow);
            }}
          >
            📄 New Workflow
          </button>

          {savedWorkflows.length > 0 && (
            <select
              className="automation-page__workflow-selector"
              value={currentWorkflow?.id || ''}
              onChange={(e) => {
                const workflow = savedWorkflows.find(w => w.id === e.target.value);
                setCurrentWorkflow(workflow);
              }}
            >
              <option value="">Select Workflow...</option>
              {savedWorkflows.map(workflow => (
                <option key={workflow.id} value={workflow.id}>
                  {workflow.name}
                </option>
              ))}
            </select>
          )}
        </div>
      </div>

      <div className="automation-page__content">
        <WorkflowEditor
          workflow={currentWorkflow}
          onSave={handleSaveWorkflow}
          onExecute={handleExecuteWorkflow}
          className="automation-page__editor"
        />
      </div>

      {savedWorkflows.length > 0 && (
        <div className="automation-page__sidebar">
          <h3 className="automation-page__sidebar-title">📋 Saved Workflows</h3>
          <div className="automation-page__workflow-list">
            {savedWorkflows.map(workflow => (
              <div
                key={workflow.id}
                className={`automation-page__workflow-item ${
                  currentWorkflow?.id === workflow.id ? 'active' : ''
                }`}
                onClick={() => setCurrentWorkflow(workflow)}
              >
                <div className="automation-page__workflow-name">
                  {workflow.name}
                </div>
                <div className="automation-page__workflow-meta">
                  {workflow.nodes.length} nodes • {workflow.edges.length} connections
                </div>
                <div className="automation-page__workflow-updated">
                  Updated: {new Date(workflow.updatedAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AutomationPage;
