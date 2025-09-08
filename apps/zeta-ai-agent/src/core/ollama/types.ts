import ChatMessage from "ChatMessage";
import ChatOptions from "ChatOptions";
import ChatResponse from "ChatResponse";
import EmbeddingsRequest from "EmbeddingsRequest";
import EmbeddingsResponse from "EmbeddingsResponse";
import Error from "Error";
import GenerateRequest from "GenerateRequest";
import GenerateResponse from "GenerateResponse";
import ModelInfo from "ModelInfo";
import ModelListResponse from "ModelListResponse";
import OllamaConfig from "OllamaConfig";
import OllamaError from "OllamaError";
import PullRequest from "PullRequest";
import PushRequest from "PushRequest";
import StreamResponse from "StreamResponse";
export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
  images?: string[];
}

export interface ChatOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
  stop?: string[];
  topP?: number;
  topK?: number;
  format?: 'json' | 'text';
}

export interface ChatResponse {
  message: ChatMessage;
  created_at: string;
  model: string;
  done: boolean;
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  prompt_eval_duration?: number;
  eval_count?: number;
  eval_duration?: number;
}

export interface ModelInfo {
  name: string;
  modified_at: string;
  size: number;
  digest: string;
  details: {
    format: string;
    family: string;
    families?: string[];
    parameter_size: string;
    quantization_level: string;
  };
}

export interface ModelListResponse {
  models: ModelInfo[];
}

export interface PullRequest {
  name: string;
  insecure?: boolean;
  stream?: boolean;
}

export interface PushRequest {
  name: string;
  insecure?: boolean;
  stream?: boolean;
}

export interface GenerateRequest {
  model: string;
  prompt: string;
  images?: string[];
  format?: 'json';
  options?: ChatOptions;
  system?: string;
  template?: string;
  context?: number[];
  stream?: boolean;
  raw?: boolean;
  keep_alive?: string;
}

export interface GenerateResponse {
  model: string;
  created_at: string;
  response: string;
  done: boolean;
  context?: number[];
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  prompt_eval_duration?: number;
  eval_count?: number;
  eval_duration?: number;
}

export interface EmbeddingsRequest {
  model: string;
  prompt: string;
  options?: ChatOptions;
  keep_alive?: string;
}

export interface EmbeddingsResponse {
  embedding: number[];
}

export interface StreamResponse {
  model: string;
  created_at: string;
  message?: ChatMessage;
  response?: string;
  done: boolean;
}

export class OllamaError extends Error {
  constructor(
    message: string,
    public statusCode: number = 0,
    public endpoint?: string,
    public cause?: Error
  ) {
    super(message);
    this.name = 'OllamaError';
  }
}

export interface OllamaConfig {
  baseUrl: string;
  timeout: number;
  defaultModel: string;
  maxRetries: number;
  retryDelay: number;
}
