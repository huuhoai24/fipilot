"use client";

import { MessageSquare } from "lucide-react";

import type { InterviewTurn } from "../shared/interviewApi";

import styles from "./FeedbackPage.module.css";

function formatTimestamp(timestamp: string) {
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return "--:--";
  return date.toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });
}

export function FeedbackTranscriptPanel({ turns }: { turns: InterviewTurn[] }) {
  return (
    <section className={`${styles.transcriptCard} ${styles.chatTranscriptCard}`}>
      <div className={styles.transcriptHeader}>
        <div className={styles.transcriptHeading}>
          <MessageSquare aria-hidden="true" size={17} strokeWidth={1.6} />
          <h1>Interview Transcript</h1>
        </div>
      </div>

      <div className={styles.chatPanel}>
        {turns.length === 0 ? (
          <p>Phiên phỏng vấn chưa có câu trả lời nào.</p>
        ) : turns.flatMap((turn, index) => [
          <div className={styles.transcriptRow} key={`question-${index}`}>
            <div className={styles.speakerColumn}>
              <strong>Interviewer</strong>
              <time>{formatTimestamp(turn.timestamp)}</time>
            </div>
            <p>{turn.question.question}</p>
          </div>,
          <div className={styles.transcriptRow} key={`answer-${index}`}>
            <div className={styles.speakerColumn}>
              <strong>Candidate</strong>
              <time>{formatTimestamp(turn.timestamp)}</time>
            </div>
            <p>{turn.answer}</p>
          </div>,
        ])}
      </div>
    </section>
  );
}
