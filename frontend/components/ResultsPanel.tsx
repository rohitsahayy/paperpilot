"use client";

import ReactMarkdown from "react-markdown";
import {
  ExternalLink,
  RefreshCw,
  BookOpen,
  Zap,
  FileText,
  Star,
  type LucideIcon,
} from "lucide-react";
import type { ResearchResult, Source } from "@/app/page";

interface Props {
  result: ResearchResult;
  onReset: () => void;
}

function wordCount(text: string) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function insightCount(text: string) {
  const bullets = (text.match(/^[-*•]\s/gm) ?? []).length;
  const numbered = (text.match(/^\d+\.\s/gm) ?? []).length;
  return bullets + numbered;
}

function qualityBadge(n: number): { label: string; color: string } {
  if (n >= 4) return { label: "A+", color: "#22c55e" };
  if (n >= 3) return { label: "A", color: "#84cc16" };
  if (n >= 2) return { label: "B+", color: "#f59e0b" };
  return { label: "B", color: "#f97316" };
}

function MetricCard({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: LucideIcon;
  label: string;
  value: string;
  color?: string;
}) {
  return (
    <div className="flex-1 min-w-0 rounded-xl border border-[#1f1f1f] bg-[#0f0f0f] px-4 py-3.5">
      <div className="flex items-center gap-1.5 mb-2">
        <Icon size={11} className="text-[#3a3a3a]" />
        <span className="text-[10px] uppercase tracking-wider text-[#3a3a3a] font-medium">
          {label}
        </span>
      </div>
      <p
        className="text-[22px] font-bold tracking-tight leading-none"
        style={{ color: color ?? "#ededed" }}
      >
        {value}
      </p>
    </div>
  );
}

function SectionHeader({
  icon: Icon,
  title,
}: {
  icon: LucideIcon;
  title: string;
}) {
  return (
    <div className="flex items-center gap-2 px-4 py-3 border-b border-[#1a1a1a]">
      <Icon size={12} className="text-[#3a3a3a]" />
      <span className="text-[11px] font-medium text-[#555]">{title}</span>
    </div>
  );
}

