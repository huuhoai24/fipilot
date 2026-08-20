import type { InterviewReport } from "../shared/interviewApi";

import styles from "./FeedbackPage.module.css";

export function FeedbackSummarySidebar({ report }: { report: InterviewReport }) {
  return (
    <aside className={styles.summaryAside} aria-label="Interview summary">
      <section className={styles.summaryCard}>
        <div className={styles.candidateRow}>
          <div className={styles.avatar} aria-hidden="true">
            H
          </div>
          <div>
            <p className={styles.candidateName}>nguyen huy</p>
            <p className={styles.attemptDate}>Attempted today</p>
          </div>
        </div>

        <div className={styles.divider} />

        <div className={styles.recommendation}>
          <p>Recommendation</p>
          <strong>{report.normalized_score.toFixed(2)}/5</strong>
          <p>Coverage: {Math.round(report.coverage_ratio * 100)}%</p>
        </div>

        <div className={styles.divider} />

        <div className={styles.overallSummary}>
          <h2>Overall Summary</h2>
          <p>{report.overall_assessment}</p>
          <h2>Giải pháp đã trình bày</h2>
          <p>{report.solutions_summary}</p>
          <h2>Khuyến nghị</h2>
          <p>{report.recommendations}</p>
        </div>
      </section>
    </aside>
  );
}
