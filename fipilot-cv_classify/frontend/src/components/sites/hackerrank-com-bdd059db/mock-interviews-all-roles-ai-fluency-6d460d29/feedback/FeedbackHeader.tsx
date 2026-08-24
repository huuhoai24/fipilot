import { Moon } from "lucide-react";
import Link from "next/link";

import { BrandMark } from "../shared/BrandMark";

import styles from "./FeedbackPage.module.css";

export function FeedbackHeader() {
  return (
    <header className={styles.header}>
      <div className={styles.headerIdentity}>
        <div className={styles.headerBrand}>
          <BrandMark />
        </div>
        <span className={styles.headerSeparator} aria-hidden="true" />
        <p className={styles.headerTitle}>
          AI Fluency Mock Interview Feedback
        </p>
      </div>

      <div className={styles.headerActions}>
        <button
          className={styles.themeButton}
          type="button"
          aria-label="Theme settings"
        >
          <Moon aria-hidden="true" size={20} strokeWidth={1.6} />
        </button>
        <Link className={styles.doneButton} href="/dashboard">
          Done
        </Link>
      </div>
    </header>
  );
}
