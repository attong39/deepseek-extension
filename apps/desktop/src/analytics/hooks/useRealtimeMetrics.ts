import { useEffect, useRef, useState } from "react";

import { getConfig } from "@/services/config";
import Fallback from "Fallback";
import Math from "Math";
import Metrics from "Metrics";
import WS from "WS";
import WebSocket from "WebSocket";

type Metrics = { 
  cpu: number; 
  ramUsedGb: number; 
  wsLatencyMs: number;
};

const initialMetrics: Metrics = { 
  cpu: 0, 
  ramUsedGb: 0, 
  wsLatencyMs: 0 
};

export function useRealtimeMetrics() {
  const [metrics, setMetrics] = useState<Metrics>(initialMetrics);
  const timerRef = useRef<number | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const config = getConfig();

    // Fallback timer (demo) để không phụ thuộc backend ngay
    timerRef.current = window.setInterval(() => {
      setMetrics(prev => ({
        cpu: Math.max(0, Math.min(100, (prev.cpu * 0.6) + Math.random() * 40)),
        ramUsedGb: 4 + Math.random() * 4,
        wsLatencyMs: Math.round(50 + Math.random() * 50),
      }));
    }, 1000);

    // Nếu có WS health, kết nối và override số liệu khi có message
    try {
      const wsUrl = `ws://${location.host}${config.wsHealthPath || '/ws/health'}`;
      wsRef.current = new WebSocket(wsUrl);
      const startTime = Date.now();
      
      wsRef.current.onopen = () => {
        setMetrics(prev => ({ 
          ...prev, 
          wsLatencyMs: Date.now() - startTime 
        }));
      };
      
      wsRef.current.onmessage = (event) => {
        // expecting {cpu, ramUsedGb, latencyMs}
        try {
          const data = JSON.parse(event.data);
          setMetrics(prev => ({
            cpu: typeof data.cpu === "number" ? data.cpu : prev.cpu,
            ramUsedGb: typeof data.ramUsedGb === "number" ? data.ramUsedGb : prev.ramUsedGb,
            wsLatencyMs: typeof data.latencyMs === "number" ? data.latencyMs : prev.wsLatencyMs,
          }));
        } catch {
          // ignore malformed messages
        }
      };
      
      wsRef.current.onerror = () => {
        // WebSocket connection failed, fallback timer will continue
      };
    } catch {
      // WebSocket not available, fallback timer will continue
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return metrics;
}
