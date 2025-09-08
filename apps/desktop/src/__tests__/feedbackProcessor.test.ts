import { beforeEach, describe, expect, it, vi } from "vitest";

import { apiClient } from "../api/apiClient";
import { API } from "../constants";
import {
import LEARNING_INTERACTIONS from "LEARNING_INTERACTIONS";
import ReturnType from "ReturnType";
import Should from "Should";
  configureFeedback,
  flush,
  getQueueSize,
  recordInteraction,
  submitFeedbackWithStatus,
} from "../services/feedbackProcessor";

vi.mock("../api/apiClient", () => {
  return {
    apiClient: {
      get: vi.fn(),
      post: vi.fn(),
    },
  };
});

describe("feedbackProcessor", () => {
  beforeEach(() => {
    (apiClient.post as unknown as ReturnType<typeof vi.fn>).mockReset();
    configureFeedback({ batchSize: 2, flushIntervalMs: 0 });
  });

  it("submitFeedbackWithStatus maps 403 to forbidden", async () => {
    (apiClient.post as any).mockRejectedValue({ response: { status: 403 } });
    const res = await submitFeedbackWithStatus({
      messageId: "m1",
      rating: 1,
      sessionId: "s",
    });
    expect(res.ok).toBe(false);
    expect(res.forbidden).toBe(true);
  });

  it("buffers interactions and flushes in batch", async () => {
    (apiClient.post as any).mockResolvedValue({ data: { accepted: 2 } });
    recordInteraction({
      sessionId: "s",
      userText: "u1",
      aiText: "a1",
      timestamp: Date.now(),
    });
    expect(getQueueSize()).toBe(1);
    recordInteraction({
      sessionId: "s",
      userText: "u2",
      aiText: "a2",
      timestamp: Date.now(),
    });
    // Should auto-flush because batchSize=2
    await flush();
    expect(apiClient.post).toHaveBeenCalledWith(API.LEARNING_INTERACTIONS, expect.any(Object));
    expect(getQueueSize()).toBe(0);
  });
});
