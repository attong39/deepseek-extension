import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import FEEDBACK from "./FEEDBACK";
import FeedbackPayload from "FeedbackPayload";
import FeedbackResult from "FeedbackResult";
import Record from "Record";

export type FeedbackPayload = {
  rating: number; // 1..5
  comment?: string;
  context?: Record<string, unknown>;
};

export type FeedbackResult = { id: string; createdAt?: string };

export async function submitFeedback(payload: FeedbackPayload): Promise<FeedbackResult> {
  const { data } = await apiClient.post(API.FEEDBACK, payload);
  return data as FeedbackResult;
}
