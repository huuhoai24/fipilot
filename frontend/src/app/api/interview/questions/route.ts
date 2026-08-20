const REQUEST_TIMEOUT_MS = 65_000;

function getBackendUrl(): string | undefined {
  const apiUrl = process.env.RESUME_API_URL ?? process.env.NEXT_PUBLIC_RESUME_API_URL;
  if (apiUrl !== undefined) return apiUrl.replace(/\/$/, "");
  return process.env.NODE_ENV === "development" ? "http://localhost:8000" : undefined;
}

export async function POST(request: Request) {
  const backendUrl = getBackendUrl();
  if (backendUrl === undefined) {
    return Response.json({ detail: "Interview service is not configured" }, { status: 503 });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(`${backendUrl}/api/v1/interview/questions`, {
      method: "POST",
      body: await request.text(),
      headers: { "content-type": "application/json" },
      signal: controller.signal,
    });
    return new Response(await response.arrayBuffer(), {
      headers: { "content-type": response.headers.get("content-type") ?? "application/json" },
      status: response.status,
    });
  } catch {
    return Response.json({ detail: "Interview service is unavailable" }, { status: 502 });
  } finally {
    clearTimeout(timeout);
  }
}
