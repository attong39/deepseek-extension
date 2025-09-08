/**
 * useWorkflowEngine - Workflow Execution Engine Hook
 * Hook quản lý thực thi và validation workflows
 */

import { useCallback, useState } from 'react';

import { Workflow, WorkflowExecution, WorkflowLog } from '../types/workflow';
import Action from "Action";
import Already from "Already";
import Cancel from "Cancel";
import Check from "Check";
import Checking from "Checking";
import Circular from "Circular";
import Condition from "Condition";
import DFS from "DFS";
import Delay from "Delay";
import Engine from "Engine";
import Error from "Error";
import Execute from "Execute";
import Executing from "Executing";
import Execution from "Execution";
import File from "File";
import Finalizing from "Finalizing";
import Get from "Get";
import HTTP from "HTTP";
import Hook from "Hook";
import ID from "ID";
import Initializing from "Initializing";
import Methods from "Methods";
import Processing from "Processing";
import Record from "Record";
import Set from "Set";
import Simulate from "Simulate";
import State from "State";
import Timer from "Timer";
import Trigger from "Trigger";
import URL from "URL";
import Unknown from "Unknown";
import Validate from "Validate";
import ValidationResult from "ValidationResult";
import WorkflowEngineState from "WorkflowEngineState";

interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

interface WorkflowEngineState {
  executions: Record<string, WorkflowExecution>;
  isExecuting: boolean;
}

