function getBackendUrl(): string | undefined {
  const apiUrl = process.env.RESUME_API_URL ?? process.env.NEXT_PUBLIC_RESUME_API_URL;
  if (apiUrl !== undefined) return apiUrl.replace(/\/$/, "");
  return process.env.NODE_ENV === "development" ? "http://localhost:8000" : undefined;
}

export async function GET(request: Request, context: { params: Promise<{ action: string }> }) {
  return proxyAuthRequest(request, context, "GET");
}

export async function POST(request: Request, context: { params: Promise<{ action: string }> }) {
  return proxyAuthRequest(request, context, "POST");
}

async function proxyAuthRequest(
  request: Request,
  context: { params: Promise<{ action: string }> },
  method: "GET" | "POST",
) {
  const backendUrl = getBackendUrl();
  if (backendUrl === undefined) return Response.json({ detail: "Authentication service is not configured" }, { status: 503 });
  const { action } = await context.params;
  if (!["login", "register", "logout", "me"].includes(action)) {
    return Response.json({ detail: "Unknown auth action" }, { status: 404 });
  }
  const headers = new Headers();
  const cookie = request.headers.get("cookie");
  if (cookie !== null) headers.set("cookie", cookie);
  if (method === "POST") headers.set("content-type", "application/json");
  try {
    const upstream = await fetch(`${backendUrl}/api/v1/auth/${action}`, {
      method,
      headers,
      body: method === "POST" ? await request.text() : undefined,
      cache: "no-store",
    });
    const responseHeaders = new Headers({ "content-type": upstream.headers.get("content-type") ?? "application/json" });
    const setCookie = upstream.headers.get("set-cookie");
    if (setCookie !== null) responseHeaders.set("set-cookie", setCookie);
    return new Response(await upstream.arrayBuffer(), { headers: responseHeaders, status: upstream.status });
  } catch {
    return Response.json({ detail: "Authentication service is unavailable" }, { status: 502 });
  }
}
