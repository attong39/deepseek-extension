import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Blob from "Blob";
import Content from "Content";
import FormData from "FormData";
import Type from "Type";
import VOICE_STT from "VOICE_STT";
import VOICE_TTS from "VOICE_TTS";

export async function tts(text: string, voice = "default"): Promise<Blob> {
  const { data } = await apiClient.post(API.VOICE_TTS, { text, voice }, { responseType: "blob" });
  return data as Blob;
}

export async function stt(audio: Blob): Promise<{ text: string }> {
  const form = new FormData();
  form.append("audio", audio);
  const { data } = await apiClient.post(API.VOICE_STT, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data as { text: string };
}
