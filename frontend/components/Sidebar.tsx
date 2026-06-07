"use client";

import { ChevronDown } from "lucide-react";

const AUDIENCES = [
  "Academic Researchers",
  "General Public",
  "Industry Professionals",
  "Students",
];

const RESEARCH_TYPES = [
  "Comprehensive",
  "Literature Review",
  "Technical Deep-Dive",
  "Trend Analysis",
];

const SOURCES = [
  "ArXiv Papers",
  "HackerNews",
  "Wikipedia",
  "Tavily Search",
  "DEV.to Articles",
];

interface Props {
  audience: string;
  setAudience: (v: string) => void;
  researchType: string;
  setResearchType: (v: string) => void;
  pageLength: number;
  setPageLength: (v: number) => void;
}

function Select({
  value,
  onChange,
  options,
}: {
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <div className="relative">
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full bg-[#111] border border-[#242424] rounded-lg px-3 py-2 text-sm text-white pr-8 focus:outline-none focus:border-[#6366f1] transition-colors"
      >
        {options.map((o) => (
          <option key={o} value={o} style={{ backgroundColor: "#111" }}>
            {o}
          </option>
        ))}
      </select>
      <ChevronDown
        size={12}
        className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#444] pointer-events-none"
      />
    </div>
  );
}

export default function Sidebar({
  audience,
  setAudience,
  researchType,
  setResearchType,
  pageLength,
  setPageLength,
}: Props) {
  return (
    <aside
      className="flex flex-col h-full shrink-0"
      style={{
        width: "260px",
        backgroundColor: "#0d0d0d",
        borderRight: "1px solid #1a1a1a",
      }}
    >
      {/* Logo */}
      <div className="px-5 py-5" style={{ borderBottom: "1px solid #1a1a1a" }}>
        <div className="flex items-center gap-2.5">
          <div
            className="w-7 h-7 rounded-lg flex items-center justify-center text-sm select-none"
            style={{ background: "linear-gradient(135deg, #6366f1, #818cf8)" }}
          >
            🚀
          </div>
          <span className="font-semibold text-white text-sm tracking-tight">
            PaperPilot
          </span>
        </div>
        <p className="text-[11px] mt-1.5" style={{ color: "#3a3a3a" }}>
          Agentic research assistant
        </p>
      </div>

      {/* Controls */}
      <div className="flex-1 px-5 py-5 flex flex-col gap-5 overflow-y-auto">
        {/* Audience */}
        <div>
          <label className="block text-[10px] font-medium uppercase tracking-wider mb-2 text-[#555]">
            Target Audience
          </label>
          <Select value={audience} onChange={setAudience} options={AUDIENCES} />
        </div>

        {/* Research Type */}
        <div>
          <label className="block text-[10px] font-medium uppercase tracking-wider mb-2 text-[#555]">
            Research Type
          </label>
          <Select
            value={researchType}
            onChange={setResearchType}
            options={RESEARCH_TYPES}
          />
        </div>

        {/* Page Length */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-[10px] font-medium uppercase tracking-wider text-[#555]">
              Page Length
            </label>
            <span className="text-[11px] font-mono tabular-nums text-[#6366f1]">
              {pageLength.toLocaleString()}w
            </span>
          </div>
          <input
            type="range"
            min={500}
            max={5000}
            step={100}
            value={pageLength}
            onChange={(e) => setPageLength(Number(e.target.value))}
          />
          <div className="flex justify-between mt-1">
            <span className="text-[10px] text-[#333]">500</span>
            <span className="text-[10px] text-[#333]">5,000</span>
          </div>
        </div>

        {/* Divider */}
        <div style={{ borderTop: "1px solid #1a1a1a" }} />

        {/* Sources */}
        <div>
          <p className="text-[10px] font-medium uppercase tracking-wider mb-2.5 text-[#555]">
            Data Sources
          </p>
          <div className="flex flex-col gap-2">
            {SOURCES.map((s) => (
              <div key={s} className="flex items-center gap-2">
                <div
                  className="w-1.5 h-1.5 rounded-full shrink-0"
                  style={{ backgroundColor: "#6366f1" }}
                />
                <span className="text-[12px] text-[#444]">{s}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="px-5 py-3.5" style={{ borderTop: "1px solid #1a1a1a" }}>
        <p className="text-[10px] text-[#2e2e2e]">LLaMA 3.3 · 70B · Groq</p>
      </div>
    </aside>
  );
}
