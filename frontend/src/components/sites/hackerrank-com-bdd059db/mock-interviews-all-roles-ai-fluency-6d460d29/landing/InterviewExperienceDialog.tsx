"use client";

import type { KeyboardEvent } from "react";
import styles from "./landing.module.css";

export const INTERVIEW_ROLES = [
  { id: "software-engineer", title: "Software Engineer", description: "DSA, system design, coding patterns, and problem-solving" },
  { id: "frontend-developer", title: "Frontend Developer", description: "React, Angular, Vue, and problem-solving" },
  { id: "backend-developer", title: "Backend Developer", description: "Node, Python, Java, and problem-solving" },
  { id: "ai-engineer", title: "AI Engineer", description: "Machine Learning, Deep Learning, Generative AI, LLMs, and problem-solving" },
  { id: "forward-deployed-engineer", title: "Forward Deployed Engineer", description: "AWS, Azure, and problem-solving" },
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
}: InterviewExperienceDialogProps) {
  const selectionIsValid = selectedRole !== null
    && selectedExperienceLevel !== null
    && (selectedRole !== "custom" || customDescription.length >= 100);

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
          <h2 id="experience-title">Choose Your Mock Interview Experience</h2>
          <p className={styles.wizardSubtitle}>
            Start with popular ready-made roles or build your own based on a specific job description.
          </p>
          <div className={styles.roleGrid}>
            {INTERVIEW_ROLES.map((role) => (
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
                <h3>{role.title}</h3>
                <p>{role.description}</p>
              </div>
            ))}
          </div>
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
            <button className={styles.wizardSecondaryButton} onClick={onCancel} type="button">Cancel</button>
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
