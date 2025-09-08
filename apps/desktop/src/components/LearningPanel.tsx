import { useEffect, useMemo, useState } from "react";
import { HashRouter, NavLink, Link, Routes, Route } from "react-router-dom";

// React types are available globally via @types/react with react-jsx runtime
import type { DatasetInfo, JobStatus, LearningJob } from "../services/learningRouter";
import { listDatasets, listJobsMeta } from "../services/learningRouter";
import All from "All";
import ChangeEvent from "ChangeEvent";
import Datasets from "Datasets";
import Error from "Error";
import HTMLSelectElement from "HTMLSelectElement";
import Jobs from "Jobs";
import Learning from "Learning";
import LearningPanel from "./LearningPanel";
import Math from "Math";
import Next from "Next";
import No from "No";
import Page from "Page";
import Prev from "Prev";
import Readonly from "Readonly";
import Refresh from "Refresh";
import Refreshing from "Refreshing";
import Status from "../pages/Status";
import StatusBadge from "StatusBadge";

export function LearningPanel() {
  const [jobs, setJobs] = useState<LearningJob[]>([]);
  const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
  const [loadingJobs, setLoadingJobs] = useState(false);
  const [loadingDatasets, setLoadingDatasets] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<JobStatus | "">("");
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [total, setTotal] = useState<number | null>(null);

  const refreshJobs = async () => {
    setLoadingJobs(true);
    setError(null);
    try {
      const meta = await listJobsMeta({
        ...(statusFilter ? { status: statusFilter } : {}),
        page,
        pageSize,
      });
      setJobs(meta.items);
      setTotal(meta.total);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoadingJobs(false);
    }
  };

  const refreshDatasets = async () => {
    setLoadingDatasets(true);
    setError(null);
    try {
      const data = await listDatasets();
      setDatasets(data);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoadingDatasets(false);
    }
  };

  useEffect(() => {
    void refreshJobs();
    void refreshDatasets();
  }, []);

  useEffect(() => {
    setPage(1);
    void refreshJobs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  const sortedJobs = useMemo(
    () =>
      [...jobs].sort((a, b) =>
        (b.updated_at || b.created_at || "").localeCompare(a.updated_at || a.created_at || ""),
      ),
    [jobs],
  );

  const totalPages = Math.max(1, Math.ceil((total ?? sortedJobs.length) / pageSize));
  const pageJobs = sortedJobs; // server đã paging, chỉ sort để hiển thị ổn định

  return (
    <div style={{ border: "1px solid #eee", padding: 12, borderRadius: 8 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          flexWrap: "wrap",
        }}
      >
        <h3 style={{ margin: 0 }}>Learning</h3>
        <button onClick={() => void refreshJobs()} disabled={loadingJobs}>
          {loadingJobs ? "Refreshing jobs…" : "Refresh jobs"}
        </button>
        <button onClick={() => void refreshDatasets()} disabled={loadingDatasets}>
          {loadingDatasets ? "Refreshing datasets…" : "Refresh datasets"}
        </button>
        <label style={{ marginLeft: "auto" }}>
          Status:
          <select
            value={statusFilter}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
              const v = e.target.value;
              if (v === "") setStatusFilter("");
              else setStatusFilter(v as JobStatus);
            }}
            style={{ marginLeft: 6 }}
          >
            <option value="">All</option>
            <option value="queued">queued</option>
            <option value="running">running</option>
            <option value="completed">completed</option>
            <option value="failed">failed</option>
            <option value="canceled">canceled</option>
          </select>
        </label>
        <label>
          Page size:
          <select
            value={pageSize}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
              setPageSize(Number(e.target.value))
            }
            style={{ marginLeft: 6 }}
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
          </select>
        </label>
        {error && <span style={{ color: "crimson", marginLeft: "auto" }}>Error: {error}</span>}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 12,
          marginTop: 12,
        }}
      >
        <div>
          <h4 style={{ marginTop: 0 }}>Jobs</h4>
          <ul style={{ margin: 0, paddingLeft: 16 }}>
            {pageJobs.map((j) => (
              <li key={j.id}>
                <span>
                  <strong>{j.id}</strong> — <StatusBadge status={j.status} />
                  {j.dataset ? ` — ${j.dataset}` : ""}
                </span>
                <div style={{ opacity: 0.7, fontSize: 12 }}>{j.updated_at || j.created_at}</div>
              </li>
            ))}
            {sortedJobs.length === 0 && <li style={{ opacity: 0.7 }}>No jobs</li>}
          </ul>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              marginTop: 8,
            }}
          >
            <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page <= 1}>
              Prev
            </button>
            <span>
              Page {page} / {totalPages}
              {typeof total === "number" ? ` (total ${total})` : ""}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
            >
              Next
            </button>
          </div>
        </div>

        <div>
          <h4 style={{ marginTop: 0 }}>Datasets</h4>
          <ul style={{ margin: 0, paddingLeft: 16 }}>
            {datasets.map((d) => (
              <li key={d.id}>
                <strong>{d.name}</strong>
                {typeof d.size === "number" ? ` — ${d.size} items` : ""}
                {d.description ? <div style={{ opacity: 0.8 }}>{d.description}</div> : null}
              </li>
            ))}
            {datasets.length === 0 && <li style={{ opacity: 0.7 }}>No datasets</li>}
          </ul>
        </div>
      </div>
    </div>
  );
}

function StatusBadge({ status }: Readonly<{ status: LearningJob["status"] }>) {
  const colorMap = {
    completed: "green",
    running: "dodgerblue",
    failed: "crimson",
    canceled: "gray",
    queued: "orange",
  } as const;
  const isKey = (s: string): s is keyof typeof colorMap => s in colorMap;
  const key = isKey(status as string) ? (status as keyof typeof colorMap) : "queued";
  const color = colorMap[key];
  return <span style={{ color, fontWeight: 600 }}>{status}</span>;
}
