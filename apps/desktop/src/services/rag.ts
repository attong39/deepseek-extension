import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Omit from "Omit";
import RAG_INDEX from "RAG_INDEX";
import RAG_QUERY from "RAG_QUERY";
import RAG_SEARCH from "RAG_SEARCH";
import RagQueryRequest from "RagQueryRequest";
import RagResult from "RagResult";
import Record from "Record";

export type RagQueryRequest = {
  query: string;
  topK?: number;
  filters?: Record<string, unknown>;
};

export type RagResult = {
  text: string;
  source?: string;
  score?: number;
  meta?: Record<string, unknown>;
};

export async function ragQuery(req: RagQueryRequest): Promise<RagResult[]> {
  const { data } = await apiClient.post(API.RAG_QUERY, req);
  return data as RagResult[];
}

export async function ragIndex(
  documents: Array<{ id?: string; text: string }>,
): Promise<{ indexed: number }> {
  const { data } = await apiClient.post(API.RAG_INDEX, { documents });
  return data as { indexed: number };
}

export async function ragSearch(
  req: Omit<RagQueryRequest, "query"> & { text: string },
): Promise<RagResult[]> {
  const { data } = await apiClient.post(API.RAG_SEARCH, req);
  return data as RagResult[];
}
