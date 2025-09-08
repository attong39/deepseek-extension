import { useEffect, useState } from "react";

import { getHealth, type HealthReport } from "@/services/health";
import API from "../../API/index";
import App from "../../App";
import HealthBadge from "./HealthBadge";
import HealthReport from "HealthReport";
import WS from "WS";

const dotCls = (ok: boolean) =>
  `inline-block w-2 h-2 rounded-full ${ok ? "bg-emerald-500" : "bg-red-500"}`;

export function HealthBadge() {
  const [h, setH] = useState<HealthReport | null>(null);
  const [last, setLast] = useState<string>("");

  useEffect(() => {
    let alive = true;
    const tick = async () => {
      try {
        const rep = await getHealth();
        if (alive) { setH(rep); setLast(new Date().toLocaleTimeString()); }
      } catch { /* giữ state cũ */ }
    };
    tick(); // chạy ngay
    const id = window.setInterval(tick, 30_000); // mỗi 30s
    return () => { alive = false; clearInterval(id); };
  }, []);

  let wrapCls: string;
  if (h?.level === "ok") {
    wrapCls = "text-emerald-400";
  } else if (h?.level === "degraded") {
    wrapCls = "text-amber-400";
  } else {
    wrapCls = "text-red-400";
  }

  return (
    <div className={`text-xs flex items-center gap-3 ${wrapCls}`}>
      <span className="flex items-center gap-1">
        <span className={dotCls(!!h?.server.http)} /> API
      </span>
      <span className="flex items-center gap-1">
        <span className={dotCls(!!h?.server.ws)} /> WS
      </span>
      <span className="flex items-center gap-1">
        <span className={dotCls(!!h?.main.ok)} /> App
      </span>
      {last && <span className="text-[10px] opacity-70">cập nhật {last}</span>}
    </div>
  );
}
