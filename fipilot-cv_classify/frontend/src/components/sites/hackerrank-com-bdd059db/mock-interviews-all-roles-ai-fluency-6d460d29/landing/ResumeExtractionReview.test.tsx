import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { summarizeResumeExtraction } from "../shared/resumeApi";
import { ResumeExtractionReview } from "./ResumeExtractionReview";


describe("ResumeExtractionReview", () => {
  it("shows a complete extraction and every extracted entry", () => {
    render(
      <ResumeExtractionReview
        profile={{
          skills: ["Python", "Azure OpenAI", "FastAPI"],
          workExperience: [
            {
              type: "Work",
              name: "FiPilot",
              position: "Backend Engineer",
              jobDescription: "Built an interview API with Python and Azure OpenAI.",
            },
            {
              type: "Project",
              name: "Resume review",
              position: "",
              jobDescription: "Extracted grounded work and project evidence from PDF files.",
            },
          ],
        }}
      />,
    );

    expect(screen.getByRole("heading", { name: "Extraction looks complete" })).toBeVisible();
    expect(screen.getByText("2 items found")).toBeVisible();
    expect(screen.getByRole("heading", { name: "FiPilot" })).toBeVisible();
    expect(screen.getByRole("heading", { name: "Resume review" })).toBeVisible();
    expect(screen.getByText("Python, Azure OpenAI, FastAPI")).toBeVisible();
    expect(screen.queryByText("Check these details")).not.toBeInTheDocument();
  });

  it("lists missing fields and prevents an unusable extraction from continuing", () => {
    const profile = {
      workExperience: [
        {
          type: "Work" as const,
          name: "FiPilot",
          position: "",
          jobDescription: "",
        },
      ],
    };

    render(<ResumeExtractionReview profile={profile} />);

    expect(screen.getByRole("heading", { name: "Review missing details" })).toBeVisible();
    expect(screen.getByText("Item 1: The job title is missing.")).toBeVisible();
    expect(
      screen.getByText("Item 1: No responsibilities, achievements, or technologies were found."),
    ).toBeVisible();
    expect(summarizeResumeExtraction(profile).canContinue).toBe(false);
  });
});