export const useWorkflowEngine = () => {
  const [state, setState] = useState<WorkflowEngineState>({
    executions: {},
    isExecuting: false,
  });

  // Validate workflow structure
  const validateWorkflow = useCallback((workflow: Workflow): ValidationResult => {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check if workflow has nodes
    if (workflow.nodes.length === 0) {
      errors.push('Workflow must have at least one node');
    }

    // Check for trigger nodes
    const triggerNodes = workflow.nodes.filter(node => node.type === 'trigger');
    if (triggerNodes.length === 0) {
      errors.push('Workflow must have at least one trigger node');
    }

    // Check for disconnected nodes
    const connectedNodeIds = new Set<string>();
    workflow.edges.forEach(edge => {
      connectedNodeIds.add(edge.source);
      connectedNodeIds.add(edge.target);
    });

    const disconnectedNodes = workflow.nodes.filter(
      node => !connectedNodeIds.has(node.id) && workflow.nodes.length > 1
    );
    
    if (disconnectedNodes.length > 0) {
      warnings.push(`${disconnectedNodes.length} disconnected nodes found`);
    }

    // Check for circular dependencies
    const hasCircularDependency = checkCircularDependency(workflow);
    if (hasCircularDependency) {
      errors.push('Workflow contains circular dependencies');
    }

    // Validate node configurations
    workflow.nodes.forEach(node => {
      const nodeErrors = validateNodeConfig(node);
      errors.push(...nodeErrors);
    });

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    };
  }, []);

  // Check for circular dependencies using DFS
  const checkCircularDependency = (workflow: Workflow): boolean => {
    const visited = new Set<string>();
    const recursionStack = new Set<string>();

    const dfs = (nodeId: string): boolean => {
      if (recursionStack.has(nodeId)) {
        return true; // Circular dependency found
      }
      if (visited.has(nodeId)) {
        return false; // Already processed
      }

      visited.add(nodeId);
      recursionStack.add(nodeId);

      // Check all outgoing edges
      const outgoingEdges = workflow.edges.filter(edge => edge.source === nodeId);
      for (const edge of outgoingEdges) {
        if (dfs(edge.target)) {
          return true;
        }
      }

      recursionStack.delete(nodeId);
      return false;
    };

    for (const node of workflow.nodes) {
      if (!visited.has(node.id)) {
        if (dfs(node.id)) {
          return true;
        }
      }
    }

    return false;
  };

  // Validate individual node configuration
  const validateNodeConfig = (node: any): string[] => {
    const errors: string[] = [];

    switch (node.type) {
      case 'trigger':
        if (!node.data.config.type) {
          errors.push(`Trigger node ${node.id}: type is required`);
        }
        if (node.data.config.type === 'timer' && !node.data.config.interval && !node.data.config.cron) {
          errors.push(`Timer trigger ${node.id}: interval or cron expression required`);
        }
        if (node.data.config.type === 'file' && !node.data.config.path) {
          errors.push(`File trigger ${node.id}: path is required`);
        }
        break;

      case 'action':
        if (!node.data.config.type) {
          errors.push(`Action node ${node.id}: type is required`);
        }
        if (node.data.config.type === 'http' && !node.data.config.url) {
          errors.push(`HTTP action ${node.id}: URL is required`);
        }
        break;

      case 'condition':
        if (!node.data.config.variable || !node.data.config.operator || node.data.config.value === undefined) {
          errors.push(`Condition node ${node.id}: variable, operator, and value are required`);
        }
        break;

      case 'delay':
        if (!node.data.config.duration || node.data.config.duration < 0) {
          errors.push(`Delay node ${node.id}: valid duration is required`);
        }
        break;
    }

    return errors;
  };

  // Execute workflow
  const executeWorkflow = useCallback(async (workflowId: string): Promise<string> => {
    setState(prev => ({ ...prev, isExecuting: true }));

    const executionId = `exec-${workflowId}-${Date.now()}`;
    const execution: WorkflowExecution = {
      id: executionId,
      workflowId,
      status: 'running',
      startedAt: new Date().toISOString(),
      logs: [],
    };

    setState(prev => ({
      ...prev,
      executions: {
        ...prev.executions,
        [executionId]: execution,
      },
    }));

    try {
      // Simulate workflow execution
      await simulateWorkflowExecution(executionId);
      
      setState(prev => ({
        ...prev,
        executions: {
          ...prev.executions,
          [executionId]: {
            ...prev.executions[executionId],
            status: 'completed',
            completedAt: new Date().toISOString(),
          },
        },
        isExecuting: false,
      }));

      return executionId;
    } catch (error) {
      setState(prev => ({
        ...prev,
        executions: {
          ...prev.executions,
          [executionId]: {
            ...prev.executions[executionId],
            status: 'failed',
            completedAt: new Date().toISOString(),
            error: error instanceof Error ? error.message : 'Unknown error',
          },
        },
        isExecuting: false,
      }));

      throw error;
    }
  }, []);

  // Simulate workflow execution (for demo purposes)
  const simulateWorkflowExecution = async (executionId: string): Promise<void> => {
    const steps = [
      'Initializing workflow...',
      'Processing trigger node...',
      'Executing action nodes...',
      'Checking conditions...',
      'Finalizing execution...',
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const log: WorkflowLog = {
        timestamp: new Date().toISOString(),
        nodeId: `node-${i}`,
        level: 'info',
        message: steps[i],
      };

      setState(prev => ({
        ...prev,
        executions: {
          ...prev.executions,
          [executionId]: {
            ...prev.executions[executionId],
            logs: [...prev.executions[executionId].logs, log],
          },
        },
      }));
    }
  };

  // Get execution by ID
  const getExecution = useCallback((executionId: string): WorkflowExecution | undefined => {
    return state.executions[executionId];
  }, [state.executions]);

  // Get all executions for a workflow
  const getWorkflowExecutions = useCallback((workflowId: string): WorkflowExecution[] => {
    return Object.values(state.executions).filter(exec => exec.workflowId === workflowId);
  }, [state.executions]);

  // Cancel execution
  const cancelExecution = useCallback((executionId: string): void => {
    setState(prev => ({
      ...prev,
      executions: {
        ...prev.executions,
        [executionId]: {
          ...prev.executions[executionId],
          status: 'cancelled',
          completedAt: new Date().toISOString(),
        },
      },
    }));
  }, []);

  return {
    // State
    isExecuting: state.isExecuting,
    executions: state.executions,

    // Methods
    validateWorkflow,
    executeWorkflow,
    getExecution,
    getWorkflowExecutions,
    cancelExecution,
  };
};
