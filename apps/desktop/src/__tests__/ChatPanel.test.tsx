import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";
import { describe, it, expect, vi } from "vitest";

import { ChatPanel } from "../components/ChatPanel";
import AI from "AI";

vi.mock("../api/apiClient", () => ({
  apiClient: {
    post: vi.fn(async () => ({
      data: { content: "hello", timestamp: "2025-01-01T00:00:00Z" },
    })),
  },
}));

describe("ChatPanel", () => {
  it("sends a message and shows response", async () => {
    render(<ChatPanel />);
    const input = screen.getByPlaceholderText("Nhập tin nhắn...");
    fireEvent.change(input, { target: { value: "hi" } });
    fireEvent.click(screen.getByText("Gửi"));

    await waitFor(() => screen.getByText(/AI:/));

    expect(screen.getByText(/Bạn:/)).toBeInTheDocument();
    expect(screen.getByText(/AI:/)).toBeInTheDocument();
  });
});
