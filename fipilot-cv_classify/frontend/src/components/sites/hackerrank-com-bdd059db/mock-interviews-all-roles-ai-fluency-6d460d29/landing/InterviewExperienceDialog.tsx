"use client";

import type { KeyboardEvent } from "react";
import {
  getResumeRoleMatches,
  type ResumeProfile,
  type ResumeRoleMatch,
} from "../shared/resumeApi";
import styles from "./landing.module.css";

export const INTERVIEW_ROLES = [
  { id: "ai-engineer", title: "AI Engineer", description: "Machine Learning, Deep Learning, Generative AI, LLMs, and problem-solving" },
  { id: "backend-developer", title: "Backend Developer", description: "APIs, databases, distributed services, and problem-solving" },
  { id: "business-analyst", title: "Business Analyst", description: "Requirements, processes, stakeholders, and solution analysis" },
  { id: "data-engineer", title: "Data Engineer", description: "Data pipelines, warehouses, Spark, Airflow, and data platforms" },
  { id: "data-scientist", title: "Data Scientist", description: "Statistics, experiments, predictive modeling, and data insights" },
  { id: "devops-engineer", title: "DevOps Engineer", description: "CI/CD, containers, cloud infrastructure, and observability" },
  { id: "full-stack-developer", title: "Full Stack Developer", description: "Frontend, backend, databases, and end-to-end delivery" },
  { id: "software-engineer", title: "Software Engineer", description: "DSA, system design, coding patterns, and problem-solving" },
  { id: "tester-qa-qc", title: "Tester QA QC", description: "Test strategy, automation, quality assurance, and defect prevention" },
  { id: "web-developer", title: "Web Developer", description: "Web technologies, accessibility, responsive UI, and web delivery" },
  { id: "custom", title: "+ Custom Role", description: "Paste a job description for a tailored interview" },
] as const;

export type InterviewRoleId = (typeof INTERVIEW_ROLES)[number]["id"];

export const EXPERIENCE_LEVELS = ["Intern", "Junior", "Middle", "Senior"] as const;

export type ExperienceLevel = (typeof EXPERIENCE_LEVELS)[number];

interface InterviewExperienceDialogProps {
  customDescription: string;
  onCancel: () => void;
  onContinue: () => void;
  onCustomDescriptionChange: (description: string) => void;
  onExperienceLevelChange: (level: ExperienceLevel) => void;
  onRoleChange: (role: InterviewRoleId) => void;
  selectedExperienceLevel: ExperienceLevel | null;
  selectedRole: InterviewRoleId | null;
  profile: ResumeProfile;
}

