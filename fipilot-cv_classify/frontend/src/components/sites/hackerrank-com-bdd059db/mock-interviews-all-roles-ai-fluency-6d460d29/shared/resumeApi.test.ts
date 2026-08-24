import { afterEach, describe, expect, it, vi } from "vitest";
import {
  fetchLatestResume,
  focusResumeForRole,
  getResumeRoleMatches,
  type ResumeProfile,
} from "./resumeApi";

const profile: ResumeProfile = {
  skills: ["PyTorch", "FastAPI", "PostgreSQL"],
  workExperience: [
    {
      type: "Project",
      name: "Vision service",
      position: "AI Engineer",
      jobDescription: "Trained PyTorch models and served inference with FastAPI.",
    },
    {
      type: "Work",
      name: "Platform team",
      position: "Backend Engineer",
      jobDescription: "Built FastAPI services backed by PostgreSQL.",
    },
  ],
  roleMatches: [
    {
      id: "ai-engineer",
      title: "AI Engineer",
      score: 80,
      summary: "AI evidence",
      matchedSkills: ["PyTorch"],
      relevantExperienceIndexes: [0],
    },
    {
      id: "backend-developer",
      title: "Backend Developer",
      score: 20,
      summary: "Backend evidence",
      matchedSkills: ["FastAPI", "PostgreSQL"],
      relevantExperienceIndexes: [0, 1],
    },
  ],
};

describe("resume role context", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("orders role matches by resume evidence share", () => {
    expect(getResumeRoleMatches(profile).map((match) => match.score)).toEqual([80, 20]);
  });

  it("keeps only the skills and projects relevant to the selected role", () => {
    const focused = focusResumeForRole(profile, "backend-developer");

    expect(focused.skills).toEqual(["FastAPI", "PostgreSQL"]);
    expect(focused.workExperience?.map((entry) => entry.name)).toEqual([
      "Vision service",
      "Platform team",
    ]);
  });

  it("distinguishes no saved resume from a resume-service failure", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(
      JSON.stringify({ detail: "Database unavailable" }),
      { status: 503, headers: { "content-type": "application/json" } },
    )));

    await expect(fetchLatestResume()).rejects.toThrow("Database unavailable");
  });

  it("returns null only when no saved resume exists", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(
      JSON.stringify({ detail: "Resume not found" }),
      { status: 404, headers: { "content-type": "application/json" } },
    )));

    await expect(fetchLatestResume()).resolves.toBeNull();
  });

  it("allows a legitimate retry after a resume-service failure", async () => {
    const resume = { id: "resume-1", filename: "candidate.pdf", profile };
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(new Response(
        JSON.stringify({ detail: "Resume service unavailable" }),
        { status: 503, headers: { "content-type": "application/json" } },
      ))
      .mockResolvedValueOnce(new Response(
        JSON.stringify(resume),
        { status: 200, headers: { "content-type": "application/json" } },
      )));

    await expect(fetchLatestResume()).rejects.toThrow("Resume service unavailable");
    await expect(fetchLatestResume()).resolves.toEqual(resume);
  });
});
