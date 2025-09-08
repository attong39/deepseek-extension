import { Chip, Tooltip } from "@mui/material";
import React from "react";

import { httpMeta } from "../services/httpMeta";
import Element from "Element";
import JSX from "JSX";
import Math from "Math";
import Rate from "Rate";
import RateLimitBadge from "./RateLimitBadge";
import Tick from "Tick";

function secondsUntilReset(): number | null {
  const reset = httpMeta.get().rateLimit?.reset; // epoch seconds
  if (!reset) return null;
  const now = Math.floor(Date.now() / 1000);
  return Math.max(0, reset - now);
}

export function RateLimitBadge(): JSX.Element | null {
  // Tick để refresh mỗi giây
  const [, setTick] = React.useState(0);
  React.useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const meta = httpMeta.get();
  const rl = meta.rateLimit;
  if (rl?.limit == null || rl?.remaining == null) return null;

  const secs = secondsUntilReset();
  const label = `${rl.remaining}/${rl.limit}${typeof secs === "number" ? ` · ${secs}s` : ""}`;
  const titleParts = [
    `Rate limit`,
    `remaining=${rl.remaining}/${rl.limit}`,
    rl.window != null ? `window=${rl.window}s` : null,
    rl.reset != null ? `reset=${new Date(rl.reset * 1000).toLocaleTimeString()}` : null,
    meta.requestId ? `request_id=${meta.requestId}` : null,
    meta.traceId ? `trace_id=${meta.traceId}` : null,
  ].filter(Boolean);

  const color: "default" | "error" = rl.remaining > 0 ? "default" : "error";

  return (
    <Tooltip title={titleParts.join(" | ")}>
      <Chip size="small" label={label} color={color} variant="outlined" sx={{ ml: 1 }} />
    </Tooltip>
  );
}

export default RateLimitBadge;
