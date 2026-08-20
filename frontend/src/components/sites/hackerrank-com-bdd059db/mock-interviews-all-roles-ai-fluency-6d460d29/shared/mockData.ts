export const AI_FLUENCY_BASE_PATH = "/mock-interviews/all-roles/ai-fluency";

export const LANDING_BENEFITS = [
  {
    icon: "document",
    title: "Focus on projects and experience",
    description:
      "Discuss your experience with AI tools, how you use AI in your work, and your understanding of AI concepts.",
  },
  {
    icon: "microphone",
    title: "A realistic, voice-based interview",
    description:
      "Build confidence by speaking naturally, just like you would in a real interview.",
  },
  {
    icon: "document",
    title: "Demonstrate AI fluency",
    description:
      "Show how you stay current with AI trends, evaluate tools, and apply AI effectively in real-world scenarios.",
  },
  {
    icon: "clipboard",
    title: "Improve with clear, actionable feedback",
    description:
      "Get specific feedback on your clarity, depth of examples, and how well you communicate your AI experience.",
  },
] as const;

export const MOCK_TRANSCRIPT = [
  {
    speaker: "interviewer",
    text: "Xin chào, rất vui được gặp bạn. Rất hoan nghênh bạn đã tham gia buổi phỏng vấn. Tôi là người phỏng vấn AI của bạn ngày hôm nay. Chúng ta sẽ lần lượt trao đổi qua từng câu hỏi một.",
  },
] as const;

export const FEEDBACK_SUMMARY =
  "The session was not completed due to lack of substantive candidate responses. The candidate provided minimal engagement throughout the interview, with only brief acknowledgments and no meaningful answers to core AI fluency questions. Without concrete examples, reasoning, or evidence of AI collaboration practices, no reliable assessment of AI fluency can be made across any dimension. To receive actionable feedback, please complete the full interview by providing detailed answers about your AI tool usage, prompting approach, mistake-catching processes, and data handling practices.";

export const FEEDBACK_DIMENSIONS = [
  {
    title: "Delegation",
    description:
      "This section was not meaningfully assessed. The candidate did not provide substantive answers about which AI tools they use, how they choose between them, or their reasoning for delegating specific tasks to AI versus handling them manually. Without concrete examples of tool selection or cost-benefit analysis, delegation fluency cannot be evaluated.",
  },
  {
    title: "Description",
    description:
      "This section was not meaningfully assessed. The candidate did not describe their prompting structure, provide examples of multi-turn refinement, or explain how they provide context to AI tools. Without evidence of systematic prompt engineering or iteration practices, description fluency cannot be evaluated.",
  },
  {
    title: "Discernment",
    description:
      "This section was not meaningfully assessed. The candidate did not share any stories about catching AI mistakes, describe their review process, or demonstrate awareness of hallucination risks and failure modes. Without concrete examples of quality assurance or mistake detection, discernment fluency cannot be evaluated.",
  },
  {
    title: "Diligence",
    description:
      "This section was not meaningfully assessed. The candidate did not articulate their position on transparency, data privacy boundaries, or ownership of AI-generated code. Without evidence of responsible AI practices or governance thinking, diligence fluency cannot be evaluated.",
  },
] as const;

export function createMockSessionId() {
  return `mock-${Date.now().toString(36)}`;
}
