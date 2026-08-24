const CLIENT_ID_STORAGE_KEY = "fipilot_client_id";

export function getAnonymousClientId() {
  const stored = localStorage.getItem(CLIENT_ID_STORAGE_KEY);
  if (stored !== null) return stored;
  const clientId = crypto.randomUUID();
  localStorage.setItem(CLIENT_ID_STORAGE_KEY, clientId);
  return clientId;
}

export function setClientId(clientId: string) {
  localStorage.setItem(CLIENT_ID_STORAGE_KEY, clientId);
}

export function clearClientId() {
  localStorage.removeItem(CLIENT_ID_STORAGE_KEY);
}
