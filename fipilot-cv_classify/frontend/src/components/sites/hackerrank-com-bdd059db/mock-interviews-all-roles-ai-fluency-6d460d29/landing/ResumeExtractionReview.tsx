import { CheckCircle2, TriangleAlert } from "lucide-react";
import {
  summarizeResumeExtraction,
  type ResumeProfile,
} from "../shared/resumeApi";
import styles from "./landing.module.css";

interface ResumeExtractionReviewProps {
  profile: ResumeProfile;
}

export function ResumeExtractionReview({ profile }: ResumeExtractionReviewProps) {
  const summary = summarizeResumeExtraction(profile);
  const StatusIcon = summary.isComplete ? CheckCircle2 : TriangleAlert;

  return (
    <section className={styles.extractionReview} aria-labelledby="extraction-review-title">
      <header className={styles.extractionSummary} aria-live="polite">
        <div className={styles.extractionStatusIcon} data-complete={summary.isComplete || undefined}>
          <StatusIcon aria-hidden="true" size={22} />
        </div>
        <div className={styles.extractionSummaryCopy}>
          <div className={styles.extractionStatusLine}>
            <h3 id="extraction-review-title">
              {summary.isComplete ? "Extraction looks complete" : "Review missing details"}
            </h3>
            <span>
              {summary.entries.length} {summary.entries.length === 1 ? "item" : "items"} found
            </span>
          </div>
          <p>
            We use the work history and projects below to tailor your interview questions.
            Compare them with your PDF before continuing.
          </p>
        </div>
      </header>

      <dl className={styles.extractionMetrics} aria-label="Extraction summary">
        <div>
          <dt>Work experience</dt>
          <dd>{summary.workCount}</dd>
        </div>
        <div>
          <dt>Projects</dt>
          <dd>{summary.projectCount}</dd>
        </div>
        <div>
          <dt>Needs attention</dt>
          <dd>{summary.issues.length}</dd>
        </div>
      </dl>

      {Array.isArray(profile.skills) && profile.skills.length > 0 ? (
        <div className={styles.extractedSkills}>
          <strong>Technical skills found</strong>
          <p>{profile.skills.join(", ")}</p>
        </div>
      ) : null}

      {summary.issues.length > 0 ? (
        <div className={styles.extractionIssues} role="status">
          <strong>Check these details</strong>
          <ul>
            {summary.issues.map((issue, index) => (
              <li key={`${issue.entryIndex ?? "profile"}-${index}`}>
                {issue.entryIndex === null
                  ? issue.message
                  : `Item ${issue.entryIndex + 1}: ${issue.message}`}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <div className={styles.extractionEntries}>
        {summary.entries.map((entry, index) => (
          <article className={styles.extractionEntry} key={`${entry.type}-${entry.name}-${index}`}>
            <div className={styles.extractionEntryHeading}>
              <span>{entry.type}</span>
              <div>
                <h4>{entry.name || "Name not found"}</h4>
                <p>
                  {entry.position || (entry.type === "Project" ? "Project context" : "Job title not found")}
                </p>
              </div>
            </div>
            <p className={styles.extractionDescription}>
              {entry.jobDescription || "No supporting description was extracted for this item."}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
