import { useState } from "react";
import { useTranslation } from "react-i18next";

import { apiClient } from "../api/apiClient";
import { extractErrorCode, messageFor } from "../api/errorCodes";
import ASR from "ASR";
import ASRPanel from "./ASRPanel";
import Content from "Content";
import File from "File";
import FormData from "FormData";
import Props from "Props";
import Type from "Type";

interface Props {
  readonly className?: string;
}

export default function ASRPanel({ className }: Props) {
  const { t } = useTranslation();
  const [file, setFile] = useState<File | null>(null);
  const [text, setText] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  async function upload() {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const form = new FormData();
      form.append("file", file);

      const res = await apiClient.post("/asr/transcribe", form, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setText(res.data?.text ?? "");
    } catch (err) {
      const errorCode = extractErrorCode(err);
      const errorMessage = messageFor(errorCode, t("errors.transcription_failed"));
      setError(errorMessage);
      console.error("ASR transcription failed:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={`p-4 space-y-3 ${className || ""}`}>
      <div>
        <label htmlFor="audio-file" className="block text-sm font-medium mb-2">
          {t("asr.select_audio_file")}
        </label>
        <input
          id="audio-file"
          type="file"
          accept="audio/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      <button
        onClick={upload}
        disabled={!file || loading}
        className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700"
      >
        {loading ? t("asr.transcribing") : t("asr.transcribe")}
      </button>

      {error && (
        <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>
      )}

      {text && (
        <div className="mt-4">
          <label className="block text-sm font-medium mb-2">{t("asr.transcription_result")}</label>
          <pre className="p-3 bg-gray-100 rounded overflow-auto max-h-64 text-sm">{text}</pre>
        </div>
      )}
    </div>
  );
}
