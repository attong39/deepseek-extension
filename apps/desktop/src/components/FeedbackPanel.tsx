// jsx runtime from tsconfig (react-jsx)
import { useMemo, useState } from "react";

import { useChat } from "../hooks/useChat";
import { agents } from "../services/agents";
import { flush, recordInteraction, submitFeedbackWithStatus } from "../services/feedbackProcessor";
import AI from "AI";
import ChangeEvent from "ChangeEvent";
import Feedback from "Feedback";
import FeedbackPanel from "./FeedbackPanel";
import Flush from "Flush";
import Ghi from "Ghi";
import HTMLInputElement from "HTMLInputElement";
import HTMLSelectElement from "HTMLSelectElement";
import Parameters from "Parameters";
import Rating from "Rating";
import Record from "Record";

export function FeedbackPanel() {
  const { messages } = useChat();
  const [rating, setRating] = useState<Record<string, number | undefined>>({});
  const [comment, setComment] = useState<Record<string, string>>({});
  const current = agents.current();
  const sessionId = useMemo(() => (current?.id ? `agent:${current.id}` : "global"), [current?.id]);
  const [sending, setSending] = useState<Record<string, boolean>>({});
  const [done, setDone] = useState<Record<string, boolean>>({});
  const [forbidden, setForbidden] = useState<Record<string, boolean>>({});
  const [acceptedCount, setAcceptedCount] = useState<Record<string, number>>({});

  const onSubmit = async (id: string, role: string, content: string) => {
    const r = rating[id];
    const c = comment[id];
    setSending((s: Record<string, boolean>) => ({ ...s, [id]: true }));
    setDone((s: Record<string, boolean>) => ({ ...s, [id]: false }));
    setForbidden((s: Record<string, boolean>) => ({ ...s, [id]: false }));
    const payload: Parameters<typeof submitFeedbackWithStatus>[0] = {
      messageId: id,
      sessionId,
      tags: [role],
      ...(r !== undefined ? { rating: r } : {}),
      ...(c ? { comment: c } : {}),
    };
    const res = await submitFeedbackWithStatus(payload);
    setSending((s: Record<string, boolean>) => ({ ...s, [id]: false }));
    setDone((s: Record<string, boolean>) => ({ ...s, [id]: res.ok }));
    setForbidden((s: Record<string, boolean>) => ({
      ...s,
      [id]: res.forbidden,
    }));
    recordInteraction({
      sessionId,
      agentId: current?.id ?? null,
      userText: role === "user" ? content : "",
      aiText: role !== "user" ? content : "",
      ...(r !== undefined ? { rating: r } : {}),
      ...(c ? { comment: c } : {}),
      timestamp: Date.now(),
    });
    // Flush ngay để có số lượng accepted từ server (nếu batch đầy hoặc flush bắt buộc)
    try {
      const res = await flush();
      setAcceptedCount((s: Record<string, number>) => ({
        ...s,
        [id]: res.accepted,
      }));
    } catch {
      // ignore
    }
    setComment((s: Record<string, string>) => ({ ...s, [id]: "" }));
  };

  const last10 = useMemo(() => messages.slice(-10), [messages]);

  return (
    <div style={{ border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
      <h3 style={{ marginTop: 0 }}>Feedback</h3>
      <ul
        style={{
          listStyle: "none",
          padding: 0,
          margin: 0,
          display: "grid",
          gap: 8,
        }}
      >
        {last10.map((m) => {
          const key = m.id ? String(m.id) : `${m.role}-${String(m.timestamp)}`;
          return (
            <li
              key={key}
              style={{
                border: "1px solid #f0f0f0",
                padding: 8,
                borderRadius: 6,
              }}
            >
              <div style={{ marginBottom: 6 }}>
                <strong>{m.role === "user" ? "Bạn" : "AI"}:</strong> {m.content}
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  flexWrap: "wrap",
                }}
              >
                <label htmlFor={`rating-${key}`}>Rating:</label>
                <select
                  id={`rating-${key}`}
                  value={rating[key] ?? ""}
                  onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                    setRating((s: Record<string, number | undefined>) => ({
                      ...s,
                      [key]: e.target.value ? Number(e.target.value) : undefined,
                    }))
                  }
                >
                  <option value="">—</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                </select>
                <input
                  placeholder="Nhận xét..."
                  value={comment[key] ?? ""}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setComment((s: Record<string, string>) => ({
                      ...s,
                      [key]: e.target.value,
                    }))
                  }
                  style={{ flex: "1 1 240px" }}
                />
                <button
                  onClick={() => void onSubmit(key, m.role, m.content)}
                  disabled={sending[key] === true}
                >
                  {sending[key] ? "Đang gửi…" : "Gửi"}
                </button>
                {done[key] && <span style={{ color: "green" }}>Đã gửi</span>}
                {typeof acceptedCount[key] === "number" && acceptedCount[key] > 0 && (
                  <span style={{ color: "gray" }}>Ghi {acceptedCount[key]} interaction(s)</span>
                )}
                {forbidden[key] && (
                  <span style={{ color: "crimson" }}>Thiếu quyền (feedback:write)</span>
                )}
                {!done[key] && !sending[key] && (
                  <button onClick={() => void onSubmit(key, m.role, m.content)}>Thử lại</button>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
