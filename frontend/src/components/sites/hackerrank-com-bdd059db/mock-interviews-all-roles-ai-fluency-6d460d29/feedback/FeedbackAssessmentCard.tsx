import styles from "./FeedbackPage.module.css";

interface FeedbackAssessmentCardProps {
  title: string;
  description: string;
  evidence: string[];
  score: number;
  status: string;
}

export function FeedbackAssessmentCard({
  title,
  description,
  evidence,
  score,
  status,
}: FeedbackAssessmentCardProps) {
  return (
    <article className={styles.assessmentCard}>
      <div className={styles.assessmentTitleRow}>
        <h2>{title}</h2>
        <span className={styles.statusBadge}>{score}/3 · {status.replaceAll("_", " ")}</span>
      </div>
      <p>{description}</p>
      {evidence.map((quote) => (
        <blockquote className={styles.evidenceQuote} key={quote}>
          “{quote}”
        </blockquote>
      ))}
    </article>
  );
}
