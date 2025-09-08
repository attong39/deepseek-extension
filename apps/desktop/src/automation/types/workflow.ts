import AI from "AI";
import ActionConfig from "ActionConfig";
import Automation from "../index";
import Builder from "Builder";
import DELETE from "DELETE";
import File from "File";
import GET from "GET";
import HTTP from "HTTP";
import NodeType from "NodeType";
import Notification from "Notification";
import Omit from "Omit";
import POST from "POST";
import PUT from "PUT";
import Record from "Record";
import Schema from "Schema";
import Script from "Script";
import Timer from "Timer";
import TriggerConfig from "TriggerConfig";
import Types from "../../Types/index";
import URL from "URL";
import Webhook from "Webhook";
import Workflow from "./Workflow";
import WorkflowEdge from "WorkflowEdge";
import WorkflowExecution from "WorkflowExecution";
import WorkflowLog from "WorkflowLog";
import WorkflowNode from "WorkflowNode";
import WorkflowTemplate from "WorkflowTemplate";
import ZETA from "ZETA";
/**
 * Workflow Types - ZETA Automation Builder
 * Định nghĩa types cho hệ thống automation workflow
 */

export interface WorkflowNode {
  id: string;
  type: 'trigger' | 'action' | 'condition' | 'delay' | 'output';
  position: { x: number; y: number };
  data: {
    label: string;
    config: Record<string, any>;
    description?: string;
  };
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type?: string;
  animated?: boolean;
  label?: string;
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  createdAt: string;
  updatedAt: string;
  isActive: boolean;
  tags: string[];
}

export interface WorkflowTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  workflow: Omit<Workflow, 'id' | 'createdAt' | 'updatedAt'>;
  preview: string; // URL hoặc base64 image
}

export interface TriggerConfig {
  type: 'timer' | 'file' | 'manual' | 'webhook';
  config: {
    // Timer trigger
    interval?: number;
    cron?: string;
    
    // File trigger  
    path?: string;
    pattern?: string;
    action?: 'create' | 'modify' | 'delete';
    
    // Webhook trigger
    endpoint?: string;
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  };
}

export interface ActionConfig {
  type: 'http' | 'file' | 'notification' | 'script' | 'ai';
  config: {
    // HTTP action
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    body?: string;
    
    // File action
    path?: string;
    content?: string;
    operation?: 'create' | 'read' | 'update' | 'delete';
    
    // Notification action
    title?: string;
    message?: string;
    type?: 'info' | 'success' | 'warning' | 'error';
    
    // Script action
    code?: string;
    language?: 'javascript' | 'python' | 'bash';
    
    // AI action
    prompt?: string;
    model?: string;
    temperature?: number;
  };
}

export interface WorkflowExecution {
  id: string;
  workflowId: string;
  status: 'running' | 'completed' | 'failed' | 'cancelled';
  startedAt: string;
  completedAt?: string;
  error?: string;
  logs: WorkflowLog[];
}

export interface WorkflowLog {
  timestamp: string;
  nodeId: string;
  level: 'info' | 'warn' | 'error';
  message: string;
  data?: any;
}

export interface NodeType {
  type: string;
  label: string;
  description: string;
  icon: string;
  category: 'trigger' | 'action' | 'condition' | 'utility';
  configSchema: any; // JSON Schema for configuration
  defaultConfig: Record<string, any>;
}
