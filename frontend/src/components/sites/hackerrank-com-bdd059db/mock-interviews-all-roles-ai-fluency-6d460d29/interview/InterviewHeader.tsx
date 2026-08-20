import { BrandMark } from "../shared/BrandMark";
import { AI_FLUENCY_BASE_PATH } from "../shared/mockData";
import styles from "./InterviewPage.module.css";

interface InterviewHeaderProps {
  remainingSeconds: number;
  onEndInterview: () => void;
}

function formatCountdown(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  const remainder = seconds % 60;

  return `${minutes}:${remainder.toString().padStart(2, "0")} mins`;
}

export function InterviewHeader({
  remainingSeconds,
  onEndInterview,
}: InterviewHeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.headerIdentity}>
        <BrandMark href={AI_FLUENCY_BASE_PATH} compact />
        <span className={styles.headerSeparator} aria-hidden="true" />
        <span className={styles.headerTitle}>AI Fluency Mock Interview</span>
      </div>

      <div className={styles.headerActions}>
        <time className={styles.timer}>{formatCountdown(remainingSeconds)}</time>
        <span className={styles.headerSeparator} aria-hidden="true" />
        <button
          className={styles.endInterviewButton}
          type="button"
          onClick={onEndInterview}
        >
          End Interview
        </button>
      </div>
    </header>
  );
}
