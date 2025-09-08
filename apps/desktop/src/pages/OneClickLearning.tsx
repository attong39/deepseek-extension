// apps/desktop/src/pages/OneClickLearning.tsx
import React, { useEffect, useRef, useState } from "react";
import { connectRagWS, ChatClientMsg, ChatServerMsg } from "../lib/ws/rag";
import Chat from "./Chat";
import Click from "Click";
import Enter from "Enter";
import HTMLInputElement from "HTMLInputElement";
import Learning from "Learning";
import One from "One";
import OneClickLearning from "./OneClickLearning";
import RAG from "RAG";
import WS from "WS";
import WebSocket from "WebSocket";

export default function OneClickLearning() {
  const [log, setLog] = useState<string[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  // ---- open WS once ----
  useEffect(() => {
    const ws = connectRagWS();
    wsRef.current = ws;

    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data) as ChatServerMsg;
      if (msg.type === "token") setLog((l) => [...l, msg.text ?? ""]);
      if (msg.type === "error") setLog((l) => [...l, `❗️${msg.error}`]);
    };

    return () => ws.close();
  }, []);

  // ---- send message ----
  const send = (txt: string) => {
    const m: ChatClientMsg = { type: "user_message", id: crypto.randomUUID(), text: txt };
    wsRef.current?.send(JSON.stringify(m));
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl font-bold">One‑Click Learning (RAG Chat)</h1>

      <div className="flex gap-2">
        <input
          className="flex-1 border rounded px-2 py-1"
          placeholder="Hỏi gì đó..."
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              const v = (e.target as HTMLInputElement).value;
              send(v);
              (e.target as HTMLInputElement).value = "";
            }
          }}
        />
        <button
          className="px-3 py-1 rounded bg-indigo-600 text-white"
          onClick={() => {
            const inp = document.querySelector("input") as HTMLInputElement;
            if (inp?.value) {
              send(inp.value);
              inp.value = "";
            }
          }}
        >
          Gửi
        </button>
      </div>

      <div className="border rounded p-2 h-64 overflow-auto whitespace-pre-wrap bg-gray-50">
        {log.join(" ")}
      </div>
    </div>
  );
}
