import AUTO from "AUTO";
import ActionEvent from "ActionEvent";
import Artifacturl from "Artifacturl";
import Assistant from "Assistant";
import AssistantReplyEvent from "AssistantReplyEvent";
import ChatCompletedEvent from "ChatCompletedEvent";
import ChatErrorEvent from "ChatErrorEvent";
import ChatTokenEvent from "ChatTokenEvent";
import Code from "Code";
import Content from "Content";
import Conversation from "Conversation";
import ConversationHistoryEvent from "ConversationHistoryEvent";
import Desktop from "Desktop";
import Do from "Do";
import Event from "Event";
import GENERATED from "GENERATED";
import Generated from "Generated";
import Generic from "Generic";
import ISO from "ISO";
import Id from "Id";
import Is from "Is";
import Jobid from "Jobid";
import Literal from "Literal";
import Message from "Message";
import Messages from "Messages";
import NewMessageEvent from "NewMessageEvent";
import Payload from "Payload";
import PingEvent from "PingEvent";
import PongEvent from "PongEvent";
import Progress from "Progress";
import Seq from "Seq";
import Status from "../pages/Status";
import StatusUpdatedEvent from "StatusUpdatedEvent";
import Streaming from "./Streaming";
import Timestamp from "Timestamp";
import Training from "./Training";
import TrainingCompletedEvent from "TrainingCompletedEvent";
import TrainingErrorEvent from "TrainingErrorEvent";
import TrainingProgressEvent from "TrainingProgressEvent";
import Ts from "Ts";
import Type from "Type";
import Typing from "Typing";
import TypingIndicatorEvent from "TypingIndicatorEvent";
import Usage from "Usage";
import User from "User";
import WSEventType from "WSEventType";
import WS_SCHEMAS from "WS_SCHEMAS";
// AUTO-GENERATED. Do not edit.
// Generated from server websocket schemas via scripts/sync_ws_schema.mjs
/* eslint-disable */
export const WS_SCHEMAS = {
  AssistantReplyEvent: {
    description:
      "Assistant reply payload.\n\nAttributes:\n    type: Literal discriminator 'assistant_reply'.\n    content: Nội dung trả lời.\n    timestamp: ISO time optional.",
    properties: {
      type: {
        const: "assistant_reply",
        default: "assistant_reply",
        title: "Type",
        type: "string",
      },
      content: {
        title: "Content",
        type: "string",
      },
      timestamp: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Timestamp",
      },
    },
    required: ["content"],
    title: "AssistantReplyEvent",
    type: "object",
  },
  ActionEvent: {
    description: "Generic action message (optional).",
    properties: {
      type: {
        const: "action",
        default: "action",
        title: "Type",
        type: "string",
      },
      payload: {
        title: "Payload",
      },
    },
    required: ["payload"],
    title: "ActionEvent",
    type: "object",
  },
  PingEvent: {
    properties: {
      type: {
        const: "ping",
        default: "ping",
        title: "Type",
        type: "string",
      },
      ts: {
        title: "Ts",
        type: "integer",
      },
    },
    required: ["ts"],
    title: "PingEvent",
    type: "object",
  },
  PongEvent: {
    properties: {
      type: {
        const: "pong",
        default: "pong",
        title: "Type",
        type: "string",
      },
      ts: {
        title: "Ts",
        type: "integer",
      },
    },
    required: ["ts"],
    title: "PongEvent",
    type: "object",
  },
  ChatTokenEvent: {
    description: "Streaming token for chat.",
    properties: {
      type: {
        const: "chat.token",
        default: "chat.token",
        title: "Type",
        type: "string",
      },
      content: {
        title: "Content",
        type: "string",
      },
      seq: {
        anyOf: [
          {
            type: "integer",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Seq",
      },
      timestamp: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Timestamp",
      },
    },
    required: ["content"],
    title: "ChatTokenEvent",
    type: "object",
  },
  ChatCompletedEvent: {
    properties: {
      type: {
        const: "chat.completed",
        default: "chat.completed",
        title: "Type",
        type: "string",
      },
      content: {
        title: "Content",
        type: "string",
      },
      usage: {
        anyOf: [
          {
            additionalProperties: true,
            type: "object",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Usage",
      },
      timestamp: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Timestamp",
      },
    },
    required: ["content"],
    title: "ChatCompletedEvent",
    type: "object",
  },
  ChatErrorEvent: {
    properties: {
      type: {
        const: "chat.error",
        default: "chat.error",
        title: "Type",
        type: "string",
      },
      code: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Code",
      },
      message: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Message",
      },
    },
    title: "ChatErrorEvent",
    type: "object",
  },
  NewMessageEvent: {
    description: "Event khi có tin nhắn mới trong hội thoại.",
    properties: {
      type: {
        const: "new_message",
        default: "new_message",
        title: "Type",
        type: "string",
      },
      message: {
        additionalProperties: true,
        title: "Message",
        type: "object",
      },
    },
    required: ["message"],
    title: "NewMessageEvent",
    type: "object",
  },
  TypingIndicatorEvent: {
    description: "Event thông báo user đang gõ.",
    properties: {
      type: {
        const: "typing_indicator",
        default: "typing_indicator",
        title: "Type",
        type: "string",
      },
      user_id: {
        title: "User Id",
        type: "string",
      },
      is_typing: {
        title: "Is Typing",
        type: "boolean",
      },
      conversation_id: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Conversation Id",
      },
      timestamp: {
        title: "Timestamp",
        type: "string",
      },
    },
    required: ["user_id", "is_typing", "timestamp"],
    title: "TypingIndicatorEvent",
    type: "object",
  },
  ConversationHistoryEvent: {
    description: "Event trả lịch sử hội thoại.",
    properties: {
      type: {
        const: "conversation_history",
        default: "conversation_history",
        title: "Type",
        type: "string",
      },
      messages: {
        items: {
          additionalProperties: true,
          type: "object",
        },
        title: "Messages",
        type: "array",
      },
      conversation_id: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Conversation Id",
      },
      timestamp: {
        title: "Timestamp",
        type: "string",
      },
    },
    required: ["messages", "timestamp"],
    title: "ConversationHistoryEvent",
    type: "object",
  },
  StatusUpdatedEvent: {
    description: "Event cập nhật trạng thái người dùng.",
    properties: {
      type: {
        const: "status_updated",
        default: "status_updated",
        title: "Type",
        type: "string",
      },
      status: {
        title: "Status",
        type: "string",
      },
      timestamp: {
        title: "Timestamp",
        type: "string",
      },
    },
    required: ["status", "timestamp"],
    title: "StatusUpdatedEvent",
    type: "object",
  },
  TrainingProgressEvent: {
    description:
      "Training progress update.\n\nNote: field names dùng camelCase (jobId) để khớp Desktop schema.",
    properties: {
      type: {
        const: "training.progress",
        default: "training.progress",
        title: "Type",
        type: "string",
      },
      jobId: {
        title: "Jobid",
        type: "string",
      },
      progress: {
        title: "Progress",
        type: "integer",
      },
      message: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Message",
      },
    },
    required: ["jobId", "progress"],
    title: "TrainingProgressEvent",
    type: "object",
  },
  TrainingCompletedEvent: {
    properties: {
      type: {
        const: "training.completed",
        default: "training.completed",
        title: "Type",
        type: "string",
      },
      jobId: {
        title: "Jobid",
        type: "string",
      },
      progress: {
        anyOf: [
          {
            type: "integer",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Progress",
      },
      message: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Message",
      },
      artifactUrl: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Artifacturl",
      },
    },
    required: ["jobId"],
    title: "TrainingCompletedEvent",
    type: "object",
  },
  TrainingErrorEvent: {
    properties: {
      type: {
        const: "training.error",
        default: "training.error",
        title: "Type",
        type: "string",
      },
      jobId: {
        title: "Jobid",
        type: "string",
      },
      code: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Code",
      },
      message: {
        anyOf: [
          {
            type: "string",
          },
          {
            type: "null",
          },
        ],
        default: null,
        title: "Message",
      },
    },
    required: ["jobId"],
    title: "TrainingErrorEvent",
    type: "object",
  },
} as const;
export type WSEventType = keyof typeof WS_SCHEMAS;
