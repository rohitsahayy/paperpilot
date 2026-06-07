"use client";

import { useState, type KeyboardEvent } from "react";
import { Search, Loader2 } from "lucide-react";
import Sidebar from "@/components/Sidebar";
import ResultsPanel from "@/components/ResultsPanel";

export interface Source {
  source_label: string;
  source: string;
  urls: string[];
  summary: string;
}

export interface ResearchResult {
  brief: string;
  sources: Source[];
  query: string;
  status: string;
}

type AppState = "idle" | "loading" | "results" | "error";

const SUGGESTIONS = [
  "Large language models 2024",
  "Quantum computing progress",
  "CRISPR gene editing",
  "Climate change solutions",
  "Transformer architecture",
];

export default function Home() {
  const [query, setQuery] = useState("");
  const [audience, setAudience] = useState("Academic Researchers");
  const [researchType, setResearchType] = useState("Comprehensive");
  const [pageLength, setPageLength] = useState(1000);
  const [appState, setAppState] = useState<AppState>("idle");
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [error, setError] = useState("");

  async function handleResearch() {
    if (!query.trim() || appState === "loading") return;
    setAppState("loading");
    setError("");
    setResult(null);

    try {
      const base =
        process.env.NEXT_PUBLIC_API_URL ||
        "https://paperpilot-api-lm7r.onrender.com";
      const res = await fetch(`${base}/api/v1/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: query.trim(),
          audience,
          research_type: researchType,
          page_length: pageLength,
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(
          body.detail || body.message || `Server error ${res.status}`
        );
      }

      const data: ResearchResult = await res.json();
      setResult(data);
      setAppState("results");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again."
      );
      setAppState("error");
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") handleResearch();
  }

  function handleReset() {
    setAppState("idle");
    setResult(null);
    setError("");
  }

  return (
    <div className="flex h-full overflow-hidden bg-[#0a0a0a]">
      <Sidebar
        audience={audience}
        setAudience={setAudience}
        researchType={researchType}
        setResearchType={setResearchType}
        pageLength={pageLength}
        setPageLength={setPageLength}
      />

      {/* Main column */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        {/* Header */}
        <div className="shrink-0 px-8 py-5 border-b border-[#1f1f1f]">
          <h1 className="text-[17px] font-semibold text-white tracking-tight">
            Agentic Research Assistant
          </h1>
          <p className="text-[13px] text-[#4a4a4a] mt-0.5">
            Generate structured research briefs from live sources across the web
          </p>
        </div>

        {/* Search bar */}
        <div className="shrink-0 px-8 py-4 border-b border-[#1f1f1f]">
          <div className="flex gap-2.5 max-w-2xl">
            <div className="relative flex-1">
              <Search
                size={14}
                className="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#3a3a3a] pointer-events-none"
              />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={appState === "loading"}
                placeholder="Enter a research topic or question…"
                className="w-full bg-[#111] border border-[#242424] rounded-lg pl-9 pr-4 py-2.5 text-sm text-white placeholder-[#383838] focus:outline-none focus:border-[#6366f1] transition-colors disabled:opacity-50"
              />
            </div>
            <button
              onClick={handleResearch}
              disabled={!query.trim() || appState === "loading"}
              className="shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors bg-[#6366f1] hover:bg-[#5558e3] text-white disabled:bg-[#1a1a1a] disabled:text-[#3a3a3a] disabled:cursor-not-allowed"
            >
              {appState === "loading" ? (
                <Loader2 size={14} className="animate-spin" />
              ) : (
                <Search size={14} />
              )}
              Research
            </button>
          </div>
        </div>

        {/* Content area */}
        <div className="flex-1 overflow-y-auto">
          {/* ── Idle ── */}
          {appState === "idle" && (
            <div className="flex flex-col items-center justify-center h-full px-8 text-center select-none">
              <div className="w-12 h-12 rounded-2xl bg-[#111] border border-[#222] flex items-center justify-center text-xl mb-4">
                🔬
              </div>
              <h2 className="text-[15px] font-medium text-white mb-2">
                Ready to research
              </h2>
              <p className="text-[13px] text-[#444] max-w-xs leading-relaxed">
                Type any topic above. Four agents will fetch, summarise,
                critique, and write a structured brief in parallel.
              </p>
              <div className="flex flex-wrap gap-2 mt-6 justify-center max-w-md">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => setQuery(s)}
                    className="px-3 py-1.5 rounded-full text-[12px] text-[#555] bg-[#0f0f0f] border border-[#222] hover:border-[#3a3a3a] hover:text-[#888] transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* ── Loading ── */}
          {appState === "loading" && (
            <div className="flex flex-col items-center justify-center h-full px-8 text-center">
              <div className="w-12 h-12 rounded-2xl bg-[#111] border border-[#222] flex items-center justify-center mb-5">
                <Loader2 size={20} className="text-[#6366f1] animate-spin" />
              </div>
              <p className="text-[14px] font-medium text-white mb-1.5">
                Researching…
              </p>
              <p className="text-[12px] text-[#3a3a3a] mb-7">
                ArXiv · HackerNews · Wikipedia · Tavily · DEV.to
              </p>
              <div className="flex flex-col gap-2.5">
                {[
                  ["Fetcher", "0s"],
                  ["Summariser", "0.3s"],
                  ["Critic", "0.6s"],
                  ["Writer", "0.9s"],
                ].map(([name, delay]) => (
                  <div key={name} className="flex items-center gap-2.5">
                    <div
                      className="w-1.5 h-1.5 rounded-full bg-[#6366f1]"
                      style={{
                        animation: `pulse 1.4s ease-in-out ${delay} infinite`,
                      }}
                    />
                    <span className="text-[12px] text-[#3a3a3a]">
                      {name} agent
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── Error ── */}
          {appState === "error" && (
            <div className="flex flex-col items-center justify-center h-full px-8 text-center">
              <div className="w-12 h-12 rounded-2xl bg-[#180a0a] border border-[#3a1a1a] flex items-center justify-center text-xl mb-4">
                ⚠️
              </div>
              <h2 className="text-[15px] font-medium text-white mb-2">
                Research failed
              </h2>
              <p className="text-[13px] text-[#555] max-w-sm mb-5 leading-relaxed">
                {error}
              </p>
              <button
                onClick={handleReset}
                className="text-[13px] text-[#6366f1] hover:text-[#818cf8] transition-colors"
              >
                ← Try again
              </button>
            </div>
          )}

          {/* ── Results ── */}
          {appState === "results" && result && (
            <ResultsPanel result={result} onReset={handleReset} />
          )}
        </div>
      </div>
    </div>
  );
}
