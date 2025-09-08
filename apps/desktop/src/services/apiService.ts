import AI from "AI";
import API from "./API/index";
import APIs from "APIs";
import Add from "Add";
import ApiService from "./ApiService";
import Assistant from "Assistant";
import AssistantRequest from "AssistantRequest";
import AssistantResponse from "AssistantResponse";
import Authentication from "Authentication";
import Authorization from "Authorization";
import Bearer from "Bearer";
import Check from "Check";
import Content from "Content";
import CreateDatasetRequest from "CreateDatasetRequest";
import DEBUG from "DEBUG";
import DELETE from "DELETE";
import Dataset from "Dataset";
import DatasetStats from "DatasetStats";
import Desktop from "Desktop";
import ERROR from "ERROR";
import Error from "Error";
import Existing from "Existing";
import File from "File";
import FormData from "FormData";
import HTTP from "HTTP";
import Health from "./Health";
import HealthStatus from "HealthStatus";
import INFO from "INFO";
import Jobs from "Jobs";
import Local from "Local";
import LogItem from "LogItem";
import LoginResponse from "LoginResponse";
import Logs from "../pages/Logs";
import NLP from "NLP";
import NLPParseResponse from "NLPParseResponse";
import New from "New";
import POST from "POST";
import PUT from "PUT";
import ParseRequest from "ParseRequest";
import ParseResponse from "ParseResponse";
import Query from "Query";
import Record from "Record";
import RequestInit from "RequestInit";
import Rule from "Rule";
import RuleUpsert from "RuleUpsert";
import Rules from "Rules";
import Security from "./Security";
import Server from "Server";
import Service from "Service";
import Singleton from "Singleton";
import T from "T";
import Team from "Team";
import Training from "./Training";
import TrainingJob from "TrainingJob";
import TrainingJobCreate from "TrainingJobCreate";
import TrainingSampleRequest from "TrainingSampleRequest";
import TrainingSampleResponse from "TrainingSampleResponse";
import Try from "Try";
import Type from "Type";
import URLSearchParams from "URLSearchParams";
import UpdateDatasetRequest from "UpdateDatasetRequest";
import Updated from "Updated";
import Upload from "./Upload";
import UploadResponse from "UploadResponse";
import Uploads from "Uploads";
import WARNING from "WARNING";
/**
 * API Service for Desktop ↔ AI Server integration
 * Updated với Local AI APIs và Team Security
 */

// Existing interfaces
export interface UploadResponse {
  id: string;
  filename: string;
  size: number;
  content_type: string;
  upload_time: string;
}

export interface TrainingJob {
  id: string;
  name: string;
  status: 'created' | 'running' | 'paused' | 'completed' | 'cancelled' | 'failed';
  progress: number;
  created_at: string;
  updated_at: string;
  data_source?: string;
  config: Record<string, any>;
  logs: string[];
}

export interface TrainingJobCreate {
  name: string;
  data_source?: string;
  config?: Record<string, any>;
}

export interface Rule {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  config: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface RuleUpsert {
  name: string;
  description: string;
  enabled?: boolean;
  config?: Record<string, any>;
}

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    username: string;
    role: string;
  };
}

export interface Dataset {
  id: string;
  name: string;
  description: string;
  team_locked: boolean;
  creator_role: string;
  created_at: string;
  updated_at: string;
}

export interface CreateDatasetRequest {
  name: string;
  description: string;
  team_locked?: boolean;
}

export interface UpdateDatasetRequest {
  name?: string;
  description?: string;
  team_locked?: boolean;
}

export interface NLPParseResponse {
  tokens: Array<{
    text: string;
    pos: string;
    entity?: string;
  }>;
  entities: Array<{
    text: string;
    label: string;
    start: number;
    end: number;
  }>;
  sentiment?: {
    label: string;
    score: number;
  };
  metadata: Record<string, any>;
}

export interface LogItem {
  id: string;
  timestamp: string;
  level: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
  message: string;
  source: string;
  metadata: Record<string, any>;
}

