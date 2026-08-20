"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { ClipboardCheck, FileText, Mic } from "lucide-react";
import {
  preloadInterviewGreeting,
} from "../shared/greetingAudio";
import {
  createInterviewSetup,
  loadInterviewSetup,
  prepareInterviewQuestions,
  saveInterviewSetup,
} from "../shared/interviewApi";
import {
  AI_FLUENCY_BASE_PATH,
  createMockSessionId,
  LANDING_BENEFITS,
} from "../shared/mockData";
import {
  RESUME_PROFILE_STORAGE_KEY,
  loadResumeAnalysis,
  type ResumeProfile,
} from "../shared/resumeApi";
import { AppHeader } from "./AppHeader";
import { DeviceSettingsDialog } from "./DeviceSettingsDialog";
import {
  InterviewExperienceDialog,
  type ExperienceLevel,
  type InterviewRoleId,
  INTERVIEW_ROLES,
} from "./InterviewExperienceDialog";
import { PreviewHero } from "./PreviewHero";
import { ResumeUploadStep } from "./ResumeUploadStep";
import { AuthDialog, type AuthMode } from "../../../www.hackerrank.com-407abdb8/dashboard-89347bb2/AuthDialog";
import { getAuthUser } from "@/lib/auth";
import styles from "./landing.module.css";

const benefitIcons = {
  document: FileText,
  microphone: Mic,
  clipboard: ClipboardCheck,
} as const;

export function LandingPage() {
  const router = useRouter();
  const [setupStep, setSetupStep] = useState<"experience" | "resume" | "device" | null>(null);
  const [selectedRole, setSelectedRole] = useState<InterviewRoleId | null>(null);
  const [selectedExperienceLevel, setSelectedExperienceLevel] = useState<ExperienceLevel | null>(null);
  const [customDescription, setCustomDescription] = useState("");
  const [, setResume] = useState<File | null>(null);
  const [authMode, setAuthMode] = useState<AuthMode | null>(null);

  useEffect(() => {
    preloadInterviewGreeting();
  }, []);

  function handleStartTrial() {
    const currentUser = getAuthUser();
    if (currentUser === null) {
      setAuthMode("login");
      return;
    }
    setSetupStep("experience");
  }

  function startInterview() {
    const setup = loadInterviewSetup();
    if (setup !== null) router.push(`${AI_FLUENCY_BASE_PATH}/${setup.sessionId}`);
  }

  function continueToDeviceSettings() {
    if (selectedRole === null || selectedExperienceLevel === null) return;
    const storedProfile = sessionStorage.getItem(RESUME_PROFILE_STORAGE_KEY);
    if (storedProfile === null) return;

    const profile = JSON.parse(storedProfile) as ResumeProfile;
    const role = INTERVIEW_ROLES.find((option) => option.id === selectedRole)?.title;
    if (role === undefined) return;

    const setup = createInterviewSetup(
      createMockSessionId(),
      loadResumeAnalysis()?.id ?? null,
      role,
      selectedExperienceLevel,
      customDescription,
      profile,
    );
    saveInterviewSetup(setup);
    void prepareInterviewQuestions(setup).catch(() => undefined);
    setSetupStep("device");
  }

  function closeSetup() {
    setSetupStep(null);
    setSelectedRole(null);
    setSelectedExperienceLevel(null);
    setCustomDescription("");
    setResume(null);
  }

  function returnToExperience() {
    setSelectedRole(null);
    setSelectedExperienceLevel(null);
    setCustomDescription("");
    setSetupStep("experience");
  }

  return (
    <div className={styles.root}>
      <AppHeader />
      <main className={styles.landingMain}>
        <div className={styles.decoration} aria-hidden="true" />
        <section className={styles.landingContent}>
          <h1>AI Fluency</h1>
          <p className={styles.subtitle}>Practice with AI-powered voice interviews</p>
          
          <div className={styles.benefits}>
            {LANDING_BENEFITS.map((benefit) => {
              const Icon = benefitIcons[benefit.icon];
              return (
                <article className={styles.benefit} key={benefit.title}>
                  <Icon size={18} />
                  <div>
                    <h2>{benefit.title}</h2>
                    <p>{benefit.description}</p>
                  </div>
                </article>
              );
            })}
          </div>
          <button className={styles.cta} onClick={handleStartTrial} type="button">
            Try for free
          </button>
        </section>
        <PreviewHero />
      </main>
      {authMode !== null ? (
        <AuthDialog initialMode={authMode} onClose={() => setAuthMode(null)} />
      ) : null}
      {setupStep === "experience" ? (
        <InterviewExperienceDialog
          customDescription={customDescription}
          onCancel={closeSetup}
          onContinue={() => setSetupStep("resume")}
          onCustomDescriptionChange={setCustomDescription}
          onExperienceLevelChange={setSelectedExperienceLevel}
          onRoleChange={setSelectedRole}
          selectedExperienceLevel={selectedExperienceLevel}
          selectedRole={selectedRole}
        />
      ) : null}
      {setupStep === "resume" ? (
        <ResumeUploadStep
          onBack={returnToExperience}
          onContinue={continueToDeviceSettings}
          onFileChange={setResume}
        />
      ) : null}
      {setupStep === "device" ? (
        <DeviceSettingsDialog onBack={() => setSetupStep("resume")} onStart={startInterview} />
      ) : null}
    </div>
  );
}
