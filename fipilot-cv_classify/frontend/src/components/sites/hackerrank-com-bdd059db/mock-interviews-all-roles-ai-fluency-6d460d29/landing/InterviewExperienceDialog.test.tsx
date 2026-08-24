import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { INTERVIEW_ROLES, InterviewExperienceDialog } from "./InterviewExperienceDialog";

const profile = {
  skills: ["PyTorch", "FastAPI", "PostgreSQL"],
  workExperience: [
    {
      type: "Project" as const,
      name: "AI search",
      position: "AI Engineer",
      jobDescription: "Built a PyTorch retrieval model.",
    },
    {
      type: "Work" as const,
      name: "Platform API",
      position: "Backend Engineer",
      jobDescription: "Built FastAPI and PostgreSQL services.",
    },
  ],
  roleMatches: [
    {
      id: "ai-engineer",
      title: "AI Engineer",
      score: 80,
      summary: "2 matched skills and 1 relevant experience item",
      matchedSkills: ["PyTorch"],
      relevantExperienceIndexes: [0],
    },
    {
      id: "backend-developer",
      title: "Backend Developer",
      score: 20,
      summary: "2 matched skills and 1 relevant experience item",
      matchedSkills: ["FastAPI", "PostgreSQL"],
      relevantExperienceIndexes: [1],
    },
  ],
};

describe("InterviewExperienceDialog", () => {
  it("supports every role backed by a knowledge domain", () => {
    expect(INTERVIEW_ROLES.filter((role) => role.id !== "custom").map((role) => role.title)).toEqual([
      "AI Engineer",
      "Backend Developer",
      "Business Analyst",
      "Data Engineer",
      "Data Scientist",
      "DevOps Engineer",
      "Full Stack Developer",
      "Software Engineer",
      "Tester QA QC",
      "Web Developer",
    ]);
  });

  it("shows resume-derived role shares instead of every generic role", () => {
    render(
      <InterviewExperienceDialog
        customDescription=""
        onCancel={vi.fn()}
        onContinue={vi.fn()}
        onCustomDescriptionChange={vi.fn()}
        onExperienceLevelChange={vi.fn()}
        onRoleChange={vi.fn()}
        profile={profile}
        selectedExperienceLevel={null}
        selectedRole={null}
      />,
    );

    expect(screen.getByText("80%")).toBeVisible();
    expect(screen.getByText("20%")).toBeVisible();
    expect(screen.queryByText("Frontend Developer")).not.toBeInTheDocument();
  });

  it("shows the skills and experience that will drive the selected interview", () => {
    const onLevelChange = vi.fn();
    render(
      <InterviewExperienceDialog
        customDescription=""
        onCancel={vi.fn()}
        onContinue={vi.fn()}
        onCustomDescriptionChange={vi.fn()}
        onExperienceLevelChange={onLevelChange}
        onRoleChange={vi.fn()}
        profile={profile}
        selectedExperienceLevel={null}
        selectedRole="backend-developer"
      />,
    );

    expect(screen.getByRole("heading", { name: "Interview context for Backend Developer" })).toBeVisible();
    expect(screen.getByText("FastAPI, PostgreSQL")).toBeVisible();
    expect(screen.getByText("Platform API")).toBeVisible();
    fireEvent.click(screen.getByLabelText("Junior"));
    expect(onLevelChange).toHaveBeenCalledWith("Junior");
  });
});
