import { create } from 'zustand'

export interface PendingInterview {
  sessionId: string
  candidate: string
  role: string
  interviewer_email: string
  created_at: string // ISO timestamp khi được đưa vào hàng đợi, dùng để sắp xếp
}

// Seed: vài phiên "đang chờ" sẵn có để demo, không gắn giờ hẹn cụ thể —
// người dùng tự quyết định lúc nào bắt đầu.
const seedPending: PendingInterview[] = [
  {
    sessionId: 'sess_001',
    candidate: 'Nguyen Van A',
    role: 'AI Eng L3',
    interviewer_email: 'admin2026@gmail.com',
    created_at: '2026-06-21T08:00:00Z',
  },
  {
    sessionId: 'sess_002',
    candidate: 'Tran Thi B',
    role: 'AI Eng L2',
    interviewer_email: 'minh.tran@example.com',
    created_at: '2026-06-21T08:05:00Z',
  },
  {
    sessionId: 'sess_006',
    candidate: 'Vu Minh F',
    role: 'AI Eng L3',
    interviewer_email: 'admin2026@gmail.com',
    created_at: '2026-06-21T08:10:00Z',
  },
  {
    sessionId: 'sess_007',
    candidate: 'Do Thi G',
    role: 'AI Eng L2',
    interviewer_email: 'minh.tran@example.com',
    created_at: '2026-06-21T08:15:00Z',
  },
]

interface ScheduleState {
  pending: PendingInterview[]
  addPending: (item: PendingInterview) => void
  removePending: (sessionId: string) => void
}

export const useScheduleStore = create<ScheduleState>((set) => ({
  pending: seedPending,
  addPending: (item) => set((s) => ({ pending: [...s.pending, item] })),
  removePending: (sessionId) =>
    set((s) => ({ pending: s.pending.filter((p) => p.sessionId !== sessionId) })),
}))
