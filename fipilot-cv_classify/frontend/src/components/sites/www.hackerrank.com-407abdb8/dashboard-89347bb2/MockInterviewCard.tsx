import Link from "next/link";
import type { MockInterview } from "../shared/types";
import { LockIcon, UnlockIcon } from "../shared/icons";

export function MockInterviewCard({ interview }: { interview: MockInterview }) {
  const isAiFluency = interview.title === "AI Fluency";
  const card = (
    <div
      style={{
        width: "100%",
        height: "100%",
        padding: 32,
        borderRadius: 16,
        border: "1px solid #EBEBF3",
        background: "linear-gradient(90deg, rgba(174,254,187,0.2), transparent)",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        boxSizing: "border-box",
      }}
    >
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
          <h2 style={{ fontFamily: "var(--hr-font-satoshi)", fontSize: 20, fontWeight: 700, lineHeight: "32px", color: "#121418", margin: 0 }}>{interview.title}</h2>
          {interview.comingSoon ? (
            <span style={{ flex: "0 0 auto", padding: "4px 10px", borderRadius: 9999, background: "#F6F6FF", color: "#1142AF", fontFamily: "var(--hr-font-satoshi)", fontSize: 12, fontWeight: 500, lineHeight: "16px" }}>
              Coming soon
            </span>
          ) : null}
        </div>
        <p style={{ fontSize: 14, lineHeight: "20px", color: "#63646F", margin: 0, maxWidth: 240, fontFamily: "var(--hr-font-satoshi)" }}>{interview.description}</p>
        <div style={{ display: "flex", alignItems: "center", gap: 4, padding: "4px 12px", borderRadius: 9999, background: "rgba(18,20,24,0.05)", width: "fit-content" }}>
          <span style={{ display: "inline-flex", color: "#63646F" }}><UnlockIcon size={16} className="hr-icon" /></span>
          <span style={{ fontSize: 14, lineHeight: "20px", color: "#63646F", fontFamily: "var(--hr-font-satoshi)" }}>{interview.duration}</span>
        </div>
      </div>
      <span aria-hidden="true" style={{ alignSelf: "flex-start", width: 40, height: 40, border: "1px solid #9091A8", borderRadius: 8, display: "inline-flex", alignItems: "center", justifyContent: "center", color: "#121418" }}>{isAiFluency ? <UnlockIcon size={20} /> : <LockIcon size={20} />}</span>
    </div>
  );

  if (isAiFluency) {
    return <Link href="/mock-interviews/all-roles/ai-fluency" aria-label="Start AI Fluency mock interview" className="hr-mi-card hr-flex hr-align-center hr-justify-center" style={{ cursor: "pointer", display: "flex", width: "100%", textAlign: "left", textDecoration: "none" }}>{card}</Link>;
  }

  if (interview.comingSoon) {
    return <div aria-disabled="true" aria-label={`${interview.title} mock interview coming soon`} className="hr-mi-card hr-flex hr-align-center hr-justify-center" style={{ cursor: "default", display: "flex", width: "100%", textAlign: "left" }}>{card}</div>;
  }

  return <div role="button" tabIndex={0} aria-label={`Start ${interview.title} mock interview`} className="hr-mi-card hr-flex hr-align-center hr-justify-center" style={{ cursor: "pointer", display: "flex", width: "100%", textAlign: "left" }}>{card}</div>;
}
