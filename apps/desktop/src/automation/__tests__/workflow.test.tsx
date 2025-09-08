/**
 * Workflow Tests - ZETA Automation Builder
 * Basic test suite cho automation workflow components
 */

import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import NodeLibrary from '../components/NodeLibrary';
import { useWorkflowEngine } from '../hooks/useWorkflowEngine';
import Action from "Action";
import Actions from "Actions";
import Automation from "../index";
import Background from "Background";
import BackgroundVariant from "BackgroundVariant";
import Basic from "Basic";
import Builder from "Builder";
import Condition from "Condition";
import Conditions from "Conditions";
import Controls from "Controls";
import Delay from "Delay";
import Dots from "Dots";
import Drag from "Drag";
import Flow from "Flow";
import Hook from "Hook";
import Just from "Just";
import Library from "Library";
import MiniMap from "MiniMap";
import Mock from "Mock";
import Node from "Node";
import Output from "Output";
import ReactFlow from "ReactFlow";
import Tests from "../../Tests/index";
import Trigger from "Trigger";
import Triggers from "Triggers";
import Utilities from "Utilities";
import Workflow from "Workflow";
import ZETA from "ZETA";

// Mock React Flow
vi.mock('@xyflow/react', () => ({
  ReactFlow: ({ children, ...props }: any) => (
    <div data-testid="react-flow" {...props}>
      {children}
    </div>
  ),
  Controls: () => <div data-testid="react-flow-controls" />,
  MiniMap: () => <div data-testid="react-flow-minimap" />,
  Background: () => <div data-testid="react-flow-background" />,
  BackgroundVariant: { Dots: 'dots' },
  useNodesState: () => [[], vi.fn(), vi.fn()],
  useEdgesState: () => [[], vi.fn(), vi.fn()],
  addEdge: vi.fn(),
}));

// Mock workflow engine
vi.mock('../hooks/useWorkflowEngine');

describe('NodeLibrary', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders node library with title', () => {
    render(<NodeLibrary />);
    
    expect(screen.getByText('Node Library')).toBeInTheDocument();
    expect(screen.getByText('Drag nodes to canvas để tạo workflow')).toBeInTheDocument();
  });

  it('shows all node categories', () => {
    render(<NodeLibrary />);
    
    expect(screen.getByText('🚀 Triggers')).toBeInTheDocument();
    expect(screen.getByText('⚡ Actions')).toBeInTheDocument();
    expect(screen.getByText('🔀 Conditions')).toBeInTheDocument();
    expect(screen.getByText('🔧 Utilities')).toBeInTheDocument();
  });

  it('renders individual nodes', () => {
    render(<NodeLibrary />);
    
    expect(screen.getByText('Trigger')).toBeInTheDocument();
    expect(screen.getByText('Action')).toBeInTheDocument();
    expect(screen.getByText('Condition')).toBeInTheDocument();
    expect(screen.getByText('Delay')).toBeInTheDocument();
    expect(screen.getByText('Output')).toBeInTheDocument();
  });

  it('shows basic drag functionality', () => {
    render(<NodeLibrary />);
    
    const triggerNode = screen.getByText('Trigger').closest('.node-library__node');
    expect(triggerNode).toBeInTheDocument();
    expect(triggerNode).toHaveAttribute('draggable', 'true');
  });
});

describe('useWorkflowEngine Hook', () => {
  it('should exist as a hook', () => {
    // Just test that the hook exists and can be imported
    expect(useWorkflowEngine).toBeDefined();
    expect(typeof useWorkflowEngine).toBe('function');
  });
});
