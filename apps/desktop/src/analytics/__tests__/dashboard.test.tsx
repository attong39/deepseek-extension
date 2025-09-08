import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Dashboard from "@/analytics/components/Dashboard";
import Analytics from "../index";
import CPU from "CPU";
import Check from "Check";
import Connection from "Connection";
import Consumption from "Consumption";
import Health from "Health";
import Latency from "Latency";
import Memory from "../../Memory/index";
import Performance from "Performance";
import RAM from "RAM";
import Should from "Should";
import System from "System";
import Usage from "Usage";
import Used from "Used";
import WebSocket from "WebSocket";

describe("Analytics Dashboard", () => {
  it("renders three metric cards with proper labels", () => {
    render(<Dashboard />);
    
    // Check for metric card labels
    expect(screen.getByText(/CPU Usage/i)).toBeInTheDocument();
    expect(screen.getByText(/RAM Used/i)).toBeInTheDocument();
    expect(screen.getByText(/WebSocket Latency/i)).toBeInTheDocument();
  });

  it("displays metric descriptions", () => {
    render(<Dashboard />);
    
    // Check for metric descriptions
    expect(screen.getByText(/System Performance/i)).toBeInTheDocument();
    expect(screen.getByText(/Memory Consumption/i)).toBeInTheDocument();
    expect(screen.getByText(/Connection Health/i)).toBeInTheDocument();
  });

  it("shows percentage for CPU usage", () => {
    render(<Dashboard />);
    
    // Should display CPU percentage (could be 0.0% initially)
    const cpuElements = screen.getAllByText(/%$/);
    expect(cpuElements.length).toBeGreaterThan(0);
  });
});