// New Local AI interfaces
export interface AssistantRequest {
  text: string;
  rules?: string;
  context?: Record<string, any>;
}

export interface AssistantResponse {
  source: string;
  text: string;
  confidence: number;
  uncertainty: number;
  metadata: Record<string, any>;
}

export interface TrainingSampleRequest {
  input_text: string;
  output_text: string;
  rules?: string;
  category?: string;
  difficulty?: 'easy' | 'medium' | 'hard';
  meta?: Record<string, any>;
}

export interface TrainingSampleResponse {
  id: number;
  created_at: string;
  user_id: string;
  team_id: string;
  status: string;
}

export interface DatasetStats {
  total_samples: number;
  samples_by_category: Record<string, number>;
  samples_by_user: Record<string, number>;
  samples_by_difficulty: Record<string, number>;
  team_id: string;
}

export interface ParseRequest {
  text: string;
  language?: string;
  context?: Record<string, any>;
}

export interface ParseResponse {
  action: string;
  parameters: Record<string, any>;
  confidence: number;
  original_text: string;
  detected_language: string;
}

export interface HealthStatus {
  status: string;
  timestamp: string;
  version: string;
  services: {
    api: string;
    storage: string;
    total_uploads: number;
    total_jobs: number;
    total_rules: number;
    total_logs: number;
  };
}

class ApiService {
  private readonly baseUrl: string;
  private token: string | null = null;

