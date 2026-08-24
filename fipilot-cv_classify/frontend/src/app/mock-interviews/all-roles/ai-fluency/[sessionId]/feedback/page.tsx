import { FeedbackPage } from "@/components/sites/hackerrank-com-bdd059db/mock-interviews-all-roles-ai-fluency-6d460d29/feedback";

interface FeedbackRouteProps {
  params: Promise<{ sessionId: string }>;
}

export default async function AiFluencyFeedbackRoute({ params }: FeedbackRouteProps) {
  const { sessionId } = await params;

  return <FeedbackPage sessionId={sessionId} />;
}
