import { useCallback, useEffect, useRef, useState } from "react";
import SpeechRecognition from "SpeechRecognition";
import VN from "VN";
import VoiceState from "VoiceState";

export type VoiceState = {
  listening: boolean;
  transcript: string;
  error: string | null;
};

export function useVoice() {
  const [state, setState] = useState<VoiceState>({
    listening: false,
    transcript: "",
    error: null,
  });
  const recRef = useRef<any>(null);

  const start = useCallback(() => {
    try {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setState((s) => ({ ...s, error: "SpeechRecognition not supported" }));
        return;
      }
      const rec = new SpeechRecognition();
      rec.lang = "vi-VN";
      rec.continuous = true;
      rec.interimResults = true;
      rec.onresult = (e: any) => {
        let text = "";
        for (let i = e.resultIndex; i < e.results.length; i++) {
          text += e.results[i][0].transcript;
        }
        setState((s) => ({ ...s, transcript: text }));
      };
      rec.onerror = (e: any) =>
        setState((s) => ({ ...s, error: String(e?.error || "voice error") }));
      rec.onend = () => setState((s) => ({ ...s, listening: false }));
      rec.start();
      recRef.current = rec;
      setState((s) => ({ ...s, listening: true, error: null }));
    } catch (e: any) {
      setState((s) => ({ ...s, error: e?.message || "voice init failed" }));
    }
  }, []);

  const stop = useCallback(() => {
    try {
      recRef.current?.stop?.();
    } finally {
      setState((s) => ({ ...s, listening: false }));
    }
  }, []);

  useEffect(() => () => recRef.current?.stop?.(), []);

  return { ...state, start, stop };
}
