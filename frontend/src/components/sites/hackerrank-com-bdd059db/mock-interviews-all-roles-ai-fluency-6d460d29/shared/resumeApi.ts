export interface ResumeProfile {
  workExperience?: Array<Record<string, unknown>>;
  education?: Array<Record<string, unknown>>;
  [key: string]: unknown;
}

export interface ResumeUploadResult {
  id?: string | null;
  filename: string;
  profile: ResumeProfile;
}

export const RESUME_PROFILE_STORAGE_KEY = "resume_profile";
export const RESUME_RESULT_STORAGE_KEY = "resume_analysis";

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
  if (!response.ok) return null;
  return response.json();
}