  constructor(baseUrl = 'http://localhost:8002') {
    this.baseUrl = baseUrl;
    // Try to load token from localStorage
    this.token = localStorage.getItem('zeta_token');
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Add existing headers
    if (options?.headers) {
      Object.assign(headers, options.headers);
    }

    // Add Authorization header if token exists
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Authentication methods
  async login(username: string, password: string): Promise<LoginResponse> {
    return this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  setToken(token: string): void {
    this.token = token;
    localStorage.setItem('zeta_token', token);
  }

  clearToken(): void {
    this.token = null;
    localStorage.removeItem('zeta_token');
  }

  // Health Check
  async getHealth(): Promise<HealthStatus> {
    return this.request<HealthStatus>('/health');
  }

  // Assistant methods
  async assistantChat(message: string, context?: string): Promise<AssistantResponse> {
    return this.request<AssistantResponse>('/api/v1/assistant/chat', {
      method: 'POST',
      body: JSON.stringify({ message, context }),
    });
  }

  // Dataset methods
  async getDatasets(): Promise<Dataset[]> {
    return this.request<Dataset[]>('/api/v1/datasets');
  }

  async createDataset(dataset: CreateDatasetRequest): Promise<Dataset> {
    return this.request<Dataset>('/api/v1/datasets', {
      method: 'POST',
      body: JSON.stringify(dataset),
    });
  }

  async getDataset(id: string): Promise<Dataset> {
    return this.request<Dataset>(`/api/v1/datasets/${id}`);
  }

  async updateDataset(id: string, dataset: UpdateDatasetRequest): Promise<Dataset> {
    return this.request<Dataset>(`/api/v1/datasets/${id}`, {
      method: 'PUT',
      body: JSON.stringify(dataset),
    });
  }

  async deleteDataset(id: string): Promise<void> {
    return this.request<void>(`/api/v1/datasets/${id}`, {
      method: 'DELETE',
    });
  }

  // NLP methods
  async parseText(text: string, options?: { mode?: 'rule' | 'llm' | 'auto' }): Promise<NLPParseResponse> {
    return this.request<NLPParseResponse>('/api/v1/nlp/parse', {
      method: 'POST',
      body: JSON.stringify({ text, ...options }),
    });
  }

  // Uploads
  async uploadFile(file: File, description?: string): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (description) {
      formData.append('description', description);
    }

    const response = await fetch(`${this.baseUrl}/api/v1/uploads`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async getUploads(limit = 50, skip = 0): Promise<UploadResponse[]> {
    return this.request<UploadResponse[]>(`/api/v1/uploads?limit=${limit}&skip=${skip}`);
  }

  async getUpload(fileId: string): Promise<UploadResponse> {
    return this.request<UploadResponse>(`/api/v1/uploads/${fileId}`);
  }

  // Training Jobs
  async createTrainingJob(jobData: TrainingJobCreate): Promise<TrainingJob> {
    return this.request<TrainingJob>('/api/v1/training/jobs', {
      method: 'POST',
      body: JSON.stringify(jobData),
    });
  }

  async getTrainingJobs(status?: string, limit = 50, skip = 0): Promise<TrainingJob[]> {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    params.append('limit', limit.toString());
    params.append('skip', skip.toString());

    return this.request<TrainingJob[]>(`/api/v1/training/jobs?${params.toString()}`);
  }

  async getTrainingJob(jobId: string): Promise<TrainingJob> {
    return this.request<TrainingJob>(`/api/v1/training/jobs/${jobId}`);
  }

  async startTrainingJob(jobId: string): Promise<{ message: string; job_id: string }> {
    return this.request(`/api/v1/training/jobs/${jobId}/start`, {
      method: 'POST',
    });
  }

  async pauseTrainingJob(jobId: string): Promise<{ message: string; job_id: string }> {
    return this.request(`/api/v1/training/jobs/${jobId}/pause`, {
      method: 'POST',
    });
  }

  async cancelTrainingJob(jobId: string): Promise<{ message: string; job_id: string }> {
    return this.request(`/api/v1/training/jobs/${jobId}/cancel`, {
      method: 'POST',
    });
  }

  // Rules
  async createRule(ruleData: RuleUpsert): Promise<Rule> {
    return this.request<Rule>('/api/v1/rules', {
      method: 'POST',
      body: JSON.stringify(ruleData),
    });
  }

  async getRules(enabled?: boolean, limit = 50, skip = 0): Promise<Rule[]> {
    const params = new URLSearchParams();
    if (enabled !== undefined) params.append('enabled', enabled.toString());
    params.append('limit', limit.toString());
    params.append('skip', skip.toString());

    return this.request<Rule[]>(`/api/v1/rules?${params.toString()}`);
  }

  async getRule(ruleId: string): Promise<Rule> {
    return this.request<Rule>(`/api/v1/rules/${ruleId}`);
  }

  async updateRule(ruleId: string, ruleData: RuleUpsert): Promise<Rule> {
    return this.request<Rule>(`/api/v1/rules/${ruleId}`, {
      method: 'PUT',
      body: JSON.stringify(ruleData),
    });
  }

  async deleteRule(ruleId: string): Promise<{ message: string; rule_id: string }> {
    return this.request(`/api/v1/rules/${ruleId}`, {
      method: 'DELETE',
    });
  }

  // Logs
  async getLogs(
    level?: string,
    source?: string,
    limit = 100,
    skip = 0
  ): Promise<LogItem[]> {
    const params = new URLSearchParams();
    if (level) params.append('level', level);
    if (source) params.append('source', source);
    params.append('limit', limit.toString());
    params.append('skip', skip.toString());

    return this.request<LogItem[]>(`/api/v1/logs?${params.toString()}`);
  }
}

// Singleton instance
export const apiService = new ApiService();

// React Query integration helpers
export const queryKeys = {
  health: ['health'],
  uploads: (limit?: number, skip?: number) => ['uploads', { limit, skip }],
  upload: (id: string) => ['uploads', id],
  trainingJobs: (status?: string, limit?: number, skip?: number) => 
    ['training-jobs', { status, limit, skip }],
  trainingJob: (id: string) => ['training-jobs', id],
  rules: (enabled?: boolean, limit?: number, skip?: number) => 
    ['rules', { enabled, limit, skip }],
  rule: (id: string) => ['rules', id],
  logs: (level?: string, source?: string, limit?: number, skip?: number) => 
    ['logs', { level, source, limit, skip }],
} as const;
