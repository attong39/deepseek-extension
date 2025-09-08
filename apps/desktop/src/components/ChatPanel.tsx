import { Button, MenuItem, Paper, Select, Stack, TextField, Typography } from "@mui/material";
import type { SelectChangeEvent } from "@mui/material/Select";
import React, { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import type { ChatMessage } from "../hooks/useChat";
import { useChat } from "../hooks/useChat";
import type { AgentProfile } from "../services/agents";
import { agents } from "../services/agents";
import { memory } from "../services/memory";
import { subscribeWhisperPartial } from "../utils/whisper";
import AI from "AI";
import Agent from "Agent";
import ChangeEvent from "ChangeEvent";
import ChatPanel from "./ChatPanel";
import FormEvent from "FormEvent";
import HTMLInputElement from "HTMLInputElement";
import Memory from "../Memory/index";
import Model from "Model";
import Voice from "Voice";

export function ChatPanel() {
  const { t } = useTranslation();
  const { messages, loading, error, sendMessage } = useChat();
  const [text, setText] = useState("");
  const list = useMemo<AgentProfile[]>(() => agents.list(), []);
  const current = agents.current();
  const mem = memory.list(current?.id);
  const [voicePartial, setVoicePartial] = useState("");

  useEffect(() => {
    const unsub = subscribeWhisperPartial((txt) => {
      if (!txt) return;
      if (txt === "[end]") {
        // giữ nguyên transcript cuối cùng; không auto-send để tránh spam
        return;
      }
      setVoicePartial(txt);
    });
    return () => unsub?.();
  }, []);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    await sendMessage(text.trim());
    setText("");
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, maxWidth: 720 }}>
      <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
        <Typography variant="body2">Agent:</Typography>
        <Select
          size="small"
          defaultValue={current?.id ?? ""}
          onChange={(e: SelectChangeEvent<string>) =>
            agents.setCurrent((e.target.value as string) || null)
          }
        >
          <MenuItem value="">{t("chat.agentDefault", "(mặc định)")}</MenuItem>
          {list.map((a: AgentProfile) => (
            <MenuItem key={a.id} value={a.id}>
              {a.name}
            </MenuItem>
          ))}
        </Select>
        {current && (
          <Typography variant="caption" sx={{ color: "text.secondary" }}>
            Model: {current.model ?? "—"}
          </Typography>
        )}
      </Stack>
      <Stack direction="row" spacing={1}>
        <TextField
          value={text}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setText(e.target.value)}
          placeholder={t("chat.placeholder", "Nhập tin nhắn...")}
          size="small"
          fullWidth
        />
        <Button variant="contained" onClick={onSubmit as any} disabled={loading}>
          {t("chat.send", "Gửi")}
        </Button>
      </Stack>
      {voicePartial && (
        <Typography variant="caption" sx={{ mt: 0.5, color: "text.secondary" }}>
          Voice: {voicePartial}
        </Typography>
      )}
      {error && (
        <Typography color="error" sx={{ mt: 1 }}>
          Lỗi: {error}
        </Typography>
      )}
      {mem.length > 0 && (
        <Paper variant="outlined" sx={{ p: 1, mt: 1 }}>
          <Typography variant="subtitle2">Memory gần đây:</Typography>
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {mem.slice(-3).map((it) => (
              <li key={it.id}>
                {new Date(it.ts).toLocaleTimeString()} - {String((it as any).type)}
              </li>
            ))}
          </ul>
        </Paper>
      )}
      <ul style={{ listStyle: "none", padding: 0, marginTop: 12 }}>
        {messages.map((m: ChatMessage, i: number) => (
          <li key={`${m.timestamp}-${String(i)}`} style={{ marginBottom: 8 }}>
            <strong>{m.role === "user" ? "Bạn" : "AI"}:</strong> {m.content}
            <span style={{ color: "#999", marginLeft: 6, fontSize: 12 }}>
              {new Date(m.timestamp).toLocaleTimeString()}
            </span>
          </li>
        ))}
      </ul>
    </Paper>
  );
}
