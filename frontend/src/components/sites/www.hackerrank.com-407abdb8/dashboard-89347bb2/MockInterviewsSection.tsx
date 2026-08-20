"use client";

import { useMemo, useState, useSyncExternalStore, type CSSProperties } from "react";
import Link from "next/link";
import { ChevronLeftIcon, ChevronRightIcon } from "../shared/icons";
import type { MockInterview } from "../shared/types";
import { MockInterviewCard } from "./MockInterviewCard";

const INTERVIEWS: MockInterview[] = [
  { title: "AI Fluency", description: "Demonstrate your ability to build with AI and use AI tools to solve problems and improve your workflow.", duration: "30 mins" },
  { title: "Technical Screen", description: "Practice a recruiter screening to identify gaps in CS fundamentals, role fit, and interview readiness.", duration: "30 mins", comingSoon: true },
  { title: "Coding", description: "Solve algorithmic and data structure problems designed to test your problem-solving skills.", duration: "60 mins", comingSoon: true },
];

const chevBtn: CSSProperties = {
  width: 40,
  height: 40,
  borderRadius: 8,
  border: "none",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  cursor: "pointer",
  padding: 0,
};

const DESKTOP_GRID = "306px 306px 306px 306px";

function getCarouselGrid(): string {
  if (window.matchMedia("(min-width: 1440px)").matches) return "306px 306px 306px 306px";
  if (window.matchMedia("(min-width: 1280px)").matches) return "268px 268px 268px 268px";
  if (window.matchMedia("(min-width: 1024px)").matches) return "296px 296px 296px";
  if (window.matchMedia("(min-width: 768px)").matches) return "340px 340px";
  return "1fr";
}

const COLS_BY_GRID: Record<string, number> = {
  "306px 306px 306px 306px": 4,
  "268px 268px 268px 268px": 4,
  "296px 296px 296px": 3,
  "340px 340px": 2,
  "1fr": 1,
};

const MEDIA_QUERIES = [
  "(min-width: 1440px)",
  "(min-width: 1280px)",
  "(min-width: 1024px)",
  "(min-width: 768px)",
];

function subscribe(onChange: () => void) {
  for (const mq of MEDIA_QUERIES) {
    const m = window.matchMedia(mq);
    if (typeof m.addEventListener === "function") m.addEventListener("change", onChange);
  }
  window.addEventListener("resize", onChange);
  return () => {
    for (const mq of MEDIA_QUERIES) {
      const m = window.matchMedia(mq);
      if (typeof m.removeEventListener === "function") m.removeEventListener("change", onChange);
    }
    window.removeEventListener("resize", onChange);
  };
}

function getGridSnapshot(): string {
  return getCarouselGrid();
}

function getServerSnapshot(): string {
  return DESKTOP_GRID;
}

export function MockInterviewsSection() {
  const grid = useSyncExternalStore(subscribe, getGridSnapshot, getServerSnapshot);
  const cols = COLS_BY_GRID[grid] ?? 4;
  const [page, setPage] = useState(0);

  const pages = useMemo(() => {
    const chunks: MockInterview[][] = [];
    for (let i = 0; i < INTERVIEWS.length; i += cols) {
      chunks.push(INTERVIEWS.slice(i, i + cols));
    }
    return chunks;
  }, [cols]);

  const safePage = Math.min(page, pages.length - 1);
  const prev = () => setPage((p) => Math.max(0, p - 1));
  const next = () => setPage((p) => Math.min(pages.length - 1, p + 1));

  return (
    <section style={{ width: "100%", display: "flex", flexDirection: "column", gap: 32 }}>
      <div style={{ minHeight: 56, display: "flex", justifyContent: "space-between", alignItems: "center", width: "100%", gap: 32 }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 4, flex: "1 1 auto", minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <h2 style={{ fontFamily: "var(--hr-font-satoshi)", fontSize: 20, fontWeight: 700, lineHeight: "32px", color: "#121418", margin: 0 }}>AI-powered Mock Interviews</h2>
            <div style={{ fontSize: 14, fontWeight: 500, lineHeight: "20px", color: "#1142AF", background: "#F6F6FF", padding: "4px 12px", borderRadius: 100 }}>New</div>
          </div>
          <p style={{ fontFamily: "var(--hr-font-satoshi)", fontSize: 14, lineHeight: "20px", color: "#63646F", margin: 0 }}>Ace your next job interview by practicing with AI-powered mock interviews.</p>
        </div>
        <Link href="/mock-interviews/all-roles/ai-fluency" style={{ fontSize: 14, fontWeight: 500, lineHeight: "20px", color: "#2358DB", textDecoration: "none", borderRadius: 4, cursor: "pointer", fontFamily: "var(--hr-font-satoshi)" }}>Know More</Link>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        <div style={{ overflow: "hidden", width: "100%" }}>
          <div style={{ display: "flex", transition: "transform 0.45s cubic-bezier(0.2, 0.7, 0.2, 1)", transform: `translateX(-${safePage}00%)` }}>
            {pages.map((chunk, i) => (
              <div key={i} style={{ flex: "0 0 100%", display: "grid", gap: 16, alignItems: "stretch", gridTemplateColumns: grid }}>
                {chunk.map((iv, j) => <MockInterviewCard key={j} interview={iv} />)}
              </div>
            ))}
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 16, height: 40 }}>
          <button aria-label="Previous mock interviews" disabled={safePage === 0} onClick={prev} className={safePage === 0 ? "bg-transparent" : "bg-transparent hover:bg-white"} style={{ ...chevBtn, color: safePage === 0 ? "#9091A8" : "#121418" }}><ChevronLeftIcon size={20} /></button>
          <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            {pages.map((_, i) => (
              <button key={i} aria-label={`Go to mock interviews page ${i + 1}`} onClick={() => setPage(i)}
                style={{ width: i === safePage ? 24 : 8, height: 8, borderRadius: 9999, background: i === safePage ? "#18A149" : "#C1C2D6", border: "none", cursor: "pointer", transition: "width 0.3s ease, background 0.3s ease", padding: 0 }} />
            ))}
          </div>
          <button aria-label="Next mock interviews" disabled={safePage === pages.length - 1} onClick={next} className={safePage === pages.length - 1 ? "bg-transparent" : "bg-transparent hover:bg-white"} style={{ ...chevBtn, color: safePage === pages.length - 1 ? "#9091A8" : "#121418" }}><ChevronRightIcon size={20} /></button>
        </div>
      </div>
    </section>
  );
}
