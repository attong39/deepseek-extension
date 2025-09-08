/**
 * Agents Route Component
 * =====================
 * 
 * React component for agent team management with real-time WebSocket updates.
 * Features: team creation, workflow execution, live status monitoring.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle 
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
import Agent from "Agent";
import AgentTeam from "AgentTeam";
import Agents from "./Agents";
import Analysis from "Analysis";
import BACKEND_URL from "BACKEND_URL";
import Clear from "Clear";
import Code from "Code";
import Component from "Component";
import Connected from "Connected";
import Content from "Content";
import Count from "Count";
import Create from "Create";
import Creation from "Creation";
import Data from "Data";
import Details from "Details";
import Enter from "Enter";
import Events from "../Events/index";
import Execute from "Execute";
import Execution from "Execution";
import Failed from "Failed";
import Features from "../Features/index";
import Form from "Form";
import Keep from "Keep";
import List from "List";
import Live from "Live";
import Load from "Load";
import Management from "Management";
import Name from "Name";
import New from "New";
import No from "No";
import POST from "POST";
import Parallel from "Parallel";
import Please from "Please";
import Real from "Real";
import Review from "Review";
import Route from "Route";
import Selected from "Selected";
import State from "State";
import Steps from "Steps";
import StreamEvent from "StreamEvent";
import Task from "Task";
import Team from "Team";
import Teams from "Teams";
import Type from "Type";
import Update from "Update";
import WS_URL from "WS_URL";
import WebSocket from "WebSocket";
import Workflow from "Workflow";
import WorkflowSpec from "WorkflowSpec";
  Play, 
  Square, 
  Users, 
  Activity, 
  Zap 
} from 'lucide-react';

interface Agent {
  id: string;
  role: string;
  capabilities: string[];
  status: 'idle' | 'working' | 'completed' | 'error';
}

interface WorkflowSpec {
  name: string;
  steps: string[];
  parallel_execution: boolean;
}

interface AgentTeam {
  id: string;
  name: string;
  status: 'created' | 'running' | 'completed' | 'failed';
  agents: Agent[];
  workflow: WorkflowSpec;
  created_at: string;
}

interface StreamEvent {
  event: string;
  timestamp: string;
  team_id: string;
  agent_id?: string;
  step?: string;
  status?: string;
  message?: string;
}

const BACKEND_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000';

export default function Agents() {
  // State management
  const [teams, setTeams] = useState<AgentTeam[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<AgentTeam | null>(null);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  
  // Form state
  const [newTeamName, setNewTeamName] = useState('');
  const [workflowName, setWorkflowName] = useState('');
  const [workflowSteps, setWorkflowSteps] = useState('');
  const [agentCount, setAgentCount] = useState(3);
  const [parallelExecution, setParallelExecution] = useState(false);

  // Load teams on component mount
  useEffect(() => {
    loadTeams();
  }, []);

  // WebSocket connection management
  useEffect(() => {
    if (selectedTeam) {
      connectWebSocket(selectedTeam.id);
    }
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [selectedTeam]);

  const loadTeams = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/agents/teams`);
      if (response.ok) {
        const teamsData = await response.json();
        setTeams(teamsData);
      }
    } catch (error) {
      console.error('Failed to load teams:', error);
    }
  };

  const connectWebSocket = useCallback((teamId: string) => {
    if (ws) {
      ws.close();
    }

    const websocket = new WebSocket(`${WS_URL}/api/v1/agents/teams/${teamId}/stream`);
    
    websocket.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected for team:', teamId);
    };

    websocket.onmessage = (event) => {
      try {
        const streamEvent: StreamEvent = JSON.parse(event.data);
        setEvents(prev => [...prev.slice(-49), streamEvent]); // Keep last 50 events
        
        // Update team status if needed
        if (streamEvent.status) {
          setTeams(prev => prev.map(team => 
            team.id === teamId 
              ? { ...team, status: streamEvent.status as any }
              : team
          ));
        }
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    websocket.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    setWs(websocket);
  }, [ws]);

  const createTeam = async () => {
    if (!newTeamName || !workflowName || !workflowSteps) {
      alert('Please fill in all required fields');
      return;
    }

    const workflow: WorkflowSpec = {
      name: workflowName,
      steps: workflowSteps.split(',').map(s => s.trim()),
      parallel_execution: parallelExecution
    };

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/agents/teams`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          team_name: newTeamName,
          workflow,
          agent_count: agentCount
        })
      });

      if (response.ok) {
        const newTeam = await response.json();
        setTeams(prev => [...prev, newTeam]);
        
        // Clear form
        setNewTeamName('');
        setWorkflowName('');
        setWorkflowSteps('');
        setAgentCount(3);
        setParallelExecution(false);
      }
    } catch (error) {
      console.error('Failed to create team:', error);
    }
  };

  const executeTask = async (teamId: string) => {
    const task = {
      id: `task_${Date.now()}`,
      description: 'Execute team workflow',
      priority: 'normal'
    };

    try {
      const response = await fetch(`${BACKEND_URL}/api/v1/agents/teams/${teamId}/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(task)
      });

      if (response.ok) {
        // Execution started, events will come via WebSocket
        console.log('Task execution started for team:', teamId);
      }
    } catch (error) {
      console.error('Failed to execute task:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'created': return 'bg-blue-100 text-blue-800';
      case 'running': return 'bg-yellow-100 text-yellow-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'failed': return 'bg-red-100 text-red-800';
      case 'working': return 'bg-orange-100 text-orange-800';
      case 'idle': return 'bg-gray-100 text-gray-800';
      case 'error': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Agent Teams Management</h1>
      
      {/* Team Creation Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Create New Team
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Team Name</label>
              <Input
                value={newTeamName}
                onChange={(e) => setNewTeamName(e.target.value)}
                placeholder="Enter team name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Agent Count</label>
              <Input
                type="number"
                value={agentCount}
                onChange={(e) => setAgentCount(parseInt(e.target.value) || 3)}
                min={1}
                max={10}
              />
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Workflow Name</label>
              <Input
                value={workflowName}
                onChange={(e) => setWorkflowName(e.target.value)}
                placeholder="e.g., Code Review, Data Analysis"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Workflow Steps</label>
              <Input
                value={workflowSteps}
                onChange={(e) => setWorkflowSteps(e.target.value)}
                placeholder="step1, step2, step3"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="parallel"
              checked={parallelExecution}
              onChange={(e) => setParallelExecution(e.target.checked)}
              className="rounded"
            />
            <label htmlFor="parallel" className="text-sm font-medium">
              Parallel Execution
            </label>
          </div>
          
          <Button onClick={createTeam} className="w-full">
            Create Team
          </Button>
        </CardContent>
      </Card>

      {/* Teams List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {teams.map((team) => (
          <Card 
            key={team.id} 
            className={`cursor-pointer transition-all hover:shadow-md ${
              selectedTeam?.id === team.id ? 'ring-2 ring-blue-500' : ''
            }`}
            onClick={() => setSelectedTeam(team)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{team.name}</CardTitle>
                <Badge className={getStatusColor(team.status)}>
                  {team.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Agents:</span> {team.agents.length}
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Workflow:</span> {team.workflow.name}
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Steps:</span> {team.workflow.steps.length}
                </div>
                <div className="flex items-center gap-2 pt-2">
                  <Button
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      executeTask(team.id);
                    }}
                    disabled={team.status === 'running'}
                  >
                    <Play className="h-4 w-4 mr-1" />
                    Execute
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Selected Team Details */}
      {selectedTeam && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Team Details */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                {selectedTeam.name} Details
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Agents ({selectedTeam.agents.length})</h4>
                  <div className="space-y-2">
                    {selectedTeam.agents.map((agent) => (
                      <div key={agent.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <div>
                          <div className="font-medium">{agent.role}</div>
                          <div className="text-sm text-gray-600">
                            {agent.capabilities.join(', ')}
                          </div>
                        </div>
                        <Badge className={getStatusColor(agent.status)}>
                          {agent.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Workflow Steps</h4>
                  <div className="space-y-1">
                    {selectedTeam.workflow.steps.map((step, index) => (
                      <div key={index} className="flex items-center gap-2 text-sm">
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                          {index + 1}
                        </span>
                        {step}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Real-time Events */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Live Events
                {isConnected && (
                  <Badge className="bg-green-100 text-green-800">
                    <Zap className="h-3 w-3 mr-1" />
                    Connected
                  </Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {events.length === 0 ? (
                  <div className="text-gray-500 text-center py-4">
                    No events yet. Execute a task to see real-time updates.
                  </div>
                ) : (
                  events.slice().reverse().map((event, index) => (
                    <div key={index} className="p-2 bg-gray-50 rounded text-sm">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium">{event.event}</span>
                        <span className="text-xs text-gray-500">
                          {new Date(event.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                      {event.message && (
                        <div className="text-gray-600">{event.message}</div>
                      )}
                      {event.agent_id && (
                        <div className="text-xs text-blue-600">
                          Agent: {event.agent_id}
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
