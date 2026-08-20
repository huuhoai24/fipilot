export interface AuthUser {
  name: string;
  email: string;
}

const AUTH_STORAGE_KEY = "fipilot_auth_user";
export const AUTH_CHANGE_EVENT = "fipilot-auth-change";

export function getAuthUser(): AuthUser | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(AUTH_STORAGE_KEY);
  if (raw === null) return null;
  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    localStorage.removeItem(AUTH_STORAGE_KEY);
    return null;
  }
}

export function setAuthUser(user: AuthUser) {
  localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(user));
  window.dispatchEvent(new Event(AUTH_CHANGE_EVENT));
}

export function clearAuthUser() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  localStorage.removeItem("fipilot_client_id");
  localStorage.removeItem("resume_analysis");
  sessionStorage.removeItem("resume_profile");
  window.dispatchEvent(new Event(AUTH_CHANGE_EVENT));
}

export async function registerUser(fullName: string, email: string, password: string) {
  // Clear any existing anonymous/old account data before registering
  localStorage.removeItem("fipilot_client_id");
  localStorage.removeItem("resume_analysis");
  sessionStorage.removeItem("resume_profile");

  const response = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ full_name: fullName, email, password }),
  });
  const body = await response.json().catch(() => null) as AuthUser | { detail?: string } | null;
  if (!response.ok) throw new Error(body && "detail" in body ? body.detail : "Registration failed");
  setAuthUser(body as AuthUser);
  return body as AuthUser;
}

export async function loginUser(identifier: string, password: string) {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ identifier, password }),
  });
  const body = await response.json().catch(() => null) as AuthUser | { detail?: string } | null;
  if (!response.ok) throw new Error(body && "detail" in body ? body.detail : "Login failed");
  setAuthUser(body as AuthUser);
  return body as AuthUser;
}

export async function logoutUser() {
  await fetch("/api/auth/logout", { method: "POST" }).catch(() => undefined);
  clearAuthUser();
}

export async function hydrateAuthUser() {
  try {
    const response = await fetch("/api/auth/me", { cache: "no-store" });
    if (!response.ok) {
      clearAuthUser();
      return null;
    }
    const user = await response.json() as AuthUser;
    setAuthUser(user);
    return user;
  } catch {
    return getAuthUser();
  }
}
