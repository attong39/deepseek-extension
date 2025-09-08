import type { components } from "../api/generated/schema";
import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Backend from "Backend";
import DatasetInfo from "DatasetInfo";
import GET from "GET";
import JobStatus from "JobStatus";
import LEARNING_DATASETS from "LEARNING_DATASETS";
import LEARNING_INGEST_TEXT from "LEARNING_INGEST_TEXT";
import LEARNING_INGEST_URLS from "LEARNING_INGEST_URLS";
import LEARNING_JOBS from "LEARNING_JOBS";
import LearningJob from "LearningJob";
import OpenAPI from "OpenAPI";
import POST from "POST";
import Record from "Record";
import Types from "../Types/index";

// Types lấy từ OpenAPI (generated)
export type JobStatus = components["schemas"]["JobStatus"];
export type LearningJob = components["schemas"]["LearningJob"];
export type DatasetInfo = components["schemas"]["DatasetInfo"];

// POST /api/v1/learning/jobs
export async function startJob(config: Record<string, unknown>): Promise<LearningJob> {
  const { data } = await apiClient.post(API.LEARNING_JOBS, config);
  return data as LearningJob;
}

// GET /api/v1/learning/jobs/:id
export async function getJob(id: string): Promise<LearningJob> {
  const { data } = await apiClient.get(`${API.LEARNING_JOBS}/${encodeURIComponent(id)}`);
  return data as LearningJob;
}

// GET /api/v1/learning/jobs
export async function listJobs(params?: {
  status?: JobStatus;
  page?: number;
  pageSize?: number;
}): Promise<LearningJob[]> {
  const q: Record<string, unknown> = {};
  if (params?.status) {
    q.status = params.status;
    q.status_filter = params.status; // Backend compatibility
  }
  if (params?.page) q.page = params.page;
  if (params?.pageSize) q.page_size = params.pageSize;
  const { data } = await apiClient.get(API.LEARNING_JOBS, { params: q });
  return data as LearningJob[];
}

export async function listJobsMeta(params?: {
  status?: JobStatus;
  page?: number;
  pageSize?: number;
}): Promise<{
  items: LearningJob[];
  total: number | null;
  page: number | null;
  pageSize: number | null;
}> {
  const q: Record<string, unknown> = {};
  if (params?.status) {
    q.status = params.status;
    q.status_filter = params.status;
  }
  if (params?.page) q.page = params.page;
  if (params?.pageSize) q.page_size = params.pageSize;
  const resp = await apiClient.get(API.LEARNING_JOBS, { params: q });
  const items = resp.data as LearningJob[];
  const h = resp.headers ?? {};
  const total = h["x-total-count"] !== undefined ? Number(h["x-total-count"]) : null;
  const page = h["x-page"] !== undefined ? Number(h["x-page"]) : (params?.page ?? null);
  const pageSize =
    h["x-page-size"] !== undefined ? Number(h["x-page-size"]) : (params?.pageSize ?? null);
  return { items, total, page, pageSize };
}

// POST /api/v1/learning/jobs/:id/cancel
export async function cancelJob(id: string): Promise<{ ok: boolean }> {
  const { data } = await apiClient.post(`${API.LEARNING_JOBS}/${encodeURIComponent(id)}/cancel`);
  return data as { ok: boolean };
}

// POST /api/v1/learning/ingest/urls
export async function ingestUrls(
  urls: string[],
  opts?: { dataset?: string },
): Promise<{ job: LearningJob }> {
  const payload = { urls, ...(opts?.dataset ? { dataset: opts.dataset } : {}) };
  const { data } = await apiClient.post(API.LEARNING_INGEST_URLS, payload);
  return data as { job: LearningJob };
}

// POST /api/v1/learning/ingest/text
export async function ingestText(
  text: string,
  opts?: { dataset?: string },
): Promise<{ job: LearningJob }> {
  const payload = { text, ...(opts?.dataset ? { dataset: opts.dataset } : {}) };
  const { data } = await apiClient.post(API.LEARNING_INGEST_TEXT, payload);
  return data as { job: LearningJob };
}

// GET /api/v1/learning/datasets
export async function listDatasets(): Promise<DatasetInfo[]> {
  const { data } = await apiClient.get(API.LEARNING_DATASETS);
  return data as DatasetInfo[];
}
