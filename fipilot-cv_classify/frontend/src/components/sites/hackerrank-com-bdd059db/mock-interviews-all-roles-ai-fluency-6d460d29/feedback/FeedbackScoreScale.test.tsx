import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { InterviewReport } from "../shared/interviewApi";
import { FeedbackAssessmentCard } from "./FeedbackAssessmentCard";
import { FeedbackSummarySidebar } from "./FeedbackSummarySidebar";

describe("feedback 0-10 score scale", () => {
  it("renders an assessed turn on the canonical scale", () => {
    render(
      <FeedbackAssessmentCard
        description="Strong answer"
        evidence={["Relevant evidence"]}
        score={8}
        status="MET"
        title="Technical depth"
      />,
    );

    expect(screen.getByText(/8\/10/)).toBeVisible();
    expect(screen.queryByText(/8\/3/)).not.toBeInTheDocument();
  });

  it("distinguishes a missing evaluation from a real zero", () => {
    render(
      <FeedbackAssessmentCard
        description="No evaluation available"
        evidence={[]}
        score={null}
        status="NOT_ASSESSED"
        title="Technical depth"
      />,
    );

    expect(screen.getByText(/Not assessed/)).toBeVisible();
  });

  it("renders the report aggregate on the canonical scale", () => {
    const report: InterviewReport = {
      assessments: [],
      coverage_ratio: 1,
      normalized_score: 8.5,
      overall_assessment: "Strong",
      recommendations: "Continue",
      score_scale: 10,
      solutions_summary: "Clear solution",
    };

    render(<FeedbackSummarySidebar report={report} />);

    expect(screen.getByText("8.50/10")).toBeVisible();
    expect(screen.queryByText("8.50/5")).not.toBeInTheDocument();
  });
});
