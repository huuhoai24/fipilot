const REQUEST_TIMEOUT_MS = 75_000;

function getResumeApiUrl(): string | undefined {
  const apiUrl = process.env.RESUME_API_URL ?? process.env.NEXT_PUBLIC_RESUME_API_URL;
  if (apiUrl !== undefined) {
    return apiUrl.replace(/\/$/, "");
  }

  return process.env.NODE_ENV === "development" ? "http://localhost:8000" : undefined;
}

export async function POST(request: Request) {
  const apiUrl = getResumeApiUrl();
  if (apiUrl === undefined) {
    return Response.json(
      { detail: "Resume service is not configured" },
      { status: 503 },
    );
  }

  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), REQUEST_TIMEOUT_MS);

  try {
    const upstreamResponse = await fetch(`${apiUrl}/api/v1/resume/upload`, {
      method: "POST",
      body: await request.formData(),
      signal: abortController.signal,
    });
    const contentType = upstreamResponse.headers.get("content-type") ?? "application/json";

    return new Response(await upstreamResponse.arrayBuffer(), {
      headers: { "content-type": contentType },
      status: upstreamResponse.status,
    });
  } catch (error) {
    const detail = error instanceof Error && error.name === "AbortError"
      ? "Resume analysis timed out"
      : "Resume service is unavailable";
    return Response.json({ detail }, { status: 502 });
  } finally {
    clearTimeout(timeout);
  }
}
