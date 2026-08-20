function getBackendUrl(): string | undefined {
  const apiUrl = process.env.RESUME_API_URL ?? process.env.NEXT_PUBLIC_RESUME_API_URL;
  if (apiUrl !== undefined) return apiUrl.replace(/\/$/, "");
  return process.env.NODE_ENV === "development" ? "http://localhost:8000" : undefined;
}

export async function GET(
  request: Request,
  context: { params: Promise<{ sessionId: string }> },
) {
  const backendUrl = getBackendUrl();
  if (backendUrl === undefined) {
    return Response.json({ detail: "Interview service is not configured" }, { status: 503 });
  }
  const clientId = new URL(request.url).searchParams.get("client_id");
  if (clientId === null) {
    return Response.json({ detail: "client_id is required" }, { status: 400 });
  }
  const { sessionId } = await context.params;
  try {
    const response = await fetch(
      `${backendUrl}/api/v1/interview/${encodeURIComponent(sessionId)}?client_id=${encodeURIComponent(clientId)}`,
      { cache: "no-store" },
    );
    return new Response(await response.arrayBuffer(), {
      headers: { "content-type": response.headers.get("content-type") ?? "application/json" },
      status: response.status,
    });
  } catch {
    return Response.json({ detail: "Interview service is unavailable" }, { status: 502 });
  }
}
