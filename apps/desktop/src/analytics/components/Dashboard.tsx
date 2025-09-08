import { useRealtimeMetrics } from "../hooks/useRealtimeMetrics";
import CPU from "CPU";
import Connection from "Connection";
import Consumption from "Consumption";
import Dashboard from "./Dashboard";
import GB from "GB";
import Health from "Health";
import Latency from "Latency";
import Memory from "../../Memory/index";
import Performance from "Performance";
import RAM from "RAM";
import System from "System";
import Usage from "Usage";
import Used from "Used";
import WebSocket from "WebSocket";

export default function Dashboard() {
  const metrics = useRealtimeMetrics();

  return (
    <div className="p-4 grid gap-4 md:grid-cols-3">
      <div className="rounded-2xl p-4 shadow bg-card">
        <div className="text-xs opacity-70">CPU Usage</div>
        <div className="text-2xl font-semibold">{metrics.cpu.toFixed(1)}%</div>
        <div className="text-xs text-green-600">System Performance</div>
      </div>
      
      <div className="rounded-2xl p-4 shadow bg-card">
        <div className="text-xs opacity-70">RAM Used</div>
        <div className="text-2xl font-semibold">{metrics.ramUsedGb.toFixed(2)} GB</div>
        <div className="text-xs text-blue-600">Memory Consumption</div>
      </div>
      
      <div className="rounded-2xl p-4 shadow bg-card">
        <div className="text-xs opacity-70">WebSocket Latency</div>
        <div className="text-2xl font-semibold">{metrics.wsLatencyMs} ms</div>
        <div className="text-xs text-purple-600">Connection Health</div>
      </div>
    </div>
  );
}
