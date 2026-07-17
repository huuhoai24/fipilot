const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface CreateSessionData {
  name: string;
  role: string;
  level: string;
  language?: string;
  template_id?: string;
  skills?: string[];
  recent_role?: string;
  years_experience?: number;
  education?: string;
}

export interface TemplateMatchData {
  role_fit: string;
  inferred_level: number;
  skills: string[];
  target_role?: string;
}

export const api = {
  createSession: async (data: CreateSessionData) => {
    const response = await fetch(`${API_URL}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'Failed to create session');
    }
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

  getSession: async (sessionId: string | number) => {
    const response = await fetch(`${API_URL}/sessions/${sessionId}`);
    if (!response.ok) throw new Error('Failed to fetch session');
    return response.json();
  },

  getReport: async (sessionId: string | number) => {
    const response = await fetch(`${API_URL}/sessions/${sessionId}/report`);
    if (!response.ok) throw new Error('Failed to fetch report');
    return response.json();
  },

  extractCv: async (file: File, parserMode: 'workflow' | 'llm' = 'workflow') => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('parser_mode', parserMode);
    const response = await fetch(`${API_URL}/cv/extract`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      const detail = error.detail;
      throw new Error(
        typeof detail === 'string'
          ? detail
          : detail?.message || 'Failed to extract CV'
      );
    }
    return response.json();
  },

  recordProctoringEvent: async (
    sessionId: string | number,
    event: {
      event_type: 'tab_hidden' | 'window_blur';
      reason?: string;
      occurred_at?: string;
      visible?: boolean;
      focus_state?: string;
    }
  ) => {
    const response = await fetch(`${API_URL}/sessions/${sessionId}/proctoring-events`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(event),
    });
    if (!response.ok) throw new Error('Failed to record proctoring event');
    return response.json();
  },

  matchTemplates: async (data: TemplateMatchData) => {
    const response = await fetch(`${API_URL}/templates/match`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || 'Failed to match templates');
    }
    return response.json();
  }
};
