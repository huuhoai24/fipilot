"use client";

import { useEffect, useRef, useState } from "react";
import { CircleAlert, Eye, FileText, FileUp, LoaderCircle, X } from "lucide-react";
import {
  clearResumeAnalysis,
  fetchLatestResume,
  loadResumeAnalysis,
  saveResumeAnalysis,
  uploadResume,
} from "../shared/resumeApi";
import styles from "./landing.module.css";

interface ResumeUploadStepProps {
  onBack: () => void;
  onContinue: () => void;
  onFileChange: (file: File | null) => void;
}

export function ResumeUploadStep({ onBack, onContinue, onFileChange }: ResumeUploadStepProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const objectUrlRef = useRef<string | null>(null);
  const [phase, setPhase] = useState<"empty" | "uploading" | "success">("empty");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [resumeFilename, setResumeFilename] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [toastVisible, setToastVisible] = useState(false);
  const [toastMessage, setToastMessage] = useState("Unsupported file format. Only pdf formats are allowed.");

  useEffect(() => {
    const storedResume = loadResumeAnalysis();
    let cancelled = false;
    const restoreResume = async () => {
      const resume = storedResume ?? await fetchLatestResume();
      if (resume === null) return;
      if (cancelled) return;
      saveResumeAnalysis(resume);
      setResumeFilename(resume.filename);
      setPhase("success");
    };
    void restoreResume();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (phase !== "uploading" || selectedFile === null) {
      return;
    }

    let cancelled = false;
    const analysisTimer = window.setTimeout(() => setIsAnalyzing(true), 800);
    uploadResume(selectedFile)
      .then((result) => {
        if (cancelled) {
          return;
        }
        saveResumeAnalysis(result);
        setResumeFilename(result.filename);
        setPhase("success");
      })
      .catch((err: unknown) => {
        if (cancelled) {
          return;
        }
        setPhase("empty");
        setSelectedFile(null);
        setResumeFilename(null);
        clearResumeAnalysis();
        if (inputRef.current !== null) {
          inputRef.current.value = "";
        }
        onFileChange(null);
        setToastMessage(err instanceof Error ? err.message : "Upload failed. Please try again.");
        setToastVisible(true);
      });

    return () => {
      cancelled = true;
      window.clearTimeout(analysisTimer);
      setIsAnalyzing(false);
    };
  }, [phase, selectedFile, onFileChange]);

  useEffect(() => {
    return () => {
      if (objectUrlRef.current !== null) {
        URL.revokeObjectURL(objectUrlRef.current);
      }
    };
  }, []);

  function openFilePicker() {
    if (phase === "empty") {
      inputRef.current?.click();
    }
  }

  function chooseFile(file: File | null) {
    if (file === null) {
      return;
    }

    const hasPdfExtension = file.name.toLowerCase().endsWith(".pdf");
    const hasPdfMime = file.type === "application/pdf" || file.type === "";
    const withinSizeLimit = file.size <= 5 * 1024 * 1024;

    if (!hasPdfExtension || !hasPdfMime || !withinSizeLimit) {
      setToastVisible(true);
      if (inputRef.current !== null) {
        inputRef.current.value = "";
      }
      return;
    }

    if (objectUrlRef.current !== null) {
      URL.revokeObjectURL(objectUrlRef.current);
    }
    objectUrlRef.current = URL.createObjectURL(file);
    clearResumeAnalysis();
    setToastVisible(false);
    setIsAnalyzing(false);
    setSelectedFile(file);
    setResumeFilename(file.name);
    setPhase("uploading");
    onFileChange(file);
  }

  function previewFile() {
    if (objectUrlRef.current !== null) {
      window.open(objectUrlRef.current, "_blank", "noopener,noreferrer");
    }
  }

  function removeFile() {
    if (objectUrlRef.current !== null) {
      URL.revokeObjectURL(objectUrlRef.current);
      objectUrlRef.current = null;
    }
    if (inputRef.current !== null) {
      inputRef.current.value = "";
    }
    setSelectedFile(null);
    setResumeFilename(null);
    setPhase("empty");
    setToastVisible(false);
    clearResumeAnalysis();
    onFileChange(null);
  }

  return (
    <div className={styles.dialogBackdrop}>
      {toastVisible ? (
        <div className={styles.uploadToast} role="alert">
          <CircleAlert className={styles.uploadToastIcon} size={20} />
          <span>{toastMessage}</span>
          <button
            className={styles.uploadToastClose}
            onClick={() => setToastVisible(false)}
            aria-label="Dismiss upload error"
            type="button"
          >
            <X size={18} />
          </button>
        </div>
      ) : null}
      <section
        className={`${styles.wizardDialog} ${styles.resumeDialog}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="resume-title"
      >
        <div className={styles.wizardContent}>
          <h2 id="resume-title">Upload Resume</h2>
          <p className={styles.wizardSubtitle}>
            Add your resume so mock interviewer can reference it during conversation.
          </p>
          {phase === "success" && resumeFilename !== null ? (
            <div className={styles.resumeSuccess}>
              <div className={styles.resumeSuccessIntro}>
                <strong>Your resume has been added</strong>
                <p>Your resume is ready for the interview.</p>
              </div>
              <div className={styles.resumeSelectedFile}>
                <div className={styles.resumeFileMeta}>
                  <FileText size={28} />
                  <span className={styles.resumeFileName} title={resumeFilename}>{resumeFilename}</span>
                </div>
                <div className={styles.resumeFileActions}>
                  {selectedFile !== null ? (
                    <button
                      className={styles.resumeIconButton}
                      onClick={previewFile}
                      aria-label={`Preview ${resumeFilename}`}
                      type="button"
                    >
                      <Eye size={19} />
                    </button>
                  ) : null}
                  <button
                    className={styles.resumeIconButton}
                    onClick={removeFile}
                    aria-label={`Remove ${resumeFilename}`}
                    type="button"
                  >
                    <X size={19} />
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div
              className={`${styles.resumeDropzone} ${phase === "uploading" ? styles.resumeUploading : ""}`}
              onClick={openFilePicker}
              onDragOver={(event) => event.preventDefault()}
              onDrop={(event) => {
                event.preventDefault();
                if (phase === "empty") {
                  chooseFile(event.dataTransfer.files.item(0));
                }
              }}
              onKeyDown={(event) => {
                if ((event.key === " " || event.key === "Enter") && phase === "empty") {
                  event.preventDefault();
                  openFilePicker();
                }
              }}
              role={phase === "empty" ? "button" : "status"}
              tabIndex={phase === "empty" ? 0 : -1}
            >
              {phase === "uploading" && selectedFile !== null ? (
                <>
                  <strong>
                    {isAnalyzing
                      ? "Analyzing your resume..."
                      : `Uploading ${selectedFile.name}...`}
                  </strong>
                  {isAnalyzing ? <span>This can take up to a minute.</span> : null}
                </>
              ) : (
                <>
                  <FileUp size={55} strokeWidth={1.8} />
                  <strong>Drag and drop your resume here</strong>
                  <span>Supported formats: PDF</span>
                  <span>Max size: 5 MB</span>
                </>
              )}
            </div>
          )}
          <input
            accept=".pdf"
            className={styles.resumeFileInput}
            onChange={(event) => chooseFile(event.target.files?.item(0) ?? null)}
            ref={inputRef}
            type="file"
          />
          <footer className={`${styles.wizardFooter} ${styles.resumeFooter}`}>
            <button className={styles.wizardSecondaryButton} onClick={onBack} type="button">Back</button>
            <button
              className={`${styles.wizardPrimaryButton} ${phase === "uploading" ? styles.uploadingButton : ""}`}
              disabled={phase !== "success"}
              onClick={onContinue}
              type="button"
            >
              {phase === "uploading" ? (
                <>
                  <span>{isAnalyzing ? "Analyzing..." : "Uploading..."}</span>
                  <LoaderCircle className={styles.uploadSpinner} size={17} />
                </>
              ) : "Continue"}
            </button>
          </footer>
        </div>
      </section>
    </div>
  );
}
