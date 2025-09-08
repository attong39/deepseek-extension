import { create } from "zustand";

import type { ArXivEntry } from "../api/apiClient";
import SearchState from "SearchState";
import WikiResult from "WikiResult";

export type WikiResult = [string, string[], string[], string[]];

export interface SearchState {
  wiki: WikiResult | null;
  arxiv: ArXivEntry[];
  setWiki: (r: WikiResult | null) => void;
  setArxiv: (r: ArXivEntry[]) => void;
}

export const useSearchStore = create<SearchState>((set) => ({
  wiki: null,
  arxiv: [],
  setWiki: (wiki: WikiResult | null) => set({ wiki }),
  setArxiv: (arxiv: ArXivEntry[]) => set({ arxiv }),
}));
