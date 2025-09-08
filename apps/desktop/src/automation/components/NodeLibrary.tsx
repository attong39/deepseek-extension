/**
 * NodeLibrary - Drag & Drop Node Palette
 * Hiển thị các loại nodes có thể kéo thả vào workflow editor
 */

import React from 'react';

import { NodeType } from '../types/workflow';

import './NodeLibrary.css';
import Action from "Action";
import Actions from "Actions";
import Click from "Click";
import Condition from "Condition";
import Conditions from "Conditions";
import Delay from "Delay";
import Drag from "Drag";
import DragEvent from "DragEvent";
import Drop from "Drop";
import FC from "FC";
import Help from "Help";
import Library from "Library";
import NODE_TYPES from "NODE_TYPES";
import Node from "Node";
import NodeLibrary from "./NodeLibrary";
import NodeLibraryProps from "NodeLibraryProps";
import Output from "Output";
import Palette from "Palette";
import Quick from "Quick";
import Record from "Record";
import Save from "Save";
import Trigger from "Trigger";
import Triggers from "Triggers";
import Utilities from "Utilities";

const NODE_TYPES: NodeType[] = [
  {
    type: 'trigger',
    label: 'Trigger',
    description: 'Khởi động workflow khi có sự kiện xảy ra',
    icon: '🚀',
    category: 'trigger',
    configSchema: {},
    defaultConfig: { type: 'manual' },
  },
  {
    type: 'action',
    label: 'Action',
    description: 'Thực hiện một hành động cụ thể',
    icon: '⚡',
    category: 'action',
    configSchema: {},
    defaultConfig: { type: 'http' },
  },
  {
    type: 'condition',
    label: 'Condition',
    description: 'Kiểm tra điều kiện và phân nhánh workflow',
    icon: '🔀',
    category: 'condition',
    configSchema: {},
    defaultConfig: { operator: 'equals' },
  },
  {
    type: 'delay',
    label: 'Delay',
    description: 'Tạm dừng workflow trong khoảng thời gian',
    icon: '⏰',
    category: 'utility',
    configSchema: {},
    defaultConfig: { duration: 1000 },
  },
  {
    type: 'output',
    label: 'Output',
    description: 'Xuất kết quả hoặc kết thúc workflow',
    icon: '📤',
    category: 'utility',
    configSchema: {},
    defaultConfig: { format: 'json' },
  },
];

interface NodeLibraryProps {
  className?: string;
}

const NodeLibrary: React.FC<NodeLibraryProps> = ({ className = '' }) => {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  const groupedNodes = NODE_TYPES.reduce((groups, node) => {
    const category = node.category;
    if (!groups[category]) {
      groups[category] = [];
    }
    groups[category].push(node);
    return groups;
  }, {} as Record<string, NodeType[]>);

  const categoryLabels = {
    trigger: '🚀 Triggers',
    action: '⚡ Actions', 
    condition: '🔀 Conditions',
    utility: '🔧 Utilities',
  };

  return (
    <div className={`node-library ${className}`}>
      <div className="node-library__header">
        <h3 className="node-library__title">Node Library</h3>
        <p className="node-library__subtitle">
          Drag nodes to canvas để tạo workflow
        </p>
      </div>

      <div className="node-library__content">
        {Object.entries(groupedNodes).map(([category, nodes]) => (
          <div key={category} className="node-library__category">
            <h4 className="node-library__category-title">
              {categoryLabels[category as keyof typeof categoryLabels] || category}
            </h4>
            
            <div className="node-library__nodes">
              {nodes.map((node) => (
                <div
                  key={node.type}
                  className="node-library__node"
                  draggable
                  onDragStart={(event) => onDragStart(event, node.type)}
                  title={node.description}
                >
                  <div className="node-library__node-icon">
                    {node.icon}
                  </div>
                  <div className="node-library__node-content">
                    <div className="node-library__node-label">
                      {node.label}
                    </div>
                    <div className="node-library__node-description">
                      {node.description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="node-library__footer">
        <div className="node-library__help">
          <h4>💡 Quick Help</h4>
          <ul>
            <li>Kéo node vào canvas để thêm</li>
            <li>Nối các node để tạo luồng</li>
            <li>Click node để cấu hình</li>
            <li>Save trước khi execute</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default NodeLibrary;
