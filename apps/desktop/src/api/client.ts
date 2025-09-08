// Sample API client for Zeta Desktop
import axios from 'axios';
import API from "./index";
import API_BASE from "API_BASE";
import Agent from "Agent";
import Desktop from "Desktop";
import Feature from "Feature";
import FeatureFlags from "FeatureFlags";
import Handle from "Handle";
import Sample from "Sample";
import Team from "Team";
import This from "This";
import VITE_API_BASE from "VITE_API_BASE";
import VITE_ENABLE_OPA from "VITE_ENABLE_OPA";
import VITE_ENABLE_PROMETHEUS from "VITE_ENABLE_PROMETHEUS";
import VITE_ENABLE_ZERO_TRUST from "VITE_ENABLE_ZERO_TRUST";
import VITE_UNKNOWN_FEATURE from "VITE_UNKNOWN_FEATURE";
import WebSocket from "WebSocket";
import Zeta from "Zeta";
import ZetaApiClient from "ZetaApiClient";
import ZetaWebSocket from "ZetaWebSocket";

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export class ZetaApiClient {
  async getHealth() {
    return axios.get('/api/v1/health');
  }

  async getSecurityStatus() {
    return fetch('/api/v1/security/status');
  }

  async evaluatePolicy(payload: any) {
    return axios.post('/api/v1/security/policy/evaluate', payload);
  }

  async getMetrics() {
    return fetch('/api/v1/observability/metrics');
  }

  // This API doesn't exist in backend - should be flagged as extra
  async getUnknownEndpoint() {
    return fetch('/api/v1/unknown/endpoint');
  }
}

// WebSocket connection
export class ZetaWebSocket {
  private ws: WebSocket | null = null;

  connect() {
    this.ws = new WebSocket('/api/v1/ws');
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Handle different event types
      switch (data.event) {
        case 'team.started':
          this.handleTeamStarted(data);
          break;
        case 'agent.step':
          this.handleAgentStep(data);
          break;
        case 'team.done':
          this.handleTeamDone(data);
          break;
      }
      
      // Handle ping/pong
      if (data.type === 'ping') {
        this.ws?.send(JSON.stringify({ type: 'pong' }));
      }
    };
  }

  private handleTeamStarted(data: any) {
    console.log('Team started:', data);
  }

  private handleAgentStep(data: any) {
    console.log('Agent step:', data);
  }

  private handleTeamDone(data: any) {
    console.log('Team done:', data);
  }
}

// Feature flags usage
export const FeatureFlags = {
  zeroTrust: import.meta.env.VITE_ENABLE_ZERO_TRUST === 'true',
  opa: import.meta.env.VITE_ENABLE_OPA === 'true',
  metrics: import.meta.env.VITE_ENABLE_PROMETHEUS === 'true',
  // This flag doesn't exist in backend
  unknownFeature: import.meta.env.VITE_UNKNOWN_FEATURE === 'true',
};
