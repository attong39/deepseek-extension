/**
 * WorkflowEditor - Visual Workflow Builder
 * Thành phần chính để tạo và chỉnh sửa workflows bằng React Flow
 */

import {
    addEdge,
    Background,
    BackgroundVariant,
    Connection,
    Controls,
    Edge,
    MiniMap,
    Node,
    ReactFlow,
    useEdgesState,
    useNodesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import React, { useCallback, useMemo, useState } from 'react';

import NodeLibrary from './NodeLibrary';
import TriggerPanel from './TriggerPanel';
import { useWorkflowEngine } from '../hooks/useWorkflowEngine';
import { Workflow, WorkflowEdge, WorkflowNode } from '../types/workflow';

import './WorkflowEditor.css';
import ActionNode from "ActionNode";
import Builder from "Builder";
import Canvas from "Canvas";
import Check from "Check";
import ConditionNode from "ConditionNode";
import DelayNode from "DelayNode";
import Dots from "Dots";
import DragEvent from "DragEvent";
import Element from "Element";
import Errors from "Errors";
import Execute from "Execute";
import Executing from "Executing";
import FC from "FC";
import Flow from "Flow";
import Handle from "Handle";
import Header from "Header";
import Library from "Library";
import Main from "../../Main";
import MouseEvent from "MouseEvent";
import New from "New";
import OutputNode from "OutputNode";
import Please from "Please";
import Save from "Save";
import Sidebar from "../../components/nav/Sidebar";
import TriggerNode from "TriggerNode";
import Untitled from "Untitled";
import Validation from "Validation";
import Visual from "Visual";
import WorkflowEditor from "./WorkflowEditor";
import WorkflowEditorProps from "WorkflowEditorProps";

interface WorkflowEditorProps {
  workflow?: Workflow;
  onSave: (workflow: Workflow) => void;
  onExecute: (workflowId: string) => void;
  className?: string;
}

const nodeTypes = {
  trigger: React.lazy(() => import('./nodes/TriggerNode')),
  action: React.lazy(() => import('./nodes/ActionNode')),
  condition: React.lazy(() => import('./nodes/ConditionNode')),
  delay: React.lazy(() => import('./nodes/DelayNode')),
  output: React.lazy(() => import('./nodes/OutputNode')),
};

const WorkflowEditor: React.FC<WorkflowEditorProps> = ({
  workflow,
  onSave,
  onExecute,
  className = '',
}) => {
  const [nodes, setNodes, onNodesChange] = useNodesState(
    workflow?.nodes as Node[] || []
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(
    workflow?.edges as Edge[] || []
  );
  
  const [selectedNode, setSelectedNode] = useState<WorkflowNode | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  
  const { executeWorkflow, validateWorkflow } = useWorkflowEngine();

  // Handle new connections between nodes
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  // Handle node selection
  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNode(node as WorkflowNode);
  }, []);

  // Handle drag & drop from node library
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const type = event.dataTransfer.getData('application/reactflow');
      if (!type) return;

      const reactFlowBounds = (event.target as Element)
        .closest('.react-flow')
        ?.getBoundingClientRect();
      
      if (!reactFlowBounds) return;

      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      const newNode: WorkflowNode = {
        id: `${type}-${Date.now()}`,
        type: type as WorkflowNode['type'],
        position,
        data: {
          label: `${type.charAt(0).toUpperCase() + type.slice(1)} Node`,
          config: {},
          description: `New ${type} node`,
        },
      };

      setNodes((nds) => nds.concat(newNode as Node));
    },
    [setNodes]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // Save workflow
  const handleSave = useCallback(() => {
    const workflowData: Workflow = {
      id: workflow?.id || `workflow-${Date.now()}`,
      name: workflow?.name || 'Untitled Workflow',
      description: workflow?.description || '',
      nodes: nodes as WorkflowNode[],
      edges: edges as WorkflowEdge[],
      createdAt: workflow?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      isActive: workflow?.isActive || false,
      tags: workflow?.tags || [],
    };

    onSave(workflowData);
  }, [workflow, nodes, edges, onSave]);

  // Execute workflow
  const handleExecute = useCallback(async () => {
    if (!workflow?.id) {
      alert('Please save the workflow first');
      return;
    }

    const validation = validateWorkflow({
      ...workflow,
      nodes: nodes as WorkflowNode[],
      edges: edges as WorkflowEdge[],
    });

    if (!validation.isValid) {
      alert(`Workflow validation failed: ${validation.errors.join(', ')}`);
      return;
    }

    setIsExecuting(true);
    try {
      await executeWorkflow(workflow.id);
      onExecute(workflow.id);
    } catch (error) {
      console.error('Workflow execution failed:', error);
      alert('Workflow execution failed. Check console for details.');
    } finally {
      setIsExecuting(false);
    }
  }, [workflow, nodes, edges, validateWorkflow, executeWorkflow, onExecute]);

  // Validation messages
  const validationResult = useMemo(() => {
    if (nodes.length === 0) return null;
    
    return validateWorkflow({
      id: 'temp',
      name: 'temp',
      description: '',
      nodes: nodes as WorkflowNode[],
      edges: edges as WorkflowEdge[],
      createdAt: '',
      updatedAt: '',
      isActive: false,
      tags: [],
    });
  }, [nodes, edges, validateWorkflow]);

  return (
    <div className={`workflow-editor ${className}`}>
      {/* Header toolbar */}
      <div className="workflow-editor__toolbar">
        <h2 className="workflow-editor__title">
          {workflow?.name || 'New Workflow'}
        </h2>
        
        <div className="workflow-editor__actions">
          <button
            onClick={handleSave}
            className="btn btn--primary"
            disabled={nodes.length === 0}
          >
            💾 Save Workflow
          </button>
          
          <button
            onClick={handleExecute}
            className="btn btn--success"
            disabled={!workflow?.id || nodes.length === 0 || isExecuting}
          >
            {isExecuting ? '⏳ Executing...' : '▶️ Execute'}
          </button>
        </div>
      </div>

      {/* Validation status */}
      {validationResult && !validationResult.isValid && (
        <div className="workflow-editor__validation-errors">
          <h4>⚠️ Validation Errors:</h4>
          <ul>
            {validationResult.errors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="workflow-editor__content">
        {/* Node Library Sidebar */}
        <div className="workflow-editor__sidebar">
          <NodeLibrary />
          
          {selectedNode && (
            <TriggerPanel
              node={selectedNode}
              onUpdateNode={(updatedNode) => {
                setNodes((nds) =>
                  nds.map((n) =>
                    n.id === updatedNode.id ? updatedNode as Node : n
                  )
                );
                setSelectedNode(updatedNode);
              }}
              onClose={() => setSelectedNode(null)}
            />
          )}
        </div>

        {/* Main Canvas */}
        <div className="workflow-editor__canvas">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            onDrop={onDrop}
            onDragOver={onDragOver}
            nodeTypes={nodeTypes}
            fitView
            proOptions={{
              hideAttribution: true,
            }}
          >
            <Controls showInteractive={false} />
            <MiniMap />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
};

export default WorkflowEditor;
