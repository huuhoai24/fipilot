import { X } from "lucide-react";
import styles from "./InterviewPage.module.css";

interface EndInterviewDialogProps {
  remainingMinutes: number;
  onContinue: () => void;
  onEnd: () => void;
}

export function EndInterviewDialog({
  remainingMinutes,
  onContinue,
  onEnd,
}: EndInterviewDialogProps) {
  return (
    <div className={styles.dialogLayer}>
      <button
        className={styles.dialogBackdrop}
        type="button"
        aria-label="Continue interview"
        onClick={onContinue}
      />
      <section
        className={styles.endDialog}
        role="dialog"
        aria-modal="true"
        aria-labelledby="end-interview-title"
      >
        <div className={styles.dialogHeader}>
          <h2 id="end-interview-title">End interview and view feedback?</h2>
          <button
            className={styles.dialogClose}
            type="button"
            onClick={onContinue}
            aria-label="Close"
          >
            <X aria-hidden="true" />
          </button>
        </div>
        <p className={styles.dialogBody}>
          You still have {remainingMinutes} mins remaining. Ending now means you&apos;ll
          receive limited feedback and miss insights we use to create a more
          personalized improvement plan.
        </p>
        <div className={styles.dialogFooter}>
          <button
            className={styles.continueButton}
            type="button"
            onClick={onContinue}
          >
            Continue
          </button>
          <button className={styles.confirmEndButton} type="button" onClick={onEnd}>
            End
          </button>
        </div>
      </section>
    </div>
  );
}
