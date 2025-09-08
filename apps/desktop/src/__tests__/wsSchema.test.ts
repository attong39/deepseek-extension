import { describe, expect, it } from "vitest";

import { validateWsMessage } from "../services/wsSchema";

const msgs = {
  newMessage: {
    type: "new_message",
    message: {
      id: "m1",
      content: "hello",
      user_id: "u1",
      conversation_id: "c1",
      timestamp: "2025-01-01T00:00:00Z",
    },
  },
  typing: {
    type: "typing_indicator",
    user_id: "u1",
    is_typing: true,
    conversation_id: "c1",
    timestamp: "2025-01-01T00:00:00Z",
  },
  history: {
    type: "conversation_history",
    messages: [
      {
        id: "m1",
        content: "hello",
        user_id: "u1",
        conversation_id: "c1",
        timestamp: "2025-01-01T00:00:00Z",
      },
    ],
    conversation_id: "c1",
    timestamp: "2025-01-01T00:00:00Z",
  },
  status: {
    type: "status_updated",
    status: "online",
    timestamp: "2025-01-01T00:00:00Z",
  },
};

describe("wsSchema validators", () => {
  it("validates new_message", () => {
    expect(validateWsMessage(msgs.newMessage)).toBe(true);
  });
  it("validates typing_indicator", () => {
    expect(validateWsMessage(msgs.typing)).toBe(true);
  });
  it("validates conversation_history", () => {
    expect(validateWsMessage(msgs.history)).toBe(true);
  });
  it("validates status_updated", () => {
    expect(validateWsMessage(msgs.status)).toBe(true);
  });
});
