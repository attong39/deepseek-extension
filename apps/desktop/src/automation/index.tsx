import AI from "AI";
import ActionConfig from "ActionConfig";
import Automation from "./index";
import AutomationPage from "./AutomationPage";
import Desktop from "Desktop";
import Entry from "Entry";
import Module from "Module";
import NodeLibrary from "./components/NodeLibrary";
import NodeType from "NodeType";
import Re from "Re";
import TriggerConfig from "TriggerConfig";
import TriggerPanel from "./components/TriggerPanel";
import Workflow from "Workflow";
import WorkflowEdge from "WorkflowEdge";
import WorkflowEditor from "./components/WorkflowEditor";
import WorkflowExecution from "WorkflowExecution";
import WorkflowLog from "WorkflowLog";
import WorkflowNode from "WorkflowNode";
import WorkflowTemplate from "WorkflowTemplate";
import ZETA from "ZETA";
/**
 * Automation Module - ZETA Desktop AI
 * Entry point cho automation workflow system
 */

export { default as AutomationPage } from './AutomationPage';
export { default as NodeLibrary } from './components/NodeLibrary';
export { default as TriggerPanel } from './components/TriggerPanel';
export { default as WorkflowEditor } from './components/WorkflowEditor';

export { useWorkflowEngine } from './hooks/useWorkflowEngine';

export type {
    ActionConfig,
    NodeType, TriggerConfig, Workflow, WorkflowEdge, WorkflowExecution,
    WorkflowLog, WorkflowNode, WorkflowTemplate
} from './types/workflow';

// Re-export AutomationPage as default component for /automation route
export { default } from './AutomationPage';
