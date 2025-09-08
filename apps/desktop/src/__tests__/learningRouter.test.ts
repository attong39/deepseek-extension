import { HashRouter, NavLink, Link, Routes, Route } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { apiClient } from "../api/apiClient";
import { API } from "../constants";
import { ingestText, ingestUrls, listJobs } from "../services/learningRouter";
import Hello from "Hello";
import LEARNING_INGEST_TEXT from "LEARNING_INGEST_TEXT";
import LEARNING_INGEST_URLS from "LEARNING_INGEST_URLS";
import LEARNING_JOBS from "LEARNING_JOBS";
import ReturnType from "ReturnType";

vi.mock("../api/apiClient", () => {
  return {
    apiClient: {
      get: vi.fn(),
      post: vi.fn(),
    },
  };
});

describe("learningRouter API", () => {
  beforeEach(() => {
    (apiClient.get as unknown as ReturnType<typeof vi.fn>).mockReset();
    (apiClient.post as unknown as ReturnType<typeof vi.fn>).mockReset();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("listJobs passes status and status_filter when filtering", async () => {
    (apiClient.get as any).mockResolvedValue({ data: [] });
    await listJobs({ status: "queued" as any });
    expect(apiClient.get).toHaveBeenCalledTimes(1);
    const [url, opts] = (apiClient.get as any).mock.calls[0];
    expect(url).toBe(API.LEARNING_JOBS);
    expect(opts?.params).toMatchObject({
      status: "queued",
      status_filter: "queued",
    });
  });

  it("ingestText posts correct path and payload", async () => {
    (apiClient.post as any).mockResolvedValue({
      data: { job: { id: "j1", status: "queued" } },
    });
    const res = await ingestText("Hello", { dataset: "ds1" });
    expect(apiClient.post).toHaveBeenCalledWith(API.LEARNING_INGEST_TEXT, {
      text: "Hello",
      dataset: "ds1",
    });
    expect(res.job.id).toBe("j1");
  });

  it("ingestUrls posts correct path and payload", async () => {
    (apiClient.post as any).mockResolvedValue({
      data: { job: { id: "j2", status: "queued" } },
    });
    const urls = ["https://a.com", "https://b.com"];
    const res = await ingestUrls(urls, { dataset: "ds2" });
    expect(apiClient.post).toHaveBeenCalledWith(API.LEARNING_INGEST_URLS, {
      urls,
      dataset: "ds2",
    });
    expect(res.job.id).toBe("j2");
  });
});
