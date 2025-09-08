/**
 * TriggerPanel - Node Configuration Panel
 * Panel bên phải để cấu hình các node trong workflow
 */

import { zodResolver } from '@hookform/resolvers/zod';
import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { WorkflowNode } from '../types/workflow';

import './TriggerPanel.css';
import AI from "AI";
import Action from "Action";
import Advanced from "Advanced";
import Apply from "Apply";
import Assistant from "Assistant";
import Basic from "Basic";
import Body from "Body";
import CSV from "CSV";
import Cancel from "Cancel";
import Changes from "Changes";
import Close from "Close";
import Configuration from "Configuration";
import Contains from "Contains";
import Create from "Create";
import Cron from "Cron";
import Custom from "Custom";
import DELETE from "DELETE";
import Delay from "Delay";
import Delete from "Delete";
import Description from "Description";
import Duration from "Duration";
import Endpoint from "Endpoint";
import Equals from "Equals";
import Expression from "Expression";
import FC from "FC";
import File from "File";
import Format from "Format";
import GET from "GET";
import Get from "Get";
import Greater from "Greater";
import HTTP from "HTTP";
import If from "If";
import Interval from "Interval";
import Label from "Label";
import Less from "Less";
import Manual from "Manual";
import Message from "Message";
import Method from "Method";
import Milliseconds from "Milliseconds";
import Minutes from "Minutes";
import Modify from "Modify";
import No from "No";
import Node from "Node";
import Not from "Not";
import Notification from "Notification";
import Operation from "Operation";
import Operator from "Operator";
import Output from "Output";
import POST from "POST";
import PUT from "PUT";
import Panel from "Panel";
import Path from "Path";
import Pattern from "Pattern";
import Request from "Request";
import Script from "Script";
import Seconds from "Seconds";
import Text from "Text";
import Than from "Than";
import Timer from "Timer";
import Title from "Title";
import Trigger from "Trigger";
import TriggerPanel from "./TriggerPanel";
import TriggerPanelProps from "TriggerPanelProps";
import Type from "Type";
import URL from "URL";
import Unit from "Unit";
import Update from "Update";
import Validation from "Validation";
import Value from "Value";
import Variable from "Variable";
import Watch from "Watch";
import Webhook from "Webhook";

interface TriggerPanelProps {
  node: WorkflowNode;
  onUpdateNode: (node: WorkflowNode) => void;
  onClose: () => void;
  className?: string;
}

// Validation schemas for different node types
const triggerConfigSchema = z.object({
  type: z.enum(['timer', 'file', 'manual', 'webhook']),
  interval: z.number().optional(),
  cron: z.string().optional(),
  path: z.string().optional(),
  pattern: z.string().optional(),
  action: z.enum(['create', 'modify', 'delete']).optional(),
  endpoint: z.string().optional(),
  method: z.enum(['GET', 'POST', 'PUT', 'DELETE']).optional(),
});

const actionConfigSchema = z.object({
  type: z.enum(['http', 'file', 'notification', 'script', 'ai']),
  url: z.string().optional(),
  method: z.string().optional(),
  headers: z.record(z.string()).optional(),
  body: z.string().optional(),
  path: z.string().optional(),
  content: z.string().optional(),
  operation: z.enum(['create', 'read', 'update', 'delete']).optional(),
  title: z.string().optional(),
  message: z.string().optional(),
  code: z.string().optional(),
  language: z.enum(['javascript', 'python', 'bash']).optional(),
  prompt: z.string().optional(),
  model: z.string().optional(),
  temperature: z.number().min(0).max(2).optional(),
});

const conditionConfigSchema = z.object({
  operator: z.enum(['equals', 'not_equals', 'greater_than', 'less_than', 'contains']),
  value: z.string(),
  variable: z.string(),
});

const delayConfigSchema = z.object({
  duration: z.number().min(100).max(300000), // 100ms to 5 minutes
  unit: z.enum(['milliseconds', 'seconds', 'minutes']).default('milliseconds'),
});

const outputConfigSchema = z.object({
  format: z.enum(['json', 'text', 'csv']),
  destination: z.enum(['console', 'file', 'webhook']).optional(),
  path: z.string().optional(),
  url: z.string().optional(),
});

