"use client";

import { useEffect, useState } from "react";
import {
  fetchPersistedInterview,
  loadInterviewReport,
  loadInterviewTurns,
  type InterviewReport,
  type InterviewTurn,
} from "../shared/interviewApi";

import { FeedbackAssessmentCard } from "./FeedbackAssessmentCard";
import { FeedbackHeader } from "./FeedbackHeader";
import styles from "./FeedbackPage.module.css";
import { FeedbackSummarySidebar } from "./FeedbackSummarySidebar";
import { FeedbackTranscriptPanel } from "./FeedbackTranscriptPanel";

interface FeedbackPageProps {
  sessionId: string;
}

export function FeedbackPage({ sessionId }: FeedbackPageProps) {
  const [report, setReport] = useState<InterviewReport | null>();
  const [turns, setTurns] = useState<InterviewTurn[]>([]);

  useEffect(() => {
    let cancelled = false;
    const localReport = loadInterviewReport(sessionId);
    const localTurns = loadInterviewTurns(sessionId);
    if (localReport !== null) {
      setReport(localReport);
      setTurns(localTurns);
      return;
    }
    void fetchPersistedInterview(sessionId).then((result) => {
      if (cancelled) return;
      setReport(result?.report ?? null);
      setTurns(result?.turns ?? []);
    });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  if (report === undefined) {
    return (
      <div className={styles.page} data-session-id={sessionId}>
        <FeedbackHeader />
        <main className={styles.shell}>
          <div className={styles.assessmentCard}>Đang tải báo cáo phỏng vấn...</div>
        </main>
      </div>
    );
  }

  if (report === null) {
    return (
      <div className={styles.page} data-session-id={sessionId}>
        <FeedbackHeader />
        <main className={styles.shell}>
          <div className={styles.assessmentCard}>
            Không tìm thấy báo cáo cho phiên phỏng vấn này.
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className={styles.page} data-session-id={sessionId}>
      <FeedbackHeader />
      <main className={styles.shell}>
        <FeedbackSummarySidebar report={report} />
        <div className={styles.mainColumn}>
          <FeedbackTranscriptPanel turns={turns} />
          <div className={styles.assessmentList}>
            {report.assessments.map((assessment) => (
              <FeedbackAssessmentCard
                description={assessment.rationale}
                evidence={assessment.evidence.map((item) => item.quote)}
                key={assessment.turn_index}
                score={assessment.raw_score}
                status={assessment.status}
                title={assessment.evaluation_goal}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}