function SourcesList({ sources }: { sources: Source[] }) {
  return (
    <div className="px-4 py-3 flex flex-col gap-3.5">
      {sources.length === 0 ? (
        <p className="text-[12px] text-[#333]">No sources returned</p>
      ) : (
        sources.map((src, i) => (
          <div key={i}>
            <p className="text-[10px] uppercase tracking-wider text-[#6366f1] font-medium mb-1.5">
              {src.source_label || src.source}
            </p>
            <div className="flex flex-col gap-1">
              {src.urls.slice(0, 3).map((url, j) => (
                <a
                  key={j}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-center gap-1.5 text-[12px] text-[#484848] hover:text-[#818cf8] transition-colors"
                >
                  <ExternalLink
                    size={9}
                    className="shrink-0 text-[#2e2e2e] group-hover:text-[#6366f1] transition-colors"
                  />
                  <span className="truncate">
                    {url
                      .replace(/^https?:\/\//, "")
                      .replace(/\/$/, "")
                      .slice(0, 50)}
                    {url.length > 58 ? "…" : ""}
                  </span>
                </a>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

function InsightsList({ sources }: { sources: Source[] }) {
  const withSummary = sources.filter((s) => s.summary).slice(0, 5);
  return (
    <div className="px-4 py-3 flex flex-col gap-3">
      {withSummary.length === 0 ? (
        <p className="text-[12px] text-[#333]">No insights available</p>
      ) : (
        withSummary.map((src, i) => (
          <div key={i} className="border-l-2 border-[#252525] pl-3">
            <p className="text-[10px] text-[#6366f1] font-medium mb-1 uppercase tracking-wider">
              {src.source_label || src.source}
            </p>
            <p className="text-[12px] text-[#484848] leading-relaxed line-clamp-3">
              {src.summary}
            </p>
          </div>
        ))
      )}
    </div>
  );
}

function CitationsList({ sources }: { sources: Source[] }) {
  const all = sources.flatMap((s) =>
    s.urls.map((url) => ({ url, label: s.source_label || s.source }))
  );
  if (all.length === 0) return null;
  return (
    <div className="px-4 py-3 flex flex-col gap-1.5">
      {all.slice(0, 15).map(({ url, label }, i) => (
        <div key={i} className="flex items-start gap-2">
          <span className="text-[10px] font-mono text-[#2e2e2e] mt-px shrink-0">
            [{i + 1}]
          </span>
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            title={`${label} — ${url}`}
            className="text-[11px] text-[#3a3a3a] hover:text-[#818cf8] transition-colors truncate"
          >
            {url.replace(/^https?:\/\//, "").slice(0, 58)}
            {url.length > 66 ? "…" : ""}
          </a>
        </div>
      ))}
    </div>
  );
}

export default function ResultsPanel({ result, onReset }: Props) {
  const { brief, sources, query } = result;
  const words = wordCount(brief);
  const insights = insightCount(brief);
  const quality = qualityBadge(sources.length);

  return (
    <div className="p-6">
      {/* Row: title + new search */}
      <div className="flex items-start justify-between mb-5 gap-4">
        <div className="min-w-0">
          <p className="text-[10px] uppercase tracking-wider text-[#3a3a3a] mb-1">
            Research Brief
          </p>
          <h2 className="text-[15px] font-semibold text-white leading-snug">
            {query}
          </h2>
        </div>
        <button
          onClick={onReset}
          className="shrink-0 flex items-center gap-1.5 text-[12px] text-[#444] hover:text-[#888] transition-colors mt-0.5"
        >
          <RefreshCw size={11} />
          New search
        </button>
      </div>

      {/* Metric cards */}
      <div className="flex gap-3 mb-5">
        <MetricCard
          icon={BookOpen}
          label="Sources"
          value={String(sources.length)}
          color="#6366f1"
        />
        <MetricCard
          icon={Zap}
          label="Insights"
          value={String(insights)}
          color="#818cf8"
        />
        <MetricCard icon={FileText} label="Words" value={words.toLocaleString()} />
        <MetricCard
          icon={Star}
          label="Quality"
          value={quality.label}
          color={quality.color}
        />
      </div>

      {/* Two-column grid */}
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: "1fr 360px", alignItems: "start" }}
      >
        {/* Left — Brief */}
        <div
          className="rounded-xl border border-[#1a1a1a] bg-[#0d0d0d] overflow-hidden"
          style={{ minWidth: 0 }}
        >
          <SectionHeader icon={FileText} title="Research Brief" />
          <div className="px-6 py-5 prose overflow-auto max-h-[calc(100vh-310px)]">
            <ReactMarkdown>{brief}</ReactMarkdown>
          </div>
        </div>

        {/* Right — Sources + Insights + Citations */}
        <div
          className="flex flex-col gap-3 overflow-auto"
          style={{ maxHeight: "calc(100vh - 310px)" }}
        >
          {/* Literature Sources */}
          <div className="rounded-xl border border-[#1a1a1a] bg-[#0d0d0d] overflow-hidden">
            <SectionHeader icon={BookOpen} title="Literature Sources" />
            <SourcesList sources={sources} />
          </div>

          {/* Data Insights */}
          <div className="rounded-xl border border-[#1a1a1a] bg-[#0d0d0d] overflow-hidden">
            <SectionHeader icon={Zap} title="Data Insights" />
            <InsightsList sources={sources} />
          </div>

          {/* Citations */}
          <div className="rounded-xl border border-[#1a1a1a] bg-[#0d0d0d] overflow-hidden">
            <SectionHeader icon={ExternalLink} title="All Citations" />
            <CitationsList sources={sources} />
          </div>
        </div>
      </div>
    </div>
  );
}
