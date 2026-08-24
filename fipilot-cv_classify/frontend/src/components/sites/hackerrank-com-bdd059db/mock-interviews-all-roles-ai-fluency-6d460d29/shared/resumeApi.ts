export interface ResumeExperience {
  type: "Work" | "Project";
  name: string;
  position: string;
  jobDescription: string;
}

export interface ResumeRoleMatch {
  id: string;
  title: string;
  score: number;
  summary: string;
  matchedSkills: string[];
  relevantExperienceIndexes: number[];
}

export interface ResumeProfile {
  workExperience?: ResumeExperience[];
  skills?: string[];
  roleMatches?: ResumeRoleMatch[];
  education?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export function getResumeRoleMatches(profile: ResumeProfile): ResumeRoleMatch[] {
  if (!Array.isArray(profile.roleMatches)) return [];
  return profile.roleMatches
    .filter((match) => (
      typeof match?.id === "string"
      && typeof match.title === "string"
      && Number.isInteger(match.score)
      && match.score > 0
      && Array.isArray(match.matchedSkills)
      && Array.isArray(match.relevantExperienceIndexes)
    ))
    .sort((left, right) => right.score - left.score);
}

export function focusResumeForRole(
  profile: ResumeProfile,
  roleId: string,
): ResumeProfile {
  const match = getResumeRoleMatches(profile).find((item) => item.id === roleId);
  if (match === undefined) return profile;
  const entries = Array.isArray(profile.workExperience) ? profile.workExperience : [];
  return {
    ...profile,
    skills: match.matchedSkills,
    workExperience: match.relevantExperienceIndexes
      .map((index) => entries[index])
      .filter((entry): entry is ResumeExperience => entry !== undefined),
  };
}

export interface ResumeExtractionIssue {
  entryIndex: number | null;
  message: string;
}

export interface ResumeExtractionSummary {
  canContinue: boolean;
  entries: ResumeExperience[];
  issues: ResumeExtractionIssue[];
  isComplete: boolean;
  projectCount: number;
  workCount: number;
}

export interface ResumeUploadResult {
  id?: string | null;
  filename: string;
  profile: ResumeProfile;
}

export const RESUME_PROFILE_STORAGE_KEY = "resume_profile";
export const RESUME_RESULT_STORAGE_KEY = "resume_analysis";

function cleanText(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

export function summarizeResumeExtraction(
  profile: ResumeProfile,
): ResumeExtractionSummary {
  const rawEntries = Array.isArray(profile.workExperience)
    ? profile.workExperience
    : [];
  const entries: ResumeExperience[] = rawEntries.map((entry) => ({
    type: entry?.type === "Project" ? "Project" : "Work",
    name: cleanText(entry?.name),
    position: cleanText(entry?.position),
    jobDescription: cleanText(entry?.jobDescription),
  }));
  const issues: ResumeExtractionIssue[] = [];

  if (entries.length === 0) {
    issues.push({
      entryIndex: null,
      message: "No work experience or projects were extracted.",
    });
  }

  entries.forEach((entry, entryIndex) => {
    if (!entry.name) {
      issues.push({ entryIndex, message: "The company or project name is missing." });
    }
    if (entry.type === "Work" && !entry.position) {
      issues.push({ entryIndex, message: "The job title is missing." });
    }
    if (!entry.jobDescription) {
      issues.push({
        entryIndex,
        message: "No responsibilities, achievements, or technologies were found.",
      });
    }
  });

  return {
    canContinue: entries.some((entry) => Boolean(entry.name && entry.jobDescription)),
    entries,
    issues,
    isComplete: entries.length > 0 && issues.length === 0,
    projectCount: entries.filter((entry) => entry.type === "Project").length,
    workCount: entries.filter((entry) => entry.type === "Work").length,
  };
}

export function saveResumeAnalysis(result: ResumeUploadResult) {
  localStorage.setItem(RESUME_RESULT_STORAGE_KEY, JSON.stringify(result));
  sessionStorage.setItem(RESUME_PROFILE_STORAGE_KEY, JSON.stringify(result.profile));
}

export function loadResumeAnalysis(): ResumeUploadResult | null {
  if (typeof window === "undefined") return null;
  const storedResult = localStorage.getItem(RESUME_RESULT_STORAGE_KEY);
  if (storedResult === null) return null;
  try {
    return JSON.parse(storedResult) as ResumeUploadResult;
  } catch {
    localStorage.removeItem(RESUME_RESULT_STORAGE_KEY);
    return null;
  }
}

export function clearResumeAnalysis() {
  localStorage.removeItem(RESUME_RESULT_STORAGE_KEY);
  sessionStorage.removeItem(RESUME_PROFILE_STORAGE_KEY);
}

export async function uploadResume(file: File): Promise<ResumeUploadResult> {
  const { getAnonymousClientId } = await import("./clientIdentity");
  const formData = new FormData();
  formData.append("file", file);
  formData.append("client_id", getAnonymousClientId());

  const response = await fetch("/api/resume/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    throw new Error(body?.detail ?? `Upload failed (HTTP ${response.status})`);
  }

  return response.json();
}

export async function fetchLatestResume(): Promise<ResumeUploadResult | null> {
  const { getAnonymousClientId } = await import("./clientIdentity");
  const response = await fetch(
    `/api/resume/latest?client_id=${encodeURIComponent(getAnonymousClientId())}`,
    { cache: "no-store" },
  );
  if (response.status === 404) return null;
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    throw new Error(body?.detail ?? `Resume lookup failed (HTTP ${response.status})`);
  }
  return response.json();
}
