"use client";

import { useSyncExternalStore } from "react";

const ICON_BASE = "/sites/www.hackerrank.com-407abdb8/dashboard-89347bb2/icons";

const TOPICS = [
  { name: "Algorithms", icon: `${ICON_BASE}/Algorithm.svg`, href: "https://www.hackerrank.com/domains/algorithms" },
  { name: "Data Structures", icon: `${ICON_BASE}/DataStructure.svg`, href: "https://www.hackerrank.com/domains/data-structures" },
  { name: "Mathematics", icon: `${ICON_BASE}/Mathematics.svg`, href: "https://www.hackerrank.com/domains/mathematics" },
  { name: "Artificial Intelligence", icon: `${ICON_BASE}/AI.svg`, href: "https://www.hackerrank.com/domains/artificial-intelligence" },
  { name: "C", icon: `${ICON_BASE}/C.svg`, href: "https://www.hackerrank.com/domains/c" },
  { name: "C++", icon: `${ICON_BASE}/C++.svg`, href: "https://www.hackerrank.com/domains/cpp" },
  { name: "Java", icon: `${ICON_BASE}/Java.svg`, href: "https://www.hackerrank.com/domains/java" },
  { name: "Python", icon: `${ICON_BASE}/Python.svg`, href: "https://www.hackerrank.com/domains/python" },
  { name: "Ruby", icon: `${ICON_BASE}/Ruby.svg`, href: "https://www.hackerrank.com/domains/ruby" },
  { name: "SQL", icon: `${ICON_BASE}/SQL.svg`, href: "https://www.hackerrank.com/domains/sql" },
  { name: "Databases", icon: `${ICON_BASE}/DataBase.svg`, href: "https://www.hackerrank.com/domains/databases" },
  { name: "Linux Shell", icon: `${ICON_BASE}/LinuxShell.svg`, href: "https://www.hackerrank.com/domains/shell" },
  { name: "Functional Programming", icon: `${ICON_BASE}/FunctionalProgramming.svg`, href: "https://www.hackerrank.com/domains/functions" },
  { name: "Regex", icon: `${ICON_BASE}/regex.svg`, href: "https://www.hackerrank.com/domains/regex" },
  { name: "React", icon: `${ICON_BASE}/react.svg`, href: "https://www.hackerrank.com/domains/react" },
];

const DESKTOP_GRID = "306px 306px 306px 306px";

const MEDIA_QUERIES = [
  "(min-width: 1440px)",
  "(min-width: 1281px)",
  "(min-width: 1025px)",
  "(min-width: 651px)",
];

function getTopicsGrid(): string {
  if (window.matchMedia("(min-width: 1440px)").matches) return "306px 306px 306px 306px";
  if (window.matchMedia("(min-width: 1281px)").matches) return "268px 268px 268px 268px";
  if (window.matchMedia("(min-width: 1025px)").matches) return "repeat(3, 1fr)";
  if (window.matchMedia("(min-width: 651px)").matches) return "repeat(2, 1fr)";
  return "1fr";
}

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
  return getTopicsGrid();
}

function getServerSnapshot(): string {
  return DESKTOP_GRID;
}

export function PracticeSkillsSection() {
  const cols = useSyncExternalStore(subscribe, getGridSnapshot, getServerSnapshot);

  return (
    <section style={{ width: "100%" }}>
      <h2
        style={{
          fontFamily: "var(--hr-font-satoshi)",
          fontSize: 20,
          fontWeight: 700,
          lineHeight: "32px",
          color: "#121418",
          margin: 0,
        }}
      >
        Practice Skills
      </h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: cols,
          gap: 16,
          width: "100%",
          marginTop: 32,
        }}
      >
        {TOPICS.map((t) => (
          <a
            key={t.name}
            href={t.href}
            className="hover:bg-[#EBEBF3]"
            style={{
              borderRadius: 16,
              background: "#F7F8FD",
              padding: 32,
              display: "flex",
              alignItems: "center",
              gap: 8,
              cursor: "pointer",
              boxSizing: "border-box",
              height: 88,
              textDecoration: "none",
              transition: "all",
            }}
          >
            <img
              src={t.icon}
              alt=""
              width={24}
              height={24}
              style={{ display: "block" }}
            />
            <span
              style={{
                fontFamily: "var(--hr-font-satoshi)",
                fontSize: 16,
                fontWeight: 700,
                lineHeight: "24px",
                color: "#121418",
              }}
            >
              {t.name}
            </span>
          </a>
        ))}
      </div>
    </section>
  );
}
