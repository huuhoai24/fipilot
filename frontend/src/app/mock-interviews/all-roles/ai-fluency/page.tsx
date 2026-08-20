import type { Metadata } from "next";

import { LandingPage } from "@/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/landing";

export const metadata: Metadata = {
  title: "AI Fluency Mock Interview Practice | Fipilot",
  description:
    "Practice a real AI Fluency interview with Fipilot's AI interviewer. Discuss your experience with AI tools, how you use AI in your work, and your understanding of AI concepts. Get personalized feedback to improve your interview performance.",
};

export default function AiFluencyLandingRoute() {
  return <LandingPage />;
}
