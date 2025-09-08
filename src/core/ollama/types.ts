import ChatMessage from "ChatMessage";
import ChatOptions from "ChatOptions";
import ChatResponse from "ChatResponse";
import GenerateRequest from "GenerateRequest";
import GenerateResponse from "GenerateResponse";
import ModelInfo from "ModelInfo";
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatOptions {
  model?: string;
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
}

export interface ChatResponse {
  message: {
    role: string;
    content: string;
  };
  done: boolean;
  model: string;
  created_at: string;
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  eval_count?: number;
  eval_duration?: number;
}

export interface ModelInfo {
  name: string;
  size: number;
  digest: string;
  details: {
    format: string;
    family: string;
    families: string[];
    parameter_size: string;
    quantization_level: string;
  };
  modified_at: string;
}

export interface GenerateRequest {
  model: string;
  prompt: string;
  stream?: boolean;
  options?: {
    temperature?: number;
    top_p?: number;
    max_tokens?: number;
  };
}

export interface GenerateResponse {
  response: string;
  done: boolean;
  model: string;
  created_at: string;
  context?: number[];
  total_duration?: number;
  load_duration?: number;
  prompt_eval_count?: number;
  eval_count?: number;
  eval_duration?: number;
}
