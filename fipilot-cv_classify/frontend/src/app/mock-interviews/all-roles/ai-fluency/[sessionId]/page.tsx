import { InterviewPage } from "@/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/interview";

interface InterviewRouteProps {
  params: Promise<{ sessionId: string }>;
}

export default async function AiFluencyInterviewRoute({ params }: InterviewRouteProps) {
  const { sessionId } = await params;

  return <InterviewPage sessionId={sessionId} />;
}
