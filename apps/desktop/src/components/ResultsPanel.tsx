// jsx runtime from tsconfig (react-jsx)
import React from "react";

import { ragQuery, type RagResult } from "../services/rag";
import { useSearchStore, type SearchState } from "../stores/searchStore";
import ChangeEvent from "ChangeEvent";
import HTMLInputElement from "HTMLInputElement";
import RAG from "RAG";
import RagResult from "RagResult";
import Results from "Results";
import ResultsPanel from "./ResultsPanel";
import Search from "Search";
import SearchState from "SearchState";
import Wikipedia from "Wikipedia";

export function ResultsPanel() {
  const wiki = useSearchStore((s: SearchState) => s.wiki);
  const arxiv = useSearchStore((s: SearchState) => s.arxiv);
  const [q, setQ] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [rag, setRag] = React.useState<RagResult[]>([]);
  const [err, setErr] = React.useState<string | null>(null);

  async function onRagSearch() {
    if (!q.trim()) return;
    setLoading(true);
    setErr(null);
    try {
      const data = await ragQuery({ query: q.trim(), topK: 5 });
      setRag(data);
    } catch (e: any) {
      setErr(e?.message || "RAG query thất bại");
    } finally {
      setLoading(false);
    }
  }

  if (!wiki && (!arxiv || arxiv.length === 0)) return null;

  return (
    <div style={{ border: "1px dashed #ccc", padding: 12, borderRadius: 8 }}>
      <h4 style={{ marginTop: 0 }}>Search Results</h4>
      {/* RAG quick box (tối giản, không đổi layout lớn) */}
      <div
        style={{
          display: "flex",
          gap: 8,
          alignItems: "center",
          marginBottom: 8,
        }}
      >
        <input
          placeholder="Hỏi RAG..."
          value={q}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQ(e.target.value)}
        />
        <button disabled={loading || !q.trim()} onClick={onRagSearch}>
          Tìm
        </button>
        {loading && <span>Đang tìm…</span>}
        {err && <span style={{ color: "crimson" }}>{err}</span>}
      </div>
      {rag.length > 0 && (
        <div style={{ marginBottom: 8 }}>
          <strong>Kết quả RAG</strong>
          <ol>
            {rag.map((r) => (
              <li key={`${r.source ?? ""}-${r.text.slice(0, 64)}`}>
                <div>{r.text}</div>
                <small>
                  {r.source ? `source: ${r.source}` : ""}
                  {typeof r.score === "number" ? ` · score: ${r.score.toFixed(3)}` : ""}
                </small>
              </li>
            ))}
          </ol>
        </div>
      )}
      {wiki && (
        <div style={{ marginBottom: 8 }}>
          <strong>Wikipedia</strong>
          <ul>
            {(wiki[1] ?? []).slice(0, 5).map((title: string, i: number) => {
              const link = wiki[3]?.[i] as string | undefined;
              const key = link || `${title}-${i}`;
              return (
                <li key={key}>
                  {link ? (
                    <a href={link} target="_blank" rel="noreferrer">
                      {title}
                    </a>
                  ) : (
                    title
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}
      {arxiv && arxiv.length > 0 && (
        <div>
          <strong>arXiv</strong>
          <ul>
            {arxiv.slice(0, 5).map((p) => (
              <li key={p.id}>
                <a href={p.link} target="_blank" rel="noreferrer">
                  {p.title}
                </a>
                {p.authors?.length ? ` — ${p.authors.join(", ")}` : ""}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
