const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface CreateSessionData {
  name: string;
  role: string;
  level: string;
  language?: string;
  template_id?: string;
}

export const api = {
  createSession: async (data: CreateSessionData) => {
    const response = await fetch(`${API_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create session');
    return response.json();
  },

  endSession: async (sessionId: string | number) => {
    const response = await fetch(`${API_URL}/sessions/${sessionId}/end`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to end session');
    return response.json();
  },

  getSessions: async () => {
    const response = await fetch(`${API_URL}/sessions`);
    if (!response.ok) throw new Error('Failed to fetch sessions');
    return response.json();
  },

  getReport: async (sessionId: string | number) => {
    const response = await fetch(`${API_URL}/sessions/${sessionId}/report`);
    if (!response.ok) throw new Error('Failed to fetch report');
    return response.json();
  },

  extractCv: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_URL}/cv/extract`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Failed to extract CV');
    return response.json();
  }
};