export function InterviewExperienceDialog({
  customDescription,
  onCancel,
  onContinue,
  onCustomDescriptionChange,
  onExperienceLevelChange,
  onRoleChange,
  selectedExperienceLevel,
  selectedRole,
  profile,
}: InterviewExperienceDialogProps) {
  const selectionIsValid = selectedRole !== null
    && selectedExperienceLevel !== null
    && (selectedRole !== "custom" || customDescription.length >= 100);
  const roleMatches = getResumeRoleMatches(profile);
  const rolesById = new Map(INTERVIEW_ROLES.map((role) => [role.id, role]));
  const matchedRoles = roleMatches.flatMap((match) => {
    const role = rolesById.get(match.id as InterviewRoleId);
    return role === undefined || role.id === "custom" ? [] : [{ role, match }];
  });
  const customRole = INTERVIEW_ROLES.find((role) => role.id === "custom");
  const selectedMatch = roleMatches.find((match) => match.id === selectedRole);

  function onCardKeyDown(event: KeyboardEvent<HTMLDivElement>, role: InterviewRoleId) {
    if (event.key === " " || event.key === "Enter") {
      event.preventDefault();
      onRoleChange(role);
    }
  }

  return (
    <div className={styles.dialogBackdrop}>
      <section
        className={`${styles.wizardDialog} ${styles.experienceDialog}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="experience-title"
      >
        <div className={styles.wizardContent}>
          <h2 id="experience-title">Choose your interview focus</h2>
          <p className={styles.wizardSubtitle}>
            These percentages show how your resume evidence is distributed across roles. They are not hiring probabilities.
          </p>
          {matchedRoles.length === 0 ? (
            <div className={styles.noRoleMatches} role="status">
              No supported technical role had enough project or work evidence. You can use a job description instead.
            </div>
          ) : null}
          <div className={styles.roleGrid}>
            {[...matchedRoles, ...(customRole === undefined ? [] : [{ role: customRole, match: null }])].map(({ role, match }) => (
              <div
                className={styles.roleCard}
                data-custom={role.id === "custom" || undefined}
                data-selected={selectedRole === role.id || undefined}
                key={role.id}
                onClick={() => onRoleChange(role.id)}
                onKeyDown={(event) => onCardKeyDown(event, role.id)}
                role="button"
                tabIndex={0}
                aria-pressed={selectedRole === role.id}
              >
                <div className={styles.roleCardHeading}>
                  <h3>{role.title}</h3>
                  {match !== null ? <strong>{match.score}%</strong> : null}
                </div>
                <p>{match?.summary ?? role.description}</p>
                {match !== null && match.matchedSkills.length > 0 ? (
                  <span className={styles.roleSkills}>
                    {match.matchedSkills.slice(0, 3).join(" · ")}
                  </span>
                ) : null}
              </div>
            ))}
          </div>
          {selectedMatch !== undefined ? (
            <RoleEvidencePreview match={selectedMatch} profile={profile} />
          ) : null}
          {selectedRole === "custom" ? (
            <div className={styles.customRoleFields}>
              <textarea
                aria-label="Custom role job description"
                onChange={(event) => onCustomDescriptionChange(event.target.value)}
                placeholder="Paste your job description here and we'll create a tailored interview..."
                value={customDescription}
              />
              <p>Minimum 100 characters required</p>
            </div>
          ) : null}
          {selectedRole !== null ? (
            <fieldset className={styles.experienceLevelFields}>
              <legend>Experience level</legend>
              <div className={styles.experienceLevelOptions}>
                {EXPERIENCE_LEVELS.map((level) => (
                  <label
                    className={styles.experienceLevelOption}
                    data-selected={selectedExperienceLevel === level || undefined}
                    key={level}
                  >
                    <input
                      checked={selectedExperienceLevel === level}
                      name="experience-level"
                      onChange={() => onExperienceLevelChange(level)}
                      type="radio"
                      value={level}
                    />
                    {level}
                  </label>
                ))}
              </div>
            </fieldset>
          ) : null}
          <footer
            className={`${styles.wizardFooter} ${styles.experienceFooter}`}
            data-has-level={selectedRole !== null || undefined}
          >
            <button className={styles.wizardSecondaryButton} onClick={onCancel} type="button">Back</button>
            <button
              className={styles.wizardPrimaryButton}
              disabled={!selectionIsValid}
              onClick={onContinue}
              type="button"
            >
              Continue
            </button>
          </footer>
        </div>
      </section>
    </div>
  );
}

function RoleEvidencePreview({
  match,
  profile,
}: {
  match: ResumeRoleMatch;
  profile: ResumeProfile;
}) {
  const entries = profile.workExperience ?? [];
  const relevantEntries = match.relevantExperienceIndexes
    .map((index) => entries[index])
    .filter((entry) => entry !== undefined);

  return (
    <section className={styles.roleEvidencePreview} aria-labelledby="role-evidence-title">
      <div>
        <h3 id="role-evidence-title">Interview context for {match.title}</h3>
        <p>The question set will use only the matching evidence below.</p>
      </div>
      <dl>
        <div>
          <dt>Skills</dt>
          <dd>{match.matchedSkills.join(", ") || "No explicit skills found"}</dd>
        </div>
        <div>
          <dt>Relevant experience</dt>
          <dd>{relevantEntries.map((entry) => entry.name).join(", ")}</dd>
        </div>
      </dl>
    </section>
  );
}
