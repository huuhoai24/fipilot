"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getAnonymousClientId } from "../../hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/shared/clientIdentity";

import { AUTH_CHANGE_EVENT, getAuthUser, type AuthUser } from "@/lib/auth";

interface HistoryItem {
  session_id: string;
  role: string;
  level: string;
  status: string;
  created_at: string;
  completed_at: string | null;
  normalized_score: number | null;
}

export function InterviewHistory() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [items, setItems] = useState<HistoryItem[]>([]);

  useEffect(() => {
    const syncUser = () => setUser(getAuthUser());
    syncUser();
    window.addEventListener(AUTH_CHANGE_EVENT, syncUser);
    window.addEventListener("storage", syncUser);
    return () => {
      window.removeEventListener(AUTH_CHANGE_EVENT, syncUser);
      window.removeEventListener("storage", syncUser);
    };
  }, []);

  useEffect(() => {
    if (user === null) {
      setItems([]);
      return;
    }
    let active = true;
    fetch(`/api/interview/history?client_id=${encodeURIComponent(getAnonymousClientId())}`, {
      cache: "no-store",
    })
      .then((response) => (response.ok ? response.json() : null))
      .then((body: { interviews?: HistoryItem[] } | null) => {
        if (active) setItems(body?.interviews ?? []);
      })
      .catch(() => undefined);
    return () => {
      active = false;
    };
  }, [user]);

  return (
    <section style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div>
        <h2 style={{ margin: 0, color: "#121418", fontSize: 20, fontWeight: 700, lineHeight: "32px" }}>
          Interview History
        </h2>
        <p style={{ margin: 0, color: "#63646F", fontSize: 14, lineHeight: "20px" }}>
          Review your previous interviews and feedback.
        </p>
      </div>
      {user === null ? null : items.length === 0 ? (
        <div
          style={{
            padding: "24px 20px",
            border: "1px dashed #D1D2DF",
            borderRadius: 12,
            background: "#F9FAFC",
            color: "#63646F",
            fontSize: 14,
            textAlign: "center",
          }}
        >
          No completed interviews yet. Start your first mock interview above!
        </div>
      ) : (
        <div style={{ display: "grid", gap: 12 }}>
          {items.map((item) => (
            <Link
              key={item.session_id}
              href={`/mock-interviews/all-roles/ai-fluency/${encodeURIComponent(item.session_id)}/feedback`}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: 16,
                padding: "16px 20px",
                border: "1px solid #EBEBF3",
                borderRadius: 12,
                color: "#121418",
                background: "#FFF",
                textDecoration: "none",
              }}
            >
              <span style={{ minWidth: 0 }}>
                <strong style={{ display: "block", fontSize: 15 }}>{item.role || "AI Fluency"}</strong>
                <span style={{ color: "#63646F", fontSize: 13 }}>
                  {new Date(item.completed_at ?? item.created_at).toLocaleDateString()} · {item.level}
                </span>
              </span>
              <span style={{ flexShrink: 0, color: "#18A149", fontWeight: 700 }}>
                {item.normalized_score === null ? "View feedback" : `${item.normalized_score.toFixed(2)}/5`}
              </span>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
