const REQUEST_TIMEOUT_MS = 90_000;

function getBackendUrl(): string | undefined {
  const apiUrl = process.env.RESUME_API_URL ?? process.env.NEXT_PUBLIC_RESUME_API_URL;
  if (apiUrl !== undefined) return apiUrl.replace(/\/$/, "");
  return process.env.NODE_ENV === "development" ? "http://localhost:8000" : undefined;
}

export async function POST(request: Request) {
  const backendUrl = getBackendUrl();
  if (backendUrl === undefined) {
    return Response.json({ detail: "Speech service is not configured" }, { status: 503 });
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(`${backendUrl}/api/v1/speech/recognize`, {
      method: "POST",
      body: await request.formData(),
      signal: controller.signal,
    });
    return new Response(await response.arrayBuffer(), {
      headers: { "content-type": response.headers.get("content-type") ?? "application/json" },
      status: response.status,
    });
  } catch (error) {
    const detail = error instanceof Error && error.name === "AbortError"
      ? "Speech recognition timed out"
      : "Speech service is unavailable";
    return Response.json({ detail }, { status: 502 });
  } finally {
    clearTimeout(timeout);
  }
}
