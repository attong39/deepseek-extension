import ADMIN_CONFIG from "ADMIN_CONFIG";
import ADMIN_USERS from "ADMIN_USERS";
import AGENT from "AGENT";
import AGENTS from "../routes/AGENTS";
import API from "../API/index";
import ASSISTANT from "ASSISTANT";
import ASSISTANTS from "ASSISTANTS";
import AUTH_LOGIN from "AUTH_LOGIN";
import AUTH_REFRESH from "AUTH_REFRESH";
import Admin from "Admin";
import Agents from "../routes/Agents";
import Assistants from "Assistants";
import Auth from "Auth";
import CHAT from "../pages/CHAT";
import CHAT_CONVERSATIONS from "CHAT_CONVERSATIONS";
import CHAT_MESSAGES from "CHAT_MESSAGES";
import Chat from "../pages/Chat";
import DEFAULT_API_BASE_URL from "DEFAULT_API_BASE_URL";
import DEFAULT_WS_URL from "DEFAULT_WS_URL";
import DESKTOP_API_BASE_URL from "DESKTOP_API_BASE_URL";
import Desktop from "Desktop";
import FEDERATED_JOBS from "FEDERATED_JOBS";
import FEDERATED_ROUNDS from "FEDERATED_ROUNDS";
import FEDERATED_STATUS from "FEDERATED_STATUS";
import FEEDBACK from "FEEDBACK";
import FILES_DELETE from "FILES_DELETE";
import FILES_DOWNLOAD from "FILES_DOWNLOAD";
import FILES_LIST from "FILES_LIST";
import FILES_UPLOAD from "FILES_UPLOAD";
import Federated from "Federated";
import Feedback from "Feedback";
import Files from "Files";
import HEALTH from "HEALTH";
import HEALTH_DETAILED from "HEALTH_DETAILED";
import Health from "Health";
import LEARNING_DATASETS from "LEARNING_DATASETS";
import LEARNING_INGEST_TEXT from "LEARNING_INGEST_TEXT";
import LEARNING_INGEST_URLS from "LEARNING_INGEST_URLS";
import LEARNING_INTERACTIONS from "LEARNING_INTERACTIONS";
import LEARNING_JOB from "LEARNING_JOB";
import LEARNING_JOBS from "LEARNING_JOBS";
import LEARNING_JOB_CANCEL from "LEARNING_JOB_CANCEL";
import LLM from "LLM";
import LLM_CHAT from "LLM_CHAT";
import LLM_COMPLETE from "LLM_COMPLETE";
import LLM_EMBED from "LLM_EMBED";
import Learning from "Learning";
import MENTOR_GUIDE from "MENTOR_GUIDE";
import MENTOR_GUIDE_STREAM from "MENTOR_GUIDE_STREAM";
import Mentor from "Mentor";
import OpenAPI from "OpenAPI";
import PERFORMANCE_METRICS from "PERFORMANCE_METRICS";
import PERFORMANCE_PROFILE from "PERFORMANCE_PROFILE";
import PLANNING_CREATE from "PLANNING_CREATE";
import PLANNING_EXECUTE from "PLANNING_EXECUTE";
import PLANNING_OPTIMIZE from "PLANNING_OPTIMIZE";
import PLANNING_VALIDATE from "PLANNING_VALIDATE";
import PRIVACY_POLICIES from "PRIVACY_POLICIES";
import PRIVACY_SANITIZE from "PRIVACY_SANITIZE";
import Performance from "Performance";
import Planning from "Planning";
import Privacy from "Privacy";
import RAG from "RAG";
import RAG_INDEX from "RAG_INDEX";
import RAG_QUERY from "RAG_QUERY";
import RAG_SEARCH from "RAG_SEARCH";
import SETTINGS from "../pages/SETTINGS";
import SETTINGS_RELOAD from "SETTINGS_RELOAD";
import SYSTEM_INFO from "SYSTEM_INFO";
import SYSTEM_VERSION from "SYSTEM_VERSION";
import Settings from "../pages/Settings";
import System from "System";
import TRAINING_JOB from "TRAINING_JOB";
import TRAINING_JOBS from "TRAINING_JOBS";
import TRAINING_JOB_CANCEL from "TRAINING_JOB_CANCEL";
import TRAINING_MODELS from "TRAINING_MODELS";
import TRAINING_START from "TRAINING_START";
import Training from "../pages/Training";
import URL from "URL";
import VITE_API_BASE_URL from "VITE_API_BASE_URL";
import VITE_WS_URL from "VITE_WS_URL";
import VOICE_STT from "VOICE_STT";
import VOICE_TTS from "VOICE_TTS";
import Vite from "Vite";
import Voice from "Voice";
import WS from "WS";
export const API = {
  // Health
  HEALTH: "/health",
  HEALTH_DETAILED: "/health/detailed",
  // Feedback
  FEEDBACK: "/feedback",
  // Learning
  LEARNING_INGEST_URLS: "/learning/ingest/urls",
  LEARNING_INGEST_TEXT: "/learning/ingest/text",
  LEARNING_DATASETS: "/learning/datasets",
  LEARNING_JOBS: "/learning/jobs",
  LEARNING_JOB: (job_id: string) => `/learning/jobs/${job_id}`,
  LEARNING_JOB_CANCEL: (job_id: string) => `/learning/jobs/${job_id}/cancel`,
  LEARNING_INTERACTIONS: "/learning/interactions",
  // Agents
  AGENTS: "/agents",
  AGENT: (agent_id: string) => `/agents/${agent_id}`,
  // Chat
  CHAT: "/chat",
  CHAT_CONVERSATIONS: "/chat/conversations",
  CHAT_MESSAGES: (conversation_id: string) => `/chat/conversations/${conversation_id}/messages`,
  // Mentor
  MENTOR_GUIDE: "/mentor/guide",
  MENTOR_GUIDE_STREAM: "/mentor/guide/stream",
  // Files
  FILES_LIST: "/files",
  FILES_UPLOAD: "/files/upload",
  FILES_DOWNLOAD: (file_id: string) => `/files/${file_id}/download`,
  FILES_DELETE: (file_id: string) => `/files/${file_id}`,
  // Training
  TRAINING_JOBS: "/training/jobs",
  TRAINING_JOB: (job_id: string) => `/training/jobs/${job_id}`,
  TRAINING_JOB_CANCEL: (job_id: string) => `/training/jobs/${job_id}/cancel`,
  TRAINING_MODELS: "/training/models",
  TRAINING_START: "/training/start",
  // RAG
  RAG_QUERY: "/rag/query",
  RAG_INDEX: "/rag/index",
  RAG_SEARCH: "/rag/search",
  // Voice
  VOICE_TTS: "/voice/tts",
  VOICE_STT: "/voice/stt",
  // Planning
  PLANNING_CREATE: "/planning/create",
  PLANNING_EXECUTE: "/planning/execute",
  PLANNING_OPTIMIZE: "/planning/optimize",
  PLANNING_VALIDATE: "/planning/validate",
  // Privacy
  PRIVACY_SANITIZE: "/privacy/sanitize",
  PRIVACY_POLICIES: "/privacy/policies",
  // Performance
  PERFORMANCE_METRICS: "/performance/metrics",
  PERFORMANCE_PROFILE: "/performance/profile",
  // LLM
  LLM_COMPLETE: "/llm/complete",
  LLM_CHAT: "/llm/chat",
  LLM_EMBED: "/llm/embed",
  // Settings
  SETTINGS: "/settings",
  SETTINGS_RELOAD: "/settings/reload",
  // System
  SYSTEM_INFO: "/system/info",
  SYSTEM_VERSION: "/system/version",
  // Admin
  ADMIN_USERS: "/admin/users",
  ADMIN_CONFIG: "/admin/config",
  // Auth
  AUTH_LOGIN: "/auth/login",
  AUTH_REFRESH: "/auth/refresh",
  // Federated
  FEDERATED_STATUS: "/federated/status",
  FEDERATED_JOBS: "/federated/jobs",
  FEDERATED_ROUNDS: "/federated/rounds",
  // Assistants
  ASSISTANTS: "/assistants",
  ASSISTANT: (assistant_id: string) => `/assistants/${assistant_id}`,
} as const;

// Desktop will call server at root; server already has /api/v1 prefix baked into OpenAPI servers.
function readEnv(key: string): string | undefined {
  try {
    // Vite style
    const v = (import.meta as any)?.env?.[key];
    if (typeof v === "string" && v) return v;
  } catch {}
  return undefined;
}

export const DEFAULT_API_BASE_URL =
  (window as any).DESKTOP_API_BASE_URL ||
  readEnv("VITE_API_BASE_URL") ||
  "http://127.0.0.1:8000/api/v1";

const defaultWsBase = (() => {
  try {
    const url = new URL(DEFAULT_API_BASE_URL);
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
    // Mặc định trỏ tới kênh chat WS phổ biến
    url.pathname = "/ws/chat";
    return url.toString();
  } catch {
    return "ws://127.0.0.1:8000/ws/chat";
  }
})();

export const DEFAULT_WS_URL = readEnv("VITE_WS_URL") || defaultWsBase;