const TriggerPanel: React.FC<TriggerPanelProps> = ({
  node,
  onUpdateNode,
  onClose,
  className = '',
}) => {
  const [activeTab, setActiveTab] = useState<'basic' | 'advanced'>('basic');

  // Get schema based on node type
  const getSchema = (nodeType: string) => {
    switch (nodeType) {
      case 'trigger':
        return triggerConfigSchema;
      case 'action':
        return actionConfigSchema;
      case 'condition':
        return conditionConfigSchema;
      case 'delay':
        return delayConfigSchema;
      case 'output':
        return outputConfigSchema;
      default:
        return z.object({});
    }
  };

  const schema = getSchema(node.type);
  
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isDirty },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues: node.data.config,
  });

  const watchedType = watch('type');

  // Update form when node changes
  useEffect(() => {
    Object.entries(node.data.config).forEach(([key, value]) => {
      setValue(key as any, value);
    });
  }, [node.data.config, setValue]);

  const onSubmit = (data: any) => {
    const updatedNode: WorkflowNode = {
      ...node,
      data: {
        ...node.data,
        config: data,
        label: generateNodeLabel(node.type, data),
      },
    };
    onUpdateNode(updatedNode);
  };

  const generateNodeLabel = (nodeType: string, config: any): string => {
    switch (nodeType) {
      case 'trigger':
        return `Trigger: ${config.type || 'manual'}`;
      case 'action':
        return `Action: ${config.type || 'http'}`;
      case 'condition':
        return `If ${config.variable || 'value'} ${config.operator || 'equals'} ${config.value || ''}`;
      case 'delay':
        return `Delay: ${config.duration || 1000}${config.unit === 'seconds' ? 's' : config.unit === 'minutes' ? 'm' : 'ms'}`;
      case 'output':
        return `Output: ${config.format || 'json'}`;
      default:
        return node.data.label;
    }
  };

  const renderTriggerConfig = () => (
    <div className="trigger-panel__config-section">
      <div className="form-group">
        <label className="form-label">Trigger Type</label>
        <select {...register('type')} className="form-select">
          <option value="manual">Manual</option>
          <option value="timer">Timer</option>
          <option value="file">File Watch</option>
          <option value="webhook">Webhook</option>
        </select>
        {errors.type && <span className="form-error">{errors.type.message}</span>}
      </div>

      {watchedType === 'timer' && (
        <>
          <div className="form-group">
            <label className="form-label">Interval (ms)</label>
            <input
              type="number"
              {...register('interval', { valueAsNumber: true })}
              className="form-input"
              placeholder="5000"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Cron Expression (optional)</label>
            <input
              type="text"
              {...register('cron')}
              className="form-input"
              placeholder="0 */5 * * * *"
            />
          </div>
        </>
      )}

      {watchedType === 'file' && (
        <>
          <div className="form-group">
            <label className="form-label">Watch Path</label>
            <input
              type="text"
              {...register('path')}
              className="form-input"
              placeholder="/path/to/watch"
            />
          </div>
          <div className="form-group">
            <label className="form-label">File Pattern</label>
            <input
              type="text"
              {...register('pattern')}
              className="form-input"
              placeholder="*.txt"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Action</label>
            <select {...register('action')} className="form-select">
              <option value="create">Create</option>
              <option value="modify">Modify</option>
              <option value="delete">Delete</option>
            </select>
          </div>
        </>
      )}

      {watchedType === 'webhook' && (
        <>
          <div className="form-group">
            <label className="form-label">Endpoint</label>
            <input
              type="text"
              {...register('endpoint')}
              className="form-input"
              placeholder="/api/webhook"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Method</label>
            <select {...register('method')} className="form-select">
              <option value="POST">POST</option>
              <option value="GET">GET</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
            </select>
          </div>
        </>
      )}
    </div>
  );

  const renderActionConfig = () => (
    <div className="trigger-panel__config-section">
      <div className="form-group">
        <label className="form-label">Action Type</label>
        <select {...register('type')} className="form-select">
          <option value="http">HTTP Request</option>
          <option value="file">File Operation</option>
          <option value="notification">Notification</option>
          <option value="script">Script</option>
          <option value="ai">AI Assistant</option>
        </select>
      </div>

      {watchedType === 'http' && (
        <>
          <div className="form-group">
            <label className="form-label">URL</label>
            <input
              type="url"
              {...register('url')}
              className="form-input"
              placeholder="https://api.example.com/endpoint"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Method</label>
            <select {...register('method')} className="form-select">
              <option value="GET">GET</option>
              <option value="POST">POST</option>
              <option value="PUT">PUT</option>
              <option value="DELETE">DELETE</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Request Body</label>
            <textarea
              {...register('body')}
              className="form-textarea"
              placeholder='{"key": "value"}'
              rows={4}
            />
          </div>
        </>
      )}

      {watchedType === 'notification' && (
        <>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input
              type="text"
              {...register('title')}
              className="form-input"
              placeholder="Notification Title"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Message</label>
            <textarea
              {...register('message')}
              className="form-textarea"
              placeholder="Notification message"
              rows={3}
            />
          </div>
        </>
      )}
    </div>
  );

  const renderBasicConfig = () => {
    switch (node.type) {
      case 'trigger':
        return renderTriggerConfig();
      case 'action':
        return renderActionConfig();
      case 'condition':
        return (
          <div className="trigger-panel__config-section">
            <div className="form-group">
              <label className="form-label">Variable</label>
              <input
                type="text"
                {...register('variable')}
                className="form-input"
                placeholder="variable_name"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Operator</label>
              <select {...register('operator')} className="form-select">
                <option value="equals">Equals</option>
                <option value="not_equals">Not Equals</option>
                <option value="greater_than">Greater Than</option>
                <option value="less_than">Less Than</option>
                <option value="contains">Contains</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Value</label>
              <input
                type="text"
                {...register('value')}
                className="form-input"
                placeholder="comparison_value"
              />
            </div>
          </div>
        );
      case 'delay':
        return (
          <div className="trigger-panel__config-section">
            <div className="form-group">
              <label className="form-label">Duration</label>
              <input
                type="number"
                {...register('duration', { valueAsNumber: true })}
                className="form-input"
                placeholder="1000"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Unit</label>
              <select {...register('unit')} className="form-select">
                <option value="milliseconds">Milliseconds</option>
                <option value="seconds">Seconds</option>
                <option value="minutes">Minutes</option>
              </select>
            </div>
          </div>
        );
      case 'output':
        return (
          <div className="trigger-panel__config-section">
            <div className="form-group">
              <label className="form-label">Format</label>
              <select {...register('format')} className="form-select">
                <option value="json">JSON</option>
                <option value="text">Text</option>
                <option value="csv">CSV</option>
              </select>
            </div>
          </div>
        );
      default:
        return <div>No configuration available for this node type.</div>;
    }
  };

  return (
    <div className={`trigger-panel ${className}`}>
      <div className="trigger-panel__header">
        <h3 className="trigger-panel__title">
          {node.data.label || `${node.type} Node`}
        </h3>
        <button
          type="button"
          onClick={onClose}
          className="trigger-panel__close"
          aria-label="Close panel"
        >
          ✕
        </button>
      </div>

      <div className="trigger-panel__tabs">
        <button
          type="button"
          className={`trigger-panel__tab ${activeTab === 'basic' ? 'active' : ''}`}
          onClick={() => setActiveTab('basic')}
        >
          Basic
        </button>
        <button
          type="button"
          className={`trigger-panel__tab ${activeTab === 'advanced' ? 'active' : ''}`}
          onClick={() => setActiveTab('advanced')}
        >
          Advanced
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="trigger-panel__form">
        <div className="trigger-panel__content">
          {activeTab === 'basic' && renderBasicConfig()}
          
          {activeTab === 'advanced' && (
            <div className="trigger-panel__config-section">
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  value={node.data.description || ''}
                  onChange={(e) => {
                    const updatedNode = {
                      ...node,
                      data: {
                        ...node.data,
                        description: e.target.value,
                      },
                    };
                    onUpdateNode(updatedNode);
                  }}
                  className="form-textarea"
                  placeholder="Node description..."
                  rows={3}
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Custom Label</label>
                <input
                  type="text"
                  value={node.data.label || ''}
                  onChange={(e) => {
                    const updatedNode = {
                      ...node,
                      data: {
                        ...node.data,
                        label: e.target.value,
                      },
                    };
                    onUpdateNode(updatedNode);
                  }}
                  className="form-input"
                  placeholder="Custom node label"
                />
              </div>
            </div>
          )}
        </div>

        <div className="trigger-panel__footer">
          <button
            type="submit"
            className="btn btn--primary"
            disabled={!isDirty}
          >
            💾 Apply Changes
          </button>
          <button
            type="button"
            onClick={onClose}
            className="btn btn--secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TriggerPanel;
