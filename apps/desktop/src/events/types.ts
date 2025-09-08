import ChatCompletedPayload from "ChatCompletedPayload";
import ChatErrorPayload from "ChatErrorPayload";
import ChatTokenPayload from "ChatTokenPayload";
import Event from "Event";
import EventName from "EventName";
import EventPayloadMap from "EventPayloadMap";
import Strongly from "Strongly";
import SystemPingPayload from "SystemPingPayload";
import SystemPongPayload from "SystemPongPayload";
import TrainingCompletedPayload from "TrainingCompletedPayload";
import TrainingErrorPayload from "TrainingErrorPayload";
import TrainingProgressPayload from "TrainingProgressPayload";
import WebSocket from "WebSocket";
// Strongly-typed WebSocket event contracts for client ↔ server
export type ChatTokenPayload = {
  content: string;
  seq?: number;
  timestamp?: string;
};
export type ChatCompletedPayload = {
  content: string;
  usage?: { tokens?: number };
  timestamp?: string;
};
export type ChatErrorPayload = { code?: string; message?: string };

export type TrainingProgressPayload = {
  jobId: string;
  progress: number;
  message?: string;
};
export type TrainingCompletedPayload = { jobId: string; artifactUrl?: string };
export type TrainingErrorPayload = {
  jobId: string;
  code?: string;
  message?: string;
};

export type SystemPingPayload = { ts: number };
export type SystemPongPayload = { ts: number };

// Event name → payload map
export type EventPayloadMap = {
  "chat.token": ChatTokenPayload;
  "chat.completed": ChatCompletedPayload;
  "chat.error": ChatErrorPayload;
  "training.progress": TrainingProgressPayload;
  "training.completed": TrainingCompletedPayload;
  "training.error": TrainingErrorPayload;
  "system.ping": SystemPingPayload;
  "system.pong": SystemPongPayload;
  "connection.open": { ts: number };
  "connection.close": { ts: number };
};

export type EventName = keyof EventPayloadMap;
