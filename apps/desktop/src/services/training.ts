import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Record from "Record";
import TRAINING_JOB from "TRAINING_JOB";
import TRAINING_JOBS from "TRAINING_JOBS";
import TRAINING_JOB_CANCEL from "TRAINING_JOB_CANCEL";
import TRAINING_START from "TRAINING_START";
import TrainingJob from "TrainingJob";

export type TrainingJob = {
  id: string;
  status: "queued" | "running" | "succeeded" | "failed" | "canceled";
  createdAt?: string;
  updatedAt?: string;
  meta?: Record<string, unknown>;
};

export async function listJobs(): Promise<TrainingJob[]> {
  const { data } = await apiClient.get(API.TRAINING_JOBS);
  return data as TrainingJob[];
}

export async function getJob(jobId: string): Promise<TrainingJob> {
  const { data } = await apiClient.get(API.TRAINING_JOB(jobId));
  return data as TrainingJob;
}

export async function cancelJob(jobId: string): Promise<{ canceled: boolean }> {
  const { data } = await apiClient.post(API.TRAINING_JOB_CANCEL(jobId), {});
  return data as { canceled: boolean };
}

export async function startTraining(payload: Record<string, unknown>): Promise<TrainingJob> {
  const { data } = await apiClient.post(API.TRAINING_START, payload);
  return data as TrainingJob;
}
